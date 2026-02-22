"""
╔══════════════════════════════════════════════════════════╗
║       CYBER TOOL — Phishing Email Service                ║
║   For AUTHORISED security awareness testing ONLY         ║
╚══════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import messagebox
import smtplib
import threading
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import stats_tracker
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# ── Palette ────────────────────────────────────────────────────
BG_DARK    = "#2E2E2E"
PANEL_BG   = "#1F1F1F"
CARD_BG    = "#0a0a0a"
ACCENT     = "#00FF66"
ACCENT2    = "#00CC55"
TEXT_MAIN  = "#00FF66"
TEXT_MUTED = "#666666"
BORDER     = "#003300"
ERROR_C    = "#FF4444"
SUCCESS_C  = "#00FF66"
WARN_C     = "#FFAA00"
ENTRY_BG   = "#000000"

# ══════════════════════════════════════════════════════════════
#  Pre-made HTML Email Templates
# ══════════════════════════════════════════════════════════════
TEMPLATES = {
    "🔴 Google — Security Alert": {
        "subject": "Security Alert: New sign-in to your Google Account",
        "preview": "Someone signed into your account from a new device.",
        "from_name": "Google Security Team",
        "html": """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f1f3f4;font-family:Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" bgcolor="#f1f3f4">
  <tr><td align="center" style="padding:40px 0;">
    <table width="520" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.15);">
      <tr><td style="background:#4285F4;padding:20px 30px;border-radius:8px 8px 0 0;">
        <span style="color:#fff;font-size:22px;font-weight:bold;">G</span>
        <span style="color:#fff;font-size:16px;font-weight:600;margin-left:6px;">oogle</span>
      </td></tr>
      <tr><td style="padding:30px 30px 10px;">
        <h2 style="color:#202124;font-size:22px;margin:0 0 16px;">Security alert</h2>
        <p style="color:#3c4043;font-size:15px;line-height:1.6;margin:0 0 16px;">
          A new sign-in was detected on your Google Account <strong>{TARGET_EMAIL}</strong>.
        </p>
        <table cellpadding="0" cellspacing="0" style="background:#f8f9fa;border-radius:6px;width:100%;margin:16px 0;">
          <tr><td style="padding:14px 18px;">
            <p style="margin:0;font-size:13px;color:#5f6368;"><strong>Device:</strong> Windows PC (Chrome)</p>
            <p style="margin:6px 0 0;font-size:13px;color:#5f6368;"><strong>Location:</strong> Mumbai, India</p>
            <p style="margin:6px 0 0;font-size:13px;color:#5f6368;"><strong>Time:</strong> {SEND_TIME}</p>
          </td></tr>
        </table>
        <p style="color:#3c4043;font-size:14px;">If this was you, no action needed. If not, secure your account immediately:</p>
        <table cellpadding="0" cellspacing="0"><tr><td style="padding:16px 0;">
          <a href="https://accounts.google.com"
             style="background:#4285F4;color:#fff;padding:12px 28px;border-radius:4px;text-decoration:none;font-size:14px;font-weight:600;">
            Review Activity
          </a>
        </td></tr></table>
      </td></tr>
      <tr><td style="padding:16px 30px;border-top:1px solid #e8eaed;">
        <p style="color:#80868b;font-size:12px;margin:0;">© 2024 Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043</p>
      </td></tr>
    </table>
  </td></tr>
</table>
</body></html>""",
    },

    "🔵 PayPal — Account Limited": {
        "subject": "Your PayPal account access has been limited",
        "preview": "We've limited account access. Verify your info to restore it.",
        "from_name": "PayPal Service",
        "html": """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:Arial,sans-serif;">
