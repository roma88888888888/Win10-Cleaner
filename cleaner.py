import customtkinter as ctk
import os
import subprocess
import threading
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CleanerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("System Cleaner Pro")
        self.geometry("600x700")

        # Icon setup
        if getattr(sys, 'frozen', False):
            bundle_dir = sys._MEIPASS
        else:
            bundle_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(bundle_dir, "icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        # --- TABS SETUP ---
        self.tabview = ctk.CTkTabview(self, width=550, height=630)
        self.tabview.pack(pady=10, padx=10)
        
        self.tab_main = self.tabview.add("Main")
        self.tab_dev = self.tabview.add("Developer Options")

        # --- MAIN TAB ---
        self.main_label = ctk.CTkLabel(self.tab_main, text="SYSTEM CLEANER", font=("Segoe UI", 26, "bold"))
        self.main_label.pack(pady=20)

        self.log_view = ctk.CTkTextbox(self.tab_main, width=480, height=350, font=("Consolas", 12))
        self.log_view.pack(pady=10)

        self.start_button = ctk.CTkButton(self.tab_main, text="START CLEANING", 
                                         font=("Segoe UI", 14, "bold"),
                                         command=self.start_cleaning_thread)
        self.start_button.pack(pady=20)

        # --- DEVELOPER OPTIONS TAB ---
        self.dev_label = ctk.CTkLabel(self.tab_dev, text="ADVANCED TWEAKS", font=("Segoe UI", 20, "bold"))
        self.dev_label.pack(pady=20)

        # Telemetry Section
        self.t_label = ctk.CTkLabel(self.tab_dev, text="Telemetry Services:", font=("Segoe UI", 12, "bold"))
        self.t_label.pack(pady=5)
        self.create_dev_buttons("Telemetry", self.toggle_telemetry)

        # Windows Update Section
        self.u_label = ctk.CTkLabel(self.tab_dev, text="Windows Update:", font=("Segoe UI", 12, "bold"))
        self.u_label.pack(pady=5)
        self.create_dev_buttons("Updates", self.toggle_updates)

        # Copilot Section
        self.c_label = ctk.CTkLabel(self.tab_dev, text="Microsoft Copilot:", font=("Segoe UI", 12, "bold"))
        self.c_label.pack(pady=5)
        self.create_dev_buttons("Copilot", self.toggle_copilot)

    def create_dev_buttons(self, name, command_func):
        frame = ctk.CTkFrame(self.tab_dev, fg_color="transparent")
        frame.pack(pady=5)
        btn_off = ctk.CTkButton(frame, text=f"Disable {name}", fg_color="#d9534f", hover_color="#c9302c", 
                               width=150, command=lambda: command_func(False))
        btn_off.pack(side="left", padx=10)
        btn_on = ctk.CTkButton(frame, text=f"Enable {name}", fg_color="#5cb85c", hover_color="#4cae4c", 
                              width=150, command=lambda: command_func(True))
        btn_on.pack(side="left", padx=10)

    def log(self, text):
        self.log_view.insert("end", text + "\n")
        self.log_view.see("end")

    # --- TWEAK LOGIC ---

    def toggle_telemetry(self, enable):
        state = "start= auto" if enable else "start= disabled"
        cmd = "start" if enable else "stop"
        subprocess.run(f'sc config DiagTrack {state}', shell=True, capture_output=True)
        subprocess.run(f'sc {cmd} DiagTrack', shell=True, capture_output=True)
        self.log(f"Developer Mode: Telemetry {'Enabled' if enable else 'Disabled'}")

    def toggle_updates(self, enable):
        state = "start= auto" if enable else "start= disabled"
        cmd = "start" if enable else "stop"
        # Windows Update service name is 'wuauserv'
        subprocess.run(f'sc config wuauserv {state}', shell=True, capture_output=True)
        subprocess.run(f'sc {cmd} wuauserv', shell=True, capture_output=True)
        self.log(f"Developer Mode: Windows Updates {'Enabled' if enable else 'Disabled'}")

    def toggle_copilot(self, enable):
        val = 0 if enable else 1 # 1 means Disabled in Registry
        reg_path = r'HKCU\Software\Policies\Microsoft\Windows\WindowsCopilot'
        if not enable:
            subprocess.run(f'reg add "{reg_path}" /v "TurnOffWindowsCopilot" /t REG_DWORD /d 1 /f', shell=True, capture_output=True)
        else:
            subprocess.run(f'reg delete "{reg_path}" /v "TurnOffWindowsCopilot" /f', shell=True, capture_output=True)
        self.log(f"Developer Mode: Copilot {'Enabled' if enable else 'Disabled'} (Restart Explorer to see changes)")

    def start_cleaning_thread(self):
        self.start_button.configure(state="disabled", text="RUNNING...")
        self.log_view.delete("1.0", "end")
        threading.Thread(target=self.clean_logic).start()

    def clean_logic(self):
        self.log(">>> Starting Deep Cleanup...")
        # Temp files
        temp_path = os.environ.get("TEMP")
        if temp_path:
            subprocess.run(f'del /q /f /s "{temp_path}\\*.*"', shell=True, capture_output=True)
        
        self.log(">>> Temporary files cleared.")
        self.log(">>> Cleanup finished!")
        self.start_button.configure(state="normal", text="START CLEANING")

if __name__ == "__main__":
    app = CleanerApp()
    app.mainloop()