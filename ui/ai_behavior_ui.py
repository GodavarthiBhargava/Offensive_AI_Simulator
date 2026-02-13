import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import os
from datetime import datetime
from collections import Counter
import re
import json

class AIBehaviorModule:
    def __init__(self, window):
        self.window = window
        self.window.title("AI Behavior Engine")
        self.window.geometry("1200x700")
        self.window.configure(bg="#2E2E2E")
        
        # Top bar
        navbar = tk.Frame(window, bg="#1F1F1F", height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        
        tk.Label(navbar, text="🧠 AI BEHAVIOR ENGINE - Pattern Learning & Prediction",
                font=("Consolas", 14, "bold"), bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        tk.Frame(window, bg="#003300", height=1).pack(fill="x")
        
        # Main content
        content = tk.Frame(window, bg="#2E2E2E")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel - Analysis
        left_panel = tk.Frame(content, bg="#1F1F1F", relief="solid", bd=2)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        tk.Label(left_panel, text="📊 LEARNED PATTERNS", font=("Consolas", 14, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        # Pattern display
        self.pattern_text = tk.Text(left_panel, bg="#000000", fg="#00FF66",
                                   font=("Consolas", 11, "bold"), relief="flat",
                                   padx=15, pady=15, wrap=tk.WORD)
        self.pattern_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Right panel - Predictions
        right_panel = tk.Frame(content, bg="#1F1F1F", relief="solid", bd=2)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        tk.Label(right_panel, text="🎯 AI PREDICTIONS", font=("Consolas", 14, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        # User input for prediction
        input_frame = tk.Frame(right_panel, bg="#1F1F1F")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Label(input_frame, text="First Name:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(anchor="w", pady=(0, 5))
        self.first_name_entry = tk.Entry(input_frame, font=("Consolas", 11, "bold"),
                                         bg="#000000", fg="#00FF66", relief="solid", bd=1)
        self.first_name_entry.pack(fill="x", ipady=5, pady=(0, 10))
        
        tk.Label(input_frame, text="Last Name:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(anchor="w", pady=(0, 5))
        self.last_name_entry = tk.Entry(input_frame, font=("Consolas", 11, "bold"),
                                        bg="#000000", fg="#00FF66", relief="solid", bd=1)
        self.last_name_entry.pack(fill="x", ipady=5, pady=(0, 10))
        
        predict_btn = tk.Button(input_frame, text="🔮 GENERATE PREDICTIONS",
                               font=("Consolas", 11, "bold"), bg="#000000", fg="#00FF66",
                               activebackground="#003300", relief="solid", bd=2,
                               cursor="hand2", command=self.generate_predictions)
        predict_btn.pack(fill="x", ipady=8)
        
        # Prediction display
        self.prediction_text = tk.Text(right_panel, bg="#000000", fg="#00FF66",
                                      font=("Consolas", 11, "bold"), relief="flat",
                                      padx=15, pady=15, wrap=tk.WORD)
        self.prediction_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Bottom buttons
        btn_frame = tk.Frame(content, bg="#2E2E2E")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        analyze_btn = tk.Button(btn_frame, text="🔄 ANALYZE DATABASE",
                               font=("Consolas", 11, "bold"), bg="#000000", fg="#00FF66",
                               activebackground="#003300", relief="solid", bd=2,
                               cursor="hand2", command=self.analyze_patterns)
        analyze_btn.pack(side="left", padx=5, ipady=8, ipadx=20)
        
        # Load initial analysis
        self.analyze_patterns()
    
    def analyze_patterns(self):
        """Analyze password patterns from database"""
        self.pattern_text.delete(1.0, tk.END)
        
        db_path = "cases/attack_results.db"
        if not os.path.exists(db_path):
            self.pattern_text.insert(tk.END, "⚠ No data available. Run password attacks first.\n")
            return
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT cracked_password FROM attack_results WHERE cracked_password != 'N/A'")
        passwords = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        if not passwords:
            self.pattern_text.insert(tk.END, "⚠ No cracked passwords found for analysis.\n")
            return
        
        self.pattern_text.insert(tk.END, f"📈 ANALYSIS RESULTS ({len(passwords)} passwords analyzed)\n")
        self.pattern_text.insert(tk.END, "="*60 + "\n\n")
        
        # Length analysis
        lengths = [len(p) for p in passwords]
        avg_length = sum(lengths) / len(lengths)
        self.pattern_text.insert(tk.END, f"📏 Average Length: {avg_length:.1f} characters\n")
        self.pattern_text.insert(tk.END, f"   Most common: {Counter(lengths).most_common(1)[0][0]} chars\n\n")
        
        # Character type analysis
        numeric_only = sum(1 for p in passwords if p.isdigit())
        alpha_only = sum(1 for p in passwords if p.isalpha())
        mixed = len(passwords) - numeric_only - alpha_only
        
        self.pattern_text.insert(tk.END, f"🔤 Character Types:\n")
        self.pattern_text.insert(tk.END, f"   Numeric only: {numeric_only} ({numeric_only/len(passwords)*100:.1f}%)\n")
        self.pattern_text.insert(tk.END, f"   Alpha only: {alpha_only} ({alpha_only/len(passwords)*100:.1f}%)\n")
        self.pattern_text.insert(tk.END, f"   Mixed: {mixed} ({mixed/len(passwords)*100:.1f}%)\n\n")
        
        # Common patterns
        patterns = []
        for p in passwords:
            if re.search(r'\d{3,}', p):
                patterns.append("Sequential numbers")
            if re.search(r'123', p):
                patterns.append("Contains '123'")
            if any(year in p for year in ['2024', '2025', '2023']):
                patterns.append("Contains year")
        
        if patterns:
            pattern_counts = Counter(patterns)
            self.pattern_text.insert(tk.END, f"🎯 Common Patterns:\n")
            for pattern, count in pattern_counts.most_common(5):
                self.pattern_text.insert(tk.END, f"   • {pattern}: {count} times\n")
            self.pattern_text.insert(tk.END, "\n")
        
        # Most common passwords
        common = Counter(passwords).most_common(5)
        self.pattern_text.insert(tk.END, f"🔥 Most Common Passwords:\n")
        for pwd, count in common:
            self.pattern_text.insert(tk.END, f"   • '{pwd}': {count} times\n")
    
    def generate_predictions(self):
        """Generate password predictions based on user info"""
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        
        if not first_name and not last_name:
            messagebox.showerror("Error", "Enter at least one name")
            return
        
        self.prediction_text.delete(1.0, tk.END)
        
        self.prediction_text.insert(tk.END, f"🎯 AI PREDICTIONS FOR: {first_name} {last_name}\n")
        self.prediction_text.insert(tk.END, "="*60 + "\n\n")
        
        predictions = []
        
        # Name-based predictions
        if first_name:
            predictions.extend([
                first_name.lower(),
                first_name.capitalize(),
                first_name.upper(),
                first_name.lower() + "123",
                first_name.lower() + "2024",
                first_name.lower() + "2025",
                first_name.lower() + "!",
                first_name.lower() + "@123"
            ])
        
        if last_name:
            predictions.extend([
                last_name.lower(),
                last_name.capitalize(),
                last_name.lower() + "123",
                last_name.lower() + "2024"
            ])
        
        if first_name and last_name:
            predictions.extend([
                first_name.lower() + last_name.lower(),
                first_name[0].lower() + last_name.lower(),
                first_name.lower() + last_name[0].lower(),
                first_name.lower() + last_name.lower() + "123"
            ])
        
        # Common patterns
        predictions.extend([
            "password123",
            "admin123",
            "welcome123",
            "qwerty123"
        ])
        
        self.prediction_text.insert(tk.END, "📋 HIGH PROBABILITY PASSWORDS:\n\n")
        for i, pred in enumerate(predictions[:20], 1):
            self.prediction_text.insert(tk.END, f"{i:2d}. {pred}\n")
        
        self.prediction_text.insert(tk.END, f"\n✅ Generated {len(predictions)} predictions\n")
        self.prediction_text.insert(tk.END, "💡 Use these in Password Attack Simulator\n")


if __name__ == "__main__":
    root = tk.Tk()
    AIBehaviorModule(root)
    root.mainloop()
