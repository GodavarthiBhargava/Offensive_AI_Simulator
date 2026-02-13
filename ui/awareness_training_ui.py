import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sqlite3
import os
from datetime import datetime

class AwarenessTrainingModule:
    def __init__(self, window):
        self.window = window
        self.window.title("Awareness Training")
        self.window.geometry("1200x750")
        self.window.configure(bg="#2E2E2E")
        
        # Top bar
        navbar = tk.Frame(window, bg="#1F1F1F", height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        
        tk.Label(navbar, text="🎓 SECURITY AWARENESS TRAINING",
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
        self.mistakes_tab = tk.Frame(tab_control, bg="#2E2E2E")
        self.password_tab = tk.Frame(tab_control, bg="#2E2E2E")
        self.phishing_tab = tk.Frame(tab_control, bg="#2E2E2E")
        self.quiz_tab = tk.Frame(tab_control, bg="#2E2E2E")
        
        tab_control.add(self.mistakes_tab, text="⚠️ Your Mistakes")
        tab_control.add(self.password_tab, text="🔐 Password Security")
        tab_control.add(self.phishing_tab, text="📧 Phishing Awareness")
        tab_control.add(self.quiz_tab, text="📝 Security Quiz")
        
        tab_control.pack(fill="both", expand=True)
        
        self.setup_mistakes_tab()
        self.setup_password_tab()
        self.setup_phishing_tab()
        self.setup_quiz_tab()
    
    def setup_mistakes_tab(self):
        """Setup mistakes review tab"""
        content = tk.Frame(self.mistakes_tab, bg="#2E2E2E")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(content, text="YOUR SECURITY MISTAKES", font=("Consolas", 16, "bold"),
                bg="#2E2E2E", fg="#FF4444").pack(pady=(0, 20))
        
        # Mistakes display
        self.mistakes_text = scrolledtext.ScrolledText(content, font=("Consolas", 11, "bold"),
                                                      bg="#000000", fg="#00FF66",
                                                      relief="solid", bd=2, wrap=tk.WORD)
        self.mistakes_text.pack(fill="both", expand=True, pady=(0, 10))
        
        # Refresh button
        refresh_btn = tk.Button(content, text="🔄 REFRESH MISTAKES",
                               font=("Consolas", 11, "bold"), bg="#000000", fg="#00FF66",
                               activebackground="#003300", relief="solid", bd=2,
                               cursor="hand2", command=self.load_mistakes)
        refresh_btn.pack(ipady=8, ipadx=20)
        
        self.load_mistakes()
    
    def setup_password_tab(self):
        """Setup password security tips tab"""
        content = tk.Frame(self.password_tab, bg="#2E2E2E")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(content, text="PASSWORD SECURITY BEST PRACTICES", font=("Consolas", 16, "bold"),
                bg="#2E2E2E", fg="#00FF66").pack(pady=(0, 20))
        
        tips_text = scrolledtext.ScrolledText(content, font=("Consolas", 11, "bold"),
                                             bg="#000000", fg="#00FF66",
                                             relief="solid", bd=2, wrap=tk.WORD)
        tips_text.pack(fill="both", expand=True)
        
        tips = """
🔐 PASSWORD SECURITY GUIDELINES

1. LENGTH MATTERS
   ✅ Use at least 12-16 characters
   ❌ Avoid short passwords (less than 8 characters)
   
   Example:
   ❌ Bad: "pass123"
   ✅ Good: "MyD0g!sN@med$p0t2024"

2. COMPLEXITY IS KEY
   ✅ Mix uppercase, lowercase, numbers, and symbols
   ❌ Don't use only letters or only numbers
   
   Example:
   ❌ Bad: "password"
   ✅ Good: "P@ssw0rd!2024#Secure"

3. AVOID PERSONAL INFORMATION
   ❌ Don't use your name, birthday, or family names
   ❌ Don't use common words or patterns
   
   Example:
   ❌ Bad: "john1990" or "john123"
   ✅ Good: "Tr0pic@l$unset!42"

4. UNIQUE PASSWORDS
   ✅ Use different passwords for different accounts
   ❌ Never reuse passwords across sites
   
   💡 Tip: Use a password manager to store unique passwords

5. ENABLE MULTI-FACTOR AUTHENTICATION (MFA)
   ✅ Always enable 2FA/MFA when available
   ✅ Use authenticator apps (Google Authenticator, Authy)
   ❌ Avoid SMS-based 2FA when possible

6. REGULAR UPDATES
   ✅ Change passwords every 3-6 months
   ✅ Change immediately if breach suspected
   ❌ Don't wait for a security incident

7. PASSWORD MANAGERS
   ✅ Use reputable password managers (LastPass, 1Password, Bitwarden)
   ✅ Let them generate strong random passwords
   ✅ Only remember one master password

8. COMMON MISTAKES TO AVOID
   ❌ "password123"
   ❌ "qwerty"
   ❌ "123456"
   ❌ "admin"
   ❌ Your name + year
   ❌ Sequential patterns (abc123, 111111)

9. PASSPHRASE METHOD
   ✅ Use memorable phrases with modifications
   
   Example:
   "I love pizza on Fridays!" → "!L0v3P!zz@0nFr!d@ys!"

10. SECURITY QUESTIONS
    ✅ Use fake answers that only you know
    ❌ Don't use real answers (easily guessable)
    
    Example:
    Question: "Mother's maiden name?"
    ❌ Bad: Real name
    ✅ Good: "Tr0pic@lP@rr0t42"

═══════════════════════════════════════════════════════════

💡 REMEMBER: Your password is the first line of defense!

🎯 ACTION ITEMS:
1. Review all your passwords today
2. Update weak passwords immediately
3. Enable MFA on all important accounts
4. Consider using a password manager
5. Never share passwords with anyone
"""
        
        tips_text.insert(1.0, tips)
        tips_text.config(state="disabled")
    
    def setup_phishing_tab(self):
        """Setup phishing awareness tab"""
        content = tk.Frame(self.phishing_tab, bg="#2E2E2E")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(content, text="PHISHING AWARENESS GUIDE", font=("Consolas", 16, "bold"),
                bg="#2E2E2E", fg="#00FF66").pack(pady=(0, 20))
        
        guide_text = scrolledtext.ScrolledText(content, font=("Consolas", 11, "bold"),
                                              bg="#000000", fg="#00FF66",
                                              relief="solid", bd=2, wrap=tk.WORD)
        guide_text.pack(fill="both", expand=True)
        
        guide = """
📧 PHISHING DETECTION & PREVENTION

═══════════════════════════════════════════════════════════

🚨 RED FLAGS - SIGNS OF PHISHING

1. URGENCY & THREATS
   ⚠️ "Act now or your account will be closed!"
   ⚠️ "Urgent action required within 24 hours!"
   ⚠️ "Your account has been suspended!"
   
   💡 Legitimate companies don't create artificial urgency

2. SUSPICIOUS SENDER
   ⚠️ Misspelled email addresses (paypa1@email.com)
   ⚠️ Generic greetings ("Dear Customer")
   ⚠️ Unfamiliar sender addresses
   
   ✅ Always verify sender through official channels

3. REQUESTS FOR PERSONAL INFORMATION
   ⚠️ Asking for passwords
   ⚠️ Requesting credit card details
   ⚠️ Asking for SSN or sensitive data
   
   💡 Real companies NEVER ask for passwords via email

4. SUSPICIOUS LINKS
   ⚠️ Hover over links to see real destination
   ⚠️ Links with IP addresses (http://192.168.1.1)
   ⚠️ Shortened URLs (bit.ly, tinyurl)
   ⚠️ Misspelled domains (amaz0n.com, g00gle.com)
   
   ✅ Type URLs directly into browser

5. POOR GRAMMAR & SPELLING
   ⚠️ Multiple spelling errors
   ⚠️ Awkward phrasing
   ⚠️ Unprofessional formatting
   
   💡 Professional companies proofread their emails

6. UNEXPECTED ATTACHMENTS
   ⚠️ Unsolicited attachments
   ⚠️ Executable files (.exe, .bat)
   ⚠️ Compressed files from unknown sources
   
   ❌ NEVER open suspicious attachments

7. TOO GOOD TO BE TRUE
   ⚠️ "You've won $10,000!"
   ⚠️ "Free iPhone - Click here!"
   ⚠️ "Congratulations! You're a winner!"
   
   💡 If it sounds too good to be true, it is

═══════════════════════════════════════════════════════════

✅ WHAT TO DO IF YOU RECEIVE A PHISHING EMAIL

1. DON'T CLICK any links or attachments
2. DON'T REPLY to the email
3. DON'T PROVIDE any information
4. VERIFY through official channels
5. REPORT to your IT department
6. DELETE the email
7. MARK as spam/phishing

═══════════════════════════════════════════════════════════

🛡️ PROTECTION STRATEGIES

1. VERIFY BEFORE YOU TRUST
   • Call the company using official phone number
   • Visit website by typing URL directly
   • Check official social media accounts

2. USE EMAIL FILTERS
   • Enable spam filters
   • Use email security tools
   • Keep software updated

3. EDUCATE YOURSELF
   • Stay informed about new phishing tactics
   • Participate in security training
   • Share knowledge with colleagues

4. ENABLE SECURITY FEATURES
   • Use email authentication (SPF, DKIM, DMARC)
   • Enable link protection
   • Use anti-phishing browser extensions

5. REPORT PHISHING
   • Report to IT/Security team
   • Forward to abuse@[company].com
   • Report to Anti-Phishing Working Group (reportphishing@apwg.org)

═══════════════════════════════════════════════════════════

📱 MOBILE PHISHING (SMISHING)

Watch out for:
• Fake delivery notifications
• Bank security alerts
• Prize/lottery messages
• Requests to click links

💡 Same rules apply: Verify before you trust!

═══════════════════════════════════════════════════════════

🎯 REMEMBER: When in doubt, throw it out!
"""
        
        guide_text.insert(1.0, guide)
        guide_text.config(state="disabled")
    
    def setup_quiz_tab(self):
        """Setup security quiz tab"""
        content = tk.Frame(self.quiz_tab, bg="#2E2E2E")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(content, text="SECURITY AWARENESS QUIZ", font=("Consolas", 16, "bold"),
                bg="#2E2E2E", fg="#00FF66").pack(pady=(0, 20))
        
        # Quiz questions
        self.questions = [
            {
                "q": "What is the minimum recommended password length?",
                "options": ["6 characters", "8 characters", "12 characters", "16 characters"],
                "correct": 2
            },
            {
                "q": "Should you use the same password for multiple accounts?",
                "options": ["Yes, it's easier to remember", "No, use unique passwords", "Only for unimportant accounts", "Yes, if it's strong"],
                "correct": 1
            },
            {
                "q": "What should you do if you receive a suspicious email?",
                "options": ["Click the link to verify", "Reply asking if it's real", "Delete and report it", "Forward to friends"],
                "correct": 2
            },
            {
                "q": "Is it safe to share your password with IT support?",
                "options": ["Yes, they need it to help", "No, never share passwords", "Only over the phone", "Yes, via email"],
                "correct": 1
            },
            {
                "q": "What is phishing?",
                "options": ["A type of fishing", "Fraudulent attempt to obtain sensitive information", "A computer virus", "A firewall"],
                "correct": 1
            }
        ]
        
        self.current_question = 0
        self.score = 0
        
        # Question display
        self.question_frame = tk.Frame(content, bg="#1F1F1F", relief="solid", bd=2)
        self.question_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        self.question_label = tk.Label(self.question_frame, text="", font=("Consolas", 12, "bold"),
                                       bg="#1F1F1F", fg="#00FF66", wraplength=800, justify="left")
        self.question_label.pack(pady=20, padx=20)
        
        # Options
        self.option_var = tk.IntVar()
        self.option_buttons = []
        
        for i in range(4):
            rb = tk.Radiobutton(self.question_frame, text="", variable=self.option_var, value=i,
                               font=("Consolas", 11, "bold"), bg="#1F1F1F", fg="#00FF66",
                               selectcolor="#000000", activebackground="#1F1F1F",
                               activeforeground="#00FF66", wraplength=700, justify="left")
            rb.pack(anchor="w", padx=40, pady=5)
            self.option_buttons.append(rb)
        
        # Buttons
        btn_frame = tk.Frame(content, bg="#2E2E2E")
        btn_frame.pack()
        
        self.submit_btn = tk.Button(btn_frame, text="SUBMIT ANSWER",
                                    font=("Consolas", 11, "bold"), bg="#000000", fg="#00FF66",
                                    activebackground="#003300", relief="solid", bd=2,
                                    cursor="hand2", command=self.check_answer)
        self.submit_btn.pack(side="left", padx=5, ipady=8, ipadx=20)
        
        restart_btn = tk.Button(btn_frame, text="RESTART QUIZ",
                               font=("Consolas", 11, "bold"), bg="#000000", fg="#FFAA00",
                               activebackground="#333300", relief="solid", bd=2,
                               cursor="hand2", command=self.restart_quiz)
        restart_btn.pack(side="left", padx=5, ipady=8, ipadx=20)
        
        self.load_question()
    
    def load_mistakes(self):
        """Load user mistakes from databases"""
        self.mistakes_text.delete(1.0, tk.END)
        
        self.mistakes_text.insert(tk.END, "⚠️ YOUR SECURITY MISTAKES & LEARNING POINTS\n")
        self.mistakes_text.insert(tk.END, "="*70 + "\n\n")
        
        mistakes_found = False
        
        # Check password attacks
        if os.path.exists("cases/attack_results.db"):
            conn = sqlite3.connect("cases/attack_results.db")
            cursor = conn.cursor()
            cursor.execute("SELECT first_name, last_name, cracked_password, result FROM attack_results WHERE cracked_password != 'N/A'")
            results = cursor.fetchall()
            conn.close()
            
            if results:
                mistakes_found = True
                self.mistakes_text.insert(tk.END, "🔐 WEAK PASSWORDS DETECTED\n\n")
                for r in results:
                    self.mistakes_text.insert(tk.END, f"User: {r[0]} {r[1]}\n")
                    self.mistakes_text.insert(tk.END, f"Cracked Password: '{r[2]}'\n")
                    self.mistakes_text.insert(tk.END, f"💡 Lesson: Use longer, more complex passwords\n")
                    self.mistakes_text.insert(tk.END, "-"*70 + "\n\n")
        
        # Check phishing clicks
        if os.path.exists("cases/phishing_campaigns.db"):
            conn = sqlite3.connect("cases/phishing_campaigns.db")
            cursor = conn.cursor()
            cursor.execute("SELECT campaign_name, scenario_type FROM campaigns WHERE credentials_entered = 1")
            results = cursor.fetchall()
            conn.close()
            
            if results:
                mistakes_found = True
                self.mistakes_text.insert(tk.END, "📧 PHISHING VULNERABILITIES\n\n")
                for r in results:
                    self.mistakes_text.insert(tk.END, f"Campaign: {r[0]}\n")
                    self.mistakes_text.insert(tk.END, f"Scenario: {r[1]}\n")
                    self.mistakes_text.insert(tk.END, f"💡 Lesson: Always verify before entering credentials\n")
                    self.mistakes_text.insert(tk.END, "-"*70 + "\n\n")
        
        if not mistakes_found:
            self.mistakes_text.insert(tk.END, "✅ No security mistakes recorded yet!\n\n")
            self.mistakes_text.insert(tk.END, "Keep up the good security practices!\n")
    
    def load_question(self):
        """Load current quiz question"""
        if self.current_question >= len(self.questions):
            self.show_results()
            return
        
        q = self.questions[self.current_question]
        self.question_label.config(text=f"Question {self.current_question + 1}/{len(self.questions)}:\n\n{q['q']}")
        
        for i, option in enumerate(q['options']):
            self.option_buttons[i].config(text=option)
        
        self.option_var.set(-1)
    
    def check_answer(self):
        """Check quiz answer"""
        if self.option_var.get() == -1:
            messagebox.showwarning("Warning", "Please select an answer")
            return
        
        q = self.questions[self.current_question]
        if self.option_var.get() == q['correct']:
            self.score += 1
            messagebox.showinfo("Correct!", "✅ That's correct!")
        else:
            correct_answer = q['options'][q['correct']]
            messagebox.showinfo("Incorrect", f"❌ Incorrect.\n\nCorrect answer: {correct_answer}")
        
        self.current_question += 1
        self.load_question()
    
    def show_results(self):
        """Show quiz results"""
        percentage = (self.score / len(self.questions)) * 100
        
        if percentage >= 80:
            grade = "EXCELLENT"
            color = "#00FF66"
        elif percentage >= 60:
            grade = "GOOD"
            color = "#FFAA00"
        else:
            grade = "NEEDS IMPROVEMENT"
            color = "#FF4444"
        
        result_msg = f"Quiz Complete!\n\nScore: {self.score}/{len(self.questions)} ({percentage:.0f}%)\n\nGrade: {grade}"
        messagebox.showinfo("Quiz Results", result_msg)
        
        self.submit_btn.config(state="disabled")
    
    def restart_quiz(self):
        """Restart quiz"""
        self.current_question = 0
        self.score = 0
        self.submit_btn.config(state="normal")
        self.load_question()


if __name__ == "__main__":
    root = tk.Tk()
    AwarenessTrainingModule(root)
    root.mainloop()
