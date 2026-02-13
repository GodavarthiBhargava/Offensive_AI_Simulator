import tkinter as tk
from tkinter import ttk, scrolledtext
import sqlite3
import os
from datetime import datetime
from collections import Counter

class AnalyticsDashboard:
    def __init__(self, window):
        self.window = window
        self.window.title("Risk & Analytics Dashboard")
        self.window.geometry("1400x800")
        self.window.configure(bg="#2E2E2E")
        
        # Top bar
        navbar = tk.Frame(window, bg="#1F1F1F", height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        
        tk.Label(navbar, text="📊 RISK & ANALYTICS DASHBOARD",
                font=("Consolas", 14, "bold"), bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        tk.Frame(window, bg="#003300", height=1).pack(fill="x")
        
        # Main content
        content = tk.Frame(window, bg="#2E2E2E")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Top metrics row
        metrics_frame = tk.Frame(content, bg="#2E2E2E")
        metrics_frame.pack(fill="x", pady=(0, 20))
        
        self.metric_cards = []
        metrics = [
            ("Total Attacks", "0", "#FF4444"),
            ("Passwords Cracked", "0", "#FFAA00"),
            ("Phishing Clicks", "0", "#FF6666"),
            ("Avg Risk Score", "0", "#00FF66")
        ]
        
        for title, value, color in metrics:
            card = self.create_metric_card(metrics_frame, title, value, color)
            self.metric_cards.append(card)
        
        # Middle section - Charts
        charts_frame = tk.Frame(content, bg="#2E2E2E")
        charts_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Left chart - Password Analysis
        left_chart = tk.Frame(charts_frame, bg="#1F1F1F", relief="solid", bd=2)
        left_chart.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        tk.Label(left_chart, text="🔐 PASSWORD STRENGTH ANALYSIS", font=("Consolas", 12, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=10)
        
        self.password_chart = tk.Text(left_chart, bg="#000000", fg="#00FF66",
                                     font=("Consolas", 10, "bold"), relief="flat",
                                     padx=15, pady=15, wrap=tk.WORD, height=12)
        self.password_chart.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Right chart - Vulnerability Score
        right_chart = tk.Frame(charts_frame, bg="#1F1F1F", relief="solid", bd=2)
        right_chart.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        tk.Label(right_chart, text="⚠️ USER VULNERABILITY SCORES", font=("Consolas", 12, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=10)
        
        self.vulnerability_chart = tk.Text(right_chart, bg="#000000", fg="#00FF66",
                                          font=("Consolas", 10, "bold"), relief="flat",
                                          padx=15, pady=15, wrap=tk.WORD, height=12)
        self.vulnerability_chart.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Bottom section - Detailed reports
        reports_frame = tk.Frame(content, bg="#1F1F1F", relief="solid", bd=2)
        reports_frame.pack(fill="both", expand=True)
        
        tk.Label(reports_frame, text="📋 DETAILED ACTIVITY REPORT", font=("Consolas", 12, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=10)
        
        self.report_text = scrolledtext.ScrolledText(reports_frame, font=("Consolas", 10, "bold"),
                                                    bg="#000000", fg="#00FF66",
                                                    relief="flat", padx=15, pady=15, wrap=tk.WORD)
        self.report_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Refresh button
        refresh_btn = tk.Button(content, text="🔄 REFRESH ANALYTICS",
                               font=("Consolas", 12, "bold"), bg="#000000", fg="#00FF66",
                               activebackground="#003300", relief="solid", bd=2,
                               cursor="hand2", command=self.load_analytics)
        refresh_btn.pack(pady=(10, 0), ipady=10, ipadx=30)
        
        # Load initial data
        self.load_analytics()
    
    def create_metric_card(self, parent, title, value, color):
        """Create metric card"""
        card = tk.Frame(parent, bg="#1F1F1F", relief="solid", bd=2)
        card.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(card, text=title, font=("Consolas", 10, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=(10, 5))
        
        value_label = tk.Label(card, text=value, font=("Consolas", 24, "bold"),
                              bg="#1F1F1F", fg=color)
        value_label.pack(pady=(5, 10))
        
        return value_label
    
    def load_analytics(self):
        """Load analytics from all databases"""
        # Password attacks
        password_data = self.get_password_data()
        phishing_data = self.get_phishing_data()
        email_data = self.get_email_data()
        se_data = self.get_se_data()
        
        # Update metrics
        total_attacks = password_data['total']
        passwords_cracked = password_data['cracked']
        phishing_clicks = phishing_data['total']
        
        # Calculate average risk score
        all_scores = []
        if email_data['scores']:
            all_scores.extend(email_data['scores'])
        if se_data['scores']:
            all_scores.extend(se_data['scores'])
        
        avg_risk = sum(all_scores) / len(all_scores) if all_scores else 0
        
        self.metric_cards[0].config(text=str(total_attacks))
        self.metric_cards[1].config(text=str(passwords_cracked))
        self.metric_cards[2].config(text=str(phishing_clicks))
        self.metric_cards[3].config(text=f"{avg_risk:.0f}")
        
        # Update password chart
        self.update_password_chart(password_data)
        
        # Update vulnerability chart
        self.update_vulnerability_chart(password_data, phishing_data, se_data)
        
        # Update detailed report
        self.update_detailed_report(password_data, phishing_data, email_data, se_data)
    
    def get_password_data(self):
        """Get password attack data"""
        db_path = "cases/attack_results.db"
        if not os.path.exists(db_path):
            return {'total': 0, 'cracked': 0, 'passwords': [], 'users': []}
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT first_name, last_name, cracked_password, result FROM attack_results")
        results = cursor.fetchall()
        conn.close()
        
        cracked = sum(1 for r in results if r[2] and r[2] != 'N/A')
        passwords = [r[2] for r in results if r[2] and r[2] != 'N/A']
        users = [(r[0], r[1]) for r in results]
        
        return {'total': len(results), 'cracked': cracked, 'passwords': passwords, 'users': users}
    
    def get_phishing_data(self):
        """Get phishing campaign data"""
        db_path = "cases/phishing_campaigns.db"
        if not os.path.exists(db_path):
            return {'total': 0, 'clicked': 0, 'credentials': 0}
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT clicked, credentials_entered FROM campaigns")
        results = cursor.fetchall()
        conn.close()
        
        clicked = sum(r[0] for r in results if r[0])
        credentials = sum(r[1] for r in results if r[1])
        
        return {'total': len(results), 'clicked': clicked, 'credentials': credentials}
    
    def get_email_data(self):
        """Get email analysis data"""
        db_path = "cases/email_analysis.db"
        if not os.path.exists(db_path):
            return {'total': 0, 'malicious': 0, 'scores': []}
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT risk_score, classification FROM analyzed_emails")
        results = cursor.fetchall()
        conn.close()
        
        malicious = sum(1 for r in results if r[1] == 'MALICIOUS')
        scores = [r[0] for r in results if r[0]]
        
        return {'total': len(results), 'malicious': malicious, 'scores': scores}
    
    def get_se_data(self):
        """Get social engineering data"""
        db_path = "cases/social_engineering.db"
        if not os.path.exists(db_path):
            return {'total': 0, 'scores': []}
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT awareness_score FROM simulations")
        results = cursor.fetchall()
        conn.close()
        
        scores = [r[0] for r in results if r[0]]
        
        return {'total': len(results), 'scores': scores}
    
    def update_password_chart(self, data):
        """Update password strength chart"""
        self.password_chart.delete(1.0, tk.END)
        
        if not data['passwords']:
            self.password_chart.insert(tk.END, "⚠️ No password data available\n")
            return
        
        # Analyze password lengths
        lengths = [len(p) for p in data['passwords']]
        avg_length = sum(lengths) / len(lengths)
        
        # Analyze character types
        numeric_only = sum(1 for p in data['passwords'] if p.isdigit())
        alpha_only = sum(1 for p in data['passwords'] if p.isalpha())
        mixed = len(data['passwords']) - numeric_only - alpha_only
        
        self.password_chart.insert(tk.END, f"📊 ANALYSIS OF {len(data['passwords'])} CRACKED PASSWORDS\n\n")
        
        self.password_chart.insert(tk.END, f"Average Length: {avg_length:.1f} characters\n\n")
        
        self.password_chart.insert(tk.END, "Character Type Distribution:\n")
        self.password_chart.insert(tk.END, f"  Numeric only: {numeric_only} ({numeric_only/len(data['passwords'])*100:.1f}%)\n")
        self.password_chart.insert(tk.END, f"  Alpha only:   {alpha_only} ({alpha_only/len(data['passwords'])*100:.1f}%)\n")
        self.password_chart.insert(tk.END, f"  Mixed:        {mixed} ({mixed/len(data['passwords'])*100:.1f}%)\n\n")
        
        # Most common passwords
        common = Counter(data['passwords']).most_common(5)
        self.password_chart.insert(tk.END, "Most Common Passwords:\n")
        for pwd, count in common:
            self.password_chart.insert(tk.END, f"  • '{pwd}': {count} times\n")
    
    def update_vulnerability_chart(self, password_data, phishing_data, se_data):
        """Update vulnerability scores"""
        self.vulnerability_chart.delete(1.0, tk.END)
        
        # Calculate vulnerability scores per user
        user_scores = {}
        
        # From password attacks
        for first, last in password_data['users']:
            user = f"{first} {last}"
            if user not in user_scores:
                user_scores[user] = {'password': 0, 'phishing': 0, 'se': 0, 'total': 0}
            user_scores[user]['password'] += 30  # Vulnerable if attacked
        
        # Calculate overall scores
        for user, scores in user_scores.items():
            total = scores['password'] + scores['phishing'] + scores['se']
            user_scores[user]['total'] = min(total, 100)
        
        if not user_scores:
            self.vulnerability_chart.insert(tk.END, "⚠️ No user data available\n")
            return
        
        self.vulnerability_chart.insert(tk.END, f"👥 VULNERABILITY ASSESSMENT ({len(user_scores)} users)\n\n")
        
        # Sort by vulnerability
        sorted_users = sorted(user_scores.items(), key=lambda x: x[1]['total'], reverse=True)
        
        for user, scores in sorted_users[:10]:
            score = scores['total']
            if score >= 70:
                risk = "HIGH RISK"
                color = "🔴"
            elif score >= 40:
                risk = "MEDIUM RISK"
                color = "🟡"
            else:
                risk = "LOW RISK"
                color = "🟢"
            
            self.vulnerability_chart.insert(tk.END, f"{color} {user}\n")
            self.vulnerability_chart.insert(tk.END, f"   Score: {score}/100 - {risk}\n\n")
    
    def update_detailed_report(self, password_data, phishing_data, email_data, se_data):
        """Update detailed activity report"""
        self.report_text.delete(1.0, tk.END)
        
        self.report_text.insert(tk.END, "📋 COMPREHENSIVE SECURITY REPORT\n")
        self.report_text.insert(tk.END, "="*70 + "\n\n")
        
        # Password attacks section
        self.report_text.insert(tk.END, "🔐 PASSWORD ATTACK ANALYSIS\n")
        self.report_text.insert(tk.END, f"   Total Attacks: {password_data['total']}\n")
        self.report_text.insert(tk.END, f"   Successful Cracks: {password_data['cracked']}\n")
        if password_data['total'] > 0:
            success_rate = password_data['cracked'] / password_data['total'] * 100
            self.report_text.insert(tk.END, f"   Success Rate: {success_rate:.1f}%\n")
        self.report_text.insert(tk.END, "\n")
        
        # Phishing section
        self.report_text.insert(tk.END, "📧 PHISHING CAMPAIGN ANALYSIS\n")
        self.report_text.insert(tk.END, f"   Total Campaigns: {phishing_data['total']}\n")
        self.report_text.insert(tk.END, f"   Clicks: {phishing_data['clicked']}\n")
        self.report_text.insert(tk.END, f"   Credentials Entered: {phishing_data['credentials']}\n")
        if phishing_data['clicked'] > 0:
            cred_rate = phishing_data['credentials'] / phishing_data['clicked'] * 100
            self.report_text.insert(tk.END, f"   Credential Entry Rate: {cred_rate:.1f}%\n")
        self.report_text.insert(tk.END, "\n")
        
        # Email analysis section
        self.report_text.insert(tk.END, "🔍 EMAIL ANALYSIS\n")
        self.report_text.insert(tk.END, f"   Emails Analyzed: {email_data['total']}\n")
        self.report_text.insert(tk.END, f"   Malicious Detected: {email_data['malicious']}\n")
        if email_data['scores']:
            avg_risk = sum(email_data['scores']) / len(email_data['scores'])
            self.report_text.insert(tk.END, f"   Average Risk Score: {avg_risk:.1f}/100\n")
        self.report_text.insert(tk.END, "\n")
        
        # Social engineering section
        self.report_text.insert(tk.END, "📞 SOCIAL ENGINEERING SIMULATIONS\n")
        self.report_text.insert(tk.END, f"   Total Simulations: {se_data['total']}\n")
        if se_data['scores']:
            avg_awareness = sum(se_data['scores']) / len(se_data['scores'])
            self.report_text.insert(tk.END, f"   Average Awareness Score: {avg_awareness:.1f}/100\n")
        self.report_text.insert(tk.END, "\n")
        
        self.report_text.insert(tk.END, "="*70 + "\n\n")
        
        # Recommendations
        self.report_text.insert(tk.END, "💡 RECOMMENDATIONS\n\n")
        
        if password_data['cracked'] > 0:
            self.report_text.insert(tk.END, "• Implement stronger password policies\n")
            self.report_text.insert(tk.END, "• Require multi-factor authentication\n")
        
        if phishing_data['credentials'] > 0:
            self.report_text.insert(tk.END, "• Conduct phishing awareness training\n")
            self.report_text.insert(tk.END, "• Implement email filtering solutions\n")
        
        if email_data['malicious'] > 0:
            self.report_text.insert(tk.END, "• Deploy advanced email security tools\n")
        
        if se_data['scores'] and sum(se_data['scores'])/len(se_data['scores']) < 70:
            self.report_text.insert(tk.END, "• Increase social engineering awareness training\n")


if __name__ == "__main__":
    root = tk.Tk()
    AnalyticsDashboard(root)
    root.mainloop()
