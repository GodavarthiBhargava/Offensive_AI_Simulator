# 🔐 Two-Factor Authentication (2FA) Setup Guide

## Overview

SECURENETRA now includes **Two-Factor Authentication (2FA)** for enhanced security. Users must verify their email with an OTP (One-Time Password) during signup and login.

---

## 📧 Email Configuration Setup

### Step 1: Get Gmail App Password

1. **Go to Google Account Security**
   - Visit: https://myaccount.google.com/security

2. **Enable 2-Step Verification**
   - Click on "2-Step Verification"
   - Follow the setup process

3. **Generate App Password**
   - Visit: https://myaccount.google.com/apppasswords
   - Select "Mail" as the app
   - Select "Windows Computer" as the device
   - Click "Generate"
   - **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

### Step 2: Configure email_config.py

1. Open `email_config.py` in the project root
2. Replace the placeholder values:

```python
SENDER_EMAIL = "youremail@gmail.com"  # Your Gmail address
APP_PASSWORD = "abcdefghijklmnop"     # Your 16-char App Password (no spaces)
```

3. Save the file

---

## 🚀 Authentication Flow

### 1️⃣ Signup Process

```
User enters Email & Password
         ↓
System creates account
         ↓
OTP sent to Email (6-digit code)
         ↓
User enters OTP
         ↓
Account verified ✅
         ↓
Access granted to modules
```

### 2️⃣ Login Process

```
User enters Email & Password
         ↓
System verifies credentials
         ↓
OTP sent to Email (6-digit code)
         ↓
User enters OTP
         ↓
Login successful ✅
         ↓
Access granted to modules
```

---

## 🔒 Security Features

### OTP Security
- ✅ **6-digit random code** (100,000 - 999,999)
- ✅ **5-minute expiration** - OTP expires after 5 minutes
- ✅ **Single-use** - OTP cleared after verification
- ✅ **Email-specific** - OTP tied to specific email address

### Password Security
- ✅ **SHA-256 hashing** - Passwords never stored in plain text
- ✅ **Minimum 6 characters** - Enforced password length
- ✅ **Unique emails** - No duplicate accounts

### Database Security
- ✅ **SQLite local storage** - Data stored in `cases/users.db`
- ✅ **Verified flag** - Tracks account verification status
- ✅ **No plain passwords** - Only hashed passwords stored

---

## 📊 Database Schema

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    verified INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
```

---

## 🎯 User Experience

### Login Screen
- Email input field
- Password input field (masked)
- "LOGIN WITH OTP" button
- Link to signup page

### Signup Screen
- Email input field
- Password input field (masked)
- Confirm password field (masked)
- "SIGN UP WITH OTP" button
- Link to login page

### OTP Verification Screen
- Shows email where OTP was sent
- 6-digit OTP input field
- "VERIFY OTP" button
- "Resend OTP" link
- 5-minute countdown indicator

---

## ⚠️ Troubleshooting

### "Email configuration not found"
**Solution:** Create `email_config.py` in the project root with your credentials

### "Please configure email_config.py"
**Solution:** Replace placeholder values with your actual Gmail and App Password

### "Failed to send OTP: Authentication failed"
**Solution:** 
- Verify your Gmail address is correct
- Ensure 2-Step Verification is enabled
- Generate a new App Password
- Remove spaces from App Password

### "OTP expired"
**Solution:** Click "Resend OTP" to get a new code

### "Invalid OTP"
**Solution:** 
- Check your email for the latest OTP
- Ensure you're entering all 6 digits
- Request a new OTP if needed

---

## 🛡️ Best Practices

### For Developers
1. **Never commit `email_config.py`** to version control
2. Add `email_config.py` to `.gitignore`
3. Use environment variables for production
4. Implement rate limiting for OTP requests
5. Log authentication attempts

### For Users
1. Use a **strong password** (12+ characters)
2. Don't share your OTP with anyone
3. Check OTP expiration time
4. Use a valid email address you can access
5. Keep your account credentials secure

---

## 📁 File Structure

```
Offensive_AI_Simulator/
│
├── backend/
│   └── authentication.py       # Authentication logic
│
├── ui/
│   └── authentication_ui.py    # Login/Signup UI
│
├── cases/
│   └── users.db               # User database (auto-created)
│
├── email_config.py            # Email configuration (user creates)
├── EMAIL_SETUP_GUIDE.md       # This file
└── main.py                    # Entry point with auth flow
```

---

## 🔄 Application Flow

```
Application Start
      ↓
Splash Screen (3.5s)
      ↓
Authentication Screen
      ↓
Login/Signup
      ↓
OTP Verification
      ↓
Welcome Screen (Case Selection)
      ↓
Dashboard (Modules)
```

---

## 💡 Technical Implementation

### OTP Generation
```python
def generate_otp():
    return str(random.randint(100000, 999999))
```

### Password Hashing
```python
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
```

### OTP Expiration Check
```python
if time.time() - otp_timestamp > 300:  # 5 minutes
    return False, "OTP expired"
```

---

## 📞 Support

For issues or questions:
- Check this guide first
- Review error messages carefully
- Verify email configuration
- Test with a different email if needed

---

## ✅ Quick Start Checklist

- [ ] Enable Gmail 2-Step Verification
- [ ] Generate Gmail App Password
- [ ] Create `email_config.py`
- [ ] Add your email and App Password
- [ ] Save the file
- [ ] Run the application
- [ ] Test signup with your email
- [ ] Check email for OTP
- [ ] Verify OTP
- [ ] Access granted! 🎉

---

**Remember: Keep your credentials secure and never share your App Password!** 🔐
