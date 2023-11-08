from flask import Flask, render_template, Response, request, redirect, session, jsonify, json, send_file, send_from_directory
from datetime import datetime, timedelta
import requests
import glob
import io
from io import StringIO, BytesIO
import csv
from werkzeug.wrappers import Response
import sqlite3
import socket
import os
import base64
import random
import subprocess
import qrcode
import threading
import webview
from folderCreator import folderCreator, usersFolder

app = Flask(__name__)

app.secret_key = 'nkvjbnkjkjkjnskni3w89ufhbbisef89090hfknkjn'

# Date today
current_date = datetime.now().strftime('%d/%m/%Y')
current_time = datetime.now().time()
formatted_time = current_time.strftime("%H:%M:%S")

# Previous 7th Date
def previous_seventh_date():
    current_date = datetime.now()
    previous_seventh_date = current_date - timedelta(days=7)
    formatted_date = previous_seventh_date.strftime('%d/%m/%Y')
    return formatted_date

# SQLite 3 connection 
def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

# Get System IP address
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


@app.route('/print-new-qr', methods=['GET'])
def print_image_new():
    try:
        # Check if the 'image' field is in the request
        data = request.args.get('w_reg_num')
        wName = request.args.get('w_name')
        #print('worReg -> ', data)
        full_data = str(data) + "\n" + str(wName)
        if not data:
            return 'Data parameter is required.', 400

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
        temp_img_path = 'temp_qr.png'
        img = qr.make_image(fill_color='black', back_color='white')
        img.save(temp_img_path)

        # Serve the temporary QR code image
        #return send_file(temp_img_path, mimetype='image/png')
        
        # Get the uploaded image file
        uploaded_file = 'static/swims-qr.png'
       
        # Save the uploaded image to a temporary file
        #temp_img_path = 'static/swims-qr.png'
    
        # Execute the C# executable with the image path as an argument
        csharp_exe = 'windowsPrint\\bin\\Release\\net7.0\\win-x64\\windowsPrint.exe'
        #command = [csharp_exe, temp_img_path]
        width_cm = 3
        height_cm = 3
        command = [csharp_exe, temp_img_path, full_data, str(width_cm), str(height_cm)]
        
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Delete the temporary image file
        #os.remove(temp_img_path)

        if result.returncode == 0:
            session['print_qr_success'] = f'QR for {data} printed successfully.'
            return redirect('/admin-print-qr-code')
        else:
            session['print_qr_fail'] = f'QR for {data} printing failed.'
            return redirect('/admin-print-qr-code')

    except Exception as e:
        session['print_qr_fail'] = f'QR for {data} printing failed.'
        return redirect('/admin-print-qr-code')



@app.route('/user-print-new-qr', methods=['GET'])
def user_print_image_new():
    try:
        # Check if the 'image' field is in the request
        data = request.args.get('w_reg_num')
        #print('worReg -> ', data)
        wName = request.args.get('w_name')
        #print('worReg -> ', data)
        full_data = str(data) + "\n" + str(wName)
        
        if not data:
            return 'Data parameter is required.', 400

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
        temp_img_path = 'temp_qr.png'
        img = qr.make_image(fill_color='black', back_color='white')
        img.save(temp_img_path)

        # Serve the temporary QR code image
        #return send_file(temp_img_path, mimetype='image/png')
        
        # Get the uploaded image file
        uploaded_file = 'static/swims-qr.png'
       
        # Save the uploaded image to a temporary file
        #temp_img_path = 'static/swims-qr.png'
    
        # Execute the C# executable with the image path as an argument
        csharp_exe = 'windowsPrint\\bin\\Release\\net7.0\\win-x64\\windowsPrint.exe'
        #command = [csharp_exe, temp_img_path]
        width_cm = 3
        height_cm = 3
        command = [csharp_exe, temp_img_path, full_data, str(width_cm), str(height_cm)]
        
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Delete the temporary image file
        #os.remove(temp_img_path)

        if result.returncode == 0:
            session['user_print_qr_success'] = f'QR for {data} printed successfully.'
            return redirect('/my-registration-list')
        else:
            session['user_print_qr_fail'] = f'QR for {data} printing failed.'
            return redirect('/my-registration-list')

    except Exception as e:
        session['user_print_qr_fail'] = f'QR for {data} printing failed.'
        return redirect('/my-registration-list')





# ----------------------------
# -- Request to Staff Admin --
# ----------------------------

# Connection to Staff Admin
def connectionStaffServer(serverIP):
    url = f"http://{serverIP}:6787/staff-server-req"
    data = {
        'server_ip': serverIP
    }
    try:
        response = requests.post(url, data=data, timeout=1)
        response.raise_for_status() 

        data = response.json()
        return data
    except requests.exceptions.ConnectionError:
        return 'connection_lost'
    except requests.exceptions.RequestException as e:
        return f'error: {str(e)}'



# Check - Connection to Staff Admin
@app.route("/server-connection", methods=['GET'])
def serverConnection():
    url = request.args.get('url')
    # check
    result = connectionStaffServer(url)
    if result == 'connection_lost':
        return jsonify({"status": "connection_lost"})
    elif result == 'fail':
         return jsonify({"Request to the server failed."})
    else:
       return jsonify({"status": "connected"})

# Add a new route to get the server IP from the database
@app.route("/get-server-ip", methods=['GET'])
def getServerIP():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT admin_server_ip FROM staff_status")
        serverIP = cur.fetchone()
        conn.close()

        if serverIP:
            return jsonify({"serverIP": serverIP[0]})
        else:
            return jsonify({"serverIP": ""})  # Return an empty string if no IP is found
    except Exception as e:
        return jsonify({"error": str(e)})

# SignIn Page
@app.route("/connect-server", methods=['POST'])
def connectServer():
    if request.method == 'POST':
        try:
            #port = request.environ.get('SERVER_PORT')
            conn = get_db_connection()
            cur = conn.cursor()

            serverIP = request.form.get('server_ip')
            print(serverIP)

            
            result = connectionStaffServer(serverIP)
            if result == 'connection_lost':
                session['auth_error'] = 'not_connected'
                return redirect('/')
            elif result == 'fail':
                session['auth_error'] = 'not_connected'
                return redirect('/')
            else:
                cur.execute("DELETE FROM staff_status")
                cur.execute("INSERT INTO staff_status(admin_server_ip) VALUES(?)", (serverIP,))
                conn.commit()
                conn.close()
                session['auth_stat'] = 'connected'
                return redirect('/')

        except Exception as e:
            session['auth_error'] = 'not_connected'
            return redirect('/')
    else:
        session['auth_error'] = "access_denied"
        return redirect('/')
    


def staff_verification_request(getIP, port, username, password):
    url = f"http://{getIP}:6787/staff-verification"
    allData = {
        'username': username,
        'password': password,
        'staff_server_ip': ip_address,
        'staff_server_port': port
    }

    try:
        response = requests.post(url, data=allData, timeout=1)

        if response.status_code == 200:
            data = response.json()
            #print('Response:', data)
            return data
        else:
            print(f'Request failed with status code: {response.status_code}')
            return None
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        return None




def confirmCompanyProfile(compName):
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]

        # request
        url = f"http://{getIP}:6787/staff-confirm-company-profile"
        data = {
            'company_name': compName
        }

        try:
            response = requests.post(url, data=data)
            response.raise_for_status() 

            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'
    

def getCompanyProfile(username):
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]

        # request
        url = f"http://{getIP}:6787/staff-get-company-profile"
        data = {
            'username': username
        }

        try:
            response = requests.post(url, data=data)
            response.raise_for_status() 

            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'
    
  
# send worker data
def sendWorkerData(username, data):
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]

        # request
        url = f"http://{getIP}:6787/staff-insert-worker"
        data = {
            'username': username,
            'data': data
        }

        try:
            response = requests.post(url, json=data)
            response.raise_for_status() 

            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'
    

    

# Staff Profile
def staffProfile(username):
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]

        # request
        url = f"http://{getIP}:6787/staff-profile"
        data = {
            'username': username
        }

        try:
            response = requests.post(url, data=data)
            response.raise_for_status() 

            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'


# Staff worker list
def staffWorkerList(username):
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]

        # request
        url = f"http://{getIP}:6787/staff-worker-list"
        data = {
            'username': username
        }

        try:
            response = requests.post(url, data=data)
            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            res = {
                'status': 'connection lost'
            }
            return jsonify(res)
        except requests.exceptions.RequestException as e:
            res = {
                'status': 'request failed'
            }
            return jsonify(res)
    else:
        res = {
            'status': 'no server ip'
        }
        return jsonify(res)



# employment Detail   
def employmentDetail():
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        # request
        url = f"http://{getIP}:6787/staff-employment-detail"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'
    
# Citizenship  
def citizenship():
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        # request
        url = f"http://{getIP}:6787/staff-citizenship"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'
    
@app.route("/get-citizenship", methods=['GET'])
def get_citizenship():
    citizenship_data = citizenship()  # Call the 'citizenship' function to fetch real-time gender data
    return jsonify({"citizenshipList": citizenship_data})  
  
# Marital 
def marital():
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        # request
        url = f"http://{getIP}:6787/staff-marital"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'


@app.route("/get-maritial", methods=['GET'])
def get_marital():
    maritial_data = marital()  # Call the 'citizenship' function to fetch real-time gender data
    return jsonify({"maritialList": maritial_data})           

# poe 
def poe():
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        # request
        url = f"http://{getIP}:6787/staff-poe"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'


# gender 
def gender():
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        # request
        url = f"http://{getIP}:6787/staff-gender"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'
@app.route("/get-gender", methods=['GET'])
def get_gender():
    gender_data = gender()  # Call the 'gender' function to fetch real-time gender data
    return jsonify({"genderList": gender_data})

# religion 
def religion():
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        # request
        url = f"http://{getIP}:6787/staff-religion"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'

# race 
def race():
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        # request
        url = f"http://{getIP}:6787/staff-race"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'

# relationship 
def relationship():
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        # request
        url = f"http://{getIP}:6787/staff-relationship"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'

# job_sector 
def job_sector():
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        # request
        url = f"http://{getIP}:6787/staff-job-sector"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'

# job_status_sponsor 
def job_status_sponsor():
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        # request
        url = f"http://{getIP}:6787/staff-job-status-sponsor"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'


# city 
def city():
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        # request
        url = f"http://{getIP}:6787/staff-city"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'


# state 
def state():
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        # request
        url = f"http://{getIP}:6787/staff-state"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'
    
# issuingCountry 
def issuingCountry():
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        # request
        url = f"http://{getIP}:6787/staff-issuingCountry"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'


# docStatus 
def docStatus():
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        # request
        url = f"http://{getIP}:6787/staff-docStatus"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'

# curDocStatus 
def curDocStatus():
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        # request
        url = f"http://{getIP}:6787/staff-curDocStatus"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'

# typeOfDoc 
def typeOfDoc():
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        # request
        url = f"http://{getIP}:6787/staff-typeOfDoc"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'
    

# employment_status 
def employment_status():
    conn = get_db_connection()
    cur = conn.cursor()
    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        # request
        url = f"http://{getIP}:6787/staff-employment-status"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            resD = response.json()
            return resD
        except requests.exceptions.ConnectionError:
            return 'connection_lost'
        except requests.exceptions.RequestException as e:
            return 'error'
    else:
        return 'no_server_ip'






# ----------------------------------
# -- End * Request to Staff Admin --
# ----------------------------------




# SignIn Page
@app.route("/")
def login():
    #port = request.environ.get('SERVER_PORT')
    conn = get_db_connection()
    cur = conn.cursor()
    
    if 'admin_session' in session:
        return redirect('/admin-dash')
    elif 'user_session' in session:
        return redirect('/add-worker')
    elif 'subAdmin_session' in session:
        return redirect('/sub-admin-dash')
    elif 'subUser_session' in session:
        return redirect('/sub-user-add-worker')
    
    return render_template('login.html')



# Auth the admin & Users
@app.route("/auth", methods=['POST'])
def auth():
    if(request.method == 'POST'):
        username = request.form.get('user')
        password = request.form.get('pwd')
        port = request.environ.get('SERVER_PORT')
    
        # Database
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check Connection
        cur.execute("SELECT admin_server_ip FROM staff_status")
        qD = cur.fetchall()
        qD_len = len(qD)
        if qD_len == 1:
            getIP = qD[0][0]
            #print(getIP)
            response = connectionStaffServer(getIP)
            #print('response: ', response)

            if response == 'connection_lost':
                session['auth_error'] = 'not_connected'
                return redirect('/')
            elif response['status'] == 'success':
                if username and password:
                    try:
                        response = staff_verification_request(getIP, port, username, password)
                        if response['status'] == 'success':
                            session['user_session'] = response['data']
                            return redirect('/add-worker')
                        else:
                            #print('endpoint error')
                            session['auth_error'] = 'error'
                            return redirect('/') 

                    except Exception as e:
                        #print(e)
                        session['auth_error'] = 'error'
                        return redirect('/')
                else:
                    session['auth_error'] = 'error'
                    return redirect('/')
            else:
                session['auth_error'] = 'not_connected'
                return redirect('/')
        else:
            session['auth_error'] = 'not_connected'    
            return redirect('/')
    else:
        return redirect('/')



@app.route('/my-reg-list-request', methods=['GET'])
def staff_reg_list_request():
    if 'user_session' in session:
        searchData = request.args.get('request_data')
        print(searchData)
        # Database
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT admin_server_ip FROM staff_status")
        qD = cur.fetchall()
        qD_len = len(qD)
        if qD_len == 1:
            getIP = qD[0][0]
            #print(getIP)
            response = connectionStaffServer(getIP)

            if response == 'connection_lost':
                session['auth_error'] = 'not_connected'
                return redirect('/')
            elif response['status'] == 'success':
                url = f"http://{getIP}:6787/staff-my-registration-list-request"
                req_data = {
                    'search_data': searchData
                }

                try:
                    response = requests.post(url, data=req_data)

                    if response.status_code == 200:
                        data = response.json()
                        if data['status'] == 'success':
                            workerD = data['worker_data']
                            totalWorker = data['total_worker']
                            return render_template('my-registration-list.html', workerList2 = workerD, totalForm2=totalWorker)
                        else:
                            return render_template('my-registration-list.html', status='no_data')
                    else:
                        print(f'Request failed with status code: {response.status_code}')
                        return None
                    
                except requests.exceptions.RequestException as e:
                    print(f'Request failed: {e}')
                    return None 
            else:
                session['auth_error'] = 'not_connected'
                return redirect('/')
        else:
            redirect('/')
    else:
        return redirect('/')


@app.route('/company-list')
def staff_companyList():
    if 'user_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT admin_server_ip FROM staff_status")
        qD = cur.fetchall()
        qD_len = len(qD)
        if qD_len == 1:
            getIP = qD[0][0]
            
            response = connectionStaffServer(getIP)

            if response == 'connection_lost':
                session['auth_error'] = 'not_connected'
                return redirect('/')
            elif response['status'] == 'success':
                url = f"http://{getIP}:6787/staff-company-list-req"
                print(url)
                try:
                    response = requests.get(url)

                    if response.status_code == 200:
                        data = response.json()
                        if data['status'] == 'success':
                            return data
                        else:
                            response = {
                                'status': 'no_data'
                            }
                            return jsonify(response)
                            
                    else:
                        response = {
                            'status': 'fail'
                        }
                        return jsonify(response)
                    
                except requests.exceptions.RequestException as e:
                    response = {
                            'status': 'fail'
                    }
                    return jsonify(response)
            else:
                session['auth_error'] = 'not_connected'
                return redirect('/')
        else:
            redirect('/')
    else:
        return redirect('/')
    
'''
# Upload Worker Docs
@app.route("/upload-worker-docs", methods=['POST'])
def uploadWorkerDocs():
    try:
        res = {}
        # DB
        conn = get_db_connection()
        cur = conn.cursor()

        workerRegNum = request.form.get('q_rN')
        docNum = request.form.get('q_dN')
        avatar = request.form.get('avatar')
        
        if workerRegNum and docNum and avatar:
            # check query
            cur.execute('SELECT worker_reg_no FROM workers_document WHERE document_link=? AND worker_reg_no=?', (docNum, workerRegNum))
            q = cur.fetchall()
            qLen = len(q)
            if qLen == 0:
                cur.execute('INSERT INTO workers_document(document_link, worker_reg_no, document_image) VALUES(?, ?, ?)', (docNum, workerRegNum, avatar))
            elif qLen == 1:
                cur.execute('UPDATE workers_document SET document_image=? WHERE document_link=? AND worker_reg_no=?', (avatar, docNum, workerRegNum))

            conn.commit()
            conn.close()
            res['status'] = 'success'    
            return (jsonify(res))
        else:
            res['status'] = 'error'    
            return (jsonify(res))
    except Exception as e:
        res['status'] = 'error'    
        return (jsonify(res))
'''

@app.route("/upload-worker-docs", methods=['POST'])
def uploadWorkerDocs():
    
    res = {}
    # DB
    conn = get_db_connection()
    cur = conn.cursor()

    workerRegNum = request.form.get('q_rN')
    docNum = request.form.get('q_dN')
    avatar = request.form.get('avatar')
    
    if workerRegNum and docNum and avatar:
        cur.execute("SELECT admin_server_ip FROM staff_status")
        qD = cur.fetchall()
        qD_len = len(qD)
        if qD_len == 1:
            getIP = qD[0][0]
            #print(getIP)
            response = connectionStaffServer(getIP)

            if response == 'connection_lost':
                session['auth_error'] = 'not_connected'
                return redirect('/')
            elif response['status'] == 'success':
                url = f"http://{getIP}:6787/staff-upload-worker-docs"
                req_data = {
                    'workerRegNum': workerRegNum,
                    'docNum': docNum,
                    'avatar': avatar
                }

                try:
                    response = requests.post(url, data=req_data)

                    if response.status_code == 200:
                        data = response.json()
                        if data['status'] == 'success':
                            res['status'] = 'success'
                            return jsonify(res)
                        else:
                            res['status'] = 'response fail'
                            return jsonify(res)
                    else:
                        res['status'] = 'Request failed'
                        return jsonify(res)
                    
                except requests.exceptions.RequestException as e:
                    print(f'Request failed: {e}')
                    res['status'] = 'request failed'    
                    return jsonify(res)
            else:
                res['status'] = 'unable to connect server'    
                return jsonify(res)
        else:
            res['status'] = 'error'    
            return jsonify(res)      
    else:
        res['status'] = 'error'    
        return jsonify(res)
    


# Fetch Worker Docs
'''
@app.route("/fetch-worker-docs", methods=['POST'])
def fetchWorkerDocs():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        data = request.get_json()
        
        workerRegNum = data.get('q_rN')
        docNum = data.get('q_dN')
        # check query
        cur.execute('SELECT document_image FROM workers_document WHERE document_link=? AND worker_reg_no=?', (docNum, workerRegNum))
        q = cur.fetchall()
        qLen = len(q)
        if qLen == 0:
            response = {
                'status': 'success',
                'imageData': 'None'
            }
            return jsonify(response)    
        elif qLen == 1:
            response = {
                'status': 'success',
                'imageData': q
            }
            return jsonify(response)
        
    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }
        return jsonify(response)
'''
@app.route("/fetch-worker-docs", methods=['POST'])
def fetchWorkerDocs():
    conn = get_db_connection()
    cur = conn.cursor()

    data = request.get_json()
    
    workerRegNum = data.get('q_rN')
    docNum = data.get('q_dN')

    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        #print(getIP)
        response = connectionStaffServer(getIP)

        if response == 'connection_lost':
            session['auth_error'] = 'not_connected'
            return redirect('/')
        elif response['status'] == 'success':
            url = f"http://{getIP}:6787/staff-fetch-worker-docs"
            req_data = {
                'workerRegNum': workerRegNum,
                'docNum': docNum
            }

            try:
                response = requests.post(url, data=req_data)

                if response.status_code == 200:
                    data = response.json()
                    if data['status'] == 'success':
                        res = {
                            'status': 'success',
                            'imageData': data['imageData']
                        }
                        return jsonify(res) 
                    else:
                        res = {
                            'status': 'no image data'
                        }
                        return jsonify(res) 

                else:
                    res = {
                        'status': 'no result'
                    }
                    return jsonify(res) 
                
            except requests.exceptions.RequestException as e:
                res = {}
                res['status'] = 'request failed'    
                return jsonify(res)
        else:
            res = {}
            res['status'] = 'unable to connect server'    
            return jsonify(res)
    else:
        res = {}
        res['status'] = 'not found your server'    
        return jsonify(res)      
    

'''
# Upload fMember Docs
@app.route("/upload-fMember-docs", methods=['POST'])
def upload_fMemberDocs():
    try:
        res = {}
        # DB
        conn = get_db_connection()
        cur = conn.cursor()

        workerRegNum = request.form.get('q_rN')
        docNum = request.form.get('q_dN')
        avatar = request.form.get('avatar')
        
        if workerRegNum and docNum and avatar:
            # check query
            cur.execute('SELECT fm_reg_no FROM fm_document WHERE document_link=? AND fm_reg_no=?', (docNum, workerRegNum))
            q = cur.fetchall()
            qLen = len(q)
            if qLen == 0:
                cur.execute('INSERT INTO fm_document(document_link, fm_reg_no, document_image) VALUES(?, ?, ?)', (docNum, workerRegNum, avatar))
            elif qLen == 1:
                cur.execute('UPDATE fm_document SET document_image=? WHERE document_link=? AND fm_reg_no=?', (avatar, docNum, workerRegNum))

            conn.commit()
            conn.close()
            res['status'] = 'success'    
            return (jsonify(res))
        else:
            res['status'] = 'error'    
            return (jsonify(res))
    except Exception as e:
        res['status'] = 'error'    
        return (jsonify(res))
'''
@app.route("/upload-fMember-docs", methods=['POST'])
def upload_fMemberDocs():
    
    res = {}
    # DB
    conn = get_db_connection()
    cur = conn.cursor()

    workerRegNum = request.form.get('q_rN')
    docNum = request.form.get('q_dN')
    avatar = request.form.get('avatar')
    
    if workerRegNum and docNum and avatar:
        cur.execute("SELECT admin_server_ip FROM staff_status")
        qD = cur.fetchall()
        qD_len = len(qD)
        if qD_len == 1:
            getIP = qD[0][0]
            #print(getIP)
            response = connectionStaffServer(getIP)

            if response == 'connection_lost':
                session['auth_error'] = 'not_connected'
                return redirect('/')
            elif response['status'] == 'success':
                url = f"http://{getIP}:6787/staff-upload-fMember-docs"
                req_data = {
                    'workerRegNum': workerRegNum,
                    'docNum': docNum,
                    'avatar': avatar
                }

                try:
                    response = requests.post(url, data=req_data)

                    if response.status_code == 200:
                        data = response.json()
                        if data['status'] == 'success':
                            res['status'] = 'success'
                            return jsonify(res)
                        else:
                            res['status'] = 'response fail'
                            return jsonify(res)
                    else:
                        res['status'] = 'Request failed'
                        return jsonify(res)
                    
                except requests.exceptions.RequestException as e:
                    print(f'Request failed: {e}')
                    res['status'] = 'request failed'    
                    return jsonify(res)
            else:
                res['status'] = 'unable to connect server'    
                return jsonify(res)
        else:
            res['status'] = 'error'    
            return jsonify(res)      
    else:
        res['status'] = 'error'    
        return jsonify(res)

'''
# Fetch fMember Docs
@app.route("/fetch-fMember-docs", methods=['POST'])
def fetch_fMemberDocs():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        data = request.get_json()
        
        workerRegNum = data.get('q_rN')
        docNum = data.get('q_dN')
        #print('find data: ->', workerRegNum, docNum)
        # check query
        cur.execute('SELECT document_image FROM fm_document WHERE document_link=? AND fm_reg_no=?', (docNum, workerRegNum))
        q = cur.fetchall()
        qLen = len(q)
        if qLen == 0:
            response = {
                'status': 'success',
                'imageData': 'None'
            }
            return jsonify(response)    
        elif qLen == 1:
            #print('response Data: ', q)
            response = {
                'status': 'success',
                'imageData': q
            }
            return jsonify(response)
        
    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }
        return jsonify(response)
'''
@app.route("/fetch-fMember-docs", methods=['POST'])
def fetch_fMemberDocs():
    conn = get_db_connection()
    cur = conn.cursor()

    data = request.get_json()
    
    workerRegNum = data.get('q_rN')
    docNum = data.get('q_dN')

    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]
        #print(getIP)
        response = connectionStaffServer(getIP)

        if response == 'connection_lost':
            session['auth_error'] = 'not_connected'
            return redirect('/')
        elif response['status'] == 'success':
            url = f"http://{getIP}:6787/staff-fetch-fMember-docs"
            req_data = {
                'workerRegNum': workerRegNum,
                'docNum': docNum
            }

            try:
                response = requests.post(url, data=req_data)

                if response.status_code == 200:
                    data = response.json()
                    if data['status'] == 'success':
                        res = {
                            'status': 'success',
                            'imageData': data['imageData']
                        }
                        return jsonify(res) 
                    else:
                        res = {
                            'status': 'no image data'
                        }
                        return jsonify(res) 

                else:
                    res = {
                        'status': 'no result'
                    }
                    return jsonify(res) 
                
            except requests.exceptions.RequestException as e:
                res = {}
                res['status'] = 'request failed'    
                return jsonify(res)
        else:
            res = {}
            res['status'] = 'unable to connect server'    
            return jsonify(res)
    else:
        res = {}
        res['status'] = 'not found your server'    
        return jsonify(res)      










# ----------------------
# * Start User Section *
# ----------------------

# ref Gender
@app.route("/ref-gender", methods=['GET'])
def refGender():
    try:
        gender_detail = gender()
        gender_status = gender_detail['status']
        if gender_status == 'success':
            gender_data = gender_detail['gender']
            return gender_data
        return False
    except Exception as e:
        return False
    
# ref Citizenship
@app.route("/ref-citizenship", methods=['GET'])
def refCitizenship():
    try:
        citizenship_detail = citizenship()
        citizenship_status = citizenship_detail['status']
        if citizenship_status == 'success':
            citizenship_data = citizenship_detail['citizenship']
            return citizenship_data
        return False
    except Exception as e:
        return False

# ref maritial Status
@app.route("/ref-maritial", methods=['GET'])
def refMarital():
    try:
        marital_detail = marital()
        marital_status = marital_detail['status']
        if marital_status == 'success':
            marital_data = marital_detail['marital']
            return marital_data  # Fixed the variable name here, from "maritial_data" to "marital_data"
        return False
    except Exception as e:
        return False

# ref Poe
@app.route("/ref-poe", methods=['GET'])
def refPoe():
    try:
        poe_detail = poe()
        poe_status = poe_detail['status']
        if poe_status == 'success':
            poe_data = poe_detail['poe']
            return poe_data  # Fixed the variable name here, from "poe" to "poe"
        return False
    except Exception as e:
        return False

# ref Religion
@app.route("/ref-religion", methods=['GET'])
def refReligion():
    try:
        religion_detail = religion()
        religion_status = religion_detail['status']
        if religion_status == 'success':
            religion_data = religion_detail['religion']
            return religion_data  # Fixed the variable name here, from "religion" to "religion"
        return False
    except Exception as e:
        return False

# ref Race
@app.route("/ref-race", methods=['GET'])
def refRace():
    try:
        race_detail = race()
        race_status = race_detail['status']
        if race_status == 'success':
            race_data = race_detail['race']
            return race_data  # Fixed the variable name here, from "race" to "race"
        return False
    except Exception as e:
        return False


# ref Relationship
@app.route("/ref-relationship", methods=['GET'])
def refRelationship():
    try:
        relationship_detail = relationship()
        relationship_status = relationship_detail['status']
        if relationship_status == 'success':
            relationship_data = relationship_detail['relationship']
            return relationship_data  # Fixed the variable name here, from "relationship" to "relationship"
        return False
    except Exception as e:
        return False


# ref Sector
@app.route("/ref-sector", methods=['GET'])
def refSector():
    try:
        job_sector_detail = job_sector()
        job_sector_status = job_sector_detail['status']
        if job_sector_status == 'success':
            job_sector_data = job_sector_detail['job_sector']
            return job_sector_data  # Fixed the variable name here, from "sector_data" to "job_sector_data"
        return False
    except Exception as e:
        return False


# ref Employment Detail
@app.route("/ref-emp-detail", methods=['GET'])
def refEmploymentDetail():
    try:
        employment_status_detail = employment_status()
        employment_status_status = employment_status_detail['status']
        if employment_status_status == 'success':
            employment_status_data = employment_status_detail['employment_status']
            return employment_status_data  # Fixed the variable name here, from "employment_status" to "employment_status"
        return False
    except Exception as e:
        return False



# ref Working Status
@app.route("/ref-working-status", methods=['GET'])
def refEmploymentSponsorship():
    try:
        job_status_sponsor_detail = job_status_sponsor()
        job_status_sponsor_status = job_status_sponsor_detail['status']
        if job_status_sponsor_status == 'success':
            job_status_sponsor_data = job_status_sponsor_detail['job_status_sponsor']
            return job_status_sponsor_data  # Fixed the variable name here, from "employment_status" to "employment_status"
        return False
    except Exception as e:
        return False

# ref City
@app.route("/ref-city", methods=['GET'])
def refCity():
    try:
        city_detail = city()
        city_status = city_detail['status']
        if city_status == 'success':
            city_data = city_detail['city']
            return city_data  # Fixed the variable name here, from "city" to "city"
        return False
    except Exception as e:
        return False

# ref State
@app.route("/ref-state", methods=['GET'])
def refState():
    try:
        state_detail = state()
        state_status = state_detail['status']
        if state_status == 'success':
            state_data = state_detail['state']
            return state_data  # Fixed the variable name here, from "state" to "state"
        return False
    except Exception as e:
        return False


# Get Company Name in Sort form
def company_first_letters(input_string):
    words = input_string.split()
    first_letters = [word[0] for word in words]
    return ''.join(first_letters)


