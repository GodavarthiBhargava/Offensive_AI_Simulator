# Project Structure

```
Offensive_AI_Simulator/
│
├── assets/                      # Application assets
│   ├── icon.ico                 # Application icon
│   └── README.md
│
├── backend/                     # Core logic modules
│   ├── ai_analyzer.py           # AI-based password analysis
│   ├── brute_force.py           # Brute force simulation
│   ├── database.py              # Database operations
│   ├── dictionary_attack.py     # Dictionary attack simulation
│   ├── hashing.py               # Password hashing (MD5, SHA256)
│   ├── password_engine.py       # Master controller
│   └── session_store.py         # Session data storage
│
├── cases/                       # Case files storage
│   └── attack_results.db        # Attack results database
│
├── database/                    # Database files
│   ├── forensics_cases.db       # Forensics cases database
│   └── README.md
│
├── resources/                   # Application resources
│   └── wordlist.txt             # Common password dictionary
│
├── ui/                          # User interface modules
│   ├── assessts/                # UI assets
│   │   ├── icon.jpg             # Icon image
│   │   └── welcome.jpg          # Welcome screen image
│   ├── case_detail_ui.py        # Case detail interface
│   ├── case_history_ui.py       # Case history interface
│   ├── font_loader.py           # Font management utility
│   └── module1_ui.py            # Password module UI
│
├── main.py                      # Application entry point
├── CyberformDemo.otf            # Custom font (optional)
├── CHANGELOG.md                 # Version history
├── MODULE1_GUIDE.md             # Module 1 documentation
├── QUICKSTART.md                # Quick start guide
├── README.md                    # Main documentation
└── requirements.txt             # Python dependencies
```

## Cleaned Up Files

The following unused files have been removed:
- Futuristic-Font-*.png (10 preview images)
- CyberformDemo-Oblique.otf (unused font variant)
- skill_palavar.py (duplicate/unused)
- test_*.py (test files)
- Readme.txt (duplicate)
- ui/main_window.py (replaced by main.py)
- ui/password_ui.py (old version)
- ui/password_ui_new.py (old version)
- ui/terminal_password_ui.py (unused)
- backend/ai_attack.py (unused)
- backend/hashing_utils.py (unused)
- ui/assessts/bg.jpg (unused background)
