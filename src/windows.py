import os
import sys
from tkinter import Tk, Label, Button, Frame
from PIL import Image, ImageTk
from smartcard.System import readers
from smartcard.util import toHexString

# Function to decode Thai characters
def thai2unicode(data):
    return bytes(data).decode('tis-620').strip()

# Function to get data from the card
def get_data(cmd, req=[0x00, 0xc0, 0x00, 0x00]):
    data, sw1, sw2 = connection.transmit(cmd)
    data, sw1, sw2 = connection.transmit(req + [cmd[-1]])
    return [data, sw1, sw2];

# Function to display data in the GUI
def display_data():
    data = {}
    commands = {
        "CID": CMD_CID,
        "TH Fullname": CMD_THFULLNAME,
        "EN Fullname": CMD_ENFULLNAME,
        "Date of Birth": CMD_BIRTH,
        "Gender": CMD_GENDER,
        "Card Issuer": CMD_ISSUER,
        "Issue Date": CMD_ISSUE,
        "Expire Date": CMD_EXPIRE,
        "Address": CMD_ADDRESS
    }

    for key, cmd in commands.items():
        response = get_data(cmd)
        if response:
            data[key] = thai2unicode(response)

    # Update labels with card data
    for widget in frame.winfo_children():
        widget.destroy()  # Clear previous labels
    for key, value in data.items():
        Label(frame, text=f"{key}: {value}").pack()

    # Load and display an image
    if "CID" in data:
        img_path = f"{data['CID']}.jpg"
        try:
            img = Image.open(img_path)
            img = img.resize((100, 100), Image.ANTIALIAS)
            img_label = Label(frame, image=ImageTk.PhotoImage(img))
            img_label.image = img  # Keep a reference to avoid garbage collection
            img_label.pack()
        except FileNotFoundError:
            print("Image not found.")

# Initialize smart card reader
reader_list = readers()
if not reader_list:
    print("No smart card readers found.")
    sys.exit(1)

reader = reader_list[0]
connection = reader.createConnection()
connection.connect()
atr = connection.getATR()
print("ATR: " + toHexString(atr))

# Commands to retrieve data
SELECT = [0x00, 0xA4, 0x04, 0x00, 0x08]
THAI_CARD = [0xA0, 0x00, 0x00, 0x00, 0x54, 0x48, 0x00, 0x01]
CMD_CID = [0x80, 0xb0, 0x00, 0x04, 0x02, 0x00, 0x0d]
CMD_THFULLNAME = [0x80, 0xb0, 0x00, 0x11, 0x02, 0x00, 0x64]
CMD_ENFULLNAME = [0x80, 0xb0, 0x00, 0x75, 0x02, 0x00, 0x64]
CMD_BIRTH = [0x80, 0xb0, 0x00, 0xD9, 0x02, 0x00, 0x08]
CMD_GENDER = [0x80, 0xb0, 0x00, 0xE1, 0x02, 0x00, 0x01]
CMD_ISSUER = [0x80, 0xb0, 0x00, 0xF6, 0x02, 0x00, 0x64]
CMD_ISSUE = [0x80, 0xb0, 0x01, 0x67, 0x02, 0x00, 0x08]
CMD_EXPIRE = [0x80, 0xb0, 0x01, 0x6F, 0x02, 0x00, 0x08]
CMD_ADDRESS = [0x80, 0xb0, 0x15, 0x79, 0x02, 0x00, 0x64]

# Create the main window
root = Tk()
root.title("Thai ID Smart Card Reader")

frame = Frame(root)
frame.pack(padx=10, pady=10)

Button(frame, text="Read Card Data", command=display_data).pack()

root.mainloop()