# Add Worker
@app.route("/add-worker", methods=['GET'])
def addWorker():
    if 'user_session' in session:
        active_user_session = session.get('user_session')
        serverPort = request.environ.get('SERVER_PORT')
        
        compName = request.args.get('company_name')
        worker_reg_no = request.args.get('wRgNo')

        # DB
        conn = get_db_connection()
        cur = conn.cursor()

        if compName and worker_reg_no:
            # request
            confirmProfile = confirmCompanyProfile(compName)

            confirmProfile_status = confirmProfile['status']
            if confirmProfile_status != 'success':
                session['incomplete_company_profile'] = 'not completed'
                return render_template('add-worker.html', profileC=0)
            
            profile_username = confirmProfile['username']

            # Profile request
            getProfile = getCompanyProfile(profile_username)
            getProfile_status = getProfile['status']
            if confirmProfile_status != 'success':
                session['incomplete_company_profile'] = 'not completed'
                return render_template('add-worker.html', profileC=0)

            profileBranchAddress = getProfile['profile']
            for row in profileBranchAddress:
                branch_address1 = row[0]
                branch_address2 = row[1]
                branch_address3 = row[2]
                aps_contact_person = row[3]
                branch_state = row[4]
                branch_city = row[5]

            fMember_regNum_1 = f'{worker_reg_no}-1'
            fMember_regNum_2 = f'{worker_reg_no}-2'
            fMember_regNum_3 = f'{worker_reg_no}-3'
            fMember_regNum_4 = f'{worker_reg_no}-4'
            fMember_regNum_5 = f'{worker_reg_no}-5'
            fMember_regNum_6 = f'{worker_reg_no}-6'
            fMember_regNum_7 = f'{worker_reg_no}-7'
            fMember_regNum_8 = f'{worker_reg_no}-8'
            fMember_regNum_9 = f'{worker_reg_no}-9'
            fMember_regNum_10 = f'{worker_reg_no}-10'
            


            citizenship_detail = citizenship()
            citizenship_status = citizenship_detail['status']
            if citizenship_status == 'success':
                citizenship_data = citizenship_detail['citizenship']


           
            marital_detail = marital()
            marital_status = marital_detail['status']
            if marital_status == 'success':
                marital_data = marital_detail['marital']

           
            poe_detail = poe()
            poe_status = poe_detail['status']
            if poe_status == 'success':
                poe_data = poe_detail['poe']

           
            gender_detail = gender()
            gender_status = gender_detail['status']
            if gender_status == 'success':
                gender_data = gender_detail['gender']

            religion_detail = religion()
            religion_status = religion_detail['status']
            if religion_status == 'success':
                religion_data = religion_detail['religion']


           
            race_detail = race()
            race_status = race_detail['status']
            if race_status == 'success':
                race_data = race_detail['race']

            
            relationship_detail = relationship()
            relationship_status = relationship_detail['status']
            if relationship_status == 'success':
                relationship_data = relationship_detail['relationship']

            
            job_sector_detail = job_sector()
            job_sector_status = job_sector_detail['status']
            if job_sector_status == 'success':
                job_sector_data = job_sector_detail['job_sector']

           
            job_status_sponsor_detail = job_status_sponsor()
            job_status_sponsor_status = job_status_sponsor_detail['status']
            if job_status_sponsor_status == 'success':
                job_status_sponsor_data = job_status_sponsor_detail['job_status_sponsor']

           
            city_detail = city()
            city_status = city_detail['status']
            if city_status == 'success':
                city_data = city_detail['city']

            
            state_detail = state()
            state_status = state_detail['status']
            if state_status == 'success':
                state_data = state_detail['state']

            
            issuingCountry_detail = issuingCountry()
            issuingCountry_status = issuingCountry_detail['status']
            if issuingCountry_status == 'success':
                issuingCountry_data = issuingCountry_detail['issuingCountry']

           
            docStatus_detail = docStatus()
            docStatus_status = docStatus_detail['status']
            if docStatus_status == 'success':
                docStatus_data = docStatus_detail['docStatus']

           
            curDocStatus_detail = curDocStatus()
            curDocStatus_status = curDocStatus_detail['status']
            if curDocStatus_status == 'success':
                curDocStatus_data = curDocStatus_detail['curDocStatus']

            typeOfDoc_detail = typeOfDoc()
            typeOfDoc_status = typeOfDoc_detail['status']
            if typeOfDoc_status == 'success':
                typeOfDoc_data = typeOfDoc_detail['typeOfDoc']

           
            employment_status_detail = employment_status()
            employment_status_status = employment_status_detail['status']
            if employment_status_status == 'success':
                employment_status_data = employment_status_detail['employment_status']


            employment_detail = employmentDetail()
            get_employment_detail = employment_detail['status']
            if get_employment_detail == 'success':
                employment_detail_data = employment_detail['employment_detail']
            

            conn.commit()
            cur.close()

            return render_template('add-worker.html', branch_city=branch_city, branch_state=branch_state, fMember_regNum_1=fMember_regNum_1, fMember_regNum_2=fMember_regNum_2, fMember_regNum_3=fMember_regNum_3, fMember_regNum_4=fMember_regNum_4, fMember_regNum_5=fMember_regNum_5, fMember_regNum_6=fMember_regNum_6, fMember_regNum_7=fMember_regNum_7, fMember_regNum_8=fMember_regNum_8, fMember_regNum_9=fMember_regNum_9, fMember_regNum_10=fMember_regNum_10,  aps_contact_person=aps_contact_person, ip_address=ip_address, serverPort=serverPort, branch_address1=branch_address1, branch_address2=branch_address2, branch_address3=branch_address3, workerRegistrationNumber=worker_reg_no, citizenshipList=citizenship_data, maritialList=marital_data, poeList=poe_data, genderList=gender_data, religionList=religion_data, raceList=race_data, relationshipList=relationship_data, jobSectorList=job_sector_data, cityList=city_data, stateList=state_data, issuingCountryList=issuingCountry_data, docStatusList=docStatus_data, curDocStatusList=curDocStatus_data, typeOfDocList=typeOfDoc_data, employement_statusList=employment_status_data, jobStatusSponsorList = job_status_sponsor_data, employment_detail=employment_detail_data)
        else:
            return render_template('add-worker.html', profileC=0)    
    else:
        return redirect('/')
    
# For add worker >> sub sector
@app.route("/add-worker-sub-sector", methods=['GET', 'POST'])
def addWorker_subSector():
    if 'user_session' in session:
        sector = request.form.get('job_sector')
        # check profile data
        conn = get_db_connection()
        cur = conn.cursor()
        # for Date & time
        currentDate = datetime.now()
        cYear = currentDate.strftime("%y")

        cur.execute("SELECT job_sub_sector FROM detailed_dd_job_sub_sector where job_sector=?", (sector,))
        job_sub_sector = cur.fetchall()
        return jsonify(job_sub_sector)
    else:
        return redirect('/')
# End For add worker >> sub sector


# Submit Worker 2nd
# Save Worker
'''
@app.route("/insertWorker", methods=['POST'])
def insertWorker():
    conn = get_db_connection()
    cur = conn.cursor()

    active_user_session = session.get('user_session')

    form_date = datetime.now().strftime('%d%m%Y')
    form_rand = random.randrange(10000, 99999)
    form_unique_key = 'DT'+form_date+'N'+str(form_rand)

    form_time = datetime.now().strftime('%H:%M:%S')
    
    if 'user_session' in session:
        if request.method == 'POST':
            try:
                data = request.get_json()
    
                #print('All Data: ->', data)
                formStatus = data.get('status')
                workerD = data.get('workerData')
                docD = data.get('docData')
                fmData = data.get('familyMemberData')

                
                # Worker & Family
                if formStatus == 'workerOnly':
                    #print(formStatus)
                    
                    workerData = json.loads(workerD)
                    docData = json.loads(docD)

                    # Form Data 
                    for worker in workerData:
                        form_created_by = active_user_session
                        form_created_date = current_date
                        form_worker_reg_no = worker['awl_worker_registration_no']
                        no_family_mem = worker['no_of_family_member']
                        worker_detail_worker_legal_status = worker['awl_worker_legal_status']
                        worker_detail_name_of_worker = worker['awl_name_of_worker']
                        
                        worker_detail_family_name = worker['awl_family_name']
                        worker_detail_gender = worker['awl_gender']
                        worker_detail_DOB = worker['awl_d_o_b']
                        worker_detail_place_birth = worker['awl_place_of_birth']
                        worker_detail_citizenship = worker['awl_citizenship']
                        
                        worker_detail_marital_status = worker['awl_maritial_status']
                        worker_detail_poe = worker['awl_point_of_entry']
                        worker_detail_religion = worker['awl_religion']
                        worker_detail_race = worker['awl_race']
                        worker_detail_contact_no = worker['awl_worker_contact_no']
                        
                        worker_detail_email = worker['awl_worker_email']
                        worker_detail_nok = worker['awl_name_of_next_kin']
                        worker_detail_relationship = worker['awl_relationship']
                        worker_detail_nok_contact_no = worker['awl_nok_contact_no']
                        worker_emp_dtl_job_sector = worker['awl_job_sector']
                        
                        worker_emp_dtl_job_sub_sector = worker['awl_job_sub_sector']
                        worker_emp_dtl_emp_sponsorship_status = worker['awl_employement_sponsorship_status']
                        worker_emp_dtl_address1 = worker['awl_address1']
                        worker_emp_dtl_address2 = worker['awl_address2']
                        worker_emp_dtl_address3 = worker['awl_address3']
                        
                        worker_emp_dtl_postcode = 'postcode - static' #worker['']
                        worker_emp_dtl_city = worker['awl_city']
                        worker_emp_dtl_state = worker['awl_state']
                        worker_doc_dtl_doc_id = 'document_id-123456'
                        worker_doc_dtl_type_of_doc = 'type_of_documents'
                        
                        worker_doc_dtl_no_of_doc = 'static' #worker['']
                        worker_doc_dtl_images_path_email = 'static' # worker[)
                        worker_doc_dtl_place_of_issue = 'static' # worker['awl_place_of_issue']
                        worker_doc_dtl_issue_date = 'static' # worker['awl_document_issued_date']
                        worker_doc_dtl_expiry_date = 'static' # worker['awl_document_expiry_date']
                        
                        worker_doc_dtl_country_doc_issued =  'static' #worker['awl_issuing_country']
                        worker_doc_dtl_doc_status = 'static' # worker['awl_document_status']
                        worker_doc_dtl_doc_current_status ='static' #  worker['awl_status_of_current_document']
                        worker_doc_dtl_doc_no = 'static' 
                        form_position = 'static' 
                        
                        form_status = 'static' 
                    
                    # Find Last Key of Worker
                    cur.execute('SELECT MAX(worker_key) FROM half_form')
                    last_key = cur.fetchone()[0]

                    if last_key == None:
                        next_key = 1
                    else:
                        next_key = last_key + 1
                    #print('Last Key: ', last_key, 'Next Key: ', next_key)
                    

                    
                    # Worker Insert
                    cur.execute('INSERT INTO half_form (worker_key, form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, worker_doc_dtl_doc_id, worker_doc_dtl_type_of_doc, worker_doc_dtl_no_of_doc, worker_doc_dtl_images_path_email, worker_doc_dtl_place_of_issue, worker_doc_dtl_issue_date, worker_doc_dtl_expiry_date, worker_doc_dtl_country_doc_issued, worker_doc_dtl_doc_status, worker_doc_dtl_doc_current_status, worker_doc_dtl_doc_no, form_position, form_status, form_unique_key) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, worker_doc_dtl_doc_id, worker_doc_dtl_type_of_doc, worker_doc_dtl_no_of_doc, worker_doc_dtl_images_path_email, worker_doc_dtl_place_of_issue, worker_doc_dtl_issue_date, worker_doc_dtl_expiry_date, worker_doc_dtl_country_doc_issued, worker_doc_dtl_doc_status, worker_doc_dtl_doc_current_status, worker_doc_dtl_doc_no, form_position, form_status, form_unique_key))
                    
                    # Insert Worker Date & Time
                    cur.execute('INSERT INTO half_form_time (worker_reg_no, reg_date, reg_time) VALUES(?, ?, ?)', (form_worker_reg_no, current_date, form_time))
                    
                    # Insert Workers Document
                    for docs in docData:
                        document_link = docs['document_link']
                        type_of_documents = docs['type_of_documents']
                        document_id = docs['document_id']
                        place_of_issue = docs['place_of_issue']
                        document_issued_date = docs['document_issued_date']
                        document_expiry_date = docs['document_expiry_date']
                        issuing_country = docs['issuing_country']
                        document_status = docs['document_status']
                        status_of_current_document = docs['status_of_current_document']
                    
                        #query
                        cur.execute('INSERT INTO workers_document (worker_key, document_link, type_of_douments, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document, form_unique_key) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, document_link, type_of_documents, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document, form_unique_key))
                    # End Insert Workers Document
                    
                elif formStatus == 'workerWithFamily':
                    #print(formStatus)
                    # Worker & Family
                
                    # JSON to Obj
                    workerData = json.loads(workerD)
                    docData = json.loads(docD)
                    familyMemberData = json.loads(fmData)
                    
                    # Form Data
                    for worker in workerData:
                        form_created_by = active_user_session
                        form_created_date = current_date
                        form_worker_reg_no = worker['awl_worker_registration_no']
                        no_family_mem = worker['no_of_family_member']
                        worker_detail_worker_legal_status = worker['awl_worker_legal_status']
                        worker_detail_name_of_worker = worker['awl_name_of_worker']
                        
                        worker_detail_family_name = worker['awl_family_name']
                        worker_detail_gender = worker['awl_gender']
                        worker_detail_DOB = worker['awl_d_o_b']
                        worker_detail_place_birth = worker['awl_place_of_birth']
                        worker_detail_citizenship = worker['awl_citizenship']
                        
                        worker_detail_marital_status = worker['awl_maritial_status']
                        worker_detail_poe = worker['awl_point_of_entry']
                        worker_detail_religion = worker['awl_religion']
                        worker_detail_race = worker['awl_race']
                        worker_detail_contact_no = worker['awl_worker_contact_no']
                        
                        worker_detail_email = worker['awl_worker_email']
                        worker_detail_nok = worker['awl_name_of_next_kin']
                        worker_detail_relationship = worker['awl_relationship']
                        worker_detail_nok_contact_no = worker['awl_nok_contact_no']
                        worker_emp_dtl_job_sector = worker['awl_job_sector']
                        
                        worker_emp_dtl_job_sub_sector = worker['awl_job_sub_sector']
                        worker_emp_dtl_emp_sponsorship_status = worker['awl_employement_sponsorship_status']
                        worker_emp_dtl_address1 = worker['awl_address1']
                        worker_emp_dtl_address2 = worker['awl_address2']
                        worker_emp_dtl_address3 = worker['awl_address3']
                        
                        worker_emp_dtl_postcode = 'postcode - static' #worker['']
                        worker_emp_dtl_city = worker['awl_city']
                        worker_emp_dtl_state = worker['awl_state']
                        worker_doc_dtl_doc_id = 'document_id-123456'
                        worker_doc_dtl_type_of_doc = 'type_of_documents'
                        
                        worker_doc_dtl_no_of_doc = 'static' #worker['']
                        worker_doc_dtl_images_path_email = 'static' # worker[)
                        worker_doc_dtl_place_of_issue = 'static' # worker['awl_place_of_issue']
                        worker_doc_dtl_issue_date = 'static' # worker['awl_document_issued_date']
                        worker_doc_dtl_expiry_date = 'static' # worker['awl_document_expiry_date']
                        
                        worker_doc_dtl_country_doc_issued =  'static' #worker['awl_issuing_country']
                        worker_doc_dtl_doc_status = 'static' # worker['awl_document_status']
                        worker_doc_dtl_doc_current_status ='static' #  worker['awl_status_of_current_document']
                        worker_doc_dtl_doc_no = 'static' 
                        form_position = 'static' 
                        
                        form_status = 'static' 
                        
                    
                    # Find Last Key of Worker
                    cur.execute('SELECT MAX(worker_key) FROM half_form')
                    last_key = cur.fetchone()[0]
                    
                    if last_key == None:
                        next_key = 1
                    else:
                        next_key = last_key + 1
                    #print('Last Key: ', last_key, 'Next Key: ', next_key)
                    
                    
                    # Worker Insert
                    cur.execute('INSERT INTO half_form (worker_key, form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, worker_doc_dtl_doc_id, worker_doc_dtl_type_of_doc, worker_doc_dtl_no_of_doc, worker_doc_dtl_images_path_email, worker_doc_dtl_place_of_issue, worker_doc_dtl_issue_date, worker_doc_dtl_expiry_date, worker_doc_dtl_country_doc_issued, worker_doc_dtl_doc_status, worker_doc_dtl_doc_current_status, worker_doc_dtl_doc_no, form_position, form_status, form_unique_key) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, worker_doc_dtl_doc_id, worker_doc_dtl_type_of_doc, worker_doc_dtl_no_of_doc, worker_doc_dtl_images_path_email, worker_doc_dtl_place_of_issue, worker_doc_dtl_issue_date, worker_doc_dtl_expiry_date, worker_doc_dtl_country_doc_issued, worker_doc_dtl_doc_status, worker_doc_dtl_doc_current_status, worker_doc_dtl_doc_no, form_position, form_status, form_unique_key))
                    
                    # Insert Worker Date & Time
                    cur.execute('INSERT INTO half_form_time (worker_reg_no, reg_date, reg_time) VALUES(?, ?, ?)', (form_worker_reg_no, current_date, form_time))
                    
                    # Insert Workers Document
                    for docs in docData:
                        document_link = docs['document_link']
                        type_of_documents = docs['type_of_documents']
                        document_id = docs['document_id']
                        place_of_issue = docs['place_of_issue']
                        document_issued_date = docs['document_issued_date']
                        document_expiry_date = docs['document_expiry_date']
                        issuing_country = docs['issuing_country']
                        document_status = docs['document_status']
                        status_of_current_document = docs['status_of_current_document']
                    
                        #query
                        cur.execute('INSERT INTO workers_document (worker_key, document_link, type_of_douments, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document, form_unique_key) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, document_link, type_of_documents, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document, form_unique_key))
                    # End Insert Workers Document
                    
                    # Insert Worker Family
                    for fmD in familyMemberData:
                        fm_worker_registration_no = fmD['fm_worker_registration_no']
                        fm_worker_name = fmD['fm_worker_name']
                        fm_relationship = fmD['fm_relationship']
                        fm_name_of_family_member = fmD['fm_name_of_family_member']
                        fm_family_name = fmD['fm_family_name']
                        fm_is_family_member_together = fmD['fm_is_family_member_together']
                        fm_point_of_entry = fmD['fm_point_of_entry']
                        fm_citizenship = fmD['fm_citizenship']
                        fm_religion = fmD['fm_religion']
                        fm_marital_status = fmD['fm_marital_status']
                        fm_gender = fmD['fm_gender']
                        fm_address1 = fmD['fm_address1']
                        fm_address2 = fmD['fm_address2']
                        fm_address3 = fmD['fm_address3']
                        fm_postcode = fmD['fm_postcode']
                        fm_city = fmD['fm_city']
                        fm_state = fmD['fm_state']
                        fm_contact_no = fmD['fm_contact_no']
                        fm_race = fmD['fm_race']
                        fm_place_of_birth = fmD['fm_place_of_birth']
                        fm_dob = fmD['fm_dob']
                        fm_employment_status = fmD['fm_employment_status']
                        fm_same_employer_as_worker = fmD['fm_same_employer_as_worker']
                        fm_employer_name = fmD['fm_employer_name']
                        fm_employer_address = fmD['fm_employer_address']

                        fmDoc1_type_of_documents = fmD['fmDoc1_type_of_documents']
                        fmDoc1_document_id = fmD['fmDoc1_document_id']
                        fmDoc1_place_of_issue = fmD['fmDoc1_place_of_issue']
                        fmDoc1_document_issued_date = fmD['fmDoc1_document_issued_date']
                        fmDoc1_document_expiry_date = fmD['fmDoc1_document_expiry_date']
                        fmDoc1_issuing_country = fmD['fmDoc1_issuing_country']
                        fmDoc1_document_status = fmD['fmDoc1_document_status']
                        fmDoc1_status_of_current_document = fmD['fmDoc1_status_of_current_document']

                        fmDoc2_type_of_documents = fmD['fmDoc2_type_of_documents']
                        fmDoc2_document_id = fmD['fmDoc2_document_id']
                        fmDoc2_place_of_issue = fmD['fmDoc2_place_of_issue']
                        fmDoc2_document_issued_date = fmD['fmDoc2_document_issued_date']
                        fmDoc2_document_expiry_date = fmD['fmDoc2_document_expiry_date']
                        fmDoc2_issuing_country = fmD['fmDoc2_issuing_country']
                        fmDoc2_document_status = fmD['fmDoc2_document_status']
                        fmDoc2_status_of_current_document = fmD['fmDoc2_status_of_current_document']
                        
                        # fmData Query
                        cur.execute('INSERT INTO family_form (worker_key, form_created_by, form_created_date, form_unique_key, form_family_reg_no, family_form_worker_name, family_form_relationship, family_form_name_of_family_member, family_form_family_name, family_form_is_famliy_togther, family_form_family_form_poe, family_form_citizenship, family_form_religion,family_form_marital_status, family_form_gender, family_form_address1, family_form_address2, family_form_address3, family_form_postcode, family_form_city, family_form_state, family_form_contact_no, family_form_race, family_form_place_of_birth, family_form_emp_status, family_form_emp_name, family_form_emp_address, family_form_doc_path_email, family_form_doc_image_no, fmDoc1_type_of_documents, fmDoc1_document_id, fmDoc1_place_of_issue, fmDoc1_document_issued_date, fmDoc1_document_expiry_date, fmDoc1_issuing_country, fmDoc1_document_status, fmDoc1_status_of_current_document, fmDoc2_type_of_documents, fmDoc2_document_id, fmDoc2_place_of_issue, fmDoc2_document_issued_date, fmDoc2_document_expiry_date, fmDoc2_issuing_country, fmDoc2_document_status, fmDoc2_status_of_current_document) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, form_created_by, current_date, form_unique_key, fm_worker_registration_no, fm_worker_name, fm_relationship, fm_name_of_family_member, fm_family_name, fm_is_family_member_together, fm_point_of_entry, fm_citizenship, fm_religion, fm_marital_status, fm_gender, fm_address1, fm_address2, fm_address3, fm_postcode, fm_city, fm_state, fm_contact_no, fm_race, fm_place_of_birth, fm_employment_status, fm_employer_name, fm_employer_address, 'static email', 'doc image- static', fmDoc1_type_of_documents, fmDoc1_document_id, fmDoc1_place_of_issue, fmDoc1_document_issued_date, fmDoc1_document_expiry_date, fmDoc1_issuing_country, fmDoc1_document_status, fmDoc1_status_of_current_document, fmDoc2_type_of_documents, fmDoc2_document_id, fmDoc2_place_of_issue, fmDoc2_document_issued_date, fmDoc2_document_expiry_date, fmDoc2_issuing_country, fmDoc2_document_status, fmDoc2_status_of_current_document))
                        
                    # End Insert Worker Family
                    
        
                conn.commit()
                cur.close()
               
                #print('success')
                return jsonify({'status': 'success'})
            
            except Exception as e:    
                #print('Insert Worker Error: ', str(e))
                return jsonify({'status': 'failure'})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid request method'})
    else:
        return jsonify({'status': 'error', 'message': 'User not logged in'})

# Save Worker
@app.route("/insertWorker", methods=['POST'])
def insertWorker():
    conn = get_db_connection()
    cur = conn.cursor()
    
    active_user_session = session.get('user_session')

    form_date = datetime.now().strftime('%d%m%Y')
    form_rand = random.randrange(10000, 99999)
    form_unique_key = 'DT'+form_date+'N'+str(form_rand)

    form_time = datetime.now().strftime('%H:%M:%S')
    
    if 'user_session' in session:
        if request.method == 'POST':
            try:
                data = request.get_json()
    
                print('All Data: ->', data)

                
                for ddd in data:
                    print(ddd)


                formStatus = data.get('status')
                workerD = data.get('workerData')
                docD = data.get('docData')
                fmData = data.get('familyMemberData')
                fmDocs = data.get('familyMemberDocs')

                # Worker & Family
                if formStatus == 'workerOnly' or formStatus == 'workerWithFamily':
                    
                    workerData = json.loads(workerD)
                    docData = json.loads(docD)
                    familyMemberData = json.loads(fmData)
                    fm_doc_data = json.loads(fmDocs)

                    workerData_len = len(workerData)
                    docData_len = len(docData)
                    familyMemberData_len = len(familyMemberData)
                    fm_doc_data_len = len(fm_doc_data)

                    print('length of all: ', workerData_len, docData_len, familyMemberData_len, fm_doc_data_len)

                    # Form Data 
                    if workerData_len >= 1:
                        for worker in workerData:
                            form_created_by = active_user_session
                            form_created_date = current_date
                            form_worker_reg_no = worker['awl_worker_registration_no']
                            no_family_mem = worker['no_of_family_member']
                            worker_detail_worker_legal_status = worker['awl_worker_legal_status']
                            worker_detail_name_of_worker = worker['awl_name_of_worker']
                            
                            worker_detail_family_name = worker['awl_family_name']
                            worker_detail_gender = worker['awl_gender']
                            worker_detail_DOB = worker['awl_d_o_b']
                            worker_detail_place_birth = worker['awl_place_of_birth']
                            worker_detail_citizenship = worker['awl_citizenship']
                            
                            worker_detail_marital_status = worker['awl_maritial_status']
                            worker_detail_poe = worker['awl_point_of_entry']
                            worker_detail_religion = worker['awl_religion']
                            worker_detail_race = worker['awl_race']
                            worker_detail_contact_no = worker['awl_worker_contact_no']
                            
                            worker_detail_email = worker['awl_worker_email']
                            worker_detail_nok = worker['awl_name_of_next_kin']
                            worker_detail_relationship = worker['awl_relationship']
                            worker_detail_nok_contact_no = worker['awl_nok_contact_no']
                            worker_emp_dtl_job_sector = worker['awl_job_sector']
                            
                            worker_emp_dtl_job_sub_sector = worker['awl_job_sub_sector']
                            worker_emp_dtl_emp_sponsorship_status = worker['awl_employement_sponsorship_status']
                            worker_emp_dtl_address1 = worker['awl_address1']
                            worker_emp_dtl_address2 = worker['awl_address2']
                            worker_emp_dtl_address3 = worker['awl_address3']
                            
                            worker_emp_dtl_postcode = 'postcode - static' #worker['']
                            worker_emp_dtl_city = worker['awl_city']
                            worker_emp_dtl_state = worker['awl_state']
                            form_position = 'static' 
                            form_status = 'static' 
                        
                        # Find Last Key of Worker
                        cur.execute('SELECT MAX(worker_key) FROM half_form')
                        last_key = cur.fetchone()[0]

                        if last_key == None:
                            next_key = 1
                        else:
                            next_key = last_key + 1
                        #print('Last Key: ', last_key, 'Next Key: ', next_key)
                    

                    
                        # Worker Insert
                        cur.execute('INSERT INTO half_form (worker_key, form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, form_position, form_status, form_unique_key) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, form_position, form_status, form_unique_key))
                        
                        # Insert Worker Date & Time
                        cur.execute('INSERT INTO half_form_time (worker_reg_no, reg_date, reg_time) VALUES(?, ?, ?)', (form_worker_reg_no, current_date, form_time))
                        
                        # Update Worker Tracking
                        cur.execute('UPDATE reg_num_tracking SET status="complete" WHERE worker_reg_no=?', (form_worker_reg_no,))

                        # Insert Workers Document
                        for docs in docData:
                            document_link = docs['document_link']
                            type_of_documents = docs['type_of_documents']
                            document_id = docs['document_id']
                            place_of_issue = docs['place_of_issue']
                            document_issued_date = docs['document_issued_date']
                            document_expiry_date = docs['document_expiry_date']
                            issuing_country = docs['issuing_country']
                            document_status = docs['document_status']
                            status_of_current_document = docs['status_of_current_document']

                            # Check Worker Docs
                            cur.execute('SELECT id FROM workers_document WHERE document_link=? AND worker_reg_no=?', (document_link, form_worker_reg_no))
                            q_wDocs = cur.fetchall()
                            q_wDocs_len = len(q_wDocs)
                            if q_wDocs_len == 0:
                                #query
                                cur.execute('INSERT INTO workers_document (worker_key, document_link, type_of_douments, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document, form_unique_key, worker_reg_no) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, document_link, type_of_documents, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document, form_unique_key, form_worker_reg_no))
                            elif q_wDocs_len == 1:
                                #query
                                cur.execute('UPDATE workers_document SET worker_key=?, type_of_douments=?, document_id=?, place_of_issue=?, document_issued_date=?, document_expiry_date=?, issuing_country=?, document_status=?, status_of_current_document=?, form_unique_key=? WHERE document_link=? AND worker_reg_no=?', (next_key, type_of_documents, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document, form_unique_key, document_link, form_worker_reg_no))
                        # End Insert Workers Document

                
                   
                    
                        # Insert Worker Family  
                        for fmD in familyMemberData:
                            fm_worker_registration_no = fmD['fm_worker_registration_no']
                            fm_worker_name = fmD['fm_worker_name']
                            fm_relationship = fmD['fm_relationship']
                            fm_name_of_family_member = fmD['fm_name_of_family_member']
                            fm_family_name = fmD['fm_family_name']
                            fm_is_family_member_together = fmD['fm_is_family_member_together']
                            fm_point_of_entry = fmD['fm_point_of_entry']
                            fm_citizenship = fmD['fm_citizenship']
                            fm_religion = fmD['fm_religion']
                            fm_marital_status = fmD['fm_marital_status']
                            fm_gender = fmD['fm_gender']
                            fm_address1 = fmD['fm_address1']
                            fm_address2 = fmD['fm_address2']
                            fm_address3 = fmD['fm_address3']
                            fm_postcode = fmD['fm_postcode']
                            fm_city = fmD['fm_city']
                            fm_state = fmD['fm_state']
                            fm_contact_no = fmD['fm_contact_no']
                            fm_race = fmD['fm_race']
                            fm_place_of_birth = fmD['fm_place_of_birth']
                            fm_dob = fmD['fm_dob']
                            fm_employment_status = fmD['fm_employment_status']
                            fm_same_employer_as_worker = fmD['fm_same_employer_as_worker']
                            fm_employer_name = fmD['fm_employer_name']
                            fm_employer_address = fmD['fm_employer_address']
                            # fmData Query
                            cur.execute('INSERT INTO family_form (worker_key, form_created_by, form_created_date, form_unique_key, form_family_reg_no, family_form_worker_name, family_form_relationship, family_form_name_of_family_member, family_form_family_name, family_form_is_famliy_togther, family_form_family_form_poe, family_form_citizenship, family_form_religion,family_form_marital_status, family_form_gender, family_form_address1, family_form_address2, family_form_address3, family_form_postcode, family_form_city, family_form_state, family_form_contact_no, family_form_race, family_form_place_of_birth, family_form_emp_status, family_form_emp_name, family_form_emp_address, family_form_doc_path_email, family_form_doc_image_no) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, form_created_by, current_date, form_unique_key, fm_worker_registration_no, fm_worker_name, fm_relationship, fm_name_of_family_member, fm_family_name, fm_is_family_member_together, fm_point_of_entry, fm_citizenship, fm_religion, fm_marital_status, fm_gender, fm_address1, fm_address2, fm_address3, fm_postcode, fm_city, fm_state, fm_contact_no, fm_race, fm_place_of_birth, fm_employment_status, fm_employer_name, fm_employer_address, 'static email', 'doc image- static'))
                        # End Insert Worker Family

                        # Insert FM documents
                        for fmD in fm_doc_data:
                            document_link = fmD['document_link']
                            type_of_documents = fmD['type_of_documents']
                            document_id = fmD['document_id']
                            place_of_issue = fmD['place_of_issue']
                            document_issued_date = fmD['document_issued_date']
                            document_expiry_date = fmD['document_expiry_date']
                            issuing_country = fmD['issuing_country']
                            document_status = fmD['document_status']
                            status_of_current_document = fmD['status_of_current_document']
                            fm_reg_no = fmD['fm_reg_no']
                        
                            # Check Worker Docs
                            cur.execute('SELECT id FROM fm_document WHERE document_link=? AND fm_reg_no=?', (document_link, fm_reg_no))
                            q_wDocs = cur.fetchall()
                            q_wDocs_len = len(q_wDocs)
                            if q_wDocs_len == 0:
                                #query
                                cur.execute('INSERT INTO fm_document (worker_key, document_link, type_of_douments, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document, form_unique_key, fm_reg_no) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, document_link, type_of_documents, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document, form_unique_key, fm_reg_no))
                            elif q_wDocs_len == 1:
                                #query
                                cur.execute('UPDATE fm_document SET worker_key=?, type_of_douments=?, document_id=?, place_of_issue=?, document_issued_date=?, document_expiry_date=?, issuing_country=?, document_status=?, status_of_current_document=?, form_unique_key=? WHERE document_link=? AND fm_reg_no=?', (next_key, type_of_documents, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document, form_unique_key, document_link, fm_reg_no))
                        # End * Insert Worker Family
                 
                    conn.commit()
                    cur.close()
                    return jsonify({'status': 'success'})
                else:
                    return jsonify({'status': 'Data not found!'})
            
            except Exception as e:    
                print('Insert Worker Error: ', str(e))
                return jsonify({'status': 'failure'})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid request method'})
    else:
        return jsonify({'status': 'error', 'message': 'access denied'})
    
# End Submit Worker 2nd
'''


# Save Worker
@app.route("/insertWorker", methods=['POST'])
def insertWorker():
    if 'user_session' in session:
        if request.method == 'POST':
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                active_user_session = session.get('user_session')

                data = request.get_json()
                
                result = sendWorkerData(active_user_session, data)
                
                if result == 'connection_lost':
                    return 'connection_lost'
                elif result == 'error':
                    return 'error'
                elif result['status'] == 'success':
                    return jsonify({'status': 'success'})
                else:
                    print(result)
                    return jsonify({'status': 'failure'})    
            except Exception as e:    
                print('Insert Worker Error: ', str(e))
                return jsonify({'status': 'failure'})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid request'})
    else:
        return jsonify({'status': 'error', 'message': 'access denied'})
    
# End Submit Worker 2nd



# Worker & Family Member Folder Creation
@app.route("/worker-fm-folderCreator", methods=['GET', 'POST'])
def worker_fm_folderCreator():
    if 'user_session' in session:
        if(request.method == 'POST'):
            active_user_session = session.get('user_session')

            folderData = request.get_json()
            worker_registration_folder_name = folderData.get('worker_registration_folder_name')
            
            fMember_prefix = folderData.get('fMember_prefix')
            fm_last_ID = folderData.get('fm_last_ID')
            total_fMember = folderData.get('total_fMember')
            
            # Final Family member registration number 
            userRoot = active_user_session + 'Docs'
            folderCreator(userRoot, worker_registration_folder_name, 'legal', fMember_prefix, fm_last_ID, total_fMember)
            return ({"status":"success"})
            
            
            


