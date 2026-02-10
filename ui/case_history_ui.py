import tkinter as tk
from tkinter import Canvas, Scrollbar
from backend.database import get_all_cases, init_database, delete_case
import os

class CaseHistoryUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Skill Palavar - Case Files")
        self.window.geometry("1200x700")
        self.window.configure(bg="#0d0d0d")
        
        # Initialize database
        init_database()
        
        # Set icon
        try:
            from PIL import Image
            if os.path.exists("ui/assessts/icon.jpg"):
                img = Image.open("ui/assessts/icon.jpg")
                img.save("assets/icon.ico", format="ICO")
            self.window.iconbitmap("assets/icon.ico")
        except:
            pass
        
        # Top Navigation Bar
        navbar = tk.Frame(window, bg="#000000", height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        
        tk.Label(navbar, text="◈ CASE FILES - FORENSIC DATABASE ◈",
                font=("Consolas", 14, "bold"), bg="#000000", fg="#00FF66").pack(pady=15)
        
        # Bottom border with glow effect
        tk.Frame(window, bg="#00FF66", height=2).pack(fill="x")
        
        # Main scrollable content
        main_frame = tk.Frame(window, bg="#0d0d0d")
        main_frame.pack(fill="both", expand=True)
        
        # Canvas with scrollbar
        canvas = Canvas(main_frame, bg="#0d0d0d", highlightthickness=0)
        scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview, bg="#0d0d0d")
        scrollable_frame = tk.Frame(canvas, bg="#0d0d0d")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Load and display cases
        self.display_cases(scrollable_frame)
    
    def display_cases(self, parent):
        """Display cases as cards in grid layout"""
        cases = get_all_cases()
        
        if not cases:
            # No cases message
            empty_frame = tk.Frame(parent, bg="#0d0d0d")
            empty_frame.pack(expand=True, fill="both", pady=150)
            
            tk.Label(empty_frame, text="⚠ NO CASES FOUND", 
                    font=("Consolas", 20, "bold"), bg="#0d0d0d", fg="#FF4444").pack(pady=10)
            tk.Label(empty_frame, text="Investigation Not Started", 
                    font=("Consolas", 12), bg="#0d0d0d", fg="#666666").pack()
            return
        
        # Create grid of cards (3 per row)
        row_frame = None
        for idx, case in enumerate(cases):
            if idx % 3 == 0:
                row_frame = tk.Frame(parent, bg="#0d0d0d")
                row_frame.pack(fill="x", pady=10)
            
            self.create_case_card(row_frame, case)
    
    def create_case_card(self, parent, case):
        """Create a single case card"""
        _, case_id, first_name, last_name, password_input, password_type, attack_type, algorithm, result, cracked_pwd, timestamp = case
        
        # Card container
        card = tk.Frame(parent, bg="#141414", relief="solid", bd=0, 
                       highlightbackground="#00FF66", highlightthickness=2)
        card.pack(side="left", padx=10, ipadx=15, ipady=15, fill="both", expand=True)
        
        # Hover effects
        def on_enter(e):
            card.config(highlightbackground="#00FF00", highlightthickness=3)
        
        def on_leave(e):
            card.config(highlightbackground="#00FF66", highlightthickness=2)
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        # TOP SECTION - Case ID & Timestamp
        top_frame = tk.Frame(card, bg="#141414")
        top_frame.pack(fill="x", pady=(0, 10))
        
        # Case ID badge
        case_id_frame = tk.Frame(top_frame, bg="#003300", relief="solid", bd=1)
        case_id_frame.pack(anchor="w")
        
        tk.Label(case_id_frame, text=f"◈ {case_id} ◈", 
                font=("Consolas", 11, "bold"), bg="#003300", fg="#00FF66",
                padx=10, pady=3).pack()
        
        # Timestamp
        tk.Label(top_frame, text=timestamp, 
                font=("Consolas", 8), bg="#141414", fg="#666666").pack(anchor="w", pady=(5, 0))
        
        # MIDDLE SECTION - Case Details
        middle_frame = tk.Frame(card, bg="#141414")
        middle_frame.pack(fill="x", pady=10)
        
        self._add_detail(middle_frame, "NAME:", f"{first_name} {last_name}")
        self._add_detail(middle_frame, "TYPE:", password_type)
        self._add_detail(middle_frame, "ATTACK:", attack_type)
        self._add_detail(middle_frame, "ALGO:", algorithm if algorithm else "N/A")
        
        # Separator line
        tk.Frame(card, bg="#00FF66", height=1).pack(fill="x", pady=10)
        
        # BOTTOM SECTION - Action Buttons Only
        bottom_frame = tk.Frame(card, bg="#141414")
        bottom_frame.pack(fill="x")
        
        # Open Case button
        open_btn = tk.Button(bottom_frame, text="OPEN FULL CASE", 
                            font=("Consolas", 9, "bold"), bg="#000000", fg="#00FF66",
                            activebackground="#003300", activeforeground="#00FF66",
                            relief="solid", bd=1, cursor="hand2",
                            command=lambda: self.open_case_details(case_id))
        open_btn.pack(fill="x", pady=(0, 5))
        
        open_btn.bind("<Enter>", lambda e: open_btn.config(bg="#003300"))
        open_btn.bind("<Leave>", lambda e: open_btn.config(bg="#000000"))
        
        # Delete button
        delete_btn = tk.Button(bottom_frame, text="DELETE CASE", 
                              font=("Consolas", 9, "bold"), bg="#000000", fg="#FF4444",
                              activebackground="#330000", activeforeground="#FF4444",
                              relief="solid", bd=1, cursor="hand2",
                              command=lambda: self.delete_case(case_id))
        delete_btn.pack(fill="x")
        
        delete_btn.bind("<Enter>", lambda e: delete_btn.config(bg="#330000"))
        delete_btn.bind("<Leave>", lambda e: delete_btn.config(bg="#000000"))
    
    def _add_detail(self, parent, label, value):
        """Add a detail row to card"""
        row = tk.Frame(parent, bg="#141414")
        row.pack(fill="x", pady=2)
        
        tk.Label(row, text=label, font=("Consolas", 9, "bold"), 
                bg="#141414", fg="#00FF66", width=8, anchor="w").pack(side="left")
        tk.Label(row, text=value, font=("Consolas", 9), 
                bg="#141414", fg="#CCCCCC", anchor="w").pack(side="left", padx=5)
    
    def open_case_details(self, case_id):
        """Open case details window"""
        from ui.case_detail_ui import CaseDetailUI
        detail_window = tk.Toplevel(self.window)
        CaseDetailUI(detail_window, case_id)
    
    def delete_case(self, case_id):
        """Delete a case after confirmation"""
        from tkinter import messagebox
        
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete case {case_id}?\n\nThis action cannot be undone."
        )
        
        if result:
            try:
                delete_case(case_id)
                messagebox.showinfo("Success", f"Case {case_id} deleted successfully")
                # Refresh the display
                for widget in self.window.winfo_children():
                    if isinstance(widget, tk.Frame):
                        widget.destroy()
                self.__init__(self.window)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete case: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    CaseHistoryUI(root)
    root.mainloop()
