# Module 1 Enhancement - Usage Guide

## 🎨 UI Improvements

### Professional Cybersecurity Theme
- Dark theme (#1e1e1e background, #2d2d2d cards)
- Cyan accent color (#00d9ff) for headers and active elements
- Monospaced console-style results display
- Card-based layout with clear section separation
- Professional icons and emojis for visual clarity

### Layout Structure
1. **Title Section**: Module name and description
2. **User Context Section**: Optional username and full name inputs
3. **Input Mode Section**: Radio buttons for password/hash selection
4. **Credential Input Section**: Single input field (masked for passwords)
5. **Hash Algorithm Section**: Dropdown for MD5/SHA256
6. **Action Button**: Large, prominent simulation trigger
7. **Results Section**: Console-style output display

## 🔧 New Features

### Dual Input Mode
- **Password Mode**: Enter plaintext password (masked with •)
  - Password is hashed internally
  - Full attack simulation runs
  - AI analysis includes user context

- **Hash Mode**: Enter hash directly
  - Hash is used as-is for attack simulation
  - No password reversal attempted
  - AI analysis shows "Unknown" if not cracked

### User Context Integration
- **Username**: Optional field for AI risk analysis
- **Full Name**: Optional field for AI risk analysis
- AI checks if username/name appears in password
- Increases risk score if personal info detected

## 📊 Result Fields

All results display:
- **Status**: CRACKED ❌ or NOT CRACKED ✓
- **Attack Used**: Dictionary / BruteForce / None
- **Password Strength**: Weak / Medium / Strong / Unknown
- **AI Risk Level**: Low / Medium / High / Unknown
- **Cracked Password**: Shown only if cracked

## 🧪 Testing Scenarios

### Test 1: Weak Password (Dictionary)
- Input Mode: Password
- Password: `password`
- Algorithm: MD5
- Expected: CRACKED via Dictionary, Weak strength, High risk

### Test 2: Numeric Brute Force
- Input Mode: Password
- Password: `1234`
- Algorithm: SHA256
- Expected: CRACKED via BruteForce, Weak strength, High risk

### Test 3: Strong Password
- Input Mode: Password
- Password: `MyS3cur3P@ssw0rd!`
- Algorithm: SHA256
- Expected: NOT CRACKED, Strong strength, Low risk

### Test 4: Hash Mode
- Input Mode: Hash
- Hash: `5f4dcc3b5aa765d61d8327deb882cf99` (MD5 of "password")
- Algorithm: MD5
- Expected: CRACKED via Dictionary, shows cracked password

### Test 5: User Context Risk
- Username: `john`
- Full Name: `John Smith`
- Password: `john123`
- Expected: Higher AI risk due to username in password

## 🔐 Security Notes

- All operations are simulations
- No real attacks performed
- No network connectivity
- No data stored or transmitted
- Brute force limited to 4-digit numeric only
- Educational purposes only

## 🚀 Running the Application

```bash
python main.py
```

1. Main dashboard opens
2. Click "Module 1: Password Attack Simulation"
3. Fill in optional user context
4. Select input mode (Password/Hash)
5. Enter credential
6. Select hash algorithm
7. Click "SIMULATE PASSWORD ATTACK"
8. View results in console-style display

## 📦 Future .exe Packaging

```bash
pyinstaller --onefile --windowed --name "OffensiveAISimulator" main.py
```

The dark theme and professional UI will be preserved in the executable.
