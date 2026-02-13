import tkinter as tk
from tkinter import filedialog, messagebox
import os
from datetime import datetime
from PIL import Image, ImageTk
from ui.font_loader import FontLoader

class WelcomeScreen:
    def __init__(self, root, on_case_ready):
        self.root = root
        self.on_case_ready = on_case_ready
        self.root.title("SECURENETRA - Digital Forensics Simulator")
        self.root.geometry("1200x700")
        self.root.configure(bg="#2E2E2E")
        
        # Set icon
        try:
            if os.path.exists("ui/assessts/icon.jpg"):
                img = Image.open("ui/assessts/icon.jpg")
                img.save("assets/icon.ico", format="ICO")
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass
        
        # Top Navigation Bar with 3-column layout
        navbar = tk.Frame(root, bg="#1F1F1F", height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        
        # LEFT: Logo/Emoji
        left_frame = tk.Frame(navbar, bg="#1F1F1F")
        left_frame.pack(side="left", padx=20, pady=15)
        tk.Label(left_frame, text="🛡️", font=("Segoe UI Emoji", 24, "bold"), bg="#1F1F1F").pack()
        
        # CENTER: Project Name
        center_frame = tk.Frame(navbar, bg="#1F1F1F")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(center_frame, text="SECURENETRA - Digital Forensics Simulator",
                font=("Courier New", 14, "bold"), bg="#1F1F1F", fg="#00FF66").pack()
        
        # RIGHT: Live Date
        right_frame = tk.Frame(navbar, bg="#1F1F1F")
        right_frame.pack(side="right", padx=20, pady=15)
        live_date = datetime.now().strftime("%A, %d %B %Y")
        tk.Label(right_frame, text=live_date,
                font=("Courier New", 11, "bold"), bg="#1F1F1F", fg="#00FF66").pack()
        
        # Load welcome image as full background
        try:
            if os.path.exists("ui/assessts/welcome.jpg") or os.path.exists("ui/assessts/welcome.png"):
                bg_path = "ui/assessts/welcome.jpg" if os.path.exists("ui/assessts/welcome.jpg") else "ui/assessts/welcome.png"
                img = Image.open(bg_path)
                img = img.resize((1200, 650), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                bg_label = tk.Label(root, image=photo)
                bg_label.image = photo
                bg_label.place(x=0, y=51, width=1200, height=649)
        except Exception as e:
            pass
        
        # Bottom border
        tk.Frame(root, bg="#003300", height=1).pack(fill="x")
        
        # Right side - Options panel overlay (centered)
        right_frame = tk.Frame(root, bg="#1F1F1F")
        right_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=450)
        
        tk.Label(right_frame, text="WELCOME TO SECURENETRA", 
                font=("Courier New", 20, "bold"), bg="#1F1F1F", fg="#00FF66").pack(pady=40)
        
        options_frame = tk.Frame(right_frame, bg="#1F1F1F")
        options_frame.pack(expand=True, fill="both", padx=20)
        
        self._create_option(options_frame, "Create New Case", self.create_new_case)
        self._create_option(options_frame, "Open Existing Case", self.open_existing_case)
        self._create_option(options_frame, "Open Recent Case", self.open_recent_case)
    
    def _create_option(self, parent, text, command):
        btn = tk.Button(parent, text=text, font=("Courier New", 13, "bold"),
                       bg="#000000", fg="#00FF66", relief="solid", bd=2,
                       activebackground="#003300", activeforeground="#00FF66",
                       cursor="hand2", command=command, height=2)
        btn.pack(fill="x", pady=10)
        
        btn.bind("<Enter>", lambda e: btn.config(bg="#003300"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))
    
    def create_new_case(self):
        # Open modal window
        modal = tk.Toplevel(self.root)
        modal.title("Create New Case")
        modal.geometry("500x300")
        modal.configure(bg="#2E2E2E")
        modal.transient(self.root)
        modal.grab_set()
        
        # Center modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (500 // 2)
        y = (modal.winfo_screenheight() // 2) - (300 // 2)
        modal.geometry(f"500x300+{x}+{y}")
        
        tk.Label(modal, text="CREATE NEW CASE", font=("Courier New", 16, "bold"),
                bg="#2E2E2E", fg="#00FF66").pack(pady=30)
        
        # Case name input
        tk.Label(modal, text="CASE NAME:", font=("Courier New", 12, "bold"),
                bg="#2E2E2E", fg="#00FF66").pack(pady=(20, 5))
        
        case_entry = tk.Entry(modal, font=("Courier New", 12, "bold"), bg="#000000", fg="#00FF66",
                             relief="solid", bd=1, insertbackground="#00FF66")
        case_entry.pack(padx=50, fill="x", ipady=8)
        case_entry.insert(0, f"Case_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        def create():
            case_name = case_entry.get().strip()
            if not case_name:
                messagebox.showerror("Error", "Please enter case name")
                return
            
            case_path = os.path.join("cases", case_name)
            os.makedirs(case_path, exist_ok=True)
            
            with open(os.path.join(case_path, "case_info.txt"), "w") as f:
                f.write(f"Case Name: {case_name}\nCreated: {datetime.now()}\n")
            
            modal.destroy()
            self.on_case_ready(case_name)
        
        btn_frame = tk.Frame(modal, bg="#2E2E2E")
        btn_frame.pack(pady=30)
        
        create_btn = tk.Button(btn_frame, text="CREATE", font=("Courier New", 12, "bold"),
                              bg="#000000", fg="#00FF66", relief="solid", bd=2,
                              activebackground="#003300", cursor="hand2", command=create,
                              width=15, height=2)
        create_btn.pack(side="left", padx=5)
        
        cancel_btn = tk.Button(btn_frame, text="CANCEL", font=("Courier New", 12, "bold"),
                              bg="#000000", fg="#00FF66", relief="solid", bd=2,
                              activebackground="#003300", cursor="hand2", command=modal.destroy,
                              width=15, height=2)
        cancel_btn.pack(side="left", padx=5)
    
    def open_existing_case(self):
        case_path = filedialog.askdirectory(initialdir="cases", title="Select Case Folder")
        if case_path:
            case_name = os.path.basename(case_path)
            self.on_case_ready(case_name)
    
    def open_recent_case(self):
        if not os.path.exists("cases") or not os.listdir("cases"):
            messagebox.showinfo("No Recent Cases", "No recent cases found.")
            return
        
        cases = sorted([d for d in os.listdir("cases") if os.path.isdir(os.path.join("cases", d))], reverse=True)
        if cases:
            self.on_case_ready(cases[0])


class Dashboard:
    def __init__(self, root, case_name):
        self.root = root
        self.case_name = case_name
        
        # Clear window
        for widget in root.winfo_children():
            widget.destroy()
        
        root.configure(bg="#2E2E2E")
        
        # Top Navigation Bar with 3-column layout
        navbar = tk.Frame(root, bg="#1F1F1F", height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        
        # LEFT: Logo/Emoji
        left_frame = tk.Frame(navbar, bg="#1F1F1F")
        left_frame.pack(side="left", padx=20, pady=15)
        tk.Label(left_frame, text="🛡️", font=("Segoe UI Emoji", 24, "bold"), bg="#1F1F1F").pack()
        
        # CENTER: Project Name
        center_frame = tk.Frame(navbar, bg="#1F1F1F")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(center_frame, text="SECURENETRA - Digital Forensics Simulator",
                font=("Courier New", 14, "bold"), bg="#1F1F1F", fg="#00FF66").pack()
        
        # RIGHT: Case Name, History Button and Live Date
        right_frame = tk.Frame(navbar, bg="#1F1F1F")
        right_frame.pack(side="right", padx=20, pady=15)
        
        # History button
        history_btn = tk.Button(right_frame, text="📁 HISTORY", font=("Courier New", 10, "bold"),
                               bg="#000000", fg="#00FF66", relief="solid", bd=1,
                               activebackground="#003300", cursor="hand2",
                               command=self.open_case_history, padx=10, pady=5)
        history_btn.pack(side="top", pady=(0, 5))
        history_btn.bind("<Enter>", lambda e: history_btn.config(bg="#003300"))
        history_btn.bind("<Leave>", lambda e: history_btn.config(bg="#000000"))
        
        tk.Label(right_frame, text=f"Case: {case_name}", font=("Courier New", 9, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack()
        live_date = datetime.now().strftime("%A, %d %B %Y")
        tk.Label(right_frame, text=live_date, font=("Courier New", 8, "bold"),
                bg="#1F1F1F", fg="#00FF66").pack()
        
        # Bottom border
        tk.Frame(root, bg="#003300", height=1).pack(fill="x")
        
        # Main layout: Sidebar + Content
        main_container = tk.Frame(root, bg="#2E2E2E")
        main_container.pack(fill="both", expand=True)
        
        # LEFT SIDEBAR
        sidebar = tk.Frame(main_container, bg="#1F1F1F", width=280)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        tk.Label(sidebar, text="MODULES", font=("Courier New", 16, "bold"),
                bg="#1F1F1F", fg="#00FF66", pady=20).pack()
        
        tk.Frame(sidebar, bg="#003300", height=2).pack(fill="x", padx=10)
        
        modules = [
            ("Password Attack Simulator", self.open_password_module),
            ("AI Behavior Engine", self.open_ai_behavior),
            ("Phishing Campaign Simulator", self.open_phishing_campaign),
            ("Voice / Social Engineering", self.open_social_engineering),
            ("Email & Message Analyzer", self.open_email_analyzer),
            ("Domain Verification", self.open_domain_verification),
            ("Risk & Analytics Dashboard", self.open_analytics),
            ("Awareness Training", self.open_awareness_training)
        ]
        
        for name, cmd in modules:
            self._create_sidebar_item(sidebar, name, cmd, True)
        
        # RIGHT: Content Area
        content = tk.Frame(main_container, bg="#2E2E2E")
        content.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(content, text="Welcome to Case Analysis", font=("Courier New", 18, "bold"),
                bg="#2E2E2E", fg="#00FF66").pack(pady=50)
        tk.Label(content, text="Select a module from the sidebar to begin", font=("Courier New", 12, "bold"),
                bg="#2E2E2E", fg="#666666").pack()
    
    def _create_sidebar_item(self, parent, text, command, enabled):
        btn = tk.Button(parent, text=text, font=("Courier New", 11, "bold"),
                       bg="#000000" if enabled else "#2E2E2E",
                       fg="#00FF66" if enabled else "#666666",
                       activebackground="#003300" if enabled else "#2E2E2E",
                       relief="flat", bd=0, anchor="w", padx=20, pady=15,
                       cursor="hand2" if enabled else "arrow",
                       command=command if enabled else None)
        btn.pack(fill="x", padx=10, pady=5)
        
        if enabled:
            btn.bind("<Enter>", lambda e: btn.config(bg="#003300"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))
    
    def open_password_module(self):
        from ui.module1_ui import PasswordAttackModule
        module_window = tk.Toplevel(self.root)
        module_window.configure(bg="#2E2E2E")
        PasswordAttackModule(module_window)
    
    def open_ai_behavior(self):
        from ui.ai_behavior_ui import AIBehaviorModule
        module_window = tk.Toplevel(self.root)
        module_window.configure(bg="#2E2E2E")
        AIBehaviorModule(module_window)
    
    def open_phishing_campaign(self):
        from ui.phishing_campaign_ui import PhishingCampaignModule
        module_window = tk.Toplevel(self.root)
        module_window.configure(bg="#2E2E2E")
        PhishingCampaignModule(module_window)
    
    def open_social_engineering(self):
        from ui.social_engineering_ui import SocialEngineeringModule
        module_window = tk.Toplevel(self.root)
        module_window.configure(bg="#2E2E2E")
        SocialEngineeringModule(module_window)
    
    def open_email_analyzer(self):
        from ui.email_analyzer_ui import EmailAnalyzerModule
        module_window = tk.Toplevel(self.root)
        module_window.configure(bg="#2E2E2E")
        EmailAnalyzerModule(module_window)
    
    def open_domain_verification(self):
        from ui.domain_verification_ui import DomainVerificationModule
        module_window = tk.Toplevel(self.root)
        module_window.configure(bg="#2E2E2E")
        DomainVerificationModule(module_window)
    
    def open_analytics(self):
        from ui.analytics_ui import AnalyticsDashboard
        module_window = tk.Toplevel(self.root)
        module_window.configure(bg="#2E2E2E")
        AnalyticsDashboard(module_window)
    
    def open_awareness_training(self):
        from ui.awareness_training_ui import AwarenessTrainingModule
        module_window = tk.Toplevel(self.root)
        module_window.configure(bg="#2E2E2E")
        AwarenessTrainingModule(module_window)
    
    def open_case_history(self):
        from ui.case_history_ui import CaseHistoryUI
        history_window = tk.Toplevel(self.root)
        history_window.configure(bg="#2E2E2E")
        CaseHistoryUI(history_window)


class SplashScreen:
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete
        self.root.title("SECURENETRA - Digital Forensics Simulator")
        self.root.geometry("1200x700")
        self.root.configure(bg="#2E2E2E")
        
        # Set icon
        try:
            if os.path.exists("ui/assessts/icon.jpg"):
                img = Image.open("ui/assessts/icon.jpg")
                img.save("assets/icon.ico", format="ICO")
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass
        
        # Full screen container
        container = tk.Frame(root, bg="#1F1F1F")
        container.pack(fill="both", expand=True)
        
        # Load and display loading image
        try:
            if os.path.exists("ui/assessts/loadingpage.jpg") or os.path.exists("ui/assessts/loading.jpg") or os.path.exists("ui/assessts/loading.png"):
                if os.path.exists("ui/assessts/loadingpage.jpg"):
                    bg_path = "ui/assessts/loadingpage.jpg"
                elif os.path.exists("ui/assessts/loading.jpg"):
                    bg_path = "ui/assessts/loading.jpg"
                else:
                    bg_path = "ui/assessts/loading.png"
                img = Image.open(bg_path)
                img = img.resize((1200, 700), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                bg_label = tk.Label(container, image=photo, bg="#1F1F1F")
                bg_label.image = photo
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading image: {e}")
        
        # Loading indicator and text overlay (transparent, directly on image)
        # Loading text
        loading_label = tk.Label(container, text="Initializing Secure Simulation Environment...",
                                font=("Courier New", 13, "bold"), bg="#1F1F1F", fg="#00FF66")
        loading_label.place(relx=0.5, rely=0.82, anchor="center")
        
        # Progress bar (cylinder filling effect)
        self.progress_canvas = tk.Canvas(container, width=300, height=30, bg="#1F1F1F", highlightthickness=0)
        self.progress_canvas.place(relx=0.5, rely=0.88, anchor="center")
        
        # Draw progress bar border
        self.progress_canvas.create_rectangle(2, 2, 298, 28, outline="#00FF66", width=2)
        
        # Progress fill
        self.progress_fill = self.progress_canvas.create_rectangle(4, 4, 4, 26, fill="#00FF66", outline="")
        
        self.progress = 0
        self.animate_progress()
        
        # Transition after 3.5 seconds
        root.after(3500, self.transition_to_welcome)
    
    def animate_progress(self):
        if self.progress < 294:
            self.progress += 8
            self.progress_canvas.coords(self.progress_fill, 4, 4, self.progress, 26)
            self.root.after(100, self.animate_progress)
    
    def transition_to_welcome(self):
        # Fade out effect
        self.fade_out()
    
    def fade_out(self, alpha=1.0):
        if alpha > 0:
            self.root.attributes("-alpha", alpha)
            self.root.after(50, lambda: self.fade_out(alpha - 0.1))
        else:
            self.on_complete()


def main():
    root = tk.Tk()
    
    def on_case_ready(case_name):
        Dashboard(root, case_name)
    
    def show_welcome():
        # Clear splash screen
        for widget in root.winfo_children():
            widget.destroy()
        root.attributes("-alpha", 1.0)
        WelcomeScreen(root, on_case_ready)
    
    SplashScreen(root, show_welcome)
    root.mainloop()


if __name__ == "__main__":
    main()
