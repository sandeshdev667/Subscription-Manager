import imaplib
import os
from dotenv import load_dotenv

load_dotenv("credentials.env") # Use your specific filename here
user = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")

print(f"Testing login for: {user}")
try:
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(user, password)
    print("✅ SUCCESS: Connection working!")
    mail.logout()
except Exception as e:
    print(f"❌ FAILED: {e}")