import tkinter as tk
from tkinter import messagebox
import requests
import time
import ctypes
import os

# Этот блок скрывает консоль в Windows
def hide_console():
    if os.name == 'nt':
        window = ctypes.windll.kernel32.GetConsoleWindow()
        if window != 0:
            ctypes.windll.user32.ShowWindow(window, 0)

hide_console()

def start_sending():
    url = url_entry.get()
    text = message_entry.get()
    
    try:
        count = int(count_entry.get())
        # Получаем задержку и преобразуем в число с плавающей точкой (float)
        delay = float(delay_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Quantity and delay must be numbers!")
        return

    if not url or not text:
        messagebox.showwarning("Warning", "fill all fields!")
        return

    send_button.config(state=tk.DISABLED, text="Sending...")
    root.update() # Обновляем окно, чтобы кнопка сразу изменилась

    for i in range(count):
        try:
            response = requests.post(url, json={"content": text})
            
            if response.status_code == 429:
                wait = response.json().get('retry_after', 1)
                time.sleep(wait)
            
            # Используем введенную пользователем задержку
            time.sleep(delay)
            
        except Exception as e:
            messagebox.showerror("Error", f"an error occurred: {e}")
            break

    send_button.config(state=tk.NORMAL, text="Start boom")
    messagebox.showinfo("Ready", f"Sent successfully {count} messages!")

# Создание окна
root = tk.Tk()
root.title("Discord Webhook Boomer")
root.geometry("400x400")
root.resizable(False, False)

# Поля интерфейса
tk.Label(root, text="Webhook URL:", font=("Arial", 10, "bold")).pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=2)

tk.Label(root, text="Message text:").pack(pady=5)
message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=2)

tk.Label(root, text="How many times?").pack(pady=5)
count_entry = tk.Entry(root, width=15)
count_entry.insert(0, "1") # Значение по умолчанию
count_entry.pack(pady=2)

# НОВОЕ ПОЛЕ: Задержка
tk.Label(root, text="Delay between messages (seconds):", fg="blue").pack(pady=5)
delay_entry = tk.Entry(root, width=15)
delay_entry.insert(0, "1.0") # Значение по умолчанию (1 секунда)
delay_entry.pack(pady=2)

# Кнопка
send_button = tk.Button(root, text="Start boom", command=start_sending, 
                        bg="#7289da", fg="white", font=("Arial", 10, "bold"), height=2)
send_button.pack(pady=25)

root.mainloop()