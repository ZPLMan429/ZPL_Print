import socket
import tkinter as tk
from tkinter import filedialog, messagebox
import json

# Define a configuration file to save the IP
CONFIG_FILE = 'printer_config.json'

def save_printer_ip(ip_address):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(ip_address, f)

def load_printer_ip():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return ''

def send_to_printer(zpl_file_path, printer_ip):
    try:
        with open(zpl_file_path, 'r') as zpl_file:
            zpl_data = zpl_file.read()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        printer_address = (printer_ip, 9100)
        sock.connect(printer_address)

        try:
            sock.sendall(zpl_data.encode())
        finally:
            sock.close()

        # Save the printer IP for next time
        save_printer_ip(printer_ip)

        messagebox.showinfo("Success", "File sent to printer successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_files():
    filename = filedialog.askopenfilename(filetypes =[('ZPL Files', '*.zpl')])
    return filename

def create_gui():
    window = tk.Tk()
    window.title("ZPL Printer")

    file_label = tk.Label(window, text="No file selected")
    file_label.grid(column=0, row=0)

    printer_entry = tk.Entry(window)
    printer_entry.insert(0, load_printer_ip())
    printer_entry.grid(column=0, row=1)

    browse_button = tk.Button(window, text="Browse ZPL files", command=lambda: file_label.config(text=browse_files()))
    browse_button.grid(column=1, row=0)

    print_button = tk.Button(window, text="Print", command=lambda: send_to_printer(file_label.cget("text"), printer_entry.get()))
    print_button.grid(column=1, row=1)

    window.mainloop()

# Run the GUI
create_gui()