# Set number of Family member
@app.route("/number-of-family-member", methods=['GET', 'POST'])
def setFamilyMember():
    if 'user_session' in session:
        if(request.method == 'POST'):
            family_member = request.form.get('family_member_number', type=int)
            session['family_member'] = family_member
            return redirect('/add-worker')

    
# Profile    
@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if 'user_session' in session:
        try:
            active_user_session = session.get('user_session')
            conn = get_db_connection()
            cur = conn.cursor()
            
            name = None
            email = None
            password = None

            profile = staffProfile(active_user_session)
            status = profile['status']

            if status == 'success':
                profile_data = profile['profile']
                name = profile_data[0][1]
                email = profile_data[0][2]
                password = profile_data[0][3]
        
            return render_template('profile.html', name=name, password=password, email=email)
        except Exception as e:
            return redirect('/')
    else:
        return redirect('/')
    

# Profile Form Data
@app.route("/profile-form-data", methods=['POST'])
def profileFormData():
    if 'user_session' in session:
        #Get DB
        conn = get_db_connection()
        cur = conn.cursor()

        active_user_session = session.get('user_session')
        cur.execute("SELECT * FROM profile WHERE aps_email=?", (active_user_session,))
        checkPro = cur.fetchall()
        checkPro = len(checkPro)
        
        if(checkPro == 1):
           session['profile_completed'] = 'profile completed'
           return redirect('/profile')   
        else:
            if request.method == 'POST':
                try:
                    # APS Data

                    aps_agency_pekerjaan = request.form.get('aps_agency_pekerjaan')
                    aps_license_category = request.form.get('aps_license_category')
                    aps_postcode = request.form.get('aps_postcode')
                    aps_office_telephone_no = request.form.get('aps_office_telephone_no')
                    aps_new_ssm_number = request.form.get('aps_new_ssm_number')
                    aps_address1 = request.form.get('aps_address1')
                    aps_city = request.form.get('aps_city')
                    aps_mobile_number = request.form.get('aps_mobile_number')
                    aps_old_ssm_number = request.form.get('aps_old_ssm_number')
                    aps_address2 = request.form.get('aps_address2')
                    aps_state = request.form.get('aps_state')
                    aps_email = request.form.get('aps_email')
                    aps_license_no = request.form.get('aps_license_no')
                    aps_address3 = request.form.get('aps_address3')
                    aps_license_exp_date = request.form.get('aps_license_exp_date')
                    aps_contact_person = request.form.get('aps_contact_person')
                    
                    # Employer Data
                    employer_company_name = request.form.get('employer_company_name')
                    employer_new_ssm_number = request.form.get('employer_new_ssm_number')
                    employer_old_ssm_number = request.form.get('employer_old_ssm_number')
                    employer_address1 = request.form.get('employer_address1')
                    employer_address2 = request.form.get('employer_address2')
                    employer_address3 = request.form.get('employer_address3')
                    employer_postcode = request.form.get('employer_postcode')
                    employer_city = request.form.get('employer_city')
                    employer_state = request.form.get('employer_state')
                    employer_office_telephone_no = request.form.get('employer_office_telephone_no')
                    employer_mobile_no = request.form.get('employer_mobile_no')
                    employer_fax_number = request.form.get('employer_fax_number')
                    employer_year_of_commence = request.form.get('employer_year_of_commence')
                    employer_sector = request.form.get('employer_sector')
                    employer_name_of_person_in_charge = request.form.get('employer_name_of_person_in_charge')
                    employer_designation = request.form.get('employer_designation')
                    employer_pic_mobile_number = request.form.get('employer_pic_mobile_number')
                    
                    # Branch Location Data
                    branch_employment_location_name = request.form.get('branch_employment_location_name')
                    branch_address1 = request.form.get('branch_address1')
                    branch_address2 = request.form.get('branch_address2')
                    branch_address3 = request.form.get('branch_address3')
                    branch_postcode = request.form.get('branch_postcode')
                    branch_state = request.form.get('branch_state')
                    branch_city = request.form.get('branch_city')
                    branch_office_telephone_number = request.form.get('branch_office_telephone_number')
                    branch_office_mobile_number = 'none'
                    branch_email = request.form.get('branch_email')
                    branch_name_of_person_in_charge = request.form.get('branch_name_of_person_in_charge')
                    branch_designation = request.form.get('branch_designation')
                    branch_pic_mobile_number = request.form.get('branch_pic_mobile_number')
                    
                    cur.execute('INSERT INTO profile(aps_agency_pekerjaan, aps_license_category, aps_postcode, aps_office_telephone_no, aps_new_ssm_number, aps_address1, aps_city, aps_mobile_number, aps_old_ssm_number, aps_address2, aps_state, aps_email, aps_license_no, aps_address3, aps_license_exp_date, aps_contact_person, employer_company_name, employer_new_ssm_number, employer_old_ssm_number, employer_address1, employer_address2, employer_address3, employer_postcode, employer_city, employer_state, employer_office_telephone_no, employer_mobile_no, employer_fax_number, employer_year_of_commence, employer_sector, employer_name_of_person_in_charge, employer_designation, employer_pic_mobile_number, branch_employment_location_name, branch_address1, branch_address2, branch_address3, branch_postcode, branch_state, branch_city, branch_office_telephone_number, branch_office_mobile_number, branch_email, branch_name_of_person_in_charge, branch_designation, branch_pic_mobile_number) VALUES("'+aps_agency_pekerjaan+'", "'+aps_license_category+'", "'+aps_postcode+'", "'+aps_office_telephone_no+'", "'+aps_new_ssm_number+'", "'+aps_address1+'", "'+aps_city+'", "'+aps_mobile_number+'", "'+aps_old_ssm_number+'", "'+aps_address2+'", "'+aps_state+'", "'+aps_email+'", "'+aps_license_no+'", "'+aps_address3+'", "'+aps_license_exp_date+'", "'+aps_contact_person+'", "'+employer_company_name+'", "'+employer_new_ssm_number+'", "'+employer_old_ssm_number+'", "'+employer_address1+'", "'+employer_address2+'", "'+employer_address3+'", "'+employer_postcode+'", "'+employer_city+'", "'+employer_state+'", "'+employer_office_telephone_no+'", "'+employer_mobile_no+'", "'+employer_fax_number+'", "'+employer_year_of_commence+'", "'+employer_sector+'", "'+employer_name_of_person_in_charge+'", "'+employer_designation+'", "'+employer_pic_mobile_number+'", "'+branch_employment_location_name+'", "'+branch_address1+'", "'+branch_address2+'", "'+branch_address3+'", "'+branch_postcode+'", "'+branch_state+'", "'+branch_city+'", "'+branch_office_telephone_number+'", "'+branch_office_mobile_number+'", "'+branch_email+'", "'+branch_name_of_person_in_charge+'", "'+branch_designation+'", "'+branch_pic_mobile_number+'")')
                    conn.commit()
                    conn.close()  
                    session['profile_success'] = 'success'
                    return redirect('/profile') 
                except Exception as e:
                    #print(e)
                    session['profile_error'] = 'error'
                    return redirect('/profile')
        # end the profile check
    else:
        return redirect('/')


# Profile    
@app.route("/edit-profile", methods=['GET', 'POST'])
def editProfile():
    if 'user_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()

        active_user_session = session.get('user_session')

        cur.execute("SELECT * FROM profile WHERE aps_email=?", (active_user_session,))
        checkPro = cur.fetchall()
        checkPro = len(checkPro)
        
        if(checkPro == 0):
           session['profile_empty'] = 'profile empty'
           return redirect('/profile')
        

        cur.execute("SELECT * FROM profile WHERE aps_email=?", (active_user_session,))
        profile = cur.fetchall()
        
        # for the license category
        cur.execute("SELECT license_list FROM detailed_dd_license_category")
        licenseCategory = cur.fetchall()

        # for the city
        cur.execute("SELECT city FROM detailed_dd_city")
        city = cur.fetchall()

        # for the state 
        cur.execute("SELECT state FROM detailed_dd_state")
        state = cur.fetchall()

        # for the sector 
        cur.execute("SELECT job_sector FROM detailed_dd_job_sector")
        sector = cur.fetchall()

         # for the designation 
        cur.execute("SELECT designation FROM detailed_dd_designation")
        designation = cur.fetchall()
        
        return render_template('edit-profile.html', profileData = profile, licenseCategoryList=licenseCategory, cityList=city, stateList=state, sectorList=sector, designationList=designation)
    else:
        return redirect('/')
    

# Edit Profile Form Data
@app.route("/edit-profile-form-data", methods=['GET', 'POST'])
def editProfileFormData():
    if 'user_session' in session:
        if request.method == 'POST':
            try:
                # APS Data
                active_user_session = session.get('user_session')
                
                profile_id = request.form.get('profile_id')

                aps_agency_pekerjaan = request.form.get('aps_agency_pekerjaan')
                aps_license_category = request.form.get('aps_license_category')
                aps_postcode = request.form.get('aps_postcode')
                aps_office_telephone_no = request.form.get('aps_office_telephone_no')
                aps_new_ssm_number = request.form.get('aps_new_ssm_number')
                aps_address1 = request.form.get('aps_address1')
                aps_city = request.form.get('aps_city')
                aps_mobile_number = request.form.get('aps_mobile_number')
                aps_old_ssm_number = request.form.get('aps_old_ssm_number')
                aps_address2 = request.form.get('aps_address2')
                aps_state = request.form.get('aps_state')
                #aps_email = request.form.get('aps_email')
                aps_license_no = request.form.get('aps_license_no')
                aps_address3 = request.form.get('aps_address3')
                aps_license_exp_date = request.form.get('aps_license_exp_date')
                aps_contact_person = request.form.get('aps_contact_person')
                
                # Employer Data
                employer_company_name = request.form.get('employer_company_name')
                employer_new_ssm_number = request.form.get('employer_new_ssm_number')
                employer_old_ssm_number = request.form.get('employer_old_ssm_number')
                employer_address1 = request.form.get('employer_address1')
                employer_address2 = request.form.get('employer_address2')
                employer_address3 = request.form.get('employer_address3')
                employer_postcode = request.form.get('employer_postcode')
                employer_city = request.form.get('employer_city')
                employer_state = request.form.get('employer_state')
                employer_office_telephone_no = request.form.get('employer_office_telephone_no')
                employer_mobile_no = request.form.get('employer_mobile_no')
                employer_fax_number = request.form.get('employer_fax_number')
                employer_year_of_commence = request.form.get('employer_year_of_commence')
                employer_sector = request.form.get('employer_sector')
                employer_name_of_person_in_charge = request.form.get('employer_name_of_person_in_charge')
                employer_designation = request.form.get('employer_designation')
                employer_pic_mobile_number = request.form.get('employer_pic_mobile_number')
                
                # Branch Location Data
                branch_employment_location_name = request.form.get('branch_employment_location_name')
                branch_address1 = request.form.get('branch_address1')
                branch_address2 = request.form.get('branch_address2')
                branch_address3 = request.form.get('branch_address3')
                branch_postcode = request.form.get('branch_postcode')
                branch_state = request.form.get('branch_state')
                branch_city = request.form.get('branch_city')
                branch_office_telephone_number = request.form.get('branch_office_telephone_number')
                branch_office_mobile_number = request.form.get('branch_office_mobile_number')
                branch_email = request.form.get('branch_email')
                branch_name_of_person_in_charge = request.form.get('branch_name_of_person_in_charge')
                branch_designation = request.form.get('branch_designation')
                branch_pic_mobile_number = request.form.get('branch_pic_mobile_number')
                
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute('UPDATE profile SET aps_agency_pekerjaan="'+aps_agency_pekerjaan+'", aps_license_category="'+aps_license_category+'", aps_postcode="'+aps_postcode+'", aps_office_telephone_no="'+aps_office_telephone_no+'", aps_new_ssm_number="'+aps_new_ssm_number+'", aps_address1="'+aps_address1+'", aps_city="'+aps_city+'", aps_mobile_number="'+aps_mobile_number+'", aps_old_ssm_number="'+aps_old_ssm_number+'", aps_address2="'+aps_address2+'", aps_state="'+aps_state+'", aps_license_no="'+aps_license_no+'", aps_address3="'+aps_address3+'", aps_license_exp_date="'+aps_license_exp_date+'", aps_contact_person="'+aps_contact_person+'", employer_company_name="'+employer_company_name+'", employer_new_ssm_number="'+employer_new_ssm_number+'", employer_old_ssm_number="'+employer_old_ssm_number+'", employer_address1="'+employer_address1+'", employer_address2="'+employer_address2+'", employer_address3="'+employer_address3+'", employer_postcode="'+employer_postcode+'", employer_city="'+employer_city+'", employer_state="'+employer_state+'", employer_office_telephone_no="'+employer_office_telephone_no+'", employer_mobile_no="'+employer_mobile_no+'", employer_fax_number="'+employer_fax_number+'", employer_year_of_commence="'+employer_year_of_commence+'", employer_sector="'+employer_sector+'", employer_name_of_person_in_charge="'+employer_name_of_person_in_charge+'", employer_designation="'+employer_designation+'", employer_pic_mobile_number="'+employer_pic_mobile_number+'", branch_employment_location_name="'+branch_employment_location_name+'", branch_address1="'+branch_address1+'", branch_address2="'+branch_address2+'", branch_address3="'+branch_address3+'", branch_postcode="'+branch_postcode+'", branch_state="'+branch_state+'", branch_city="'+branch_city+'", branch_office_telephone_number="'+branch_office_telephone_number+'", branch_office_mobile_number="'+branch_office_mobile_number+'", branch_email="'+branch_email+'", branch_name_of_person_in_charge="'+branch_name_of_person_in_charge+'", branch_designation="'+branch_designation+'", branch_pic_mobile_number="'+branch_pic_mobile_number+'" WHERE id="'+profile_id+'"')
                conn.commit()
                conn.close()  
                session['edit_profile_success'] = 'success'
                return redirect('/edit-profile') 
            except Exception as e:
                #print(e)
                session['edit_profile_error'] = 'error'
                return redirect('/edit-profile')
    else:
        return redirect('/')

# Upload Worker Avatar

@app.route("/upload-image", methods=['POST'])
def uploadAvatar():
    try:
        res = {}
        
        fPath = request.form.get('fPath')
        avatarPath = f'./static/documents/' + fPath
        avatar = request.form.get('avatar')
        
        #print('Resp: ', fPath, avatar)
        
        image_bytes = base64.b64decode(avatar)
        # Save the image to the upload folder
        image_path = os.path.join(avatarPath, 'uploaded_image.jpg')
        with open(image_path, 'wb') as f:
            f.write(image_bytes)
          
        res['status'] = 'success'    
        return (jsonify(res))
    except Exception as e:
        return str(e)


# Upload Worker Avatar
@app.route("/fetch-docs", methods=['POST'])
def fetchDocs():
    try:
        dirData = request.get_json()
        dirPath = dirData.get('dirPath')
        completePath = f"./static/documents/{dirPath}*"
        
        oldImages = glob.glob('./static/img/uploaded-image/legal1/*')
        
        image_paths = glob.glob(completePath)
        
        response = {
            'status': 'success',
            'imagePaths': image_paths
        }
        return jsonify(response)
    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }
        return jsonify(response)
    
    

# Document link image view
@app.route("/view-img", methods=['GET'])
def imgView():
    if 'user_session' in session:
        active_user_session = session.get('user_session')

        img = request.args.get('doc')
        return render_template('view-img.html', viewImg=img)
    


# Create Sub Users
@app.route("/create-sub-users", methods=['GET'])
def createSubUsers():
    if 'user_session' in session:
        return render_template('create-sub-users.html')
    else:
        return redirect('/') 
# End * Create Sub Users

# Insert Sub Users
@app.route('/insert-sub-users', methods=['POST'])
def insertSubUsers():
    if 'user_session' in session:
        try:
            active_user_session = session.get('user_session')

            name = request.form.get('name')
            username = request.form.get('email')
            password = request.form.get('password')
            creator = active_user_session
            # Date & Time
            creation_date = datetime.now().strftime('%d/%m/%Y')
            creation_time = datetime.now().strftime('%H:%M:%S')
            
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            # Check Admin
            admin = cur.execute('SELECT email FROM admin WHERE email=?', (username,))
            admin = cur.fetchall()
            adminLen = len(admin)
            if adminLen == 1:
                session['create_sub_users_status'] = 'user_exist'
                return redirect('/create-sub-users')


            # Check Users
            users = cur.execute('SELECT email FROM users WHERE email=?', (username,))
            users = cur.fetchall()
            userLen = len(users)
            if userLen == 1:
                session['create_sub_users_status'] = 'user_exist'
                return redirect('create-sub-users')

            # Check Sub Admin
            subAdmin = cur.execute('SELECT email FROM sub_admin WHERE email=?', (username,))
            subAdmin = cur.fetchall()
            subAdminLen = len(subAdmin)
            if subAdminLen == 1:
                session['create_sub_users_status'] = 'user_exist'
                return redirect('/create-sub-users')
            
            # Check Sub User
            subUser = cur.execute('SELECT username FROM sub_users WHERE username=?', (username,))
            subUser = cur.fetchall()
            subUserLen = len(subUser)
            if subUserLen == 1:
                session['create_sub_users_status'] = 'user_exist'
                return redirect('/create-sub-users')
            else:
                # Insert Insert Sub Users
                cur.execute("INSERT INTO sub_users(name, username, password, creator, creation_date, creation_time) VALUES(?, ?, ?, ?, ?, ?)", (name, username, password, creator, creation_date, creation_time))
                conn.commit()
                conn.close()
                session['create_sub_users_status'] = 'success'
                return redirect('/create-sub-users')
            
        except Exception as e:
                session['create_sub_users_status'] = 'error'
                return redirect('/create-sub-users')
    else:
        return redirect('/')


# View Sub Users
@app.route('/view-sub-users')
def viewSubUsers():
    if 'user_session' in session:
        try:
            active_user_session = session.get('user_session')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()
            # Check
            cur.execute('SELECT * FROM sub_users WHERE creator=?', (active_user_session,))
            subUsers = cur.fetchall()
            subUsersLen = len(subUsers)
            return render_template('/view-sub-users.html', subUsersList=subUsers, totalSubUsers=subUsersLen)
        
        except Exception as e:
            return redirect('/add-worker')
    else:
        return redirect('/')
    
# Del Sub Users
@app.route('/del-sub-users', methods=['GET'])
def delSubUsers():
    if 'user_session' in session:
        try:
            subUrs = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM sub_users WHERE id=?', (subUrs,))
            conn.commit()
            conn.close()
            session['del_sub_users_status'] = 'success'
            return redirect('/view-sub-users')
        except Exception as e:
            session['del_sub_users_status'] = 'error'
            return redirect('/view-sub-users')       
    else:
        return redirect('/') 


# Worker Registration List
@app.route("/registration-list", methods=['GET', 'POST'])
def registrationList():
    if 'user_session' in session:
        active_user_session = session.get('user_session')

        conn = get_db_connection()
        cur = conn.cursor()
        totalWorker = cur.execute("SELECT id, form_worker_reg_no, worker_detail_name_of_worker FROM half_form WHERE form_created_by=?", (active_user_session,))
        workerD = cur.fetchall()
        totalWorker = len(workerD)
        return render_template('registration-list.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')
    
# view-registered-worker
@app.route("/my-registration-list", methods=['GET', 'POST'])
def myRegistrationList():
    if 'user_session' in session:
        active_user_session = session.get('user_session')

        conn = get_db_connection()
        cur = conn.cursor()

        '''
        # Get form Unique Key 
        subUsers_form_unique_key_list = []
        subUser_q = cur.execute("SELECT form_unique_key FROM sub_users_datalog WHERE parent=?", (active_user_session,))
        form_unique_key = subUser_q.fetchall()

        for key in form_unique_key:
            subUsers_form_unique_key_list.append(key[0])

        form_unique_key_tuple = tuple(subUsers_form_unique_key_list)
        form_key_as_string = ', '.join(form_unique_key_tuple)

        placeholders = ', '.join(['?'] * len(form_unique_key_tuple))
        query = f'SELECT id, form_worker_reg_no, worker_detail_name_of_worker FROM half_form WHERE form_created_by=? AND form_unique_key NOT IN ({placeholders})'
        parameters = (active_user_session,) + form_unique_key_tuple
        # Execute the query
        cur.execute(query, parameters)
        workerD = cur.fetchall()
        totalWorker = len(workerD)

        #totalWorker = cur.execute("SELECT id, form_worker_reg_no, worker_detail_name_of_worker FROM half_form WHERE form_created_by=?", (active_user_session,))
        #workerD = cur.fetchall()
        #totalWorker = len(workerD)
        '''
        query = f'SELECT id, form_worker_reg_no, worker_detail_name_of_worker FROM half_form'
        
        # Execute the query
        cur.execute(query)
        workerD = cur.fetchall()
        totalWorker = len(workerD)
        return render_template('my-registration-list.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')
    

# view-registered-worker
@app.route("/staff-registration-list", methods=['GET', 'POST'])
def staffRegistrationList():
    if 'user_session' in session:
        try:
            active_user_session = session.get('user_session')
            conn = get_db_connection()
            cur = conn.cursor()

            result = staffWorkerList(active_user_session)
            print(result)
            result_status = None
            result_status = result['status']

            if result_status == 'success':
                totalWorker = len(result['worker_ls'])
                workerD = result['worker_ls']
                return render_template('staff-registration-list.html', workerList = workerD, totalForm=totalWorker)
            else:
                totalWorker = 0
                workerD = []
                return render_template('staff-registration-list.html', workerList = workerD, totalForm=totalWorker)
        except Exception as e:
            totalWorker = 0
            workerD = []
            return render_template('staff-registration-list.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')
    


    

#my-reg-subusers-list
@app.route("/my-reg-subusers-list", methods=['GET', 'POST'])
def myRegSubUsersList():
    if 'user_session' in session:
        try:
            active_user_session = session.get('user_session')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()
            # Check
            cur.execute('SELECT * FROM sub_users WHERE creator=?', (active_user_session,))
            subUsers = cur.fetchall()
            subUsersLen = len(subUsers)
            return render_template('/my-reg-subusers-list.html', subUsersList=subUsers, totalSubUsers=subUsersLen)
        
        except Exception as e:
            return redirect('/add-worker')
    else:
        return redirect('/') 
    

# subusers-registration-list
@app.route("/subusers-registration-list", methods=['GET', 'POST'])
def subUsersRegistrationList():
    if 'user_session' in session:
        try:
            active_user_session = session.get('user_session')

            creator = request.args.get('q')

            session['regList_path'] = creator

            conn = get_db_connection()
            cur = conn.cursor()


            # Get form Unique Key 
            subUsers_form_unique_key_list = []
            subUser_q = cur.execute("SELECT form_unique_key FROM sub_users_datalog WHERE creator=?", (creator,))
            form_unique_key = subUser_q.fetchall()

            for key in form_unique_key:
                subUsers_form_unique_key_list.append(key[0])

            form_unique_key_tuple = tuple(subUsers_form_unique_key_list)
            form_key_as_string = ', '.join(form_unique_key_tuple)

            placeholders = ', '.join(['?'] * len(form_unique_key_tuple))
            query = f'SELECT id, form_worker_reg_no, worker_detail_name_of_worker FROM half_form WHERE form_created_by=? AND form_unique_key IN ({placeholders})'
            parameters = (active_user_session,) + form_unique_key_tuple
            # Execute the query
            cur.execute(query, parameters)
            workerD = cur.fetchall()
            totalWorker = len(workerD)

            return render_template('subusers-registration-list.html',workerList = workerD, totalForm=totalWorker)
        except Exception as e:
            return redirect('/my-reg-subusers-list')
    else:
        return redirect('/')
    
    


# View Registered Worker
@app.route("/view-registered-worker", methods=['GET', 'POST'])
def viewRegisteredWorker():
    if 'user_session' in session:
        try:
            active_user_session = session.get('user_session')

            workerId = request.args.get('view-regWor')
            conn = get_db_connection()
            cur = conn.cursor()

            # fetch workers
            cur.execute("SELECT * FROM half_form WHERE id=? AND form_created_by=?", (workerId, active_user_session))
            workerD = cur.fetchall()
            form_unique_key = workerD[0][44]

            # get worker reg time
            worker_reg_no = workerD[0][4]
            cur.execute("SELECT reg_time FROM half_form_time WHERE worker_reg_no=?", (worker_reg_no,))
            workerRegNo = cur.fetchall()
            if workerRegNo:
                workerRegTime = workerRegNo[0][0]
            else:
                workerRegTime = 'N/A'

            # Worker Document Path
            docsPath = f"./static/documents/{active_user_session}Docs/{worker_reg_no}/"

            # fetch worker Docs
            cur.execute("SELECT * FROM workers_document WHERE form_unique_key=?", (form_unique_key,))
            workerDocs = cur.fetchall()

            # fetch worker Family members
            cur.execute("SELECT * FROM family_form WHERE form_unique_key=?", (form_unique_key,))
            workerFM = cur.fetchall()
            
            return render_template('view-registered-worker.html', docsPath=docsPath, workerRegTime=workerRegTime, workerList=workerD, workerDocs=workerDocs, workerFM=workerFM)
        except Exception as e:
            return redirect('registration-list')
    else:
        return redirect('/')

# Worker view-family-member
@app.route("/view-family-member", methods=['GET', 'POST'])
def viewFamilyMember():
    if 'user_session' in session:
        active_user_session = session.get('user_session')
        try:
            fmId = request.args.get('fm')
            fmN = request.args.get('fmN')

            conn = get_db_connection()
            cur = conn.cursor()

            # fetch workers
            cur.execute("SELECT * FROM family_form where id=? AND form_created_by=?", (fmId, active_user_session))
            fmData = cur.fetchall()

            # get Family member Path details
            fmRegNo =  fmData[0][4]
            formUniqueKey = fmData[0][3]
            cur.execute("SELECT id, form_worker_reg_no FROM half_form WHERE form_unique_key=?", (formUniqueKey,))
            workerRegN = cur.fetchall()
            if workerRegN:
                workerId = workerRegN[0][0]
                workerRegNo = workerRegN[0][1]
            
            docsPath = f"./static/documents/{active_user_session}Docs/{workerRegNo}/familyMembers/{fmRegNo}/"
 

            return render_template('view-family-member.html', wori=workerId, worReN=workerRegNo, fmN=fmN, docsPath=docsPath, fmData=fmData)
        except Exception as e:
            return redirect('/registration-list')
    else:
        return redirect('/')
    

# Edit Registered Worker
@app.route("/edit-registered-worker", methods=['GET', 'POST'])
def editRegisteredWorker():
    if 'user_session' in session:
        active_user_session = session.get('user_session')

        try:
            workerId = request.args.get('view-regWor')
            conn = get_db_connection()
            cur = conn.cursor()

            # fetch workers
            cur.execute("SELECT * FROM half_form where id=? AND form_created_by=?", (workerId, active_user_session))
            workerD = cur.fetchall()
            form_unique_key = workerD[0][44]

            # fetch worker Docs
            cur.execute("SELECT * FROM workers_document WHERE form_unique_key=?", (form_unique_key,))
            workerDocs = cur.fetchall()

            # fetch worker Family members
            cur.execute("SELECT * FROM family_form where form_unique_key=?", (form_unique_key,))
            workerFM = cur.fetchall()
            return render_template('edit-registered-worker.html', workerList = workerD, workerDocs=workerDocs, workerFM=workerFM)
        except Exception as e:
            return redirect('/registration-list')
    else:
        return redirect('/')
    
# Update Registered Worker
@app.route("/update-registered-worker", methods=['POST'])
def updateRegisteredWorker():
    if 'user_session' in session:
        if request.method == 'POST':
            active_user_session = session.get('user_session')

            conn = get_db_connection()
            cur = conn.cursor()

            w_id = request.form.get('w_id')
            w_name = request.form.get('w_name')
            w_fm_no = request.form.get('w_fm_no')
            w_status = request.form.get('w_status')
            w_gender = request.form.get('w_gender')

            w_dob = request.form.get('w_dob')
            w_citizenship = request.form.get('w_citizenship')
            w_marital_status = request.form.get('w_marital_status')
            w_religion = request.form.get('w_religion')
            w_contact_no = request.form.get('w_contact_no')

            w_address1 = request.form.get('w_address1')
            w_address2 = request.form.get('w_address2')
            w_address3 = request.form.get('w_address3')
            w_postcode = request.form.get('w_postcode')
            w_city = request.form.get('w_city')
            w_state = request.form.get('w_state')

            # Update Worker details
            cur.execute("UPDATE half_form SET no_family_mem=?, worker_detail_worker_legal_status=?, worker_detail_name_of_worker=?, worker_detail_gender=?, worker_detail_DOB=?, worker_detail_citizenship=?, worker_detail_marital_status=?, worker_detail_religion=?, worker_detail_contact_no=?, worker_emp_dtl_address1=?, worker_emp_dtl_address2=?, worker_emp_dtl_address3=?, worker_emp_dtl_postcode=?, worker_emp_dtl_city=?, worker_emp_dtl_state=? WHERE id=?", (w_fm_no, w_status, w_name, w_gender, w_dob, w_citizenship, w_marital_status, w_religion, w_contact_no, w_address1, w_address2, w_address3, w_postcode, w_city, w_state, w_id))
            conn.commit()
            conn.close()

            session['registration_list_update'] = 'success'
            return redirect('/registration-list')
        else:
            response = {
                'status': 'error',
                'msg': 'method error'
            }
            return jsonify(response)
    else:
        return redirect('/')



# Update Registered Worker Docs
@app.route("/update-worker-docs", methods=['POST'])
def updateWorkerDocs():
    if 'user_session' in session:
        if request.method == 'POST':
            conn = get_db_connection()
            cur = conn.cursor()

            docs_id = request.form.get('docs_id')
            type_of_document = request.form.get('type_of_document')
            document_id = request.form.get('document_id')
            place_of_issue = request.form.get('place_of_issue')
            issue_date = request.form.get('issue_date')

            expiry_date = request.form.get('expiry_date')
            issuing_country = request.form.get('issuing_country')
            document_status = request.form.get('document_status')
            document_current_status = request.form.get('document_current_status')
        
            # Update Worker details
            cur.execute("UPDATE workers_document SET type_of_douments=?, document_id=?, place_of_issue=?, document_issued_date=?, document_expiry_date=?, issuing_country=?, document_status=?, status_of_current_document=?  WHERE id=?", (type_of_document, document_id, place_of_issue, issue_date, expiry_date, issuing_country, document_status, document_current_status, docs_id))
            conn.commit()
            conn.close()
            session['registration_list_update'] = 'success'
            return redirect('/registration-list')   
        else:
            response = {
                'status': 'error',
                'msg': 'method error'
            }
            return jsonify(response)
    else:
        return redirect('/')


# edit-family-member
@app.route("/edit-family-member", methods=['GET', 'POST'])
def editFamilyMember():
    if 'user_session' in session:
        active_user_session = session.get('user_session')

        try:
            fmId = request.args.get('fm')
            conn = get_db_connection()
            cur = conn.cursor()

            # fetch workers
            cur.execute("SELECT * FROM family_form where id=? AND form_created_by=?", (fmId, active_user_session))
            fmData = cur.fetchall()
            return render_template('edit-family-member.html', fmData=fmData)
        except Exception as e:
            return redirect('/registration-list')
    else:
        return redirect('/')
    

