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


# Internet Connection status
def check_internet():
    try:
        response = requests.get('http://159.223.32.228:6787', timeout=5)
        if response.status_code == 200:
            return ('online')
    except requests.ConnectionError:
        return ('offline')


# SignIn Page
@app.route("/check-connection")
def checkConnection():
    status = check_internet()
    return status



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



'''
@app.route('/print-new-qr')
def print_image_new():
    # image_url = request.form.get('image_url')
    image_url = "C:\\Users\\Admin\\Downloads\\swims-qr.png"
    
    
    try:
        # Download the image from the URL to a temporary file
        response = requests.get(image_url)
        img_data = response.content
        temp_img_path = 'temp_img.png'
        with open(temp_img_path, 'wb') as temp_img_file:
            temp_img_file.write(img_data)

        # Execute the C# executable with the image path as an argument
        csharp_exe =  'C:\\Users\\Admin\\Downloads\\windowsPrint\\bin\\Release\\net7.0\\win-x64\\windowsPrint.exe'  # 
        subprocess.run([csharp_exe, temp_img_path], check=True)

        # Delete the temporary image file
        os.remove(temp_img_path)

        return jsonify({'message': 'Image printed successfully.'})

    except Exception as e:
        return jsonify({'error': str(e)})
'''





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
        status = 'Block'

        # Database
        conn = get_db_connection()
        cur = conn.cursor()

        if username and password:
            try:
                # Admin Auth
                admin = cur.execute("SELECT email FROM admin WHERE email=? AND password=?", (username, password))
                admin = admin.fetchall()
                adminLen = len(admin)

                # Sub Admin Auth
                subAdmin = cur.execute("SELECT email FROM sub_admin WHERE email=? AND password=?", (username, password))
                subAdmin = subAdmin.fetchall()
                subAdmin_len = len(subAdmin)

                # Sub Admin Auth Check Status
                subAdmin_status = cur.execute("SELECT email FROM sub_admin WHERE email=? AND status=?", (username, password))
                subAdmin_status = subAdmin_status.fetchall()
                subAdmin_status_len = len(subAdmin_status)
                if subAdmin_status_len == 1:
                    session['auth_error']  = 'block'
                    return redirect('/')

                # Users Auth
                user = cur.execute("SELECT email FROM users WHERE email=? AND password=?", (username, password))
                user = user.fetchall()
                userLen = len(user)

                # Sub Users Auth
                subUser = cur.execute("SELECT username FROM sub_users WHERE username=? AND password=?", (username, password))
                subUser = subUser.fetchall()
                subUser_len = len(subUser)

                
                if(adminLen == 1):
                    adminSession = admin[0][0]
                    session['admin_session']  = adminSession
                    return redirect('/admin-dash')

                if(subAdmin_len == 1):
                    subAdminSession = subAdmin[0][0]
                    session['subAdmin_session']  = subAdminSession
                    return redirect('/sub-admin-dash') 
                
                elif(userLen == 1):
                    userSession = user[0][0]
                    session['user_session'] = userSession
                    return redirect('/add-worker')
                
                elif(subUser_len == 1):
                    subUserSession = subUser[0][0]
                    session['subUser_session']  = subUserSession
                    return redirect('/sub-user-add-worker')
                    
                else:
                    session['auth_error']  = 'error'
                    return redirect('/')
            except Exception as e:
                return redirect('/')
        else:    
            return redirect('/')
    else:
        return redirect('/')
    



# -----------------------
# * Start Admin Section *
# -----------------------

# admin dash
@app.route('/admin-dash')
def adminDash():
    if 'admin_session' in session:
        dateToday = datetime.now().strftime('%Y-%m-%d')
        # DB
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM outreach WHERE date_for=?", (dateToday, ))
        outreach = cur.fetchall()
        if outreach:
            plantation_name = outreach[0][2]
            total_legal_worker = outreach[0][3]
            total_undocumented_worker = outreach[0][4]
            total_legal_fm = outreach[0][5]
            total_undocumented_fm = outreach[0][6]
            total_pati_imm = outreach[0][7]
        else:
            plantation_name = 0
            total_legal_worker = 0
            total_undocumented_worker = 0
            total_legal_fm = 0
            total_undocumented_fm = 0
            total_pati_imm = 0


        totalData = int(total_legal_worker) + int(total_undocumented_worker) + int(total_legal_fm) + int(total_undocumented_fm) + int(total_pati_imm)

        return render_template('admin-dash.html', plantation_name=plantation_name, total_legal_worker=total_legal_worker, total_undocumented_worker=total_undocumented_worker, total_legal_fm=total_legal_fm, total_undocumented_fm=total_undocumented_fm, total_pati_imm=total_pati_imm, totalData=totalData)
    
    else:
        return redirect('/')
    

# admin Outreach
@app.route('/admin-outreach')
def adminOutreach():
    if 'admin_session' in session:
        return render_template('admin-outreach.html')
    else:
        return redirect('/')


