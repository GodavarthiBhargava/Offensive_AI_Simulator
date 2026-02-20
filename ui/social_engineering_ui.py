import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import threading

class VoiceAnalysisModule:
    def __init__(self, window):
        self.window = window
        self.window.title("Voice / Social Engineering Analyzer")
        self.window.geometry("1400x800")
        self.window.configure(bg="#2E2E2E")
        
        self.model = None
        self.classifier = None
        self.models_loaded = False
        
        # Top bar
        navbar = tk.Frame(window, bg="#1F1F1F", height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        
        tk.Label(navbar, text="🎤 VOICE / SOCIAL ENGINEERING ANALYZER",
                font=("Consolas", 14, "bold"), bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        tk.Frame(window, bg="#003300", height=1).pack(fill="x")
        
        # Main content
        content = tk.Frame(window, bg="#2E2E2E")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel - Upload
        left_panel = tk.Frame(content, bg="#1F1F1F", relief="solid", bd=2)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        tk.Label(left_panel, text="🎙️ VOICE RECORDING ANALYSIS", font=("Consolas", 14, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        # Upload section
        upload_frame = tk.Frame(left_panel, bg="#1F1F1F")
        upload_frame.pack(fill="x", padx=20, pady=20)
        
        tk.Label(upload_frame, text="Select Language:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(anchor="w", pady=(0, 10))
        
        self.language_var = tk.StringVar(value="Telugu")
        lang_frame = tk.Frame(upload_frame, bg="#1F1F1F")
        lang_frame.pack(fill="x", pady=(0, 15))
        
        for lang in ["Telugu", "Hindi", "English"]:
            rb = tk.Radiobutton(lang_frame, text=lang, variable=self.language_var, value=lang,
                               font=("Consolas", 10, "bold"), bg="#1F1F1F", fg="#00FF66",
                               selectcolor="#000000", activebackground="#1F1F1F",
                               activeforeground="#00FF66")
            rb.pack(side="left", padx=10)
        
        tk.Label(upload_frame, text="Upload Audio File:", font=("Consolas", 11, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(anchor="w", pady=(10, 10))
        
        self.file_label = tk.Label(upload_frame, text="No file selected", font=("Consolas", 10, "bold"),
                                   bg="#000000", fg="#666666", anchor="w", padx=10, pady=10)
        self.file_label.pack(fill="x", pady=(0, 10))
        
        upload_btn = tk.Button(upload_frame, text="📁 BROWSE FILE",
                              font=("Consolas", 12, "bold"), bg="#000000", fg="#00FF66",
                              activebackground="#003300", relief="solid", bd=2,
                              cursor="hand2", command=self.browse_file)
        upload_btn.pack(fill="x", ipady=10)
        
        # Supported formats
        formats_frame = tk.Frame(left_panel, bg="#000000", relief="solid", bd=1)
        formats_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(formats_frame, text="Supported Formats:", font=("Consolas", 9, "bold"),
                bg="#000000", fg="#00FF66").pack(anchor="w", padx=10, pady=(10, 5))
        tk.Label(formats_frame, text="• MP3, WAV, M4A, FLAC, OGG", font=("Consolas", 9, "bold"),
                bg="#000000", fg="#FFFFFF").pack(anchor="w", padx=10)
        tk.Label(formats_frame, text="• Supports 90+ languages", font=("Consolas", 9, "bold"),
                bg="#000000", fg="#FFFFFF").pack(anchor="w", padx=10, pady=(0, 10))
        
        # Analyze button
        analyze_btn = tk.Button(left_panel, text="🔍 ANALYZE VOICE",
                               font=("Consolas", 13, "bold"), bg="#00FF66", fg="#000000",
                               activebackground="#00CC52", relief="solid", bd=2,
                               cursor="hand2", command=self.analyze_voice)
        analyze_btn.pack(fill="x", padx=20, pady=20, ipady=15)
        
        # Status
        self.status_label = tk.Label(left_panel, text="⏳ Ready to analyze", font=("Consolas", 10, "bold"),
                                     bg="#1F1F1F", fg="#FFAA00")
        self.status_label.pack(pady=10)
        
        # Right panel - Results
        right_panel = tk.Frame(content, bg="#1F1F1F", relief="solid", bd=2)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        tk.Label(right_panel, text="📊 ANALYSIS RESULTS", font=("Consolas", 14, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack(pady=15)
        
        self.results_text = scrolledtext.ScrolledText(right_panel, font=("Consolas", 10, "bold"),
                                                     bg="#000000", fg="#00FF66",
                                                     relief="flat", padx=15, pady=15, wrap=tk.WORD)
        self.results_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.file_path = None
        
        # Load models in background
        self.load_models_async()
    
    def load_models_async(self):
        """Load AI models in background"""
        def load():
            try:
                self.status_label.config(text="⏳ Loading AI models...", fg="#FFAA00")
                
                from faster_whisper import WhisperModel
                from transformers import pipeline
                
                self.model = WhisperModel("medium", device="cpu", compute_type="int8")
                self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
                
                self.models_loaded = True
                self.status_label.config(text="✅ Models loaded - Ready", fg="#00FF66")
            except Exception as e:
                self.status_label.config(text=f"❌ Error loading models", fg="#FF4444")
                messagebox.showerror("Error", f"Failed to load AI models:\n{str(e)}\n\nInstall: pip install faster-whisper transformers torch")
        
        thread = threading.Thread(target=load, daemon=True)
        thread.start()
    
    def browse_file(self):
        """Browse and select audio file"""
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.m4a *.flac *.ogg *.mpeg *.mp4"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self.file_path = file_path
            filename = os.path.basename(file_path)
            self.file_label.config(text=f"✅ {filename}", fg="#00FF66")
    
    def analyze_voice(self):
        """Analyze voice recording"""
        if not self.file_path:
            messagebox.showerror("Error", "Please select an audio file first")
            return
        
        if not self.models_loaded:
            messagebox.showerror("Error", "AI models are still loading. Please wait...")
            return
        
        self.status_label.config(text="⏳ Analyzing...", fg="#FFAA00")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Processing audio file...\n\n")
        
        # Run analysis in thread
        thread = threading.Thread(target=self.run_analysis, daemon=True)
        thread.start()
    
    def run_analysis(self):
        """Run speech-to-text and risk analysis"""
        try:
            # Speech to text
            self.update_results("🎤 TRANSCRIBING AUDIO...\n\n")
            
            # Get language code
            lang_map = {"Telugu": "te", "Hindi": "hi", "English": "en"}
            selected_lang = lang_map[self.language_var.get()]
            
            segments, info = self.model.transcribe(
                self.file_path,
                task="transcribe",
                language=selected_lang,
                beam_size=5,
                vad_filter=True,
                word_timestamps=False
            )
            
            full_text = ""
            for segment in segments:
                full_text += segment.text + " "
            
            full_text = full_text.strip()
            detected_language = info.language
            
            if not full_text:
                self.update_results("❌ No speech detected in audio file")
                self.status_label.config(text="❌ Analysis failed", fg="#FF4444")
                return
            
            # Display transcription
            self.update_results(f"🌍 DETECTED LANGUAGE: {detected_language.upper()}\n\n")
            self.update_results("📝 TRANSCRIPTION:\n")
            self.update_results("─" * 70 + "\n")
            self.update_results(f"{full_text}\n")
            self.update_results("─" * 70 + "\n\n")
            
            # Risk analysis
            self.update_results("🔍 ANALYZING RISK...\n\n")
            
            labels = [
                "phishing attempt",
                "social engineering",
                "financial fraud",
                "scam call",
                "identity theft",
                "normal conversation"
            ]
            
            result = self.classifier(full_text, labels, multi_label=False)
            
            # Calculate risk score
            risk_keywords = ["phishing", "social engineering", "fraud", "scam", "theft"]
            risk_score = 0
            
            for label, score in zip(result["labels"], result["scores"]):
                if any(keyword in label.lower() for keyword in risk_keywords):
                    risk_score += score * 100
            
            risk_score = min(100, int(risk_score))
            
            if risk_score >= 70:
                risk_level = "HIGH RISK"
                risk_color = "🔴"
            elif risk_score >= 40:
                risk_level = "MEDIUM RISK"
                risk_color = "🟡"
            else:
                risk_level = "LOW RISK"
                risk_color = "🟢"
            
            # Display risk score
            self.update_results(f"⚠️ RISK ASSESSMENT:\n\n")
            self.update_results(f"{risk_color} Risk Level: {risk_level}\n")
            self.update_results(f"📊 Risk Score: {risk_score}/100\n\n")
            
            # Top classifications
            self.update_results("🎯 CLASSIFICATION RESULTS:\n\n")
            for i, (label, score) in enumerate(zip(result["labels"][:3], result["scores"][:3]), 1):
                percentage = int(score * 100)
                self.update_results(f"{i}. {label.upper()}: {percentage}%\n")
            
            # Identify trap keywords
            self.update_results("\n🚨 IDENTIFIED TRAP KEYWORDS:\n\n")
            
            trap_keywords = {
                "urgent": "Creates false urgency",
                "verify": "Verification scam",
                "account": "Account compromise attempt",
                "suspended": "Fear tactic",
                "confirm": "Information phishing",
                "password": "Credential theft",
                "bank": "Financial fraud",
                "credit card": "Payment scam",
                "prize": "Prize scam",
                "winner": "Lottery scam",
                "tax": "Tax fraud",
                "refund": "Refund scam",
                "click": "Phishing link",
                "download": "Malware distribution",
                "social security": "Identity theft"
            }
            
            found_keywords = []
            text_lower = full_text.lower()
            
            for keyword, description in trap_keywords.items():
                if keyword in text_lower:
                    found_keywords.append((keyword, description))
            
            if found_keywords:
                for keyword, description in found_keywords:
                    self.update_results(f"• '{keyword.upper()}' - {description}\n")
            else:
                self.update_results("✅ No common trap keywords detected\n")
            
            # Recommendations
            self.update_results("\n💡 RECOMMENDATIONS:\n\n")
            
            if risk_score >= 70:
                self.update_results("❌ DO NOT RESPOND to this call\n")
                self.update_results("❌ DO NOT share any personal information\n")
                self.update_results("✅ Report this as a scam attempt\n")
                self.update_results("✅ Block the caller immediately\n")
            elif risk_score >= 40:
                self.update_results("⚠️ Exercise extreme caution\n")
                self.update_results("⚠️ Verify caller identity independently\n")
                self.update_results("⚠️ Do not share sensitive information\n")
            else:
                self.update_results("✅ Call appears legitimate\n")
                self.update_results("✅ Standard precautions apply\n")
            
            self.status_label.config(text="✅ Analysis complete", fg="#00FF66")
            
        except Exception as e:
            self.update_results(f"\n❌ ERROR: {str(e)}\n")
            self.status_label.config(text="❌ Analysis failed", fg="#FF4444")
    
    def update_results(self, text):
        """Update results text widget"""
        self.results_text.insert(tk.END, text)
        self.results_text.see(tk.END)
        self.window.update()


if __name__ == "__main__":
    root = tk.Tk()
    VoiceAnalysisModule(root)
    root.mainloop()