# Update Family Member
@app.route("/update-family-member", methods=['POST'])
def updateFamilyMember():
    if 'user_session' in session:
        if request.method == 'POST':
            conn = get_db_connection()
            cur = conn.cursor()

            fm_id = request.form.get('fm_id')

            fm_name = request.form.get('fm_name')
            fm_relationship = request.form.get('fm_relationship')
            fm_family_name = request.form.get('fm_family_name')
            family_together = request.form.get('family_together')
            poe = request.form.get('poe')

            gender = request.form.get('gender')
            marital_status = request.form.get('marital_status')
            citizenship = request.form.get('citizenship')
            religion = request.form.get('religion')
            address1 = request.form.get('address1')

            address2 = request.form.get('address2')
            address3 = request.form.get('address3')
            postcode = request.form.get('postcode')
            city = request.form.get('city')
            state = request.form.get('state')

            contact_no = request.form.get('contact_no')
            race = request.form.get('race')
            place_of_birth = request.form.get('place_of_birth')
            employee_status = request.form.get('employee_status')
            employee_name = request.form.get('employee_name')
            employee_address = request.form.get('employee_address')

            # Docs 1
            type_of_document1 = request.form.get('type_of_document1')
            document_id1 = request.form.get('document_id1')
            place_of_issue1 = request.form.get('place_of_issue1')
            issue_date1 = request.form.get('issue_date1')
            expiry_date1 = request.form.get('expiry_date1')
            issuing_country1 = request.form.get('issuing_country1')
            document_status1 = request.form.get('document_status1')
            document_current_status1 = request.form.get('document_current_status1')

            # Docs 2
            type_of_document2 = request.form.get('type_of_document2')
            document_id2 = request.form.get('document_id2')
            place_of_issue2 = request.form.get('place_of_issue2')
            issue_date2 = request.form.get('issue_date2')
            expiry_date2 = request.form.get('expiry_date2')
            issuing_country2 = request.form.get('issuing_country2')
            document_status2 = request.form.get('document_status2')
            document_current_status2 = request.form.get('document_current_status2')
        
            # Update Worker details
            cur.execute("UPDATE family_form SET family_form_name_of_family_member=?, family_form_relationship=?, family_form_family_name=?, family_form_is_famliy_togther=?, family_form_family_form_poe=?, family_form_gender=?, family_form_marital_status=?, family_form_citizenship=?, family_form_religion=?, family_form_address1=?, family_form_address2=?, family_form_address3=?, family_form_postcode=?, family_form_city=?, family_form_state=?, family_form_contact_no=?, family_form_race=?, family_form_place_of_birth=?, family_form_emp_status=?, family_form_emp_name=?, family_form_emp_address=?, fmDoc1_type_of_documents=?, fmDoc1_document_id=?, fmDoc1_place_of_issue=?, fmDoc1_document_issued_date=?, fmDoc1_document_expiry_date=?, fmDoc1_issuing_country=?, fmDoc1_document_status=?, fmDoc1_status_of_current_document=?, fmDoc2_type_of_documents=?, fmDoc2_document_id=?, fmDoc2_place_of_issue=?, fmDoc2_document_issued_date=?, fmDoc2_document_expiry_date=?, fmDoc2_issuing_country=?, fmDoc2_document_status=?, fmDoc2_status_of_current_document=? WHERE id=?", (fm_name, fm_relationship, fm_family_name, family_together, poe, gender, marital_status, citizenship, religion, address1, address2, address3, postcode, city, state, contact_no, race, place_of_birth, employee_status, employee_name, employee_address, type_of_document1, document_id1, place_of_issue1, issue_date1, expiry_date1, issuing_country1, document_status1, document_current_status1, type_of_document2, document_id2, place_of_issue2, issue_date2, expiry_date2, issuing_country2, document_status2, document_current_status2, fm_id))
            conn.commit()
            conn.close()
            session['registration_list_update'] = 'success'
            return redirect('/registration-list')   
        else:
            response = {
                'status': 'error',
                'msg': 'method error'
            }
            return jsonify(response)
    else:
        return redirect('/')
    
# delete workers and their family members
@app.route("/del-registered-worker", methods=['GET'])
def delRegisteredWorker():
    if 'user_session' in session:
        active_user_session = session.get('user_session')
        try:
            worker_id = request.args.get('del')
            conn = get_db_connection()
            cur = conn.cursor()

            # fetch workers
            cur.execute("SELECT form_unique_key FROM half_form where id=? AND form_created_by=?", (worker_id, active_user_session))
            workerKey = cur.fetchall()
            form_unique_key = workerKey[0][0]

            # del worker
            cur.execute("DELETE FROM half_form WHERE id=? AND form_created_by=?", (worker_id, active_user_session))
            # del worker documents
            cur.execute("DELETE FROM workers_document where form_unique_key=?", (form_unique_key,))
            # del worker family members
            cur.execute("DELETE FROM family_form where form_unique_key=?", (form_unique_key,))
            
            conn.commit()
            conn.close()
            session['registration_list_delete'] = 'success'
            return redirect('/registration-list')
        except Exception as e:
            return redirect('/registration-list')
    else:
        return redirect('/')


# -- For My List -- 

# View Registered Worker
@app.route("/view-registered-worker1", methods=['GET', 'POST'])
def viewRegisteredWorker1():
    if 'user_session' in session:
        try:
            active_user_session = session.get('user_session')

            workerId = request.args.get('view-regWor')
            conn = get_db_connection()
            cur = conn.cursor()
            
            cur.execute("SELECT admin_server_ip FROM staff_status")
            qD = cur.fetchall()
            qD_len = len(qD)
            if qD_len == 1:
                getIP = qD[0][0]
                #print(getIP)
                response = connectionStaffServer(getIP)
                if response == 'connection_lost':
                    session['auth_error'] = 'not_connected'
                    return redirect('/')
                elif response['status'] == 'success':
                    url = f"http://{getIP}:6787/staff-view-registered-worker-req"
                    req_data = {
                        'workerID': workerId
                    }
                    try:
                        response = requests.post(url, data=req_data)

                        if response.status_code == 200:
                            data = response.json()
                            #print(data)

                            if data['status'] == 'success':
                                workerBiodata = data['workerBiodata']
                                workerRegTime = data['workerRegTime']
                                workerList = data['workerList']
                                workerDocs = data['workerDocs']
                                workerFM = data['workerFM']
                                
                                return render_template('view-registered-worker1.html', workerBiodata=workerBiodata, workerRegTime=workerRegTime, workerList=workerList, workerDocs=workerDocs, workerFM=workerFM)
                            else:
                                return render_template('view-registered-worker1.html', status='no_data')
                        else:
                            print(f'Request failed with status code: {response.status_code}')
                            return None
                        
                    except requests.exceptions.RequestException as e:
                        print(f'Request failed: {e}')
                        return None 
                else:
                    session['auth_error'] = 'not_connected'
                    return redirect('/')
            else:
                redirect('/')
        except Exception as e:
            return redirect('/my-registration-list')
    else:
        return redirect('/')

# Worker view-family-member
@app.route("/view-family-member1", methods=['GET', 'POST'])
def viewFamilyMember1():
    if 'user_session' in session:
        active_user_session = session.get('user_session')
        
        fmId = request.args.get('fm')
        fmN = request.args.get('fmN')

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT admin_server_ip FROM staff_status")
        qD = cur.fetchall()
        qD_len = len(qD)
        if qD_len == 1:
            getIP = qD[0][0]
            #print(getIP)
            response = connectionStaffServer(getIP)
            if response == 'connection_lost':
                session['auth_error'] = 'not_connected'
                return redirect('/')
            elif response['status'] == 'success':
                url = f"http://{getIP}:6787/staff-view-family-member-req"
                req_data = {
                    'fmID': fmId
                }
                try:
                    response = requests.post(url, data=req_data)

                    if response.status_code == 200:
                        data = response.json()
                        print('FMData: ', data)

                        if data['status'] == 'success':

                            print('FMData success: ', data)
                            workerId = data['workerId']
                            worker_reg_no = data['worker_reg_no']
                            fmList = data['fmList']
                            fmDocs = data['fmDocs']
                            fmBiodata = data['fmBiodata']
                            
                            return render_template('view-family-member1.html', fmBiodata=fmBiodata, wori=workerId, worReN=worker_reg_no, fmN=fmN, fmData=fmList, fmDocs=fmDocs)
                        else:
                            return render_template('view-family-member1.html', status='no_data')
        
                    else:
                        print(f'Request failed with status code: {response.status_code}')
                        return render_template('view-family-member1.html', status='no_data')
                    
                except requests.exceptions.RequestException as e:
                    print(f'Request failed: {e}')
                    return render_template('view-family-member1.html', status='no_data')
            else:
                session['auth_error'] = 'not_connected'
                print('eerror')
                return redirect('/')
        else:
            redirect('/my-registration-list')
    else:
        return redirect('/')




    
# ---------------------# RESTful API > Testing # ---------------------
# Define the SIFW API endpoints and your credentials
def dermalop_ip_address():
    conn = get_db_connection()
    cur = conn.cursor()
    # fetch IP
    #cur.execute("SELECT dermalog_ip FROM dermalog_ip where id=1")
    #dermalog_ip = cur.fetchone()[0]
    #return dermalog_ip

    # Check Connection
    cur.execute("SELECT admin_server_ip FROM staff_status")
    qD = cur.fetchall()
    qD_len = len(qD)
    if qD_len == 1:
        getIP = qD[0][0]

        # request
        url = f"http://{getIP}:6787/staff-dermalog-ip-address"

        try:
            response = requests.post(url, timeout=2)

            if response.status_code == 200:
                resD = response.json()
                if resD['status'] == 'success':
                    return resD['dermalog_ip']
                else:
                    return False
            else:    
                return False
            
        except requests.exceptions.ConnectionError:
            res = {
                'status': 'connection lost'
            }
            return jsonify(res)
        except requests.exceptions.RequestException as e:
            res = {
                'status': 'error'
            }
            return jsonify(res)
    else:
        res = {
            'status': 'Admin server ip not found'
        }
        return jsonify(res)
    


# Function to authenticate and get the token
def authenticate_user():
    # Get IP
    get_dermalog_ip = dermalop_ip_address()
    global SIFW_API_BASE_URL
    SIFW_API_BASE_URL = f"{get_dermalog_ip}/SIFWAPI"
    USERNAME = "SIFWuser1"
    PASSWORD = "User1SIFW2019"
    #token = None


    global token
    url = f"{SIFW_API_BASE_URL}/AuthenticateUser"
    data = {
        "Username": USERNAME,
        "Password": PASSWORD,
    }
    response = requests.post(url, json=data, verify=False)
    if response.status_code == 200:
        token = response.json().get("Token")
        return token
    return False

# Function to get profile bio data
def get_profile_bio_data(doc_id):
    if not token:
        return {"error": "Authentication token is missing or invalid"}, 401
    url = f"{SIFW_API_BASE_URL}/getprofilebiodata"
    headers = {
        "Token": token,
        "Content-Type": "application/json"  # Specify the Content-Type as JSON
    }
    data = {
        "DocID": doc_id,
    }
    response = requests.post(url, json=data, headers=headers, verify=False)
    print('check:: ', response.json())
    return response.json()

@app.route('/authenticate')
def authenticate():
    if authenticate_user():
        return jsonify({"message > ": authenticate_user()})
    else:
        return jsonify({"error": "Authentication failed"}), 401

@app.route('/get-profile-bio-data', methods=['GET'])
def get_profile_bio_data_route():
    try:
        # Call for token authentication
        authenticate_user()
        active_user_session = session.get('user_session')
        doc_id = request.args.get('DocID')
        view_regWor = request.args.get('view_regWor')
        response_data = get_profile_bio_data(doc_id)
        
        # Added For Edit Registered Worker
        workerId = request.args.get('view_regWor')
        conn = get_db_connection()
        cur = conn.cursor()
        
        # fetch workers
        cur.execute("SELECT * FROM half_form where id=?", (workerId,))
        workerD = cur.fetchall()
        form_unique_key = workerD[0][33]
        worker_reg_no = workerD[0][4]
        
        
        # fetch worker Docs
        cur.execute("SELECT * FROM workers_document WHERE form_unique_key=?", (form_unique_key,))
        workerDocs = cur.fetchall()
        
        # fetch worker Family members
        cur.execute("SELECT * FROM family_form where form_unique_key=?", (form_unique_key,))
        workerFM = cur.fetchall()
        
        return render_template('edit-registered-worker1.html', worker_reg_no=worker_reg_no, bioData=response_data, view_regWor=workerId, workerList=workerD, workerDocs=workerDocs, workerFM=workerFM)
    except Exception as e:
        error_msg = str(e)
        session['dermalog_status'] = error_msg
        return redirect('/my-registration-list')
    
    
@app.route('/get-profile-bio-data2', methods=['GET'])
def get_profile_bio_data_route2():
    try:
        # Call for token authentication
        authenticate_user()
        active_user_session = session.get('user_session')
        doc_id = request.args.get('DocID')
        fmId = request.args.get('fm')
        response_data = get_profile_bio_data(doc_id)
        
        # Added For Edit Registered Worker
        
        fmId = request.args.get('fm')
        conn = get_db_connection()
        cur = conn.cursor()

        # fetch workers
        cur.execute("SELECT * FROM family_form where id=? AND form_created_by=?", (fmId, active_user_session))
        fmData = cur.fetchall()
        

        # get Family member Path details
        fmRegNo =  fmData[0][4]
        formUniqueKey = fmData[0][3]
        cur.execute("SELECT id, form_worker_reg_no FROM half_form WHERE form_unique_key=?", (formUniqueKey,))
        workerRegN = cur.fetchall()
        if workerRegN:
            workerId = workerRegN[0][0]
            workerRegNo = workerRegN[0][1]
        
        docsPath = f"./static/documents/{active_user_session}Docs/{workerRegNo}/familyMembers/{fmRegNo}/"
        
        
        return render_template('edit-family-member1.html',fm_reg_no=fmRegNo, bioData=response_data, fm=fmId,  wori=workerId, worReN=workerRegNo, docsPath=docsPath, fmData=fmData)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------
# End * Restful API > Testing
# ---------------------------

'''
# Update Worker BioData
@app.route("/update-worker-biodata", methods=['POST'])
def updateWorkerBiodata():
    if 'user_session' in session:
        if request.method == 'POST':
            try:
                active_user_session = session.get('user_session')
                conn = get_db_connection()
                cur = conn.cursor()

                worker_reg_no = request.form.get('worker_reg_no')
                docId = request.form.get('docId')
                faceImage = request.form.get('faceImage')
                totalFingers = request.form.get('totalFingers')
                
                updated_date = datetime.now().strftime('%d/%m/%Y')
                updated_time = datetime.now().strftime('%H:%M:%S')
                
                # Check Worker BioData
                cur.execute("SELECT worker_reg_no FROM worker_biodata WHERE worker_reg_no=?", (worker_reg_no,))
                checkData = cur.fetchall()
                checkData = len(checkData)
                print('cd, ', checkData)
                if(checkData == 1):
                    cur.execute("UPDATE worker_biodata SET docId=?, faceImage=?, updated_date=?, updated_time=? WHERE worker_reg_no=?", (docId, faceImage, updated_date, updated_time, worker_reg_no))
                    # Update Fingers
                    for num in range(1, int(totalFingers)+1):
                        
                        fingerRemarks = request.form.get(f'fingerRemarks{num}')
                        fingerImage = request.form.get(f'fingerImage{num}')
                        
                        fRem = f'fingerRemarks{num}'
                        fImg = f'fingerImage{num}'
                        # Update
                        uQ = f"UPDATE worker_biodata SET {fRem}=?, {fImg}=? WHERE worker_reg_no=?" 
                        cur.execute(uQ, (fingerRemarks, fingerImage, worker_reg_no))
                    
                else:
                    cur.execute("INSERT INTO worker_biodata(worker_reg_no, docId, faceImage, updated_date, updated_time)  VALUES(?, ?, ?, ?, ?)", (worker_reg_no, docId, faceImage, updated_date, updated_time)) 
                    # Update Fingers
                    for num in range(1, int(totalFingers)+1):
                        
                        fingerRemarks = request.form.get(f'fingerRemarks{num}')
                        fingerImage = request.form.get(f'fingerImage{num}')
                        
                        fRem = f'fingerRemarks{num}'
                        fImg = f'fingerImage{num}'
                        # Update
                        uQ = f"UPDATE worker_biodata SET {fRem}=?, {fImg}=? WHERE worker_reg_no=?" 
                        cur.execute(uQ, (fingerRemarks, fingerImage, worker_reg_no))
                
                
                conn.commit()
                conn.close()
                session['biodata_success'] = 'success'
                return redirect('/my-registration-list')
            except Exception as e:
                session['biodata_error'] = 'error'
                return redirect('/my-registration-list')    
        else:
            return redirect('/my-registration-list')
    else:
        return redirect('/')
'''

# Update Worker BioData
@app.route("/update-worker-biodata", methods=['POST'])
def updateWorkerBiodata():
    if 'user_session' in session:
        if request.method == 'POST':
            
            active_user_session = session.get('user_session')
            conn = get_db_connection()
            cur = conn.cursor()

            #worker_reg_no = request.form.get('worker_reg_no')
            #docId = request.form.get('docId')
            #faceImage = request.form.get('faceImage')
            #totalFingers = request.form.get('totalFingers')
            
            formData = request.form

            cur.execute("SELECT admin_server_ip FROM staff_status")
            qD = cur.fetchall()
            qD_len = len(qD)
            if qD_len == 1:
                getIP = qD[0][0]
                #print(getIP)
                response = connectionStaffServer(getIP)
                if response == 'connection_lost':
                    session['auth_error'] = 'not_connected'
                    return redirect('/')
                elif response['status'] == 'success':
                    url = f"http://{getIP}:6787/staff-update-worker-biodata"
                    req_data = {
                        #'active_user_session': active_user_session,
                        #'worker_reg_no': worker_reg_no,
                        #'docId': docId,
                        #'faceImage': faceImage,
                        #'totalFingers': totalFingers
                    }
                    try:
                        response = requests.post(url, data=formData)

                        if response.status_code == 200:
                            data = response.json()
                            print('FMData: ', data)

                            if data['status'] == 'success':
                                session['biodata_success'] = 'success'
                                return redirect('/my-registration-list')
                            else:
                                session['biodata_success'] = 'error'
                                return redirect('/my-registration-list')
            
                        else:
                            session['biodata_success'] = 'error'
                            return redirect('/my-registration-list')
                        
                    except requests.exceptions.RequestException as e:
                        session['biodata_success'] = 'error'
                        return redirect('/my-registration-list')
                else:
                    session['biodata_success'] = 'error'
                    return redirect('/my-registration-list')
            else:
                session['biodata_success'] = 'error'
                return redirect('/my-registration-list')
        else:
            session['biodata_success'] = 'error'
            return redirect('/my-registration-list')
    else:
        return redirect('/')
    

'''
# Update Family Member BioData
@app.route("/update-fm-biodata", methods=['POST'])
def updateFMBiodata():
    if 'user_session' in session:
        if request.method == 'POST':
            try:
                active_user_session = session.get('user_session')
                conn = get_db_connection()
                cur = conn.cursor()

                fm_reg_no = request.form.get('fm_reg_no')
                docId = request.form.get('docId')
                faceImage = request.form.get('faceImage')
                totalFingers = request.form.get('totalFingers')
                
                updated_date = datetime.now().strftime('%d/%m/%Y')
                updated_time = datetime.now().strftime('%H:%M:%S')
                
                # Check Worker BioData
                cur.execute("SELECT fm_reg_no FROM fm_biodata WHERE fm_reg_no=?", (fm_reg_no,))
                checkData = cur.fetchall()
                checkData = len(checkData)
                print('cd, ', checkData)
                if(checkData == 1):
                    cur.execute("UPDATE fm_biodata SET docId=?, faceImage=?, updated_date=?, updated_time=? WHERE fm_reg_no=?", (docId, faceImage, updated_date, updated_time, fm_reg_no))
                    # Update Fingers
                    for num in range(1, int(totalFingers)+1):
                        
                        fingerRemarks = request.form.get(f'fingerRemarks{num}')
                        fingerImage = request.form.get(f'fingerImage{num}')
                        
                        fRem = f'fingerRemarks{num}'
                        fImg = f'fingerImage{num}'
                        # Update
                        uQ = f"UPDATE fm_biodata SET {fRem}=?, {fImg}=? WHERE fm_reg_no=?" 
                        cur.execute(uQ, (fingerRemarks, fingerImage, fm_reg_no))
                    
                else:
                    cur.execute("INSERT INTO fm_biodata(fm_reg_no, docId, faceImage, updated_date, updated_time)  VALUES(?, ?, ?, ?, ?)", (fm_reg_no, docId, faceImage, updated_date, updated_time)) 
                    # Update Fingers
                    for num in range(1, int(totalFingers)+1):
                        
                        fingerRemarks = request.form.get(f'fingerRemarks{num}')
                        fingerImage = request.form.get(f'fingerImage{num}')
                        
                        fRem = f'fingerRemarks{num}'
                        fImg = f'fingerImage{num}'
                        # Update
                        uQ = f"UPDATE fm_biodata SET {fRem}=?, {fImg}=? WHERE fm_reg_no=?" 
                        cur.execute(uQ, (fingerRemarks, fingerImage, fm_reg_no))
                
                
                conn.commit()
                conn.close()
                session['biodata_success'] = 'success'
                return redirect('/my-registration-list')
            except Exception as e:
                session['biodata_error'] = 'error'
                return redirect('/my-registration-list')    
        else:
            return redirect('/my-registration-list')
    else:
        return redirect('/')
'''

@app.route("/update-fm-biodata", methods=['POST'])
def updateFMBiodata():
    if 'user_session' in session:
        if request.method == 'POST':
            
            active_user_session = session.get('user_session')
            conn = get_db_connection()
            cur = conn.cursor()

            fm_reg_no = request.form.get('fm_reg_no')
            docId = request.form.get('docId')
            faceImage = request.form.get('faceImage')
            totalFingers = request.form.get('totalFingers')
            
            

            cur.execute("SELECT admin_server_ip FROM staff_status")
            qD = cur.fetchall()
            qD_len = len(qD)
            if qD_len == 1:
                getIP = qD[0][0]
                #print(getIP)
                response = connectionStaffServer(getIP)
                if response == 'connection_lost':
                    session['auth_error'] = 'not_connected'
                    return redirect('/')
                elif response['status'] == 'success':
                    url = f"http://{getIP}:6787/staff-update-fm-biodata"
                    req_data = {
                        'active_user_session': active_user_session,
                        'fm_reg_no': fm_reg_no,
                        'docId': docId,
                        'faceImaage': faceImage,
                        'totalFingers': totalFingers
                    }
                    try:
                        response = requests.post(url, data=req_data)

                        if response.status_code == 200:
                            data = response.json()
                            print('FMData: ', data)

                            if data['status'] == 'success':
                                session['biodata_success'] = 'success'
                                return redirect('/my-registration-list')
                            else:
                                session['biodata_success'] = 'error'
                                return redirect('/my-registration-list')
                        else:
                            session['biodata_success'] = 'error'
                            return redirect('/my-registration-list')
                        
                    except requests.exceptions.RequestException as e:
                        session['biodata_success'] = 'error'
                        return redirect('/my-registration-list')
                else:
                    session['biodata_success'] = 'error'
                    return redirect('/my-registration-list')
            else:
                session['biodata_success'] = 'error'
                return redirect('/my-registration-list')
        else:
            session['biodata_success'] = 'error'
            return redirect('/my-registration-list')
    else:
        return redirect('/')
    












# Edit Registered Worker
@app.route("/edit-registered-worker1", methods=['GET', 'POST'])
def editRegisteredWorker1():
    if 'user_session' in session:
        active_user_session = session.get('user_session')

        try:
            workerId = request.args.get('view-regWor')
            conn = get_db_connection()
            cur = conn.cursor()


            # Common Data
            # -----------
            citizenship_detail = citizenship()
            citizenship_status = citizenship_detail['status']
            if citizenship_status == 'success':
                citizenship_data = citizenship_detail['citizenship']


           
            marital_detail = marital()
            marital_status = marital_detail['status']
            if marital_status == 'success':
                marital_data = marital_detail['marital']

           
            poe_detail = poe()
            poe_status = poe_detail['status']
            if poe_status == 'success':
                poe_data = poe_detail['poe']

           
            gender_detail = gender()
            gender_status = gender_detail['status']
            if gender_status == 'success':
                gender_data = gender_detail['gender']

            religion_detail = religion()
            religion_status = religion_detail['status']
            if religion_status == 'success':
                religion_data = religion_detail['religion']


           
            race_detail = race()
            race_status = race_detail['status']
            if race_status == 'success':
                race_data = race_detail['race']

            
            relationship_detail = relationship()
            relationship_status = relationship_detail['status']
            if relationship_status == 'success':
                relationship_data = relationship_detail['relationship']

            
            job_sector_detail = job_sector()
            job_sector_status = job_sector_detail['status']
            if job_sector_status == 'success':
                job_sector_data = job_sector_detail['job_sector']

           
            job_status_sponsor_detail = job_status_sponsor()
            job_status_sponsor_status = job_status_sponsor_detail['status']
            if job_status_sponsor_status == 'success':
                job_status_sponsor_data = job_status_sponsor_detail['job_status_sponsor']

           
            city_detail = city()
            city_status = city_detail['status']
            if city_status == 'success':
                city_data = city_detail['city']

            
            state_detail = state()
            state_status = state_detail['status']
            if state_status == 'success':
                state_data = state_detail['state']

            
            issuingCountry_detail = issuingCountry()
            issuingCountry_status = issuingCountry_detail['status']
            if issuingCountry_status == 'success':
                issuingCountry_data = issuingCountry_detail['issuingCountry']

           
            docStatus_detail = docStatus()
            docStatus_status = docStatus_detail['status']
            if docStatus_status == 'success':
                docStatus_data = docStatus_detail['docStatus']

           
            curDocStatus_detail = curDocStatus()
            curDocStatus_status = curDocStatus_detail['status']
            if curDocStatus_status == 'success':
                curDocStatus_data = curDocStatus_detail['curDocStatus']

            typeOfDoc_detail = typeOfDoc()
            typeOfDoc_status = typeOfDoc_detail['status']
            if typeOfDoc_status == 'success':
                typeOfDoc_data = typeOfDoc_detail['typeOfDoc']

           
            employment_status_detail = employment_status()
            employment_status_status = employment_status_detail['status']
            if employment_status_status == 'success':
                employment_status_data = employment_status_detail['employment_status']


            employment_detail = employmentDetail()
            get_employment_detail = employment_detail['status']
            if get_employment_detail == 'success':
                employment_detail_data = employment_detail['employment_detail']
            

            # check
            cur.execute("SELECT admin_server_ip FROM staff_status")
            qD = cur.fetchall()
            qD_len = len(qD)
            if qD_len == 1:
                getIP = qD[0][0]
                response = connectionStaffServer(getIP)
                if response == 'connection_lost':
                    session['auth_error'] = 'not_connected'
                    return redirect('/')
                elif response['status'] == 'success':
                    url = f"http://{getIP}:6787/staff-edit-registered-worker-req"
                    req_data = {
                        'workerID': workerId
                    }
                    try:
                        response = requests.post(url, data=req_data)

                        if response.status_code == 200:
                            data = response.json()
                            
                            if data['status'] == 'success':
                                workerBiodata = data['workerBiodata']
                                workerRegTime = data['workerRegTime']
                                workerList = data['workerList']
                                workerDocs = data['workerDocs']
                                workerFM = data['workerFM']
                                
                                return render_template('edit-registered-worker1.html', workerBiodata=workerBiodata, workerRegTime=workerRegTime, workerList=workerList, workerDocs=workerDocs, workerFM=workerFM, employment_detail=employment_detail_data, view_regWor=workerId, citizenshipList=citizenship_data, maritialList=marital_data, poeList=poe_data, genderList=gender_data, religionList=religion_data, raceList=race_data, relationshipList=relationship_data, jobSectorList=job_sector_data, cityList=city_data, stateList=state_data, issuingCountryList=issuingCountry_data, docStatusList=docStatus_data, curDocStatusList=curDocStatus_data, typeOfDocList=typeOfDoc_data, employement_statusList=employment_status_data, jobStatusSponsorList = job_status_sponsor_data)
                            else:
                                return render_template('edit-registered-worker1.html', status='no_data')
            
                        else:
                            print(f'Request failed with status code: {response.status_code}')
                            return None
                        
                    except requests.exceptions.RequestException as e:
                        print(f'Request failed: {e}')
                        return None 
                else:
                    session['auth_error'] = 'not_connected'
                    return redirect('/')
            else:
                redirect('/')
            
            
            #return render_template('edit-registered-worker1.html', employment_detail=employment_detail_data, worker_reg_no=worker_reg_no, view_regWor=workerId, workerList = workerD, workerDocs=workerDocs, workerFM=workerFM, citizenshipList=citizenship_data, maritialList=marital_data, poeList=poe_data, genderList=gender_data, religionList=religion_data, raceList=race_data, relationshipList=relationship_data, jobSectorList=job_sector_data, cityList=city_data, stateList=state_data, issuingCountryList=issuingCountry_data, docStatusList=docStatus_data, curDocStatusList=curDocStatus_data, typeOfDocList=typeOfDoc_data, employement_statusList=employment_status_data, jobStatusSponsorList = job_status_sponsor_data)
        except Exception as e:
            print(e)
            return redirect('/my-registration-list')
    else:
        return redirect('/')
    
# Update Registered Worker
@app.route("/update-registered-worker1", methods=['POST'])
def updateRegisteredWorker1():
    if 'user_session' in session:
        if request.method == 'POST':
            active_user_session = session.get('user_session')
            conn = get_db_connection()
            cur = conn.cursor()

            form_data = request.form
            
            # check
            cur.execute("SELECT admin_server_ip FROM staff_status")
            qD = cur.fetchall()
            qD_len = len(qD)
            if qD_len == 1:
                getIP = qD[0][0]
                response = connectionStaffServer(getIP)
                if response == 'connection_lost':
                    session['auth_error'] = 'not_connected'
                    return redirect('/')
                elif response['status'] == 'success':
                    url = f"http://{getIP}:6787/staff-update-registered-worker"
                    
                    try:
                        response = requests.post(url, data=form_data)
                        if response.status_code == 200:
                            data = response.json()
                            print('Update resp :: ', data)

                            session['registration_list_update1'] = 'success'
                            return redirect('/my-registration-list')
                            
                        else:
                            session['registration_list_update1'] = 'error'
                            return redirect('/my-registration-list')
                        
                    except requests.exceptions.RequestException as e:
                        session['registration_list_update1'] = 'error'
                        return redirect('/my-registration-list')
                else:
                    session['registration_list_update1'] = 'request fail'
                    return redirect('/my-registration-list')
            else:
                session['registration_list_update1'] = 'server not connected'
                return redirect('/my-registration-list')
            
        else:
            session['registration_list_update1'] = 'server not'
            return redirect('/my-registration-list')
    else:
        return redirect('/')



# Update Registered Worker Docs
@app.route("/update-worker-docs1", methods=['POST'])
def updateWorkerDocs1():
    if 'user_session' in session:
        if request.method == 'POST':
            conn = get_db_connection()
            cur = conn.cursor()

            form_data = request.form
            # check
            cur.execute("SELECT admin_server_ip FROM staff_status")
            qD = cur.fetchall()
            qD_len = len(qD)
            if qD_len == 1:
                getIP = qD[0][0]
                response = connectionStaffServer(getIP)
                if response == 'connection_lost':
                    session['auth_error'] = 'not_connected'
                    return redirect('/')
                elif response['status'] == 'success':
                    url = f"http://{getIP}:6787/staff-update-worker-docs"
                    
                    try:
                        response = requests.post(url, data=form_data)
                        if response.status_code == 200:
                            data = response.json()
                            print('Update resp :: ', data)

                            session['registration_list_update1'] = 'success'
                            return redirect('/my-registration-list')
                            
                        else:
                            session['registration_list_update1'] = 'error'
                            return redirect('/my-registration-list')
                        
                    except requests.exceptions.RequestException as e:
                        session['registration_list_update1'] = 'error'
                        return redirect('/my-registration-list')
                else:
                    session['registration_list_update1'] = 'request fail'
                    return redirect('/my-registration-list')
            else:
                session['registration_list_update1'] = 'server not connected'
                return redirect('/my-registration-list')
  
        else:
            response = {
                'status': 'error',
                'msg': 'method error'
            }
            return jsonify(response)
    else:
        return redirect('/')


