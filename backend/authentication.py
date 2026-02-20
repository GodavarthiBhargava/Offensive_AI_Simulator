import sqlite3
import os
import hashlib
import random
import smtplib
import time
from email.message import EmailMessage

class AuthenticationSystem:
    def __init__(self):
        self.db_path = "cases/users.db"
        self.init_database()
        self.current_otp = None
        self.otp_email = None
        self.otp_timestamp = None
        self.otp_expiry = 300  # 5 minutes
        
    def init_database(self):
        """Initialize users database"""
        os.makedirs("cases", exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                app_password TEXT NOT NULL,
                verified INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def generate_otp(self):
        """Generate 6-digit OTP"""
        return str(random.randint(100000, 999999))
    
    def send_otp_email(self, receiver_email, otp, sender_password=None):
        """Send OTP to user's email using configured SMTP"""
        try:
            # Use email_config.py for SMTP credentials
            try:
                from email_config import SENDER_EMAIL, APP_PASSWORD
            except ImportError:
                return False, "Email configuration not found. Please configure email_config.py"
            
            if SENDER_EMAIL == "your_email@gmail.com" or APP_PASSWORD == "your_16_char_app_password":
                return False, "Please configure email_config.py with SMTP credentials"
            
            msg = EmailMessage()
            msg.set_content(f"""
SECURENETRA
Offensive AI Security Simulator

🔐 TWO-FACTOR AUTHENTICATION

Hello,

You have requested access to SECURENETRA. To complete your authentication, please use the following One-Time Password (OTP):

YOUR OTP CODE: {otp}

⏱️ VALIDITY: This code is valid for 5 minutes only.

⚠️ SECURITY NOTICE:
• Do not share this code with anyone.
• SECURENETRA will never ask for your OTP via phone or email.
• If you did not request this code, please ignore this email.

🛡️ Need Help?
This is an automated security email from SECURENETRA.
For support, contact your system administrator.

© 2024 SECURENETRA
Digital Forensics Simulator
Educational Cybersecurity Training Platform
            """)
            msg["Subject"] = "🔐 SECURENETRA - Your Security Access Code"
            msg["From"] = f"SECURENETRA <{SENDER_EMAIL}>"
            msg["To"] = receiver_email
            
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(SENDER_EMAIL, APP_PASSWORD)
                smtp.send_message(msg)
            
            return True, "OTP sent successfully"
        except smtplib.SMTPAuthenticationError:
            return False, "SMTP authentication failed. Check email_config.py credentials."
        except Exception as e:
            return False, f"Failed to send OTP: {str(e)}"
    
    def request_otp(self, email):
        """Generate and send OTP to email"""
        self.current_otp = self.generate_otp()
        self.otp_email = email
        self.otp_timestamp = time.time()
        
        success, message = self.send_otp_email(email, self.current_otp)
        return success, message
    
    def verify_otp(self, email, otp):
        """Verify OTP"""
        if not self.current_otp or not self.otp_email:
            return False, "No OTP requested"
        
        if email != self.otp_email:
            return False, "Email mismatch"
        
        # Check expiry
        if time.time() - self.otp_timestamp > self.otp_expiry:
            self.current_otp = None
            return False, "OTP expired. Please request a new one."
        
        if otp == self.current_otp:
            self.current_otp = None  # Clear OTP after successful verification
            return True, "OTP verified successfully"
        else:
            return False, "Invalid OTP"
    
    def signup(self, email, password):
        """Register new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                conn.close()
                return False, "Email already registered"
            
            # Hash password and store user
            password_hash = self.hash_password(password)
            cursor.execute("""
                INSERT INTO users (email, password_hash, app_password, verified)
                VALUES (?, ?, '', 0)
            """, (email, password_hash))
            
            conn.commit()
            conn.close()
            return True, "Account created successfully"
        except Exception as e:
            return False, f"Signup failed: {str(e)}"
    
    def verify_user(self, email):
        """Mark user as verified after OTP confirmation"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("UPDATE users SET verified = 1 WHERE email = ?", (email,))
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def login(self, email, password):
        """Verify login credentials"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            cursor.execute("""
                SELECT email, verified FROM users 
                WHERE email = ? AND password_hash = ?
            """, (email, password_hash))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                if result[1] == 1:  # verified
                    return True, "Credentials valid"
                else:
                    return False, "Account not verified"
            else:
                return False, "Invalid email or password"
        except Exception as e:
            return False, f"Login failed: {str(e)}"
    
    def user_exists(self, email):
        """Check if user exists"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
            result = cursor.fetchone()
            conn.close()
            return result is not None
        except:
            return False
    
    def get_app_password(self, email):
        """Get stored app password for user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT app_password FROM users WHERE email = ?", (email,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else None
        except:
            return None
