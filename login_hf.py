"""
Login to Hugging Face with token
"""
from huggingface_hub import login

# SECURITY: Replace with your token or use environment variable
# Get token from: https://huggingface.co/settings/tokens
token = "YOUR_TOKEN_HERE"  # Replace this before using

print("Logging in to Hugging Face...")
try:
    login(token=token)
    print("[SUCCESS] Login successful!")
    print("Token saved. You can now use PassGPT model.")
except Exception as e:
    print(f"[ERROR] Login failed: {e}")
