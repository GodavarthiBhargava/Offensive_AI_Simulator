# Email Configuration Template
# 
# INSTRUCTIONS:
# 1. Copy this file and rename it to: email_config.py
# 2. Follow the setup guide in EMAIL_SETUP_GUIDE.md
# 3. Replace the values below with your actual credentials
# 4. Save the file
#
# For Gmail App Password setup:
# Visit: https://myaccount.google.com/apppasswords
#

SENDER_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_16_char_app_password"

# SMTP Settings (Default for Gmail - Don't change unless using different provider)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# ⚠️ SECURITY WARNING:
# - Never share this file or commit it to version control
# - Keep your App Password secure
# - Use App Passwords, NOT your actual Gmail password
# - This file is already in .gitignore for your protection
