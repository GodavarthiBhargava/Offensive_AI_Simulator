# 🛡️ Offensive AI Simulator (SECURENETRA)

## 📋 Project Description

**Offensive AI Simulator** is a comprehensive educational desktop cybersecurity simulation tool designed for college students and security professionals to understand password security, phishing attacks, domain verification, and defensive strategies. This is a **SIMULATOR ONLY** - it performs no real attacks and operates completely offline.

## ⚠️ Ethical Disclaimer

**FOR EDUCATIONAL PURPOSES ONLY**

This tool is designed exclusively for:
- ✅ Educational learning in controlled environments
- ✅ Understanding cybersecurity concepts
- ✅ Password security awareness training
- ✅ Academic research and projects
- ✅ Security awareness training

**PROHIBITED USES:**
- ❌ Real-world attacks or unauthorized access attempts
- ❌ Testing systems you don't own or have permission to test
- ❌ Any malicious or illegal activities
- ❌ Unauthorized penetration testing

**By using this tool, you agree to use it responsibly and ethically.**

---

## 🎯 Features

### 🔐 Two-Factor Authentication (2FA)
- **Email-Based OTP**: Secure 6-digit one-time password verification
- **Signup Protection**: Email verification required for new accounts
- **Login Security**: OTP verification on every login attempt
- **5-Minute Expiry**: Time-limited OTP codes for enhanced security
- **Password Hashing**: SHA-256 encryption for stored passwords
- **User Database**: Secure SQLite storage with verification tracking
- **Resend Functionality**: Request new OTP if expired or not received

### ✅ Module 1: Password Attack Simulator
- **Hashing Engine**: MD5 and SHA-256 password hashing
- **Dictionary Attack**: Simulates dictionary-based password cracking
- **Brute Force Attack**: Safe brute force (numeric only, max 4 characters)
- **AI Risk Analyzer**: Rule-based password strength analysis
- **Case Management**: Store and track attack results with case history
- **Results Dashboard**: Visual feedback on attack success and password strength

### ✅ Module 2: Email & Message Analyzer
- **Multi-Format Support**: Analyze Email, WhatsApp, and SMS messages
- **Phishing Detection**: Advanced phishing detection engine
- **Sender Analysis**: Verify sender authenticity and domain reputation
- **Link Analysis**: Detect malicious URLs and suspicious links
- **Urgency Detection**: Identify social engineering tactics
- **Brand Impersonation**: Detect fake brand communications
- **Risk Scoring**: Comprehensive risk assessment (0-100)

### ✅ Module 3: Domain Verification & Spoof Detection
- **SSL Certificate Validation**: Real-time SSL/TLS certificate verification
- **DNS Resolution**: Active DNS lookup and IP address verification
- **Spoof Detection**: Levenshtein distance-based brand impersonation detection
- **TLD Analysis**: High-risk top-level domain identification
- **Homograph Attack Detection**: Character substitution pattern recognition
- **Real-time Analysis**: Live domain security assessment
- **Risk Classification**: Safe, Suspicious, or High Risk categorization

### ✅ Module 4: AI Behavior Engine
- **Pattern Learning**: Analyze password patterns from cracked credentials
- **Predictive Analysis**: AI-based password prediction
- **Behavioral Insights**: User password creation behavior analysis
- **Risk Profiling**: Identify common security weaknesses

### ✅ Module 5: Phishing Campaign Simulator
- **Email Templates**: Pre-built phishing email templates
- **Fake Login Pages**: Simulated credential harvesting pages
- **Campaign Tracking**: Monitor click rates and credential submissions
- **Awareness Testing**: Test user susceptibility to phishing

### ✅ Module 6: Risk & Analytics Dashboard
- **Case-Based Architecture**: Comprehensive case management system
- **Executive Summary**: Auto-generated security assessment reports
- **Risk Metrics**: Total attacks, crack rates, phishing clicks, vulnerability scores
- **Module Reports**: Detailed reports from all security modules
- **Timeline View**: Chronological activity tracking
- **Export Options**: 
  - 📄 **PDF Reports**: Professional security assessment reports
  - 💾 **JSON Export**: Complete case data with raw database records
  - 📦 **Evidence Download**: Collect all case evidence

