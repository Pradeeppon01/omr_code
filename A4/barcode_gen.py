import barcode
from barcode.writer import ImageWriter
import time
import os
import qrcode


def generateBarcode(value):
    # Disable text display in the barcode image
    barcode.base.Barcode.default_writer_options['write_text'] = False

    # Generate the barcode
    barcode_value = value
    code128 = barcode.get_barcode_class('code128')
    barcode_instance = code128(barcode_value, writer=ImageWriter())

    # Specify the desired width and height for the barcode image
    width_px = 224
    height_px = 77

    # Save the barcode image with the specified width and height
    barcode_filename = value
    barcode_instance.save(f"images/barcodes/{barcode_filename}",{"module_width":0.32, "module_height":9, "font_size": 18, "text_distance": 1, "quiet_zone": 3})
    
    
    return f"images/barcodes/{barcode_filename}.png"


def generateQRCode(value):
    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(value)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Specify the desired width and height for the QR code image
    width_px = 84
    height_px = 84

    # Resize the QR code image
    qr_img = qr_img.resize((width_px, height_px))

    # Save the QR code image
    qr_filename = value
    qr_img.save(f"images/barcodes/{qr_filename}.png")
    
    return f"images/barcodes/{qr_filename}.png"