<table width="100%" bgcolor="#f5f5f5" cellpadding="0" cellspacing="0">
  <tr><td align="center" style="padding:30px 0;">
    <table width="500" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:4px;border:1px solid #ddd;">
      <tr><td style="background:#003087;padding:18px 24px;border-radius:4px 4px 0 0;text-align:center;">
        <span style="color:#fff;font-size:26px;font-weight:bold;font-style:italic;">PayPal</span>
      </td></tr>
      <tr><td style="padding:28px 32px;">
        <h2 style="color:#2c2e2f;font-size:20px;margin:0 0 14px;">Your account access has been limited</h2>
        <p style="color:#444;font-size:14px;line-height:1.6;">
          Dear PayPal member,<br><br>
          We noticed unusual activity on your PayPal account associated with <strong>{TARGET_EMAIL}</strong>.
          To ensure the safety of your account, we have temporarily limited access until you verify your information.
        </p>
        <table cellpadding="0" cellspacing="0" style="background:#fef5e7;border-left:4px solid #f5a623;width:100%;margin:14px 0;">
          <tr><td style="padding:12px 16px;">
            <p style="margin:0;font-size:13px;color:#635e57;">⚠️ <strong>Action Required:</strong> Your account will be permanently limited if not verified within <strong>24 hours</strong>.</p>
          </td></tr>
        </table>
        <p style="font-size:14px;color:#444;">Please confirm your identity to restore full account access:</p>
        <table cellpadding="0" cellspacing="0"><tr><td style="padding:16px 0;">
          <a href="https://www.paypal.com"
             style="background:#009cde;color:#fff;padding:12px 32px;border-radius:4px;text-decoration:none;font-size:14px;font-weight:bold;">
            Confirm Your Identity
          </a>
        </td></tr></table>
      </td></tr>
      <tr><td style="background:#f5f5f5;padding:14px 24px;border-top:1px solid #ddd;border-radius:0 0 4px 4px;">
        <p style="color:#9da3a6;font-size:11px;margin:0;text-align:center;">
          PayPal • 2211 North First Street • San Jose, CA 95131
        </p>
      </td></tr>
    </table>
  </td></tr>
</table>
</body></html>""",
    },

    "🟠 Amazon — Order Suspended": {
        "subject": "Action Required: Your Amazon order has been suspended",
        "preview": "Your recent order has been put on hold. Verify payment details.",
        "from_name": "Amazon Customer Service",
        "html": """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f0f2f2;font-family:Arial,sans-serif;">
<table width="100%" bgcolor="#f0f2f2" cellpadding="0" cellspacing="0">
  <tr><td align="center" style="padding:30px 0;">
    <table width="520" cellpadding="0" cellspacing="0" style="background:#fff;border:1px solid #ddd;">
      <tr><td style="background:#131921;padding:14px 24px;">
        <span style="color:#ff9900;font-size:28px;font-weight:bold;letter-spacing:-1px;">amazon</span>
      </td></tr>
      <tr><td style="padding:28px 32px;">
        <h2 style="color:#0f1111;font-size:19px;margin:0 0 12px;">Your order has been suspended</h2>
        <p style="color:#555;font-size:14px;line-height:1.6;">
          Hello,<br><br>
          We were unable to process the payment for your recent order. Your account
          <strong>{TARGET_EMAIL}</strong> requires immediate attention.
        </p>
        <table cellpadding="0" cellspacing="0" style="background:#fff3cd;border:1px solid #ff9900;border-radius:4px;width:100%;margin:16px 0;">
          <tr><td style="padding:12px 16px;">
            <p style="margin:0 0 6px;font-size:13px;color:#333;"><strong>Order #: 402-8827491-7364712</strong></p>
            <p style="margin:0;font-size:13px;color:#c45500;">Status: <strong>Payment Failed — Action Required</strong></p>
          </td></tr>
        </table>
        <p style="font-size:14px;color:#555;">Update your payment method to release your order:</p>
        <table cellpadding="0" cellspacing="0"><tr><td style="padding:16px 0;">
          <a href="https://www.amazon.com"
             style="background:#ff9900;color:#131921;padding:12px 28px;border-radius:4px;text-decoration:none;font-size:14px;font-weight:bold;">
            Update Payment Method
          </a>
        </td></tr></table>
      </td></tr>
      <tr><td style="background:#f0f2f2;padding:14px 24px;border-top:1px solid #ddd;text-align:center;">
        <p style="color:#999;font-size:11px;margin:0;">© 2024 Amazon.com, Inc. or its affiliates. All rights reserved.</p>
      </td></tr>
    </table>
  </td></tr>
