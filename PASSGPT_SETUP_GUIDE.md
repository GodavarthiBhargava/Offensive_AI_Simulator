# 🤖 PassGPT Setup Guide - AI Password Prediction

## 📋 Overview

The AI Behavior Engine uses **PassGPT** (javirandor/passgpt-16characters) - a GPT-2 based model trained on leaked passwords to generate realistic weak password predictions for security research.

---

## ⚠️ IMPORTANT: Educational Use Only

This tool is for:
- ✅ Security research and education
- ✅ Password strength analysis
- ✅ Defensive security training
- ❌ **NOT for unauthorized access attempts**

---

## 🔧 Installation Steps

### Step 1: Install Required Packages

```bash
pip install transformers torch huggingface_hub
```

For CPU-only (recommended):
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Step 2: Create Hugging Face Account

1. Visit: https://huggingface.co/join
2. Create a free account
3. Verify your email

### Step 3: Get Access Token

1. Visit: https://huggingface.co/settings/tokens
2. Click **"Create new token"**
3. Name: `PassGPT_Access`
4. Role: **Read**
5. Click **"Generate token"**
6. **Copy the token** (starts with `hf_...`)

### Step 4: Login via CLI (Recommended)

Open terminal/command prompt:

```bash
pip install huggingface_hub
huggingface-cli login
```

When prompted:
```
Enter your token: [paste your token here]
```

You should see:
```
Login successful
```

### Step 5: Restart Application

Close and restart the Offensive AI Simulator application.

---

## 🔄 Alternative: Direct Token Method

If CLI login doesn't work, you can use token directly in code.

**⚠️ Security Warning:** Never commit tokens to version control!

Create a file: `huggingface_token.py`

```python
# Hugging Face Token Configuration
HF_TOKEN = "hf_your_token_here"
```

Add to `.gitignore`:
```
huggingface_token.py
```

---

## 🧪 Testing the Model

Test if model loads correctly:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "javirandor/passgpt-16characters"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

print("✅ Model loaded successfully!")

# Generate sample passwords
input_ids = tokenizer.encode("", return_tensors="pt")
outputs = model.generate(
    input_ids,
    max_length=16,
    num_return_sequences=5,
    do_sample=True,
    top_k=50,
    top_p=0.95,
    temperature=1.0
)

print("\n🔮 Sample Generated Passwords:")
for output in outputs:
    print(tokenizer.decode(output, skip_special_tokens=True))
```

Expected output:
```
✅ Model loaded successfully!

🔮 Sample Generated Passwords:
password123
abc@1234
qwerty2022
welcome2024
admin123!
```

---

## 🐛 Troubleshooting

### Error: 401 Unauthorized

**Cause:** Not logged in to Hugging Face

**Solution:**
1. Run: `huggingface-cli login`
2. Paste your token
3. Restart application

### Error: Model not found

**Cause:** Network issue or model name incorrect

**Solution:**
1. Check internet connection
2. Verify model exists: https://huggingface.co/javirandor/passgpt-16characters
3. Clear cache: Delete `C:\Users\YourName\.cache\huggingface`

### Error: Out of memory

**Cause:** Model too large for RAM

**Solution:**
1. Close other applications
2. Use smaller batch size
3. Reduce `num_return_sequences`

### Error: transformers version

**Cause:** Outdated transformers library

**Solution:**
```bash
pip install --upgrade transformers huggingface_hub torch
```

---

## 📊 Model Parameters

### Generation Settings

```python
max_length=16          # Maximum password length
num_return_sequences=20  # Number of predictions
do_sample=True         # Enable randomness
top_k=50              # Top 50 likely characters
top_p=0.95            # Nucleus sampling (95%)
temperature=1.0       # Randomness control (0.7-1.2)
```

### Parameter Tuning

- **Higher temperature** (1.2-1.5) → More random/creative
- **Lower temperature** (0.7-0.9) → More predictable/common
- **Higher top_k** (100) → More variety
- **Lower top_k** (20) → More focused

---

## 🎯 How PassGPT Works

1. **Training Data:** Trained on millions of leaked passwords
2. **Architecture:** GPT-2 based language model
3. **Prediction:** Learns character-level patterns
4. **Output:** Generates realistic weak passwords

### What It Predicts:

- ✅ Common patterns (password123, qwerty)
- ✅ Year patterns (2024, 2025)
- ✅ Special character usage (@, !, #)
- ✅ Length distributions
- ❌ **NOT personalized** (doesn't use names directly)

---

## 🔐 Security Best Practices

### For Researchers:

1. ✅ Use only on test systems
2. ✅ Document all experiments
3. ✅ Follow ethical guidelines
4. ✅ Obtain proper authorization

### For Students:

1. ✅ Use in controlled lab environment
2. ✅ Never test on real accounts
3. ✅ Understand legal implications
4. ✅ Report findings responsibly

---

## 📚 Additional Resources

- **Model Page:** https://huggingface.co/javirandor/passgpt-16characters
- **Research Paper:** "PassGPT: Password Modeling and Generation with Large Language Models"
- **Hugging Face Docs:** https://huggingface.co/docs
- **Transformers Docs:** https://huggingface.co/docs/transformers

---

## 💡 Tips for Best Results

1. **Combine with Rule-Based:** Use both AI and name-based predictions
2. **Filter Results:** Remove duplicates and invalid passwords
3. **Adjust Parameters:** Tune temperature for your use case
4. **Batch Processing:** Generate in batches for efficiency
5. **Cache Results:** Save predictions to avoid regeneration

---

## 🆘 Support

If you encounter issues:

1. Check this guide first
2. Verify all dependencies installed
3. Test with simple script above
4. Check Hugging Face status: https://status.huggingface.co
5. Review error messages carefully

---

## ⚖️ Legal Disclaimer

This tool is provided for **educational and research purposes only**. Users are solely responsible for ensuring their use complies with all applicable laws and regulations. Unauthorized access to computer systems is illegal.

**By using this tool, you agree to use it responsibly and ethically.**

---

**Remember: Use for defense, not offense. Build secure systems, don't break them.** 🛡️
