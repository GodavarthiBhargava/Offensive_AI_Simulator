# PassGPT Setup - Quick Start

## Current Status
The PassGPT model requires Hugging Face authentication because it's a **gated repository**.

## Setup Steps (5 minutes)

### Step 1: Create Hugging Face Account
1. Go to: https://huggingface.co/join
2. Sign up (free)
3. Verify your email

### Step 2: Request Access to PassGPT Model
1. Visit: https://huggingface.co/javirandor/passgpt-16characters
2. Click **"Request Access"** button
3. Wait for approval (usually instant)

### Step 3: Get Your Token
1. Go to: https://huggingface.co/settings/tokens
2. Click **"Create new token"**
3. Name: `PassGPT_Access`
4. Role: Select **"Read"**
5. Click **"Generate token"**
6. **COPY THE TOKEN** (starts with `hf_...`)

### Step 4: Login via CLI
Open Command Prompt and run:

```bash
huggingface-cli login
```

When prompted, paste your token and press Enter.

You should see:
```
Login successful
```

### Step 5: Test the Setup
Run the test script:

```bash
python test_passgpt.py
```

If successful, you'll see:
```
[SUCCESS] PassGPT is working correctly!
```

### Step 6: Run the Application
```bash
python main.py
```

Navigate to **AI Behavior Engine** module and generate predictions!

---

## Troubleshooting

### "401 Client Error" or "Access restricted"
- You need to request access at: https://huggingface.co/javirandor/passgpt-16characters
- Make sure you're logged in: `huggingface-cli login`

### "huggingface-cli not found"
```bash
pip install huggingface_hub
```

### Model takes too long to load
- First download is ~500MB, takes 2-5 minutes
- Subsequent loads are instant (cached)

### Out of memory
- Close other applications
- Reduce number of predictions in the UI

---

## What You'll Get

Once setup, the AI Behavior Engine will:
- Generate realistic weak passwords using AI
- Combine rule-based (name patterns) + AI predictions
- Provide 20-50 password guesses per request
- Learn from password patterns in your database

---

## Alternative: Skip PassGPT (Use Rule-Based Only)

If you don't want to setup PassGPT, the module will still work with rule-based predictions only. The AI features will be disabled but name-based patterns will still generate predictions.

---

## Need Help?

1. Check PASSGPT_SETUP_GUIDE.md for detailed instructions
2. Run `python test_passgpt.py` to diagnose issues
3. Verify you have access at: https://huggingface.co/javirandor/passgpt-16characters

---

**Remember: This tool is for educational and security research purposes only!**