### ✅ Module 7: Awareness Training & Feedback
- **Security Tips**: Best practices for password and email security
- **Interactive Quiz**: Test security knowledge
- **Mistake Tracking**: Learn from common security errors
- **Training Modules**: Comprehensive security awareness content

### ✅ Module 8: Voice/Social Engineering Simulator
- **AI Call Scripts**: Simulated social engineering phone calls
- **Voice Phishing**: Vishing attack simulations
- **Awareness Scoring**: Measure susceptibility to voice attacks
- **Training Scenarios**: Real-world social engineering scenarios

---

## 🏗️ Project Structure

```
Offensive_AI_Simulator/
│
├── ui/                              # User interface modules
│   ├── main.py                      # Main application entry point
│   ├── authentication_ui.py         # 2FA Login/Signup UI
│   ├── module1_ui.py                # Password Attack Simulator UI
│   ├── email_analyzer_ui.py         # Email/Message Analyzer UI
│   ├── domain_verification_ui.py    # Domain Verification UI
│   ├── ai_behavior_ui.py            # AI Behavior Engine UI
│   ├── phishing_campaign_ui.py      # Phishing Campaign UI
│   ├── analytics_ui.py              # Risk & Analytics Dashboard UI
│   ├── awareness_training_ui.py     # Awareness Training UI
│   ├── social_engineering_ui.py     # Voice/Social Engineering UI
│   ├── case_history_ui.py           # Case History Display
│   ├── case_detail_ui.py            # Case Detail View
│   └── assets/                      # UI assets and images
│       └── moduleimage.png.jpg      # Module display image
│
├── backend/                         # Core logic modules
│   ├── authentication.py            # 2FA authentication system
│   ├── hashing.py                   # Password hashing (MD5, SHA256)
│   ├── dictionary_attack.py         # Dictionary attack simulation
│   ├── brute_force.py               # Brute force simulation
│   ├── ai_analyzer.py               # AI-based password analysis
│   ├── ai_attack.py                 # AI-based attack patterns
│   ├── phishing_detector.py         # Phishing detection engine
│   ├── password_engine.py           # Master password controller
│   ├── database.py                  # Database management
│   └── session_store.py             # Session data storage
│
├── cases/                           # Database storage (auto-created)
│   ├── users.db                     # User accounts and authentication
│   ├── attack_results.db            # Password attack results
│   ├── email_analysis.db            # Email analysis records
│   ├── domain_verification.db       # Domain check results
│   └── phishing_campaigns.db        # Phishing campaign data
│
├── resources/                       # Application resources
│   └── wordlist.txt                 # Common password dictionary
│
├── main.py                          # Application entry point
├── email_config.py                  # Email SMTP configuration (user creates)
├── email_config_template.py         # Email config template
├── EMAIL_SETUP_GUIDE.md             # 2FA setup instructions
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

---

## 🚀 How to Run

### Prerequisites
- **Python 3.8 or higher**
- **Windows OS** (designed for Windows desktop)
- **Internet connection** (for initial setup only)

### Installation

1. **Clone or download the project:**
```bash
git clone https://github.com/yourusername/Offensive_AI_Simulator.git
cd Offensive_AI_Simulator
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure Email for 2FA (Required):**
```bash
# Copy the email configuration template
copy email_config_template.py email_config.py

# Edit email_config.py with your Gmail credentials
# See EMAIL_SETUP_GUIDE.md for detailed instructions
```

4. **Run the application:**
```bash
python main.py
```

---

## 🔐 Two-Factor Authentication Setup

### Quick Setup Guide

1. **Enable Gmail 2-Step Verification**
   - Visit: https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Visit: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the 16-character password

3. **Configure email_config.py**
   ```python
   SENDER_EMAIL = "youremail@gmail.com"
   APP_PASSWORD = "your16charpassword"  # No spaces
   ```

4. **Test Authentication**
   - Run the application
   - Sign up with your email
   - Check email for OTP
   - Enter OTP to verify

📖 **For detailed setup instructions, see [EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md)**

### Authentication Flow

```
Application Start → Splash Screen → Login/Signup Screen
                                           ↓
                                    Enter Credentials
                                           ↓
                                    OTP Sent to Email
                                           ↓
                                    Verify 6-Digit OTP
                                           ↓
                                    Access Granted ✅
                                           ↓
                                    Case Selection → Modules
```

