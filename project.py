import re
import imaplib
import email
from email.header import decode_header
import os
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv



class Subscription:

    def __init__(self, service, cost, date):
        self.service = service
        self.cost = float(cost)
        self.date = date

    def __str__(self):
        return f"{self.service}: ${self.cost:.2f} on {self.date}"



def parse_price(text):
    
    match = re.search(r"\$(\d+\.\d{2})", text)
    if match:
        return match.group(1)
    return None



def connect_to_email():
    # Force the code to look for your specific filename
    load_dotenv("credentials.env") 
    
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(user, password)
        return mail
    except Exception as e:
        # This will now show the REAL error if one occurs
        st.error(f"IMAP Error: {e}") 
        return None



def get_email_body(msg):
    """Extracts the plain text body safely from an email."""
    if msg.is_multipart():
        for part in msg.walk():
            # Only look for the plain text part of the email
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                # 'ignore' skips characters that cause the crash
                return payload.decode(errors='ignore')
    else:
        payload = msg.get_payload(decode=True)
        return payload.decode(errors='ignore')
    return ""

def scan_for_subscriptions(mail, sender):
    mail.select("inbox")
    status, data = mail.search(None, f'FROM "{sender}"')
    
    found_subs = []
    # Keywords that indicate an actual transaction
    transaction_keywords = ["receipt", "invoice", "charged", "confirmation", "billing"]

    for num in data[0].split():
        status, msg_data = mail.fetch(num, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = msg.get("Subject", "").lower()
                body = get_email_body(msg).lower()
                
                # Only proceed if a keyword is found in the subject or body
                if any(word in subject or word in body for word in transaction_keywords):
                    price = parse_price(body)
                    if price:
                        date = msg.get("Date")
                        found_subs.append(Subscription(sender, price, date))
    return found_subs




def build_dashboard(subs_list):

    st.set_page_config(page_title="Subscription Manager", layout="wide")
    st.title("💳 My Subscription Manager")
    
    if not subs_list:
        st.warning("No subscriptions found yet. Try scanning your inbox!")
        return

    # 1. Convert objects to a DataFrame for easy graphing
    data = {
        "Service": [s.service for s in subs_list],
        "Cost": [s.cost for s in subs_list],
        "Date": [s.date for s in subs_list]
    }
    df = pd.DataFrame(data)

    # 2. Display Key Metrics
    total_spend = df["Cost"].sum()
    col1, col2 = st.columns(2)
    col1.metric("Total Monthly Spend", f"${total_spend:.2f}")
    col2.metric("Total Active Services", len(df))

    # 3. Create a Spending Chart
    st.subheader("Spending by Service")
    fig = px.pie(df, values='Cost', names='Service', hole=0.4)
    st.plotly_chart(fig)

    # 4. Display the raw table
    st.subheader("All Detected Subscriptions")
    st.dataframe(df.sort_values(by="Cost", ascending=False), use_container_width=True)




def main():

    load_dotenv()

    # Create a button so we don't scan every time the page refreshes
    if st.sidebar.button("🚀 Start Email Scan"):
        mail = connect_to_email()
        if not mail:
            st.error("Authentication failed. Check your .env file!")
            return

        services = ["netflix.com", "spotify.com", "apple.com", "amazon.com"]
        all_subs = []
        
        with st.spinner("Analyzing receipts..."):
            for service in services:
                all_subs.extend(scan_for_subscriptions(mail, service))
        
        # Save results to session state so they stay on screen
        st.session_state['subs'] = all_subs
        mail.logout()
        st.success("Scan Complete!")

    # Display the dashboard if we have data
    if 'subs' in st.session_state:
        build_dashboard(st.session_state['subs'])
    else:
        st.info("Click the button in the sidebar to begin.")

if __name__ == "__main__":
    main()