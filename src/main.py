import usb.core
import usb.util

# ค้นหาอุปกรณ์ USB
device = usb.core.find(idVendor=0x2ce3, idProduct=0x9563)

if device is None:
    raise ValueError("ไม่พบเครื่องอ่านบัตรประชาชน")

# ถ้ามีการตั้งค่า interface ต้องทำการ detach
if device.is_kernel_driver_active(0):
    device.detach_kernel_driver(0)

# ตั้งค่า endpoint และ interface
device.set_configuration()

# อ่านข้อมูลจากบัตร
try:
    # อ่านข้อมูลจาก Endpoint 0x81
    data = device.read(0x81, 4)  # ใช้ขนาด 4 bytes ตามที่กำหนด
    print("Data from card:", data.tobytes())  # แสดงข้อมูลในรูปแบบ bytes
except usb.core.USBError as e:
    print("Error reading:", e)