# admin Insert Outreach
@app.route('/admin-insert-outreach', methods=['POST'])
def adminInsertOutreach():
    if 'admin_session' in session:
        try:
            date_for = request.form.get('date_for')
            plantation_name = request.form.get('plantation_name')
            total_legal_worker = request.form.get('total_legal_worker')
            total_undocumented_worker = request.form.get('total_undocumented_worker')
            total_legal_fm = request.form.get('total_legal_fm')
            total_undocumented_fm = request.form.get('total_undocumented_fm')
            total_pati_imm = request.form.get('total_pati_imm')

            # Date & Time
            creation_date = datetime.now().strftime('%d/%m/%Y')
            creation_time = datetime.now().strftime('%H:%M:%S')
            
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            # Check Outreach
            dateToday = datetime.now().strftime('%Y-%m-%d')
            cur.execute("SELECT * FROM outreach WHERE date_for=?", (dateToday, ))
            outreach = cur.fetchall()
            if outreach:
                session['admin_outreach_status'] = 'exist'
                return redirect('/admin-outreach')


            # Insert Outreach
            cur.execute("INSERT INTO outreach(date_for, plantation_name, total_legal_worker, total_undocumented_worker, total_legal_fm, total_undocumented_fm, total_pati_imm, creation_date, creation_time) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (date_for, plantation_name, total_legal_worker, total_undocumented_worker, total_legal_fm, total_undocumented_fm, total_pati_imm, creation_date, creation_time))
            conn.commit()
            conn.close()

            session['admin_outreach_status'] = 'success'
            return redirect('/admin-outreach')
        except Exception as e:
                #print(e)
                session['admin_outreach_status'] = 'error'
                return redirect('/admin-outreach')
    else:
        return redirect('/')
    


# admin profile
@app.route('/admin-profile')
def adminProfile():
    if 'admin_session' in session:
        # DB
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin where id=1")
        profile = cur.fetchall()
        return render_template('admin-profile.html', profileData=profile)
    
    else:
        return redirect('/')
    

# admin Update profile
@app.route('/admin-update-profile', methods=['POST'])
def adminUpdateProfile():
    if 'admin_session' in session:
        try:
            x_path = 'static/img/admin/'
            #avatar.save(avatarPath+avatar.filename)

            profile = request.files['profile']
            userID = request.form.get('userID')
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            
            profile_path = x_path + profile.filename
            #print(profile_path)

            # DB
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("UPDATE admin SET name=?, email=?, password=?, profile_path=? where id=?", (name, email, password, profile_path, userID))
            conn.commit()
            conn.close()
            
            profile.save(profile_path)

            session['admin_update_status'] = 'success'
            return redirect('/admin-profile')
        except Exception as e:
                session['admin_update_status'] = 'error'
                return redirect('/admin-profile')
    else:
        return redirect('/')
    
    
# Admin Create Exe Users
@app.route('/admin-create-exe-users')
def adminCreateExeUsers():
    if 'admin_session' in session:
        return render_template('admin-create-exe-users.html', profileData=profile)
    else:
        return redirect('/')
    
# Admin Insert Exe Users
@app.route('/admin-insert-exe-users', methods=['POST'])
def adminInsertExeUsers():
    if 'admin_session' in session:
        if request.method == 'POST':
            try:
                user_name = request.form.get('user_name')
                user_email = request.form.get('user_email')
                user_password = request.form.get('user_password')

                dateStr = datetime.now().strftime('%d%m%Y')
                timeStr = datetime.now().strftime('%H%M%S')
                randStr = random.randrange(100000, 999999)
                worker_registration_prefix = f'R{randStr}SN{dateStr}{timeStr}'

                created_at = current_date
                created_time = formatted_time

                # DB
                conn = get_db_connection()
                cur = conn.cursor()

                # Check Admin
                admin = cur.execute('SELECT email FROM admin WHERE email=?', (user_email,))
                admin = cur.fetchall()
                adminLen = len(admin)
                if adminLen == 1:
                    session['admin_create_exe_users_status'] = 'user_exist'
                    return render_template('admin-create-exe-users.html')
                

                # Check Sub Admin
                subAdmin = cur.execute('SELECT email FROM sub_admin WHERE email=?', (user_email,))
                subAdmin = cur.fetchall()
                subAdminLen = len(subAdmin)
                if subAdminLen == 1:
                    session['admin_create_exe_users_status'] = 'user_exist'
                    return render_template('admin-create-exe-users.html')


                # Check Users
                users = cur.execute('SELECT email FROM users WHERE email=?', (user_email,))
                users = cur.fetchall()
                userLen = len(users)

                
                # Check Worker Registration Prefix
                WRP = cur.execute('SELECT worker_registration_prefix FROM users WHERE worker_registration_prefix=?', (worker_registration_prefix,))
                WRP = cur.fetchall()
                wrpLen = len(WRP)
                if wrpLen == 1:
                    session['admin_create_exe_users_status'] = 'worker_registration_prefix_exist'
                    return render_template('admin-create-exe-users.html')



                if userLen == 1:
                    session['admin_create_exe_users_status'] = 'user_exist'
                    return render_template('admin-create-exe-users.html')
                else:
                    cur.execute('INSERT INTO users(name, email, password, created_at, created_time, worker_registration_prefix) values(?, ?, ?, ?, ?, ?)', (user_name, user_email, user_password, created_at, created_time, worker_registration_prefix))
                    conn.commit()
                    conn.close()

                    # Make Users document Folder
                    usersFolder(user_email)
                    
                    session['admin_create_exe_users_status'] = 'success'
                    return render_template('admin-create-exe-users.html')
            
            except Exception as e:
                session['admin_create_exe_users_status'] = 'error'
                return redirect('/admin-create-exe-users')
            
        else:
            session['admin_create_exe_users_status'] = 'method_error'
            return redirect('/admin-create-exe-users')        
    else:
        return redirect('/')
    


# Admin View Exe Users
@app.route('/admin-view-exe-users')
def adminViewExeUsers():
    if 'admin_session' in session:
        try:
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            users = cur.execute('SELECT id, name, email, password, worker_registration_prefix FROM users')
            users = cur.fetchall()
            totalUsers = len(users)
            userList = users
            
            conn.commit()
            conn.close()
            return render_template('admin-view-exe-users.html', totalUsers=totalUsers, userList=userList)
        except Exception as e:
            return redirect('/admin-dash')       
    else:
        return redirect('/') 

# Admin Edit Exe Users
@app.route('/admin-edit-exe-users', methods=['GET'])
def adminEditExeUsers():
    if 'admin_session' in session:
        try:
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            userID = request.args.get('usI')

            users = cur.execute('SELECT id, name, email, password, worker_registration_prefix FROM users WHERE id=?', (userID,))
            users = cur.fetchall()
            userList = users
            
            conn.commit()
            conn.close()
            return render_template('admin-edit-exe-users.html', userList=userList)
        except Exception as e:
            return redirect('/admin-dash')       
    else:
        return redirect('/')
    
# Admin Update Exe Users
@app.route('/admin-update-exe-users', methods=['POST'])
def adminUpdateExeUsers():
    if 'admin_session' in session:
        try:
            userID = request.form.get('userID')
            user_name = request.form.get('user_name')
            
            user_password = request.form.get('user_password')
            
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('UPDATE users SET name=?, password=? WHERE id=?', (user_name, user_password, userID))
            conn.commit()
            conn.close()
            
            session['admin_update_exe_users_status'] = 'success'
            return redirect('/admin-view-exe-users')
        except Exception as e:
            session['admin_update_exe_users_status'] = 'error'
            return redirect('/admin-view-exe-users')       
    else:
        return redirect('/') 
    

# Admin Del Exe Users
@app.route('/admin-del-exe-users', methods=['GET'])
def adminDelExeUsers():
    if 'admin_session' in session:
        try:
            userID = request.args.get('usI')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM users WHERE id=?', (userID,))
            conn.commit()
            conn.close()
            session['admin_del_exe_users_status'] = 'success'
            return redirect('/admin-view-exe-users')
        except Exception as e:
            session['admin_del_exe_users_status'] = 'error'
            return redirect('/admin-view-exe-users')       
    else:
        return redirect('/') 



# Admin Create Sub Admin
@app.route('/admin-create-sub-admin')
def adminCreateSubAdmin():
    if 'admin_session' in session:
        return render_template('admin-create-sub-admin.html')
    else:
        return redirect('/')
    

# Admin Insert Sub Admin
@app.route('/admin-insert-sub-admin', methods=['POST'])
def adminInsertSubAdmin():
    if 'admin_session' in session:
        if request.method == 'POST':
            try:
                name = request.form.get('name')
                email = request.form.get('email')
                password = request.form.get('password')
                status = 'Active'
                created_at = current_date
                created_time = formatted_time

                # DB
                conn = get_db_connection()
                cur = conn.cursor()

                # Check Admin
                admin = cur.execute('SELECT email FROM admin WHERE email=?', (email,))
                admin = cur.fetchall()
                adminLen = len(admin)
                if adminLen == 1:
                    session['admin_create_sub_admin_status'] = 'user_exist'
                    return render_template('admin-create-sub-admin.html')


                # Check Users
                users = cur.execute('SELECT email FROM users WHERE email=?', (email,))
                users = cur.fetchall()
                userLen = len(users)
                if userLen == 1:
                    session['admin_create_sub_admin_status'] = 'user_exist'
                    return render_template('admin-create-sub-admin.html')

                # Check Sub Admin
                subAdmin = cur.execute('SELECT email FROM sub_admin WHERE email=?', (email,))
                subAdmin = cur.fetchall()
                subAdminLen = len(subAdmin)
                if subAdminLen == 1:
                    session['admin_create_sub_admin_status'] = 'user_exist'
                    return redirect('/admin-create-sub-admin')
                else:
                    cur.execute('INSERT INTO sub_admin(name, email, password, status, created_at, created_time) values(?, ?, ?, ?, ?, ?)', (name, email, password, status, created_at, created_time))
                    conn.commit()
                    conn.close()
                    
                    session['admin_create_sub_admin_status'] = 'success'
                    return redirect('/admin-create-sub-admin')
            
            except Exception as e:
                session['admin_create_sub_admin_status'] = 'error'
                return redirect('/admin-create-sub-admin')
            
        else:
            session['admin_create_sub_admin_status'] = 'method_error'
            return redirect('/admin-create-sub-admin')        
    else:
        return redirect('/')


# Admin View Sub Admin
@app.route('/admin-view-sub-admin')
def adminViewSubAdmin():
    if 'admin_session' in session:
        try:
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            subAdmin = cur.execute('SELECT id, name, email, password, status, created_at FROM sub_admin')
            subAdmin = cur.fetchall()
            total_subAdmin = len(subAdmin)
            subAdmin_list = subAdmin
            
            conn.commit()
            conn.close()
            return render_template('admin-view-sub-admin.html', total_subAdmin=total_subAdmin, subAdmin_list=subAdmin_list)
        except Exception as e:
            return redirect('/admin-dash')       
    else:
        return redirect('/')


# Admin Edit Sub Admin
@app.route('/admin-edit-sub-admin', methods=['GET'])
def adminEditSubAdmin():
    if 'admin_session' in session:
        try:
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            userID = request.args.get('usI')

            users = cur.execute('SELECT id, name, email, password, status FROM sub_admin WHERE id=?', (userID,))
            users = cur.fetchall()
            userList = users
            
            conn.commit()
            conn.close()
            return render_template('admin-edit-sub-admin.html', userList=userList)
        except Exception as e:
            return redirect('/admin-dash')       
    else:
        return redirect('/')
    
# Admin Update Sub Admin
@app.route('/admin-update-sub-admin', methods=['POST'])
def adminUpdateSubAdmin():
    if 'admin_session' in session:
        try:
            userID = request.form.get('userID')
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            status = request.form.get('status')

            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            # Check Admin
            admin = cur.execute('SELECT email FROM admin WHERE email=?', (email,))
            admin = cur.fetchall()
            adminLen = len(admin)
            if adminLen == 1:
                session['admin_update_sub_admin_status'] = 'error'
                return redirect('/admin-view-sub-admin')


            # Check Users
            users = cur.execute('SELECT email FROM users WHERE email=?', (email,))
            users = cur.fetchall()
            userLen = len(users)
            if userLen == 1:
                session['admin_update_sub_admin_status'] = 'error'
                return redirect('/admin-view-sub-admin')

            cur.execute('UPDATE sub_admin SET name=?, email=?, password=?, status=? WHERE id=?', (name, email, password, status, userID))
            conn.commit()
            conn.close()
            
            session['admin_update_sub_admin_status'] = 'success'
            return redirect('/admin-view-sub-admin')
        except Exception as e:
            session['admin_update_sub_admin_status'] = 'error'
            return redirect('/admin-view-sub-admin')       
    else:
        return redirect('/') 
    

# Admin Del Sub Admin
@app.route('/admin-del-sub-admin', methods=['GET'])
def adminDelSubAdmin():
    if 'admin_session' in session:
        try:
            userID = request.args.get('usI')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM sub_admin WHERE id=?', (userID,))
            conn.commit()
            conn.close()
            session['admin_del_sub_admin_status'] = 'success'
            return redirect('/admin-view-sub-admin')
        except Exception as e:
            session['admin_del_sub_admin_status'] = 'error'
            return redirect('/admin-view-sub-admin')       
    else:
        return redirect('/') 


# Admin City
@app.route('/admin-city')
def adminCity():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detailed_dd_city")
        cityList = cur.fetchall()
        return render_template('admin-city.html', cityList=cityList)
    else:
        return redirect('/')
    
@app.route('/admin-create-city', methods=['POST'])
def adminCreateCity():
    if 'admin_session' in session:
        try:
            city = request.form.get('city')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO detailed_dd_city(city, category_list) values(?, ?)', (city, 'City'))
            conn.commit()
            conn.close()
            session['admin_create_city_status'] = 'success'
            return redirect('/admin-city')
        except Exception as e:
            session['admin_create_city_status'] = 'error'
            return redirect('/admin-city')       
    else:
        return redirect('/')
    
# Admin Del City
@app.route('/admin-del-city', methods=['GET'])
def adminDelCity():
    if 'admin_session' in session:
        try:
            delID = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM detailed_dd_city WHERE id=?', (delID,))
            conn.commit()
            conn.close()
            session['admin_del_city_status'] = 'success'
            return redirect('/admin-city')
        except Exception as e:
            session['admin_del_city_status'] = 'error'
            return redirect('/admin-city')       
    else:
        return redirect('/') 


# Admin State
@app.route('/admin-state')
def adminState():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detailed_dd_state")
        dataList = cur.fetchall()
        return render_template('admin-state.html', dataList=dataList)
    else:
        return redirect('/')
    
# admin Create State
@app.route('/admin-create-state', methods=['POST'])
def adminCreateState():
    if 'admin_session' in session:
        try:
            state_data = request.form.get('state')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO detailed_dd_state(state, category_list) values(?, ?)', (state_data, 'State'))
            conn.commit()
            conn.close()
            session['admin_create_state_status'] = 'success'
            return redirect('/admin-state')
        except Exception as e:
            #print(e)
            session['admin_create_state_status'] = 'error'
            return redirect('/admin-state')       
    else:
        return redirect('/')
    
# Admin Del State
@app.route('/admin-del-state', methods=['GET'])
def adminDelState():
    if 'admin_session' in session:
        try:
            delID = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM detailed_dd_state WHERE id=?', (delID,))
            conn.commit()
            conn.close()
            session['admin_del_state_status'] = 'success'
            return redirect('/admin-state')
        except Exception as e:
            session['admin_del_state_status'] = 'error'
            return redirect('/admin-state')       
    else:
        return redirect('/') 
    

# Admin Gender
@app.route('/admin-gender')
def adminGender():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detailed_dd_gender")
        dataList = cur.fetchall()
        return render_template('admin-gender.html', dataList=dataList)
    else:
        return redirect('/')
    
# admin Create Gender
@app.route('/admin-create-gender', methods=['POST'])
def adminCreateGender():
    if 'admin_session' in session:
        try:
            gender = request.form.get('gender')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO detailed_dd_gender(gender, category_list) values(?, ?)', (gender, 'Gender'))
            conn.commit()
            conn.close()
            session['admin_create_gender_status'] = 'success'
            return redirect('/admin-gender')
        except Exception as e:
            session['admin_create_gender_status'] = 'error'
            return redirect('/admin-gender')       
    else:
        return redirect('/')
    
# Admin Del Gender
@app.route('/admin-del-gender', methods=['GET'])
def adminDelGender():
    if 'admin_session' in session:
        try:
            delID = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM detailed_dd_gender WHERE id=?', (delID,))
            conn.commit()
            conn.close()
            session['admin_del_gender_status'] = 'success'
            return redirect('/admin-gender')
        except Exception as e:
            session['admin_del_gender_status'] = 'error'
            return redirect('/admin-gender')       
    else:
        return redirect('/') 



# Admin Citizenship
@app.route('/admin-citizenship')
def adminCitizenship():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detailed_dd_citizenship")
        dataList = cur.fetchall()
        return render_template('admin-citizenship.html', dataList=dataList)
    else:
        return redirect('/')
    
# admin Create Citizenship
@app.route('/admin-create-citizenship', methods=['POST'])
def adminCreateCitizenship():
    if 'admin_session' in session:
        try:
            citizenship = request.form.get('citizenship')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO detailed_dd_citizenship(citizenship, category_list) values(?, ?)', (citizenship, 'Citizenship'))
            conn.commit()
            conn.close()
            session['admin_create_citizenship_status'] = 'success'
            return redirect('/admin-citizenship')
        except Exception as e:
            session['admin_create_citizenship_status'] = 'error'
            return redirect('/admin-citizenship')       
    else:
        return redirect('/')
    
# Admin Del citizenship
@app.route('/admin-del-citizenship', methods=['GET'])
def adminDelCitizenship():
    if 'admin_session' in session:
        try:
            delID = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM detailed_dd_citizenship WHERE id=?', (delID,))
            conn.commit()
            conn.close()
            session['admin_del_citizenship_status'] = 'success'
            return redirect('/admin-citizenship')
        except Exception as e:
            session['admin_del_citizenship_status'] = 'error'
            return redirect('/admin-citizenship')       
    else:
        return redirect('/') 





# Admin Designation
@app.route('/admin-designation')
def adminDesignation():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detailed_dd_designation")
        dataList = cur.fetchall()
        return render_template('admin-designation.html', dataList=dataList)
    else:
        return redirect('/')
    
# admin Create designation
@app.route('/admin-create-designation', methods=['POST'])
def adminCreateDesignation():
    if 'admin_session' in session:
        try:
            designation = request.form.get('designation')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO detailed_dd_designation(designation, category_list) values(?, ?)', (designation, 'Designation'))
            conn.commit()
            conn.close()
            session['admin_create_designation_status'] = 'success'
            return redirect('/admin-designation')
        except Exception as e:
            session['admin_create_designation_status'] = 'error'
            return redirect('/admin-designation')       
    else:
        return redirect('/')
    
    
# Admin Del designation
@app.route('/admin-del-designation', methods=['GET'])
def adminDelDesignation():
    if 'admin_session' in session:
        try:
            delID = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM detailed_dd_designation WHERE id=?', (delID,))
            conn.commit()
            conn.close()
            session['admin_del_designation_status'] = 'success'
            return redirect('/admin-designation')
        except Exception as e:
            session['admin_del_designation_status'] = 'error'
            return redirect('/admin-designation')       
    else:
        return redirect('/') 




# Admin marital Status
@app.route('/admin-marital-status')
def adminMaritalStatus():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detailed_dd_maritail_status")
        dataList = cur.fetchall()
        return render_template('admin-marital-status.html', dataList=dataList)
    else:
        return redirect('/')
    
# admin Create marital-status
@app.route('/admin-create-marital-status', methods=['POST'])
def adminCreateMaritalStatus():
    if 'admin_session' in session:
        try:
            marital_status = request.form.get('marital_status')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO detailed_dd_maritail_status(maritial_status, category_list) values(?, ?)', (marital_status, 'Maritial Status'))
            conn.commit()
            conn.close()
            session['admin_create_marital_status'] = 'success'
            return redirect('/admin-marital-status')
        except Exception as e:
            session['admin_create_marital_status'] = 'error'
            return redirect('/admin-marital-status')       
    else:
        return redirect('/')
    
    
# Admin Del marital-status
@app.route('/admin-del-marital-status', methods=['GET'])
def adminDelMaritalStatus():
    if 'admin_session' in session:
        try:
            delID = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM detailed_dd_maritail_status WHERE id=?', (delID,))
            conn.commit()
            conn.close()
            session['admin_del_marital_status'] = 'success'
            return redirect('/admin-marital-status')
        except Exception as e:
            session['admin_del_marital_status'] = 'error'
            return redirect('/admin-marital-status')       
    else:
        return redirect('/') 



# Admin POINT OF ENTRY
@app.route('/admin-point-of-entry')
def adminPointofEntry():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detailed_dd_poe")
        dataList = cur.fetchall()
        return render_template('admin-point-of-entry.html', dataList=dataList)
    else:
        return redirect('/')
    
# admin Create POINT OF ENTRY
@app.route('/admin-create-point-of-entry', methods=['POST'])
def adminCreatePointofEntry():
    if 'admin_session' in session:
        try:
            poe = request.form.get('poe')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO detailed_dd_poe(poe, category_list) values(?, ?)', (poe, 'Point of Entry'))
            conn.commit()
            conn.close()
            session['admin_create_poe_status'] = 'success'
            return redirect('/admin-point-of-entry')
        except Exception as e:
            session['admin_create_poe_status'] = 'error'
            return redirect('/admin-point-of-entry')       
    else:
        return redirect('/')
    
    
# Admin Del POINT OF ENTRY
@app.route('/admin-del-point-of-entry', methods=['GET'])
def adminDelPointofEntry():
    if 'admin_session' in session:
        try:
            delID = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM detailed_dd_poe WHERE id=?', (delID,))
            conn.commit()
            conn.close()
            session['admin_del_poe_status'] = 'success'
            return redirect('/admin-point-of-entry')
        except Exception as e:
            session['admin_del_poe_status'] = 'error'
            return redirect('/admin-point-of-entry')       
    else:
        return redirect('/') 



# Admin Religion
@app.route('/admin-religion')
def adminReligion():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detailed_dd_religion")
        dataList = cur.fetchall()
        return render_template('admin-religion.html', dataList=dataList)
    else:
        return redirect('/')
    
# admin Create Religion
@app.route('/admin-create-religion', methods=['POST'])
def adminCreateReligion():
    if 'admin_session' in session:
        try:
            religion = request.form.get('religion')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO detailed_dd_religion(religion, category_list) values(?, ?)', (religion, 'Religion'))
            conn.commit()
            conn.close()
            session['admin_create_religion_status'] = 'success'
            return redirect('/admin-religion')
        except Exception as e:
            session['admin_create_religion_status'] = 'error'
            return redirect('/admin-religion')       
    else:
        return redirect('/')
    
    
# Admin Del Religion
@app.route('/admin-del-religion', methods=['GET'])
def adminDelReligion():
    if 'admin_session' in session:
        try:
            delID = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM detailed_dd_religion WHERE id=?', (delID,))
            conn.commit()
            conn.close()
            session['admin_del_religion_status'] = 'success'
            return redirect('/admin-religion')
        except Exception as e:
            session['admin_del_religion_status'] = 'error'
            return redirect('/admin-religion')       
    else:
        return redirect('/') 



# Admin Race
@app.route('/admin-race')
def adminRace():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detailed_dd_race")
        dataList = cur.fetchall()
        return render_template('admin-race.html', dataList=dataList)
    else:
        return redirect('/')
    
# admin Create Race
@app.route('/admin-create-race', methods=['POST'])
def adminCreateRace():
    if 'admin_session' in session:
        try:
            race = request.form.get('race')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO detailed_dd_race(race, category_list) values(?, ?)', (race, 'Race'))
            conn.commit()
            conn.close()
            session['admin_create_race_status'] = 'success'
            return redirect('/admin-race')
        except Exception as e:
            session['admin_create_race_status'] = 'error'
            return redirect('/admin-race')       
    else:
        return redirect('/')
    
    
# Admin Del Race
@app.route('/admin-del-race', methods=['GET'])
def adminDelRace():
    if 'admin_session' in session:
        try:
            delID = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM detailed_dd_race WHERE id=?', (delID,))
            conn.commit()
            conn.close()
            session['admin_del_race_status'] = 'success'
            return redirect('/admin-race')
        except Exception as e:
            session['admin_del_race_status'] = 'error'
            return redirect('/admin-race')       
    else:
        return redirect('/') 
    


# Admin Sector
@app.route('/admin-sector')
def adminSector():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detailed_dd_job_sector")
        dataList = cur.fetchall()
        return render_template('admin-sector.html', dataList=dataList)
    else:
        return redirect('/')
    
# admin Create Sector
@app.route('/admin-create-sector', methods=['POST'])
def adminCreateSector():
    if 'admin_session' in session:
        try:
            sector = request.form.get('sector')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO detailed_dd_job_sector(job_sector, category_list) values(?, ?)', (sector, 'Sector'))
            conn.commit()
            conn.close()
            session['admin_create_sector_status'] = 'success'
            return redirect('/admin-sector')
        except Exception as e:
            session['admin_create_sector_status'] = 'error'
            return redirect('/admin-sector')       
    else:
        return redirect('/')
    
    
# Admin Del Sector
@app.route('/admin-del-sector', methods=['GET'])
def adminDelSector():
    if 'admin_session' in session:
        try:
            delID = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM detailed_dd_job_sector WHERE id=?', (delID,))
            conn.commit()
            conn.close()
            session['admin_del_sector_status'] = 'success'
            return redirect('/admin-sector')
        except Exception as e:
            session['admin_del_sector_status'] = 'error'
            return redirect('/admin-sector')       
    else:
        return redirect('/') 



# Admin Job sub Sector
@app.route('/admin-job-sub-sector')
def adminJobSubSector():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detailed_dd_job_sub_sector")
        dataList = cur.fetchall()

        cur.execute("SELECT job_sector FROM detailed_dd_job_sector")
        jobSectorList = cur.fetchall()

        return render_template('admin-job-sub-sector.html', dataList=dataList, jobSectorList=jobSectorList)
    else:
        return redirect('/')
    
# admin Create Job sub Sector
@app.route('/admin-create-job-sub-sector', methods=['POST'])
def adminCreateJobSubSector():
    if 'admin_session' in session:
        try:
            job_sub_sector = request.form.get('job_sub_sector')
            job_sector = request.form.get('job_sector')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO detailed_dd_job_sub_sector(job_sub_sector, job_sector) values(?, ?)', (job_sub_sector, job_sector))
            conn.commit()
            conn.close()
            session['admin_create_job_sub_sector_status'] = 'success'
            return redirect('/admin-job-sub-sector')
        except Exception as e:
            session['admin_create_job_sub_sector_status'] = 'error'
            return redirect('/admin-job-sub-sector')       
    else:
        return redirect('/')
    
    
# Admin Del Job sub Sector
@app.route('/admin-del-job-sub-sector', methods=['GET'])
def adminDelJobSubSector():
    if 'admin_session' in session:
        try:
            delID = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM detailed_dd_job_sub_sector WHERE id=?', (delID,))
            conn.commit()
            conn.close()
            session['admin_del_job_sub_sector_status'] = 'success'
            return redirect('/admin-job-sub-sector')
        except Exception as e:
            session['admin_del_job_sub_sector_status'] = 'error'
            return redirect('/admin-job-sub-sector')       
    else:
        return redirect('/') 


# Admin Working Status
@app.route('/admin-working-status')
def adminWorkingStatus():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detailed_dd_employement_status")
        dataList = cur.fetchall()
        return render_template('admin-working-status.html', dataList=dataList)
    else:
        return redirect('/')
    
# admin Create Working Status
@app.route('/admin-create-working-status', methods=['POST'])
def adminCreateWorkingStatus():
    if 'admin_session' in session:
        try:
            working_status = request.form.get('working_status')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO detailed_dd_employement_status(employement_status) values(?)', (working_status,))
            conn.commit()
            conn.close()
            session['admin_create_working_status'] = 'success'
            return redirect('/admin-working-status')
        except Exception as e:
            session['admin_create_working_status'] = 'error'
            return redirect('/admin-working-status')       
    else:
        return redirect('/')
    
    
# Admin Del Working Status
@app.route('/admin-del-working-status', methods=['GET'])
def adminDelWorkingStatus():
    if 'admin_session' in session:
        try:
            delID = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM detailed_dd_employement_status WHERE id=?', (delID,))
            conn.commit()
            conn.close()
            session['admin_del_working_status'] = 'success'
            return redirect('/admin-working-status')
        except Exception as e:
            session['admin_del_working_status'] = 'error'
            return redirect('/admin-working-status')       
    else:
        return redirect('/') 



# Admin License category
@app.route('/admin-license-category')
def adminLicenseCategory():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detailed_dd_license_category")
        dataList = cur.fetchall()
        return render_template('admin-license-category.html', dataList=dataList)
    else:
        return redirect('/')
    
# admin Create License category
@app.route('/admin-create-license-category', methods=['POST'])
def adminCreateLicenseCategory():
    if 'admin_session' in session:
        try:
            license = request.form.get('license')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO detailed_dd_license_category(license_list) values(?)', (license,))
            conn.commit()
            conn.close()
            session['admin_create_license_status'] = 'success'
            return redirect('/admin-license-category')
        except Exception as e:
            session['admin_create_license_status'] = 'error'
            return redirect('/admin-license-category')       
    else:
        return redirect('/')
    
    
# Admin Del License category
@app.route('/admin-del-license-category', methods=['GET'])
def adminDelLicenseCategory():
    if 'admin_session' in session:
        try:
            delID = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM detailed_dd_license_category WHERE id=?', (delID,))
            conn.commit()
            conn.close()
            session['admin_del_license_status'] = 'success'
            return redirect('/admin-license-category')
        except Exception as e:
            session['admin_del_license_status'] = 'error'
            return redirect('/admin-license-category')       
    else:
        return redirect('/')


# admin-relationship-to-worker
@app.route('/admin-relationship-to-worker')
def adminRelationshiptoWorker():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detailed_dd_relationship")
        dataList = cur.fetchall()
        return render_template('admin-relationship-to-worker.html', dataList=dataList)
    else:
        return redirect('/')
    
# admin Create relationship-to-worker
@app.route('/admin-create-relationship-to-worker', methods=['POST'])
def adminCreateRelationshiptoWorker():
    if 'admin_session' in session:
        try:
            relationship = request.form.get('relationship')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO detailed_dd_relationship(relationship) values(?)', (relationship,))
            conn.commit()
            conn.close()
            session['admin_create_relationship_status'] = 'success'
            return redirect('/admin-relationship-to-worker')
        except Exception as e:
            session['admin_create_relationship_status'] = 'error'
            return redirect('/admin-relationship-to-worker')       
    else:
        return redirect('/')
    
    
# Admin Del relationship-to-worker
@app.route('/admin-del-relationship-to-worker', methods=['GET'])
def adminDelRelationshiptoworker():
    if 'admin_session' in session:
        try:
            delID = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM detailed_dd_relationship WHERE id=?', (delID,))
            conn.commit()
            conn.close()
            session['admin_del_relationship_status'] = 'success'
            return redirect('/admin-relationship-to-worker')
        except Exception as e:
            session['admin_del_relationship_status'] = 'error'
            return redirect('/admin-relationship-to-worker')       
    else:
        return redirect('/') 
    


# Admin Type of Document
@app.route('/admin-type-of-document')
def adminTypeofDocument():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detailed_dd_type_of_doc")
        dataList = cur.fetchall()
        return render_template('admin-type-of-document.html', dataList=dataList)
    else:
        return redirect('/')
    
# admin Create Type of Document
@app.route('/admin-create-type-of-document', methods=['POST'])
def adminCreateTypeofDocument():
    if 'admin_session' in session:
        try:
            type_of_document = request.form.get('type_of_document')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO detailed_dd_type_of_doc(type_of_doc) values(?)', (type_of_document,))
            conn.commit()
            conn.close()
            session['admin_create_type_of_document_status'] = 'success'
            return redirect('/admin-type-of-document')
        except Exception as e:
            session['admin_create_type_of_document_status'] = 'error'
            return redirect('/admin-type-of-document')       
    else:
        return redirect('/')
    
    
# Admin Del Type of Document
@app.route('/admin-del-type-of-document', methods=['GET'])
def adminDelTypeofDocument():
    if 'admin_session' in session:
        try:
            delID = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM detailed_dd_type_of_doc WHERE id=?', (delID,))
            conn.commit()
            conn.close()
            session['admin_del_type_of_document_status'] = 'success'
            return redirect('/admin-type-of-document')
        except Exception as e:
            session['admin_del_type_of_document_status'] = 'error'
            return redirect('/admin-type-of-document')       
    else:
        return redirect('/') 
    

# Admin Issuing Country
@app.route('/admin-issuing-country')
def adminIssuingCountry():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detailed_dd_country_issued_doc")
        dataList = cur.fetchall()
        return render_template('admin-issuing-country.html', dataList=dataList)
    else:
        return redirect('/')
    
# admin Create Issuing Country
@app.route('/admin-create-issuing-country', methods=['POST'])
def adminCreateIssuingCountry():
    if 'admin_session' in session:
        try:
            issuing_country = request.form.get('issuing_country')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO detailed_dd_country_issued_doc(country_issued_doc) values(?)', (issuing_country,))
            conn.commit()
            conn.close()
            session['admin_create_issuing_country_status'] = 'success'
            return redirect('/admin-issuing-country')
        except Exception as e:
            session['admin_create_issuing_country_status'] = 'error'
            return redirect('/admin-issuing-country')       
    else:
        return redirect('/')
    
    
# Admin Del Issuing Country
@app.route('/admin-del-issuing-country', methods=['GET'])
def adminDelIssuingCountry():
    if 'admin_session' in session:
        try:
            delID = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM detailed_dd_country_issued_doc WHERE id=?', (delID,))
            conn.commit()
            conn.close()
            session['admin_del_issuing_country_status'] = 'success'
            return redirect('/admin-issuing-country')
        except Exception as e:
            session['admin_del_issuing_country_status'] = 'error'
            return redirect('/admin-issuing-country')       
    else:
        return redirect('/')


# Admin status_of_current_document
@app.route('/admin-status-of-current-document')
def adminStatusofCurrentDocument():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detailed_dd_current_status_doc")
        dataList = cur.fetchall()
        return render_template('admin-status-of-current-document.html', dataList=dataList)
    else:
        return redirect('/')
    
# admin Create status_of_current_document
@app.route('/admin-create-status-of-current-document', methods=['POST'])
def adminCreateStatus_of_DurrentDocument():
    if 'admin_session' in session:
        try:
            status_of_current_document = request.form.get('status_of_current_document')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO detailed_dd_current_status_doc(current_status_doc) values(?)', (status_of_current_document,))
            conn.commit()
            conn.close()
            session['admin_create_status_of_current_document_status'] = 'success'
            return redirect('/admin-status-of-current-document')
        except Exception as e:
            session['admin_create_status_of_current_document_status'] = 'error'
            return redirect('/admin-status-of-current-document')       
    else:
        return redirect('/')
    
    
# Admin Del status_of_current_document
@app.route('/admin-del-status-of-current-document', methods=['GET'])
def adminDelstatus_of_current_document():
    if 'admin_session' in session:
        try:
            delID = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM detailed_dd_current_status_doc WHERE id=?', (delID,))
            conn.commit()
            conn.close()
            session['admin_del_status_of_current_document_status'] = 'success'
            return redirect('/admin-status-of-current-document')
        except Exception as e:
            session['admin_del_status_of_current_document_status'] = 'error'
            return redirect('/admin-status-of-current-document')       
    else:
        return redirect('/') 
    


# Admin legal-status
@app.route('/admin-legal-status')
def adminLegalStatus():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detailed_dd_worker_legal_status")
        dataList = cur.fetchall()
        return render_template('admin-legal-status.html', dataList=dataList)
    else:
        return redirect('/')
    
# admin Create legal-status
@app.route('/admin-create-legal-status', methods=['POST'])
def adminCreateLegalStatus():
    if 'admin_session' in session:
        try:
            legal_status = request.form.get('legal_status')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO detailed_dd_worker_legal_status(legal_status) values(?)', (legal_status,))
            conn.commit()
            conn.close()
            session['admin_create_legal_status_status'] = 'success'
            return redirect('/admin-legal-status')
        except Exception as e:
            session['admin_create_legal_status_status'] = 'error'
            return redirect('/admin-legal-status')       
    else:
        return redirect('/')
    
    
# Admin Del legal-status
@app.route('/admin-del-legal-status', methods=['GET'])
def adminDel_legalstatus():
    if 'admin_session' in session:
        try:
            delID = request.args.get('del')
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('DELETE FROM detailed_dd_worker_legal_status WHERE id=?', (delID,))
            conn.commit()
            conn.close()
            session['admin_del_legal_status_status'] = 'success'
            return redirect('/admin-legal-status')
        except Exception as e:
            session['admin_del_legal_status_status'] = 'error'
            return redirect('/admin-legal-status')       
    else:
        return redirect('/') 
    


# Admin Registration Log List
@app.route("/admin-registration-log-list")
def adminRegistrationLogList():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        totalWorker = cur.execute("SELECT id, name, email, worker_registration_prefix FROM users")
        workerD = cur.fetchall()
        totalWorker = len(workerD)
        return render_template('admin-registration-log-list.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')
    

# Admin Registration-log  
@app.route("/admin-registration-log", methods=['GET'])
def adminRegistrationLog():
    if 'admin_session' in session:

        conn = get_db_connection()
        cur = conn.cursor()

        active_user_session = request.args.get('uEm')
        
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
        
        return render_template('admin-registration-log.html', regNumber=regNumber, memberReg=regMemberDay, totalWorker=regWorkerDay, grandTotal=regNumberWeek, totalLegal=totalLegal, totalIllegal=totalIllegal)
    else:
        return redirect('/')
    



# Admin Print QR Code
@app.route("/admin-print-qr-code", methods=['GET', 'POST'])
def adminPrintQrCode():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()

        totalWorker = cur.execute("SELECT id, form_worker_reg_no, worker_detail_name_of_worker, form_status FROM half_form")
        workerD = cur.fetchall()
        totalWorker = len(workerD)
        return render_template('admin-print-qr-code.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')


# Admin Worker Details
@app.route("/admin-worker-details", methods=['GET', 'POST'])
def adminWorkerDetails():
    if 'admin_session' in session:
        workerId = request.args.get('wrkr')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, form_worker_reg_no, worker_detail_name_of_worker, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state form_status FROM half_form where id='"+workerId+"'")
        workerD = cur.fetchall()
        totalWorker = len(workerD)
        return render_template('admin-worker-details.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')


# Admin Print QR
@app.route("/admin-print-qr", methods=['GET', 'POST'])
def adminPrintQr():
    if 'admin_session' in session:
        status = request.args.get('status')
        workerName = request.args.get('name')
        workerRegNum = request.args.get('regN')
        
        if status == 'qr':
            return render_template('admin-print-qr.html', workerName=workerName, workerRegNum=workerRegNum)
        elif status == 'qr-3x3':
            return render_template('admin-print-qr-3x3.html', workerName=workerName, workerRegNum=workerRegNum)
    else:
        return redirect('/')


# Admin Set Malay language
@app.route("/lang-malay")
def adminLangMalay():
    session['langMalay'] = 'malay'
    return redirect('/admin-dash')

# Admin Set Eng Lang
@app.route("/lang-english")
def adminLangEnglish():
    if 'langMalay' in session:
        session.pop('langMalay', None)
        return redirect('/admin-dash')
    else:
        return redirect('/admin-dash')


# Admin Online Server Sync
@app.route("/admin-online-server-sync", methods=['GET', 'POST'])
def adminOnlineServerSync():
    if 'admin_session' in session:
        status = check_internet()
        if status == 'online':
            response = requests.get('http://159.223.32.228:6787/outreach-company-list') 
            if response.status_code == 200:
                data = response.json()
                return render_template('admin-online-server-sync.html', company_ls=data)
            else:
                return "Error fetching data."
        else:
            return render_template('admin-online-server-sync.html')
        #return render_template('admin-online-server-sync.html')
    else:
        return redirect('/')
    

# Admin Online Server Sync
@app.route("/admin-upload-data-to-server", methods=['GET', 'POST'])
def adminUploadDataToServer():
    if 'admin_session' in session:
        status = check_internet()
        return render_template('admin-upload-data-to-server.html')
    else:
        return redirect('/')
    


# Admin  Pull Data
@app.route("/admin-pull-data", methods=['POST'])
def adminPullData():
    if 'admin_session' in session:
        if request.method == 'POST':
            conn = get_db_connection()
            cur = conn.cursor()

            target_date = request.form.get('target_date')
            selected_plantation = request.form.get('selected_plantation')

            allData = {
                'target_date': target_date,
                'selected_plantation': selected_plantation
            }

            response = requests.post('http://159.223.32.228:6787/outreach-sync', data=allData) 
            if response.status_code == 200:
                data = response.json()

                workers = data[16]['workers']
                #print('workers ****** >>', workers)
                for worker in workers:
                    wor_check = worker[3]
                    cur.execute("SELECT id from half_form WHERE form_worker_reg_no=?", (wor_check,))
                    wor_check_len = cur.fetchall()
                    wor_check_len = len(wor_check_len)
                    if wor_check_len == 0:
                        worker = tuple(worker)
                        cur.execute("INSERT INTO half_form(worker_key, form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_name_of_worker, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", worker)

                # Insert Members
                family_members = data[17]['family_members']
                #print('members ****** >>', family_members)
                for member in family_members:
                    fm_check = member[3]
                    cur.execute("SELECT id from family_form WHERE form_family_reg_no=?", (fm_check,))
                    fm_check_len = cur.fetchall()
                    fm_check_len = len(fm_check_len)
                    if fm_check_len == 0:
                        member = tuple(member)
                        cur.execute("INSERT INTO family_form(form_created_by, form_created_date, form_unique_key, form_family_reg_no, family_form_worker_name, family_form_relationship, family_form_name_of_family_member, family_form_family_name, family_form_is_famliy_togther, family_form_family_form_poe, family_form_citizenship, family_form_religion, family_form_marital_status, family_form_gender, family_form_address1, family_form_address2, family_form_address3, family_form_postcode, family_form_city, family_form_state, family_form_contact_no, family_form_race, family_form_place_of_birth, family_form_emp_status, family_form_emp_name, family_form_emp_address, worker_key) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", member)

                # For the worker_docs
                worker_docs = data[18]['worker_docs']
                for wDocs in worker_docs:
                    wDocs = tuple(wDocs)
                    cur.execute("INSERT INTO workers_document(worker_key, document_link, type_of_douments, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document, form_unique_key, worker_reg_no, document_image) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", wDocs)

                # For the worker_docs
                fm_docs = data[19]['fm_docs']
                for fm_Docs in fm_docs:
                    fm_Docs = tuple(fm_Docs)
                    cur.execute("INSERT INTO fm_document(worker_key, document_link, type_of_douments, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document, form_unique_key, fm_reg_no, document_image) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", fm_Docs)


                conn.commit()
                conn.close()
                session['admin_pull_data'] = 'success'
                return redirect('/admin-online-server-sync')
            else:
                return "Error fetching data."
                #return render_template('admin-online-server-sync.html'
        else:
            return redirect('/admin-online-server-sync')
    else:
        return redirect('/')


# Admin Worker Registration List
@app.route("/admin-registration-list", methods=['GET', 'POST'])
def adminRegistrationList():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        totalWorker = cur.execute("SELECT id, form_worker_reg_no, worker_detail_name_of_worker FROM half_form")
        workerD = cur.fetchall()
        totalWorker = len(workerD)
        return render_template('admin-registration-list.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')


# Admin Download Excel File
@app.route('/admin-download-excel-file', methods=['GET'])
def admin_download_log():
    if 'admin_session' in session:
        scheme = request.scheme
        port = request.environ.get('SERVER_PORT')

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
            cur.execute("SELECT form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe,worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, form_position, form_status, form_unique_key FROM half_form")
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
                    xWorkerData = [ f"Document {docsIndex}", xWDocs[3], xWDocs[4], xWDocs[5], xWDocs[6], xWDocs[7], xWDocs[8], xWDocs[9], xWDocs[10], f'{scheme}://{ip_address}:{port}/static/documents/{worker_allData[0]}Docs/{worker_allData[2]}/doc{docsIndex}/uploaded_image.jpg']
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
                    xWorkerFM = [ f"Family Member {fmIndex}", xW_FM[1], xW_FM[2], f"{worker_allData[2]}-{fmIndex}", xW_FM[5], xW_FM[6], xW_FM[7], xW_FM[8], xW_FM[9], xW_FM[10], xW_FM[11], xW_FM[12], xW_FM[13], xW_FM[14], xW_FM[15], xW_FM[16], xW_FM[17], xW_FM[18], xW_FM[19], xW_FM[20], xW_FM[21], xW_FM[22], xW_FM[23], xW_FM[24], xW_FM[25], xW_FM[26], xW_FM[30], xW_FM[31], xW_FM[32], xW_FM[33], xW_FM[34], xW_FM[35], xW_FM[36], xW_FM[37], f'{scheme}://{ip_address}:{port}/static/documents/{worker_allData[0]}Docs/{worker_allData[2]}/familyMember/{xW_FM[4]}/doc1/uploaded_image.jpg', xW_FM[38], xW_FM[39], xW_FM[40], xW_FM[41], xW_FM[42], xW_FM[43], xW_FM[44], xW_FM[45], f'{scheme}://{ip_address}:{port}/static/documents/{worker_allData[0]}Docs/{worker_allData[2]}/familyMember/{xW_FM[4]}/doc2/uploaded_image.jpg']
                    #print(xWorkerFM)
                    log.append(xWorkerFM)
                    fmIndex += 1

                log.append([''])
                # End testing Code

        elif result_single == 'single_id':
            workerId = workerData
            cur.execute("SELECT form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe,worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, form_position, form_status, form_unique_key FROM half_form where id=?", (workerId,))
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
                xWorkerData = [ f"Document {docsIndex}", xWDocs[3], xWDocs[4], xWDocs[5], xWDocs[6], xWDocs[7], xWDocs[8], xWDocs[9], xWDocs[10], f'{scheme}://{ip_address}:{port}/static/documents/{log1[0][0]}Docs/{log1[0][2]}/doc{docsIndex}/uploaded_image.jpg']
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
                xWorkerFM = [ f"Family Member {fmIndex}", xW_FM[1], xW_FM[2], f"{log1[0][2]}-{fmIndex}", xW_FM[5], xW_FM[6], xW_FM[7], xW_FM[8], xW_FM[9], xW_FM[10], xW_FM[11], xW_FM[12], xW_FM[13], xW_FM[14], xW_FM[15], xW_FM[16], xW_FM[17], xW_FM[18], xW_FM[19], xW_FM[20], xW_FM[21], xW_FM[22], xW_FM[23], xW_FM[24], xW_FM[25], xW_FM[26], xW_FM[30], xW_FM[31], xW_FM[32], xW_FM[33], xW_FM[34], xW_FM[35], xW_FM[36], xW_FM[37], f'{scheme}://{ip_address}:{port}/static/documents/{log1[0][0]}Docs/{log1[0][2]}/familyMember/{xW_FM[4]}/doc1/uploaded_image.jpg', xW_FM[38], xW_FM[39], xW_FM[40], xW_FM[41], xW_FM[42], xW_FM[43], xW_FM[44], xW_FM[45], f'{scheme}://{ip_address}:{port}/static/documents/{log1[0][0]}Docs/{log[0][2]}/familyMember/{xW_FM[4]}/doc2/uploaded_image.jpg']
                #print(xWorkerFM)
                log.append(xWorkerFM)
                fmIndex += 1

            log.append([''])
            # End testing Code

        else:
            workerId = json.loads(workerData)
            cur.execute("SELECT form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe,worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, form_position, form_status, form_unique_key FROM half_form WHERE id IN ("+workerId+")")
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
                    xWorkerData = [ f"Document {docsIndex}", xWDocs[3], xWDocs[4], xWDocs[5], xWDocs[6], xWDocs[7], xWDocs[8], xWDocs[9], xWDocs[10], f'{scheme}://{ip_address}:{port}/static/documents/{worker_allData[0]}Docs/{worker_allData[2]}/doc{docsIndex}/uploaded_image.jpg']
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
                    xWorkerFM = [ f"Family Member {fmIndex}", xW_FM[1], xW_FM[2], f"{worker_allData[2]}-{fmIndex}", xW_FM[5], xW_FM[6], xW_FM[7], xW_FM[8], xW_FM[9], xW_FM[10], xW_FM[11], xW_FM[12], xW_FM[13], xW_FM[14], xW_FM[15], xW_FM[16], xW_FM[17], xW_FM[18], xW_FM[19], xW_FM[20], xW_FM[21], xW_FM[22], xW_FM[23], xW_FM[24], xW_FM[25], xW_FM[26], xW_FM[30], xW_FM[31], xW_FM[32], xW_FM[33], xW_FM[34], xW_FM[35], xW_FM[36], xW_FM[37],  f'{scheme}://{ip_address}:{port}/static/documents/{worker_allData[0]}Docs/{worker_allData[2]}/familyMember/{xW_FM[4]}/doc1/uploaded_image.jpg', xW_FM[38], xW_FM[39], xW_FM[40], xW_FM[41], xW_FM[42], xW_FM[43], xW_FM[44], xW_FM[45], f'{scheme}://{ip_address}:{port}/static/documents/{worker_allData[0]}Docs/{worker_allData[2]}/familyMember/{xW_FM[4]}/doc2/uploaded_image.jpg']
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
    


# Admin View Registered Worker
@app.route("/admin-view-registered-worker", methods=['GET', 'POST'])
def adminViewRegisteredWorker():
    if 'admin_session' in session:
        workerId = request.args.get('view-regWor')
        conn = get_db_connection()
        cur = conn.cursor()

        # fetch workers
        cur.execute("SELECT * FROM half_form where id=?", (workerId,))
        workerD = cur.fetchall()
        worker_key = workerD[0][1]


        # get worker reg time
        worker_reg_no = workerD[0][4]
        cur.execute("SELECT reg_time FROM half_form_time WHERE worker_reg_no=?", (worker_reg_no,))
        workerRegNo = cur.fetchall()
        if workerRegNo:
            workerRegTime = workerRegNo[0][0]
        else:
            workerRegTime = 'N/A'

        # fetch worker Docs
        cur.execute("SELECT * FROM workers_document where worker_key=?", (worker_key,))
        workerDocs = cur.fetchall()

        # fetch worker Family members
        cur.execute("SELECT * FROM family_form where worker_key=?", (worker_key,))
        workerFM = cur.fetchall()

        # Worker Document Path
        userRoot = workerD[0][2]
        docsPath = f"./static/documents/{userRoot}Docs/{worker_reg_no}/"
        
        return render_template('admin-view-registered-worker.html', docsPath=docsPath, workerRegTime=workerRegTime, workerList=workerD, workerDocs=workerDocs, workerFM=workerFM)
    else:
        return redirect('/')


# Admin Worker > view-family-member
@app.route("/admin-view-family-member", methods=['GET', 'POST'])
def adminViewFamilyMember():
    if 'admin_session' in session:
        fmId = request.args.get('fm')
        fmN = request.args.get('fmN')

        conn = get_db_connection()
        cur = conn.cursor()

        # fetch workers
        cur.execute("SELECT * FROM family_form where id=?", (fmId,))
        fmData = cur.fetchall()

        # get Family member Path details
        userRoot = fmData[0][1]
        fmRegNo =  fmData[0][4]
        formUniqueKey = fmData[0][3]
        cur.execute("SELECT id, form_worker_reg_no FROM half_form WHERE form_unique_key=?", (formUniqueKey,))
        workerRegN = cur.fetchall()
        if workerRegN:
            workerId = workerRegN[0][0]
            workerRegNo = workerRegN[0][1]
        docsPath = f"./static/documents/{userRoot}Docs/{workerRegNo}/familyMembers/{fmRegNo}/"
        
        return render_template('admin-view-family-member.html', wori=workerId, worReN=workerRegNo, fmN=fmN, docsPath=docsPath, fmData=fmData)
    else:
        return redirect('/')


# Admin Edit Registered Worker
@app.route("/admin-edit-registered-worker", methods=['GET', 'POST'])
def adminEditRegisteredWorker():
    if 'admin_session' in session:
        workerId = request.args.get('view-regWor')
        conn = get_db_connection()
        cur = conn.cursor()

        # fetch workers
        cur.execute("SELECT * FROM half_form where id=?", (workerId,))
        workerD = cur.fetchall()
        worker_key = workerD[0][1]

        # fetch worker Docs
        cur.execute("SELECT * FROM workers_document where worker_key=?", (worker_key,))
        workerDocs = cur.fetchall()

        # fetch worker Family members
        cur.execute("SELECT * FROM family_form where worker_key=?", (worker_key,))
        workerFM = cur.fetchall()
        
        return render_template('admin-edit-registered-worker.html', workerList = workerD, workerDocs=workerDocs, workerFM=workerFM)
    else:
        return redirect('/')
    
# Admin Update Registered Worker
@app.route("/admin-update-registered-worker", methods=['POST'])
def adminUpdateRegisteredWorker():
    if 'admin_session' in session:
        if request.method == 'POST':
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

            session['admin_registration_list_update'] = 'success'
            return redirect('/admin-registration-list')
        else:
            response = {
                'status': 'error',
                'msg': 'method error'
            }
            return jsonify(response)
    else:
        return redirect('/')



# Admin Update Registered Worker Docs
@app.route("/admin-update-worker-docs", methods=['POST'])
def adminUpdateWorkerDocs():
    if 'admin_session' in session:
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
            session['admin_registration_list_update'] = 'success'
            return redirect('/admin-registration-list')   
        else:
            response = {
                'status': 'error',
                'msg': 'method error'
            }
            return jsonify(response)
    else:
        return redirect('/')


# Admin edit-family-member
@app.route("/admin-edit-family-member", methods=['GET', 'POST'])
def adminEditFamilyMember():
    if 'admin_session' in session:
        fmId = request.args.get('fm')
        conn = get_db_connection()
        cur = conn.cursor()

        # fetch workers
        cur.execute("SELECT * FROM family_form where id=?", (fmId,))
        fmData = cur.fetchall()
        return render_template('admin-edit-family-member.html', fmData=fmData)
    else:
        return redirect('/')
    

# Admin Update Family Member
@app.route("/admin-update-family-member", methods=['POST'])
def adminUpdateFamilyMember():
    if 'admin_session' in session:
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
            session['admin_registration_list_update'] = 'success'
            return redirect('/admin-registration-list')   
        else:
            response = {
                'status': 'error',
                'msg': 'method error'
            }
            return jsonify(response)
    else:
        return redirect('/')
    
# Admin delete workers and their family members
@app.route("/admin-del-registered-worker", methods=['GET'])
def adminDelRegisteredWorker():
    if 'admin_session' in session:
        worker_id = request.args.get('del')
        conn = get_db_connection()
        cur = conn.cursor()

        # fetch workers
        cur.execute("SELECT worker_key FROM half_form where id=?", (worker_id,))
        workerKey = cur.fetchall()
        worker_key = workerKey[0][0]

        # del worker
        cur.execute("DELETE FROM half_form WHERE id=?", (worker_id,))
        # del worker documents
        cur.execute("DELETE FROM workers_document where id=?", (worker_key,))
        # del worker family members
        cur.execute("DELETE FROM family_form where id=?", (worker_key,))
        
        conn.commit()
        conn.close()
        session['admin_registration_list_delete'] = 'success'
        return redirect('/admin-registration-list')
    else:
        return redirect('/')


# Admin Set Dermalog IP
@app.route("/admin-set-dermalog-ip", methods=['GET', 'POST'])
def adminSetDermaLogIP():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT dermalog_ip FROM dermalog_ip WHERE id=1")
        new_dermalog_ip = cur.fetchone()[0]
        
        return render_template('admin-set-dermalog-ip.html', dermalog_ip=new_dermalog_ip)
    else:
        return redirect('/')

# Admin Set Dermalog IP
@app.route("/admin-insert-set-dermalog-ip", methods=['POST'])
def adminInsertSetDermaLogIP():
    if 'admin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        
        dermalog_ip = request.form.get('dermalog_ip')
        creator = session.get('admin_session')
        date_now = datetime.now().strftime('%d/%m/%Y')
        time_now = datetime.now().strftime('%H:%M:%S')
        # Update
        cur.execute("UPDATE dermalog_ip SET dermalog_ip=?, creator=?, updated_date=?, updated_time=? where id=?", (dermalog_ip, creator, date_now, time_now, 1))
        cur.execute("SELECT dermalog_ip FROM dermalog_ip WHERE id=1")
        new_dermalog_ip = cur.fetchone()[0]
        conn.commit()
        conn.close()
        
        return render_template('admin-set-dermalog-ip.html', dermalog_ip=new_dermalog_ip)
    else:
        return redirect('/')


# Admin Logout
@app.route("/admin-logout")
def adminLogout():
    if 'admin_session' in session:
        session.clear()
        return redirect('/')
    else:
        return redirect('/')



# ---------------------
# * End Admin Section *
# ---------------------




# ---------------------------
# * Start - Sub Admin Section *
# ---------------------------

# subAdmin dash
@app.route('/sub-admin-dash')
def subAdminDash():
    if 'subAdmin_session' in session:
        # DB
        conn = get_db_connection()
        cur = conn.cursor()
        profile = cur.execute("SELECT * FROM profile")
        return render_template('sub-admin-dash.html')
    
    else:
        return redirect('/')
    
# subAdmin profile
@app.route('/sub-admin-profile')
def subAdminProfile():
    if 'subAdmin_session' in session:
        active_subAdmin = session.get('subAdmin_session')
        # DB
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM sub_admin where email=?", (active_subAdmin,))
        profile = cur.fetchall()
        return render_template('sub-admin-profile.html', profileData=profile)
    
    else:
        return redirect('/')
    

# subAdmin Update profile
@app.route('/sub-admin-update-profile', methods=['POST'])
def subAdminUpdateProfile():
    if 'subAdmin_session' in session:
        try:
            active_subAdmin = session.get('subAdmin_session')
            x_path = 'static/img/subAdmin/'
            
            profile = request.files['profile']
            userID = request.form.get('userID')
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')

            
            img_date = datetime.now().strftime('%d%m%Y')
            img_rand = random.randrange(100000, 999999)

            unique_img = img_date + str(img_rand)

            profile_path = x_path + unique_img +'_'+profile.filename
            #print(profile_path)

            # DB
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("UPDATE sub_admin SET name=?, email=?, password=?, profile_path=? where id=?", (name, email, password, profile_path, userID))
            conn.commit()
            conn.close()
            
            profile.save(profile_path)

            session['sub_admin_update_status'] = 'success'
            return redirect('/sub-admin-profile')
        except Exception as e:
                session['sub_admin_update_status'] = 'error'
                return redirect('/sub-admin-profile')   
    else:
        return redirect('/')


# subAdmin View Exe Users
@app.route('/sub-admin-view-exe-users')
def subAdminViewExeUsers():
    if 'subAdmin_session' in session:
        try:
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            users = cur.execute('SELECT id, name, email, password, worker_registration_prefix FROM users')
            users = cur.fetchall()
            totalUsers = len(users)
            userList = users
            
            conn.commit()
            conn.close()
            return render_template('sub-admin-view-exe-users.html', totalUsers=totalUsers, userList=userList)
        except Exception as e:
            return redirect('/sub-admin-dash')       
    else:
        return redirect('/') 

# subAdmin Edit Exe Users
@app.route('/sub-admin-edit-exe-users', methods=['GET'])
def subAdminEditExeUsers():
    if 'subAdmin_session' in session:
        try:
            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            userID = request.args.get('usI')

            users = cur.execute('SELECT id, name, email, password, worker_registration_prefix FROM users WHERE id=?', (userID,))
            users = cur.fetchall()
            userList = users
            
            conn.commit()
            conn.close()
            return render_template('sub-admin-edit-exe-users.html', userList=userList)
        except Exception as e:
            return redirect('/sub-admin-dash')       
    else:
        return redirect('/')
    
# subAdmin Update Exe Users
@app.route('/sub-admin-update-exe-users', methods=['POST'])
def subAdminUpdateExeUsers():
    if 'subAdmin_session' in session:
        try:
            userID = request.form.get('userID')
            user_password = request.form.get('user_password')

            # DB
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('UPDATE users SET password=? WHERE id=?', (user_password, userID))
            conn.commit()
            conn.close()
            
            session['sub_admin_update_exe_users_status'] = 'success'
            return redirect('/sub-admin-view-exe-users')
        except Exception as e:
            session['sub_admin_update_exe_users_status'] = 'error'
            return redirect('/sub-admin-view-exe-users')       
    else:
        return redirect('/') 




# subAdmin Registration Log List
@app.route("/sub-admin-registration-log-list")
def subAdminRegistrationLogList():
    if 'subAdmin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        totalWorker = cur.execute("SELECT id, name, email, worker_registration_prefix FROM users")
        workerD = cur.fetchall()
        totalWorker = len(workerD)
        return render_template('sub-admin-registration-log-list.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')
    

# subAdmin Registration-log  
@app.route("/sub-admin-registration-log", methods=['GET'])
def subAdminRegistrationLog():
    if 'subAdmin_session' in session:

        conn = get_db_connection()
        cur = conn.cursor()

        active_user_session = request.args.get('uEm')
        
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
        
        return render_template('sub-admin-registration-log.html', regNumber=regNumber, memberReg=regMemberDay, totalWorker=regWorkerDay, grandTotal=regNumberWeek, totalLegal=totalLegal, totalIllegal=totalIllegal)
    else:
        return redirect('/')
    


# subAdmin Print QR Code
@app.route("/sub-admin-print-qr-code", methods=['GET', 'POST'])
def subAdminPrintQrCode():
    if 'subAdmin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()

        totalWorker = cur.execute("SELECT id, form_worker_reg_no, worker_detail_name_of_worker, form_status FROM half_form")
        workerD = cur.fetchall()
        totalWorker = len(workerD)
        return render_template('sub-admin-print-qr-code.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')


# subAdmin Worker Details
@app.route("/sub-admin-worker-details", methods=['GET', 'POST'])
def subAdminWorkerDetails():
    if 'subAdmin_session' in session:
        workerId = request.args.get('wrkr')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, form_worker_reg_no, worker_detail_name_of_worker, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state form_status FROM half_form where id='"+workerId+"'")
        workerD = cur.fetchall()
        totalWorker = len(workerD)
        return render_template('sub-admin-worker-details.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')


# subAdmin Print QR
@app.route("/sub-admin-print-qr", methods=['GET', 'POST'])
def subAdminPrintQr():
    if 'subAdmin_session' in session:
        status = request.args.get('status')
        workerName = request.args.get('name')
        workerRegNum = request.args.get('regN')
        
        if status == 'qr':
            return render_template('sub-admin-print-qr.html', workerName=workerName, workerRegNum=workerRegNum)
        elif status == 'qr-3x3':
            return render_template('sub-admin-print-qr-3x3.html', workerName=workerName, workerRegNum=workerRegNum)
    else:
        return redirect('/')


# subAdmin Set Malay language
@app.route("/sub-admin-lang-malay")
def subAdminLangMalay():
    session['langMalay'] = 'malay'
    return redirect('/sub-admin-dash')

# subAdmin Set Eng Lang
@app.route("/sub-admin-lang-english")
def subAdminLangEnglish():
    if 'langMalay' in session:
        session.pop('langMalay', None)
        return redirect('/sub-admin-dash')
    else:
        return redirect('/sub-admin-dash')



# subAdmin Worker Registration List
@app.route("/sub-admin-registration-list", methods=['GET', 'POST'])
def subAdminRegistrationList():
    if 'subAdmin_session' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        totalWorker = cur.execute("SELECT id, form_worker_reg_no, worker_detail_name_of_worker FROM half_form")
        workerD = cur.fetchall()
        totalWorker = len(workerD)
        return render_template('sub-admin-registration-list.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')


# subAdmin Download Excel File
@app.route('/sub-admin-download-excel-file', methods=['GET'])
def subAdmin_download_log():
    if 'subAdmin_session' in session:
        scheme = request.scheme
        port = request.environ.get('SERVER_PORT')

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
            cur.execute("SELECT form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe,worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, form_position, form_status, form_unique_key FROM half_form")
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
                    xWorkerData = [ f"Document {docsIndex}", xWDocs[3], xWDocs[4], xWDocs[5], xWDocs[6], xWDocs[7], xWDocs[8], xWDocs[9], xWDocs[10], f'{scheme}://{ip_address}:{port}/static/documents/{worker_allData[0]}Docs/{worker_allData[2]}/doc{docsIndex}/uploaded_image.jpg']
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
                    xWorkerFM = [ f"Family Member {fmIndex}", xW_FM[1], xW_FM[2], f"{worker_allData[2]}-{fmIndex}", xW_FM[5], xW_FM[6], xW_FM[7], xW_FM[8], xW_FM[9], xW_FM[10], xW_FM[11], xW_FM[12], xW_FM[13], xW_FM[14], xW_FM[15], xW_FM[16], xW_FM[17], xW_FM[18], xW_FM[19], xW_FM[20], xW_FM[21], xW_FM[22], xW_FM[23], xW_FM[24], xW_FM[25], xW_FM[26], xW_FM[30], xW_FM[31], xW_FM[32], xW_FM[33], xW_FM[34], xW_FM[35], xW_FM[36], xW_FM[37], f'{scheme}://{ip_address}:{port}/static/documents/{worker_allData[0]}Docs/{worker_allData[2]}/familyMember/{xW_FM[4]}/doc1/uploaded_image.jpg', xW_FM[38], xW_FM[39], xW_FM[40], xW_FM[41], xW_FM[42], xW_FM[43], xW_FM[44], xW_FM[45], f'{scheme}://{ip_address}:{port}/static/documents/{worker_allData[0]}Docs/{worker_allData[2]}/familyMember/{xW_FM[4]}/doc2/uploaded_image.jpg']
                    #print(xWorkerFM)
                    log.append(xWorkerFM)
                    fmIndex += 1

                log.append([''])
                # End testing Code

        elif result_single == 'single_id':
            workerId = workerData
            cur.execute("SELECT form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe,worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, form_position, form_status, form_unique_key FROM half_form where id=?", (workerId,))
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
                xWorkerData = [ f"Document {docsIndex}", xWDocs[3], xWDocs[4], xWDocs[5], xWDocs[6], xWDocs[7], xWDocs[8], xWDocs[9], xWDocs[10], f'{scheme}://{ip_address}:{port}/static/documents/{log1[0][0]}Docs/{log1[0][2]}/doc{docsIndex}/uploaded_image.jpg']
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
                xWorkerFM = [ f"Family Member {fmIndex}", xW_FM[1], xW_FM[2], f"{log1[0][2]}-{fmIndex}", xW_FM[5], xW_FM[6], xW_FM[7], xW_FM[8], xW_FM[9], xW_FM[10], xW_FM[11], xW_FM[12], xW_FM[13], xW_FM[14], xW_FM[15], xW_FM[16], xW_FM[17], xW_FM[18], xW_FM[19], xW_FM[20], xW_FM[21], xW_FM[22], xW_FM[23], xW_FM[24], xW_FM[25], xW_FM[26], xW_FM[30], xW_FM[31], xW_FM[32], xW_FM[33], xW_FM[34], xW_FM[35], xW_FM[36], xW_FM[37], f'{scheme}://{ip_address}:{port}/static/documents/{log1[0][0]}Docs/{log1[0][2]}/familyMember/{xW_FM[4]}/doc1/uploaded_image.jpg', xW_FM[38], xW_FM[39], xW_FM[40], xW_FM[41], xW_FM[42], xW_FM[43], xW_FM[44], xW_FM[45], f'{scheme}://{ip_address}:{port}/static/documents/{log1[0][0]}Docs/{log[0][2]}/familyMember/{xW_FM[4]}/doc2/uploaded_image.jpg']
                #print(xWorkerFM)
                log.append(xWorkerFM)
                fmIndex += 1

            log.append([''])
            # End testing Code

        else:
            workerId = json.loads(workerData)
            cur.execute("SELECT form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe,worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, form_position, form_status, form_unique_key FROM half_form WHERE id IN ("+workerId+")")
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
                    xWorkerData = [ f"Document {docsIndex}", xWDocs[3], xWDocs[4], xWDocs[5], xWDocs[6], xWDocs[7], xWDocs[8], xWDocs[9], xWDocs[10], f'{scheme}://{ip_address}:{port}/static/documents/{worker_allData[0]}Docs/{worker_allData[2]}/doc{docsIndex}/uploaded_image.jpg']
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
                    xWorkerFM = [ f"Family Member {fmIndex}", xW_FM[1], xW_FM[2], f"{worker_allData[2]}-{fmIndex}", xW_FM[5], xW_FM[6], xW_FM[7], xW_FM[8], xW_FM[9], xW_FM[10], xW_FM[11], xW_FM[12], xW_FM[13], xW_FM[14], xW_FM[15], xW_FM[16], xW_FM[17], xW_FM[18], xW_FM[19], xW_FM[20], xW_FM[21], xW_FM[22], xW_FM[23], xW_FM[24], xW_FM[25], xW_FM[26], xW_FM[30], xW_FM[31], xW_FM[32], xW_FM[33], xW_FM[34], xW_FM[35], xW_FM[36], xW_FM[37],  f'{scheme}://{ip_address}:{port}/static/documents/{worker_allData[0]}Docs/{worker_allData[2]}/familyMember/{xW_FM[4]}/doc1/uploaded_image.jpg', xW_FM[38], xW_FM[39], xW_FM[40], xW_FM[41], xW_FM[42], xW_FM[43], xW_FM[44], xW_FM[45], f'{scheme}://{ip_address}:{port}/static/documents/{worker_allData[0]}Docs/{worker_allData[2]}/familyMember/{xW_FM[4]}/doc2/uploaded_image.jpg']
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
    


# subAdmin View Registered Worker
@app.route("/sub-admin-view-registered-worker", methods=['GET', 'POST'])
def subAdminViewRegisteredWorker():
    if 'subAdmin_session' in session:
        workerId = request.args.get('view-regWor')
        conn = get_db_connection()
        cur = conn.cursor()

        # fetch workers
        cur.execute("SELECT * FROM half_form where id=?", (workerId,))
        workerD = cur.fetchall()
        worker_key = workerD[0][1]

        # get worker reg time
        worker_reg_no = workerD[0][4]
        cur.execute("SELECT reg_time FROM half_form_time WHERE worker_reg_no=?", (worker_reg_no,))
        workerRegNo = cur.fetchall()
        if workerRegNo:
            workerRegTime = workerRegNo[0][0]
        else:
            workerRegTime = 'N/A'

        # fetch worker Docs
        cur.execute("SELECT * FROM workers_document where worker_key=?", (worker_key,))
        workerDocs = cur.fetchall()

        # fetch worker Family members
        cur.execute("SELECT * FROM family_form where worker_key=?", (worker_key,))
        workerFM = cur.fetchall()

        # Worker Document Path
        userRoot = workerD[0][2]
        docsPath = f"./static/documents/{userRoot}Docs/{worker_reg_no}/"

        
        return render_template('sub-admin-view-registered-worker.html', docsPath=docsPath, workerRegTime=workerRegTime, workerList=workerD, workerDocs=workerDocs, workerFM=workerFM)
    else:
        return redirect('/')


# subAdmin Worker > view-family-member
@app.route("/sub-admin-view-family-member", methods=['GET', 'POST'])
def subAdminViewFamilyMember():
    if 'subAdmin_session' in session:
        fmId = request.args.get('fm')
        fmN = request.args.get('fmN')

        conn = get_db_connection()
        cur = conn.cursor()

        # fetch workers
        cur.execute("SELECT * FROM family_form where id=?", (fmId,))
        fmData = cur.fetchall()

        # get Family member Path details
        userRoot = fmData[0][1]
        fmRegNo =  fmData[0][4]
        formUniqueKey = fmData[0][3]
        cur.execute("SELECT id, form_worker_reg_no FROM half_form WHERE form_unique_key=?", (formUniqueKey,))
        workerRegN = cur.fetchall()
        if workerRegN:
            workerId = workerRegN[0][0]
            workerRegNo = workerRegN[0][1]
        docsPath = f"./static/documents/{userRoot}Docs/{workerRegNo}/familyMembers/{fmRegNo}/"
        
        
        return render_template('sub-admin-view-family-member.html', wori=workerId, worReN=workerRegNo, fmN=fmN, docsPath=docsPath, fmData=fmData)
    else:
        return redirect('/')



# subAdmin Logout
@app.route("/sub-admin-logout")
def subAdminLogout():
    if 'subAdmin_session' in session:
        session.clear()
        return redirect('/')
    else:
        return redirect('/')

# ---------------------------
# * End - Sub Admin Section *
# ---------------------------




# ----------------------
# * Start User Section *
# ----------------------

# Get Company Name in Sort form
def company_first_letters(input_string):
    words = input_string.split()
    first_letters = [word[0] for word in words]
    return ''.join(first_letters)


# Add Worker
@app.route("/add-worker")
def addWorker():
    if 'user_session' in session:
        active_user_session = session.get('user_session')
        
        serverPort = request.environ.get('SERVER_PORT')

        userRoot = active_user_session + 'Docs'
        
        # check profile data
        conn = get_db_connection()
        cur = conn.cursor()

        
        profile = cur.execute("SELECT * FROM profile WHERE aps_email=?", (active_user_session,))
        profile = profile.fetchall()
        profileLen = len(profile)
        if profileLen == 0:
            return render_template('add-worker.html', profileC=profileLen)

        
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
        
        # Find The lask Family member
        cur.execute('SELECT MAX(id) FROM family_form')
        fm_last_key = cur.fetchone()[0]
        if fm_last_key == None:
            new_fMemberID = 0
        else:
            new_fMemberID = fm_last_key

        fmPrefix = 'FM'
        fm_registrationPrefix = fmPrefix + currentYear + companyShortName.upper()
        
        # End Find The lask Family member
        '''

        # -----------------------
        # Find Last Key of Worker
        # -----------------------
        # check incomplete Status  MAX(tracking_id),
        cur.execute('SELECT worker_reg_no FROM reg_num_tracking WHERE user=? AND creator=? AND status=?', (active_user_session, active_user_session, 'incomplete'))
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

                fMember_regNum_1 = track_fm[0][0]
                fMember_regNum_2 = track_fm[1][0]
                fMember_regNum_3 = track_fm[2][0]
                fMember_regNum_4 = track_fm[3][0]
                fMember_regNum_5 = track_fm[4][0]
                fMember_regNum_6 = track_fm[5][0]
                fMember_regNum_7 = track_fm[6][0]
                fMember_regNum_8 = track_fm[7][0]
                fMember_regNum_9 = track_fm[8][0]
                fMember_regNum_10 = track_fm[9][0]
                
                
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
                    cur.execute('INSERT INTO reg_num_tracking(tracking_id, user, creator, worker_reg_no, status, creation_date, creation_time) VALUES(?, ?, ?, ?, ?, ?, ?)', (workerSerialNumber, active_user_session, active_user_session, workerRegistrationNumber, 'incomplete', creation_date, creation_time))

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
                        cur.execute('INSERT INTO fm_reg_num_tracking(tracking_id, user, creator, worker_reg_no, fm_reg_no, status, creation_date, creation_time) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (fmSerialNumber, active_user_session, active_user_session, workerRegistrationNumber, fmRegistrationNumber,'incomplete', creation_date, creation_time))

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
                    cur.execute('INSERT INTO reg_num_tracking(tracking_id, user, creator, worker_reg_no, status, creation_date, creation_time) VALUES(?, ?, ?, ?, ?, ?, ?)', (workerSerialNumber, active_user_session, active_user_session, workerRegistrationNumber, 'incomplete', creation_date, creation_time))
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
                        cur.execute('INSERT INTO fm_reg_num_tracking(tracking_id, user, creator, worker_reg_no, fm_reg_no, status, creation_date, creation_time) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (fmSerialNumber, active_user_session, active_user_session, workerRegistrationNumber, fmRegistrationNumber,'incomplete', creation_date, creation_time))

                    # Create the Folder For Worker
                    userRoot = active_user_session + 'Docs'
                    folderCreator(userRoot, workerRegistrationNumber, 'legal', fm_registrationPrefix , new_fm_last_key, 10)

                    # Now return FMamily members
                    cur.execute('SELECT fm_reg_no FROM fm_reg_num_tracking WHERE user=? AND worker_reg_no=?', (active_user_session, workerRegistrationNumber))
                    track_fm = cur.fetchall()
                    track_fm_len = len(track_fm)
                    #print('FM Track -> ', track_fm, track_fm_len)
        
        

        
            
        

        # ------------------------------
        # End Worker Registration Number
        # ------------------------------
        
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

        return render_template('add-worker.html', fMember_regNum_1=fMember_regNum_1, fMember_regNum_2=fMember_regNum_2, fMember_regNum_3=fMember_regNum_3, fMember_regNum_4=fMember_regNum_4, fMember_regNum_5=fMember_regNum_5, fMember_regNum_6=fMember_regNum_6, fMember_regNum_7=fMember_regNum_7, fMember_regNum_8=fMember_regNum_8, fMember_regNum_9=fMember_regNum_9, fMember_regNum_10=fMember_regNum_10,  aps_contact_person=aps_contact_person, legalStatusList=legalStatusList, userRoot=userRoot, ip_address=ip_address, serverPort=serverPort, branch_address1=branch_address1, branch_address2=branch_address2, branch_address3=branch_address3, workerRegistrationNumber=workerRegistrationNumber, fm_registrationPrefix=fm_registrationPrefix, filename=gallery_images, filename2=gallery_images2, filename3=gallery_images3, filename4=gallery_images4, filename5=gallery_images5, filename6=gallery_images6, filename7=gallery_images7, filename8=gallery_images8, citizenshipList=citizenship, maritialList=maritial, poeList=poe, genderList=gender, religionList=religion, raceList=race, relationshipList=relationship, jobSectorList=job_sector, cityList=city, stateList=state, issuingCountryList=issuingCountry, docStatusList=docStatus, curDocStatusList=curDocStatus, typeOfDocList=typeOfDoc, employement_statusList=employement_status, jobStatusSponsorList = job_status_sponsor)
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
'''
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
    
                #print('All Data: ->', data)
                formStatus = data.get('status')
                workerD = data.get('workerData')
                docD = data.get('docData')
                fmData = data.get('familyMemberData')
                fmDocs = data.get('familyMemberDocs')

                
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

                elif formStatus == 'workerWithFamily':
                    #print(formStatus)
                    # Worker & Family
                
                    # JSON to Obj
                    workerData = json.loads(workerD)
                    docData = json.loads(docD)
                    familyMemberData = json.loads(fmData)
                    fm_doc_data = json.loads(fmDocs)
                    
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
               
                #print('success')
                return jsonify({'status': 'success'})
            
            except Exception as e:    
                print('Insert Worker Error: ', str(e))
                return jsonify({'status': 'failure'})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid request method'})
    else:
        return jsonify({'status': 'error', 'message': 'User not logged in'})
    
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
        active_user_session = session.get('user_session')
        conn = get_db_connection()
        cur = conn.cursor()
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
        
        cur.execute("SELECT name, email, password, worker_registration_prefix FROM users where email=?", (active_user_session,))
        users = cur.fetchall()
        usersLen = len(users)
        if usersLen == 1:
            name = users[0][0]
            email = users[0][1]
            password = users[0][2]
            worker_registration_prefix = users[0][3]
       
        return render_template('profile.html', name=name, password=password, worker_registration_prefix=worker_registration_prefix, email=email, your_email=active_user_session, licenseCategoryList=licenseCategory, cityList=city, stateList=state, sectorList=sector, designationList=designation)
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
            '''
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
            
            
            # Worker BioData
            cur.execute("SELECT * FROM worker_biodata WHERE worker_reg_no=?", (worker_reg_no,))
            workerBiodata = cur.fetchall()
            '''
            # fetch workers
            cur.execute("SELECT * FROM half_form WHERE id=?", (workerId,))
            workerD = cur.fetchall()
            form_unique_key = workerD[0][33]

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
            
            
            # Worker BioData
            cur.execute("SELECT * FROM worker_biodata WHERE worker_reg_no=?", (worker_reg_no,))
            workerBiodata = cur.fetchall()
            
            
            return render_template('view-registered-worker1.html', workerBiodata=workerBiodata, docsPath=docsPath, workerRegTime=workerRegTime, workerList=workerD, workerDocs=workerDocs, workerFM=workerFM)
        except Exception as e:
            print(e)
            return redirect('/my-registration-list')
    else:
        return redirect('/')

# Worker view-family-member
@app.route("/view-family-member1", methods=['GET', 'POST'])
def viewFamilyMember1():
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
    
            # Worker BioData
            cur.execute("SELECT * FROM fm_biodata WHERE fm_reg_no=?", (fmRegNo,))
            fmBiodata = cur.fetchall()

            return render_template('view-family-member1.html', fmBiodata=fmBiodata, wori=workerId, worReN=workerRegNo, fmN=fmN, docsPath=docsPath, fmData=fmData)
        except Exception as e:
            return redirect('/my-registration-list')
    else:
        return redirect('/')




    
# ---------------------# RESTful API > Testing # ---------------------
# Define the SIFW API endpoints and your credentials
def dermalop_ip_address():
    conn = get_db_connection()
    cur = conn.cursor()
    # fetch IP
    cur.execute("SELECT dermalog_ip FROM dermalog_ip where id=1")
    dermalog_ip = cur.fetchone()[0]
    return dermalog_ip


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
        return jsonify({"error": str(e)}), 500
    
    
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





# Edit Registered Worker
@app.route("/edit-registered-worker1", methods=['GET', 'POST'])
def editRegisteredWorker1():
    if 'user_session' in session:
        active_user_session = session.get('user_session')

        try:
            workerId = request.args.get('view-regWor')
            conn = get_db_connection()
            cur = conn.cursor()

            # fetch workers
            cur.execute("SELECT * FROM half_form where id=?", (workerId,))
            workerD = cur.fetchall()
            form_unique_key = workerD[0][33]
            
            worker_reg_no = workerD[0][4]
            # Worker Document Path
            docsPath = f"./static/documents/{active_user_session}Docs/{worker_reg_no}/"

            # fetch worker Docs
            cur.execute("SELECT * FROM workers_document WHERE form_unique_key=?", (form_unique_key,))
            workerDocs = cur.fetchall()

            # fetch worker Family members
            cur.execute("SELECT * FROM family_form where form_unique_key=?", (form_unique_key,))
            workerFM = cur.fetchall()
            return render_template('edit-registered-worker1.html', worker_reg_no=worker_reg_no, view_regWor=workerId, docsPath=docsPath, workerList = workerD, workerDocs=workerDocs, workerFM=workerFM)
        except Exception as e:
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

            session['registration_list_update1'] = 'success'
            return redirect('/my-registration-list')
        else:
            response = {
                'status': 'error',
                'msg': 'method error'
            }
            return jsonify(response)
    else:
        return redirect('/')



# Update Registered Worker Docs
@app.route("/update-worker-docs1", methods=['POST'])
def updateWorkerDocs1():
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
            session['registration_list_update1'] = 'success'
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
                workerRegNo = workerRegN[0][1]
            
            docsPath = f"./static/documents/{active_user_session}Docs/{workerRegNo}/familyMembers/{fmRegNo}/"
            
            
            return render_template('edit-family-member1.html', fm=fmId,  wori=workerId, worReN=workerRegNo, docsPath=docsPath, fmData=fmData)
        except Exception as e:
            return redirect('/my-registration-list')
    else:
        return redirect('/')
    

# Update Family Member
@app.route("/update-family-member1", methods=['POST'])
def updateFamilyMember1():
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
            session['registration_list_update1'] = 'success'
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
    app.run(host=ip_address, port=6787)

'''

def start_webview():
    # Create a webview window
    webview.create_window("Swims App", f"http://{ip_address}:9689/", js_api=True)
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