"""
Phishing Email Detection Engine
Rule-based + AI-based analysis for educational simulation
"""

import re

class PhishingDetector:
    def __init__(self):
        self.suspicious_domains = [
            'amaz0n', 'paypa1', 'g00gle', 'micros0ft', 'faceb00k',
            'bank-alert', 'verify', 'secure-', 'account-'
        ]
        
        self.urgency_keywords = [
            'urgent', 'immediately', 'account suspended', 'verify now',
            'click below', 'limited time', 'otp', 'password reset',
            'expires', 'final warning', 'act now', 'confirm immediately'
        ]
        
        self.sensitive_requests = [
            'password', 'otp', 'bank details', 'credit card', 'ssn',
            'personal data', 'card number', 'cvv', 'pin', 'account number'
        ]
        
        self.brands = [
            'amazon', 'paypal', 'bank', 'whatsapp', 'google', 
            'microsoft', 'facebook', 'instagram', 'netflix', 'apple'
        ]
    
    def analyze_message(self, sender, body, message_type):
        """Analyze WhatsApp or SMS message"""
        risk_score = 0
        red_flags = []
        
        # Sender analysis
        sender_score, sender_flags = self._analyze_sender_number(sender, message_type)
        risk_score += sender_score
        red_flags.extend(sender_flags)
        
        # Urgency detection
        urgency_score, urgency_flags = self._detect_urgency(body)
        risk_score += urgency_score
        red_flags.extend(urgency_flags)
        
        # Link analysis
        link_score, link_flags = self._analyze_links(body)
        risk_score += link_score
        red_flags.extend(link_flags)
        
        # Sensitive info detection
        sensitive_score, sensitive_flags = self._detect_sensitive_requests(body)
        risk_score += sensitive_score
        red_flags.extend(sensitive_flags)
        
        # Brand impersonation
        brand_score, brand_flags = self._detect_brand_impersonation(body)
        risk_score += brand_score
        red_flags.extend(brand_flags)
        
        risk_score = min(risk_score, 100)
        
        # Domain analysis
        domain_analysis = self._analyze_domain_from_links(body)
        
        # Classification
        if risk_score <= 30:
            classification = "SAFE"
            risk_level = "LOW"
        elif risk_score <= 60:
            classification = "SUSPICIOUS"
            risk_level = "MEDIUM"
        else:
            classification = "MALICIOUS"
            risk_level = "HIGH"
        
        attack_type = f"{message_type} Phishing" if classification == "MALICIOUS" else classification
        
        return {
            'message_type': message_type,
            'attack_type': attack_type,
            'classification': classification,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'red_flags': red_flags,
            'domain_analysis': domain_analysis
        }
    
    def analyze_email(self, sender, subject, body):
        risk_score = 0
        red_flags = []
        
        # Sender analysis
        sender_score, sender_flags = self._analyze_sender(sender)
        risk_score += sender_score
        red_flags.extend(sender_flags)
        
        # Urgency detection
        urgency_score, urgency_flags = self._detect_urgency(subject + " " + body)
        risk_score += urgency_score
        red_flags.extend(urgency_flags)
        
        # Link analysis
        link_score, link_flags = self._analyze_links(body)
        risk_score += link_score
        red_flags.extend(link_flags)
        
        # Sensitive info detection
        sensitive_score, sensitive_flags = self._detect_sensitive_requests(body)
        risk_score += sensitive_score
        red_flags.extend(sensitive_flags)
        
        # Grammar check
        grammar_score, grammar_flags = self._check_grammar(body)
        risk_score += grammar_score
        red_flags.extend(grammar_flags)
        
        risk_score = min(risk_score, 100)
        
        # Domain analysis
        domain_analysis = self._analyze_domain(sender, body)
        
        # Classification
        if risk_score <= 30:
            classification = "SAFE"
            risk_level = "LOW"
        elif risk_score <= 60:
            classification = "SUSPICIOUS"
            risk_level = "MEDIUM"
        else:
            classification = "MALICIOUS"
            risk_level = "HIGH"
        
        return {
            'message_type': 'Email',
            'attack_type': 'Email Phishing' if classification == 'MALICIOUS' else classification,
            'classification': classification,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'red_flags': red_flags,
            'domain_analysis': domain_analysis
        }
    
    def _analyze_sender_number(self, sender, message_type):
        score = 0
        flags = []
        sender_lower = sender.lower()
        
        if sender.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            if len(sender.replace('+', '').replace('-', '').replace(' ', '')) < 10:
                score += 25
                flags.append("Short code or suspicious number detected")
        
        for brand in self.brands:
            if brand in sender_lower:
                score += 30
                flags.append(f"Potential {brand.capitalize()} impersonation")
                break
        
        if any(x in sender_lower for x in ['admin', 'support', 'security', 'team']):
            score += 20
            flags.append("Generic sender name detected")
        
        return score, flags
    
    def _detect_brand_impersonation(self, text):
        score = 0
        flags = []
        text_lower = text.lower()
        
        detected_brands = [brand for brand in self.brands if brand in text_lower]
        if detected_brands:
            score += 25
            flags.append(f"Brand impersonation: {', '.join(detected_brands)}")
        
        return score, flags
    
    def _analyze_domain_from_links(self, body):
        link_domain = "None detected"
        brand_impersonation = "No"
        domain_risk = "Low"
        trust_status = "Unknown"
        
        if 'http' in body:
            match = re.search(r'https?://([^\s/]+)', body)
            if match:
                link_domain = match.group(1)
                
                for brand in self.brands:
                    if brand in link_domain.lower() and any(x in link_domain for x in ['0', '1', '-', 'secure', 'verify']):
                        brand_impersonation = "Yes"
                        domain_risk = "High"
                        break
                
                trusted_domains = ['amazon.com', 'paypal.com', 'google.com']
                trust_status = "Trusted" if link_domain in trusted_domains else "Untrusted"
        
        return {
            'link_domain': link_domain,
            'brand_impersonation': brand_impersonation,
            'domain_risk_level': domain_risk,
            'trust_status': trust_status
        }
    
    def _analyze_sender(self, sender):
        score = 0
        flags = []
        sender_lower = sender.lower()
        
        for domain in self.suspicious_domains:
            if domain in sender_lower:
                score += 30
                flags.append(f"Suspicious domain: {domain}")
                break
        
        if any(x in sender_lower for x in ['@gmail', '@yahoo', '@hotmail']):
            if any(x in sender_lower for x in ['bank', 'paypal', 'amazon', 'support']):
                score += 30
                flags.append("Public domain pretending to be company")
        
        return score, flags
    
    def _detect_urgency(self, text):
        score = 0
        flags = []
        text_lower = text.lower()
        
        count = sum(1 for keyword in self.urgency_keywords if keyword in text_lower)
        if count >= 3:
            score += 30
            flags.append(f"Multiple urgency keywords ({count})")
        elif count > 0:
            score += 15
            flags.append("Urgency/threat language detected")
        
        return score, flags
    
    def _analyze_links(self, body):
        score = 0
        flags = []
        
        if re.search(r'http://', body):
            score += 20
            flags.append("Non-HTTPS link detected")
        
        if any(x in body.lower() for x in ['bit.ly', 'tinyurl', 'goo.gl']):
            score += 20
            flags.append("Shortened URL detected")
        
        return score, flags
    
    def _detect_sensitive_requests(self, body):
        score = 0
        flags = []
        body_lower = body.lower()
        
        count = sum(1 for keyword in self.sensitive_requests if keyword in body_lower)
        if count > 0:
            score += 25
            flags.append(f"Requests sensitive information ({count} types)")
        
        return score, flags
    
    def _check_grammar(self, body):
        score = 0
        flags = []
        
        if '!!' in body or '???' in body:
            score += 10
            flags.append("Excessive punctuation detected")
        
        return score, flags
    
    def _analyze_domain(self, sender, body):
        sender_domain = sender.split('@')[1] if '@' in sender else sender
        
        link_domain = "None detected"
        if 'http' in body:
            match = re.search(r'https?://([^\s/]+)', body)
            if match:
                link_domain = match.group(1)
        
        domain_match = "Yes" if link_domain == "None detected" or sender_domain in link_domain else "No"
        
        brand_impersonation = "Yes" if any(brand in sender_domain.lower() for brand in self.brands) and any(x in sender_domain for x in ['0', '1', '-']) else "No"
        
        domain_risk = "High" if brand_impersonation == "Yes" or domain_match == "No" else "Low"
        
        trusted_domains = ['gmail.com', 'yahoo.com', 'outlook.com']
        trust_status = "Trusted" if sender_domain in trusted_domains else "Untrusted"
        
        return {
            'sender_domain': sender_domain,
            'link_domain': link_domain,
            'domain_match': domain_match,
            'brand_impersonation': brand_impersonation,
            'domain_risk_level': domain_risk,
            'trust_status': trust_status
        }
