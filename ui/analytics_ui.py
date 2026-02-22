import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.case_database import get_case_analytics, get_password_attacks, get_email_analysis, get_domain_verification, get_phishing_campaigns, get_voice_analysis

class AnalyticsDashboard:
    def __init__(self, window, case_name):
        self.window = window
        self.case_name = case_name
        self.window.title(f"Risk & Analytics Dashboard - {case_name}")
        self.window.geometry("1400x800")
        self.window.configure(bg="#2E2E2E")
        
        self.analytics = get_case_analytics(case_name)
        self._build_ui()
    
    def _build_ui(self):
        # Top Navigation Bar
        navbar = tk.Frame(self.window, bg="#1F1F1F", height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        
        tk.Label(navbar, text=f"Risk & Analytics Dashboard - Case: {self.case_name}",
                font=("Consolas", 14, "bold"), bg="#1F1F1F", fg="#00FF66").pack(side="left", padx=20, pady=15)
        
        tk.Button(navbar, text="🔄 Refresh", font=("Consolas", 10, "bold"),
                 bg="#000000", fg="#00FF66", relief="solid", bd=1,
                 cursor="hand2", command=self._refresh_data).pack(side="right", padx=20)
        
        tk.Frame(self.window, bg="#003300", height=1).pack(fill="x")
        
        # Main content with scrollbar
        main_canvas = tk.Canvas(self.window, bg="#2E2E2E", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.window, orient="vertical", command=main_canvas.yview)
        scroll_frame = tk.Frame(main_canvas, bg="#2E2E2E")
        
        scroll_frame.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
        main_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        content = scroll_frame
        
        # Overall Risk Score
        risk_frame = tk.Frame(content, bg="#1F1F1F", relief="solid", bd=2)
        risk_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(risk_frame, text="OVERALL RISK SCORE", font=("Consolas", 16, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=(15, 5))
        
        risk_score = self.analytics["overall_risk_score"]
        risk_color = "#00FF66" if risk_score < 30 else "#FFAA00" if risk_score < 70 else "#FF4444"
        
        tk.Label(risk_frame, text=f"{risk_score}%", font=("Consolas", 48, "bold"),
                bg="#1F1F1F", fg=risk_color).pack(pady=10)
        
        risk_level = "LOW RISK" if risk_score < 30 else "MEDIUM RISK" if risk_score < 70 else "HIGH RISK"
        tk.Label(risk_frame, text=risk_level, font=("Consolas", 14, "bold"),
                bg="#1F1F1F", fg=risk_color).pack(pady=(0, 15))
        
        # Module Cards Grid
        cards_container = tk.Frame(content, bg="#2E2E2E")
        cards_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Row 1
        row1 = tk.Frame(cards_container, bg="#2E2E2E")
        row1.pack(fill="x", pady=(0, 10))
        
        self._create_module_card(row1, "🔐 PASSWORD ATTACKS", self.analytics["password_attacks"], "left")
        self._create_module_card(row1, "📧 EMAIL ANALYSIS", self.analytics["email_analysis"], "left")
        self._create_module_card(row1, "🌐 DOMAIN VERIFICATION", self.analytics["domain_verification"], "left")
        
        # Row 2
        row2 = tk.Frame(cards_container, bg="#2E2E2E")
        row2.pack(fill="x", pady=(0, 10))
        
        self._create_module_card(row2, "🎣 PHISHING CAMPAIGNS", self.analytics["phishing_campaigns"], "left")
        self._create_module_card(row2, "📞 VOICE ANALYSIS", self.analytics["voice_analysis"], "left")
        
        # Detailed Reports
        details_frame = tk.Frame(content, bg="#1F1F1F", relief="solid", bd=2)
        details_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        tk.Label(details_frame, text="DETAILED MODULE REPORTS", font=("Consolas", 14, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        # Tabs for each module
        tab_frame = tk.Frame(details_frame, bg="#1F1F1F")
        tab_frame.pack(fill="x", padx=10)
        
        self.current_tab = "password"
        
        tabs = [
            ("Password Attacks", "password"),
            ("Email Analysis", "email"),
            ("Domain Verification", "domain"),
            ("Phishing Campaigns", "phishing"),
            ("Voice Analysis", "voice")
        ]
        
        for tab_name, tab_id in tabs:
            btn = tk.Button(tab_frame, text=tab_name, font=("Consolas", 10, "bold"),
                           bg="#000000" if self.current_tab == tab_id else "#2E2E2E",
                           fg="#00FF66", relief="flat", cursor="hand2",
                           command=lambda tid=tab_id: self._switch_tab(tid))
            btn.pack(side="left", padx=2, pady=5, ipadx=10, ipady=5)
        
        # Tab content
        self.tab_content = tk.Frame(details_frame, bg="#000000", relief="solid", bd=1)
        self.tab_content.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self._show_tab_content("password")
    
    def _create_module_card(self, parent, title, data, side):
        card = tk.Frame(parent, bg="#1F1F1F", relief="solid", bd=2, width=400)
        card.pack(side=side, fill="both", expand=True, padx=5)
        
        tk.Label(card, text=title, font=("Consolas", 12, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=(10, 5))
        
        tk.Frame(card, bg="#003300", height=1).pack(fill="x", padx=10)
        
        stats_frame = tk.Frame(card, bg="#1F1F1F")
        stats_frame.pack(fill="both", expand=True, pady=10)
        
        if "total" in data:
            self._add_stat(stats_frame, "Total", data["total"])
        
        if "cracked" in data:
            self._add_stat(stats_frame, "Cracked", data["cracked"], "#FF4444")
            self._add_stat(stats_frame, "Failed", data["failed"], "#00FF66")
            self._add_stat(stats_frame, "Crack Rate", f"{data['crack_rate']}%", "#FFAA00")
        
        if "phishing" in data:
            self._add_stat(stats_frame, "Phishing", data["phishing"], "#FF4444")
            self._add_stat(stats_frame, "Suspicious", data["suspicious"], "#FFAA00")
            self._add_stat(stats_frame, "Safe", data["safe"], "#00FF66")
            self._add_stat(stats_frame, "Avg Risk", f"{data['avg_risk_score']}%", "#FFAA00")
        
        if "high_risk" in data and "suspicious" in data and "safe" in data:
            self._add_stat(stats_frame, "High Risk", data["high_risk"], "#FF4444")
            self._add_stat(stats_frame, "Suspicious", data["suspicious"], "#FFAA00")
            self._add_stat(stats_frame, "Safe", data["safe"], "#00FF66")
        
        if "sent" in data:
            self._add_stat(stats_frame, "Sent", data["sent"], "#FFAA00")
        
        if "avg_risk_score" in data and "phishing" not in data:
            self._add_stat(stats_frame, "Avg Risk", f"{data['avg_risk_score']}%", "#FFAA00")
    
    def _add_stat(self, parent, label, value, color="#00FF66"):
        row = tk.Frame(parent, bg="#1F1F1F")
        row.pack(fill="x", padx=15, pady=2)
        
        tk.Label(row, text=f"{label}:", font=("Consolas", 10, "bold"),
                bg="#1F1F1F", fg="#666666", anchor="w").pack(side="left")
        
        tk.Label(row, text=str(value), font=("Consolas", 10, "bold"),
                bg="#1F1F1F", fg=color, anchor="e").pack(side="right")
    
    def _switch_tab(self, tab_id):
        self.current_tab = tab_id
        self._show_tab_content(tab_id)
    
    def _show_tab_content(self, tab_id):
        for widget in self.tab_content.winfo_children():
            widget.destroy()
        
        text_widget = tk.Text(self.tab_content, bg="#000000", fg="#00FF66",
                             font=("Consolas", 10, "bold"), wrap="word",
                             padx=15, pady=15)
        text_widget.pack(fill="both", expand=True)
        
        if tab_id == "password":
            attacks = get_password_attacks(self.case_name)
            if attacks:
                for i, attack in enumerate(attacks, 1):
                    text_widget.insert("end", f"[{i}] Password Attack\n", "header")
                    text_widget.insert("end", f"Name: {attack[1]} {attack[2]}\n")
                    text_widget.insert("end", f"Attack Type: {attack[5]}\n")
                    text_widget.insert("end", f"Algorithm: {attack[6]}\n")
                    text_widget.insert("end", f"Result: {attack[7]}\n")
                    text_widget.insert("end", f"Cracked Password: {attack[8]}\n")
                    text_widget.insert("end", f"Timestamp: {attack[9]}\n")
                    text_widget.insert("end", "-" * 80 + "\n\n")
            else:
                text_widget.insert("end", "No password attacks recorded for this case.\n")
        
        elif tab_id == "email":
            emails = get_email_analysis(self.case_name)
            if emails:
                for i, email in enumerate(emails, 1):
                    text_widget.insert("end", f"[{i}] Email Analysis\n", "header")
                    text_widget.insert("end", f"Type: {email[1]}\n")
                    text_widget.insert("end", f"Sender: {email[2]}\n")
                    text_widget.insert("end", f"Subject: {email[3]}\n")
                    text_widget.insert("end", f"Risk Score: {email[5]}%\n")
                    text_widget.insert("end", f"Classification: {email[6]}\n")
                    text_widget.insert("end", f"Timestamp: {email[8]}\n")
                    text_widget.insert("end", "-" * 80 + "\n\n")
            else:
                text_widget.insert("end", "No email analysis recorded for this case.\n")
        
        elif tab_id == "domain":
            domains = get_domain_verification(self.case_name)
            if domains:
                for i, domain in enumerate(domains, 1):
                    text_widget.insert("end", f"[{i}] Domain Verification\n", "header")
                    text_widget.insert("end", f"Domain: {domain[1]}\n")
                    text_widget.insert("end", f"SSL Valid: {'Yes' if domain[2] else 'No'}\n")
                    text_widget.insert("end", f"DNS Resolved: {'Yes' if domain[3] else 'No'}\n")
                    text_widget.insert("end", f"Spoofed: {'Yes' if domain[4] else 'No'}\n")
                    text_widget.insert("end", f"Risk Level: {domain[5]}\n")
                    text_widget.insert("end", f"Timestamp: {domain[7]}\n")
                    text_widget.insert("end", "-" * 80 + "\n\n")
            else:
                text_widget.insert("end", "No domain verification recorded for this case.\n")
        
        elif tab_id == "phishing":
            campaigns = get_phishing_campaigns(self.case_name)
            if campaigns:
                for i, campaign in enumerate(campaigns, 1):
                    text_widget.insert("end", f"[{i}] Phishing Campaign\n", "header")
                    text_widget.insert("end", f"From: {campaign[1]} <{campaign[2]}>\n")
                    text_widget.insert("end", f"To: {campaign[3]}\n")
                    text_widget.insert("end", f"Subject: {campaign[4]}\n")
                    text_widget.insert("end", f"Template: {campaign[5]}\n")
                    text_widget.insert("end", f"Status: {campaign[6]}\n")
                    text_widget.insert("end", f"Timestamp: {campaign[7]}\n")
                    text_widget.insert("end", "-" * 80 + "\n\n")
            else:
                text_widget.insert("end", "No phishing campaigns recorded for this case.\n")
        
        elif tab_id == "voice":
            voices = get_voice_analysis(self.case_name)
            if voices:
                for i, voice in enumerate(voices, 1):
                    text_widget.insert("end", f"[{i}] Voice Analysis\n", "header")
                    text_widget.insert("end", f"Caller: {voice[1]}\n")
                    text_widget.insert("end", f"Scenario: {voice[2]}\n")
                    text_widget.insert("end", f"Risk Score: {voice[3]}%\n")
                    text_widget.insert("end", f"Manipulation Detected: {'Yes' if voice[4] else 'No'}\n")
                    text_widget.insert("end", f"Timestamp: {voice[6]}\n")
                    text_widget.insert("end", "-" * 80 + "\n\n")
            else:
                text_widget.insert("end", "No voice analysis recorded for this case.\n")
        
        text_widget.config(state="disabled")
    
    def _refresh_data(self):
        self.analytics = get_case_analytics(self.case_name)
        for widget in self.window.winfo_children():
            widget.destroy()
        self._build_ui()


if __name__ == "__main__":
    root = tk.Tk()
    AnalyticsDashboard(root, "Test_Case")
    root.mainloop()
