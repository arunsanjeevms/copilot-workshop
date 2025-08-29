import tkinter as tk
from tkinter import messagebox
import pywhatkit as kit
from datetime import datetime
import time
import threading

# Global data storage
customers = []

# Function to add a customer
def add_customer():
    name = name_entry.get()
    phone = phone_entry.get()
    alert_date = date_entry.get()
    if not name or not phone or not alert_date:
        messagebox.showerror("Error", "All fields are required!")
        return
    
    try:
        # Validate date format
        datetime.strptime(alert_date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Date must be in YYYY-MM-DD format!")
        return
    
    # Add to customers list
    customers.append({"name": name, "phone": phone, "alert_date": alert_date})
    messagebox.showinfo("Success", f"Added alert for {name} on {alert_date}")
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)

# Function to send WhatsApp messages
def send_whatsapp_message(phone, message):
    try:
        # Schedule the message immediately (add a few seconds delay)
        now = datetime.now()
        kit.sendwhatmsg(phone, message, now.hour, now.minute + 1)
    except Exception as e:
        print(f"Failed to send message to {phone}: {e}")

# Function to check and send alerts
def check_alerts():
    while True:
        today = datetime.now().strftime("%Y-%m-%d")
        for customer in customers:
            if customer["alert_date"] == today:
                message = f"Hello {customer['name']}, this is your reminder!"
                send_whatsapp_message(customer["phone"], message)
                print(f"Message sent to {customer['name']} ({customer['phone']})")
        
        time.sleep(86400)  # Check once every day

# Start alert checking in a separate thread
def start_alert_thread():
    thread = threading.Thread(target=check_alerts, daemon=True)
    thread.start()

# GUI Setup
root = tk.Tk()
root.title("WhatsApp Alert Automation")
root.geometry("400x300")

# UI Components
tk.Label(root, text="Customer Name").pack(pady=5)
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)

tk.Label(root, text="Phone Number (+CountryCode)").pack(pady=5)
phone_entry = tk.Entry(root, width=30)
phone_entry.pack(pady=5)

tk.Label(root, text="Alert Date (YYYY-MM-DD)").pack(pady=5)
date_entry = tk.Entry(root, width=30)
date_entry.pack(pady=5)

add_button = tk.Button(root, text="Add Alert", command=add_customer)
add_button.pack(pady=10)

tk.Label(root, text="Alerts will be automatically checked daily.").pack(pady=10)

# Start the background alert checking thread
start_alert_thread()

# Start the Tkinter event loop
root.mainloop()

