💳 Subscription Manager
Video Demo: <[Insert your YouTube/Streamlit link here]>
Description:
A "high-end" personal finance tool built with Python that automatically identifies and tracks monthly subscriptions by scanning your email inboxes. Instead of manually checking bank statements, this app uses IMAP automation and Regular Expressions to find digital receipts from services like Netflix, Spotify, Amazon, and more.

The data is then visualized in a professional Streamlit web dashboard, providing insights into your "Monthly Burn Rate" and spending distribution.

🚀 Key Features
Multi-Account Scanning: Connects to multiple Gmail accounts via secure IMAP.

Regex-Powered Extraction: Uses advanced Regular Expressions to pull precise dollar amounts from messy email bodies.

Smart Filtering: Implements keyword-based validation to distinguish between actual transaction receipts and promotional marketing offers.

Interactive Dashboard: Displays spending metrics, pie charts, and searchable data tables using Streamlit and Plotly.

Security First: Utilizes .env files and Google App Passwords to ensure user credentials are never hardcoded or pushed to GitHub.

🛠️ Project Structure
project.py: The main application containing the email scraping logic, the Subscription class, and the Streamlit UI code.

test_project.py: Contains pytest functions to verify the accuracy of the price parsing and data cleaning logic.

requirements.txt: Lists all necessary Python libraries (Streamlit, Pandas, Plotly, etc.).

.env: (Excluded from Git) Stores sensitive credentials like EMAIL_USER and EMAIL_PASS.

.gitignore: Prevents sensitive configuration files from being uploaded to public repositories.

💻 Installation & Usage
Clone the Repository:

git clone https://github.com/yourusername/subscription-manager.git


cd subscription-manager

Install Dependencies:

pip install -r requirements.txt

Configure Credentials: Create a .env file and add your Gmail address and 16-character App Password.

Run the App:

streamlit run project.py

🧪 Testing
To ensure the parsing logic is robust against different email formats, run the included tests:

pytest test_project.py

📚 Technical References
This project was built using concepts from the following specialized resources:

Automate the Boring Stuff with Python: Guided the implementation of the imaplib email automation.

Streamlit for Data Science: Provided the framework for the real-time web dashboard.
