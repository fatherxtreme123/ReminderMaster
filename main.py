import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import pygame
import TKinterModernThemes as TKMT
import webbrowser

def createToolTip(widget, text):
    try:
        def enter(event):
            widget._after_id = widget.after(600, show_tooltip, event)

        def leave(event):
            widget.after_cancel(widget._after_id)
            tooltip = getattr(widget, "_tooltip", None)
            if tooltip:
                tooltip.destroy()
                widget._tooltip = None

        def show_tooltip(event):
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root}+{event.y_root}")
            label = tk.Label(tooltip, text=text, background="black", foreground="white")
            label.grid()
            widget._tooltip = tooltip

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        try:
            super().__init__("ReminderMaster", "Sun-valley", "dark")
            self.master.iconbitmap('ReminderMaster.ico')
            self.master.resizable(False, False)

            self.main_frame = ttk.Frame(self.master)
            self.main_frame.grid(row=0, column=0, sticky="nsew")

            self.left_frame = ttk.Frame(self.main_frame, width=200, height=400)
            self.left_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ns")

            self.right_frame = ttk.Frame(self.main_frame)
            self.right_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

            self.text_input = ttk.Entry(self.right_frame)
            createToolTip(self.text_input, "Enter the text for the reminder.")
            self.text_input.grid(row=0, column=1, sticky="ew", pady=10)

            self.time_input = ttk.Entry(self.right_frame)
            createToolTip(self.time_input, "Enter the time for the reminder in the format (hours:minutes:seconds).\nFor example, 1:30:00 represents 1 hour, 30 minutes, and 0 seconds.")
            self.time_input.grid(row=1, column=1, sticky="ew", pady=10)

            self.repeat_var = tk.IntVar(value=1)
            self.repeat_check = ttk.Checkbutton(self.right_frame, text="Repeat Reminder", variable=self.repeat_var)
            createToolTip(self.repeat_check, "Enable repeating reminders.")
            self.repeat_check.grid(row=3, column=0, columnspan=2, pady=10)

            self.start_button = ttk.Button(self.right_frame, text="Start Reminder", command=self.start_reminder)
            createToolTip(self.start_button, "Click to start the reminder.")
            self.start_button.grid(row=4, column=0, columnspan=2, pady=10)

            self.status_label = ttk.Label(self.right_frame, text="Reminder not started", foreground="red")
            self.status_label.grid(row=7, column=0, columnspan=2, pady=10)

            self.sound_path = tk.StringVar()
            self.sound_path.set("No Sound")

            self.browse_sound_button = ttk.Button(self.right_frame, text="Browse Sound", command=self.browse_sound)
            createToolTip(self.browse_sound_button, "Browse and select a sound file (MP3) for the reminder.")
            self.browse_sound_button.grid(row=6, column=0, columnspan=2, pady=10)

            self.send_feedback_button = ttk.Button(self.left_frame, text="Send Feedback", command=self.send_feedback)
            createToolTip(self.send_feedback_button, "Click to open the GitHub issues page and send feedback")
            self.send_feedback_button.grid(row=6, column=0, sticky="ew", pady=10)

            self.reminder_thread = None
            self.time_input.insert(0, "0:05:00")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def browse_sound(self):
        try:
            sound_file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
            if sound_file_path:
                self.sound_path.set(sound_file_path)
            else:
                self.sound_path.set("default_reminder.mp3")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def start_reminder(self):
        try:
            text = self.text_input.get()
            time_str = self.time_input.get()
            if not time_str:
                return
            hours, minutes, seconds = map(int, time_str.split(":"))
            time_interval = hours * 3600 + minutes * 60 + seconds
            sound_path = self.sound_path.get()
            if sound_path == "No Sound":
                sound_path = "default_reminder.mp3"
            self.status_label.config(text="Reminder started", foreground="green")
            self.reminder_thread = threading.Thread(target=self.reminder, args=(time_interval, sound_path, text))
            self.reminder_thread.start()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def reminder(self, time_interval, sound_path, text):
        try:
            pygame.mixer.init()
            def play_sound():
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play()
            while True:
                time.sleep(time_interval)
                reminder_window = tk.Toplevel()
                reminder_window.geometry("400x200")
                reminder_window.attributes('-topmost', 1)
                if sound_path != "No Sound":
                    play_sound()
                label = tk.Label(reminder_window, text=text, font=("Arial", 12))
                label.pack()
                reminder_window.after(3000, lambda: self.stop_sound(reminder_window))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            pygame.mixer.quit()
            return
        
    def stop_sound(self, reminder_window):
        try:
            pygame.mixer.music.stop()
            reminder_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def send_feedback(self):
        try:
            webbrowser.open("https://github.com/fatherxtreme123/ReminderMaster/issues")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        App().run()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
