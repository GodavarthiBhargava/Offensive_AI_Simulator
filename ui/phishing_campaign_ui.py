import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import os
from datetime import datetime
import random

class PhishingCampaignModule:
    def __init__(self, window):
        self.window = window
        self.window.title("Phishing Campaign Simulator")
        self.window.geometry("1400x750")
        self.window.configure(bg="#2E2E2E")
        
        # Initialize database
        self.init_phishing_db()
        
        # Top bar
        navbar = tk.Frame(window, bg="#1F1F1F", height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        
        tk.Label(navbar, text="📧 PHISHING CAMPAIGN SIMULATOR",
                font=("Consolas", 14, "bold"), bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        tk.Frame(window, bg="#003300", height=1).pack(fill="x")
        
        # Main content with tabs
        tab_control = ttk.Notebook(window)
        
        # Style for tabs
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background='#2E2E2E', borderwidth=0)
        style.configure('TNotebook.Tab', background='#1F1F1F', foreground='#00FF66',
                       padding=[20, 10], font=('Consolas', 10, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', '#003300')])
        
        # Create tabs
        self.scenario_tab = tk.Frame(tab_control, bg="#2E2E2E")
        self.template_tab = tk.Frame(tab_control, bg="#2E2E2E")
        self.simulation_tab = tk.Frame(tab_control, bg="#2E2E2E")
        self.results_tab = tk.Frame(tab_control, bg="#2E2E2E")
        
        tab_control.add(self.scenario_tab, text="📋 Create Scenario")
        tab_control.add(self.template_tab, text="✉️ Email Templates")
        tab_control.add(self.simulation_tab, text="🎭 Fake Login Sim")
        tab_control.add(self.results_tab, text="📊 Campaign Results")
        
        tab_control.pack(fill="both", expand=True)
        
        self.setup_scenario_tab()
        self.setup_template_tab()
        self.setup_simulation_tab()
        self.setup_results_tab()
    
    def init_phishing_db(self):
        """Initialize phishing database"""
        os.makedirs("cases", exist_ok=True)
        conn = sqlite3.connect("cases/phishing_campaigns.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_name TEXT,
                scenario_type TEXT,
                target_email TEXT,
                email_subject TEXT,
                email_body TEXT,
                clicked INTEGER DEFAULT 0,
                credentials_entered INTEGER DEFAULT 0,
                timestamp TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def setup_scenario_tab(self):
        """Setup scenario creation tab"""
        content = tk.Frame(self.scenario_tab, bg="#2E2E2E")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(content, text="CREATE PHISHING SCENARIO", font=("Consolas", 16, "bold"),
                bg="#2E2E2E", fg="#00FF66").pack(pady=(0, 20))
        
        # Campaign name
        tk.Label(content, text="Campaign Name:", font=("Consolas", 11, "bold"),
                bg="#2E2E2E", fg="#00FF66").pack(anchor="w", pady=(0, 5))
        self.campaign_name = tk.Entry(content, font=("Consolas", 11, "bold"),
                                     bg="#000000", fg="#00FF66", relief="solid", bd=1)
        self.campaign_name.pack(fill="x", ipady=8, pady=(0, 15))
        
        # Scenario type
        tk.Label(content, text="Scenario Type:", font=("Consolas", 11, "bold"),
                bg="#2E2E2E", fg="#00FF66").pack(anchor="w", pady=(0, 5))
        
        scenarios = [
            "Bank Account Verification",
            "Password Reset Request",
            "Prize/Lottery Winner",
            "IT Security Alert",
            "Package Delivery Notice",
            "Social Media Security",
            "Tax Refund Notice"
        ]
        
        self.scenario_var = tk.StringVar(value=scenarios[0])
        scenario_combo = ttk.Combobox(content, textvariable=self.scenario_var,
                                     values=scenarios, state="readonly",
                                     font=("Consolas", 11, "bold"))
        scenario_combo.pack(fill="x", ipady=8, pady=(0, 15))
        
        # Target email
        tk.Label(content, text="Target Email:", font=("Consolas", 11, "bold"),
                bg="#2E2E2E", fg="#00FF66").pack(anchor="w", pady=(0, 5))
        self.target_email = tk.Entry(content, font=("Consolas", 11, "bold"),
                                    bg="#000000", fg="#00FF66", relief="solid", bd=1)
        self.target_email.pack(fill="x", ipady=8, pady=(0, 20))
        
        # Create button
        create_btn = tk.Button(content, text="🚀 CREATE CAMPAIGN",
                              font=("Consolas", 12, "bold"), bg="#000000", fg="#00FF66",
                              activebackground="#003300", relief="solid", bd=2,
                              cursor="hand2", command=self.create_campaign)
        create_btn.pack(ipady=10, ipadx=30)
    
    def setup_template_tab(self):
        """Setup email template tab"""
        content = tk.Frame(self.template_tab, bg="#2E2E2E")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(content, text="EMAIL TEMPLATE GENERATOR", font=("Consolas", 16, "bold"),
                bg="#2E2E2E", fg="#00FF66").pack(pady=(0, 20))
        
        # Template selection
        tk.Label(content, text="Select Template:", font=("Consolas", 11, "bold"),
                bg="#2E2E2E", fg="#00FF66").pack(anchor="w", pady=(0, 5))
        
        templates = ["Bank Alert", "Password Reset", "Prize Winner", "IT Security"]
        self.template_var = tk.StringVar(value=templates[0])
        template_combo = ttk.Combobox(content, textvariable=self.template_var,
                                     values=templates, state="readonly",
                                     font=("Consolas", 11, "bold"))
        template_combo.pack(fill="x", ipady=8, pady=(0, 10))
        template_combo.bind("<<ComboboxSelected>>", lambda e: self.load_template())
        
        # Subject
        tk.Label(content, text="Email Subject:", font=("Consolas", 11, "bold"),
                bg="#2E2E2E", fg="#00FF66").pack(anchor="w", pady=(10, 5))
        self.email_subject = tk.Entry(content, font=("Consolas", 11, "bold"),
                                     bg="#000000", fg="#00FF66", relief="solid", bd=1)
        self.email_subject.pack(fill="x", ipady=8, pady=(0, 10))
        
        # Body
        tk.Label(content, text="Email Body:", font=("Consolas", 11, "bold"),
                bg="#2E2E2E", fg="#00FF66").pack(anchor="w", pady=(0, 5))
        self.email_body = scrolledtext.ScrolledText(content, font=("Consolas", 10, "bold"),
                                                   bg="#000000", fg="#00FF66",
                                                   relief="solid", bd=1, height=15)
        self.email_body.pack(fill="both", expand=True, pady=(0, 10))
        
        # Generate button
        gen_btn = tk.Button(content, text="🤖 AI GENERATE MESSAGE",
                           font=("Consolas", 11, "bold"), bg="#000000", fg="#00FF66",
                           activebackground="#003300", relief="solid", bd=2,
                           cursor="hand2", command=self.ai_generate_message)
        gen_btn.pack(ipady=8, ipadx=20)
        
        self.load_template()
    
    def setup_simulation_tab(self):
        """Setup fake login simulation tab"""
        content = tk.Frame(self.simulation_tab, bg="#2E2E2E")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(content, text="FAKE LOGIN PAGE SIMULATION", font=("Consolas", 16, "bold"),
                bg="#2E2E2E", fg="#00FF66").pack(pady=(0, 20))
        
        # Simulated login page
        login_frame = tk.Frame(content, bg="#FFFFFF", relief="solid", bd=2)
        login_frame.pack(pady=20, padx=100, fill="both", expand=True)
        
        tk.Label(login_frame, text="🏦 Secure Bank Login", font=("Arial", 18, "bold"),
                bg="#FFFFFF", fg="#003366").pack(pady=20)
        
        tk.Label(login_frame, text="⚠️ Your account requires verification",
                font=("Arial", 11), bg="#FFFFFF", fg="#CC0000").pack(pady=10)
        
        tk.Label(login_frame, text="Username:", font=("Arial", 11, "bold"),
                bg="#FFFFFF").pack(anchor="w", padx=50, pady=(20, 5))
        self.sim_username = tk.Entry(login_frame, font=("Arial", 11), relief="solid", bd=1)
        self.sim_username.pack(fill="x", padx=50, ipady=5)
        
        tk.Label(login_frame, text="Password:", font=("Arial", 11, "bold"),
                bg="#FFFFFF").pack(anchor="w", padx=50, pady=(10, 5))
        self.sim_password = tk.Entry(login_frame, font=("Arial", 11), show="*", relief="solid", bd=1)
        self.sim_password.pack(fill="x", padx=50, ipady=5)
        
        login_btn = tk.Button(login_frame, text="LOGIN", font=("Arial", 11, "bold"),
                             bg="#003366", fg="#FFFFFF", cursor="hand2",
                             command=self.simulate_login)
        login_btn.pack(pady=20, ipadx=40, ipady=5)
        
        tk.Label(content, text="⚠️ EDUCATIONAL SIMULATION - No real data is collected",
                font=("Consolas", 10, "bold"), bg="#2E2E2E", fg="#FF4444").pack(pady=10)
    
    def setup_results_tab(self):
        """Setup campaign results tab"""
        content = tk.Frame(self.results_tab, bg="#2E2E2E")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(content, text="CAMPAIGN RESULTS & ANALYTICS", font=("Consolas", 16, "bold"),
                bg="#2E2E2E", fg="#00FF66").pack(pady=(0, 20))
        
        # Results display
        self.results_text = scrolledtext.ScrolledText(content, font=("Consolas", 11, "bold"),
                                                     bg="#000000", fg="#00FF66",
                                                     relief="solid", bd=2)
        self.results_text.pack(fill="both", expand=True, pady=(0, 10))
        
        # Refresh button
        refresh_btn = tk.Button(content, text="🔄 REFRESH RESULTS",
                               font=("Consolas", 11, "bold"), bg="#000000", fg="#00FF66",
                               activebackground="#003300", relief="solid", bd=2,
                               cursor="hand2", command=self.load_results)
        refresh_btn.pack(ipady=8, ipadx=20)
        
        self.load_results()
    
    def create_campaign(self):
        """Create new phishing campaign"""
        name = self.campaign_name.get().strip()
        scenario = self.scenario_var.get()
        email = self.target_email.get().strip()
        
        if not name or not email:
            messagebox.showerror("Error", "Fill all fields")
            return
        
        conn = sqlite3.connect("cases/phishing_campaigns.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO campaigns (campaign_name, scenario_type, target_email, timestamp)
            VALUES (?, ?, ?, ?)
        """, (name, scenario, email, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", f"Campaign '{name}' created successfully!")
        self.campaign_name.delete(0, tk.END)
        self.target_email.delete(0, tk.END)
    
    def load_template(self):
        """Load email template"""
        template = self.template_var.get()
        
        templates = {
            "Bank Alert": {
                "subject": "⚠️ Urgent: Verify Your Account Now",
                "body": """Dear Valued Customer,

We have detected unusual activity on your account. For your security, we need you to verify your identity immediately.

Click here to verify: [VERIFICATION LINK]

If you don't verify within 24 hours, your account will be temporarily suspended.

Thank you,
Security Team
Secure Bank"""
            },
            "Password Reset": {
                "subject": "Password Reset Request",
                "body": """Hello,

We received a request to reset your password. If you didn't make this request, please ignore this email.

Click here to reset: [RESET LINK]

This link expires in 1 hour.

Best regards,
Support Team"""
            },
            "Prize Winner": {
                "subject": "🎉 Congratulations! You've Won $10,000!",
                "body": """Dear Winner,

Congratulations! You have been selected as the winner of our annual sweepstakes!

Prize Amount: $10,000

To claim your prize, click here: [CLAIM LINK]

Act fast! Offer expires in 48 hours.

Sincerely,
Prize Distribution Team"""
            },
            "IT Security": {
                "subject": "IT Security: Mandatory Password Update Required",
                "body": """Dear Employee,

As part of our security policy, all passwords must be updated immediately.

Click here to update: [UPDATE LINK]

Failure to comply will result in account suspension.

IT Security Department"""
            }
        }
        
        t = templates.get(template, templates["Bank Alert"])
        self.email_subject.delete(0, tk.END)
        self.email_subject.insert(0, t["subject"])
        self.email_body.delete(1.0, tk.END)
        self.email_body.insert(1.0, t["body"])
    
    def ai_generate_message(self):
        """AI generate phishing message"""
        scenario = self.template_var.get()
        
        urgency_words = ["urgent", "immediate", "now", "today", "expires soon"]
        authority_words = ["security team", "IT department", "management", "official"]
        
        subject = f"⚠️ {random.choice(['Urgent', 'Important', 'Action Required'])}: {scenario}"
        
        body = f"""Dear User,

{random.choice(['We have detected', 'Our system shows', 'We noticed'])} an issue that requires your immediate attention.

{random.choice(['Click here', 'Verify now', 'Update immediately'])} to resolve this issue.

{random.choice(['Failure to act', 'If you ignore this', 'Without action'])} may result in account suspension.

Best regards,
{random.choice(authority_words).title()}"""
        
        self.email_subject.delete(0, tk.END)
        self.email_subject.insert(0, subject)
        self.email_body.delete(1.0, tk.END)
        self.email_body.insert(1.0, body)
        
        messagebox.showinfo("AI Generated", "Message generated with psychological triggers!")
    
    def simulate_login(self):
        """Simulate login attempt"""
        username = self.sim_username.get()
        password = self.sim_password.get()
        
        if not username or not password:
            messagebox.showwarning("Warning", "Enter credentials")
            return
        
        # Log the attempt
        conn = sqlite3.connect("cases/phishing_campaigns.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO campaigns (campaign_name, scenario_type, credentials_entered, timestamp)
            VALUES (?, ?, ?, ?)
        """, ("Simulation Test", "Fake Login", 1, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        messagebox.showwarning("⚠️ PHISHING DETECTED!",
                              "This was a simulated phishing attack!\n\n"
                              "You just entered credentials on a fake page.\n\n"
                              "In a real attack, your data would be stolen.\n\n"
                              "Always verify URLs before entering credentials!")
        
        self.sim_username.delete(0, tk.END)
        self.sim_password.delete(0, tk.END)
    
    def load_results(self):
        """Load campaign results"""
        self.results_text.delete(1.0, tk.END)
        
        conn = sqlite3.connect("cases/phishing_campaigns.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM campaigns ORDER BY timestamp DESC")
        campaigns = cursor.fetchall()
        conn.close()
        
        if not campaigns:
            self.results_text.insert(tk.END, "⚠️ No campaigns found\n")
            return
        
        self.results_text.insert(tk.END, f"📊 CAMPAIGN ANALYTICS ({len(campaigns)} total)\n")
        self.results_text.insert(tk.END, "="*70 + "\n\n")
        
        total_clicks = sum(c[6] for c in campaigns if c[6])
        total_creds = sum(c[7] for c in campaigns if c[7])
        
        self.results_text.insert(tk.END, f"📈 OVERALL STATISTICS:\n")
        self.results_text.insert(tk.END, f"   Total Campaigns: {len(campaigns)}\n")
        self.results_text.insert(tk.END, f"   Total Clicks: {total_clicks}\n")
        self.results_text.insert(tk.END, f"   Credentials Entered: {total_creds}\n")
        if total_clicks > 0:
            self.results_text.insert(tk.END, f"   Success Rate: {total_creds/total_clicks*100:.1f}%\n")
        self.results_text.insert(tk.END, "\n" + "="*70 + "\n\n")
        
        self.results_text.insert(tk.END, "📋 RECENT CAMPAIGNS:\n\n")
        for c in campaigns[:10]:
            self.results_text.insert(tk.END, f"Campaign: {c[1] or 'N/A'}\n")
            self.results_text.insert(tk.END, f"Scenario: {c[2] or 'N/A'}\n")
            self.results_text.insert(tk.END, f"Target: {c[3] or 'N/A'}\n")
            self.results_text.insert(tk.END, f"Timestamp: {c[8]}\n")
            self.results_text.insert(tk.END, "-"*70 + "\n\n")


if __name__ == "__main__":
    root = tk.Tk()
    PhishingCampaignModule(root)
    root.mainloop()
