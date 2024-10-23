import usb.core
import usb.util

# ค้นหาอุปกรณ์ USB
device = usb.core.find(idVendor=0x2ce3, idProduct=0x9563)   # แทนที่ด้วยค่า idVendor และ idProduct ของเครื่องอ่านบัตร

if device is None:
    raise ValueError("ไม่พบเครื่องอ่านบัตรประชาชน")

# ดึงข้อมูล Serial Number ของอุปกรณ์
serial_number = usb.util.get_string(device, device.iSerialNumber)
print(f"Serial Number: {serial_number}")

# แสดง Device Descriptor
print("Device Descriptor:")
print(f"  bLength: {device.bLength}")
print(f"  bDescriptorType: {device.bDescriptorType}")
print(f"  bcdUSB: {device.bcdUSB}")
print(f"  bDeviceClass: {device.bDeviceClass}")
print(f"  bDeviceSubClass: {device.bDeviceSubClass}")
print(f"  bDeviceProtocol: {device.bDeviceProtocol}")
print(f"  bMaxPacketSize0: {device.bMaxPacketSize0}")
print(f"  idVendor: {device.idVendor}")
print(f"  idProduct: {device.idProduct}")
print(f"  bcdDevice: {device.bcdDevice}")
print(f"  iManufacturer: {device.iManufacturer}")
print(f"  iProduct: {device.iProduct}")
print(f"  iSerialNumber: {device.serial_number}")

# ดึงชื่อผู้ผลิตและผลิตภัณฑ์
manufacturer = usb.util.get_string(device, device.iManufacturer) if device.iManufacturer else "N/A"
product = usb.util.get_string(device, device.iProduct) if device.iProduct else "N/A"
serial_number = usb.util.get_string(device, device.iSerialNumber) if device.iSerialNumber else "N/A"

print(f"  Manufacturer: {manufacturer}")
print(f"  Product: {product}")
print(f"  Serial Number: {serial_number}")

print(device)

# อ่านข้อมูลจากเครื่องอ่านบัตร
# try:
#     data = device.read(0x9, 9)  # ขนาดและ endpoint จะขึ้นอยู่กับเครื่องอ่าน
#     print("Data from card:", data)
# except usb.core.USBError as e:
#     print("Error reading:", e)