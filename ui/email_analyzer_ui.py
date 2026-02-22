import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import sqlite3
import os
from datetime import datetime
import re
from backend.phishing_detector import PhishingDetector

class EmailAnalyzerModule:
    def __init__(self, window):
        self.window = window
        self.window.title("Email & Message Analyzer")
        self.window.geometry("1400x750")
        self.window.configure(bg="#2E2E2E")
        
        self.init_analyzer_db()
        self.detector = PhishingDetector()
        
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
        
        tk.Label(left_panel, text="📧 MESSAGE INPUT", font=("Consolas", 14, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        # Message type selection
        type_frame = tk.Frame(left_panel, bg="#1F1F1F")
        type_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Label(type_frame, text="Message Type:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(anchor="w", pady=(0, 5))
        
        self.message_type = tk.StringVar(value="Email")
        type_combo = ttk.Combobox(type_frame, textvariable=self.message_type,
                                 values=["Email", "WhatsApp", "SMS"], state="readonly",
                                 font=("Consolas", 11, "bold"))
        type_combo.pack(fill="x", ipady=5)
        type_combo.bind("<<ComboboxSelected>>", self.on_type_change)
        
        # Email details
        details_frame = tk.Frame(left_panel, bg="#1F1F1F")
        details_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.from_label = tk.Label(details_frame, text="From:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66")
        self.from_label.pack(anchor="w", pady=(0, 5))
        self.from_entry = tk.Entry(details_frame, font=("Consolas", 11, "bold"),
                                   bg="#000000", fg="#00FF66", relief="solid", bd=1)
        self.from_entry.pack(fill="x", ipady=5, pady=(0, 10))
        
        self.subject_label = tk.Label(details_frame, text="Subject:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66")
        self.subject_label.pack(anchor="w", pady=(0, 5))
        self.subject_entry = tk.Entry(details_frame, font=("Consolas", 11, "bold"),
                                      bg="#000000", fg="#00FF66", relief="solid", bd=1)
        self.subject_entry.pack(fill="x", ipady=5, pady=(0, 10))
        
        self.body_label = tk.Label(details_frame, text="Email Body:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66")
        self.body_label.pack(anchor="w", pady=(0, 5))
        
        self.email_body = scrolledtext.ScrolledText(details_frame, font=("Consolas", 10, "bold"),
                                                   bg="#000000", fg="#00FF66",
                                                   relief="solid", bd=1, height=15, wrap=tk.WORD)
        self.email_body.pack(fill="both", expand=True, pady=(0, 10))
        
        # Buttons
        btn_frame = tk.Frame(left_panel, bg="#1F1F1F")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        analyze_btn = tk.Button(btn_frame, text="🔍 ANALYZE MESSAGE",
                               font=("Consolas", 12, "bold"), bg="#000000", fg="#00FF66",
                               activebackground="#003300", relief="solid", bd=2,
                               cursor="hand2", command=self.analyze_email)
        analyze_btn.pack(side="left", padx=5, ipady=8, ipadx=20)
        self.analyze_btn = analyze_btn
        
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
    
    def on_type_change(self, event=None):
        """Handle message type change"""
        msg_type = self.message_type.get()
        
        if msg_type == "Email":
            self.from_label.config(text="From:")
            self.subject_label.pack(anchor="w", pady=(0, 5))
            self.subject_entry.pack(fill="x", ipady=5, pady=(0, 10))
            self.body_label.config(text="Email Body:")
            self.analyze_btn.config(text="🔍 ANALYZE EMAIL")
        elif msg_type == "WhatsApp":
            self.from_label.config(text="Sender Name/Number:")
            self.subject_label.pack_forget()
            self.subject_entry.pack_forget()
            self.body_label.config(text="WhatsApp Message:")
            self.analyze_btn.config(text="🔍 ANALYZE WHATSAPP")
        else:  # SMS
            self.from_label.config(text="Sender Name/Number:")
            self.subject_label.pack_forget()
            self.subject_entry.pack_forget()
            self.body_label.config(text="SMS Content:")
            self.analyze_btn.config(text="🔍 ANALYZE SMS")
    
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
        """Analyze email/message for phishing indicators"""
        msg_type = self.message_type.get()
        sender = self.from_entry.get().strip()
        body = self.email_body.get(1.0, tk.END).strip()
        
        if msg_type == "Email":
            subject = self.subject_entry.get().strip()
            if not sender or not subject or not body:
                messagebox.showerror("Error", "Fill all fields")
                return
            result = self.detector.analyze_email(sender, subject, body)
        else:
            if not sender or not body:
                messagebox.showerror("Error", "Fill sender and message content")
                return
            result = self.detector.analyze_message(sender, body, msg_type)
        
        # Update UI
        classification = result['classification']
        risk_score = result['risk_score']
        
        color_map = {"SAFE": "#00FF66", "SUSPICIOUS": "#FFAA00", "MALICIOUS": "#FF0000"}
        color = color_map.get(classification, "#666666")
        
        self.risk_label.config(text=classification, fg=color)
        self.risk_score_label.config(text=f"Risk Score: {risk_score}/100", fg=color)
        
        # Display analysis
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, f"🔍 {msg_type.upper()} ANALYSIS REPORT\n")
        self.analysis_text.insert(tk.END, "="*60 + "\n\n")
        
        self.analysis_text.insert(tk.END, f"📊 Risk Score: {risk_score}/100\n")
        self.analysis_text.insert(tk.END, f"🏷️ Classification: {classification}\n")
        self.analysis_text.insert(tk.END, f"⚠️ Risk Level: {result['risk_level']}\n\n")
        
        # Domain analysis
        domain = result['domain_analysis']
        self.analysis_text.insert(tk.END, "🌐 DOMAIN ANALYSIS:\n")
        self.analysis_text.insert(tk.END, f"  Link Domain: {domain['link_domain']}\n")
        self.analysis_text.insert(tk.END, f"  Brand Impersonation: {domain['brand_impersonation']}\n")
        self.analysis_text.insert(tk.END, f"  Domain Risk: {domain['domain_risk_level']}\n")
        self.analysis_text.insert(tk.END, f"  Trust Status: {domain['trust_status']}\n\n")
        
        # Red flags
        if result['red_flags']:
            self.analysis_text.insert(tk.END, "⚠️ RED FLAGS DETECTED:\n\n")
            for i, flag in enumerate(result['red_flags'], 1):
                self.analysis_text.insert(tk.END, f"{i}. {flag}\n")
            self.analysis_text.insert(tk.END, "\n")
        else:
            self.analysis_text.insert(tk.END, "✅ No obvious threats detected\n\n")
        
        self.analysis_text.insert(tk.END, "="*60 + "\n\n")
        
        # Recommendation
        if classification == "MALICIOUS":
            self.analysis_text.insert(tk.END, "❌ RECOMMENDATION: DELETE IMMEDIATELY\n")
            self.analysis_text.insert(tk.END, "This message shows strong phishing indicators.\n")
        elif classification == "SUSPICIOUS":
            self.analysis_text.insert(tk.END, "⚠️ RECOMMENDATION: PROCEED WITH CAUTION\n")
            self.analysis_text.insert(tk.END, "Verify through official channels.\n")
        else:
            self.analysis_text.insert(tk.END, "✅ RECOMMENDATION: APPEARS SAFE\n")
            self.analysis_text.insert(tk.END, "However, always remain vigilant.\n")
        
        # Save to database
        conn = sqlite3.connect("cases/email_analysis.db")
        cursor = conn.cursor()
        
        subject_val = self.subject_entry.get().strip() if msg_type == "Email" else msg_type
        cursor.execute("""
            INSERT INTO analyzed_emails (sender, subject, body, risk_score, classification, threats_found, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (sender, subject_val, body[:500], risk_score, classification, "; ".join(result['red_flags']), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Analysis Complete", f"Classified as: {classification}\nRisk Score: {risk_score}/100")
    
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
