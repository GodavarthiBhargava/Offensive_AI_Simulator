"""
╔══════════════════════════════════════════════════════════╗
║ Anonymous Email Sender (Educational) ║
║ Similar to emkei.cz ║
╚══════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    import email_config
    SENDER_EMAIL = email_config.SENDER_EMAIL
    APP_PASSWORD = email_config.APP_PASSWORD
except:
    SENDER_EMAIL = ""
    APP_PASSWORD = ""

class PhishingCampaignModule:
    def __init__(self, window):
        self.window = window
        self.window.title("Offensive AI Simulator - Module 5: Phishing Campaign")
        self.window.geometry("1000x700")
        self.window.configure(bg="#2E2E2E")
        self._build_ui()

    def _build_ui(self):
        # Top Navigation Bar
        navbar = tk.Frame(self.window, bg="#1F1F1F", height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        
        tk.Label(navbar, text="Module 5: Phishing Campaign Simulator",
                font=("Consolas", 14, "bold"), bg="#1F1F1F", fg="#00FF66").pack(side="left", padx=20, pady=15)
        
        tk.Label(navbar, text="⚠ FOR AUTHORIZED SECURITY TESTING ONLY",
                font=("Consolas", 10, "bold"), bg="#1F1F1F", fg="#FF6B35").pack(side="right", padx=20)
        
        tk.Frame(self.window, bg="#003300", height=1).pack(fill="x")
        
        # Main content
        content = tk.Frame(self.window, bg="#2E2E2E")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel - Form (with fixed width)
        left_panel = tk.Frame(content, bg="#2E2E2E", width=450)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Template Selection
        tk.Label(left_panel, text="SELECT TEMPLATE",
                font=("Consolas", 12, "bold"), bg="#2E2E2E", fg="#00FF66", anchor="w").pack(fill="x", pady=(0, 5))
        
        self.template_var = tk.StringVar(value="Custom")
        template_frame = tk.Frame(left_panel, bg="#000000", relief="solid", bd=1)
        template_frame.pack(fill="x", pady=(0, 15))
        
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TCombobox',
                       fieldbackground="#000000",
                       background="#000000",
                       foreground="#00FF66",
                       bordercolor="#003300",
                       arrowcolor="#00FF66")
        
        template_combo = ttk.Combobox(template_frame, textvariable=self.template_var,
                                     values=["Custom", "Google Security Alert", "PayPal Account Limited", 
                                            "Facebook Security Notice", "Instagram Verification Required"],
                                     state="readonly", font=("Consolas", 11, "bold"),
                                     style='Custom.TCombobox')
        template_combo.pack(fill="x", ipady=6, padx=2, pady=2)
        template_combo.bind("<<ComboboxSelected>>", self._load_template)
        
        # From Name
        tk.Label(left_panel, text="FROM NAME (DISPLAY NAME)",
                font=("Consolas", 12, "bold"), bg="#2E2E2E", fg="#00FF66", anchor="w").pack(fill="x", pady=(0, 5))
        
        self.from_name = tk.Entry(left_panel, font=("Consolas", 12, "bold"),
                                 bg="#000000", fg="#00FF66", relief="solid", bd=1,
                                 insertbackground="#00FF66")
        self.from_name.pack(fill="x", ipady=8, pady=(0, 15))
        
        # From Email
        tk.Label(left_panel, text="FROM EMAIL (SPOOFED ADDRESS)",
                font=("Consolas", 12, "bold"), bg="#2E2E2E", fg="#00FF66", anchor="w").pack(fill="x", pady=(0, 5))
        
        self.from_email = tk.Entry(left_panel, font=("Consolas", 12, "bold"),
                                  bg="#000000", fg="#00FF66", relief="solid", bd=1,
                                  insertbackground="#00FF66")
        self.from_email.pack(fill="x", ipady=8, pady=(0, 15))
        
        # To Email
        tk.Label(left_panel, text="TO EMAIL (RECIPIENT)",
                font=("Consolas", 12, "bold"), bg="#2E2E2E", fg="#00FF66", anchor="w").pack(fill="x", pady=(0, 5))
        
        self.to_email = tk.Entry(left_panel, font=("Consolas", 12, "bold"),
                                bg="#000000", fg="#00FF66", relief="solid", bd=1,
                                insertbackground="#00FF66")
        self.to_email.pack(fill="x", ipady=8, pady=(0, 15))
        
        # Subject
        tk.Label(left_panel, text="SUBJECT",
                font=("Consolas", 12, "bold"), bg="#2E2E2E", fg="#00FF66", anchor="w").pack(fill="x", pady=(0, 5))
        
        self.subject = tk.Entry(left_panel, font=("Consolas", 12, "bold"),
                               bg="#000000", fg="#00FF66", relief="solid", bd=1,
                               insertbackground="#00FF66")
        self.subject.pack(fill="x", ipady=8, pady=(0, 15))
        
        # Message Body
        tk.Label(left_panel, text="MESSAGE BODY",
                font=("Consolas", 12, "bold"), bg="#2E2E2E", fg="#00FF66", anchor="w").pack(fill="x", pady=(0, 5))
        
        msg_frame = tk.Frame(left_panel, bg="#000000", relief="solid", bd=1, height=200)
        msg_frame.pack(fill="x", pady=(0, 15))
        msg_frame.pack_propagate(False)
        
        self.message = tk.Text(msg_frame, font=("Consolas", 11, "bold"),
                              bg="#000000", fg="#00FF66", insertbackground="#00FF66",
                              relief="flat", padx=5, pady=5, wrap="word")
        self.message.pack(fill="both", expand=True)
        
        # Buttons (fixed at bottom)
        btn_frame = tk.Frame(left_panel, bg="#2E2E2E")
        btn_frame.pack(fill="x", pady=(0, 10))
        
        self.send_btn = tk.Button(btn_frame, text="📤 SEND EMAIL",
                                 font=("Consolas", 12, "bold"), bg="#00FF66", fg="#000000",
                                 activebackground="#00CC55", activeforeground="#000000",
                                 relief="solid", bd=0, cursor="hand2",
                                 command=self._send_email, height=2)
        self.send_btn.pack(fill="x", pady=(0, 8))
        
        self.send_btn.bind("<Enter>", lambda e: self.send_btn.config(bg="#00CC55"))
        self.send_btn.bind("<Leave>", lambda e: self.send_btn.config(bg="#00FF66"))
        
        clear_btn = tk.Button(btn_frame, text="🗑 CLEAR",
                 font=("Consolas", 12, "bold"), bg="#000000", fg="#00FF66",
                 activebackground="#003300", activeforeground="#00FF66",
                 relief="solid", bd=2, cursor="hand2",
                 command=self._clear_form, height=2)
        clear_btn.pack(fill="x")
        
        clear_btn.bind("<Enter>", lambda e: clear_btn.config(bg="#003300"))
        clear_btn.bind("<Leave>", lambda e: clear_btn.config(bg="#000000"))
        
        # Right panel - Console
        right_panel = tk.Frame(content, bg="#000000", relief="solid", bd=2)
        right_panel.pack(side="right", fill="both", expand=True)
        
        self.console = tk.Text(right_panel, bg="#000000", fg="#00FF00",
                              font=("Consolas", 12, "bold"), insertbackground="#00FF00",
                              relief="flat", state="disabled", padx=15, pady=15)
        self.console.pack(fill="both", expand=True)
        
        self.print_console("[SYSTEM] Phishing Campaign Module Ready")
        self.print_console("[WARNING] For authorized security testing only")

    def _load_template(self, event=None):
        template = self.template_var.get()
        
        templates = {
            "Google Security Alert": {
                "from_name": "Google Security Team",
                "from_email": "no-reply@google.com",
                "subject": "Security Alert: New sign-in from Windows device",
                "message": """Hi there,

