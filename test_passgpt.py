"""
PassGPT Model Test Script
Test if PassGPT model loads correctly with authentication
"""

print("Testing PassGPT Model Setup...")
print("="*60)

# Step 1: Check imports
print("\n[1] Checking required packages...")
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    print("   [OK] transformers installed")
    print("   [OK] torch installed")
except ImportError as e:
    print(f"   [ERROR] Missing package: {e}")
    print("\n   Install with: pip install transformers torch")
    exit(1)

# Step 2: Check authentication
print("\n[2] Checking Hugging Face authentication...")
try:
    from huggingface_hub import HfFolder
    token = HfFolder.get_token()
    if token:
        print(f"   [OK] Logged in (token: {token[:10]}...)")
    else:
        print("   [WARNING] Not logged in")
        print("\n   Login with: huggingface-cli login")
        print("   Get token from: https://huggingface.co/settings/tokens")
except Exception as e:
    print(f"   [WARNING] Could not check auth: {e}")

# Step 3: Try loading model
print("\n[3] Loading PassGPT model...")
print("   (This may take a few minutes on first run)")

try:
    model_name = "javirandor/passgpt-16characters"
    
    print(f"   Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print("   [OK] Tokenizer loaded")
    
    print(f"   Loading model...")
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()
    print("   [OK] Model loaded")
    
    # Step 4: Generate test passwords
    print("\n[4] Generating test passwords...")
    
    input_ids = tokenizer.encode("", return_tensors="pt")
    outputs = model.generate(
        input_ids,
        max_length=16,
        num_return_sequences=5,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=1.0,
        pad_token_id=tokenizer.eos_token_id
    )
    
    print("\n   Sample Generated Passwords:")
    for i, output in enumerate(outputs, 1):
        password = tokenizer.decode(output, skip_special_tokens=True).strip()
        print(f"   {i}. {password}")
    
    print("\n" + "="*60)
    print("[SUCCESS] PassGPT is working correctly!")
    print("="*60)
    print("\nYou can now use the AI Behavior Engine in the application.")
    
except Exception as e:
    print(f"\n   [ERROR] {e}")
    print("\n" + "="*60)
    print("[SETUP REQUIRED]")
    print("="*60)
    
    error_str = str(e)
    
    if "401" in error_str or "authentication" in error_str.lower():
        print("\nAUTHENTICATION ISSUE")
        print("\nFollow these steps:")
        print("1. Install: pip install huggingface_hub")
        print("2. Login: huggingface-cli login")
        print("3. Visit: https://huggingface.co/settings/tokens")
        print("4. Create token (Role: Read)")
        print("5. Paste token when prompted")
        print("6. Run this script again")
    else:
        print("\nINSTALLATION ISSUE")
        print("\nTry:")
        print("pip install --upgrade transformers torch huggingface_hub")
        print("\nFor CPU-only:")
        print("pip install torch --index-url https://download.pytorch.org/whl/cpu")
    
    print("\nSee PASSGPT_SETUP_GUIDE.md for detailed instructions")
