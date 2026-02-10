import tkinter as tk
from tkinter import scrolledtext
from backend.database import get_case_by_id, get_case_history
import os

class CaseDetailUI:
    def __init__(self, window, case_id):
        self.window = window
        self.case_id = case_id
        self.window.title(f"Case Details - {case_id}")
        self.window.geometry("900x700")
        self.window.configure(bg="#2E2E2E")
        
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
        navbar = tk.Frame(window, bg="#1F1F1F", height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        
        tk.Label(navbar, text=f"Case File: {case_id}",
                font=("Consolas", 12, "bold"), bg="#1F1F1F", fg="#00FF66").pack(side="left", padx=20, pady=15)
        
        # Bottom border
        tk.Frame(window, bg="#003300", height=1).pack(fill="x")
        
        # Main content with scrollbar
        main_frame = tk.Frame(window, bg="#2E2E2E")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Get case data
        case = get_case_by_id(case_id)
        
        if not case:
            tk.Label(main_frame, text="Case not found", font=("Consolas", 14),
                    bg="#2E2E2E", fg="#FF0000").pack(pady=50)
            return
        
        # Parse case data
        _, case_id, first_name, last_name, password_input, password_type, attack_type, algorithm, result, cracked_pwd, timestamp = case
        
        # Case Information Section
        info_frame = self._create_section(main_frame, "CASE INFORMATION")
        
        info_grid = tk.Frame(info_frame, bg="#1F1F1F")
        info_grid.pack(fill="x", padx=20, pady=15)
        
        self._add_field(info_grid, "Case ID:", case_id, 0)
        self._add_field(info_grid, "First Name:", first_name, 1)
        self._add_field(info_grid, "Last Name:", last_name, 2)
        self._add_field(info_grid, "Password Type:", password_type, 3)
        self._add_field(info_grid, "Entered Password/Hash:", password_input[:50] + "..." if len(password_input) > 50 else password_input, 4)
        self._add_field(info_grid, "Selected Algorithm:", algorithm if algorithm else "N/A", 5)
        self._add_field(info_grid, "Attack Type:", attack_type, 6)
        self._add_field(info_grid, "Date & Time:", timestamp, 7)
        
        # Result Section
        result_frame = self._create_section(main_frame, "RESULT")
        
        result_grid = tk.Frame(result_frame, bg="#1F1F1F")
        result_grid.pack(fill="x", padx=20, pady=15)
        
        # Status
        status_color = "#00FF66" if "Cracked" in result or "SUCCESS" in result else "#FF4444"
        status_text = "CRACKED" if "Cracked" in result or "SUCCESS" in result else "NOT CRACKED"
        
        tk.Label(result_grid, text="Status:", font=("Consolas", 10, "bold"),
                bg="#1F1F1F", fg="#00FF66").grid(row=0, column=0, sticky="w", pady=8, padx=10)
        tk.Label(result_grid, text=status_text, font=("Consolas", 12, "bold"),
                bg="#1F1F1F", fg=status_color).grid(row=0, column=1, sticky="w", pady=8, padx=10)
        
        # Result details
        tk.Label(result_grid, text="Details:", font=("Consolas", 10, "bold"),
                bg="#1F1F1F", fg="#00FF66").grid(row=1, column=0, sticky="nw", pady=8, padx=10)
        
        result_text = tk.Text(result_grid, font=("Consolas", 9), bg="#000000", fg="#00FF66",
                             height=3, width=70, relief="solid", bd=1, wrap=tk.WORD)
        result_text.insert("1.0", result)
        result_text.config(state="disabled")
        result_text.grid(row=1, column=1, sticky="w", pady=8, padx=10)
        
        if cracked_pwd:
            tk.Label(result_grid, text="Cracked Password:", font=("Consolas", 10, "bold"),
                    bg="#1F1F1F", fg="#00FF66").grid(row=2, column=0, sticky="w", pady=8, padx=10)
            tk.Label(result_grid, text=cracked_pwd, font=("Consolas", 11, "bold"),
                    bg="#1F1F1F", fg="#00FF66").grid(row=2, column=1, sticky="w", pady=8, padx=10)
        
        # History Timeline Section
        history_frame = self._create_section(main_frame, "ATTACK HISTORY TIMELINE")
        
        timeline_container = tk.Frame(history_frame, bg="#1F1F1F")
        timeline_container.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Get all attempts for this person
        history = get_case_history(first_name, last_name)
        
        if len(history) > 1:
            tk.Label(timeline_container, text=f"Total Attempts: {len(history)}", 
                    font=("Consolas", 10, "bold"), bg="#1F1F1F", fg="#00FF66").pack(anchor="w", pady=(0, 10))
            
            # Timeline text area
            timeline_text = scrolledtext.ScrolledText(timeline_container, font=("Consolas", 9),
                                                     bg="#000000", fg="#00FF66", height=10,
                                                     relief="solid", bd=1, wrap=tk.WORD)
            timeline_text.pack(fill="both", expand=True)
            
            for idx, h in enumerate(history, 1):
                h_case_id, h_timestamp, h_attack, h_algo, h_result = h[1], h[10], h[6], h[7], h[8]
                status_icon = "✓" if "Cracked" in h_result or "SUCCESS" in h_result else "✗"
                
                timeline_text.insert(tk.END, f"[{h_timestamp}] {status_icon} {h_attack}", "header")
                timeline_text.insert(tk.END, f" - {h_algo if h_algo else 'N/A'}\n")
                timeline_text.insert(tk.END, f"  Case: {h_case_id} | Result: {h_result}\n\n")
            
            timeline_text.tag_config("header", foreground="#00d9ff", font=("Consolas", 9, "bold"))
            timeline_text.config(state="disabled")
        else:
            tk.Label(timeline_container, text="No previous attempts found for this person.",
                    font=("Consolas", 10), bg="#1F1F1F", fg="#666666").pack(pady=20)
        
        # Close button
        close_btn = tk.Button(main_frame, text="CLOSE", font=("Consolas", 10, "bold"),
                             bg="#000000", fg="#00FF66", relief="solid", bd=2,
                             cursor="hand2", command=window.destroy, width=20, height=2)
        close_btn.pack(pady=20)
    
    def _create_section(self, parent, title):
        """Create a styled section frame"""
        frame = tk.LabelFrame(parent, text=title, font=("Consolas", 11, "bold"),
                             bg="#1F1F1F", fg="#00FF66", relief="solid", bd=2,
                             labelanchor="nw", padx=5, pady=5)
        frame.pack(fill="both", expand=True, pady=10)
        return frame
    
    def _add_field(self, parent, label, value, row):
        """Add a field to the grid"""
        tk.Label(parent, text=label, font=("Consolas", 10, "bold"),
                bg="#1F1F1F", fg="#00FF66").grid(row=row, column=0, sticky="w", pady=8, padx=10)
        tk.Label(parent, text=value, font=("Consolas", 10),
                bg="#1F1F1F", fg="#FFFFFF").grid(row=row, column=1, sticky="w", pady=8, padx=10)


if __name__ == "__main__":
    root = tk.Tk()
    CaseDetailUI(root, "CASE2026_001")
    root.mainloop()