---

## 📖 Module Usage Guide

### 🔐 Module 1: Password Attack Simulator
1. Launch the application
2. Click **"Module 1: Password Attack Simulator"**
3. Enter user details (First Name, Last Name)
4. Enter a password to test
5. Select password type (Text or Numeric)
6. Select hash algorithm (MD5 or SHA256)
7. Click **"Simulate Password Attack"**
8. View results:
   - ✅ Cracked status
   - 🔍 Attack method used (Dictionary/Brute Force/AI)
   - 📊 Password strength assessment
   - ⚠️ AI risk level
9. Results automatically saved to case database

### 📧 Module 2: Email & Message Analyzer
1. Click **"Module 2: Email & Message Analyzer"**
2. Select message type (Email/WhatsApp/SMS)
3. Enter message content
4. Click **"Analyze Message"**
5. Review comprehensive analysis:
   - Risk score (0-100)
   - Classification (Safe/Suspicious/Phishing)
   - Sender analysis
   - Link detection
   - Urgency indicators
   - Brand impersonation warnings

### 🌐 Module 3: Domain Verification
1. Click **"Module 3: Domain Verification"**
2. Enter URL or domain name
3. Click **"Analyze Domain"**
4. View real-time security checks:
   - ✅ SSL Certificate validation
   - 🌐 DNS resolution
   - 🎭 Spoof detection
   - 🌍 TLD risk assessment
   - 🔤 Homograph attack detection
5. Review detailed risk classification

### 🤖 Module 4: AI Behavior Engine
1. Click **"Module 4: AI Behavior Engine"**
2. Train AI on cracked passwords
3. View pattern analysis
4. Test AI predictions
5. Review behavioral insights

### 📨 Module 5: Phishing Campaign Simulator
1. Click **"Module 5: Phishing Campaign Simulator"**
2. Select email template
3. Configure campaign settings
4. Launch simulation
5. Track user interactions
6. Review campaign results

### 📊 Module 6: Risk & Analytics Dashboard
1. Click **"Module 6: Risk & Analytics Dashboard"**
2. View comprehensive case analysis:
   - 📋 Case header with risk score
   - 📌 Executive summary
   - 📊 Risk metrics overview
   - 🧩 Module-specific reports
   - 🕒 Activity timeline
   - 🛡️ Security recommendations
3. Export options:
   - **📄 Export PDF Report**: Generate professional PDF report
   - **💾 Export JSON Data**: Export complete case data
   - **📦 Download Evidence**: Collect all evidence files

### 🎓 Module 7: Awareness Training
1. Click **"Module 7: Awareness Training"**
2. Read security tips
3. Take interactive quiz
4. Review mistake tracking
5. Complete training modules

### 📞 Module 8: Voice/Social Engineering
1. Click **"Module 8: Voice/Social Engineering"**
2. Select scenario
3. Review AI-generated call scripts
4. Test awareness
5. View scoring results

---

## 🔧 Building Standalone Executable

To create a standalone `.exe` file:

```bash
pyinstaller --onefile --windowed --name "OffensiveAISimulator" --icon=icon.ico main.py
```

The executable will be in the `dist/` folder.

**Note:** Add `--add-data "resources;resources"` to include resource files.

---

## 📚 Technical Details

### Hashing Algorithms
- **MD5**: Fast but cryptographically broken (educational demonstration)
- **SHA-256**: More secure, widely used in real applications

### Attack Simulations

**Dictionary Attack:**
- Compares password hash against common password hashes
- Uses `wordlist.txt` containing ~35 common passwords
- Demonstrates why common passwords are vulnerable

**Brute Force Attack:**
- Limited to numeric passwords (0-9)
- Maximum length: 4 characters
- Safe limits prevent resource exhaustion
- Demonstrates computational feasibility

**AI-Based Attack:**
- Pattern recognition from cracked passwords
- Predictive password generation
- Behavioral analysis

### Security Checks

**Domain Verification:**
- Real SSL certificate validation using Python `ssl` module
- Actual DNS resolution with `socket` library
- Levenshtein distance algorithm for spoof detection
- Homograph attack detection with character substitutions
- TLD risk assessment against known malicious extensions

