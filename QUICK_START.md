# 🚀 Quick Start Guide - SECURENETRA

## Get Started in 5 Minutes!

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Email (2FA Required)

#### Option A: Copy Template
```bash
copy email_config_template.py email_config.py
```

#### Option B: Create Manually
Create `email_config.py` with:
```python
SENDER_EMAIL = "youremail@gmail.com"
APP_PASSWORD = "your16charpassword"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
```

### Step 3: Get Gmail App Password

1. **Visit:** https://myaccount.google.com/apppasswords
2. **Select:** Mail + Windows Computer
3. **Copy:** 16-character password (remove spaces)
4. **Paste:** Into `email_config.py`

### Step 4: Run Application
```bash
python main.py
```

### Step 5: Create Account

1. Click **"Sign Up"**
2. Enter your email and password
3. Check your email for OTP
4. Enter 6-digit OTP
5. Account verified! ✅

### Step 6: Start Using Modules

1. Create a new case
2. Select any module from sidebar
3. Start testing!

---

## 🎯 First Time User Flow

```
Run Application
    ↓
Splash Screen (3.5s)
    ↓
Sign Up Screen
    ↓
Enter Email & Password
    ↓
Check Email for OTP
    ↓
Enter OTP Code
    ↓
Account Verified ✅
    ↓
Create New Case
    ↓
Access All 8 Modules
```

---

## 📧 Email Configuration Example

```python
# email_config.py
SENDER_EMAIL = "john.doe@gmail.com"
APP_PASSWORD = "abcdefghijklmnop"  # 16 chars, no spaces
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
```

---

## ⚡ Quick Tips

- ✅ Use a real email you can access
- ✅ OTP expires in 5 minutes
- ✅ Click "Resend OTP" if needed
- ✅ Password must be 6+ characters
- ✅ Keep `email_config.py` secure

---

## 🆘 Troubleshooting

### "Email configuration not found"
**Fix:** Create `email_config.py` from template

### "Authentication failed"
**Fix:** Generate new Gmail App Password

### "OTP expired"
**Fix:** Click "Resend OTP" button

---

## 📚 Need More Help?

- 📖 Read [EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md)
- 📖 Read [README.md](README.md)

---

**Ready to go! Start exploring cybersecurity simulations! 🛡️**
