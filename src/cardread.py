import usb.core
import usb.util

# ค้นหาอุปกรณ์ USB ที่เชื่อมต่อ
device = usb.core.find(idVendor=0x2ce3, idProduct=0x9563)  # รหัส Vendor และ Product ของเครื่องอ่านบัตร

if device is None:
    raise ValueError("ไม่พบเครื่องอ่านบัตรประชาชน")

# ถ้ามีการตั้งค่า interface ต้องทำการ detach
# if device.is_kernel_driver_active(0):
#     device.detach_kernel_driver(0)

# ตั้งค่า endpoint และ interface
device.set_configuration()

# อ่านข้อมูลจากเครื่องอ่านบัตร
try:
    data = device.read(0x81, 16)  # ขนาดและ endpoint จะขึ้นอยู่กับเครื่องอ่าน
    print("Data from card:", data)
except usb.core.USBError as e:
    print("Error reading:", e)