**Phishing Detection:**
- Sender domain analysis
- Urgency keyword detection
- Link extraction and validation
- Brand impersonation detection
- Comprehensive risk scoring

### Database Architecture
- **SQLite3** for local data storage
- Separate databases for each module
- Case-based data organization
- Full CRUD operations
- Export-ready data structure

---

## 🛡️ Safety Features

- ✅ No network connectivity required (except domain verification)
- ✅ No real password databases accessed
- ✅ Limited brute force scope (numeric, 4 chars max)
- ✅ All operations are simulations
- ✅ Data stored locally in SQLite databases
- ✅ No external data transmission
- ✅ Safe for educational environments

---

## 🎨 UI/UX Features

- **Modern Dark Theme**: Professional cybersecurity aesthetic
- **Color Scheme**: 
  - Primary: `#00FF66` (Matrix Green)
  - Background: `#1F1F1F`, `#2E2E2E` (Dark Gray)
  - Accent: `#000000` (Black)
- **Responsive Design**: Adaptive layouts for different screen sizes
- **Real-time Feedback**: Live analysis and progress indicators
- **Visual Indicators**: Color-coded risk levels (Green/Yellow/Red)
- **Smooth Animations**: Fade-in effects and transitions

---

## 📊 Dependencies

```
pyinstaller==6.3.0
Pillow==10.1.0
pyglet
reportlab==4.0.7
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

---

## 👨‍💻 Development

**Language:** Python 3.x  
**GUI Framework:** Tkinter  
**Database:** SQLite3  
**PDF Generation:** ReportLab  
**Architecture:** Modular, scalable design  
**Packaging:** PyInstaller for .exe conversion

---

## 📖 Learning Outcomes

Students will understand:
- ✅ Two-factor authentication implementation
- ✅ Email-based OTP verification systems
- ✅ Secure password storage with hashing
- ✅ How password hashing works
- ✅ Why weak passwords are dangerous
- ✅ Dictionary vs brute force attacks
- ✅ Password complexity requirements
- ✅ Phishing attack vectors and detection
- ✅ Domain spoofing techniques
- ✅ Social engineering tactics
- ✅ Security awareness best practices
- ✅ Defensive security strategies
- ✅ Risk assessment methodologies

---

## 🎓 Educational Use Cases

1. **Cybersecurity Courses**: Hands-on password security demonstrations
2. **Security Awareness Training**: Employee phishing awareness programs
3. **Penetration Testing Labs**: Safe attack simulation environment
4. **Research Projects**: Password pattern analysis and behavioral studies
5. **Workshops & Seminars**: Interactive security demonstrations

---

## 📄 License

**Educational use only.** Not for commercial distribution.

This project is intended for educational purposes in academic and training environments. Users must comply with all applicable laws and ethical guidelines.

---

## 🤝 Contributing

This is a college project. Contributions should maintain:
- ✅ Ethical simulation approach
- ✅ Clean, documented code
- ✅ No real attack capabilities
- ✅ Educational focus
- ✅ Security best practices

### How to Contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🐛 Known Issues

- 2FA requires email configuration before first use
- Domain verification requires internet connection for SSL/DNS checks
- PDF export requires `reportlab` library installation
- Some antivirus software may flag the executable (false positive)
- Gmail App Password required (regular password won't work)

---

## 🔮 Future Enhancements

- [ ] Machine learning-based password prediction
- [ ] Advanced phishing template library
- [ ] Network traffic simulation
- [ ] Multi-language support
- [ ] Cloud-based case management
- [ ] Real-time collaboration features
- [ ] Mobile app version

---

## 🙏 Acknowledgments

- Developed as part of cybersecurity education initiative
- Inspired by real-world penetration testing tools
- Built with educational ethics in mind
- Thanks to all contributors and testers

---

## ⚖️ Disclaimer

This tool is provided "as is" for educational purposes only. The developers assume no liability for misuse or damage caused by this software. Users are solely responsible for ensuring their use complies with applicable laws and regulations.

---

<div align="center">

**Remember: Use responsibly. Learn ethically. Build securely.** 🔐

---

Made with ❤️ for Cybersecurity Education

**⭐ Star this repo if you find it useful!**

</div>