We detected a new sign-in to your Google Account on a Windows device.

Device: Windows PC
Location: Mumbai, India
Time: Just now

If this was you, you can ignore this email. If not, we'll help you secure your account.

Review Activity: https://accounts.google.com/signin/review

The Google Accounts team

⚠️ PHISHING ALERT: This is a simulated phishing email for security awareness training. Never click suspicious links or provide credentials."""
            },
            "PayPal Account Limited": {
                "from_name": "PayPal Service",
                "from_email": "service@paypal.com",
                "subject": "Action Required: Your PayPal account has been limited",
                "message": """Dear PayPal Member,

We've noticed some unusual activity in your account. For your protection, we've temporarily limited what you can do with your account until we confirm your identity.

What's the problem?
We need to verify your account information to ensure it's up to date.

How to restore your account:
1. Log in to your PayPal account
2. Complete the verification steps
3. Confirm your identity

Resolve Now: https://www.paypal.com/verify

We appreciate your patience as we work together to protect your account.

Sincerely,
PayPal Account Review Department

⚠️ PHISHING ALERT: This is a simulated phishing email for security awareness training. PayPal never asks for sensitive information via email."""
            },
            "Facebook Security Notice": {
                "from_name": "Facebook Security",
                "from_email": "security@facebookmail.com",
                "subject": "Your Facebook account was accessed from a new location",
                "message": """Hi,

