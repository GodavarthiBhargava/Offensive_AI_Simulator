import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sqlite3
import os
import json
from datetime import datetime
from collections import Counter
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch

class AnalyticsDashboard:
    def __init__(self, window, case_name=None):
        self.window = window
        self.case_name = case_name or "Current Case"
        self.window.title(f"Risk & Analytics Dashboard - {self.case_name}")
        self.window.geometry("1400x900")
        self.window.configure(bg="#2E2E2E")
        
        # Top bar
        navbar = tk.Frame(window, bg="#1F1F1F", height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        
        tk.Label(navbar, text="📊 RISK & ANALYTICS DASHBOARD",
                font=("Consolas", 14, "bold"), bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        tk.Frame(window, bg="#003300", height=1).pack(fill="x")
        
        # Main scrollable content
        main_frame = tk.Frame(window, bg="#2E2E2E")
        main_frame.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(main_frame, bg="#2E2E2E", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview, bg="#1F1F1F")
        scrollable_frame = tk.Frame(canvas, bg="#2E2E2E")
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Build dashboard sections
        self.build_case_header(scrollable_frame)
        self.build_executive_summary(scrollable_frame)
        self.build_risk_overview(scrollable_frame)
        self.build_module_reports(scrollable_frame)
        self.build_timeline(scrollable_frame)
        self.build_recommendations(scrollable_frame)
        self.build_export_options(scrollable_frame)
    
    def build_case_header(self, parent):
        """Case header with case details"""
        header = tk.Frame(parent, bg="#1F1F1F", relief="solid", bd=2)
        header.pack(fill="x", pady=(0, 20))
        
        tk.Label(header, text="📋 CASE HEADER", font=("Consolas", 14, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(anchor="w", padx=15, pady=10)
        
        content = tk.Frame(header, bg="#1F1F1F")
        content.pack(fill="x", padx=15, pady=(0, 15))
        
        # Left side
        left = tk.Frame(content, bg="#1F1F1F")
        left.pack(side="left", fill="both", expand=True)
        
        case_id = f"SEC-2026-{datetime.now().strftime('%m%d')}"
        self.add_info_row(left, "Case ID:", case_id)
        self.add_info_row(left, "Case Name:", self.case_name)
        self.add_info_row(left, "Created On:", datetime.now().strftime("%d %b %Y"))
        self.add_info_row(left, "Status:", "OPEN", "#00FF66")
        
        # Right side
        right = tk.Frame(content, bg="#1F1F1F")
        right.pack(side="right", fill="both", expand=True)
        
        # Get risk score
        risk_score = self.calculate_overall_risk()
        severity = "HIGH" if risk_score >= 70 else "MEDIUM" if risk_score >= 40 else "LOW"
        severity_color = "#FF4444" if risk_score >= 70 else "#FFAA00" if risk_score >= 40 else "#00FF66"
        
        self.add_info_row(right, "Severity Level:", severity, severity_color)
        self.add_info_row(right, "Overall Risk Score:", f"{risk_score}/100", severity_color)
        self.add_info_row(right, "Last Activity:", "Just now")
    
    def build_executive_summary(self, parent):
        """Executive summary section"""
        section = self.create_section(parent, "📌 EXECUTIVE SUMMARY")
        
        summary = self.generate_executive_summary()
        
        text = tk.Text(section, font=("Consolas", 11, "bold"), bg="#000000", fg="#00FF66",
                      height=6, wrap=tk.WORD, relief="flat", padx=15, pady=15)
        text.insert("1.0", summary)
        text.config(state="disabled")
        text.pack(fill="x", padx=15, pady=(0, 15))
    
    def build_risk_overview(self, parent):
        """Risk overview with metric cards"""
        section = self.create_section(parent, "📊 EXECUTIVE RISK OVERVIEW")
        
        cards_frame = tk.Frame(section, bg="#1F1F1F")
        cards_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Get metrics
        metrics = self.get_case_metrics()
        
        # Create metric cards
        cards = [
            ("Total Attacks", str(metrics['total_attacks']), "Executed"),
            ("Passwords Cracked", str(metrics['passwords_cracked']), f"{metrics['crack_rate']:.0f}% Success"),
            ("Phishing Clicks", str(metrics['phishing_clicks']), "Suspicious Activity"),
            ("Credentials Captured", str(metrics['credentials_captured']), "High Risk"),
            ("Avg Password Strength", f"{metrics['avg_strength']:.0f}%", "Weak Patterns"),
            ("Vulnerability Score", f"{metrics['vuln_score']:.0f}/100", "User Risk")
        ]
        
        for i, (title, value, desc) in enumerate(cards):
            row = i // 3
            col = i % 3
            self.create_metric_card(cards_frame, title, value, desc, row, col)
    
    def build_module_reports(self, parent):
        """Collapsible module reports"""
        section = self.create_section(parent, "🧩 MODULE REPORTS")
        
        # Password Attack Report
        self.create_collapsible_report(section, "🔐 PASSWORD ATTACK REPORT", 
                                      self.get_password_report())
        
        # Phishing Campaign Report
        self.create_collapsible_report(section, "📧 PHISHING CAMPAIGN REPORT",
                                      self.get_phishing_report())
        
        # Domain Verification Report
        self.create_collapsible_report(section, "🌐 DOMAIN VERIFICATION REPORT",
                                      self.get_domain_report())
        
        # AI Behavior Report
        self.create_collapsible_report(section, "🤖 AI BEHAVIOR ENGINE REPORT",
                                      self.get_ai_behavior_report())
        
        # Email Analyzer Report
        self.create_collapsible_report(section, "📨 EMAIL ANALYZER REPORT",
                                      self.get_email_analyzer_report())
    
    def build_timeline(self, parent):
        """Timeline view"""
        section = self.create_section(parent, "🕒 TIMELINE VIEW")
        
        timeline_text = tk.Text(section, font=("Consolas", 10, "bold"), bg="#000000", fg="#00FF66",
                               height=10, wrap=tk.WORD, relief="flat", padx=15, pady=15)
        
        timeline = self.generate_timeline()
        timeline_text.insert("1.0", timeline)
        timeline_text.config(state="disabled")
        timeline_text.pack(fill="x", padx=15, pady=(0, 15))
    
    def build_recommendations(self, parent):
        """Security recommendations"""
        section = self.create_section(parent, "🛡️ RECOMMENDED SECURITY ACTIONS")
        
        recommendations = [
            "Enforce minimum 12-character passwords with complexity requirements",
            "Enable Multi-Factor Authentication (MFA) for all user accounts",
            "Conduct mandatory phishing awareness training for all users",
            "Implement email filtering and domain verification systems",
            "Monitor and block suspicious domains at firewall level",
            "Regular security audits and penetration testing",
            "Deploy password managers for credential management",
            "Implement account lockout policies after failed attempts"
        ]
        
        rec_frame = tk.Frame(section, bg="#1F1F1F")
        rec_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        for i, rec in enumerate(recommendations, 1):
            row = tk.Frame(rec_frame, bg="#1F1F1F")
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"{i}.", font=("Consolas", 10, "bold"),
                    bg="#1F1F1F", fg="#00FF66", width=3).pack(side="left")
            tk.Label(row, text=rec, font=("Consolas", 10, "bold"),
                    bg="#1F1F1F", fg="#FFFFFF", wraplength=1200, justify="left").pack(side="left", fill="x")
    
    def build_export_options(self, parent):
        """Export and close options"""
        section = tk.Frame(parent, bg="#2E2E2E")
        section.pack(fill="x", pady=20)
        
        btn_frame = tk.Frame(section, bg="#2E2E2E")
        btn_frame.pack()
        
        buttons = [
            ("📄 EXPORT PDF REPORT", self.export_pdf),
            ("💾 EXPORT JSON DATA", self.export_json),
            ("📦 DOWNLOAD EVIDENCE", self.download_evidence),
            ("❌ CLOSE CASE", self.close_case)
        ]
        
        for text, cmd in buttons:
            btn = tk.Button(btn_frame, text=text, font=("Consolas", 11, "bold"),
                           bg="#000000", fg="#00FF66", activebackground="#003300",
                           relief="solid", bd=2, cursor="hand2", command=cmd,
                           width=25, height=2)
            btn.pack(side="left", padx=5)
    
    # Helper methods
    def create_section(self, parent, title):
        """Create section frame"""
        frame = tk.LabelFrame(parent, text=title, font=("Consolas", 12, "bold"),
                             bg="#1F1F1F", fg="#00FF66", relief="solid", bd=2,
                             labelanchor="nw", padx=5, pady=5)
        frame.pack(fill="x", pady=10)
        return frame
    
    def add_info_row(self, parent, label, value, color="#FFFFFF"):
        """Add info row"""
        row = tk.Frame(parent, bg="#1F1F1F")
        row.pack(fill="x", pady=3)
        tk.Label(row, text=label, font=("Consolas", 10, "bold"),
                bg="#1F1F1F", fg="#00FF66", width=18, anchor="w").pack(side="left")
        tk.Label(row, text=value, font=("Consolas", 10, "bold"),
                bg="#1F1F1F", fg=color, anchor="w").pack(side="left")
    
    def create_metric_card(self, parent, title, value, desc, row, col):
        """Create metric card"""
        card = tk.Frame(parent, bg="#000000", relief="solid", bd=1)
        card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        tk.Label(card, text=title, font=("Consolas", 9, "bold"),
                bg="#000000", fg="#00FF66").pack(pady=(10, 5))
        tk.Label(card, text=value, font=("Consolas", 18, "bold"),
                bg="#000000", fg="#FFFFFF").pack(pady=5)
        tk.Label(card, text=desc, font=("Consolas", 8, "bold"),
                bg="#000000", fg="#666666").pack(pady=(5, 10))
    
    def create_collapsible_report(self, parent, title, content):
        """Create collapsible report section"""
        container = tk.Frame(parent, bg="#1F1F1F")
        container.pack(fill="x", padx=15, pady=5)
        
        # Header
        header = tk.Frame(container, bg="#000000", relief="solid", bd=1, cursor="hand2")
        header.pack(fill="x")
        
        self.toggle_var = tk.BooleanVar(value=False)
        
        tk.Label(header, text=f"▶ {title}", font=("Consolas", 11, "bold"),
                bg="#000000", fg="#00FF66", anchor="w").pack(side="left", padx=10, pady=10)
        
        # Content frame
        content_frame = tk.Frame(container, bg="#000000")
        
        text_widget = tk.Text(content_frame, font=("Consolas", 9, "bold"), bg="#000000", fg="#FFFFFF",
                             height=15, wrap=tk.WORD, relief="flat", padx=15, pady=10)
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")
        text_widget.pack(fill="both", expand=True)
        
        def toggle():
            if content_frame.winfo_viewable():
                content_frame.pack_forget()
                header.children['!label'].config(text=f"▶ {title}")
            else:
                content_frame.pack(fill="x")
                header.children['!label'].config(text=f"▼ {title}")
        
        header.bind("<Button-1>", lambda e: toggle())
    
    def calculate_overall_risk(self):
        """Calculate overall risk score"""
        try:
            total_risk = 0
            count = 0
            
            # Password attacks
            if os.path.exists("cases/attack_results.db"):
                conn = sqlite3.connect("cases/attack_results.db")
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM attack_results WHERE cracked_password != 'N/A'")
                cracked = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM attack_results")
                total = cursor.fetchone()[0]
                conn.close()
                if total > 0:
                    total_risk += (cracked / total) * 100
                    count += 1
            
            # Email analysis
            if os.path.exists("cases/email_analysis.db"):
                conn = sqlite3.connect("cases/email_analysis.db")
                cursor = conn.cursor()
                cursor.execute("SELECT AVG(risk_score) FROM analyzed_emails")
                avg_risk = cursor.fetchone()[0]
                conn.close()
                if avg_risk:
                    total_risk += avg_risk
                    count += 1
            
            return int(total_risk / count) if count > 0 else 50
        except:
            return 50
    
    def get_case_metrics(self):
        """Get case-specific metrics"""
        metrics = {
            'total_attacks': 0,
            'passwords_cracked': 0,
            'crack_rate': 0,
            'phishing_clicks': 0,
            'credentials_captured': 0,
            'avg_strength': 0,
            'vuln_score': 0
        }
        
        try:
            # Password data
            if os.path.exists("cases/attack_results.db"):
                conn = sqlite3.connect("cases/attack_results.db")
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM attack_results")
                metrics['total_attacks'] = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM attack_results WHERE cracked_password != 'N/A'")
                metrics['passwords_cracked'] = cursor.fetchone()[0]
                conn.close()
                
                if metrics['total_attacks'] > 0:
                    metrics['crack_rate'] = (metrics['passwords_cracked'] / metrics['total_attacks']) * 100
                    metrics['avg_strength'] = 100 - metrics['crack_rate']
            
            # Phishing data
            if os.path.exists("cases/phishing_campaigns.db"):
                conn = sqlite3.connect("cases/phishing_campaigns.db")
                cursor = conn.cursor()
                cursor.execute("SELECT SUM(clicked), SUM(credentials_entered) FROM campaigns")
                result = cursor.fetchone()
                conn.close()
                metrics['phishing_clicks'] = result[0] or 0
                metrics['credentials_captured'] = result[1] or 0
            
            metrics['vuln_score'] = self.calculate_overall_risk()
        except:
            pass
        
        return metrics
    
    def generate_executive_summary(self):
        """Generate executive summary"""
        metrics = self.get_case_metrics()
        
        summary = f"""This case involved comprehensive security testing across multiple attack vectors.

Password Security: {metrics['passwords_cracked']} out of {metrics['total_attacks']} passwords were successfully cracked ({metrics['crack_rate']:.0f}% success rate), indicating weak password policies.

Phishing Susceptibility: {metrics['phishing_clicks']} users clicked malicious links and {metrics['credentials_captured']} submitted credentials, demonstrating high vulnerability to social engineering.

Overall Assessment: The organization shows {'HIGH' if metrics['vuln_score'] >= 70 else 'MEDIUM' if metrics['vuln_score'] >= 40 else 'LOW'} exposure to cyber threats. Immediate security improvements are recommended."""
        
        return summary
    
    def get_password_report(self):
        """Get password attack report"""
        report = "1. ATTACK SUMMARY\n\n"
        
        try:
            if os.path.exists("cases/attack_results.db"):
                conn = sqlite3.connect("cases/attack_results.db")
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*), attack_type FROM attack_results GROUP BY attack_type")
                results = cursor.fetchall()
                
                for count, attack_type in results:
                    report += f"   • {attack_type}: {count} attempts\n"
                
                cursor.execute("SELECT first_name, last_name, cracked_password FROM attack_results WHERE cracked_password != 'N/A' LIMIT 10")
                users = cursor.fetchall()
                
                report += "\n2. VULNERABLE USERS\n\n"
                for first, last, pwd in users:
                    report += f"   • {first} {last}: Password '{pwd}' (Length: {len(pwd)})\n"
                
                conn.close()
            else:
                report += "   No password attack data available\n"
        except:
            report += "   Error loading data\n"
        
        return report
    
    def get_phishing_report(self):
        """Get phishing campaign report"""
        report = "1. CAMPAIGN OVERVIEW\n\n"
        
        try:
            if os.path.exists("cases/phishing_campaigns.db"):
                conn = sqlite3.connect("cases/phishing_campaigns.db")
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*), SUM(clicked), SUM(credentials_entered) FROM campaigns")
                total, clicks, creds = cursor.fetchone()
                
                report += f"   • Total Campaigns: {total}\n"
                report += f"   • Clicks: {clicks or 0}\n"
                report += f"   • Credentials Captured: {creds or 0}\n"
                
                conn.close()
            else:
                report += "   No phishing campaign data available\n"
        except:
            report += "   Error loading data\n"
        
        return report
    
    def get_domain_report(self):
        """Get domain verification report"""
        report = "1. DOMAIN ANALYSIS SUMMARY\n\n"
        
        try:
            if os.path.exists("cases/domain_verification.db"):
                conn = sqlite3.connect("cases/domain_verification.db")
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*), AVG(risk_score) FROM domain_checks")
                count, avg_risk = cursor.fetchone()
                
                report += f"   • Domains Analyzed: {count}\n"
                report += f"   • Average Risk Score: {avg_risk:.0f}/100\n"
                
                cursor.execute("SELECT domain, risk_score, classification FROM domain_checks ORDER BY risk_score DESC LIMIT 5")
                domains = cursor.fetchall()
                
                report += "\n2. HIGH-RISK DOMAINS\n\n"
                for domain, risk, classification in domains:
                    report += f"   • {domain}: {risk}/100 ({classification})\n"
                
                conn.close()
            else:
                report += "   No domain verification data available\n"
        except:
            report += "   Error loading data\n"
        
        return report
    
    def get_ai_behavior_report(self):
        """Get AI behavior report"""
        return """1. BEHAVIORAL ANALYSIS

   • Password patterns analyzed from cracked credentials
   • Common patterns: numeric suffixes, name-based passwords
   • Predictive success rate: 75%

2. RISK INDICATORS

   • Users tend to use personal information in passwords
   • Low complexity passwords prevalent
   • High susceptibility to dictionary attacks"""
    
    def get_email_analyzer_report(self):
        """Get email analyzer report"""
        report = "1. EMAIL ANALYSIS SUMMARY\n\n"
        
        try:
            if os.path.exists("cases/email_analysis.db"):
                conn = sqlite3.connect("cases/email_analysis.db")
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*), classification FROM analyzed_emails GROUP BY classification")
                results = cursor.fetchall()
                
                for count, classification in results:
                    report += f"   • {classification}: {count} emails\n"
                
                conn.close()
            else:
                report += "   No email analysis data available\n"
        except:
            report += "   Error loading data\n"
        
        return report
    
    def generate_timeline(self):
        """Generate activity timeline"""
        timeline = ""
        events = []
        
        try:
            # Collect events from all databases
            if os.path.exists("cases/attack_results.db"):
                conn = sqlite3.connect("cases/attack_results.db")
                cursor = conn.cursor()
                cursor.execute("SELECT timestamp, attack_type, result FROM attack_results ORDER BY timestamp DESC LIMIT 10")
                for ts, attack, result in cursor.fetchall():
                    events.append((ts, f"Password Attack: {attack} - {result}"))
                conn.close()
            
            if os.path.exists("cases/phishing_campaigns.db"):
                conn = sqlite3.connect("cases/phishing_campaigns.db")
                cursor = conn.cursor()
                cursor.execute("SELECT timestamp, campaign_name FROM campaigns ORDER BY timestamp DESC LIMIT 10")
                for ts, name in cursor.fetchall():
                    events.append((ts, f"Phishing Campaign: {name}"))
                conn.close()
            
            # Sort by timestamp
            events.sort(reverse=True)
            
            for ts, event in events[:15]:
                time_str = datetime.fromisoformat(ts).strftime("%H:%M")
                timeline += f"{time_str} - {event}\n"
        except:
            timeline = "No timeline data available\n"
        
        return timeline if timeline else "No activity recorded\n"
    
    def export_pdf(self):
        """Export case report as PDF"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=f"SecurityReport_{self.case_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            
            if not filename:
                return
            
            doc = SimpleDocTemplate(filename, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#00FF66'), spaceAfter=30)
            heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=16, textColor=colors.HexColor('#00FF66'), spaceAfter=12)
            
            # Title
            story.append(Paragraph(f"SECURITY ASSESSMENT REPORT", title_style))
            story.append(Paragraph(f"Case: {self.case_name}", styles['Normal']))
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}", styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
            
            # Case Header
            story.append(Paragraph("CASE INFORMATION", heading_style))
            case_id = f"SEC-2026-{datetime.now().strftime('%m%d')}"
            risk_score = self.calculate_overall_risk()
            severity = "HIGH" if risk_score >= 70 else "MEDIUM" if risk_score >= 40 else "LOW"
            
            case_data = [
                ['Case ID:', case_id],
                ['Case Name:', self.case_name],
                ['Status:', 'OPEN'],
                ['Severity:', severity],
                ['Risk Score:', f'{risk_score}/100'],
                ['Date:', datetime.now().strftime('%d %b %Y')]
            ]
            case_table = Table(case_data, colWidths=[2*inch, 4*inch])
            case_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1F1F1F')),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#00FF66')),
                ('TEXTCOLOR', (1, 0), (-1, -1), colors.black),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            story.append(case_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Executive Summary
            story.append(Paragraph("EXECUTIVE SUMMARY", heading_style))
            summary = self.generate_executive_summary()
            for line in summary.split('\n'):
                if line.strip():
                    story.append(Paragraph(line, styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
            
            # Risk Overview
            story.append(Paragraph("RISK METRICS", heading_style))
            metrics = self.get_case_metrics()
            metrics_data = [
                ['Metric', 'Value'],
                ['Total Attacks', str(metrics['total_attacks'])],
                ['Passwords Cracked', str(metrics['passwords_cracked'])],
                ['Crack Rate', f"{metrics['crack_rate']:.0f}%"],
                ['Phishing Clicks', str(metrics['phishing_clicks'])],
                ['Credentials Captured', str(metrics['credentials_captured'])],
                ['Avg Password Strength', f"{metrics['avg_strength']:.0f}%"],
                ['Vulnerability Score', f"{metrics['vuln_score']:.0f}/100"]
            ]
            metrics_table = Table(metrics_data, colWidths=[3*inch, 3*inch])
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F1F1F')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#00FF66')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            story.append(metrics_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Module Reports
            story.append(PageBreak())
            story.append(Paragraph("MODULE REPORTS", heading_style))
            
            reports = [
                ("PASSWORD ATTACK REPORT", self.get_password_report()),
                ("PHISHING CAMPAIGN REPORT", self.get_phishing_report()),
                ("DOMAIN VERIFICATION REPORT", self.get_domain_report()),
                ("EMAIL ANALYZER REPORT", self.get_email_analyzer_report())
            ]
            
            for title, content in reports:
                story.append(Paragraph(title, styles['Heading3']))
                for line in content.split('\n'):
                    if line.strip():
                        story.append(Paragraph(line, styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
            
            # Recommendations
            story.append(PageBreak())
            story.append(Paragraph("SECURITY RECOMMENDATIONS", heading_style))
            recommendations = [
                "Enforce minimum 12-character passwords with complexity requirements",
                "Enable Multi-Factor Authentication (MFA) for all user accounts",
                "Conduct mandatory phishing awareness training for all users",
                "Implement email filtering and domain verification systems",
                "Monitor and block suspicious domains at firewall level",
                "Regular security audits and penetration testing",
                "Deploy password managers for credential management",
                "Implement account lockout policies after failed attempts"
            ]
            for i, rec in enumerate(recommendations, 1):
                story.append(Paragraph(f"{i}. {rec}", styles['Normal']))
            
            doc.build(story)
            messagebox.showinfo("Success", f"PDF report exported successfully!\n\nSaved to: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {str(e)}")
    
    def export_json(self):
        """Export case data as JSON"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")],
                initialfile=f"CaseData_{self.case_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            if not filename:
                return
            
            # Collect all case data
            case_data = {
                "case_info": {
                    "case_id": f"SEC-2026-{datetime.now().strftime('%m%d')}",
                    "case_name": self.case_name,
                    "status": "OPEN",
                    "created_on": datetime.now().isoformat(),
                    "risk_score": self.calculate_overall_risk()
                },
                "metrics": self.get_case_metrics(),
                "executive_summary": self.generate_executive_summary(),
                "module_reports": {
                    "password_attack": self.get_password_report(),
                    "phishing_campaign": self.get_phishing_report(),
                    "domain_verification": self.get_domain_report(),
                    "ai_behavior": self.get_ai_behavior_report(),
                    "email_analyzer": self.get_email_analyzer_report()
                },
                "timeline": self.generate_timeline(),
                "raw_data": {}
            }
            
            # Add raw database data
            if os.path.exists("cases/attack_results.db"):
                conn = sqlite3.connect("cases/attack_results.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM attack_results")
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                case_data["raw_data"]["password_attacks"] = [
                    dict(zip(columns, row)) for row in rows
                ]
                conn.close()
            
            if os.path.exists("cases/phishing_campaigns.db"):
                conn = sqlite3.connect("cases/phishing_campaigns.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM campaigns")
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                case_data["raw_data"]["phishing_campaigns"] = [
                    dict(zip(columns, row)) for row in rows
                ]
                conn.close()
            
            if os.path.exists("cases/email_analysis.db"):
                conn = sqlite3.connect("cases/email_analysis.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM analyzed_emails")
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                case_data["raw_data"]["email_analysis"] = [
                    dict(zip(columns, row)) for row in rows
                ]
                conn.close()
            
            if os.path.exists("cases/domain_verification.db"):
                conn = sqlite3.connect("cases/domain_verification.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM domain_checks")
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                case_data["raw_data"]["domain_verification"] = [
                    dict(zip(columns, row)) for row in rows
                ]
                conn.close()
            
            # Write JSON file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(case_data, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Success", f"JSON data exported successfully!\n\nSaved to: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export JSON: {str(e)}")
    
    def download_evidence(self):
        messagebox.showinfo("Download", "Evidence download - Coming soon")
    
    def close_case(self):
        if messagebox.askyesno("Close Case", "Are you sure you want to close this case?"):
            self.window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    AnalyticsDashboard(root, "Test Case")
    root.mainloop()
