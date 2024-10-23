import usb.core
import usb.util

# ค้นหาอุปกรณ์
device = usb.core.find(idVendor=0x2ce3, idProduct=0x9563)   # แทนที่ด้วยค่า idVendor และ idProduct ที่ถูกต้อง

if device is None:
    print("ไม่พบอุปกรณ์")
else:
    print("อุปกรณ์เชื่อมต่อสำเร็จ")
