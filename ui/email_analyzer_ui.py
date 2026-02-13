import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import sqlite3
import os
from datetime import datetime
import re

class EmailAnalyzerModule:
    def __init__(self, window):
        self.window = window
        self.window.title("Email & Message Analyzer")
        self.window.geometry("1400x750")
        self.window.configure(bg="#2E2E2E")
        
        self.init_analyzer_db()
        
        # Top bar
        navbar = tk.Frame(window, bg="#1F1F1F", height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        
        tk.Label(navbar, text="🔍 EMAIL & MESSAGE ANALYZER - AI Threat Detection",
                font=("Consolas", 14, "bold"), bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        tk.Frame(window, bg="#003300", height=1).pack(fill="x")
        
        # Main content
        content = tk.Frame(window, bg="#2E2E2E")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel - Input
        left_panel = tk.Frame(content, bg="#1F1F1F", relief="solid", bd=2)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        tk.Label(left_panel, text="📧 EMAIL INPUT", font=("Consolas", 14, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        # Email details
        details_frame = tk.Frame(left_panel, bg="#1F1F1F")
        details_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Label(details_frame, text="From:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(anchor="w", pady=(0, 5))
        self.from_entry = tk.Entry(details_frame, font=("Consolas", 11, "bold"),
                                   bg="#000000", fg="#00FF66", relief="solid", bd=1)
        self.from_entry.pack(fill="x", ipady=5, pady=(0, 10))
        
        tk.Label(details_frame, text="Subject:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(anchor="w", pady=(0, 5))
        self.subject_entry = tk.Entry(details_frame, font=("Consolas", 11, "bold"),
                                      bg="#000000", fg="#00FF66", relief="solid", bd=1)
        self.subject_entry.pack(fill="x", ipady=5, pady=(0, 10))
        
        tk.Label(details_frame, text="Email Body:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(anchor="w", pady=(0, 5))
        
        self.email_body = scrolledtext.ScrolledText(details_frame, font=("Consolas", 10, "bold"),
                                                   bg="#000000", fg="#00FF66",
                                                   relief="solid", bd=1, height=15, wrap=tk.WORD)
        self.email_body.pack(fill="both", expand=True, pady=(0, 10))
        
        # Buttons
        btn_frame = tk.Frame(left_panel, bg="#1F1F1F")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        analyze_btn = tk.Button(btn_frame, text="🔍 ANALYZE EMAIL",
                               font=("Consolas", 12, "bold"), bg="#000000", fg="#00FF66",
                               activebackground="#003300", relief="solid", bd=2,
                               cursor="hand2", command=self.analyze_email)
        analyze_btn.pack(side="left", padx=5, ipady=8, ipadx=20)
        
        clear_btn = tk.Button(btn_frame, text="🗑️ CLEAR",
                             font=("Consolas", 11, "bold"), bg="#000000", fg="#FF4444",
                             activebackground="#330000", relief="solid", bd=2,
                             cursor="hand2", command=self.clear_fields)
        clear_btn.pack(side="left", padx=5, ipady=8, ipadx=20)
        
        # Right panel - Analysis results
        right_panel = tk.Frame(content, bg="#1F1F1F", relief="solid", bd=2)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        tk.Label(right_panel, text="📊 ANALYSIS RESULTS", font=("Consolas", 14, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        # Risk score display
        self.risk_frame = tk.Frame(right_panel, bg="#000000", relief="solid", bd=2)
        self.risk_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Label(self.risk_frame, text="THREAT LEVEL", font=("Consolas", 12, "bold"),
                bg="#000000", fg="#00FF66").pack(pady=10)
        
        self.risk_label = tk.Label(self.risk_frame, text="UNKNOWN", font=("Consolas", 20, "bold"),
                                   bg="#000000", fg="#666666")
        self.risk_label.pack(pady=10)
        
        self.risk_score_label = tk.Label(self.risk_frame, text="Risk Score: 0/100",
                                         font=("Consolas", 12, "bold"), bg="#000000", fg="#666666")
        self.risk_score_label.pack(pady=(0, 10))
        
        # Analysis details
        self.analysis_text = scrolledtext.ScrolledText(right_panel, font=("Consolas", 10, "bold"),
                                                      bg="#000000", fg="#00FF66",
                                                      relief="flat", padx=15, pady=15, wrap=tk.WORD)
        self.analysis_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Load sample button
        sample_btn = tk.Button(right_panel, text="📝 LOAD SAMPLE EMAIL",
                              font=("Consolas", 11, "bold"), bg="#000000", fg="#00FF66",
                              activebackground="#003300", relief="solid", bd=2,
                              cursor="hand2", command=self.load_sample)
        sample_btn.pack(pady=10, ipady=8, ipadx=20)
    
    def init_analyzer_db(self):
        """Initialize analyzer database"""
        os.makedirs("cases", exist_ok=True)
        conn = sqlite3.connect("cases/email_analysis.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analyzed_emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT,
                subject TEXT,
                body TEXT,
                risk_score INTEGER,
                classification TEXT,
                threats_found TEXT,
                timestamp TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def analyze_email(self):
        """Analyze email for phishing indicators"""
        sender = self.from_entry.get().strip()
        subject = self.subject_entry.get().strip()
        body = self.email_body.get(1.0, tk.END).strip()
        
        if not sender or not subject or not body:
            messagebox.showerror("Error", "Fill all fields")
            return
        
        # Analysis
        risk_score = 0
        threats = []
        
        # Phishing keywords
        phishing_keywords = [
            'urgent', 'verify', 'suspend', 'confirm', 'account', 'password',
            'click here', 'act now', 'limited time', 'expire', 'security alert',
            'unusual activity', 'locked', 'update', 'validate', 'prize', 'winner',
            'congratulations', 'claim', 'refund', 'tax', 'payment'
        ]
        
        body_lower = body.lower()
        subject_lower = subject.lower()
        
        keyword_count = sum(1 for kw in phishing_keywords if kw in body_lower or kw in subject_lower)
        if keyword_count > 0:
            risk_score += min(keyword_count * 10, 40)
            threats.append(f"Phishing keywords detected: {keyword_count}")
        
        # Suspicious links
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)
        if urls:
            risk_score += min(len(urls) * 15, 30)
            threats.append(f"Suspicious links found: {len(urls)}")
            
            # Check for IP addresses in URLs
            if any(re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url) for url in urls):
                risk_score += 20
                threats.append("URL contains IP address (highly suspicious)")
        
        # Urgency indicators
        urgency_words = ['urgent', 'immediate', 'now', 'today', 'asap', 'quickly', 'hurry']
        urgency_count = sum(1 for word in urgency_words if word in body_lower or word in subject_lower)
        if urgency_count > 0:
            risk_score += min(urgency_count * 8, 20)
            threats.append(f"Urgency manipulation detected: {urgency_count} indicators")
        
        # Suspicious sender
        if sender:
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', sender):
                risk_score += 15
                threats.append("Invalid email format")
            elif any(susp in sender.lower() for susp in ['noreply', 'no-reply', 'donotreply']):
                risk_score += 10
                threats.append("Suspicious sender address")
        
        # Spelling/grammar (simple check)
        if body.count('!!') > 0 or body.count('???') > 0:
            risk_score += 10
            threats.append("Excessive punctuation detected")
        
        # Request for personal info
        personal_info_keywords = ['password', 'ssn', 'social security', 'credit card', 'bank account', 'pin']
        if any(kw in body_lower for kw in personal_info_keywords):
            risk_score += 25
            threats.append("Requests personal/financial information")
        
        # Cap risk score at 100
        risk_score = min(risk_score, 100)
        
        # Classification
        if risk_score >= 70:
            classification = "MALICIOUS"
            color = "#FF0000"
        elif risk_score >= 40:
            classification = "SUSPICIOUS"
            color = "#FFAA00"
        else:
            classification = "SAFE"
            color = "#00FF66"
        
        # Update UI
        self.risk_label.config(text=classification, fg=color)
        self.risk_score_label.config(text=f"Risk Score: {risk_score}/100", fg=color)
        
        # Display analysis
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, "🔍 DETAILED ANALYSIS\n")
        self.analysis_text.insert(tk.END, "="*60 + "\n\n")
        
        self.analysis_text.insert(tk.END, f"📊 Risk Score: {risk_score}/100\n")
        self.analysis_text.insert(tk.END, f"🏷️ Classification: {classification}\n\n")
        
        if threats:
            self.analysis_text.insert(tk.END, "⚠️ THREATS DETECTED:\n\n")
            for i, threat in enumerate(threats, 1):
                self.analysis_text.insert(tk.END, f"{i}. {threat}\n")
            self.analysis_text.insert(tk.END, "\n")
        else:
            self.analysis_text.insert(tk.END, "✅ No obvious threats detected\n\n")
        
        if urls:
            self.analysis_text.insert(tk.END, "🔗 LINKS FOUND:\n\n")
            for url in urls:
                self.analysis_text.insert(tk.END, f"  • {url}\n")
            self.analysis_text.insert(tk.END, "\n⚠️ Do not click suspicious links!\n\n")
        
        self.analysis_text.insert(tk.END, "="*60 + "\n\n")
        
        if classification == "MALICIOUS":
            self.analysis_text.insert(tk.END, "❌ RECOMMENDATION: DELETE THIS EMAIL\n")
            self.analysis_text.insert(tk.END, "This email shows strong indicators of phishing/scam.\n")
        elif classification == "SUSPICIOUS":
            self.analysis_text.insert(tk.END, "⚠️ RECOMMENDATION: PROCEED WITH CAUTION\n")
            self.analysis_text.insert(tk.END, "Verify sender through official channels before responding.\n")
        else:
            self.analysis_text.insert(tk.END, "✅ RECOMMENDATION: APPEARS SAFE\n")
            self.analysis_text.insert(tk.END, "However, always remain vigilant.\n")
        
        # Save to database
        conn = sqlite3.connect("cases/email_analysis.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO analyzed_emails (sender, subject, body, risk_score, classification, threats_found, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (sender, subject, body[:500], risk_score, classification, "; ".join(threats), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Analysis Complete", f"Email classified as: {classification}\nRisk Score: {risk_score}/100")
    
    def clear_fields(self):
        """Clear all input fields"""
        self.from_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.email_body.delete(1.0, tk.END)
        self.analysis_text.delete(1.0, tk.END)
        self.risk_label.config(text="UNKNOWN", fg="#666666")
        self.risk_score_label.config(text="Risk Score: 0/100", fg="#666666")
    
    def load_sample(self):
        """Load sample phishing email"""
        samples = [
            {
                "from": "security@paypa1-verify.com",
                "subject": "⚠️ URGENT: Verify Your Account Now!",
                "body": """Dear Valued Customer,

We have detected unusual activity on your PayPal account. Your account has been temporarily suspended for your protection.

To restore full access, you must verify your identity immediately by clicking the link below:

http://paypa1-verify.com/secure/login.php?id=12345

If you do not verify within 24 hours, your account will be permanently closed and all funds will be forfeited.

This is an automated security measure. Please do not reply to this email.

Thank you,
PayPal Security Team"""
            },
            {
                "from": "noreply@amazon-security.net",
                "subject": "Your Amazon order #12345 has been cancelled",
                "body": """Hello,

Your recent order has been cancelled due to payment verification issues.

Order Details:
- iPhone 15 Pro Max
- Amount: $1,299.99

If you did not cancel this order, please verify your payment information immediately:

Click here to verify: http://192.168.1.100/amazon/verify

Failure to verify will result in account suspension.

Amazon Customer Service"""
            }
        ]
        
        sample = samples[0]
        self.from_entry.delete(0, tk.END)
        self.from_entry.insert(0, sample["from"])
        self.subject_entry.delete(0, tk.END)
        self.subject_entry.insert(0, sample["subject"])
        self.email_body.delete(1.0, tk.END)
        self.email_body.insert(1.0, sample["body"])
        
        messagebox.showinfo("Sample Loaded", "Sample phishing email loaded!\n\nClick 'ANALYZE EMAIL' to see the AI detection in action.")


if __name__ == "__main__":
    root = tk.Tk()
    EmailAnalyzerModule(root)
    root.mainloop()