We noticed a login to your Facebook account from a device or location we didn't recognize.

Device: Chrome on Windows
Location: Bangalore, Karnataka, India
Time: Today at 2:45 PM

If this was you:
You can ignore this message. We're just being extra careful.

If this wasn't you:
Please secure your account immediately.

Secure Account: https://facebook.com/checkpoint

Thanks,
The Facebook Security Team

⚠️ PHISHING ALERT: This is a simulated phishing email for security awareness training. Always verify sender authenticity before clicking links."""
            },
            "Instagram Verification Required": {
                "from_name": "Instagram Support",
                "from_email": "no-reply@instagram.com",
                "subject": "Verify your Instagram account to avoid suspension",
                "message": """Hello,

Your Instagram account requires immediate verification to comply with our updated security policies.

Account: @yourhandle
Status: Pending Verification
Deadline: 24 hours

Failure to verify your account within 24 hours may result in:
• Temporary account suspension
• Loss of followers and content
• Permanent account deletion

Verify your account now to maintain full access:
https://instagram.com/accounts/verify

Thank you for helping us keep Instagram safe.

The Instagram Team

⚠️ PHISHING ALERT: This is a simulated phishing email for security awareness training. Instagram never threatens account deletion via email."""
            }
        }
        
        if template in templates:
            t = templates[template]
            self.from_name.delete(0, "end")
            self.from_name.insert(0, t["from_name"])
            
            self.from_email.delete(0, "end")
            self.from_email.insert(0, t["from_email"])
            
            self.subject.delete(0, "end")
            self.subject.insert(0, t["subject"])
            
            self.message.delete("1.0", "end")
            self.message.insert("1.0", t["message"])
        elif template == "Custom":
            self._clear_form()
    
    def _send_email(self):
        from_name = self.from_name.get().strip()
        from_email = self.from_email.get().strip()
        to_email = self.to_email.get().strip()
        subject = self.subject.get().strip()
        message = self.message.get("1.0", "end-1c").strip()

        if not all([from_name, from_email, to_email, subject, message]):
            messagebox.showerror("Error", "All fields are required!")
            return

        self.send_btn.configure(state="disabled", text="⏳ Sending...")
        self.print_console("[INFO] Sending email...")

        def send_thread():
            try:
                # Create message with spoofed headers
                msg = MIMEMultipart()
                msg['From'] = f"{from_name} <{from_email}>"
                msg['To'] = to_email
                msg['Subject'] = subject
                msg.attach(MIMEText(message, 'plain'))

                # Use your Gmail SMTP but with spoofed From header
                smtp_user = SENDER_EMAIL
                smtp_pass = APP_PASSWORD
                
                if not smtp_user or not smtp_pass:
                    raise Exception("Configure SENDER_EMAIL and APP_PASSWORD in email_config.py")
                
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(smtp_user, smtp_pass)
                
                # Send with actual sender email (Gmail requires this)
                server.sendmail(smtp_user, to_email, msg.as_string())
                server.quit()

                self.window.after(0, lambda: self._send_success())
            except Exception as e:
                self.window.after(0, lambda: self._send_error(str(e)))

        threading.Thread(target=send_thread, daemon=True).start()

    def _send_success(self):
        self.send_btn.configure(state="normal", text="SEND PHISHING EMAIL")
        self.print_console("[SUCCESS] Email sent successfully!")
        messagebox.showinfo("Success", "Email sent successfully!")
        self._clear_form()

    def _send_error(self, error):
        self.send_btn.configure(state="normal", text="SEND PHISHING EMAIL")
        self.print_console(f"[ERROR] {error}")
        messagebox.showerror("Error", f"Failed to send email: {error}")

    def _clear_form(self):
        self.from_name.delete(0, "end")
        self.from_email.delete(0, "end")
        self.to_email.delete(0, "end")
        self.subject.delete(0, "end")
        self.message.delete("1.0", "end")
    
    def print_console(self, text):
        self.console.config(state="normal")
        self.console.insert("end", text + "\n")
        self.console.see("end")
        self.console.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    PhishingCampaignModule(root)
    root.mainloop()
