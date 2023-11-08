from flask import Flask, request, send_file
import qrcode
from PIL import Image, ImageDraw, ImageFont
import tempfile
import subprocess

app = Flask(__name__)

@app.route('/generate-and-print-qr', methods=['GET'])
def generate_and_print_qr():
    # Get the data for the QR code and text from the query parameters
    data = request.args.get('data')
    text = request.args.get('text')

    if not data or not text:
        return 'Both data and text parameters are required.', 400

    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add the data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create a temporary file to save the QR code image
    temp_img_path = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
    img = qr.make_image(fill_color='black', back_color='white')
    img.save(temp_img_path)

    # Open the image with PIL
    qr_image = Image.open(temp_img_path)
    draw = ImageDraw.Draw(qr_image)

    # Define the font and text position
    font = ImageFont.load_default()
    text_position = (10, qr_image.height - 30)

    # Add the text to the image
    draw.text(text_position, text, fill='black', font=font)

    # Save the modified image
    modified_img_path = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
    qr_image.save(modified_img_path)

    # Print the modified image using a system command (adjust the command based on your printer)
    print_command = ['lpr', modified_img_path]  # For Linux/Unix, you may need to install 'cups' and set up the printer
    subprocess.run(print_command, check=True)

    return 'QR code printed successfully.'

if __name__ == '__main__':
    app.run()
