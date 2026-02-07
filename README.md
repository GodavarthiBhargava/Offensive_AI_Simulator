# Offensive AI Simulator

## 📋 Project Description

**Offensive AI Simulator** is an educational desktop cybersecurity simulation tool designed for college students to understand password security, attack vectors, and defensive strategies. This is a **SIMULATOR ONLY** - it performs no real attacks and operates completely offline.

## ⚠️ Ethical Disclaimer

**FOR EDUCATIONAL PURPOSES ONLY**

This tool is designed exclusively for:
- Educational learning in controlled environments
- Understanding cybersecurity concepts
- Password security awareness training
- Academic research and projects

**PROHIBITED USES:**
- Real-world attacks or unauthorized access attempts
- Testing systems you don't own or have permission to test
- Any malicious or illegal activities

By using this tool, you agree to use it responsibly and ethically.

## 🎯 Features

### Module 1: Password Attack Simulation ✅ (Implemented)
- **Hashing Engine**: MD5 and SHA-256 password hashing
- **Dictionary Attack**: Simulates dictionary-based password cracking
- **Brute Force Attack**: Safe brute force (numeric only, max 4 characters)
- **AI Risk Analyzer**: Rule-based password strength analysis
- **Results Dashboard**: Visual feedback on attack success and password strength

### Module 2: Social Engineering & Phishing Simulation 🔜 (Coming Soon)
### Module 3: AI Learning & Behaviour Analysis 🔜 (Coming Soon)
### Module 4: Awareness Training & Feedback 🔜 (Coming Soon)

## 🏗️ Project Structure

```
Offensive_AI_Simulator/
│
├── ui/                      # User interface modules
│   ├── main_window.py       # Main dashboard
│   └── password_ui.py       # Password module UI
│
├── backend/                 # Core logic modules
│   ├── hashing.py           # Password hashing (MD5, SHA256)
│   ├── dictionary_attack.py # Dictionary attack simulation
│   ├── brute_force.py       # Brute force simulation
│   ├── ai_analyzer.py       # AI-based password analysis
│   ├── password_engine.py   # Master controller
│   └── session_store.py     # Session data storage
│
├── database/                # Future database integration
│   └── README.md
│
├── resources/               # Application resources
│   └── wordlist.txt         # Common password dictionary
│
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 How to Run

### Prerequisites
- Python 3.8 or higher
- Windows OS (designed for Windows desktop)

### Installation

1. Clone or download the project:
```bash
cd Offensive_AI_Simulator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

### Using Module 1: Password Attack Simulation

1. Launch the application
2. Click "Module 1: Password Attack Simulation"
3. Enter a password to test
4. Select hash algorithm (MD5 or SHA256)
5. Click "Simulate Password Attack"
6. View results:
   - Cracked status
   - Attack method used
   - Password strength assessment
   - AI risk level

## 🔧 Future Packaging

To create a standalone .exe file:

```bash
pyinstaller --onefile --windowed --name "OffensiveAISimulator" main.py
```

The executable will be in the `dist/` folder.

## 📚 Technical Details

### Hashing Algorithms
- **MD5**: Fast but cryptographically broken (educational demonstration)
- **SHA-256**: More secure, widely used in real applications

### Attack Simulations

**Dictionary Attack:**
- Compares password hash against common password hashes
- Uses wordlist.txt containing ~35 common passwords
- Demonstrates why common passwords are vulnerable

**Brute Force Attack:**
- Limited to numeric passwords (0-9)
- Maximum length: 4 characters
- Safe limits prevent resource exhaustion
- Demonstrates computational feasibility

**AI Risk Analyzer:**
- Rule-based analysis (not machine learning)
- Evaluates: length, character diversity, common patterns
- Risk levels: Low, Medium, High

## 🛡️ Safety Features

- No network connectivity required or used
- No real password databases accessed
- Limited brute force scope (numeric, 4 chars max)
- All operations are simulations
- No data is stored or transmitted

## 👨‍💻 Development

**Language:** Python 3.x  
**GUI Framework:** Tkinter  
**Architecture:** Modular, scalable design  
**Packaging:** PyInstaller for .exe conversion

## 📖 Learning Outcomes

Students will understand:
- How password hashing works
- Why weak passwords are dangerous
- Dictionary vs brute force attacks
- Password complexity requirements
- Defensive security strategies

## 📄 License

Educational use only. Not for commercial distribution.

## 🤝 Contributing

This is a college project. Contributions should maintain:
- Ethical simulation approach
- Clean, documented code
- No real attack capabilities
- Educational focus

## 📧 Support

For questions or issues related to this educational project, please consult your course instructor.

---

**Remember: Use responsibly. Learn ethically. Build securely.** 🔐