</table>
</body></html>""",
    },
}


# ══════════════════════════════════════════════════════════════
#  Phishing Service Module
# ══════════════════════════════════════════════════════════════
class PhishingServiceModule:
    def __init__(self, parent):
        if isinstance(parent, (tk.Tk, tk.Toplevel)):
            self.window = tk.Toplevel(parent)
        else:
            self.window = parent
        self.window.title("Phishing Email Service — SECURENETRA")
        self.window.geometry("1400x800")
        self.window.configure(bg=BG_DARK)
        self._selected_template = list(TEMPLATES.keys())[0]
        self._build_ui()

    def _build_ui(self):
        # Header
        header = tk.Frame(self.window, bg=PANEL_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="  🎣  Phishing Email Service", font=("Consolas", 20, "bold"),
                 bg=PANEL_BG, fg=ACCENT, anchor="w").pack(side="left", padx=24, pady=14)

        tk.Label(header, text="⚠  For Authorised Security Testing Only", font=("Consolas", 11, "bold"),
                 bg=PANEL_BG, fg=WARN_C).pack(side="right", padx=24)

        # Disclaimer bar
        disc = tk.Frame(self.window, bg="#0a0a0a", height=36)
        disc.pack(fill="x")
        disc.pack_propagate(False)

        tk.Label(disc, text="🔐  This tool is strictly for authorised penetration testing and security awareness training. Misuse is illegal.",
                 font=("Consolas", 10), bg="#0a0a0a", fg=WARN_C, anchor="w").pack(fill="x", padx=20, pady=8)

        # Main layout
        body = tk.Frame(self.window, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=16, pady=14)

        # Left: Template list
        left_panel = tk.Frame(body, bg=PANEL_BG, relief="solid", bd=1, width=220)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        tk.Label(left_panel, text="EMAIL TEMPLATES", font=("Consolas", 9, "bold"),
                 bg=PANEL_BG, fg=TEXT_MUTED, anchor="w").pack(fill="x", padx=14, pady=(14, 6))

        self._template_buttons = {}
        for name in TEMPLATES:
            btn = tk.Button(left_panel, text=name, anchor="w", font=("Segoe UI", 12),
                           bg=PANEL_BG, fg=TEXT_MUTED, activebackground="#003300",
                           relief="flat", bd=0, padx=20, pady=15, cursor="hand2",
                           command=lambda n=name: self._select_template(n))
            btn.pack(fill="x", padx=8, pady=2)
            self._template_buttons[name] = btn

        # Center: Preview
        center_panel = tk.Frame(body, bg=PANEL_BG, relief="solid", bd=1)
        center_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(center_panel, text="TEMPLATE PREVIEW", font=("Consolas", 9, "bold"),
                 bg=PANEL_BG, fg=TEXT_MUTED, anchor="w").pack(fill="x", padx=16, pady=(14, 4))

        self.preview_subject = tk.Label(center_panel, text="", font=("Consolas", 12, "bold"),
                                        bg=PANEL_BG, fg=ACCENT, anchor="w", wraplength=500)
        self.preview_subject.pack(fill="x", padx=16, pady=(0, 4))

        self.preview_hint = tk.Label(center_panel, text="", font=("Segoe UI", 11),
                                     bg=PANEL_BG, fg=TEXT_MUTED, anchor="w", wraplength=500)
        self.preview_hint.pack(fill="x", padx=16, pady=(0, 8))

        tk.Frame(center_panel, height=1, bg=BORDER).pack(fill="x", padx=16, pady=(0, 8))

        preview_frame = tk.Frame(center_panel, bg=PANEL_BG)
        preview_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        preview_scroll = tk.Scrollbar(preview_frame)
        preview_scroll.pack(side="right", fill="y")

        self.html_preview = tk.Text(preview_frame, bg=ENTRY_BG, fg="#00FF66", font=("Consolas", 9),
                                    relief="solid", bd=1, wrap="word", state="disabled",
                                    yscrollcommand=preview_scroll.set, height=20)
        self.html_preview.pack(side="left", fill="both", expand=True)
        preview_scroll.config(command=self.html_preview.yview)

        # Right: Config panel
        self._build_config_panel(body)

        # Select first template
        self.window.after(50, lambda: self._select_template(self._selected_template))

    def _build_config_panel(self, parent):
        panel = tk.Frame(parent, bg=PANEL_BG, relief="solid", bd=1, width=280)
        panel.pack(side="right", fill="y")
        panel.pack_propagate(False)

        canvas = tk.Canvas(panel, bg=PANEL_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(panel, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=PANEL_BG)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(scrollable_frame, text="SEND CONFIGURATION", font=("Consolas", 9, "bold"),
                 bg=PANEL_BG, fg=TEXT_MUTED, anchor="w").pack(fill="x", padx=4, pady=(8, 10))

        def field(label, placeholder, attr, show=""):
            tk.Label(scrollable_frame, text=label, font=("Consolas", 9, "bold"),
                     bg=PANEL_BG, fg=TEXT_MUTED, anchor="w").pack(fill="x", padx=4, pady=(8, 2))
            e = tk.Entry(scrollable_frame, font=("Consolas", 12), bg=ENTRY_BG, fg=TEXT_MAIN,
                        relief="solid", bd=1, insertbackground=TEXT_MAIN, show=show)
            if placeholder and not show:
                e.insert(0, placeholder)
            e.pack(fill="x", padx=4, ipady=8)
            setattr(self, attr, e)

        tk.Label(scrollable_frame, text="TARGET", font=("Consolas", 9, "bold"),
                 bg=PANEL_BG, fg=ERROR_C, anchor="w").pack(fill="x", padx=4, pady=(4, 6))

        field("TARGET EMAIL", "victim@example.com", "target_entry")
        field("YOUR EMAIL (sender)", "bhargava9553@gmail.com", "sender_email")
        field("APP PASSWORD", "brwp bkvy jtaz ygwc", "smtp_password", show="●")
        field("SENDER NAME", "Security Team", "sender_name_entry")
        field("CUSTOM SUBJECT (optional)", "", "custom_subject")

        tk.Frame(scrollable_frame, height=1, bg=BORDER).pack(fill="x", padx=4, pady=14)

        self.status_label = tk.Label(scrollable_frame, text="Ready to send", font=("Consolas", 11),
                                     bg=PANEL_BG, fg=TEXT_MUTED, wraplength=240)
        self.status_label.pack(pady=(4, 4))

        self.send_btn = tk.Button(scrollable_frame, text="  🎣  SEND PHISHING EMAIL", font=("Consolas", 12, "bold"),
                                  bg="#000000", fg=ACCENT, activebackground="#003300", relief="solid", bd=2,
                                  cursor="hand2", command=self._send_email, pady=10)
        self.send_btn.pack(fill="x", padx=4, pady=(4, 10))

        tk.Label(scrollable_frame, text="SEND LOG", font=("Consolas", 9, "bold"),
                 bg=PANEL_BG, fg=TEXT_MUTED, anchor="w").pack(fill="x", padx=4, pady=(14, 4))

        self.log_box = tk.Text(scrollable_frame, bg=ENTRY_BG, fg=SUCCESS_C, font=("Consolas", 10),
                              relief="solid", bd=1, height=10, wrap="word", state="disabled")
        self.log_box.pack(fill="x", padx=4, pady=(0, 10))

    def _select_template(self, name):
        self._selected_template = name
        for n, btn in self._template_buttons.items():
            if n == name:
                btn.configure(bg="#003300", fg=ACCENT)
            else:
                btn.configure(bg=PANEL_BG, fg=TEXT_MUTED)

        tpl = TEMPLATES[name]
        self.preview_subject.configure(text=f"📨  {tpl['subject']}")
        self.preview_hint.configure(text=f"Preview: {tpl['preview']}")

        self.html_preview.configure(state="normal")
        self.html_preview.delete("1.0", "end")
        
        preview_text = f"""EMAIL TEMPLATE: {name}

