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
        self.root.title("Skill Palavar - Digital Forensics Simulator")
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
        tk.Label(left_frame, text="🛡️", font=("Segoe UI Emoji", 20), bg="#1F1F1F").pack()
        
        # CENTER: Project Name
        center_frame = tk.Frame(navbar, bg="#1F1F1F")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(center_frame, text="Skill Palavar - Digital Forensics Simulator",
                font=FontLoader.get_font(12, "bold"), bg="#1F1F1F", fg="#00FF66").pack()
        
        # RIGHT: Live Date
        right_frame = tk.Frame(navbar, bg="#1F1F1F")
        right_frame.pack(side="right", padx=20, pady=15)
        live_date = datetime.now().strftime("%A, %d %B %Y")
        tk.Label(right_frame, text=live_date,
                font=FontLoader.get_font(9), bg="#1F1F1F", fg="#00FF66").pack()
        
        # Bottom border
        tk.Frame(root, bg="#003300", height=1).pack(fill="x")
        
        # Main content with padding
        content = tk.Frame(root, bg="#2E2E2E")
        content.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Container for split layout
        split_container = tk.Frame(content, bg="#1F1F1F")
        split_container.pack(fill="both", expand=True)
        
        # Left side - Background image (50%)
        left_frame = tk.Frame(split_container, bg="#1F1F1F")
        left_frame.pack(side="left", fill="both", expand=True)
        
        try:
            if os.path.exists("ui/assessts/welcome.jpg") or os.path.exists("ui/assessts/welcome.png"):
                bg_path = "ui/assessts/welcome.jpg" if os.path.exists("ui/assessts/welcome.jpg") else "ui/assessts/welcome.png"
                img = Image.open(bg_path)
                img = img.resize((500, 600), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                bg_label = tk.Label(left_frame, image=photo, bg="#1F1F1F")
                bg_label.image = photo
                bg_label.pack(fill="both", expand=True, padx=10, pady=10)
        except Exception as e:
            tk.Label(left_frame, text="SKILL PALAVAR", font=FontLoader.get_font(24, "bold"),
                    bg="#1F1F1F", fg="#00FF66").pack(expand=True)
        
        # Middle separator
        tk.Frame(split_container, bg="#003300", width=2).pack(side="left", fill="y", padx=20)
        
        # Right side - Options panel (50%)
        right_frame = tk.Frame(split_container, bg="#1F1F1F")
        right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=40)
        
        tk.Label(right_frame, text="WELCOME TO SKILL PALAVAR", 
                font=FontLoader.get_font(16, "bold"), bg="#1F1F1F", fg="#00FF66").pack(pady=40)
        
        options_frame = tk.Frame(right_frame, bg="#1F1F1F")
        options_frame.pack(expand=True, fill="both", padx=20)
        
        self._create_option(options_frame, "Create New Case", self.create_new_case)
        self._create_option(options_frame, "Open Existing Case", self.open_existing_case)
        self._create_option(options_frame, "Open Recent Case", self.open_recent_case)
    
    def _create_option(self, parent, text, command):
        btn = tk.Button(parent, text=text, font=FontLoader.get_font(11, "bold"),
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
        
        tk.Label(modal, text="CREATE NEW CASE", font=FontLoader.get_font(14, "bold"),
                bg="#2E2E2E", fg="#00FF66").pack(pady=30)
        
        # Case name input
        tk.Label(modal, text="CASE NAME:", font=FontLoader.get_font(10),
                bg="#2E2E2E", fg="#00FF66").pack(pady=(20, 5))
        
        case_entry = tk.Entry(modal, font=FontLoader.get_font(10), bg="#000000", fg="#00FF66",
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
        
        create_btn = tk.Button(btn_frame, text="CREATE", font=FontLoader.get_font(10, "bold"),
                              bg="#000000", fg="#00FF66", relief="solid", bd=2,
                              activebackground="#003300", cursor="hand2", command=create,
                              width=15, height=2)
        create_btn.pack(side="left", padx=5)
        
        cancel_btn = tk.Button(btn_frame, text="CANCEL", font=FontLoader.get_font(10, "bold"),
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
        tk.Label(left_frame, text="🛡️", font=("Segoe UI Emoji", 20), bg="#1F1F1F").pack()
        
        # CENTER: Project Name
        center_frame = tk.Frame(navbar, bg="#1F1F1F")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(center_frame, text="Skill Palavar - Digital Forensics Simulator",
                font=FontLoader.get_font(12, "bold"), bg="#1F1F1F", fg="#00FF66").pack()
        
        # RIGHT: Case Name and Live Date
        right_frame = tk.Frame(navbar, bg="#1F1F1F")
        right_frame.pack(side="right", padx=20, pady=15)
        tk.Label(right_frame, text=f"Case: {case_name}", font=FontLoader.get_font(9),
                bg="#1F1F1F", fg="#00FF66").pack()
        live_date = datetime.now().strftime("%A, %d %B %Y")
        tk.Label(right_frame, text=live_date, font=FontLoader.get_font(8),
                bg="#1F1F1F", fg="#00FF66").pack()
        
        # Bottom border
        tk.Frame(root, bg="#003300", height=1).pack(fill="x")
        
        # Main content
        content = tk.Frame(root, bg="#2E2E2E")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(content, text="SELECT MODULE", font=FontLoader.get_font(14, "bold"),
                bg="#2E2E2E", fg="#00FF66").pack(pady=15)
        
        # Module grid
        grid = tk.Frame(content, bg="#2E2E2E")
        grid.pack(fill="both", expand=True)
        
        modules = [
            ("Password Attack Simulation", self.open_password_module),
            ("Case Files", self.open_case_history),
            ("AI Learning & Behaviour Analysis", None),
            ("Awareness Training & Feedback", None)
        ]
        
        for i, (name, cmd) in enumerate(modules):
            row, col = i // 2, i % 2
            self._create_module_card(grid, name, cmd, row, col, i in [0, 1])
    
    def _create_module_card(self, parent, title, command, row, col, enabled):
        card = tk.Frame(parent, bg="#1F1F1F" if enabled else "#3E3E3E",
                       relief="solid", bd=2, cursor="hand2" if enabled else "arrow")
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        tk.Label(card, text=title, font=FontLoader.get_font(11, "bold"),
                bg=card["bg"], fg="#00FF66" if enabled else "#666666").pack(pady=40)
        
        status = "ACTIVE" if enabled else "COMING SOON"
        tk.Label(card, text=status, font=FontLoader.get_font(9),
                bg=card["bg"], fg="#00FF66" if enabled else "#666666").pack(pady=(0, 30))
        
        if enabled and command:
            def on_enter(e):
                card.config(bg="#003300")
            def on_leave(e):
                card.config(bg="#1F1F1F")
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
            card.bind("<Button-1>", lambda e: command())
    
    def open_password_module(self):
        from ui.module1_ui import PasswordAttackModule
        module_window = tk.Toplevel(self.root)
        module_window.configure(bg="#2E2E2E")
        PasswordAttackModule(module_window)
    
    def open_case_history(self):
        from ui.case_history_ui import CaseHistoryUI
        history_window = tk.Toplevel(self.root)
        history_window.configure(bg="#2E2E2E")
        CaseHistoryUI(history_window)


class SplashScreen:
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete
        self.root.title("Skill Palavar - Digital Forensics Simulator")
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
        
        # Load and display welcome image
        try:
            if os.path.exists("ui/assessts/welcome.jpg") or os.path.exists("ui/assessts/welcome.png"):
                bg_path = "ui/assessts/welcome.jpg" if os.path.exists("ui/assessts/welcome.jpg") else "ui/assessts/welcome.png"
                img = Image.open(bg_path)
                img = img.resize((1200, 700), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                bg_label = tk.Label(container, image=photo, bg="#1F1F1F")
                bg_label.image = photo
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            pass
        
        # Loading indicator and text overlay
        overlay = tk.Frame(container, bg="#1F1F1F")
        overlay.place(relx=0.5, rely=0.85, anchor="center")
        
        # Loading text
        loading_label = tk.Label(overlay, text="Initializing Secure Simulation Environment...",
                                font=FontLoader.get_font(11), bg="#1F1F1F", fg="#00FF66")
        loading_label.pack(pady=10)
        
        # Loading animation dots
        self.dots_label = tk.Label(overlay, text="", font=FontLoader.get_font(14, "bold"),
                                   bg="#1F1F1F", fg="#00FF66")
        self.dots_label.pack()
        
        self.dot_count = 0
        self.animate_loading()
        
        # Transition after 3.5 seconds
        root.after(3500, self.transition_to_welcome)
    
    def animate_loading(self):
        dots = "." * (self.dot_count % 4)
        self.dots_label.config(text=dots)
        self.dot_count += 1
        if self.dot_count < 15:
            self.root.after(250, self.animate_loading)
    
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
