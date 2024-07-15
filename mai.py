import requests
import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os

# List of proxies
proxies = [
    "47.251.43.115:33333",
    "43.132.124.11:3128",
    "189.240.60.171:9090",
    "47.251.43.115:33333",
    "223.135.156.183:8080",
    "45.77.147.46:3128",
    "67.43.227.226:30373"
]


# Function to create a session with a given proxy
def get_session_with_proxy(proxy):
    session = requests.Session()
    session.proxies = {
        "http": f"http://{proxy}",
        "https": f"https://{proxy}",
    }
    return session


# Function to test a proxy and update the result label
def test_proxy():
    selected_proxy = proxy_var.get()
    if selected_proxy:
        try:
            session = get_session_with_proxy(selected_proxy)
            response = session.get("http://httpbin.org/ip", timeout=5)
            response.raise_for_status()
            result_label.config(text=f"Proxy {selected_proxy} worked! IP returned: {response.json()['origin']}",
                                fg="green")

            # Set system proxy if the test is successful
            set_system_proxy(selected_proxy)

        except requests.exceptions.RequestException as e:
            result_label.config(text=f"Proxy {selected_proxy} failed: {e}", fg="red")
    else:
        result_label.config(text="Please select a proxy from the dropdown.", fg="orange")


# Function to set system-wide proxy on Windows
def set_system_proxy(proxy):
    try:
        # Create the registry path
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_WRITE)

        # Set proxy settings
        winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, proxy)
        winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)

        # Notify the system of the changes
        winreg.CloseKey(key)

        # Inform user of successful proxy setup
        result_label.config(text=f"System proxy set to {proxy}.", fg="green")

    except Exception as e:
        result_label.config(text=f"Failed to set system proxy: {e}", fg="red")


# Create the main window
root = tk.Tk()
root.title("Proxy Tester")

# Create and place the dropdown menu
proxy_var = tk.StringVar()
proxy_dropdown = ttk.Combobox(root, textvariable=proxy_var)
proxy_dropdown['values'] = proxies
proxy_dropdown.grid(row=0, column=0, padx=10, pady=10)

# Create and place the test button
test_button = tk.Button(root, text="Test Proxy", command=test_proxy)
test_button.grid(row=0, column=1, padx=10, pady=10)

# Create and place the result label
result_label = tk.Label(root, text="")
result_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
