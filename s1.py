import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import pytesseract
import requests
from reportlab.pdfgen import canvas
from twilio.rest import Client

# Initialize tkinter
root = tk.Tk()
root.title("Shop Billing System")

# Initialize variables and data structures
shop_items = {}  # Dictionary to store item details (barcode: [name, price])
creditors = {}  # Dictionary to store creditor details (name: [phone, amount])

# Twilio credentials (replace with your own values)
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'

# Initialize camera
cap = cv2.VideoCapture(0)

# Function to scan barcode using mobile camera
def scan_barcode():
    ret, frame = cap.read()
    cv2.imwrite('temp.png', frame)
    barcode_text = pytesseract.image_to_string(Image.open('temp.png'))
    if barcode_text in shop_items:
        item_name.set(shop_items[barcode_text][0])
        item_price.set(shop_items[barcode_text][1])
    else:
        messagebox.showerror("Error", "Item not found in the shop!")

# Function to add new items to the shop
def add_item():
    barcode_text = barcode_entry.get()
    item_name_text = item_name_entry.get()
    item_price_text = item_price_entry.get()
    shop_items[barcode_text] = [item_name_text, item_price_text]
    messagebox.showinfo("Success", "Item added to the shop!")

# Function to create creditors account and send WhatsApp reminder
def create_creditor_account():
    creditor_name_text = creditor_name_entry.get()
    creditor_phone_text = creditor_phone_entry.get()
    creditor_amount_text = creditor_amount_entry.get()
    creditors[creditor_name_text] = [creditor_phone_text, creditor_amount_text]
    create_pdf(creditor_name_text, creditor_phone_text, creditor_amount_text)
    send_whatsapp_message(creditor_phone_text)

    messagebox.showinfo("Success", "Creditor account created and reminder sent!")

# Function to create PDF invoice
def create_pdf(name, phone, amount):
    c = canvas.Canvas(f"{name}_invoice.pdf")
    c.drawString(100, 750, f"Name: {name}")
    c.drawString(100, 730, f"Phone: {phone}")
    c.drawString(100, 710, f"Amount: {amount}")
    c.save()

# Function to send WhatsApp reminder
def send_whatsapp_message(phone):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body="Please find the attached invoice for your credit account.",
        from_=f"whatsapp:{TWILIO_PHONE_NUMBER}",
        to=f"whatsapp:{phone}",
        media_url=['https://yourserver.com/path/to/invoice.pdf']
    )

# GUI elements
scan_button = tk.Button(root, text="Scan Barcode", command=scan_barcode)
scan_button.pack()

# ... (other GUI elements for barcode, item details, creditor details, etc.)

# Start the tkinter main loop
root.mainloop()

# Release the camera
cap.release()
cv2.destroyAllWindows()
