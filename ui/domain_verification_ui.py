import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sqlite3
import os
from datetime import datetime
from urllib.parse import urlparse
import socket
import ssl
import re
import threading

class DomainVerificationModule:
    def __init__(self, window):
        self.window = window
        self.window.title("Domain Verification Module")
        self.window.geometry("1400x800")
        self.window.configure(bg="#2E2E2E")
        
        self.init_domain_db()
        
        # Top bar
        navbar = tk.Frame(window, bg="#1F1F1F", height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        
        tk.Label(navbar, text="🛡️ DOMAIN VERIFICATION & SPOOF DETECTION",
                font=("Consolas", 14, "bold"), bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        tk.Frame(window, bg="#003300", height=1).pack(fill="x")
        
        # Main content
        content = tk.Frame(window, bg="#2E2E2E")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel - Input
        left_panel = tk.Frame(content, bg="#1F1F1F", relief="solid", bd=2)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        tk.Label(left_panel, text="🔍 DOMAIN ANALYSIS", font=("Consolas", 14, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        # URL input
        input_frame = tk.Frame(left_panel, bg="#1F1F1F")
        input_frame.pack(fill="x", padx=10, pady=(0, 20))
        
        tk.Label(input_frame, text="Enter URL or Domain:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(anchor="w", pady=(0, 5))
        
        self.url_entry = tk.Entry(input_frame, font=("Consolas", 12, "bold"),
                                  bg="#000000", fg="#00FF66", relief="solid", bd=1)
        self.url_entry.pack(fill="x", ipady=10, pady=(0, 10))
        self.url_entry.insert(0, "https://www.google.com")
        
        # Analyze button
        analyze_btn = tk.Button(input_frame, text="🔍 ANALYZE DOMAIN",
                               font=("Consolas", 12, "bold"), bg="#000000", fg="#00FF66",
                               activebackground="#003300", relief="solid", bd=2,
                               cursor="hand2", command=self.start_analysis)
        analyze_btn.pack(fill="x", ipady=10)
        
        # Risk score display
        self.risk_frame = tk.Frame(left_panel, bg="#000000", relief="solid", bd=2)
        self.risk_frame.pack(fill="x", padx=10, pady=20)
        
        tk.Label(self.risk_frame, text="RISK LEVEL", font=("Consolas", 14, "bold"),
                bg="#000000", fg="#00FF66").pack(pady=10)
        
        self.risk_label = tk.Label(self.risk_frame, text="UNKNOWN", font=("Consolas", 24, "bold"),
                                   bg="#000000", fg="#666666")
        self.risk_label.pack(pady=10)
        
        self.risk_score_label = tk.Label(self.risk_frame, text="Risk Score: 0/100",
                                         font=("Consolas", 14, "bold"), bg="#000000", fg="#666666")
        self.risk_score_label.pack(pady=(0, 10))
        
        # Quick checks display
        checks_frame = tk.Frame(left_panel, bg="#1F1F1F")
        checks_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        tk.Label(checks_frame, text="QUICK CHECKS:", font=("Consolas", 12, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(anchor="w", pady=(0, 10))
        
        self.check_labels = {}
        checks = ["SSL Certificate", "Domain Age", "Spoof Detection", "TLD Check", "DNS Resolution"]
        
        for check in checks:
            frame = tk.Frame(checks_frame, bg="#1F1F1F")
            frame.pack(fill="x", pady=3)
            
            tk.Label(frame, text=f"• {check}:", font=("Consolas", 10, "bold"),
                    bg="#1F1F1F", fg="#00FF66", width=20, anchor="w").pack(side="left")
            
            label = tk.Label(frame, text="⏳ Pending", font=("Consolas", 10, "bold"),
                           bg="#1F1F1F", fg="#666666")
            label.pack(side="left")
            self.check_labels[check] = label
        
        # Right panel - Detailed results
        right_panel = tk.Frame(content, bg="#1F1F1F", relief="solid", bd=2)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        tk.Label(right_panel, text="📊 DETAILED ANALYSIS", font=("Consolas", 14, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        self.results_text = scrolledtext.ScrolledText(right_panel, font=("Consolas", 10, "bold"),
                                                     bg="#000000", fg="#00FF66",
                                                     relief="flat", padx=15, pady=15, wrap=tk.WORD)
        self.results_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Sample buttons
        sample_frame = tk.Frame(right_panel, bg="#1F1F1F")
        sample_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(sample_frame, text="Test Samples:", font=("Consolas", 10, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(side="left", padx=(0, 10))
        
        samples = [
            ("Safe", "https://www.google.com"),
            ("Suspicious", "http://paypa1-secure.xyz"),
            ("Risky", "http://192.168.1.1/login")
        ]
        
        for name, url in samples:
            btn = tk.Button(sample_frame, text=name, font=("Consolas", 9, "bold"),
                           bg="#000000", fg="#00FF66", relief="solid", bd=1,
                           cursor="hand2", command=lambda u=url: self.load_sample(u))
            btn.pack(side="left", padx=2)
    
    def init_domain_db(self):
        """Initialize domain verification database"""
        os.makedirs("cases", exist_ok=True)
        conn = sqlite3.connect("cases/domain_verification.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS domain_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                domain TEXT,
                risk_score INTEGER,
                classification TEXT,
                ssl_valid INTEGER,
                domain_age TEXT,
                spoof_detected INTEGER,
                suspicious_tld INTEGER,
                timestamp TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def load_sample(self, url):
        """Load sample URL"""
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)
    
    def start_analysis(self):
        """Start domain analysis in thread"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Enter a URL or domain")
            return
        
        # Reset UI
        self.risk_label.config(text="ANALYZING...", fg="#FFAA00")
        self.risk_score_label.config(text="Please wait...", fg="#FFAA00")
        self.results_text.delete(1.0, tk.END)
        
        for label in self.check_labels.values():
            label.config(text="⏳ Checking...", fg="#FFAA00")
        
        # Run analysis in thread
        thread = threading.Thread(target=self.analyze_domain, args=(url,))
        thread.daemon = True
        thread.start()
    
    def analyze_domain(self, url):
        """Analyze domain with real-time checks"""
        try:
            # Extract domain
            domain = self.extract_domain(url)
            
            self.results_text.insert(tk.END, "🔍 DOMAIN VERIFICATION REPORT\n\n")
            self.results_text.insert(tk.END, "━"*70 + "\n\n")
            self.results_text.insert(tk.END, "🌐 Input Details\n\n")
            self.results_text.insert(tk.END, f"URL: {url}\n")
            self.results_text.insert(tk.END, f"Extracted Domain: {domain}\n\n")
            self.results_text.insert(tk.END, "━"*70 + "\n\n")
            
            risk_score = 0
            threats = []
            
            # Check 1: SSL Certificate
            self.results_text.insert(tk.END, "🔒 1. SSL Certificate Check\n\n")
            ssl_valid, ssl_info = self.check_ssl(domain)
            if ssl_valid:
                self.results_text.insert(tk.END, f"Status: ✅ PASSED\n")
                self.results_text.insert(tk.END, f"Certificate Info: {ssl_info}\n\n")
                self.results_text.insert(tk.END, "👉 This website supports secure HTTPS communication.\n\n")
                self.check_labels["SSL Certificate"].config(text="✅ Valid", fg="#00FF66")
            else:
                self.results_text.insert(tk.END, f"Status: ❌ FAILED\n")
                self.results_text.insert(tk.END, f"Reason: No valid SSL certificate found\n")
                self.results_text.insert(tk.END, f"Technical Detail: {ssl_info}\n\n")
                self.results_text.insert(tk.END, "👉 This means the website does not support secure HTTPS communication.\n\n")
                risk_score += 20
                threats.append("No SSL certificate")
                self.check_labels["SSL Certificate"].config(text="❌ Invalid", fg="#FF4444")
            
            # Check 2: DNS Resolution
            self.results_text.insert(tk.END, "🌐 2. DNS Resolution Check\n\n")
            dns_valid, ip_address = self.check_dns(domain)
            if dns_valid:
                self.results_text.insert(tk.END, f"Status: ✅ PASSED\n")
                self.results_text.insert(tk.END, f"Reason: Domain resolves to IP: {ip_address}\n\n")
                self.results_text.insert(tk.END, "👉 Domain is properly registered and accessible.\n\n")
                self.check_labels["DNS Resolution"].config(text="✅ Valid", fg="#00FF66")
                
                # Check if IP address in URL
                if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain):
                    self.results_text.insert(tk.END, "⚠️ WARNING: URL uses IP address instead of domain\n\n")
                    self.results_text.insert(tk.END, "👉 Legitimate websites rarely use IP addresses directly.\n\n")
                    risk_score += 30
                    threats.append("IP address in URL")
                    self.check_labels["DNS Resolution"].config(text="⚠️ IP Address", fg="#FFAA00")
            else:
                self.results_text.insert(tk.END, f"Status: ❌ FAILED\n")
                self.results_text.insert(tk.END, f"Reason: Domain does not resolve to a valid IP address\n\n")
                self.results_text.insert(tk.END, "👉 This indicates the domain may be fake or not properly registered.\n\n")
                risk_score += 40
                threats.append("Domain not resolvable")
                self.check_labels["DNS Resolution"].config(text="❌ Failed", fg="#FF4444")
            
            # Check 3: Domain Age
            self.results_text.insert(tk.END, "📅 3. Domain Age & Structure Analysis\n\n")
            age_risk, age_info = self.check_domain_age_heuristic(domain)
            if age_risk > 0:
                self.results_text.insert(tk.END, f"Status: ⚠️ WARNING\n")
                self.results_text.insert(tk.END, f"Observation: {age_info}\n\n")
                self.results_text.insert(tk.END, "👉 Suspicious patterns detected in domain structure.\n\n")
                risk_score += age_risk
                threats.append("Suspicious domain characteristics")
                self.check_labels["Domain Age"].config(text="⚠️ Suspicious", fg="#FFAA00")
            else:
                self.results_text.insert(tk.END, f"Status: ✅ PASSED\n")
                self.results_text.insert(tk.END, f"Observation: {age_info}\n\n")
                if not dns_valid:
                    self.results_text.insert(tk.END, "👉 However, domain age could not be verified due to DNS failure.\n\n")
                else:
                    self.results_text.insert(tk.END, "👉 Domain structure appears legitimate.\n\n")
                self.check_labels["Domain Age"].config(text="✅ Normal", fg="#00FF66")
            
            # Check 4: Spoof Detection
            self.results_text.insert(tk.END, "🎭 4. Spoof Detection (Similarity Check)\n\n")
            spoof_risk, spoof_info = self.check_spoof(domain)
            if spoof_risk > 0:
                self.results_text.insert(tk.END, f"Status: 🚨 DETECTED\n")
                self.results_text.insert(tk.END, f"Warning: {spoof_info}\n\n")
                self.results_text.insert(tk.END, "👉 This domain closely resembles a legitimate brand domain.\n\n")
                risk_score += spoof_risk
                threats.append("Possible domain spoofing")
                self.check_labels["Spoof Detection"].config(text="⚠️ Detected", fg="#FF4444")
            else:
                self.results_text.insert(tk.END, f"Status: ✅ CLEAN\n")
                self.results_text.insert(tk.END, f"Observation: {spoof_info}\n\n")
                self.results_text.insert(tk.END, "👉 No direct impersonation detected.\n\n")
                self.check_labels["Spoof Detection"].config(text="✅ Clean", fg="#00FF66")
            
            # Check 5: TLD Check
            self.results_text.insert(tk.END, "🌍 5. TLD (Top-Level Domain) Check\n\n")
            tld_risk, tld_info = self.check_tld(domain)
            tld = '.' + domain.split('.')[-1] if '.' in domain else 'unknown'
            if tld_risk > 0:
                self.results_text.insert(tk.END, f"Status: ⚠️ SUSPICIOUS\n")
                self.results_text.insert(tk.END, f"TLD: {tld}\n")
                self.results_text.insert(tk.END, f"Warning: {tld_info}\n\n")
                self.results_text.insert(tk.END, "👉 This TLD is commonly used in phishing attacks.\n\n")
                risk_score += tld_risk
                threats.append("Suspicious TLD")
                self.check_labels["TLD Check"].config(text="⚠️ Suspicious", fg="#FFAA00")
            else:
                self.results_text.insert(tk.END, f"Status: ✅ NORMAL\n")
                self.results_text.insert(tk.END, f"TLD: {tld}\n\n")
                self.results_text.insert(tk.END, f"👉 {tld} is considered a standard and trusted domain extension.\n\n")
                self.check_labels["TLD Check"].config(text="✅ Normal", fg="#00FF66")
            
            # Check 6: Homograph Attack
            self.results_text.insert(tk.END, "🔤 6. Homograph Attack Detection\n\n")
            homograph_risk, homograph_info = self.check_homograph(domain)
            if homograph_risk > 0:
                self.results_text.insert(tk.END, f"Status: ⚠️ WARNING\n")
                self.results_text.insert(tk.END, f"{homograph_info}\n\n")
                self.results_text.insert(tk.END, "👉 This pattern is commonly used in phishing domains to trick users.\n\n")
                risk_score += homograph_risk
                threats.append("Homograph attack detected")
            else:
                self.results_text.insert(tk.END, f"Status: ✅ CLEAN\n")
                self.results_text.insert(tk.END, f"{homograph_info}\n\n")
                self.results_text.insert(tk.END, "👉 No suspicious character substitutions detected.\n\n")
            
            # Cap risk score
            risk_score = min(risk_score, 100)
            
            # Classification
            if risk_score >= 70:
                classification = "HIGH RISK"
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
            
            # Final Summary
            self.results_text.insert(tk.END, "📊 FINAL SECURITY ANALYSIS\n\n")
            self.results_text.insert(tk.END, "━"*70 + "\n\n")
            self.results_text.insert(tk.END, f"🧮 Risk Score: {risk_score} / 100\n")
            self.results_text.insert(tk.END, f"🚨 Classification: {classification}\n\n")
            
            if threats:
                self.results_text.insert(tk.END, "⚠️ THREATS IDENTIFIED:\n\n")
                for i, threat in enumerate(threats, 1):
                    self.results_text.insert(tk.END, f"  {i}. {threat}\n")
                self.results_text.insert(tk.END, "\n")
            
            # Recommendation
            self.results_text.insert(tk.END, "💡 RECOMMENDATION:\n\n")
            if classification == "HIGH RISK":
                self.results_text.insert(tk.END, "❌ DO NOT VISIT THIS DOMAIN\n")
                self.results_text.insert(tk.END, "This domain shows strong indicators of being malicious or fake.\n")
                self.results_text.insert(tk.END, "Visiting this site may compromise your security.\n")
            elif classification == "SUSPICIOUS":
                self.results_text.insert(tk.END, "⚠️ PROCEED WITH EXTREME CAUTION\n")
                self.results_text.insert(tk.END, "This domain has suspicious characteristics.\n")
                self.results_text.insert(tk.END, "Verify through official channels before proceeding.\n")
            else:
                self.results_text.insert(tk.END, "✅ DOMAIN APPEARS SAFE\n")
                self.results_text.insert(tk.END, "This domain passed all security checks.\n")
                self.results_text.insert(tk.END, "However, always remain vigilant online.\n")
            
            # Save to database
            conn = sqlite3.connect("cases/domain_verification.db")
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO domain_checks (url, domain, risk_score, classification, ssl_valid, 
                                          spoof_detected, suspicious_tld, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (url, domain, risk_score, classification, ssl_valid, spoof_risk > 0, 
                  tld_risk > 0, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.results_text.insert(tk.END, f"\n❌ ERROR: {str(e)}\n")
            self.risk_label.config(text="ERROR", fg="#FF4444")
    
    def extract_domain(self, url):
        """Extract domain from URL"""
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        parsed = urlparse(url)
        return parsed.netloc or parsed.path
    
    def check_ssl(self, domain):
        """Check SSL certificate"""
        try:
            # Remove port if present
            domain_clean = domain.split(':')[0]
            
            context = ssl.create_default_context()
            with socket.create_connection((domain_clean, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain_clean) as ssock:
                    cert = ssock.getpeercert()
                    return True, f"Issued to: {cert.get('subject', [[('commonName', 'Unknown')]])[0][0][1]}"
        except Exception as e:
            return False, f"SSL check failed: {str(e)[:50]}"
    
    def check_dns(self, domain):
        """Check DNS resolution"""
        try:
            domain_clean = domain.split(':')[0]
            ip = socket.gethostbyname(domain_clean)
            return True, ip
        except Exception as e:
            return False, None
    
    def check_domain_age_heuristic(self, domain):
        """Heuristic domain age check"""
        # Check for suspicious patterns that indicate new/temporary domains
        suspicious_keywords = ['temp', 'test', 'verify', 'secure', 'login', 'account', 'update']
        
        domain_lower = domain.lower()
        
        # Check for multiple hyphens (common in phishing)
        if domain_lower.count('-') >= 2:
            return 15, "⚠️ Multiple hyphens detected (common in phishing domains)"
        
        # Check for suspicious keywords
        for keyword in suspicious_keywords:
            if keyword in domain_lower:
                return 10, f"⚠️ Suspicious keyword '{keyword}' found in domain"
        
        # Check for excessive length
        if len(domain) > 40:
            return 10, "⚠️ Unusually long domain name"
        
        return 0, "✅ Domain structure appears normal"
    
    def check_spoof(self, domain):
        """Check for domain spoofing using Levenshtein distance"""
        legitimate_domains = [
            'google.com', 'facebook.com', 'paypal.com', 'amazon.com', 'microsoft.com',
            'apple.com', 'netflix.com', 'instagram.com', 'twitter.com', 'linkedin.com',
            'yahoo.com', 'ebay.com', 'walmart.com', 'chase.com', 'bankofamerica.com'
        ]
        
        domain_lower = domain.lower().split(':')[0]
        
        for legit in legitimate_domains:
            distance = self.levenshtein_distance(domain_lower, legit)
            if 0 < distance <= 3:
                return 40, f"🚨 SPOOF DETECTED: Similar to '{legit}' (distance: {distance})"
        
        return 0, "✅ No spoofing detected"
    
    def levenshtein_distance(self, s1, s2):
        """Calculate Levenshtein distance between two strings"""
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def check_tld(self, domain):
        """Check for suspicious TLDs"""
        suspicious_tlds = ['.xyz', '.top', '.click', '.link', '.download', '.stream', 
                          '.ru', '.cn', '.tk', '.ml', '.ga', '.cf', '.gq']
        
        domain_lower = domain.lower()
        
        for tld in suspicious_tlds:
            if domain_lower.endswith(tld):
                return 20, f"⚠️ Suspicious TLD detected: {tld}"
        
        return 0, "✅ TLD appears normal"
    
    def check_homograph(self, domain):
        """Check for homograph attacks"""
        suspicious_chars = {
            '0': 'o', '1': 'l', '3': 'e', '5': 's', '8': 'b'
        }
        
        domain_lower = domain.lower()
        detected = []
        
        for fake, real in suspicious_chars.items():
            if fake in domain_lower:
                detected.append(f"'{fake}' \u2192 resembles letter '{real}'")
        
        # Check for 'rn' looking like 'm'
        if 'rn' in domain_lower:
            detected.append("'rn' \u2192 resembles letter 'm'")
        
        # Check for 'vv' looking like 'w'
        if 'vv' in domain_lower:
            detected.append("'vv' \u2192 resembles letter 'w'")
        
        if detected:
            result = "Suspicious Characters Detected:\n\n"
            for item in detected:
                result += f"  \u2022 {item}\n"
            return 25, result
        
        return 0, "No suspicious character substitutions detected"


if __name__ == "__main__":
    root = tk.Tk()
    DomainVerificationModule(root)
    root.mainloop()
