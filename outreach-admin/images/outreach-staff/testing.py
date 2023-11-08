from flask import Flask, render_template, Response, request, redirect, session, jsonify, json, send_file, send_from_directory
from flask_cors import CORS
from datetime import datetime, timedelta
from flask_mysqldb import MySQL
import MySQLdb.cursors
import glob
import io
from io import StringIO, BytesIO
import csv
from werkzeug.wrappers import Response
import sqlite3
import webview
import threading
import sys
import socket
import os
import base64
import qrcode
from folderCreator import folderCreator



app = Flask(__name__)
CORS(app)


app.config['UPLOAD_FOLDER'] = 'images'


#window = webview.create_window('SwimsFormDesk', app, server_args={})

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
    
app.secret_key = 'nkvjbnkjkjkjnskfnkjfbni3w89ufhbbisef89hfknkjn'


def get_ipv4_address():
    # Get the IPv4 address of the first non-loopback network interface
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip_address = s.getsockname()[0]
    except:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address

ip_address = get_ipv4_address()



# SignIn Page
@app.route("/")
def login():
    port = request.environ.get('SERVER_PORT')
    print('The Port: ', port)
    return ('<h3><a href="/get-qrcode">QR-code</a></h3>')


# QR code
@app.route('/get-qrcode')
def get_qr_code():
    ip_address = get_ipv4_address()
    port = request.environ.get('SERVER_PORT')

    # Generate QR code with server's IP address and port
    qr_data = f'http://{ip_address}:{port}/upload-image?fPath=FW23NS000012/doc1/&avatar='
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    qr_path = os.path.join(app.config['UPLOAD_FOLDER'], 'qrcode.png')
    qr_img.save(qr_path)

    return send_from_directory(app.config['UPLOAD_FOLDER'], 'qrcode.png')




@app.route("/upload-image", methods=['POST'])
def uploadAvatar():
    try:
        res = {}
        
        fPath = request.form.get('fPath')
        avatarPath = './static/documents/' + fPath
        avatar = request.form.get('avatar')
        
        print('Resp: ', fPath, avatar)
        
        image_bytes = base64.b64decode(avatar)
        # Save the image to the upload folder
        image_path = os.path.join(avatarPath, 'uploaded_image.jpg')
        with open(image_path, 'wb') as f:
            f.write(image_bytes)
          
        res['status'] = 'success'    
        return (jsonify(res))
    except Exception as e:
        return str(e)

 

def start_server():
    app.run(host=ip_address, port=5000)

if __name__ == '__main__':
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    webview.create_window("Flask", f"http://{ip_address}:5000")  # Use 0.0.0.0 to bind to all network interfaces
    webview.start()
