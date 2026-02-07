# Quick Start Guide - Offensive AI Simulator

## 🚀 Launch Application

```bash
cd Offensive_AI_Simulator
python main.py
```

## 🎯 Module 1: Password Attack Simulation

### Step-by-Step Usage

1. **Launch Main Dashboard**
   - Dark-themed window opens
   - 4 modules displayed (only Module 1 active)

2. **Open Module 1**
   - Click "🔐 Module 1: Password Attack Simulation"
   - New window opens with professional interface

3. **Enter User Context (Optional)**
   - Username: e.g., `john`
   - Full Name: e.g., `John Smith`
   - Used for AI risk analysis

4. **Select Input Mode**
   - ⚪ Enter Password (default)
   - ⚪ Enter Hash

5. **Enter Credential**
   - Password mode: Input is masked (•••)
   - Hash mode: Input is plain text

6. **Select Hash Algorithm**
   - MD5 (faster, less secure)
   - SHA256 (slower, more secure)

7. **Run Simulation**
   - Click "🚀 SIMULATE PASSWORD ATTACK"
   - Results appear in console-style display

## 📊 Understanding Results

### Status
- **CRACKED ❌**: Password found via dictionary or brute force
- **NOT CRACKED ✓**: Password not found in simulation

### Attack Used
- **Dictionary**: Found in common password list
- **BruteForce**: Found via numeric brute force (≤4 digits)
- **None**: Not cracked

### Password Strength
- **Weak**: Easily crackable or poor complexity
- **Medium**: Moderate complexity
- **Strong**: Good complexity, not cracked
- **Unknown**: Hash mode without cracking

### AI Risk Level
- **High**: Multiple risk factors detected
- **Medium**: Some risk factors present
- **Low**: Good password practices
- **Unknown**: Cannot analyze (hash mode)

## 🧪 Example Tests

### Test 1: Weak Dictionary Password
```
Input Mode: Enter Password
Password: password
Algorithm: MD5
Result: CRACKED via Dictionary, Weak, High Risk
```

### Test 2: Numeric Brute Force
```
Input Mode: Enter Password
Password: 1234
Algorithm: SHA256
Result: CRACKED via BruteForce, Weak, High Risk
```

### Test 3: Strong Password
```
Input Mode: Enter Password
Password: MyS3cur3P@ss!2024
Algorithm: SHA256
Result: NOT CRACKED, Strong, Low Risk
```

### Test 4: Hash Mode (Known)
```
Input Mode: Enter Hash
Hash: 5f4dcc3b5aa765d61d8327deb882cf99
Algorithm: MD5
Result: CRACKED via Dictionary (password: "password")
```

### Test 5: User Context Risk
```
Username: john
Full Name: John Smith
Password: john123
Result: Higher AI Risk (username in password)
```

## ⚠️ Important Notes

- **Educational Only**: This is a simulation tool
- **No Real Attacks**: All operations are simulated
- **Offline**: No network connectivity required
- **Safe Limits**: Brute force limited to 4-digit numeric
- **Ethical Use**: Follow responsible disclosure practices

## 🎨 UI Features

- **Dark Theme**: Professional cybersecurity aesthetic
- **Card Layout**: Clear section separation
- **Console Display**: Monospaced green-on-black results
- **Icons**: Visual clarity for each section
- **Responsive**: Clean, aligned interface

## 🔧 Troubleshooting

### Application won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt
```

### Module 1 button not working
- Ensure all files in `ui/` and `backend/` directories exist
- Check for Python syntax errors in console

### Results not displaying
- Ensure credential field is not empty
- Check that hash format is valid (hex string)

## 📦 Creating .exe (Optional)

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name "OffensiveAISimulator" main.py

# Find executable in dist/ folder
```

## 📚 Additional Resources

- `README.md` - Full project documentation
- `MODULE1_GUIDE.md` - Detailed Module 1 guide
- `CHANGELOG.md` - Technical change log

## 🎓 Learning Objectives

After using Module 1, you should understand:
- How password hashing works (MD5 vs SHA256)
- Why common passwords are dangerous
- Dictionary vs brute force attacks
- Password complexity requirements
- Personal information in passwords (risk)

---

**Ready to simulate! Remember: Use ethically, learn responsibly.** 🔐