# edit-family-member
@app.route("/edit-family-member1", methods=['GET', 'POST'])
def editFamilyMember1():
    if 'user_session' in session:
        active_user_session = session.get('user_session')

        fmId = request.args.get('fm')
        conn = get_db_connection()
        cur = conn.cursor()

        # Check
        cur.execute("SELECT admin_server_ip FROM staff_status")
        qD = cur.fetchall()
        qD_len = len(qD)
        if qD_len == 1:
            getIP = qD[0][0]
            #print(getIP)
            response = connectionStaffServer(getIP)
            if response == 'connection_lost':
                session['auth_error'] = 'not_connected'
                return redirect('/')
            elif response['status'] == 'success':
                url = f"http://{getIP}:6787/staff-edit-family-member-req"
                req_data = {
                    'fmID': fmId
                }
                try:
                    response = requests.post(url, data=req_data)

                    if response.status_code == 200:
                        data = response.json()
                        
                        if data['status'] == 'success':

                            workerId = data['workerId']
                            worker_reg_no = data['worker_reg_no']
                            fmList = data['fmList']
                            fmDocs = data['fmDocs']
                            fmBiodata = data['fmBiodata']
                            
                            return render_template('edit-family-member1.html', fmBiodata=fmBiodata, wori=workerId, worReN=worker_reg_no, fmData=fmList, fmDocs=fmDocs)
                        else:
                            return render_template('edit-family-member1.html', status='no_data')
        
                    else:
                        print(f'Request failed with status code: {response.status_code}')
                        return render_template('edit-family-member1.html', status='no_data')
                    
                except requests.exceptions.RequestException as e:
                    print(f'Request failed: {e}')
                    return render_template('edit-family-member1.html', status='no_data')
            else:
                session['auth_error'] = 'not_connected'
                print('error')
                return redirect('/')
        else:
            print('eerrrrr')
            return redirect('/my-registration-list')

            '''
            # fetch workers
            cur.execute("SELECT * FROM family_form where id=? AND form_created_by=?", (fmId, active_user_session))
            fmData = cur.fetchall()
            

            # get Family member Path details
            fmRegNo =  fmData[0][4]
            formUniqueKey = fmData[0][3]
            cur.execute("SELECT id, form_worker_reg_no FROM half_form WHERE form_unique_key=?", (formUniqueKey,))
            workerRegN = cur.fetchall()
            if workerRegN:
                workerId = workerRegN[0][0]
                workerRegNo = workerRegN[0][1]
            
            docsPath = f"./static/documents/{active_user_session}Docs/{workerRegNo}/familyMembers/{fmRegNo}/"
            
            
            return render_template('edit-family-member1.html', fm=fmId,  wori=workerId, worReN=workerRegNo, docsPath=docsPath, fmData=fmData)
            '''
    else:
        return redirect('/')
    

# Update Family Member
@app.route("/update-family-member1", methods=['POST'])
def updateFamilyMember1():
    if 'user_session' in session:
        if request.method == 'POST':
            conn = get_db_connection()
            cur = conn.cursor()
            form_data = request.form

            # check
            cur.execute("SELECT admin_server_ip FROM staff_status")
            qD = cur.fetchall()
            qD_len = len(qD)
            if qD_len == 1:
                getIP = qD[0][0]
                response = connectionStaffServer(getIP)
                if response == 'connection_lost':
                    session['auth_error'] = 'not_connected'
                    return redirect('/')
                elif response['status'] == 'success':
                    url = f"http://{getIP}:6787/staff-update-family-member"
                    
                    try:
                        response = requests.post(url, data=form_data)
                        if response.status_code == 200:
                            data = response.json()
                            print('Update resp :: ', data)

                            session['registration_list_update1'] = 'success'
                            return redirect('/my-registration-list')
                            
                        else:
                            session['registration_list_update1'] = 'error'
                            return redirect('/my-registration-list')
                        
                    except requests.exceptions.RequestException as e:
                        session['registration_list_update1'] = 'error'
                        return redirect('/my-registration-list')
                else:
                    session['registration_list_update1'] = 'request fail'
                    return redirect('/my-registration-list')
            else:
                session['registration_list_update1'] = 'server not connected'
                return redirect('/my-registration-list')  
        else:
            session['registration_list_update1'] = 'request error'
            return redirect('/my-registration-list') 
    else:
        return redirect('/')



# Update Registered Worker Docs
@app.route("/update-family-member1-docs", methods=['POST'])
def update_fm1_Docs():
    if 'user_session' in session:
        if request.method == 'POST':
            conn = get_db_connection()
            cur = conn.cursor()

            form_data = request.form
            # check
            cur.execute("SELECT admin_server_ip FROM staff_status")
            qD = cur.fetchall()
            qD_len = len(qD)
            if qD_len == 1:
                getIP = qD[0][0]
                response = connectionStaffServer(getIP)
                if response == 'connection_lost':
                    session['auth_error'] = 'not_connected'
                    return redirect('/')
                elif response['status'] == 'success':
                    url = f"http://{getIP}:6787/staff-update-family-member-docs"
                    
                    try:
                        response = requests.post(url, data=form_data)
                        if response.status_code == 200:
                            data = response.json()
                            print('Update resp :: ', data)

                            session['registration_list_update1'] = 'success'
                            return redirect('/my-registration-list')
                            
                        else:
                            session['registration_list_update1'] = 'error'
                            return redirect('/my-registration-list')
                        
                    except requests.exceptions.RequestException as e:
                        session['registration_list_update1'] = 'error'
                        return redirect('/my-registration-list')
                else:
                    session['registration_list_update1'] = 'request fail'
                    return redirect('/my-registration-list')
            else:
                session['registration_list_update1'] = 'server not connected'
                return redirect('/my-registration-list')
  
        else:
            response = {
                'status': 'error',
                'msg': 'method error'
            }
            return jsonify(response)
    else:
        return redirect('/')





# delete workers and their family members
@app.route("/del-registered-worker1", methods=['GET'])
def delRegisteredWorker1():
    if 'user_session' in session:
        active_user_session = session.get('user_session')
        try:
            worker_id = request.args.get('del')
            conn = get_db_connection()
            cur = conn.cursor()

            # fetch workers
            cur.execute("SELECT form_unique_key FROM half_form where id=? AND form_created_by=?", (worker_id, active_user_session))
            workerKey = cur.fetchall()
            form_unique_key = workerKey[0][0]

            # del worker
            cur.execute("DELETE FROM half_form WHERE id=? AND form_created_by=?", (worker_id, active_user_session))
            # del worker documents
            cur.execute("DELETE FROM workers_document where form_unique_key=?", (form_unique_key,))
            # del worker family members
            cur.execute("DELETE FROM family_form where form_unique_key=?", (form_unique_key,))
            
            conn.commit()
            conn.close()
            session['registration_list_delete1'] = 'success'
            return redirect('/my-registration-list')
        except Exception as e:
            return redirect('/my-registration-list')
    else:
        return redirect('/')

# -- End * For My List --
# -----------------------


# -- Sub Users List --
# View Registered Worker
@app.route("/view-registered-worker2", methods=['GET', 'POST'])
def viewRegisteredWorker2():
    if 'user_session' in session:
        try:
            active_user_session = session.get('user_session')

            regL_path = session.get('regList_path')

            workerId = request.args.get('view-regWor')
            
            conn = get_db_connection()
            cur = conn.cursor()

            # fetch workers
            cur.execute("SELECT * FROM half_form WHERE id=? AND form_created_by=?", (workerId, active_user_session))
            workerD = cur.fetchall()
            form_unique_key = workerD[0][44]

            # get worker reg time
            worker_reg_no = workerD[0][4]
            cur.execute("SELECT reg_time FROM half_form_time WHERE worker_reg_no=?", (worker_reg_no,))
            workerRegNo = cur.fetchall()
            if workerRegNo:
                workerRegTime = workerRegNo[0][0]
            else:
                workerRegTime = 'N/A'

            # Worker Document Path
            docsPath = f"./static/documents/{active_user_session}Docs/{worker_reg_no}/"

            # fetch worker Docs
            cur.execute("SELECT * FROM workers_document WHERE form_unique_key=?", (form_unique_key,))
            workerDocs = cur.fetchall()

            # fetch worker Family members
            cur.execute("SELECT * FROM family_form WHERE form_unique_key=?", (form_unique_key,))
            workerFM = cur.fetchall()
            
            return render_template('view-registered-worker2.html', regL_path=regL_path, docsPath=docsPath, workerRegTime=workerRegTime, workerList=workerD, workerDocs=workerDocs, workerFM=workerFM)
        except Exception as e:
            return redirect('/subusers-registration-list')
    else:
        return redirect('/')

# Worker view-family-member
@app.route("/view-family-member2", methods=['GET', 'POST'])
def viewFamilyMember2():
    if 'user_session' in session:
        active_user_session = session.get('user_session')
        regL_path = session.get('regList_path')
        try:
            fmId = request.args.get('fm')
            fmN = request.args.get('fmN')
            
            conn = get_db_connection()
            cur = conn.cursor()

            # fetch workers
            cur.execute("SELECT * FROM family_form where id=? AND form_created_by=?", (fmId, active_user_session))
            fmData = cur.fetchall()

            # get Family member Path details
            fmRegNo =  fmData[0][4]
            formUniqueKey = fmData[0][3]
            cur.execute("SELECT id, form_worker_reg_no FROM half_form WHERE form_unique_key=?", (formUniqueKey,))
            workerRegN = cur.fetchall()
            if workerRegN:
                workerId = workerRegN[0][0]
                workerRegNo = workerRegN[0][1]
            
            docsPath = f"./static/documents/{active_user_session}Docs/{workerRegNo}/familyMembers/{fmRegNo}/"
 

            return render_template('view-family-member2.html',regL_path=regL_path, wori=workerId, worReN=workerRegNo, fmN=fmN, docsPath=docsPath, fmData=fmData)
        except Exception as e:
            return redirect('/subusers-registration-list')
    else:
        return redirect('/')
    

# Edit Registered Worker
@app.route("/edit-registered-worker2", methods=['GET', 'POST'])
def editRegisteredWorker2():
    if 'user_session' in session:
        active_user_session = session.get('user_session')
        regL_path = session.get('regList_path')

        try:
            workerId = request.args.get('view-regWor')
            conn = get_db_connection()
            cur = conn.cursor()

            # fetch workers
            cur.execute("SELECT * FROM half_form where id=? AND form_created_by=?", (workerId, active_user_session))
            workerD = cur.fetchall()
            form_unique_key = workerD[0][44]

            # fetch worker Docs
            cur.execute("SELECT * FROM workers_document WHERE form_unique_key=?", (form_unique_key,))
            workerDocs = cur.fetchall()

            # fetch worker Family members
            cur.execute("SELECT * FROM family_form where form_unique_key=?", (form_unique_key,))
            workerFM = cur.fetchall()
            return render_template('edit-registered-worker2.html',regL_path=regL_path, workerList = workerD, workerDocs=workerDocs, workerFM=workerFM)
        except Exception as e:
            return redirect('/subusers-registration-list')
    else:
        return redirect('/')
    
# Update Registered Worker
@app.route("/update-registered-worker2", methods=['POST'])
def updateRegisteredWorker2():
    if 'user_session' in session:
        
        if request.method == 'POST':
            active_user_session = session.get('user_session')
            regL_path = session.get('regList_path')

            conn = get_db_connection()
            cur = conn.cursor()

            w_id = request.form.get('w_id')
            w_name = request.form.get('w_name')
            w_fm_no = request.form.get('w_fm_no')
            w_status = request.form.get('w_status')
            w_gender = request.form.get('w_gender')

            w_dob = request.form.get('w_dob')
            w_citizenship = request.form.get('w_citizenship')
            w_marital_status = request.form.get('w_marital_status')
            w_religion = request.form.get('w_religion')
            w_contact_no = request.form.get('w_contact_no')

            w_address1 = request.form.get('w_address1')
            w_address2 = request.form.get('w_address2')
            w_address3 = request.form.get('w_address3')
            w_postcode = request.form.get('w_postcode')
            w_city = request.form.get('w_city')
            w_state = request.form.get('w_state')

            # Update Worker details
            cur.execute("UPDATE half_form SET no_family_mem=?, worker_detail_worker_legal_status=?, worker_detail_name_of_worker=?, worker_detail_gender=?, worker_detail_DOB=?, worker_detail_citizenship=?, worker_detail_marital_status=?, worker_detail_religion=?, worker_detail_contact_no=?, worker_emp_dtl_address1=?, worker_emp_dtl_address2=?, worker_emp_dtl_address3=?, worker_emp_dtl_postcode=?, worker_emp_dtl_city=?, worker_emp_dtl_state=? WHERE id=?", (w_fm_no, w_status, w_name, w_gender, w_dob, w_citizenship, w_marital_status, w_religion, w_contact_no, w_address1, w_address2, w_address3, w_postcode, w_city, w_state, w_id))
            conn.commit()
            conn.close()

            session['registration_list_update2'] = 'success'
            return redirect(f'/subusers-registration-list?q={regL_path}')
        else:
            response = {
                'status': 'error',
                'msg': 'method error'
            }
            return jsonify(response)
    else:
        return redirect('/')



# Update Registered Worker Docs
@app.route("/update-worker-docs2", methods=['POST'])
def updateWorkerDocs2():
    if 'user_session' in session:
        if request.method == 'POST':
            conn = get_db_connection()
            cur = conn.cursor()

            regL_path = session.get('regList_path')

            docs_id = request.form.get('docs_id')
            type_of_document = request.form.get('type_of_document')
            document_id = request.form.get('document_id')
            place_of_issue = request.form.get('place_of_issue')
            issue_date = request.form.get('issue_date')

            expiry_date = request.form.get('expiry_date')
            issuing_country = request.form.get('issuing_country')
            document_status = request.form.get('document_status')
            document_current_status = request.form.get('document_current_status')
        
            # Update Worker details
            cur.execute("UPDATE workers_document SET type_of_douments=?, document_id=?, place_of_issue=?, document_issued_date=?, document_expiry_date=?, issuing_country=?, document_status=?, status_of_current_document=?  WHERE id=?", (type_of_document, document_id, place_of_issue, issue_date, expiry_date, issuing_country, document_status, document_current_status, docs_id))
            conn.commit()
            conn.close()
            session['registration_list_update2'] = 'success'
            return redirect(f'/subusers-registration-list?q={regL_path}')   
        else:
            response = {
                'status': 'error',
                'msg': 'method error'
            }
            return jsonify(response)
    else:
        return redirect('/')


# edit-family-member
@app.route("/edit-family-member2", methods=['GET', 'POST'])
def editFamilyMember2():
    if 'user_session' in session:
        active_user_session = session.get('user_session')
        regL_path = session.get('regList_path')

        try:
            fmId = request.args.get('fm')
            conn = get_db_connection()
            cur = conn.cursor()

            # fetch workers
            cur.execute("SELECT * FROM family_form where id=? AND form_created_by=?", (fmId, active_user_session))
            fmData = cur.fetchall()

            # get Family member Path details
            fmRegNo =  fmData[0][4]
            formUniqueKey = fmData[0][3]
            cur.execute("SELECT id, form_worker_reg_no FROM half_form WHERE form_unique_key=?", (formUniqueKey,))
            workerRegN = cur.fetchall()
            if workerRegN:
                workerId = workerRegN[0][0]
                

            return render_template('edit-family-member2.html', wori=workerId, regL_path=regL_path, fmData=fmData)
        except Exception as e:
            return redirect('/subusers-registration-list')
    else:
        return redirect('/')
    

# Update Family Member
@app.route("/update-family-member2", methods=['POST'])
def updateFamilyMember2():
    if 'user_session' in session:
        
        if request.method == 'POST':
            regL_path = session.get('regList_path')
            conn = get_db_connection()
            cur = conn.cursor()

            fm_id = request.form.get('fm_id')

            fm_name = request.form.get('fm_name')
            fm_relationship = request.form.get('fm_relationship')
            fm_family_name = request.form.get('fm_family_name')
            family_together = request.form.get('family_together')
            poe = request.form.get('poe')

            gender = request.form.get('gender')
            marital_status = request.form.get('marital_status')
            citizenship = request.form.get('citizenship')
            religion = request.form.get('religion')
            address1 = request.form.get('address1')

            address2 = request.form.get('address2')
            address3 = request.form.get('address3')
            postcode = request.form.get('postcode')
            city = request.form.get('city')
            state = request.form.get('state')

            contact_no = request.form.get('contact_no')
            race = request.form.get('race')
            place_of_birth = request.form.get('place_of_birth')
            employee_status = request.form.get('employee_status')
            employee_name = request.form.get('employee_name')
            employee_address = request.form.get('employee_address')

            # Docs 1
            type_of_document1 = request.form.get('type_of_document1')
            document_id1 = request.form.get('document_id1')
            place_of_issue1 = request.form.get('place_of_issue1')
            issue_date1 = request.form.get('issue_date1')
            expiry_date1 = request.form.get('expiry_date1')
            issuing_country1 = request.form.get('issuing_country1')
            document_status1 = request.form.get('document_status1')
            document_current_status1 = request.form.get('document_current_status1')

            # Docs 2
            type_of_document2 = request.form.get('type_of_document2')
            document_id2 = request.form.get('document_id2')
            place_of_issue2 = request.form.get('place_of_issue2')
            issue_date2 = request.form.get('issue_date2')
            expiry_date2 = request.form.get('expiry_date2')
            issuing_country2 = request.form.get('issuing_country2')
            document_status2 = request.form.get('document_status2')
            document_current_status2 = request.form.get('document_current_status2')
        
            # Update Worker details
            cur.execute("UPDATE family_form SET family_form_name_of_family_member=?, family_form_relationship=?, family_form_family_name=?, family_form_is_famliy_togther=?, family_form_family_form_poe=?, family_form_gender=?, family_form_marital_status=?, family_form_citizenship=?, family_form_religion=?, family_form_address1=?, family_form_address2=?, family_form_address3=?, family_form_postcode=?, family_form_city=?, family_form_state=?, family_form_contact_no=?, family_form_race=?, family_form_place_of_birth=?, family_form_emp_status=?, family_form_emp_name=?, family_form_emp_address=?, fmDoc1_type_of_documents=?, fmDoc1_document_id=?, fmDoc1_place_of_issue=?, fmDoc1_document_issued_date=?, fmDoc1_document_expiry_date=?, fmDoc1_issuing_country=?, fmDoc1_document_status=?, fmDoc1_status_of_current_document=?, fmDoc2_type_of_documents=?, fmDoc2_document_id=?, fmDoc2_place_of_issue=?, fmDoc2_document_issued_date=?, fmDoc2_document_expiry_date=?, fmDoc2_issuing_country=?, fmDoc2_document_status=?, fmDoc2_status_of_current_document=? WHERE id=?", (fm_name, fm_relationship, fm_family_name, family_together, poe, gender, marital_status, citizenship, religion, address1, address2, address3, postcode, city, state, contact_no, race, place_of_birth, employee_status, employee_name, employee_address, type_of_document1, document_id1, place_of_issue1, issue_date1, expiry_date1, issuing_country1, document_status1, document_current_status1, type_of_document2, document_id2, place_of_issue2, issue_date2, expiry_date2, issuing_country2, document_status2, document_current_status2, fm_id))
            conn.commit()
            conn.close()
            session['registration_list_update2'] = 'success'
            return redirect(f'/subusers-registration-list?q={regL_path}')   
        else:
            response = {
                'status': 'error',
                'msg': 'method error'
            }
            return jsonify(response)
    else:
        return redirect('/')
    
# delete workers and their family members
@app.route("/del-registered-worker2", methods=['GET'])
def delRegisteredWorker2():
    if 'user_session' in session:
        active_user_session = session.get('user_session')
        regL_path = session.get('regList_path')
        try:
            worker_id = request.args.get('del')
            conn = get_db_connection()
            cur = conn.cursor()

            # fetch workers
            cur.execute("SELECT form_unique_key FROM half_form where id=? AND form_created_by=?", (worker_id, active_user_session))
            workerKey = cur.fetchall()
            form_unique_key = workerKey[0][0]

            # del worker
            cur.execute("DELETE FROM half_form WHERE id=? AND form_created_by=?", (worker_id, active_user_session))
            # del worker documents
            cur.execute("DELETE FROM workers_document where form_unique_key=?", (form_unique_key,))
            # del worker family members
            cur.execute("DELETE FROM family_form where form_unique_key=?", (form_unique_key,))
            
            conn.commit()
            conn.close()
            session['registration_list_delete2'] = 'success'
            return redirect(f'/subusers-registration-list?q={regL_path}')
        except Exception as e:
            return redirect(f'/subusers-registration-list?q={regL_path}')
    else:
        return redirect('/')

# -- End * Sub users List --






# Download Excel File
@app.route('/download-excel-file', methods=['GET'])
def download_log():
    if 'user_session' in session:
        scheme = request.scheme
        port = request.environ.get('SERVER_PORT')
    
        active_user_session = session.get('user_session')

        conn = get_db_connection()
        cur = conn.cursor()
        
        workerData = request.args.get('file')

        #  Single Id
        def check_num(num):
            if num.isdigit():
                return 'single_id'    
            return None
        
        result_single = check_num(workerData)
        
        if workerData == 'exportAll':
            cur.execute("SELECT form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe,worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, form_position, form_status, form_unique_key FROM half_form WHERE form_created_by=?", (active_user_session,))
            #log = cur.fetchall()
            log1 = cur.fetchall()

            # testing Code
            log = []

            for worker_allData in log1:

                excelWorker = ['WORKER', worker_allData[0], worker_allData[1], worker_allData[2], worker_allData[3], worker_allData[4], worker_allData[5], worker_allData[6], worker_allData[7], worker_allData[8], worker_allData[9], worker_allData[10], worker_allData[11], worker_allData[12], worker_allData[13], worker_allData[14], worker_allData[15], worker_allData[16], worker_allData[17], worker_allData[18], worker_allData[19], worker_allData[20], worker_allData[21], worker_allData[22], worker_allData[23], worker_allData[24], worker_allData[25], worker_allData[26], worker_allData[27], worker_allData[28], worker_allData[29], worker_allData[30]]
                excel_formUniqueKey = worker_allData[31]
                #print(excel_formUniqueKey)

                docs_level = ['', 'Type of Document', 'Document ID', 'Place of Issue', 'Issue Date', 'Expiry Date', 'Issuing Country', 'Document Status', 'Status of Current Document', 'Document Link']
                
                # push all worker data & docs level
                log.append(excelWorker)
                log.append([''])
                log.append(docs_level)
                
                # Worker Documents
                cur.execute("SELECT * FROM workers_document WHERE form_unique_key=?", (excel_formUniqueKey,))
                excel_workerDocs = cur.fetchall()
                docsIndex = 1
                for xWDocs in excel_workerDocs:
                    xWorkerData = [ f"Document {docsIndex}", xWDocs[3], xWDocs[4], xWDocs[5], xWDocs[6], xWDocs[7], xWDocs[8], xWDocs[9], xWDocs[10], f'{scheme}://{ip_address}:{port}/static/documents/{active_user_session}Docs/{worker_allData[2]}/doc{docsIndex}/uploaded_image.jpg']
                    #print(xWorkerData)
                    log.append(xWorkerData)
                    docsIndex += 1

                # Worker Family Members Labels
                fm_label = ['', 'Created by', 'Created Date', 'Registration No', 'Worker Name', 'Relationship', 'Name', 'Family Name', 'Is Family Together', 'Point of Entry', 'Citizenship', 'Religion', 'Marital Status', 'Gender', 'Address 1', 'Address 2', 'Address 3', 'Postcode', 'City', 'State', 'Contact No', 'Race', 'Place of Birth', 'Employment Status', 'Employer Name', 'Employer Address', 'Type of Document 1', 'Document ID 1', 'Place of Issue 1', 'Issued Date 1', 'Expiry Date 1', 'Issuing Country 1', 'Document Status 1', 'Status of Current Document 1', 'Document Link 1', 'Type of Document 2', 'Document ID 2', 'Place of Issue 2', 'Issued Date 2', 'Expiry Date 2', 'Issuing Country 2', 'Document Status 2', 'Status of Current Document 2', 'Document Link 2']
                log.append([''])
                log.append(fm_label)

                # Worker Family Members
                cur.execute("SELECT * FROM family_form WHERE form_unique_key=?", (excel_formUniqueKey,))
                excel_workerFM = cur.fetchall()
                fmIndex = 1
                for xW_FM in excel_workerFM:
                    xWorkerFM = [ f"Family Member {fmIndex}", xW_FM[1], xW_FM[2], f"{worker_allData[2]}-{fmIndex}", xW_FM[5], xW_FM[6], xW_FM[7], xW_FM[8], xW_FM[9], xW_FM[10], xW_FM[11], xW_FM[12], xW_FM[13], xW_FM[14], xW_FM[15], xW_FM[16], xW_FM[17], xW_FM[18], xW_FM[19], xW_FM[20], xW_FM[21], xW_FM[22], xW_FM[23], xW_FM[24], xW_FM[25], xW_FM[26], xW_FM[30], xW_FM[31], xW_FM[32], xW_FM[33], xW_FM[34], xW_FM[35], xW_FM[36], xW_FM[37], f'{scheme}://{ip_address}:{port}/static/documents/{active_user_session}Docs/{worker_allData[2]}/familyMember/{xW_FM[4]}/doc1/uploaded_image.jpg', xW_FM[38], xW_FM[39], xW_FM[40], xW_FM[41], xW_FM[42], xW_FM[43], xW_FM[44], xW_FM[45], f'{scheme}://{ip_address}:{port}/static/documents/{active_user_session}Docs/{worker_allData[2]}/familyMember/{xW_FM[4]}/doc2/uploaded_image.jpg']
                    #print(xWorkerFM)
                    log.append(xWorkerFM)
                    fmIndex += 1

                log.append([''])
                # End testing Code

        elif result_single == 'single_id':
            workerId = workerData
            cur.execute("SELECT form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe,worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, form_position, form_status, form_unique_key FROM half_form where id=? AND form_created_by=?", (workerId, active_user_session))
            #log = cur.fetchall()

            # testing Code
            log = []

            log1 = cur.fetchall()
            
            excelWorker = ['WORKER', log1[0][0], log1[0][1], log1[0][2], log1[0][3], log1[0][4], log1[0][5], log1[0][6], log1[0][7], log1[0][8], log1[0][9], log1[0][10], log1[0][11], log1[0][12], log1[0][13], log1[0][14], log1[0][15], log1[0][16], log1[0][17], log1[0][18], log1[0][19], log1[0][20], log1[0][21], log1[0][22], log1[0][23], log1[0][24], log1[0][25], log1[0][26], log1[0][27], log1[0][28], log1[0][29], log1[0][30]]
            excel_formUniqueKey = log1[0][31]
            #print(excel_formUniqueKey)

            docs_level = ['', 'Type of Document', 'Document ID', 'Place of Issue', 'Issue Date', 'Expiry Date', 'Issuing Country', 'Document Status', 'Status of Current Document', 'Document Link']
            
            # push all worker data & docs level
            log.append(excelWorker)
            log.append([''])
            log.append(docs_level)
            
            # Worker Documents
            cur.execute("SELECT * FROM workers_document WHERE form_unique_key=?", (excel_formUniqueKey,))
            excel_workerDocs = cur.fetchall()
            docsIndex = 1
            for xWDocs in excel_workerDocs:
                xWorkerData = [ f"Document {docsIndex}", xWDocs[3], xWDocs[4], xWDocs[5], xWDocs[6], xWDocs[7], xWDocs[8], xWDocs[9], xWDocs[10], f'{scheme}://{ip_address}:{port}/static/documents/{active_user_session}Docs/{log1[0][2]}/doc{docsIndex}/uploaded_image.jpg']
                #print(xWorkerData)
                log.append(xWorkerData)
                docsIndex += 1

            # Worker Family Members Labels
            fm_label = ['', 'Created by', 'Created Date', 'Registration No', 'Worker Name', 'Relationship', 'Name', 'Family Name', 'Is Family Together', 'Point of Entry', 'Citizenship', 'Religion', 'Marital Status', 'Gender', 'Address 1', 'Address 2', 'Address 3', 'Postcode', 'City', 'State', 'Contact No', 'Race', 'Place of Birth', 'Employment Status', 'Employer Name', 'Employer Address', 'Type of Document 1', 'Document ID 1', 'Place of Issue 1', 'Issued Date 1', 'Expiry Date 1', 'Issuing Country 1', 'Document Status 1', 'Status of Current Document 1', 'Document Link 1', 'Type of Document 2', 'Document ID 2', 'Place of Issue 2', 'Issued Date 2', 'Expiry Date 2', 'Issuing Country 2', 'Document Status 2', 'Status of Current Document 2', 'Document Link 2']
            log.append([''])
            log.append(fm_label)

            # Worker Family Members
            cur.execute("SELECT * FROM family_form WHERE form_unique_key=?", (excel_formUniqueKey,))
            excel_workerFM = cur.fetchall()
            fmIndex = 1
            for xW_FM in excel_workerFM:
                xWorkerFM = [ f"Family Member {fmIndex}", xW_FM[1], xW_FM[2], f"{log1[0][2]}-{fmIndex}", xW_FM[5], xW_FM[6], xW_FM[7], xW_FM[8], xW_FM[9], xW_FM[10], xW_FM[11], xW_FM[12], xW_FM[13], xW_FM[14], xW_FM[15], xW_FM[16], xW_FM[17], xW_FM[18], xW_FM[19], xW_FM[20], xW_FM[21], xW_FM[22], xW_FM[23], xW_FM[24], xW_FM[25], xW_FM[26], xW_FM[30], xW_FM[31], xW_FM[32], xW_FM[33], xW_FM[34], xW_FM[35], xW_FM[36], xW_FM[37], f'{scheme}://{ip_address}:{port}/static/documents/{active_user_session}Docs/{log1[0][2]}/familyMember/{xW_FM[4]}/doc1/uploaded_image.jpg', xW_FM[38], xW_FM[39], xW_FM[40], xW_FM[41], xW_FM[42], xW_FM[43], xW_FM[44], xW_FM[45], f'{scheme}://{ip_address}:{port}/static/documents/{active_user_session}Docs/{log1[0][2]}/familyMember/{xW_FM[4]}/doc2/uploaded_image.jpg']
                #print(xWorkerFM)
                log.append(xWorkerFM)
                fmIndex += 1

            log.append([''])
            # End testing Code

        else:
            workerId = json.loads(workerData)
            cur.execute("SELECT form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe,worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, form_position, form_status, form_unique_key FROM half_form WHERE id IN ("+workerId+") AND form_created_by='"+active_user_session+"'")
            log1 = cur.fetchall()

            # testing Code
            log = []

            for worker_allData in log1:

                excelWorker = ['WORKER', worker_allData[0], worker_allData[1], worker_allData[2], worker_allData[3], worker_allData[4], worker_allData[5], worker_allData[6], worker_allData[7], worker_allData[8], worker_allData[9], worker_allData[10], worker_allData[11], worker_allData[12], worker_allData[13], worker_allData[14], worker_allData[15], worker_allData[16], worker_allData[17], worker_allData[18], worker_allData[19], worker_allData[20], worker_allData[21], worker_allData[22], worker_allData[23], worker_allData[24], worker_allData[25], worker_allData[26], worker_allData[27], worker_allData[28], worker_allData[29], worker_allData[30]]
                excel_formUniqueKey = worker_allData[31]
                #print(excel_formUniqueKey)

                docs_level = ['', 'Type of Document', 'Document ID', 'Place of Issue', 'Issue Date', 'Expiry Date', 'Issuing Country', 'Document Status', 'Status of Current Document', 'Document Link']
                
                # push all worker data & docs level
                log.append(excelWorker)
                log.append([''])
                log.append(docs_level)
                
                # Worker Documents
                cur.execute("SELECT * FROM workers_document WHERE form_unique_key=?", (excel_formUniqueKey,))
                excel_workerDocs = cur.fetchall()
                docsIndex = 1
                for xWDocs in excel_workerDocs:
                    xWorkerData = [ f"Document {docsIndex}", xWDocs[3], xWDocs[4], xWDocs[5], xWDocs[6], xWDocs[7], xWDocs[8], xWDocs[9], xWDocs[10], f'{scheme}://{ip_address}:{port}/static/documents/{active_user_session}Docs/{worker_allData[2]}/doc{docsIndex}/uploaded_image.jpg']
                    #print(xWorkerData)
                    log.append(xWorkerData)
                    docsIndex += 1

                # Worker Family Members Labels
                fm_label = ['', 'Created by', 'Created Date', 'Registration No', 'Worker Name', 'Relationship', 'Name', 'Family Name', 'Is Family Together', 'Point of Entry', 'Citizenship', 'Religion', 'Marital Status', 'Gender', 'Address 1', 'Address 2', 'Address 3', 'Postcode', 'City', 'State', 'Contact No', 'Race', 'Place of Birth', 'Employment Status', 'Employer Name', 'Employer Address', 'Type of Document 1', 'Document ID 1', 'Place of Issue 1', 'Issued Date 1', 'Expiry Date 1', 'Issuing Country 1', 'Document Status 1', 'Status of Current Document 1', 'Document Link 1', 'Type of Document 2', 'Document ID 2', 'Place of Issue 2', 'Issued Date 2', 'Expiry Date 2', 'Issuing Country 2', 'Document Status 2', 'Status of Current Document 2', 'Document Link 2']
                log.append([''])
                log.append(fm_label)

                # Worker Family Members
                cur.execute("SELECT * FROM family_form WHERE form_unique_key=?", (excel_formUniqueKey,))
                excel_workerFM = cur.fetchall()
                fmIndex = 1
                for xW_FM in excel_workerFM:
                    xWorkerFM = [ f"Family Member {fmIndex}", xW_FM[1], xW_FM[2], f"{worker_allData[2]}-{fmIndex}", xW_FM[5], xW_FM[6], xW_FM[7], xW_FM[8], xW_FM[9], xW_FM[10], xW_FM[11], xW_FM[12], xW_FM[13], xW_FM[14], xW_FM[15], xW_FM[16], xW_FM[17], xW_FM[18], xW_FM[19], xW_FM[20], xW_FM[21], xW_FM[22], xW_FM[23], xW_FM[24], xW_FM[25], xW_FM[26], xW_FM[30], xW_FM[31], xW_FM[32], xW_FM[33], xW_FM[34], xW_FM[35], xW_FM[36], xW_FM[37], f'{scheme}://{ip_address}:{port}/static/documents/{active_user_session}Docs/{worker_allData[2]}/familyMember/{xW_FM[4]}/doc1/uploaded_image.jpg', xW_FM[38], xW_FM[39], xW_FM[40], xW_FM[41], xW_FM[42], xW_FM[43], xW_FM[44], xW_FM[45], f'{scheme}://{ip_address}:{port}/static/documents/{active_user_session}Docs/{worker_allData[2]}/familyMember/{xW_FM[4]}/doc2/uploaded_image.jpg']
                    #print(xWorkerFM)
                    log.append(xWorkerFM)
                    fmIndex += 1

                log.append([''])
                # End testing Code

        
        def generate():
            data = StringIO()
            w = csv.writer(data)

            # write header
            w.writerow(('', 'Created by', 'Created Date', 'Registration No', 'No of Family Member', 'Legal Status', 'Name of Worker', 'Family Name', 'Gender', 'Date of Birth', 'Place of Birth', 'Citizenship', 'Marital Status', 'Point of Entry', 'Religion', 'Race', 'Contact No', 'E-mail', 'NOK', 'Relationship', 'NOK Contact No', 'Job Sector', 'Job Sub Sector', 'Employment Sponsorship Status', 'Address 1', 'Address 2', 'Address 3', 'Postcode', 'City', 'State', 'Position', 'Status'))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

            # write each log item
            for item in log:
                w.writerow(item)
                yield data.getvalue()
                data.seek(0)
                data.truncate(0)

        # stream the response as the data is generated
        response = Response(generate(), mimetype='application/vnd.ms-excel')
        # add a filename
        response.headers.set("Content-Disposition", "attachment", filename="worker.csv")
        return response
    else:
        return redirect('/')





