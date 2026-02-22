import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading

class AIBehaviorModule:
    def __init__(self, window):
        self.window = window
        self.window.title("AI Behavior Engine - PassGPT")
        self.window.geometry("1400x800")
        self.window.configure(bg="#2E2E2E")
        
        self.model = None
        self.tokenizer = None
        self.models_loaded = False
        
        # Top Header Section
        header = tk.Frame(window, bg="#1F1F1F", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Title
        tk.Label(header, text="🔐 AI Password Pattern Generator",
                font=("Consolas", 16, "bold"), bg="#1F1F1F", fg="#00FF66").pack(pady=(10, 0))
        tk.Label(header, text="Advanced Password Modeling Engine",
                font=("Consolas", 10), bg="#1F1F1F", fg="#666666").pack()
        
        # Status badge
        status_frame = tk.Frame(header, bg="#1F1F1F")
        status_frame.pack(pady=5)
        
        self.status_badge = tk.Label(status_frame, text="🟡 Loading...", 
                                     font=("Consolas", 9, "bold"),
                                     bg="#000000", fg="#FFAA00", padx=10, pady=3)
        self.status_badge.pack(side="left", padx=5)
        
        self.model_info = tk.Label(status_frame, text="Model: PassGPT-16 | CPU", 
                                   font=("Consolas", 9),
                                   bg="#000000", fg="#666666", padx=10, pady=3)
        self.model_info.pack(side="left", padx=5)
        
        tk.Frame(window, bg="#003300", height=2).pack(fill="x")
        
        # Main content
        content = tk.Frame(window, bg="#2E2E2E")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # INPUT CARD
        input_card = tk.Frame(content, bg="#1F1F1F", relief="solid", bd=2,
                             highlightbackground="#00FF66", highlightthickness=1)
        input_card.pack(fill="x", pady=(0, 20))
        
        tk.Label(input_card, text="📝 INPUT PARAMETERS", font=("Consolas", 12, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        # Input fields in grid
        fields_frame = tk.Frame(input_card, bg="#1F1F1F")
        fields_frame.pack(padx=20, pady=(0, 15))
        
        # First Name
        tk.Label(fields_frame, text="First Name:", font=("Consolas", 10, "bold"),
                bg="#1F1F1F", fg="#00FF66").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=5)
        self.first_name_entry = tk.Entry(fields_frame, font=("Consolas", 11, "bold"),
                                         bg="#000000", fg="#00FF66", relief="solid", bd=1, width=25)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Last Name
        tk.Label(fields_frame, text="Last Name:", font=("Consolas", 10, "bold"),
                bg="#1F1F1F", fg="#00FF66").grid(row=0, column=2, sticky="w", padx=(20, 10), pady=5)
        self.last_name_entry = tk.Entry(fields_frame, font=("Consolas", 11, "bold"),
                                        bg="#000000", fg="#00FF66", relief="solid", bd=1, width=25)
        self.last_name_entry.grid(row=0, column=3, padx=10, pady=5)
        
        # Date of Birth
        tk.Label(fields_frame, text="Date of Birth:", font=("Consolas", 10, "bold"),
                bg="#1F1F1F", fg="#00FF66").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)
        self.dob_entry = tk.Entry(fields_frame, font=("Consolas", 11, "bold"),
                                 bg="#000000", fg="#00FF66", relief="solid", bd=1, width=25)
        self.dob_entry.grid(row=1, column=1, padx=10, pady=5)
        self.dob_entry.insert(0, "DD/MM/YYYY")
        self.dob_entry.bind("<FocusIn>", lambda e: self.dob_entry.delete(0, tk.END) if self.dob_entry.get() == "DD/MM/YYYY" else None)
        
        # Number of predictions
        tk.Label(fields_frame, text="Predictions:", font=("Consolas", 10, "bold"),
                bg="#1F1F1F", fg="#00FF66").grid(row=1, column=2, sticky="w", padx=(20, 10), pady=5)
        self.num_predictions = ttk.Combobox(fields_frame, values=[20, 30, 50, 100], 
                                           font=("Consolas", 11, "bold"), width=23, state="readonly")
        self.num_predictions.set(50)
        self.num_predictions.grid(row=1, column=3, padx=10, pady=5)
        
        # Generate button
        generate_btn = tk.Button(fields_frame, text="🚀 GENERATE PREDICTIONS",
                               font=("Consolas", 12, "bold"), bg="#00FF66", fg="#000000",
                               activebackground="#00CC52", relief="solid", bd=2,
                               cursor="hand2", command=self.generate_predictions, height=2)
        generate_btn.grid(row=2, column=0, columnspan=4, padx=20, pady=15, sticky="ew")
        
        # OUTPUT SECTION with Tabs
        output_frame = tk.Frame(content, bg="#1F1F1F", relief="solid", bd=2)
        output_frame.pack(fill="both", expand=True)
        
        # Tab header
        tab_header = tk.Frame(output_frame, bg="#1F1F1F")
        tab_header.pack(fill="x")
        
        self.active_tab = "rule"
        
        self.tab_rule = tk.Button(tab_header, text="🔹 Rule-Based", font=("Consolas", 11, "bold"),
                                 bg="#00FF66", fg="#000000", relief="flat", bd=0,
                                 cursor="hand2", command=lambda: self.switch_tab("rule"), padx=20, pady=10)
        self.tab_rule.pack(side="left")
        
        self.tab_summary = tk.Button(tab_header, text="📊 Summary", font=("Consolas", 11, "bold"),
                                    bg="#000000", fg="#00FF66", relief="flat", bd=0,
                                    cursor="hand2", command=lambda: self.switch_tab("summary"), padx=20, pady=10)
        self.tab_summary.pack(side="left")
        
        # Tab content area
        self.tab_content = tk.Frame(output_frame, bg="#000000")
        self.tab_content.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Rule-based frame
        self.rule_frame = tk.Frame(self.tab_content, bg="#000000")
        self.rule_text = scrolledtext.ScrolledText(self.rule_frame, font=("Consolas", 10, "bold"),
                                                   bg="#000000", fg="#00FF66", relief="flat",
                                                   padx=15, pady=15, wrap=tk.WORD)
        self.rule_text.pack(fill="both", expand=True)
        
        # Summary frame
        self.summary_frame = tk.Frame(self.tab_content, bg="#000000")
        self.summary_text = tk.Text(self.summary_frame, font=("Consolas", 11, "bold"),
                                   bg="#000000", fg="#00FF66", relief="flat",
                                   padx=20, pady=20, wrap=tk.WORD)
        self.summary_text.pack(fill="both", expand=True)
        
        # Show default tab
        self.switch_tab("rule")
        
        # Load AI model
        self.load_model_async()
    
    def switch_tab(self, tab_name):
        """Switch between tabs"""
        self.active_tab = tab_name
        
        # Update button colors
        if tab_name == "rule":
            self.tab_rule.config(bg="#00FF66", fg="#000000")
            self.tab_summary.config(bg="#000000", fg="#00FF66")
            self.rule_frame.pack(fill="both", expand=True)
            self.summary_frame.pack_forget()
        else:
            self.tab_rule.config(bg="#000000", fg="#00FF66")
            self.tab_summary.config(bg="#00FF66", fg="#000000")
            self.summary_frame.pack(fill="both", expand=True)
            self.rule_frame.pack_forget()
    
    def load_model_async(self):
        """Load PassGPT model in background"""
        def load():
            try:
                self.status_badge.config(text="🟡 Loading...", fg="#FFAA00")
                
                from transformers import AutoTokenizer, AutoModelForCausalLM
                import torch
                
                model_name = "javirandor/passgpt-16characters"
                
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForCausalLM.from_pretrained(model_name)
                self.model.eval()
                
                self.models_loaded = True
                self.status_badge.config(text="🟢 Connected", fg="#00FF66")
            except Exception as e:
                self.status_badge.config(text="🔴 Offline", fg="#FF4444")
                self.model_info.config(text="Model: Not Loaded")
        
        thread = threading.Thread(target=load, daemon=True)
        thread.start()
    
    def generate_predictions(self):
        """Generate password predictions"""
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        dob = self.dob_entry.get().strip()
        
        if dob == "DD/MM/YYYY":
            dob = ""
        
        if not first_name and not last_name and not dob:
            messagebox.showerror("Error", "Enter at least one field")
            return
        
        num_samples = int(self.num_predictions.get())
        
        self.rule_text.delete(1.0, tk.END)
        self.summary_text.delete(1.0, tk.END)
        
        self.rule_text.insert(tk.END, "Generating patterns...\n\n")
        self.window.update()
        
        thread = threading.Thread(target=self._generate_thread, 
                                 args=(first_name, last_name, dob, num_samples), daemon=True)
        thread.start()
    
    def _generate_thread(self, first_name, last_name, dob, num_samples):
        """Generate predictions in background"""
        try:
            # Parse DOB
            dob_parts = []
            if dob and "/" in dob:
                parts = dob.split("/")
                if len(parts) == 3:
                    day, month, year = parts
                    dob_parts = [day, month, year, year[-2:] if len(year) == 4 else year]
            
            # Generate rule-based patterns
            patterns = []
            
            if first_name:
                fn = first_name.lower()
                patterns.extend([
                    fn, first_name.capitalize(), first_name.upper(),
                    fn + "123", fn + "1234", fn + "@123", fn + "!",
                    fn + "2024", fn + "2025", fn + "2023",
                    "2024" + fn, "2023" + fn,
                    fn + "_123", fn + ".123"
                ])
                
                # Add DOB patterns with first name
                if dob_parts:
                    patterns.extend([
                        fn + dob_parts[0], fn + dob_parts[1], fn + dob_parts[2], fn + dob_parts[3],
                        fn + dob_parts[0] + dob_parts[1], fn + dob_parts[1] + dob_parts[3],
                        fn + "@" + dob_parts[3], fn + dob_parts[3] + "!"
                    ])
            
            if last_name:
                ln = last_name.lower()
                patterns.extend([
                    ln, last_name.capitalize(), last_name.upper(),
                    ln + "123", ln + "2024", ln + "@123"
                ])
                
                # Add DOB patterns with last name
                if dob_parts:
                    patterns.extend([
                        ln + dob_parts[0], ln + dob_parts[1], ln + dob_parts[2], ln + dob_parts[3],
                        ln + dob_parts[0] + dob_parts[1]
                    ])
            
            if first_name and last_name:
                fn = first_name.lower()
                ln = last_name.lower()
                patterns.extend([
                    fn + ln, ln + fn,
                    fn + "_" + ln, fn + "." + ln, fn + "-" + ln,
                    fn[0] + ln, fn + ln[0],
                    fn + ln + "123", fn + ln + "2024",
                    fn + "123" + ln, fn + "2024" + ln
                ])
                
                # Add DOB patterns with full name
                if dob_parts:
                    patterns.extend([
                        fn + ln + dob_parts[3], fn + dob_parts[0] + ln,
                        fn[0] + ln + dob_parts[3]
                    ])
            
            # Pure DOB patterns
            if dob_parts:
                patterns.extend([
                    dob_parts[0] + dob_parts[1] + dob_parts[2],
                    dob_parts[0] + dob_parts[1] + dob_parts[3],
                    dob_parts[2], dob_parts[3],
                    dob_parts[0] + "/" + dob_parts[1] + "/" + dob_parts[2],
                    dob_parts[0] + dob_parts[1], dob_parts[1] + dob_parts[3]
                ])
            
            patterns = list(set(patterns))
            patterns = [p for p in patterns if 4 <= len(p) <= 20]
            patterns = patterns[:num_samples]
            
            # Analyze patterns
            numeric_heavy = sum(1 for p in patterns if sum(c.isdigit() for c in p) > len(p)/2)
            alpha_only = sum(1 for p in patterns if p.isalpha())
            mixed = len(patterns) - numeric_heavy - alpha_only
            
            # Display rule-based
            self.rule_text.delete(1.0, tk.END)
            self.rule_text.insert(tk.END, f"PREDICTIONS FOR: {first_name} {last_name}")
            if dob:
                self.rule_text.insert(tk.END, f" | DOB: {dob}")
            self.rule_text.insert(tk.END, "\n" + "="*60 + "\n\n")
            
            for i, pattern in enumerate(patterns, 1):
                tag = "[NUM]" if sum(c.isdigit() for c in pattern) > len(pattern)/2 else "[ALPHA]" if pattern.isalpha() else "[MIX]"
                self.rule_text.insert(tk.END, f"{i:3d}. {pattern:20s} {tag}\n")
            
            # Display summary
            self.summary_text.delete(1.0, tk.END)
            self.summary_text.insert(tk.END, "GENERATION SUMMARY\n")
            self.summary_text.insert(tk.END, "="*60 + "\n\n")
            self.summary_text.insert(tk.END, f"Target: {first_name} {last_name}\n")
            if dob:
                self.summary_text.insert(tk.END, f"DOB: {dob}\n")
            self.summary_text.insert(tk.END, f"\n📈 Total Generated: {len(patterns)}\n\n")
            self.summary_text.insert(tk.END, "PATTERN DISTRIBUTION:\n\n")
            self.summary_text.insert(tk.END, f"🔢 Numeric Heavy: {numeric_heavy} ({numeric_heavy/len(patterns)*100:.1f}%)\n")
            self.summary_text.insert(tk.END, f"🔤 Alpha Only: {alpha_only} ({alpha_only/len(patterns)*100:.1f}%)\n")
            self.summary_text.insert(tk.END, f"🔀 Mixed: {mixed} ({mixed/len(patterns)*100:.1f}%)\n\n")
            self.summary_text.insert(tk.END, f"🧠 Confidence: {'High' if len(patterns) > 30 else 'Medium'}\n\n")
            self.summary_text.insert(tk.END, "="*60 + "\n\n")
            self.summary_text.insert(tk.END, "Use these patterns in Password Attack Simulator\n")
            
        except Exception as e:
            self.rule_text.insert(tk.END, f"\nERROR: {str(e)}\n")


if __name__ == "__main__":
    root = tk.Tk()
    AIBehaviorModule(root)
    root.mainloop()