SUBJECT: {tpl['subject']}

FROM: {tpl['from_name']}

PREVIEW: {tpl['preview']}

This email will be sent as a professional HTML email with:
• Brand-specific styling and colors
• Realistic sender information
• Embedded links and buttons
• Professional formatting
• Target email personalization

The actual HTML template is ready to send."""
        
        self.html_preview.insert("1.0", preview_text)
        self.html_preview.configure(state="disabled")

        if hasattr(self, "sender_name_entry"):
            self.sender_name_entry.delete(0, "end")
            self.sender_name_entry.insert(0, tpl["from_name"])

    def _send_email(self):
        target = self.target_entry.get().strip()
        sender_email = self.sender_email.get().strip()
        smtp_pass = self.smtp_password.get().strip()
        sender_name = self.sender_name_entry.get().strip()
        
        if not all([target, sender_email, smtp_pass, sender_name]):
            messagebox.showerror("Missing Information", "Please fill in all required fields.")
            return

        self._set_status("⏳  Sending email...", ACCENT2)
        self.send_btn.configure(state="disabled", text="  ⏳  Sending...")
        
        threading.Thread(target=self._send_thread, daemon=True).start()

    def _send_thread(self):
        target = self.target_entry.get().strip()
        sender_email = self.sender_email.get().strip()
        smtp_pass = self.smtp_password.get().strip()
        sender_name = self.sender_name_entry.get().strip()
        tpl = TEMPLATES[self._selected_template]
        subject = self.custom_subject.get().strip() or tpl["subject"]
        send_time = datetime.now().strftime("%d %b %Y, %I:%M %p")
        html_body = tpl["html"].replace("{TARGET_EMAIL}", target).replace("{SEND_TIME}", send_time)

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
            server.ehlo()
            server.starttls()
            server.login(sender_email, smtp_pass)

            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{sender_name} <{sender_email}>"
            msg["To"] = target

            msg.attach(MIMEText(f"Please view this email in an HTML-compatible client.\n\nSubject: {subject}", "plain"))
            msg.attach(MIMEText(html_body, "html"))

            server.sendmail(sender_email, target, msg.as_string())
            server.quit()
            
            self.window.after(0, lambda: self._set_status("✅  Email sent successfully!", SUCCESS_C))
            self.window.after(0, lambda: self._log(f"✔  Email sent → {target}"))
            self.window.after(0, lambda: messagebox.showinfo("Success", f"Phishing email sent to {target}"))
            
            try:
                stats_tracker.record_phishing_sent(target=target, template=self._selected_template)
            except:
                pass

        except smtplib.SMTPAuthenticationError:
            self.window.after(0, lambda: self._set_status("⚠  Authentication failed. Check credentials.", ERROR_C))
            self.window.after(0, lambda: self._log("✘  SMTP Auth Error"))
        except Exception as e:
            self.window.after(0, lambda: self._set_status(f"⚠  Error: {str(e)[:50]}", ERROR_C))
            self.window.after(0, lambda: self._log(f"✘  Error: {str(e)}"))
        finally:
            self.window.after(0, lambda: self.send_btn.configure(state="normal", text="  🎣  SEND PHISHING EMAIL"))

    def _set_status(self, msg, color=TEXT_MUTED):
        self.status_label.configure(text=msg, fg=color)

    def _log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{ts}] {msg}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