# registration-log  
@app.route("/registration-log", methods=['GET', 'POST'])
def registrationLog():
    if 'user_session' in session:

        conn = get_db_connection()
        cur = conn.cursor()

        active_user_session = session.get('user_session')
        
        previous_7th_date = previous_seventh_date()

        # reg. worker Current Day
        cur.execute('SELECT * FROM half_form where form_created_by=? AND form_created_date=?', (active_user_session, current_date))
        regWorkerDay = cur.fetchall()
        regWorkerDay = len(regWorkerDay)
        
        # reg. Family member Current Day
        cur.execute('SELECT * FROM family_form where form_created_by=? AND form_created_date=?', (active_user_session, current_date))
        regMemberDay = cur.fetchall()
        regMemberDay = len(regMemberDay)
        regNumber = regWorkerDay + regMemberDay
        
        # reg. worker Current Week
        cur.execute('SELECT * FROM half_form where form_created_by=? AND form_created_date BETWEEN ? AND ?', (active_user_session, previous_7th_date, current_date))
        regWorkerWeek = cur.fetchall()
        regWorkerWeek = len(regWorkerWeek)
        
        # reg. Family member Current Week
        cur.execute('SELECT * FROM family_form where form_created_by=? AND form_created_date BETWEEN ? AND ?', (active_user_session, previous_7th_date, current_date))
        regMemberWeek = cur.fetchall()
        regMemberWeek = len(regMemberWeek)
        regNumberWeek = regWorkerWeek + regMemberWeek
        

        # Legal status
        cur.execute('SELECT * FROM half_form WHERE form_created_by=? AND worker_detail_worker_legal_status=? AND form_created_date BETWEEN ? AND ?', (active_user_session, 'Legal', previous_7th_date, current_date)) 
        totalLegal = cur.fetchall()
        totalLegal = len(totalLegal)

        # illegal status
        cur.execute('SELECT * FROM half_form WHERE form_created_by=? AND worker_detail_worker_legal_status=? AND form_created_date BETWEEN ? AND ?', (active_user_session, 'Illegal', previous_7th_date, current_date))
        totalIllegal = cur.fetchall()
        totalIllegal = len(totalIllegal)
        
        return render_template('registration-log.html', regNumber=regNumber, memberReg=regMemberDay, totalWorker=regWorkerDay, grandTotal=regNumberWeek, totalLegal=totalLegal, totalIllegal=totalIllegal)
    else:
        return redirect('/')


#  my-registration-log  
@app.route("/my-registration-log", methods=['GET', 'POST'])
def myRegistrationLog():
    if 'user_session' in session:
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            active_user_session = session.get('user_session')

            # Get form Unique Key 
            subUsers_form_unique_key_list = []
            subUser_q = cur.execute("SELECT form_unique_key FROM sub_users_datalog WHERE parent=?", (active_user_session,))
            form_unique_key = subUser_q.fetchall()

            for key in form_unique_key:
                subUsers_form_unique_key_list.append(key[0])

            form_unique_key_tuple = tuple(subUsers_form_unique_key_list)
            form_key_as_string = ', '.join(form_unique_key_tuple)
            
            
            previous_7th_date = previous_seventh_date()

            # reg. worker Current Day
            #cur.execute('SELECT * FROM half_form where form_created_by=? AND form_created_date=? AND form_unique_key IN (?)', (active_user_session, current_date, form_unique_key_tuple))
            #regWorkerDay = cur.fetchall()
            #print('RegLog: ', regWorkerDay)
            #regWorkerDay = len(regWorkerDay)

            placeholders = ', '.join(['?'] * len(form_unique_key_tuple))
            query = f'SELECT * FROM half_form WHERE form_created_by=? AND form_created_date=? AND form_unique_key NOT IN ({placeholders})'
            parameters = (active_user_session, current_date) + form_unique_key_tuple
            # Execute the query
            cur.execute(query, parameters)
            # Fetch the results
            regWorkerDay = cur.fetchall()
            regWorkerDay = len(regWorkerDay)

            # reg. Family member Current Day
            query2 = f'SELECT * FROM family_form WHERE form_created_by=? AND form_created_date=? AND form_unique_key NOT IN ({placeholders})'
            parameters2 = (active_user_session, current_date) + form_unique_key_tuple
            cur.execute(query2, parameters2)
            regMemberDay = cur.fetchall()

            #cur.execute('SELECT * FROM family_form where form_created_by=? AND form_created_date=?', (active_user_session, current_date))
            #regMemberDay = cur.fetchall()
            regMemberDay = len(regMemberDay)
            regNumber = regWorkerDay + regMemberDay

            
            # reg. worker Current Week
            #cur.execute('SELECT * FROM half_form where form_created_by=? AND form_created_date BETWEEN ? AND ?', (active_user_session, previous_7th_date, current_date))
            #regWorkerWeek = cur.fetchall()
            #regWorkerWeek = len(regWorkerWeek)

            query3 = f'SELECT * FROM half_form WHERE form_created_by=? AND form_created_date BETWEEN ? AND ? AND form_unique_key NOT IN ({placeholders})'
            parameters3 = (active_user_session, previous_7th_date, current_date) + form_unique_key_tuple
            cur.execute(query3, parameters3)
            regWorkerWeek = cur.fetchall()
            regWorkerWeek = len(regWorkerWeek)


            # reg. Family member Current Week
            #cur.execute('SELECT * FROM family_form where form_created_by=? AND form_created_date BETWEEN ? AND ?', (active_user_session, previous_7th_date, current_date))
            #regMemberWeek = cur.fetchall()
            #regMemberWeek = len(regMemberWeek)
            #regNumberWeek = regWorkerWeek + regMemberWeek

            query4 = f'SELECT * FROM family_form WHERE form_created_by=? AND form_created_date BETWEEN ? AND ? AND form_unique_key NOT IN ({placeholders})'
            parameters4 = (active_user_session, previous_7th_date, current_date) + form_unique_key_tuple
            cur.execute(query4, parameters4)
            regMemberWeek = cur.fetchall()
            regMemberWeek = len(regMemberWeek)
            regNumberWeek = regWorkerWeek + regMemberWeek
            

            # Legal status
            #cur.execute('SELECT * FROM half_form WHERE form_created_by=? AND worker_detail_worker_legal_status=? AND form_created_date BETWEEN ? AND ?', (active_user_session, 'Legal', previous_7th_date, current_date)) 
            #totalLegal = cur.fetchall()
            #totalLegal = len(totalLegal)
            query5 = f'SELECT * FROM half_form WHERE form_created_by=? AND worker_detail_worker_legal_status=? AND form_created_date BETWEEN ? AND ? AND form_unique_key NOT IN ({placeholders})'
            parameters5 = (active_user_session, 'Legal', previous_7th_date, current_date) + form_unique_key_tuple
            cur.execute(query5, parameters5)
            totalLegal = cur.fetchall()
            totalLegal = len(totalLegal)


            # illegal status
            #cur.execute('SELECT * FROM half_form WHERE form_created_by=? AND worker_detail_worker_legal_status=? AND form_created_date BETWEEN ? AND ?', (active_user_session, 'Illegal', previous_7th_date, current_date))
            #totalIllegal = cur.fetchall()
            #totalIllegal = len(totalIllegal)
            query6 = f'SELECT * FROM half_form WHERE form_created_by=? AND worker_detail_worker_legal_status=? AND form_created_date BETWEEN ? AND ? AND form_unique_key NOT IN ({placeholders})'
            parameters6 = (active_user_session, 'Illegal', previous_7th_date, current_date) + form_unique_key_tuple
            cur.execute(query6, parameters6)
            totalIllegal = cur.fetchall()
            totalIllegal = len(totalIllegal)
            
            return render_template('my-registration-log.html', regNumber=regNumber, memberReg=regMemberDay, totalWorker=regWorkerDay, grandTotal=regNumberWeek, totalLegal=totalLegal, totalIllegal=totalIllegal)

        except Exception as e:
            return redirect('/add-worker')
    else:
        return redirect('/')



# My sub users list 
@app.route("/my-subusers-list", methods=['GET', 'POST'])
def mySubUsersList():
    if 'user_session' in session:
        try:
            active_user_session = session.get('user_session')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()
            # Check
            cur.execute('SELECT * FROM sub_users WHERE creator=?', (active_user_session,))
            subUsers = cur.fetchall()
            subUsersLen = len(subUsers)
            return render_template('/my-subusers-list.html', subUsersList=subUsers, totalSubUsers=subUsersLen)
        
        except Exception as e:
            return redirect('/add-worker')
    else:
        return redirect('/') 

# Sub USers Registration Log
@app.route("/subusers-registration-log", methods=['GET'])
def subusers_registration_log():
    if 'user_session' in session:
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            subUser_session = request.args.get('q')

            # get Sub User Parent 
            subUser_root = cur.execute("SELECT creator FROM sub_users WHERE username=?", (subUser_session,))
            subUser_root = subUser_root.fetchall()
            subUser_rootLen = len(subUser_root)
            if subUser_rootLen == 0:
                return render_template('/')
            # subUserRoot
            active_user_session = subUser_root[0][0]

            # Get form Unique Key 
            form_unique_key_list = []
            subUser_q = cur.execute("SELECT form_unique_key FROM sub_users_datalog WHERE creator=?", (subUser_session,))
            form_unique_key = subUser_q.fetchall()

            for key in form_unique_key:
                form_unique_key_list.append(key[0])

            form_unique_key_tuple = tuple(form_unique_key_list)
            form_key_as_string = ', '.join(form_unique_key_tuple)
            
            
            previous_7th_date = previous_seventh_date()

            # reg. worker Current Day
            #cur.execute('SELECT * FROM half_form where form_created_by=? AND form_created_date=? AND form_unique_key IN (?)', (active_user_session, current_date, form_unique_key_tuple))
            #regWorkerDay = cur.fetchall()
            #print('RegLog: ', regWorkerDay)
            #regWorkerDay = len(regWorkerDay)

            placeholders = ', '.join(['?'] * len(form_unique_key_tuple))
            query = f'SELECT * FROM half_form WHERE form_created_by=? AND form_created_date=? AND form_unique_key IN ({placeholders})'
            parameters = (active_user_session, current_date) + form_unique_key_tuple
            # Execute the query
            cur.execute(query, parameters)
            # Fetch the results
            regWorkerDay = cur.fetchall()
            regWorkerDay = len(regWorkerDay)

            # reg. Family member Current Day
            query2 = f'SELECT * FROM family_form WHERE form_created_by=? AND form_created_date=? AND form_unique_key IN ({placeholders})'
            parameters2 = (active_user_session, current_date) + form_unique_key_tuple
            cur.execute(query2, parameters2)
            regMemberDay = cur.fetchall()

            #cur.execute('SELECT * FROM family_form where form_created_by=? AND form_created_date=?', (active_user_session, current_date))
            #regMemberDay = cur.fetchall()
            regMemberDay = len(regMemberDay)
            regNumber = regWorkerDay + regMemberDay

            
            # reg. worker Current Week
            #cur.execute('SELECT * FROM half_form where form_created_by=? AND form_created_date BETWEEN ? AND ?', (active_user_session, previous_7th_date, current_date))
            #regWorkerWeek = cur.fetchall()
            #regWorkerWeek = len(regWorkerWeek)

            query3 = f'SELECT * FROM half_form WHERE form_created_by=? AND form_created_date BETWEEN ? AND ? AND form_unique_key IN ({placeholders})'
            parameters3 = (active_user_session, previous_7th_date, current_date) + form_unique_key_tuple
            cur.execute(query3, parameters3)
            regWorkerWeek = cur.fetchall()
            regWorkerWeek = len(regWorkerWeek)


            # reg. Family member Current Week
            #cur.execute('SELECT * FROM family_form where form_created_by=? AND form_created_date BETWEEN ? AND ?', (active_user_session, previous_7th_date, current_date))
            #regMemberWeek = cur.fetchall()
            #regMemberWeek = len(regMemberWeek)
            #regNumberWeek = regWorkerWeek + regMemberWeek

            query4 = f'SELECT * FROM family_form WHERE form_created_by=? AND form_created_date BETWEEN ? AND ? AND form_unique_key IN ({placeholders})'
            parameters4 = (active_user_session, previous_7th_date, current_date) + form_unique_key_tuple
            cur.execute(query4, parameters4)
            regMemberWeek = cur.fetchall()
            regMemberWeek = len(regMemberWeek)
            regNumberWeek = regWorkerWeek + regMemberWeek
            

            # Legal status
            #cur.execute('SELECT * FROM half_form WHERE form_created_by=? AND worker_detail_worker_legal_status=? AND form_created_date BETWEEN ? AND ?', (active_user_session, 'Legal', previous_7th_date, current_date)) 
            #totalLegal = cur.fetchall()
            #totalLegal = len(totalLegal)
            query5 = f'SELECT * FROM half_form WHERE form_created_by=? AND worker_detail_worker_legal_status=? AND form_created_date BETWEEN ? AND ? AND form_unique_key IN ({placeholders})'
            parameters5 = (active_user_session, 'Legal', previous_7th_date, current_date) + form_unique_key_tuple
            cur.execute(query5, parameters5)
            totalLegal = cur.fetchall()
            totalLegal = len(totalLegal)


            # illegal status
            #cur.execute('SELECT * FROM half_form WHERE form_created_by=? AND worker_detail_worker_legal_status=? AND form_created_date BETWEEN ? AND ?', (active_user_session, 'Illegal', previous_7th_date, current_date))
            #totalIllegal = cur.fetchall()
            #totalIllegal = len(totalIllegal)
            query6 = f'SELECT * FROM half_form WHERE form_created_by=? AND worker_detail_worker_legal_status=? AND form_created_date BETWEEN ? AND ? AND form_unique_key IN ({placeholders})'
            parameters6 = (active_user_session, 'Illegal', previous_7th_date, current_date) + form_unique_key_tuple
            cur.execute(query6, parameters6)
            totalIllegal = cur.fetchall()
            totalIllegal = len(totalIllegal)
            
            return render_template('subusers-registration-log.html', regNumber=regNumber, memberReg=regMemberDay, totalWorker=regWorkerDay, grandTotal=regNumberWeek, totalLegal=totalLegal, totalIllegal=totalIllegal)

        except Exception as e:
            redirect('/my-subusers-list')
    else:
        redirect('/')    


# Print QR Code
@app.route("/print-qr-code", methods=['GET', 'POST'])
def printQrCode():
    if 'user_session' in session:
        active_user_session = session.get('user_session')

        conn = get_db_connection()
        cur = conn.cursor()
        totalWorker = cur.execute("SELECT id, form_worker_reg_no, worker_detail_name_of_worker, form_status FROM half_form WHERE form_created_by=?", (active_user_session,))
        workerD = cur.fetchall()
        totalWorker = len(workerD)
        return render_template('print-qr-code.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')
    

# Worker Details
@app.route("/worker-details", methods=['GET', 'POST'])
def workerDetails():
    if 'user_session' in session:
        active_user_session = session.get('user_session')

        workerId = request.args.get('wrkr')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, form_worker_reg_no, worker_detail_name_of_worker, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state form_status FROM half_form WHERE id=? AND form_created_by=?", (workerId, active_user_session))
        workerD = cur.fetchall()
        totalWorker = len(workerD)
        return render_template('worker-details.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')
    

# Print QR
@app.route("/print-qr", methods=['GET', 'POST'])
def printQr():
    if 'user_session' in session:
        active_user_session = session.get('user_session')

        status = request.args.get('status')
        workerName = request.args.get('name')
        workerRegNum = request.args.get('regN')
        
        if status == 'qr':
            return render_template('print-qr.html', workerName=workerName, workerRegNum=workerRegNum)
        elif status == 'qr-3x3':
            return render_template('print-qr-3x3.html', workerName=workerName, workerRegNum=workerRegNum)
    else:
        return redirect('/')
    


# Set Malay language
@app.route("/lang-malay")
def langMalay():
    session['langMalay'] = 'malay'
    return redirect('/profile')


@app.route("/lang-english")
def langEnglish():
    if 'langMalay' in session:
        session.pop('langMalay', None)
        return redirect('/profile')
    else:
        return redirect('/profile')
# End Set Malay language


# Logout
@app.route("/logout")
def logout():
    if 'user_session' in session:
        #session.pop('username', None)
        session.clear()
        return redirect('/')
    else:
        return redirect('/')

# ======================
#   End * User Section
# ======================



# ======================
#  Start subUser Section
# ======================
# subUser Profile    
@app.route("/sub-user-profile", methods=['GET', 'POST'])
def subUserProfile():
    if 'subUser_session' in session:
        subUser_session = session.get('subUser_session')
        conn = get_db_connection()
        cur = conn.cursor()

        # get Sub User Parent 
        cur.execute("SELECT * FROM sub_users WHERE username=?", (subUser_session,))
        subUserData = cur.fetchall()
        subUser_len = len(subUserData)
        if subUser_len == 0:
            return render_template('/')
        # subUserRoot
        active_user_session = subUserData[0][4]
    
        # get userRoot Data 
        cur.execute("SELECT name, email FROM users WHERE email=?", (active_user_session,))
        subUserRoot = cur.fetchall()
        subUserRoot_name = subUserRoot[0][0]
        subUserRoot_username = subUserRoot[0][1]

        return render_template('sub-user-profile.html',subUserRoot_name=subUserRoot_name, subUserRoot_username=subUserRoot_username, subUserData=subUserData)
    else:
        return redirect('/')

   
# sub-user-update-password
@app.route("/sub-user-update-password", methods=['POST'])
def subUser_updatePassword():
    if 'subUser_session' in session:
        try:
            subUser_session = session.get('subUser_session')
            conn = get_db_connection()
            cur = conn.cursor()

            password = request.form.get('password')
            # get Sub User Parent 
            cur.execute("UPDATE sub_users SET password=? WHERE username=?", (password, subUser_session,))
            conn.commit()
            conn.close()
            session['sub_user_profile_success'] = 'success'
            return redirect('sub-user-profile')
        except Exception as e:
            session['sub_user_profile_error'] = 'error'
            return redirect('/sub-user-profile')
    else:
        return redirect('/')
    


