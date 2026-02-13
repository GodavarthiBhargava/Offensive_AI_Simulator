import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import os
from datetime import datetime
import random

class SocialEngineeringModule:
    def __init__(self, window):
        self.window = window
        self.window.title("Voice / Social Engineering Simulator")
        self.window.geometry("1200x700")
        self.window.configure(bg="#2E2E2E")
        
        self.init_se_db()
        
        # Top bar
        navbar = tk.Frame(window, bg="#1F1F1F", height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        
        tk.Label(navbar, text="📞 VOICE / SOCIAL ENGINEERING SIMULATOR",
                font=("Consolas", 14, "bold"), bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        tk.Frame(window, bg="#003300", height=1).pack(fill="x")
        
        # Main content
        content = tk.Frame(window, bg="#2E2E2E")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel - Scenario selection
        left_panel = tk.Frame(content, bg="#1F1F1F", relief="solid", bd=2)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        tk.Label(left_panel, text="🎭 SCENARIO SELECTION", font=("Consolas", 14, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        # Scenario selection
        scenarios_frame = tk.Frame(left_panel, bg="#1F1F1F")
        scenarios_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.scenarios = {
            "IT Support Call": {
                "description": "Pretend to be IT support requesting password reset",
                "triggers": ["Authority", "Urgency", "Technical jargon"],
                "difficulty": "Medium"
            },
            "CEO Fraud": {
                "description": "Impersonate CEO requesting urgent wire transfer",
                "triggers": ["Authority", "Urgency", "Fear"],
                "difficulty": "Hard"
            },
            "Delivery Notice": {
                "description": "Fake delivery company requesting personal info",
                "triggers": ["Curiosity", "Expectation"],
                "difficulty": "Easy"
            },
            "Bank Security": {
                "description": "Fake bank security checking suspicious activity",
                "triggers": ["Fear", "Urgency", "Authority"],
                "difficulty": "Medium"
            },
            "Survey/Prize": {
                "description": "Survey with prize offer to collect information",
                "triggers": ["Greed", "Curiosity"],
                "difficulty": "Easy"
            }
        }
        
        self.selected_scenario = tk.StringVar(value="IT Support Call")
        
        for scenario, details in self.scenarios.items():
            rb = tk.Radiobutton(scenarios_frame, text=scenario,
                               variable=self.selected_scenario, value=scenario,
                               font=("Consolas", 11, "bold"), bg="#1F1F1F",
                               fg="#00FF66", selectcolor="#000000",
                               activebackground="#1F1F1F", activeforeground="#00FF66",
                               command=self.update_scenario_details)
            rb.pack(anchor="w", pady=5)
        
        # Scenario details
        self.details_frame = tk.Frame(left_panel, bg="#000000", relief="solid", bd=1)
        self.details_frame.pack(fill="x", padx=10, pady=10)
        
        self.details_text = tk.Text(self.details_frame, bg="#000000", fg="#00FF66",
                                   font=("Consolas", 10, "bold"), height=8, wrap=tk.WORD,
                                   relief="flat", padx=10, pady=10)
        self.details_text.pack(fill="both", expand=True)
        
        # Generate script button
        gen_btn = tk.Button(left_panel, text="🤖 GENERATE AI SCRIPT",
                           font=("Consolas", 12, "bold"), bg="#000000", fg="#00FF66",
                           activebackground="#003300", relief="solid", bd=2,
                           cursor="hand2", command=self.generate_script)
        gen_btn.pack(pady=10, ipady=10, ipadx=20)
        
        # Right panel - Script display
        right_panel = tk.Frame(content, bg="#1F1F1F", relief="solid", bd=2)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        tk.Label(right_panel, text="📜 CALL SCRIPT", font=("Consolas", 14, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        self.script_text = scrolledtext.ScrolledText(right_panel, font=("Consolas", 11, "bold"),
                                                    bg="#000000", fg="#00FF66",
                                                    relief="flat", padx=15, pady=15, wrap=tk.WORD)
        self.script_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Awareness score
        score_frame = tk.Frame(right_panel, bg="#1F1F1F")
        score_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(score_frame, text="Awareness Score:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(side="left", padx=5)
        
        self.score_label = tk.Label(score_frame, text="0/100", font=("Consolas", 14, "bold"),
                                    bg="#1F1F1F", fg="#FF4444")
        self.score_label.pack(side="left", padx=5)
        
        # Test button
        test_btn = tk.Button(right_panel, text="🎯 RUN SIMULATION TEST",
                            font=("Consolas", 11, "bold"), bg="#000000", fg="#00FF66",
                            activebackground="#003300", relief="solid", bd=2,
                            cursor="hand2", command=self.run_simulation)
        test_btn.pack(pady=10, ipady=8, ipadx=20)
        
        self.update_scenario_details()
    
    def init_se_db(self):
        """Initialize social engineering database"""
        os.makedirs("cases", exist_ok=True)
        conn = sqlite3.connect("cases/social_engineering.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS simulations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scenario_type TEXT,
                script_used TEXT,
                user_response TEXT,
                awareness_score INTEGER,
                timestamp TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def update_scenario_details(self):
        """Update scenario details display"""
        scenario = self.selected_scenario.get()
        details = self.scenarios[scenario]
        
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, f"📋 SCENARIO: {scenario}\n\n")
        self.details_text.insert(tk.END, f"Description:\n{details['description']}\n\n")
        self.details_text.insert(tk.END, f"Psychological Triggers:\n")
        for trigger in details['triggers']:
            self.details_text.insert(tk.END, f"  • {trigger}\n")
        self.details_text.insert(tk.END, f"\nDifficulty: {details['difficulty']}")
    
    def generate_script(self):
        """Generate AI call script"""
        scenario = self.selected_scenario.get()
        
        scripts = {
            "IT Support Call": """
🎭 CALL SCRIPT: IT Support

[Opening]
"Hello, this is John from IT Support. We've detected unusual activity on your account and need to verify your credentials immediately."

[Building Trust]
"I have your employee ID here as EMP-{random_number}. Can you confirm that's correct?"

[Creating Urgency]
"We need to reset your password right away to prevent unauthorized access. This is a critical security issue."

[The Ask]
"For verification purposes, can you provide your current password? I'll reset it immediately after."

[Alternative]
"Or you can click this secure link I'm sending to your email to reset it yourself."

[Closing]
"Thank you for your cooperation. Your account security is our priority."

⚠️ RED FLAGS:
- Real IT never asks for passwords
- Urgency is a manipulation tactic
- Verify caller through official channels
""",
            "CEO Fraud": """
🎭 CALL SCRIPT: CEO Impersonation

[Opening]
"This is [CEO Name]'s office. I'm calling on behalf of the CEO regarding an urgent matter."

[Authority]
"The CEO is in a meeting with investors and needs you to process a wire transfer immediately."

[Urgency + Fear]
"This is time-sensitive and confidential. The CEO specifically requested you handle this personally."

[The Ask]
"I'm sending you the wire transfer details. Please process it within the hour and confirm once done."

[Pressure]
"The CEO emphasized this is critical for the deal. Any delay could cost the company millions."

⚠️ RED FLAGS:
- Unusual urgency for financial transactions
- Bypassing normal approval processes
- Pressure to act without verification
- Always verify through official channels
""",
            "Delivery Notice": """
🎭 CALL SCRIPT: Fake Delivery

[Opening]
"Hello, this is Sarah from Express Delivery. We have a package for you but need to verify some information."

[Creating Interest]
"The package is marked as high-value and requires signature confirmation."

[The Ask]
"Can you confirm your full name, address, and phone number for our records?"

[Additional Info]
"Also, there's a small delivery fee of $5.99. Can I have your card details to process that?"

[Closing]
"Great! Your package will be delivered within 2 hours. Have a nice day!"

⚠️ RED FLAGS:
- Legitimate companies don't call for basic info
- Never give payment details over phone
- Verify tracking number on official website
""",
            "Bank Security": """
🎭 CALL SCRIPT: Fake Bank Security

[Opening]
"This is the Security Department from [Bank Name]. We've detected suspicious activity on your account."

[Creating Fear]
"There have been three unauthorized transactions totaling $2,500. We've temporarily frozen your account."

[Building Trust]
"For your protection, I need to verify your identity. Can you confirm the last 4 digits of your card?"

[The Ask]
"Now, to unlock your account, I'll need your full card number and the security code on the back."

[Urgency]
"We need to act fast before more charges go through. This is a critical security matter."

⚠️ RED FLAGS:
- Banks never ask for full card details
- Don't provide info to incoming callers
- Hang up and call bank's official number
- Verify through official channels only
""",
            "Survey/Prize": """
🎭 CALL SCRIPT: Survey with Prize

[Opening]
"Congratulations! You've been selected for our customer satisfaction survey with a chance to win $500!"

[Creating Interest]
"This will only take 2 minutes, and you'll be entered into our prize draw automatically."

[The Ask]
"First, can I have your full name, email, and phone number for the prize notification?"

[More Info]
"Great! Now, for verification, what's your date of birth and home address?"

[The Hook]
"To claim your prize if you win, we'll need your bank account details for direct deposit."

⚠️ RED FLAGS:
- Legitimate surveys don't ask for sensitive info
- Prize offers are often scams
- Never give financial details for "prizes"
- If it sounds too good to be true, it is
"""
        }
        
        script = scripts.get(scenario, "Script not available")
        self.script_text.delete(1.0, tk.END)
        self.script_text.insert(tk.END, script)
        
        messagebox.showinfo("Script Generated", "AI-generated call script ready!\n\nReview the red flags to learn how to detect this attack.")
    
    def run_simulation(self):
        """Run simulation test"""
        scenario = self.selected_scenario.get()
        
        # Simulate user response
        responses = [
            "User provided password immediately",
            "User asked to verify caller identity",
            "User hung up and called official number",
            "User requested to handle through official channels",
            "User fell for the social engineering attack"
        ]
        
        response = random.choice(responses)
        
        # Calculate awareness score
        if "verify" in response or "official" in response or "hung up" in response:
            score = random.randint(70, 100)
            color = "#00FF66"
        elif "asked" in response:
            score = random.randint(50, 70)
            color = "#FFAA00"
        else:
            score = random.randint(0, 50)
            color = "#FF4444"
        
        self.score_label.config(text=f"{score}/100", fg=color)
        
        # Save to database
        conn = sqlite3.connect("cases/social_engineering.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO simulations (scenario_type, script_used, user_response, awareness_score, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (scenario, "AI Generated", response, score, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        # Show result
        if score >= 70:
            result_msg = f"✅ EXCELLENT! (Score: {score}/100)\n\nYou demonstrated good security awareness!"
        elif score >= 50:
            result_msg = f"⚠️ MODERATE (Score: {score}/100)\n\nYou showed some caution but could improve."
        else:
            result_msg = f"❌ VULNERABLE (Score: {score}/100)\n\nYou fell for the social engineering attack!"
        
        result_msg += f"\n\nSimulated Response:\n{response}\n\n"
        result_msg += "💡 Always verify caller identity through official channels!"
        
        messagebox.showinfo("Simulation Result", result_msg)


if __name__ == "__main__":
    root = tk.Tk()
    SocialEngineeringModule(root)
    root.mainloop()