# subUser Add Worker
@app.route("/sub-user-add-worker")
def subUserAddWorker():
    if 'subUser_session' in session:
        subUser_session = session.get('subUser_session')
        conn = get_db_connection()
        cur = conn.cursor()

        # get Sub User Parent 
        subUser_root = cur.execute("SELECT creator FROM sub_users WHERE username=?", (subUser_session,))
        subUser_root = subUser_root.fetchall()
        subUser_rootLen = len(subUser_root)
        if subUser_rootLen == 0:
            return render_template('/')
        
        # subUserRoot
        active_user_session = subUser_root[0][0]
        
        serverPort = request.environ.get('SERVER_PORT')

        userRoot = active_user_session + 'Docs'
        
        # check profile data
        profile = cur.execute("SELECT * FROM profile WHERE aps_email=?", (active_user_session,))
        profile = profile.fetchall()
        profileLen = len(profile)
        if profileLen == 0:
            return redirect('/')

        
        # Register Branch Address for workers & family members
        cur.execute("SELECT branch_address1, branch_address2, branch_address3, aps_contact_person FROM profile WHERE aps_email=?", (active_user_session,))
        profileBranchAddress = cur.fetchall()
        
        for row in profileBranchAddress:
            branch_address1 = row[0]
            branch_address2 = row[1]
            branch_address3 = row[2]
            aps_contact_person = row[3]
        
        # Worker Registration Number
        # --------------------------
        # for Date & time
        workerPrefix = 'FW'
        
        currentDate = datetime.now()
        currentYear = currentDate.strftime("%y")
        
        cur.execute("SELECT employer_company_name FROM profile WHERE aps_email=?", (active_user_session,))
        companyName = cur.fetchall()
        companyName = companyName[0][0]
        companyShortName = company_first_letters(companyName)

        # FM Prefix
        fmPrefix = 'FM'
        fm_registrationPrefix = fmPrefix + currentYear + companyShortName.upper()

        creation_date = datetime.now().strftime('%d/%m/%Y')
        creation_time = datetime.now().strftime('%H:%M:%S')

        '''
        # Number of Worker
        # Find Last Key of Worker
        cur.execute('SELECT MAX(id) FROM half_form')
        last_key = cur.fetchone()[0]

        if last_key == None:
            workerSerialNumber = 1
            formatted_number = f"{workerSerialNumber:06}"
        else:
            workerSerialNumber = last_key + 1
            formatted_number = f"{workerSerialNumber:06}"
        
        workerRegistrationNumber = workerPrefix + currentYear + companyShortName.upper() + formatted_number
        
        # Create the Folder For Worker
        userRoot = active_user_session + 'Docs'
        folderCreator(userRoot, workerRegistrationNumber, 'legal', 0, 0, 0)
        # End Worker Registration Number
        # ------------------------------
        '''

        '''
        # Number of Worker
        # Find Last Key of Worker
        # -----------------------
        # check incomplete Status  MAX(tracking_id),
        cur.execute('SELECT worker_reg_no FROM reg_num_tracking WHERE user=? AND creator=? AND status=?', (active_user_session, subUser_session, 'incomplete'))
        track_worker = cur.fetchall()
        track_worker_len = len(track_worker)

        if track_worker_len == 1:
            track_worker_reg_no = track_worker[0][0]
            # Check it
            if track_worker_reg_no:
                workerRegistrationNumber = track_worker_reg_no
                print('Track Worker Reg Num-> ', track_worker_reg_no)
        else:
            # Check Complete Status ID's
            cur.execute('SELECT worker_reg_no FROM reg_num_tracking WHERE user=?', (active_user_session,))
            track_worker2 = cur.fetchall()
            track_worker_len2 = len(track_worker2)

            if track_worker_len2 >= 1:
                # Get The Last ID of Worker
                cur.execute('SELECT MAX(tracking_id) FROM reg_num_tracking WHERE user=?', (active_user_session,))
                last_key = cur.fetchone()[0]

                # Check It
                if last_key >= 1:
                    workerSerialNumber = last_key + 1
                    formatted_number = f"{workerSerialNumber:06}"
                    workerRegistrationNumber = workerPrefix + currentYear + companyShortName.upper() + formatted_number

                    print('last Key-> ', last_key)
                    # Insert New Worker Reg No.
                    cur.execute('INSERT INTO reg_num_tracking(tracking_id, user, creator, worker_reg_no, status, creation_date, creation_time) VALUES(?, ?, ?, ?, ?, ?, ?)', (workerSerialNumber, active_user_session, subUser_session, workerRegistrationNumber, 'incomplete', creation_date, creation_time))

            else:
                # Check None Data
                cur.execute('SELECT MAX(tracking_id) FROM reg_num_tracking WHERE user=?', (active_user_session,))
                last_key = cur.fetchone()[0]

                # Check It
                if last_key == None:
                    workerSerialNumber = 1
                    formatted_number = f"{workerSerialNumber:06}"
                    workerRegistrationNumber = workerPrefix + currentYear + companyShortName.upper() + formatted_number
                    # Insert New Worker Reg No.
                    cur.execute('INSERT INTO reg_num_tracking(tracking_id, user, creator, worker_reg_no, status, creation_date, creation_time) VALUES(?, ?, ?, ?, ?, ?, ?)', (workerSerialNumber, active_user_session, subUser_session, workerRegistrationNumber, 'incomplete', creation_date, creation_time))
                    print('last Key-> ', last_key)
        '''

        # -----------------------
        # Find Last Key of Worker
        # -----------------------
        # check incomplete Status  MAX(tracking_id),
        cur.execute('SELECT worker_reg_no FROM reg_num_tracking WHERE user=? AND creator=? AND status=?', (active_user_session, subUser_session, 'incomplete'))
        track_worker = cur.fetchall()
        track_worker_len = len(track_worker)

        if track_worker_len == 1:
            track_worker_reg_no = track_worker[0][0]
            # Check it
            if track_worker_reg_no:
                workerRegistrationNumber = track_worker_reg_no
                #print('Track Worker Reg Num-> ', track_worker_reg_no)
                
                # Now return FMamily members
                cur.execute('SELECT fm_reg_no FROM fm_reg_num_tracking WHERE user=? AND worker_reg_no=?', (active_user_session, workerRegistrationNumber))
                track_fm = cur.fetchall()
                track_fm_len = len(track_fm)
                #print('FM Track -> ', track_fm, track_fm_len)
                
        else:
            # Check Complete Status ID's
            cur.execute('SELECT worker_reg_no FROM reg_num_tracking WHERE user=?', (active_user_session,))
            track_worker2 = cur.fetchall()
            track_worker_len2 = len(track_worker2)

            if track_worker_len2 >= 1:
                # Get The Last ID of Worker
                cur.execute('SELECT MAX(tracking_id) FROM reg_num_tracking WHERE user=?', (active_user_session,))
                last_key = cur.fetchone()[0]

                # Check It
                if last_key >= 1:
                    workerSerialNumber = last_key + 1
                    formatted_number = f"{workerSerialNumber:06}"
                    workerRegistrationNumber = workerPrefix + currentYear + companyShortName.upper() + formatted_number

                    #print('last Key-> ', last_key)
                    # Insert New Worker Reg No.
                    cur.execute('INSERT INTO reg_num_tracking(tracking_id, user, creator, worker_reg_no, status, creation_date, creation_time) VALUES(?, ?, ?, ?, ?, ?, ?)', (workerSerialNumber, active_user_session, subUser_session, workerRegistrationNumber, 'incomplete', creation_date, creation_time))

                    # Insert Family Member Reg No.
                    # ----------------------------
                    cur.execute('SELECT MAX(tracking_id) FROM fm_reg_num_tracking WHERE user=?', (active_user_session,))
                    fm_last_key = cur.fetchone()[0]
                    if fm_last_key == None:
                        new_fm_last_key = 0
                    else:
                        new_fm_last_key = fm_last_key

                    #print(new_fm_last_key)

                    for nn in range(1, 11):
                        fmSerialNumber = new_fm_last_key + nn
                        fm_formatted_number = f"{fmSerialNumber:06}"
                        fmRegistrationNumber = fm_registrationPrefix + fm_formatted_number
                        # insert
                        cur.execute('INSERT INTO fm_reg_num_tracking(tracking_id, user, creator, worker_reg_no, fm_reg_no, status, creation_date, creation_time) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (fmSerialNumber, active_user_session, subUser_session, workerRegistrationNumber, fmRegistrationNumber,'incomplete', creation_date, creation_time))

                    # Create the Folder For Worker
                    userRoot = active_user_session + 'Docs'
                    folderCreator(userRoot, workerRegistrationNumber, 'legal',fm_registrationPrefix , new_fm_last_key, 10)

                    # Now return FMamily members
                    cur.execute('SELECT fm_reg_no FROM fm_reg_num_tracking WHERE user=? AND worker_reg_no=?', (active_user_session, workerRegistrationNumber))
                    track_fm = cur.fetchall()
                    track_fm_len = len(track_fm)
                    #print('FM Track -> ', track_fm, track_fm_len)

            else:
                # Check None Data
                cur.execute('SELECT MAX(tracking_id) FROM reg_num_tracking WHERE user=?', (active_user_session,))
                last_key = cur.fetchone()[0]

                # Check It
                if last_key == None:
                    workerSerialNumber = 1
                    formatted_number = f"{workerSerialNumber:06}"
                    workerRegistrationNumber = workerPrefix + currentYear + companyShortName.upper() + formatted_number
                    # Insert New Worker Reg No.
                    cur.execute('INSERT INTO reg_num_tracking(tracking_id, user, creator, worker_reg_no, status, creation_date, creation_time) VALUES(?, ?, ?, ?, ?, ?, ?)', (workerSerialNumber, active_user_session, subUser_session, workerRegistrationNumber, 'incomplete', creation_date, creation_time))
                    #print('last Key-> ', last_key)

                    # Insert Family Member Reg No.
                    # ----------------------------
                    cur.execute('SELECT MAX(tracking_id) FROM fm_reg_num_tracking WHERE user=?', (active_user_session,))
                    fm_last_key = cur.fetchone()[0]
                    if fm_last_key == None:
                        new_fm_last_key = 0
                    else:
                        new_fm_last_key = fm_last_key

                    for nn in range(1, 11):
                        fmSerialNumber = new_fm_last_key + nn
                        fm_formatted_number = f"{fmSerialNumber:06}"
                        fmRegistrationNumber = fm_registrationPrefix + fm_formatted_number
                        # insert
                        cur.execute('INSERT INTO fm_reg_num_tracking(tracking_id, user, creator, worker_reg_no, fm_reg_no, status, creation_date, creation_time) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (fmSerialNumber, active_user_session, subUser_session, workerRegistrationNumber, fmRegistrationNumber,'incomplete', creation_date, creation_time))

                    # Create the Folder For Worker
                    userRoot = active_user_session + 'Docs'
                    folderCreator(userRoot, workerRegistrationNumber, 'legal', fm_registrationPrefix , new_fm_last_key, 10)

                    # Now return FMamily members
                    cur.execute('SELECT fm_reg_no FROM fm_reg_num_tracking WHERE user=? AND worker_reg_no=?', (active_user_session, workerRegistrationNumber))
                    track_fm = cur.fetchall()
                    track_fm_len = len(track_fm)
                    #print('FM Track -> ', track_fm, track_fm_len)
        

        


        
        # End Check profile Data
        gallery_images = glob.glob('./static/img/uploaded-image/legal1/*')
        gallery_images2 = glob.glob('./static/img/uploaded-image/legal2/*')
        gallery_images3 = glob.glob('./static/img/uploaded-image/illegal1/*')
        gallery_images4 = glob.glob('./static/img/uploaded-image/illegal2/*')
        gallery_images5 = glob.glob('./static/img/uploaded-image/illegal3/*')
        gallery_images6 = glob.glob('./static/img/uploaded-image/illegal4/*')
        gallery_images7 = glob.glob('./static/img/uploaded-image/illegal5/*')
        gallery_images8 = glob.glob('./static/img/uploaded-image/illegal6/*')
        

        # For the citizenship
        cur.execute("SELECT citizenship FROM detailed_dd_citizenship")
        citizenship = cur.fetchall()
        
        # For the Maritial Status
        cur.execute("SELECT maritial_status FROM detailed_dd_maritail_status")
        maritial = cur.fetchall()

        # for the point of Entry
        cur.execute("SELECT poe FROM detailed_dd_poe")
        poe = cur.fetchall()

        # for the gender
        cur.execute("SELECT gender FROM detailed_dd_gender")
        gender = cur.fetchall()

        # for the religion
        cur.execute("SELECT religion FROM detailed_dd_religion")
        religion = cur.fetchall()

        # for the race
        cur.execute("SELECT race FROM detailed_dd_race")
        race = cur.fetchall()

        # for the relationship
        cur.execute("SELECT relationship FROM detailed_dd_relationship")
        relationship = cur.fetchall()

        # for the job sector
        cur.execute("SELECT job_sector FROM detailed_dd_job_sector")
        job_sector = cur.fetchall()

        # for the job_status_sponsor
        cur.execute("SELECT job_status_sponser FROM detailed_dd_job_status_sponsor")
        job_status_sponsor = cur.fetchall()

        # for the city
        cur.execute("SELECT city FROM detailed_dd_city")
        city = cur.fetchall()

        # for the state 
        cur.execute("SELECT state FROM detailed_dd_state")
        state = cur.fetchall()

        # for the Issuing Country
        cur.execute("SELECT country_issued_doc FROM detailed_dd_country_issued_doc")
        issuingCountry = cur.fetchall()

        # for the Document Status 
        cur.execute("SELECT doc_status FROM detailed_dd_doc_status")
        docStatus = cur.fetchall()

        # for the Status of current document
        cur.execute("SELECT current_status_doc FROM detailed_dd_current_status_doc")
        curDocStatus = cur.fetchall()

         # for the type of document
        cur.execute("SELECT type_of_doc FROM detailed_dd_type_of_doc")
        typeOfDoc = cur.fetchall()

        cur.execute("SELECT employement_status FROM detailed_dd_employement_status")
        employement_status = cur.fetchall()

        cur.execute("SELECT legal_status FROM detailed_dd_worker_legal_status")
        legalStatusList = cur.fetchall()

        cur.execute("SELECT job_status_sponser FROM detailed_dd_job_status_sponsor")
        job_status_sponsor = cur.fetchall()

        conn.commit()
        cur.close()

        return render_template('sub-user-add-worker.html', new_fMemberID=1, legalStatusList=legalStatusList, userRoot=userRoot, ip_address=ip_address, serverPort=serverPort, branch_address1=branch_address1, branch_address2=branch_address2, branch_address3=branch_address3, aps_contact_person=aps_contact_person, workerRegistrationNumber=workerRegistrationNumber, fm_registrationPrefix=fm_registrationPrefix, filename=gallery_images, filename2=gallery_images2, filename3=gallery_images3, filename4=gallery_images4, filename5=gallery_images5, filename6=gallery_images6, filename7=gallery_images7, filename8=gallery_images8, citizenshipList=citizenship, maritialList=maritial, poeList=poe, genderList=gender, religionList=religion, raceList=race, relationshipList=relationship, jobSectorList=job_sector, cityList=city, stateList=state, issuingCountryList=issuingCountry, docStatusList=docStatus, curDocStatusList=curDocStatus, typeOfDocList=typeOfDoc, employement_statusList=employement_status, jobStatusSponsorList = job_status_sponsor)
    else:
        return redirect('/')

# subUser For add worker >> sub sector
@app.route("/sub-user-add-worker-sub-sector", methods=['GET', 'POST'])
def subUser_addWorker_subSector():
    if 'subUser_session' in session:
        sector = request.form.get('job_sector')
        # check profile data
        conn = get_db_connection()
        cur = conn.cursor()
        # for Date & time
        currentDate = datetime.now()
        cYear = currentDate.strftime("%y")

        cur.execute("SELECT job_sub_sector FROM detailed_dd_job_sub_sector where job_sector=?", (sector,))
        job_sub_sector = cur.fetchall()
        return jsonify(job_sub_sector)
    else:
        return redirect('/')
# End For add worker >> sub sector

# subUser Add Worker
@app.route("/sub-user-insertWorker", methods=['POST'])
def subUser_insertWorker():
    conn = get_db_connection()
    cur = conn.cursor()

    subUser_session = session.get('subUser_session')

    # get Sub User Parent 
    subUser_root = cur.execute("SELECT creator FROM sub_users WHERE username=?", (subUser_session,))
    subUser_root = subUser_root.fetchall()
    subUser_rootLen = len(subUser_root)
    if subUser_rootLen == 0:
        return render_template('/')
    # subUserRoot
    active_user_session = subUser_root[0][0]


    form_date = datetime.now().strftime('%d%m%Y')
    form_rand = random.randrange(10000, 99999)
    form_unique_key = 'DT'+form_date+'N'+str(form_rand)

    form_time = datetime.now().strftime('%H:%M:%S')
    
    if 'subUser_session' in session:
        if request.method == 'POST':
            try:
                data = request.get_json()
    
                #print('All Data: ->', data)
                formStatus = data.get('status')
                workerD = data.get('workerData')
                docD = data.get('docData')
                fmData = data.get('familyMemberData')

                
                # Worker & Family
                if formStatus == 'workerOnly':
                    #print(formStatus)
                    
                    workerData = json.loads(workerD)
                    docData = json.loads(docD)

                    # Form Data 
                    for worker in workerData:
                        form_created_by = active_user_session
                        form_created_date = current_date
                        form_worker_reg_no = worker['awl_worker_registration_no']
                        no_family_mem = worker['no_of_family_member']
                        worker_detail_worker_legal_status = worker['awl_worker_legal_status']
                        worker_detail_name_of_worker = worker['awl_name_of_worker']
                        
                        worker_detail_family_name = worker['awl_family_name']
                        worker_detail_gender = worker['awl_gender']
                        worker_detail_DOB = worker['awl_d_o_b']
                        worker_detail_place_birth = worker['awl_place_of_birth']
                        worker_detail_citizenship = worker['awl_citizenship']
                        
                        worker_detail_marital_status = worker['awl_maritial_status']
                        worker_detail_poe = worker['awl_point_of_entry']
                        worker_detail_religion = worker['awl_religion']
                        worker_detail_race = worker['awl_race']
                        worker_detail_contact_no = worker['awl_worker_contact_no']
                        
                        worker_detail_email = worker['awl_worker_email']
                        worker_detail_nok = worker['awl_name_of_next_kin']
                        worker_detail_relationship = worker['awl_relationship']
                        worker_detail_nok_contact_no = worker['awl_nok_contact_no']
                        worker_emp_dtl_job_sector = worker['awl_job_sector']
                        
                        worker_emp_dtl_job_sub_sector = worker['awl_job_sub_sector']
                        worker_emp_dtl_emp_sponsorship_status = worker['awl_employement_sponsorship_status']
                        worker_emp_dtl_address1 = worker['awl_address1']
                        worker_emp_dtl_address2 = worker['awl_address2']
                        worker_emp_dtl_address3 = worker['awl_address3']
                        
                        worker_emp_dtl_postcode = 'postcode - static' #worker['']
                        worker_emp_dtl_city = worker['awl_city']
                        worker_emp_dtl_state = worker['awl_state']
                        worker_doc_dtl_doc_id = 'document_id-123456'
                        worker_doc_dtl_type_of_doc = 'type_of_documents'
                        
                        worker_doc_dtl_no_of_doc = 'static' #worker['']
                        worker_doc_dtl_images_path_email = 'static' # worker[)
                        worker_doc_dtl_place_of_issue = 'static' # worker['awl_place_of_issue']
                        worker_doc_dtl_issue_date = 'static' # worker['awl_document_issued_date']
                        worker_doc_dtl_expiry_date = 'static' # worker['awl_document_expiry_date']
                        
                        worker_doc_dtl_country_doc_issued =  'static' #worker['awl_issuing_country']
                        worker_doc_dtl_doc_status = 'static' # worker['awl_document_status']
                        worker_doc_dtl_doc_current_status ='static' #  worker['awl_status_of_current_document']
                        worker_doc_dtl_doc_no = 'static' 
                        form_position = 'static' 
                        
                        form_status = 'static' 
                    
                    # Find Last Key of Worker
                    cur.execute('SELECT MAX(worker_key) FROM half_form')
                    last_key = cur.fetchone()[0]

                    if last_key == None:
                        next_key = 1
                    else:
                        next_key = last_key + 1
                    #print('Last Key: ', last_key, 'Next Key: ', next_key)
                    

                    
                    # Worker Insert
                    cur.execute('INSERT INTO half_form (worker_key, form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, worker_doc_dtl_doc_id, worker_doc_dtl_type_of_doc, worker_doc_dtl_no_of_doc, worker_doc_dtl_images_path_email, worker_doc_dtl_place_of_issue, worker_doc_dtl_issue_date, worker_doc_dtl_expiry_date, worker_doc_dtl_country_doc_issued, worker_doc_dtl_doc_status, worker_doc_dtl_doc_current_status, worker_doc_dtl_doc_no, form_position, form_status, form_unique_key) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, worker_doc_dtl_doc_id, worker_doc_dtl_type_of_doc, worker_doc_dtl_no_of_doc, worker_doc_dtl_images_path_email, worker_doc_dtl_place_of_issue, worker_doc_dtl_issue_date, worker_doc_dtl_expiry_date, worker_doc_dtl_country_doc_issued, worker_doc_dtl_doc_status, worker_doc_dtl_doc_current_status, worker_doc_dtl_doc_no, form_position, form_status, form_unique_key))
                    
                    # Insert Worker Date & Time
                    cur.execute('INSERT INTO half_form_time (worker_reg_no, reg_date, reg_time) VALUES(?, ?, ?)', (form_worker_reg_no, current_date, form_time))
                    
                    # Insert Workers Document
                    for docs in docData:
                        document_link = docs['document_link']
                        type_of_documents = docs['type_of_documents']
                        document_id = docs['document_id']
                        place_of_issue = docs['place_of_issue']
                        document_issued_date = docs['document_issued_date']
                        document_expiry_date = docs['document_expiry_date']
                        issuing_country = docs['issuing_country']
                        document_status = docs['document_status']
                        status_of_current_document = docs['status_of_current_document']
                    
                        #query
                        cur.execute('INSERT INTO workers_document (worker_key, document_link, type_of_douments, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document, form_unique_key) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, document_link, type_of_documents, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document, form_unique_key))
                    # End Insert Workers Document

                    # Insert subUser Datalog
                    cur.execute('INSERT INTO sub_users_datalog (creator, parent, worker_reg_no, form_unique_key, creation_date, creation_time) VALUES(?, ?, ?, ?, ?, ?)', (subUser_session, active_user_session, form_worker_reg_no, form_unique_key, current_date, form_time))
                    # End * subUser Datalog
                    
                elif formStatus == 'workerWithFamily':
                    #print(formStatus)
                    # Worker & Family
                
                    # JSON to Obj
                    workerData = json.loads(workerD)
                    docData = json.loads(docD)
                    familyMemberData = json.loads(fmData)
                    
                    # Form Data
                    for worker in workerData:
                        form_created_by = active_user_session
                        form_created_date = current_date
                        form_worker_reg_no = worker['awl_worker_registration_no']
                        no_family_mem = worker['no_of_family_member']
                        worker_detail_worker_legal_status = worker['awl_worker_legal_status']
                        worker_detail_name_of_worker = worker['awl_name_of_worker']
                        
                        worker_detail_family_name = worker['awl_family_name']
                        worker_detail_gender = worker['awl_gender']
                        worker_detail_DOB = worker['awl_d_o_b']
                        worker_detail_place_birth = worker['awl_place_of_birth']
                        worker_detail_citizenship = worker['awl_citizenship']
                        
                        worker_detail_marital_status = worker['awl_maritial_status']
                        worker_detail_poe = worker['awl_point_of_entry']
                        worker_detail_religion = worker['awl_religion']
                        worker_detail_race = worker['awl_race']
                        worker_detail_contact_no = worker['awl_worker_contact_no']
                        
                        worker_detail_email = worker['awl_worker_email']
                        worker_detail_nok = worker['awl_name_of_next_kin']
                        worker_detail_relationship = worker['awl_relationship']
                        worker_detail_nok_contact_no = worker['awl_nok_contact_no']
                        worker_emp_dtl_job_sector = worker['awl_job_sector']
                        
                        worker_emp_dtl_job_sub_sector = worker['awl_job_sub_sector']
                        worker_emp_dtl_emp_sponsorship_status = worker['awl_employement_sponsorship_status']
                        worker_emp_dtl_address1 = worker['awl_address1']
                        worker_emp_dtl_address2 = worker['awl_address2']
                        worker_emp_dtl_address3 = worker['awl_address3']
                        
                        worker_emp_dtl_postcode = 'postcode - static' #worker['']
                        worker_emp_dtl_city = worker['awl_city']
                        worker_emp_dtl_state = worker['awl_state']
                        worker_doc_dtl_doc_id = 'document_id-123456'
                        worker_doc_dtl_type_of_doc = 'type_of_documents'
                        
                        worker_doc_dtl_no_of_doc = 'static' #worker['']
                        worker_doc_dtl_images_path_email = 'static' # worker[)
                        worker_doc_dtl_place_of_issue = 'static' # worker['awl_place_of_issue']
                        worker_doc_dtl_issue_date = 'static' # worker['awl_document_issued_date']
                        worker_doc_dtl_expiry_date = 'static' # worker['awl_document_expiry_date']
                        
                        worker_doc_dtl_country_doc_issued =  'static' #worker['awl_issuing_country']
                        worker_doc_dtl_doc_status = 'static' # worker['awl_document_status']
                        worker_doc_dtl_doc_current_status ='static' #  worker['awl_status_of_current_document']
                        worker_doc_dtl_doc_no = 'static' 
                        form_position = 'static' 
                        
                        form_status = 'static' 
                        
                    
                    # Find Last Key of Worker
                    cur.execute('SELECT MAX(worker_key) FROM half_form')
                    last_key = cur.fetchone()[0]
                    
                    if last_key == None:
                        next_key = 1
                    else:
                        next_key = last_key + 1
                    #print('Last Key: ', last_key, 'Next Key: ', next_key)
                    
                    
                    # Worker Insert
                    cur.execute('INSERT INTO half_form (worker_key, form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, worker_doc_dtl_doc_id, worker_doc_dtl_type_of_doc, worker_doc_dtl_no_of_doc, worker_doc_dtl_images_path_email, worker_doc_dtl_place_of_issue, worker_doc_dtl_issue_date, worker_doc_dtl_expiry_date, worker_doc_dtl_country_doc_issued, worker_doc_dtl_doc_status, worker_doc_dtl_doc_current_status, worker_doc_dtl_doc_no, form_position, form_status, form_unique_key) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, worker_doc_dtl_doc_id, worker_doc_dtl_type_of_doc, worker_doc_dtl_no_of_doc, worker_doc_dtl_images_path_email, worker_doc_dtl_place_of_issue, worker_doc_dtl_issue_date, worker_doc_dtl_expiry_date, worker_doc_dtl_country_doc_issued, worker_doc_dtl_doc_status, worker_doc_dtl_doc_current_status, worker_doc_dtl_doc_no, form_position, form_status, form_unique_key))
                    
                    # Insert Worker Date & Time
                    cur.execute('INSERT INTO half_form_time (worker_reg_no, reg_date, reg_time) VALUES(?, ?, ?)', (form_worker_reg_no, current_date, form_time))
                    
                    # Insert Workers Document
                    for docs in docData:
                        document_link = docs['document_link']
                        type_of_documents = docs['type_of_documents']
                        document_id = docs['document_id']
                        place_of_issue = docs['place_of_issue']
                        document_issued_date = docs['document_issued_date']
                        document_expiry_date = docs['document_expiry_date']
                        issuing_country = docs['issuing_country']
                        document_status = docs['document_status']
                        status_of_current_document = docs['status_of_current_document']
                    
                        #query
                        cur.execute('INSERT INTO workers_document (worker_key, document_link, type_of_douments, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document, form_unique_key) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, document_link, type_of_documents, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document, form_unique_key))
                    # End Insert Workers Document
                    
                    # Insert Worker Family
                    for fmD in familyMemberData:
                        fm_worker_registration_no = fmD['fm_worker_registration_no']
                        fm_worker_name = fmD['fm_worker_name']
                        fm_relationship = fmD['fm_relationship']
                        fm_name_of_family_member = fmD['fm_name_of_family_member']
                        fm_family_name = fmD['fm_family_name']
                        fm_is_family_member_together = fmD['fm_is_family_member_together']
                        fm_point_of_entry = fmD['fm_point_of_entry']
                        fm_citizenship = fmD['fm_citizenship']
                        fm_religion = fmD['fm_religion']
                        fm_marital_status = fmD['fm_marital_status']
                        fm_gender = fmD['fm_gender']
                        fm_address1 = fmD['fm_address1']
                        fm_address2 = fmD['fm_address2']
                        fm_address3 = fmD['fm_address3']
                        fm_postcode = fmD['fm_postcode']
                        fm_city = fmD['fm_city']
                        fm_state = fmD['fm_state']
                        fm_contact_no = fmD['fm_contact_no']
                        fm_race = fmD['fm_race']
                        fm_place_of_birth = fmD['fm_place_of_birth']
                        fm_dob = fmD['fm_dob']
                        fm_employment_status = fmD['fm_employment_status']
                        fm_same_employer_as_worker = fmD['fm_same_employer_as_worker']
                        fm_employer_name = fmD['fm_employer_name']
                        fm_employer_address = fmD['fm_employer_address']

                        fmDoc1_type_of_documents = fmD['fmDoc1_type_of_documents']
                        fmDoc1_document_id = fmD['fmDoc1_document_id']
                        fmDoc1_place_of_issue = fmD['fmDoc1_place_of_issue']
                        fmDoc1_document_issued_date = fmD['fmDoc1_document_issued_date']
                        fmDoc1_document_expiry_date = fmD['fmDoc1_document_expiry_date']
                        fmDoc1_issuing_country = fmD['fmDoc1_issuing_country']
                        fmDoc1_document_status = fmD['fmDoc1_document_status']
                        fmDoc1_status_of_current_document = fmD['fmDoc1_status_of_current_document']

                        fmDoc2_type_of_documents = fmD['fmDoc2_type_of_documents']
                        fmDoc2_document_id = fmD['fmDoc2_document_id']
                        fmDoc2_place_of_issue = fmD['fmDoc2_place_of_issue']
                        fmDoc2_document_issued_date = fmD['fmDoc2_document_issued_date']
                        fmDoc2_document_expiry_date = fmD['fmDoc2_document_expiry_date']
                        fmDoc2_issuing_country = fmD['fmDoc2_issuing_country']
                        fmDoc2_document_status = fmD['fmDoc2_document_status']
                        fmDoc2_status_of_current_document = fmD['fmDoc2_status_of_current_document']
                        
                        # fmData Query
                        cur.execute('INSERT INTO family_form (worker_key, form_created_by, form_created_date, form_unique_key, form_family_reg_no, family_form_worker_name, family_form_relationship, family_form_name_of_family_member, family_form_family_name, family_form_is_famliy_togther, family_form_family_form_poe, family_form_citizenship, family_form_religion,family_form_marital_status, family_form_gender, family_form_address1, family_form_address2, family_form_address3, family_form_postcode, family_form_city, family_form_state, family_form_contact_no, family_form_race, family_form_place_of_birth, family_form_emp_status, family_form_emp_name, family_form_emp_address, family_form_doc_path_email, family_form_doc_image_no, fmDoc1_type_of_documents, fmDoc1_document_id, fmDoc1_place_of_issue, fmDoc1_document_issued_date, fmDoc1_document_expiry_date, fmDoc1_issuing_country, fmDoc1_document_status, fmDoc1_status_of_current_document, fmDoc2_type_of_documents, fmDoc2_document_id, fmDoc2_place_of_issue, fmDoc2_document_issued_date, fmDoc2_document_expiry_date, fmDoc2_issuing_country, fmDoc2_document_status, fmDoc2_status_of_current_document) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, form_created_by, current_date, form_unique_key, fm_worker_registration_no, fm_worker_name, fm_relationship, fm_name_of_family_member, fm_family_name, fm_is_family_member_together, fm_point_of_entry, fm_citizenship, fm_religion, fm_marital_status, fm_gender, fm_address1, fm_address2, fm_address3, fm_postcode, fm_city, fm_state, fm_contact_no, fm_race, fm_place_of_birth, fm_employment_status, fm_employer_name, fm_employer_address, 'static email', 'doc image- static', fmDoc1_type_of_documents, fmDoc1_document_id, fmDoc1_place_of_issue, fmDoc1_document_issued_date, fmDoc1_document_expiry_date, fmDoc1_issuing_country, fmDoc1_document_status, fmDoc1_status_of_current_document, fmDoc2_type_of_documents, fmDoc2_document_id, fmDoc2_place_of_issue, fmDoc2_document_issued_date, fmDoc2_document_expiry_date, fmDoc2_issuing_country, fmDoc2_document_status, fmDoc2_status_of_current_document))  
                    # End Insert Worker Family

                    # Insert subUser Datalog
                    cur.execute('INSERT INTO sub_users_datalog (creator, parent, worker_reg_no, form_unique_key, creation_date, creation_time) VALUES(?, ?, ?, ?, ?, ?)', (subUser_session, active_user_session, form_worker_reg_no, form_unique_key, current_date, form_time))
                    # End * subUser Datalog

                conn.commit()
                cur.close()
               
                #print('success')
                return jsonify({'status': 'success'})
            
            except Exception as e:    
                #print('Insert Worker Error: ', str(e))
                return jsonify({'status': 'failure'})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid request method'})
    else:
        return jsonify({'status': 'error', 'message': 'User not logged in'})
    


# subUser Worker & Family Member Folder Creation
@app.route("/sub-user-worker-fm-folderCreator", methods=['GET', 'POST'])
def subUser_worker_fm_folderCreator():
    if 'subUser_session' in session:
        if(request.method == 'POST'):
            conn = get_db_connection()
            cur = conn.cursor()

            subUser_session = session.get('subUser_session')

            # get Sub User Parent 
            subUser_root = cur.execute("SELECT creator FROM sub_users WHERE username=?", (subUser_session,))
            subUser_root = subUser_root.fetchall()
            subUser_rootLen = len(subUser_root)
            if subUser_rootLen == 0:
                return render_template('/')
            # subUserRoot
            active_user_session = subUser_root[0][0]

            folderData = request.get_json()
            worker_registration_folder_name = folderData.get('worker_registration_folder_name')
            
            fMember_prefix = folderData.get('fMember_prefix')
            fm_last_ID = folderData.get('fm_last_ID')
            total_fMember = folderData.get('total_fMember')
            
            # Final Family member registration number 
            userRoot = active_user_session + 'Docs'
            folderCreator(userRoot, worker_registration_folder_name, 'legal', fMember_prefix, fm_last_ID, total_fMember)
            return ({"status":"success"})




#  subUser registration-log  
@app.route("/sub-user-registration-log", methods=['GET', 'POST'])
def subUser_registrationLog():
    if 'subUser_session' in session:

        conn = get_db_connection()
        cur = conn.cursor()

        subUser_session = session.get('subUser_session')

        # get Sub User Parent 
        subUser_root = cur.execute("SELECT creator FROM sub_users WHERE username=?", (subUser_session,))
        subUser_root = subUser_root.fetchall()
        subUser_rootLen = len(subUser_root)
        if subUser_rootLen == 0:
            return render_template('/')
        # subUserRoot
        active_user_session = subUser_root[0][0]

        # Get form Unique Key 
        form_unique_key_list = []
        subUser_q = cur.execute("SELECT form_unique_key FROM sub_users_datalog WHERE creator=?", (subUser_session,))
        form_unique_key = subUser_q.fetchall()

        for key in form_unique_key:
            form_unique_key_list.append(key[0])

        form_unique_key_tuple = tuple(form_unique_key_list)
        form_key_as_string = ', '.join(form_unique_key_tuple)
        
        
        previous_7th_date = previous_seventh_date()

        # reg. worker Current Day
        #cur.execute('SELECT * FROM half_form where form_created_by=? AND form_created_date=? AND form_unique_key IN (?)', (active_user_session, current_date, form_unique_key_tuple))
        #regWorkerDay = cur.fetchall()
        #print('RegLog: ', regWorkerDay)
        #regWorkerDay = len(regWorkerDay)

        placeholders = ', '.join(['?'] * len(form_unique_key_tuple))
        query = f'SELECT * FROM half_form WHERE form_created_by=? AND form_created_date=? AND form_unique_key IN ({placeholders})'
        parameters = (active_user_session, current_date) + form_unique_key_tuple
        # Execute the query
        cur.execute(query, parameters)
        # Fetch the results
        regWorkerDay = cur.fetchall()
        regWorkerDay = len(regWorkerDay)

        # reg. Family member Current Day
        query2 = f'SELECT * FROM family_form WHERE form_created_by=? AND form_created_date=? AND form_unique_key IN ({placeholders})'
        parameters2 = (active_user_session, current_date) + form_unique_key_tuple
        cur.execute(query2, parameters2)
        regMemberDay = cur.fetchall()

        #cur.execute('SELECT * FROM family_form where form_created_by=? AND form_created_date=?', (active_user_session, current_date))
        #regMemberDay = cur.fetchall()
        regMemberDay = len(regMemberDay)
        regNumber = regWorkerDay + regMemberDay

        
        # reg. worker Current Week
        #cur.execute('SELECT * FROM half_form where form_created_by=? AND form_created_date BETWEEN ? AND ?', (active_user_session, previous_7th_date, current_date))
        #regWorkerWeek = cur.fetchall()
        #regWorkerWeek = len(regWorkerWeek)

        query3 = f'SELECT * FROM half_form WHERE form_created_by=? AND form_created_date BETWEEN ? AND ? AND form_unique_key IN ({placeholders})'
        parameters3 = (active_user_session, previous_7th_date, current_date) + form_unique_key_tuple
        cur.execute(query3, parameters3)
        regWorkerWeek = cur.fetchall()
        regWorkerWeek = len(regWorkerWeek)


        # reg. Family member Current Week
        #cur.execute('SELECT * FROM family_form where form_created_by=? AND form_created_date BETWEEN ? AND ?', (active_user_session, previous_7th_date, current_date))
        #regMemberWeek = cur.fetchall()
        #regMemberWeek = len(regMemberWeek)
        #regNumberWeek = regWorkerWeek + regMemberWeek

        query4 = f'SELECT * FROM family_form WHERE form_created_by=? AND form_created_date BETWEEN ? AND ? AND form_unique_key IN ({placeholders})'
        parameters4 = (active_user_session, previous_7th_date, current_date) + form_unique_key_tuple
        cur.execute(query4, parameters4)
        regMemberWeek = cur.fetchall()
        regMemberWeek = len(regMemberWeek)
        regNumberWeek = regWorkerWeek + regMemberWeek
        

        # Legal status
        #cur.execute('SELECT * FROM half_form WHERE form_created_by=? AND worker_detail_worker_legal_status=? AND form_created_date BETWEEN ? AND ?', (active_user_session, 'Legal', previous_7th_date, current_date)) 
        #totalLegal = cur.fetchall()
        #totalLegal = len(totalLegal)
        query5 = f'SELECT * FROM half_form WHERE form_created_by=? AND worker_detail_worker_legal_status=? AND form_created_date BETWEEN ? AND ? AND form_unique_key IN ({placeholders})'
        parameters5 = (active_user_session, 'Legal', previous_7th_date, current_date) + form_unique_key_tuple
        cur.execute(query5, parameters5)
        totalLegal = cur.fetchall()
        totalLegal = len(totalLegal)


        # illegal status
        #cur.execute('SELECT * FROM half_form WHERE form_created_by=? AND worker_detail_worker_legal_status=? AND form_created_date BETWEEN ? AND ?', (active_user_session, 'Illegal', previous_7th_date, current_date))
        #totalIllegal = cur.fetchall()
        #totalIllegal = len(totalIllegal)
        query6 = f'SELECT * FROM half_form WHERE form_created_by=? AND worker_detail_worker_legal_status=? AND form_created_date BETWEEN ? AND ? AND form_unique_key IN ({placeholders})'
        parameters6 = (active_user_session, 'Illegal', previous_7th_date, current_date) + form_unique_key_tuple
        cur.execute(query6, parameters6)
        totalIllegal = cur.fetchall()
        totalIllegal = len(totalIllegal)
        
        return render_template('sub-user-registration-log.html', regNumber=regNumber, memberReg=regMemberDay, totalWorker=regWorkerDay, grandTotal=regNumberWeek, totalLegal=totalLegal, totalIllegal=totalIllegal)
    else:
        return redirect('/')


# subUser Set Lang Malay
@app.route("/sub-user-lang-malay")
def subUser_langMalay():
    session['langMalay'] = 'malay'
    return redirect('/sub-user-profile')


@app.route("/sub-user-lang-english")
def subUser_langEnglish():
    if 'langMalay' in session:
        session.pop('langMalay', None)
        return redirect('/sub-user-profile')
    else:
        return redirect('/sub-user-profile')
# End Set Malay language


# subUser Registration List
@app.route("/sub-user-registration-list", methods=['GET', 'POST'])
def subUser_registrationList():
    if 'subUser_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()

        subUser_session = session.get('subUser_session')
        # get Sub User Parent 
        subUser_root = cur.execute("SELECT creator FROM sub_users WHERE username=?", (subUser_session,))
        subUser_root = subUser_root.fetchall()
        subUser_rootLen = len(subUser_root)
        if subUser_rootLen == 0:
            return render_template('/')
        # subUserRoot
        active_user_session = subUser_root[0][0]

        subUser_workers = []

        
        # Get workers which is created by subUser
        cur.execute("SELECT form_unique_key FROM sub_users_datalog WHERE creator=?", (subUser_session,))
        workers_form_key = cur.fetchall()
        workers_form_key_len = len(workers_form_key)
        if workers_form_key_len == 0:
            redirect('/')
        else:
            for key in workers_form_key:
                cur.execute("SELECT id, form_worker_reg_no, worker_detail_name_of_worker FROM half_form WHERE form_unique_key=?", (key[0],))
                subUser_workers.append(cur.fetchone())

        #print('workers: ', subUser_workers)

        return render_template('sub-user-registration-list.html', totalForm=workers_form_key_len, workerList=subUser_workers)
        
    else:
        return redirect('/')
    

# sub-user- View Registered Worker
@app.route("/sub-user-view-registered-worker", methods=['GET', 'POST'])
def subUser_viewRegisteredWorker():
    if 'subUser_session' in session:
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            subUser_session = session.get('subUser_session')
            # get Sub User Parent 
            subUser_root = cur.execute("SELECT creator FROM sub_users WHERE username=?", (subUser_session,))
            subUser_root = subUser_root.fetchall()
            subUser_rootLen = len(subUser_root)
            if subUser_rootLen == 0:
                return render_template('/')
            # subUserRoot
            active_user_session = subUser_root[0][0]
            
            
            workerId = request.args.get('view-regWor')

            # fetch workers
            cur.execute("SELECT * FROM half_form WHERE id=? AND form_created_by=?", (workerId, active_user_session))
            workerD = cur.fetchall()
            form_unique_key = workerD[0][44]

            # get worker reg time
            worker_reg_no = workerD[0][4]
            cur.execute("SELECT reg_time FROM half_form_time WHERE worker_reg_no=?", (worker_reg_no,))
            workerRegNo = cur.fetchall()
            if workerRegNo:
                workerRegTime = workerRegNo[0][0]
            else:
                workerRegTime = 'N/A'

            # Worker Document Path
            docsPath = f"./static/documents/{active_user_session}Docs/{worker_reg_no}/"

            # fetch worker Docs
            cur.execute("SELECT * FROM workers_document WHERE form_unique_key=?", (form_unique_key,))
            workerDocs = cur.fetchall()

            # fetch worker Family members
            cur.execute("SELECT * FROM family_form WHERE form_unique_key=?", (form_unique_key,))
            workerFM = cur.fetchall()
            
            return render_template('sub-user-view-registered-worker.html', docsPath=docsPath, workerRegTime=workerRegTime, workerList=workerD, workerDocs=workerDocs, workerFM=workerFM)
        except Exception as e:
            return redirect('/sub-user-registration-list')
    else:
        return redirect('/')

# sub-user- Worker view-family-member
@app.route("/sub-user-view-family-member", methods=['GET', 'POST'])
def subUser_viewFamilyMember():
    if 'subUser_session' in session:

        try:
            fmId = request.args.get('fm')
            fmN = request.args.get('fmN')

            conn = get_db_connection()
            cur = conn.cursor()

            subUser_session = session.get('subUser_session')
            # get Sub User Parent 
            subUser_root = cur.execute("SELECT creator FROM sub_users WHERE username=?", (subUser_session,))
            subUser_root = subUser_root.fetchall()
            subUser_rootLen = len(subUser_root)
            if subUser_rootLen == 0:
                return render_template('/')
            # subUserRoot
            active_user_session = subUser_root[0][0]

            # fetch workers
            cur.execute("SELECT * FROM family_form where id=? AND form_created_by=?", (fmId, active_user_session))
            fmData = cur.fetchall()

            # get Family member Path details
            fmRegNo =  fmData[0][4]
            formUniqueKey = fmData[0][3]
            cur.execute("SELECT id, form_worker_reg_no FROM half_form WHERE form_unique_key=?", (formUniqueKey,))
            workerRegN = cur.fetchall()
            if workerRegN:
                workerId = workerRegN[0][0]
                workerRegNo = workerRegN[0][1]
            
            docsPath = f"./static/documents/{active_user_session}Docs/{workerRegNo}/familyMembers/{fmRegNo}/"
 

            return render_template('sub-user-view-family-member.html', wori=workerId, worReN=workerRegNo, fmN=fmN, docsPath=docsPath, fmData=fmData)
        except Exception as e:
            return redirect('/sub-user-registration-list')
    else:
        return redirect('/')
    

# sub-user-Edit Registered Worker
@app.route("/sub-user-edit-registered-worker", methods=['GET', 'POST'])
def subUser_editRegisteredWorker():
    if 'subUser_session' in session:
        try:
            workerId = request.args.get('view-regWor')
            

            conn = get_db_connection()
            cur = conn.cursor()

            subUser_session = session.get('subUser_session')
            # get Sub User Parent 
            subUser_root = cur.execute("SELECT creator FROM sub_users WHERE username=?", (subUser_session,))
            subUser_root = subUser_root.fetchall()
            subUser_rootLen = len(subUser_root)
            if subUser_rootLen == 0:
                return render_template('/')
            # subUserRoot
            active_user_session = subUser_root[0][0]

            # fetch workers
            cur.execute("SELECT * FROM half_form where id=? AND form_created_by=?", (workerId, active_user_session))
            workerD = cur.fetchall()
            form_unique_key = workerD[0][44]

            # fetch worker Docs
            cur.execute("SELECT * FROM workers_document WHERE form_unique_key=?", (form_unique_key,))
            workerDocs = cur.fetchall()

            # fetch worker Family members
            cur.execute("SELECT * FROM family_form where form_unique_key=?", (form_unique_key,))
            workerFM = cur.fetchall()
            return render_template('sub-user-edit-registered-worker.html', workerList = workerD, workerDocs=workerDocs, workerFM=workerFM)
        except Exception as e:
            return redirect('/sub-user-registration-list')
    else:
        return redirect('/')
    
# sub-user- Update Registered Worker
@app.route("/sub-user-update-registered-worker", methods=['POST'])
def subUser_updateRegisteredWorker():
    if 'subUser_session' in session:
        if request.method == 'POST':
            conn = get_db_connection()
            cur = conn.cursor()

            subUser_session = session.get('subUser_session')
            # get Sub User Parent 
            subUser_root = cur.execute("SELECT creator FROM sub_users WHERE username=?", (subUser_session,))
            subUser_root = subUser_root.fetchall()
            subUser_rootLen = len(subUser_root)
            if subUser_rootLen == 0:
                return render_template('/')
            # subUserRoot
            active_user_session = subUser_root[0][0]

            w_id = request.form.get('w_id')
            w_name = request.form.get('w_name')
            w_fm_no = request.form.get('w_fm_no')
            w_status = request.form.get('w_status')
            w_gender = request.form.get('w_gender')

            w_dob = request.form.get('w_dob')
            w_citizenship = request.form.get('w_citizenship')
            w_marital_status = request.form.get('w_marital_status')
            w_religion = request.form.get('w_religion')
            w_contact_no = request.form.get('w_contact_no')

            w_address1 = request.form.get('w_address1')
            w_address2 = request.form.get('w_address2')
            w_address3 = request.form.get('w_address3')
            w_postcode = request.form.get('w_postcode')
            w_city = request.form.get('w_city')
            w_state = request.form.get('w_state')

            # Update Worker details
            cur.execute("UPDATE half_form SET no_family_mem=?, worker_detail_worker_legal_status=?, worker_detail_name_of_worker=?, worker_detail_gender=?, worker_detail_DOB=?, worker_detail_citizenship=?, worker_detail_marital_status=?, worker_detail_religion=?, worker_detail_contact_no=?, worker_emp_dtl_address1=?, worker_emp_dtl_address2=?, worker_emp_dtl_address3=?, worker_emp_dtl_postcode=?, worker_emp_dtl_city=?, worker_emp_dtl_state=? WHERE id=?", (w_fm_no, w_status, w_name, w_gender, w_dob, w_citizenship, w_marital_status, w_religion, w_contact_no, w_address1, w_address2, w_address3, w_postcode, w_city, w_state, w_id))
            conn.commit()
            conn.close()

            session['sub_user_registration_list_update'] = 'success'
            return redirect('/sub-user-registration-list')
        else:
            response = {
                'status': 'error',
                'msg': 'method error'
            }
            return jsonify(response)
    else:
        return redirect('/')



# sub-user- Update Registered Worker Docs
@app.route("/sub-user-update-worker-docs", methods=['POST'])
def subUser_updateWorkerDocs():
    if 'subUser_session' in session:
        if request.method == 'POST':
            conn = get_db_connection()
            cur = conn.cursor()

            subUser_session = session.get('subUser_session')
            # get Sub User Parent 
            subUser_root = cur.execute("SELECT creator FROM sub_users WHERE username=?", (subUser_session,))
            subUser_root = subUser_root.fetchall()
            subUser_rootLen = len(subUser_root)
            if subUser_rootLen == 0:
                return render_template('/')
            # subUserRoot
            active_user_session = subUser_root[0][0]

            docs_id = request.form.get('docs_id')
            type_of_document = request.form.get('type_of_document')
            document_id = request.form.get('document_id')
            place_of_issue = request.form.get('place_of_issue')
            issue_date = request.form.get('issue_date')

            expiry_date = request.form.get('expiry_date')
            issuing_country = request.form.get('issuing_country')
            document_status = request.form.get('document_status')
            document_current_status = request.form.get('document_current_status')
        
            # Update Worker details
            cur.execute("UPDATE workers_document SET type_of_douments=?, document_id=?, place_of_issue=?, document_issued_date=?, document_expiry_date=?, issuing_country=?, document_status=?, status_of_current_document=?  WHERE id=?", (type_of_document, document_id, place_of_issue, issue_date, expiry_date, issuing_country, document_status, document_current_status, docs_id))
            conn.commit()
            conn.close()
            session['sub_user_registration_list_update'] = 'success'
            return redirect('/sub-user-registration-list')   
        else:
            response = {
                'status': 'error',
                'msg': 'method error'
            }
            return jsonify(response)
    else:
        return redirect('/')


# sub-user- edit-family-member
@app.route("/sub-user-edit-family-member", methods=['GET', 'POST'])
def subUser_editFamilyMember():
    if 'subUser_session' in session:

        try:
            fmId = request.args.get('fm')
            
            conn = get_db_connection()
            cur = conn.cursor()

            subUser_session = session.get('subUser_session')
            # get Sub User Parent 
            subUser_root = cur.execute("SELECT creator FROM sub_users WHERE username=?", (subUser_session,))
            subUser_root = subUser_root.fetchall()
            subUser_rootLen = len(subUser_root)
            if subUser_rootLen == 0:
                return render_template('/')
            # subUserRoot
            active_user_session = subUser_root[0][0]

            # fetch workers
            cur.execute("SELECT * FROM family_form where id=? AND form_created_by=?", (fmId, active_user_session))
            fmData = cur.fetchall()

            # get Family member Path details
            fmRegNo =  fmData[0][4]
            formUniqueKey = fmData[0][3]
            cur.execute("SELECT id, form_worker_reg_no FROM half_form WHERE form_unique_key=?", (formUniqueKey,))
            workerRegN = cur.fetchall()
            if workerRegN:
                workerId = workerRegN[0][0]

            return render_template('sub-user-edit-family-member.html', wori=workerId, fmData=fmData)
        except Exception as e:
            return redirect('/sub-user-registration-list')
    else:
        return redirect('/')
    

# sub-user- Update Family Member
@app.route("/sub-user-update-family-member", methods=['POST'])
def subUser_updateFamilyMember():
    if 'subUser_session' in session:
        if request.method == 'POST':
            conn = get_db_connection()
            cur = conn.cursor()

            subUser_session = session.get('subUser_session')
            # get Sub User Parent 
            subUser_root = cur.execute("SELECT creator FROM sub_users WHERE username=?", (subUser_session,))
            subUser_root = subUser_root.fetchall()
            subUser_rootLen = len(subUser_root)
            if subUser_rootLen == 0:
                return render_template('/')
            # subUserRoot
            active_user_session = subUser_root[0][0]

            fm_id = request.form.get('fm_id')

            fm_name = request.form.get('fm_name')
            fm_relationship = request.form.get('fm_relationship')
            fm_family_name = request.form.get('fm_family_name')
            family_together = request.form.get('family_together')
            poe = request.form.get('poe')

            gender = request.form.get('gender')
            marital_status = request.form.get('marital_status')
            citizenship = request.form.get('citizenship')
            religion = request.form.get('religion')
            address1 = request.form.get('address1')

            address2 = request.form.get('address2')
            address3 = request.form.get('address3')
            postcode = request.form.get('postcode')
            city = request.form.get('city')
            state = request.form.get('state')

            contact_no = request.form.get('contact_no')
            race = request.form.get('race')
            place_of_birth = request.form.get('place_of_birth')
            employee_status = request.form.get('employee_status')
            employee_name = request.form.get('employee_name')
            employee_address = request.form.get('employee_address')

            # Docs 1
            type_of_document1 = request.form.get('type_of_document1')
            document_id1 = request.form.get('document_id1')
            place_of_issue1 = request.form.get('place_of_issue1')
            issue_date1 = request.form.get('issue_date1')
            expiry_date1 = request.form.get('expiry_date1')
            issuing_country1 = request.form.get('issuing_country1')
            document_status1 = request.form.get('document_status1')
            document_current_status1 = request.form.get('document_current_status1')

            # Docs 2
            type_of_document2 = request.form.get('type_of_document2')
            document_id2 = request.form.get('document_id2')
            place_of_issue2 = request.form.get('place_of_issue2')
            issue_date2 = request.form.get('issue_date2')
            expiry_date2 = request.form.get('expiry_date2')
            issuing_country2 = request.form.get('issuing_country2')
            document_status2 = request.form.get('document_status2')
            document_current_status2 = request.form.get('document_current_status2')
        
            # Update Worker details
            cur.execute("UPDATE family_form SET family_form_name_of_family_member=?, family_form_relationship=?, family_form_family_name=?, family_form_is_famliy_togther=?, family_form_family_form_poe=?, family_form_gender=?, family_form_marital_status=?, family_form_citizenship=?, family_form_religion=?, family_form_address1=?, family_form_address2=?, family_form_address3=?, family_form_postcode=?, family_form_city=?, family_form_state=?, family_form_contact_no=?, family_form_race=?, family_form_place_of_birth=?, family_form_emp_status=?, family_form_emp_name=?, family_form_emp_address=?, fmDoc1_type_of_documents=?, fmDoc1_document_id=?, fmDoc1_place_of_issue=?, fmDoc1_document_issued_date=?, fmDoc1_document_expiry_date=?, fmDoc1_issuing_country=?, fmDoc1_document_status=?, fmDoc1_status_of_current_document=?, fmDoc2_type_of_documents=?, fmDoc2_document_id=?, fmDoc2_place_of_issue=?, fmDoc2_document_issued_date=?, fmDoc2_document_expiry_date=?, fmDoc2_issuing_country=?, fmDoc2_document_status=?, fmDoc2_status_of_current_document=? WHERE id=?", (fm_name, fm_relationship, fm_family_name, family_together, poe, gender, marital_status, citizenship, religion, address1, address2, address3, postcode, city, state, contact_no, race, place_of_birth, employee_status, employee_name, employee_address, type_of_document1, document_id1, place_of_issue1, issue_date1, expiry_date1, issuing_country1, document_status1, document_current_status1, type_of_document2, document_id2, place_of_issue2, issue_date2, expiry_date2, issuing_country2, document_status2, document_current_status2, fm_id))
            conn.commit()
            conn.close()
            session['sub_user_registration_list_update'] = 'success'
            return redirect('/sub-user-registration-list')   
        else:
            response = {
                'status': 'error',
                'msg': 'method error'
            }
            return jsonify(response)
    else:
        return redirect('/')
    
# sub-user- delete workers and their family members
@app.route("/sub-user-del-registered-worker", methods=['GET'])
def subUser_delRegisteredWorker():
    if 'subUser_session' in session:
        try:
            worker_id = request.args.get('del')
            
            conn = get_db_connection()
            cur = conn.cursor()

            subUser_session = session.get('subUser_session')
            # get Sub User Parent 
            subUser_root = cur.execute("SELECT creator FROM sub_users WHERE username=?", (subUser_session,))
            subUser_root = subUser_root.fetchall()
            subUser_rootLen = len(subUser_root)
            if subUser_rootLen == 0:
                return render_template('/')
            # subUserRoot
            active_user_session = subUser_root[0][0]

            # fetch workers
            cur.execute("SELECT form_unique_key FROM half_form where id=? AND form_created_by=?", (worker_id, active_user_session))
            workerKey = cur.fetchall()
            form_unique_key = workerKey[0][0]

            # del worker
            cur.execute("DELETE FROM half_form WHERE id=? AND form_created_by=?", (worker_id, active_user_session))
            # del worker documents
            cur.execute("DELETE FROM workers_document where form_unique_key=?", (form_unique_key,))
            # del worker family members
            cur.execute("DELETE FROM family_form where form_unique_key=?", (form_unique_key,))
            # del workers from Sub-User-Datalog
            cur.execute("DELETE FROM sub_users_datalog where form_unique_key=?", (form_unique_key,))
            
            conn.commit()
            conn.close()
            session['sub_user_registration_list_delete'] = 'success'
            return redirect('/sub-user-registration-list')
        except Exception as e:
            return redirect('/sub-user-registration-list')
    else:
        return redirect('/')



# Sub USer Excel Download  sub-user-download-excel-file
# Download Excel File
@app.route('/sub-user-download-excel-file', methods=['GET'])
def subUser_download_log():
    if 'subUser_session' in session:
        try:
            scheme = request.scheme
            port = request.environ.get('SERVER_PORT')

            conn = get_db_connection()
            cur = conn.cursor()

            subUser_session = session.get('subUser_session')
            # get Sub User Parent 
            subUser_root = cur.execute("SELECT creator FROM sub_users WHERE username=?", (subUser_session,))
            subUser_root = subUser_root.fetchall()
            subUser_rootLen = len(subUser_root)
            if subUser_rootLen == 0:
                return render_template('/')
            # subUserRoot
            active_user_session = subUser_root[0][0]

            workerData = request.args.get('file')

            #  Single Id
            def check_num(num):
                if num.isdigit():
                    return 'single_id'    
                return None
            
            result_single = check_num(workerData)
            
            if workerData == 'exportAll':
                cur.execute("SELECT form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe,worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, form_position, form_status, form_unique_key FROM half_form WHERE form_created_by=?", (active_user_session,))
                #log = cur.fetchall()
                log1 = cur.fetchall()

                # testing Code
                log = []

                for worker_allData in log1:

                    excelWorker = ['WORKER', worker_allData[0], worker_allData[1], worker_allData[2], worker_allData[3], worker_allData[4], worker_allData[5], worker_allData[6], worker_allData[7], worker_allData[8], worker_allData[9], worker_allData[10], worker_allData[11], worker_allData[12], worker_allData[13], worker_allData[14], worker_allData[15], worker_allData[16], worker_allData[17], worker_allData[18], worker_allData[19], worker_allData[20], worker_allData[21], worker_allData[22], worker_allData[23], worker_allData[24], worker_allData[25], worker_allData[26], worker_allData[27], worker_allData[28], worker_allData[29], worker_allData[30]]
                    excel_formUniqueKey = worker_allData[31]
                    #print(excel_formUniqueKey)

                    docs_level = ['', 'Type of Document', 'Document ID', 'Place of Issue', 'Issue Date', 'Expiry Date', 'Issuing Country', 'Document Status', 'Status of Current Document', 'Document Link']
                    
                    # push all worker data & docs level
                    log.append(excelWorker)
                    log.append([''])
                    log.append(docs_level)
                    
                    # Worker Documents
                    cur.execute("SELECT * FROM workers_document WHERE form_unique_key=?", (excel_formUniqueKey,))
                    excel_workerDocs = cur.fetchall()
                    docsIndex = 1
                    for xWDocs in excel_workerDocs:
                        xWorkerData = [ f"Document {docsIndex}", xWDocs[3], xWDocs[4], xWDocs[5], xWDocs[6], xWDocs[7], xWDocs[8], xWDocs[9], xWDocs[10], f'{scheme}://{ip_address}:{port}/static/documents/{active_user_session}Docs/{worker_allData[2]}/doc{docsIndex}/uploaded_image.jpg']
                        #print(xWorkerData)
                        log.append(xWorkerData)
                        docsIndex += 1

                    # Worker Family Members Labels
                    fm_label = ['', 'Created by', 'Created Date', 'Registration No', 'Worker Name', 'Relationship', 'Name', 'Family Name', 'Is Family Together', 'Point of Entry', 'Citizenship', 'Religion', 'Marital Status', 'Gender', 'Address 1', 'Address 2', 'Address 3', 'Postcode', 'City', 'State', 'Contact No', 'Race', 'Place of Birth', 'Employment Status', 'Employer Name', 'Employer Address', 'Type of Document 1', 'Document ID 1', 'Place of Issue 1', 'Issued Date 1', 'Expiry Date 1', 'Issuing Country 1', 'Document Status 1', 'Status of Current Document 1', 'Document Link 1', 'Type of Document 2', 'Document ID 2', 'Place of Issue 2', 'Issued Date 2', 'Expiry Date 2', 'Issuing Country 2', 'Document Status 2', 'Status of Current Document 2', 'Document Link 2']
                    log.append([''])
                    log.append(fm_label)

                    # Worker Family Members
                    cur.execute("SELECT * FROM family_form WHERE form_unique_key=?", (excel_formUniqueKey,))
                    excel_workerFM = cur.fetchall()
                    fmIndex = 1
                    for xW_FM in excel_workerFM:
                        xWorkerFM = [ f"Family Member {fmIndex}", xW_FM[1], xW_FM[2], f"{worker_allData[2]}-{fmIndex}", xW_FM[5], xW_FM[6], xW_FM[7], xW_FM[8], xW_FM[9], xW_FM[10], xW_FM[11], xW_FM[12], xW_FM[13], xW_FM[14], xW_FM[15], xW_FM[16], xW_FM[17], xW_FM[18], xW_FM[19], xW_FM[20], xW_FM[21], xW_FM[22], xW_FM[23], xW_FM[24], xW_FM[25], xW_FM[26], xW_FM[30], xW_FM[31], xW_FM[32], xW_FM[33], xW_FM[34], xW_FM[35], xW_FM[36], xW_FM[37], f'{scheme}://{ip_address}:{port}/static/documents/{active_user_session}Docs/{worker_allData[2]}/familyMember/{xW_FM[4]}/doc1/uploaded_image.jpg', xW_FM[38], xW_FM[39], xW_FM[40], xW_FM[41], xW_FM[42], xW_FM[43], xW_FM[44], xW_FM[45], f'{scheme}://{ip_address}:{port}/static/documents/{active_user_session}Docs/{worker_allData[2]}/familyMember/{xW_FM[4]}/doc2/uploaded_image.jpg']
                        #print(xWorkerFM)
                        log.append(xWorkerFM)
                        fmIndex += 1

                    log.append([''])
                    # End testing Code

            elif result_single == 'single_id':
                workerId = workerData
                cur.execute("SELECT form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe,worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, form_position, form_status, form_unique_key FROM half_form where id=? AND form_created_by=?", (workerId, active_user_session))
                #log = cur.fetchall()

                # testing Code
                log = []

                log1 = cur.fetchall()
                
                excelWorker = ['WORKER', log1[0][0], log1[0][1], log1[0][2], log1[0][3], log1[0][4], log1[0][5], log1[0][6], log1[0][7], log1[0][8], log1[0][9], log1[0][10], log1[0][11], log1[0][12], log1[0][13], log1[0][14], log1[0][15], log1[0][16], log1[0][17], log1[0][18], log1[0][19], log1[0][20], log1[0][21], log1[0][22], log1[0][23], log1[0][24], log1[0][25], log1[0][26], log1[0][27], log1[0][28], log1[0][29], log1[0][30]]
                excel_formUniqueKey = log1[0][31]
                #print(excel_formUniqueKey)

                docs_level = ['', 'Type of Document', 'Document ID', 'Place of Issue', 'Issue Date', 'Expiry Date', 'Issuing Country', 'Document Status', 'Status of Current Document', 'Document Link']
                
                # push all worker data & docs level
                log.append(excelWorker)
                log.append([''])
                log.append(docs_level)
                
                # Worker Documents
                cur.execute("SELECT * FROM workers_document WHERE form_unique_key=?", (excel_formUniqueKey,))
                excel_workerDocs = cur.fetchall()
                docsIndex = 1
                for xWDocs in excel_workerDocs:
                    xWorkerData = [ f"Document {docsIndex}", xWDocs[3], xWDocs[4], xWDocs[5], xWDocs[6], xWDocs[7], xWDocs[8], xWDocs[9], xWDocs[10], f'{scheme}://{ip_address}:{port}/static/documents/{active_user_session}Docs/{log1[0][2]}/doc{docsIndex}/uploaded_image.jpg']
                    #print(xWorkerData)
                    log.append(xWorkerData)
                    docsIndex += 1

                # Worker Family Members Labels
                fm_label = ['', 'Created by', 'Created Date', 'Registration No', 'Worker Name', 'Relationship', 'Name', 'Family Name', 'Is Family Together', 'Point of Entry', 'Citizenship', 'Religion', 'Marital Status', 'Gender', 'Address 1', 'Address 2', 'Address 3', 'Postcode', 'City', 'State', 'Contact No', 'Race', 'Place of Birth', 'Employment Status', 'Employer Name', 'Employer Address', 'Type of Document 1', 'Document ID 1', 'Place of Issue 1', 'Issued Date 1', 'Expiry Date 1', 'Issuing Country 1', 'Document Status 1', 'Status of Current Document 1', 'Document Link 1', 'Type of Document 2', 'Document ID 2', 'Place of Issue 2', 'Issued Date 2', 'Expiry Date 2', 'Issuing Country 2', 'Document Status 2', 'Status of Current Document 2', 'Document Link 2']
                log.append([''])
                log.append(fm_label)

                # Worker Family Members
                cur.execute("SELECT * FROM family_form WHERE form_unique_key=?", (excel_formUniqueKey,))
                excel_workerFM = cur.fetchall()
                fmIndex = 1
                for xW_FM in excel_workerFM:
                    xWorkerFM = [ f"Family Member {fmIndex}", xW_FM[1], xW_FM[2], f"{log1[0][2]}-{fmIndex}", xW_FM[5], xW_FM[6], xW_FM[7], xW_FM[8], xW_FM[9], xW_FM[10], xW_FM[11], xW_FM[12], xW_FM[13], xW_FM[14], xW_FM[15], xW_FM[16], xW_FM[17], xW_FM[18], xW_FM[19], xW_FM[20], xW_FM[21], xW_FM[22], xW_FM[23], xW_FM[24], xW_FM[25], xW_FM[26], xW_FM[30], xW_FM[31], xW_FM[32], xW_FM[33], xW_FM[34], xW_FM[35], xW_FM[36], xW_FM[37], f'{scheme}://{ip_address}:{port}/static/documents/{active_user_session}Docs/{log1[0][2]}/familyMember/{xW_FM[4]}/doc1/uploaded_image.jpg', xW_FM[38], xW_FM[39], xW_FM[40], xW_FM[41], xW_FM[42], xW_FM[43], xW_FM[44], xW_FM[45], f'{scheme}://{ip_address}:{port}/static/documents/{active_user_session}Docs/{log1[0][2]}/familyMember/{xW_FM[4]}/doc2/uploaded_image.jpg']
                    #print(xWorkerFM)
                    log.append(xWorkerFM)
                    fmIndex += 1

                log.append([''])
                # End testing Code

            else:
                workerId = json.loads(workerData)
                cur.execute("SELECT form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe,worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, form_position, form_status, form_unique_key FROM half_form WHERE id IN ("+workerId+") AND form_created_by='"+active_user_session+"'")
                log1 = cur.fetchall()

                # testing Code
                log = []

                for worker_allData in log1:

                    excelWorker = ['WORKER', worker_allData[0], worker_allData[1], worker_allData[2], worker_allData[3], worker_allData[4], worker_allData[5], worker_allData[6], worker_allData[7], worker_allData[8], worker_allData[9], worker_allData[10], worker_allData[11], worker_allData[12], worker_allData[13], worker_allData[14], worker_allData[15], worker_allData[16], worker_allData[17], worker_allData[18], worker_allData[19], worker_allData[20], worker_allData[21], worker_allData[22], worker_allData[23], worker_allData[24], worker_allData[25], worker_allData[26], worker_allData[27], worker_allData[28], worker_allData[29], worker_allData[30]]
                    excel_formUniqueKey = worker_allData[31]
                    #print(excel_formUniqueKey)

                    docs_level = ['', 'Type of Document', 'Document ID', 'Place of Issue', 'Issue Date', 'Expiry Date', 'Issuing Country', 'Document Status', 'Status of Current Document', 'Document Link']
                    
                    # push all worker data & docs level
                    log.append(excelWorker)
                    log.append([''])
                    log.append(docs_level)
                    
                    # Worker Documents
                    cur.execute("SELECT * FROM workers_document WHERE form_unique_key=?", (excel_formUniqueKey,))
                    excel_workerDocs = cur.fetchall()
                    docsIndex = 1
                    for xWDocs in excel_workerDocs:
                        xWorkerData = [ f"Document {docsIndex}", xWDocs[3], xWDocs[4], xWDocs[5], xWDocs[6], xWDocs[7], xWDocs[8], xWDocs[9], xWDocs[10], f'{scheme}://{ip_address}:{port}/static/documents/{active_user_session}Docs/{worker_allData[2]}/doc{docsIndex}/uploaded_image.jpg']
                        #print(xWorkerData)
                        log.append(xWorkerData)
                        docsIndex += 1

                    # Worker Family Members Labels
                    fm_label = ['', 'Created by', 'Created Date', 'Registration No', 'Worker Name', 'Relationship', 'Name', 'Family Name', 'Is Family Together', 'Point of Entry', 'Citizenship', 'Religion', 'Marital Status', 'Gender', 'Address 1', 'Address 2', 'Address 3', 'Postcode', 'City', 'State', 'Contact No', 'Race', 'Place of Birth', 'Employment Status', 'Employer Name', 'Employer Address', 'Type of Document 1', 'Document ID 1', 'Place of Issue 1', 'Issued Date 1', 'Expiry Date 1', 'Issuing Country 1', 'Document Status 1', 'Status of Current Document 1', 'Document Link 1', 'Type of Document 2', 'Document ID 2', 'Place of Issue 2', 'Issued Date 2', 'Expiry Date 2', 'Issuing Country 2', 'Document Status 2', 'Status of Current Document 2', 'Document Link 2']
                    log.append([''])
                    log.append(fm_label)

                    # Worker Family Members
                    cur.execute("SELECT * FROM family_form WHERE form_unique_key=?", (excel_formUniqueKey,))
                    excel_workerFM = cur.fetchall()
                    fmIndex = 1
                    for xW_FM in excel_workerFM:
                        xWorkerFM = [ f"Family Member {fmIndex}", xW_FM[1], xW_FM[2], f"{worker_allData[2]}-{fmIndex}", xW_FM[5], xW_FM[6], xW_FM[7], xW_FM[8], xW_FM[9], xW_FM[10], xW_FM[11], xW_FM[12], xW_FM[13], xW_FM[14], xW_FM[15], xW_FM[16], xW_FM[17], xW_FM[18], xW_FM[19], xW_FM[20], xW_FM[21], xW_FM[22], xW_FM[23], xW_FM[24], xW_FM[25], xW_FM[26], xW_FM[30], xW_FM[31], xW_FM[32], xW_FM[33], xW_FM[34], xW_FM[35], xW_FM[36], xW_FM[37], f'{scheme}://{ip_address}:{port}/static/documents/{active_user_session}Docs/{worker_allData[2]}/familyMember/{xW_FM[4]}/doc1/uploaded_image.jpg', xW_FM[38], xW_FM[39], xW_FM[40], xW_FM[41], xW_FM[42], xW_FM[43], xW_FM[44], xW_FM[45], f'{scheme}://{ip_address}:{port}/static/documents/{active_user_session}Docs/{worker_allData[2]}/familyMember/{xW_FM[4]}/doc2/uploaded_image.jpg']
                        #print(xWorkerFM)
                        log.append(xWorkerFM)
                        fmIndex += 1

                    log.append([''])
                    # End testing Code

            
            def generate():
                data = StringIO()
                w = csv.writer(data)

                # write header
                w.writerow(('', 'Created by', 'Created Date', 'Registration No', 'No of Family Member', 'Legal Status', 'Name of Worker', 'Family Name', 'Gender', 'Date of Birth', 'Place of Birth', 'Citizenship', 'Marital Status', 'Point of Entry', 'Religion', 'Race', 'Contact No', 'E-mail', 'NOK', 'Relationship', 'NOK Contact No', 'Job Sector', 'Job Sub Sector', 'Employment Sponsorship Status', 'Address 1', 'Address 2', 'Address 3', 'Postcode', 'City', 'State', 'Position', 'Status'))
                yield data.getvalue()
                data.seek(0)
                data.truncate(0)

                # write each log item
                for item in log:
                    w.writerow(item)
                    yield data.getvalue()
                    data.seek(0)
                    data.truncate(0)

            # stream the response as the data is generated
            response = Response(generate(), mimetype='application/vnd.ms-excel')
            # add a filename
            response.headers.set("Content-Disposition", "attachment", filename="worker.csv")
            return response
        except Exception as e:
            #print('Excel Error- ', e)
            return redirect('/sub-user-registration-list')
    else:
        return redirect('/')























# subUser Logout
@app.route("/sub-user-logout")
def subUserLogout():
    if 'subUser_session' in session:
        session.clear()
        return redirect('/')
    else:
        return redirect('/')
# ========================
#   End * subUser Section
# ========================


# RESTful API > Upload image
@app.route("/api-image", methods=['POST'])
def apiImage():
    if(request.method == 'POST'):
        res = {}
        avatarPath = 'static/img/'
        avatar = request.files['image']
        avatar.save(avatarPath+avatar.filename) 
        #print(avatar)
        res['status'] = 'success'
        return (jsonify(res))
    else:
        res = {}
        res['status'] = 'something wrong!'
        return (jsonify(res))
    
# Set the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part in the request!'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file!'
    
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully!'

    
if __name__ == '__main__':
    #randPort = random.randint(1000, 9999)
    app.run(host=ip_address, port=6700)


'''
def start_webview():
    # Create a webview window
    webview.create_window("FW Registration System Outreach Staff", f"http://{ip_address}:9689/", js_api=True)
    webview.start()

def start_flask():
    app.run(host=ip_address, port=9689)
            

if __name__ == '__main__':
    # Create two threads, one for Flask and one for webview
    flask_thread = threading.Thread(target=start_flask)
    
    # Start the Flask thread
    flask_thread.start()

    # Start webview in the main thread (not in a separate thread)
    start_webview()

    # Wait for the Flask thread to finish (if needed)
    flask_thread.join()

''' 