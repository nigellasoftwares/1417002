from flask import Flask, render_template, Response, request, redirect, session, jsonify, json, send_file, send_from_directory
#from flask_cors import CORS
from datetime import datetime, timedelta
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
import requests
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
from folderCreator import folderCreator
#from reportlab.pdfgen import canvas


app = Flask(__name__)
#CORS(app)


app.secret_key = 'nkvjbnkjkjkjnskfnkjfbni3w89ufhbbisef89hfknkjn'

'''
app.config['MYSQL_HOST'] = 'http://leaderformationsb.com'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'nigella@123'
app.config['MYSQL_DB'] = 'nigella_form'
mysql = MySQL(app)
'''
# Internet Connection status
def check_internet():
    try:
        response = requests.get('http://www.google.com', timeout=5)
        if response.status_code == 200:
            return ('internet_connected')
    except requests.ConnectionError:
        return ('internet_not_connected')



# Date today
current_date = datetime.now().strftime('%d/%m/%Y')

# Previous 7th Date
def previous_seventh_date():
    current_date = datetime.now()
    previous_seventh_date = current_date - timedelta(days=7)
    formatted_date = previous_seventh_date.strftime('%d/%m/%Y')
    return formatted_date

# SQLite 3 connection 
def get_db_connection():
    conn = sqlite3.connect('database.db')
    #conn.row_factory = sqlite3.Row
    return conn

conn = get_db_connection()
cur = conn.cursor()
category = cur.execute('SELECT * FROM users').fetchall()
#print(category)

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

@app.route("/api", methods=['GET'])
def api():
    return ('usersCheck = users')



# SignIn Page
@app.route("/")
def login():
    connection = check_internet()

    # MySQL
    '''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Fetch data from the users table
    cursor.execute("SELECT * FROM users")
    usersF = cursor.fetchall()
    print('UserF: ', usersF)
    #End MySQL
    '''
    port = request.environ.get('SERVER_PORT')

    conn = get_db_connection()
    cur = conn.cursor()
    users = cur.execute("SELECT * FROM users")
    return render_template('login.html', usersCheck = users, connection=connection)


# User Registration
@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if(request.method == 'POST'):
        urn = request.form.get('userr')
        pwd = request.form.get('pwdr')
        currentDate = datetime.now()
        cDate = str(currentDate.day)+"/"+str(currentDate.month)+"/"+str(currentDate.year)
        cTime = str(currentDate.hour)+":"+str(currentDate.minute)+":"+str(currentDate.second)
        # Query
        conn = get_db_connection()
        cur = conn.cursor()
        users = cur.execute("INSERT INTO users(username, password, creation_date, creation_time) VALUES('"+urn+"', '"+pwd+"', '"+cDate+"', '"+cTime+"')")
        conn.commit()
        conn.close()
        session['registration']  = 'success'
        #session.pop('registration', None)

        # End
        return redirect('/')     
    else:
        #print('not found')
        return redirect('/')

@app.route("/login", methods=['GET', 'POST'])
def loginCheck():
    if(request.method == 'POST'):
        # Check connection
        connection = check_internet()
        if connection == 'internet_not_connected':
            return render_template('login.html', connection=connection)
            

        user = request.form.get('user')
        pwd = request.form.get('pwd')
        conn = get_db_connection()
        cur = conn.cursor()
        user = cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        user = user.fetchall()
        user = len(user)
        # Start
        if(user == 1):
            session['username']  = user
            return redirect('/add-worker')    
        else:
            session['login']  = 'error'
            return redirect('/')
        # End     
    else:
        #print('not found')
        return redirect('/')
    

# Get Company Name in Sort form
def company_first_letters(input_string):
    words = input_string.split()
    first_letters = [word[0] for word in words]
    return ''.join(first_letters)


# Add Worker
@app.route("/add-worker")
def addWorker():
    if 'username' in session:
        # Check connection
        connection = check_internet()
        if connection == 'internet_not_connected':
            return render_template('login.html', connection=connection)
        

        serverPort = request.environ.get('SERVER_PORT')
        
        # check profile data
        conn = get_db_connection()
        cur = conn.cursor()
        profile = cur.execute("SELECT * FROM profile")
        
        # Register Branch Address for workers & family members
        cur.execute("SELECT branch_address1, branch_address2, branch_address3 FROM profile")
        profileBranchAddress = cur.fetchall()
        
        for row in profileBranchAddress:
            branch_address1 = row[0]
            branch_address2 = row[1]
            branch_address3 = row[2]
        
        # Worker Registration Number
        # --------------------------
        # for Date & time
        workerPrefix = 'FW'
        
        currentDate = datetime.now()
        currentYear = currentDate.strftime("%y")
        
        cur.execute("SELECT employer_company_name FROM profile where id=3")
        companyName = cur.fetchall()
        companyName = companyName[0][0]
        companyShortName = company_first_letters(companyName)
        
        # Number of Worker
        # Find Last Key of Worker
        cur.execute('SELECT MAX(id) FROM half_form')
        last_key = cur.fetchone()[0]
        workerSerialNumber = last_key + 1
        formatted_number = f"{workerSerialNumber:06}"
        
        workerRegistrationNumber = workerPrefix + currentYear + companyShortName.upper() + formatted_number
        
        # Create the Folder For Worker
        folderCreator(workerRegistrationNumber, 'legal', 0, 0, 0)
        # End Worker Registration Number
        # ------------------------------
        
        # Find The lask Family member
        cur.execute('SELECT MAX(id) FROM family_form')
        fm_last_key = cur.fetchone()[0]
        new_fMemberID = fm_last_key
        fmPrefix = 'FM'
        fm_registrationPrefix = fmPrefix + currentYear + companyShortName.upper()
        
        # End Find The lask Family member
        
        
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
        cur.execute("SELECT job_sector, uuid FROM detailed_dd_job_sector")
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

        #cur.execute("SELECT job_sub_sector FROM detailed_dd_job_sub_sector")
        #job_sub_sector = cur.fetchall()

        cur.execute("SELECT job_status_sponser FROM detailed_dd_job_status_sponsor")
        job_status_sponsor = cur.fetchall()

        return render_template('add-worker.html',ip_address=ip_address, serverPort=serverPort, branch_address1=branch_address1, branch_address2=branch_address2, branch_address3=branch_address3, workerRegistrationNumber=workerRegistrationNumber, new_fMemberID=new_fMemberID, fm_registrationPrefix=fm_registrationPrefix, profileC = profile, filename=gallery_images, filename2=gallery_images2, filename3=gallery_images3, filename4=gallery_images4, filename5=gallery_images5, filename6=gallery_images6, filename7=gallery_images7, filename8=gallery_images8, citizenshipList=citizenship, maritialList=maritial, poeList=poe, genderList=gender, religionList=religion, raceList=race, relationshipList=relationship, jobSectorList=job_sector, cityList=city, stateList=state, issuingCountryList=issuingCountry, docStatusList=docStatus, curDocStatusList=curDocStatus, typeOfDocList=typeOfDoc, employement_statusList=employement_status, jobStatusSponsorList = job_status_sponsor)
    else:
        return redirect('/')
    
# For add worker >> sub sector
@app.route("/add-worker-sub-sector", methods=['GET', 'POST'])
def addWorker_subSector():
    if 'username' in session:
        sector_uuid = request.form.get('job_sector')
        # check profile data
        conn = get_db_connection()
        cur = conn.cursor()
        # for Date & time
        currentDate = datetime.now()
        cYear = currentDate.strftime("%y")

        cur.execute("SELECT job_sub_sector FROM detailed_dd_job_sub_sector where uuid='"+sector_uuid+"'")
        job_sub_sector = cur.fetchall()
        return jsonify(job_sub_sector)
    else:
        return redirect('/')
# End For add worker >> sub sector

# Save Worker
@app.route("/save-worker", methods=['GET', 'POST'])
def saveWorker():
    conn = get_db_connection()
    cur = conn.cursor()
    if 'username' in session:
        if request.method == 'POST':
            try:
                docData = request.form.get('docData')
                workersDocData = json.loads(docData)
                
                # Fm Len 
                submittedData = request.form
                fmLen = request.form.get('familyMemberLen')
               
                # Form Data
                form_created_by = 'static'
                form_created_date = 'static'
                form_worker_reg_no = request.form.get('awl_worker_registration_no')
                no_family_mem = request.form.get('no_of_family_member')
                worker_detail_worker_legal_status = request.form.get('awl_worker_legal_status')
                worker_detail_name_of_worker = request.form.get('awl_name_of_worker')
                
                worker_detail_family_name = request.form.get('awl_family_name')
                worker_detail_gender = request.form.get('awl_gender')
                worker_detail_DOB = request.form.get('awl_d_o_b')
                worker_detail_place_birth = request.form.get('awl_place_of_birth')
                worker_detail_citizenship = request.form.get('awl_citizenship')
                
                worker_detail_marital_status = request.form.get('awl_maritial_status')
                worker_detail_poe = request.form.get('awl_point_of_entry')
                worker_detail_religion = request.form.get('awl_religion')
                worker_detail_race = request.form.get('awl_race')
                worker_detail_contact_no = request.form.get('awl_worker_contact_no')
                
                worker_detail_email = request.form.get('awl_worker_email')
                worker_detail_nok = request.form.get('awl_name_of_next_kin')
                worker_detail_relationship = request.form.get('awl_relationship')
                worker_detail_nok_contact_no = request.form.get('awl_nok_contact_no')
                worker_emp_dtl_job_sector = request.form.get('awl_job_sector')
                
                worker_emp_dtl_job_sub_sector = request.form.get('awl_job_sub_sector')
                worker_emp_dtl_emp_sponsorship_status = request.form.get('awl_employement_sponsorship_status')
                worker_emp_dtl_address1 = request.form.get('awl_address1')
                worker_emp_dtl_address2 = request.form.get('awl_address2')
                worker_emp_dtl_address3 = request.form.get('awl_address3')
                
                worker_emp_dtl_postcode = 'postcode - static' #request.form.get('')
                worker_emp_dtl_city = request.form.get('awl_city')
                worker_emp_dtl_state = request.form.get('awl_state')
                worker_doc_dtl_doc_id = request.form.get('document_id')
                worker_doc_dtl_type_of_doc = request.form.get('type_of_documents')
                
                worker_doc_dtl_no_of_doc = 'static' #request.form.get('')
                worker_doc_dtl_images_path_email = 'static' # request.form.get()
                worker_doc_dtl_place_of_issue = request.form.get('awl_place_of_issue')
                worker_doc_dtl_issue_date = request.form.get('awl_document_issued_date')
                worker_doc_dtl_expiry_date = request.form.get('awl_document_expiry_date')
                
                worker_doc_dtl_country_doc_issued = request.form.get('awl_issuing_country')
                worker_doc_dtl_doc_status = request.form.get('awl_document_status')
                worker_doc_dtl_doc_current_status = request.form.get('awl_status_of_current_document')
                worker_doc_dtl_doc_no = 'static' #request.form.get('')
                form_position = 'static' #request.form.get()
                
                form_status = 'static' #request.form.get()
                form_unique_key = 'static' #request.form.get()
                
                # Find Last Key of Worker
                cur.execute('SELECT MAX(worker_key) FROM half_form')
                last_key = cur.fetchone()[0]
                next_key = last_key + 1
                #print('Last Key: ', last_key, 'Next Key: ', next_key)
                

                
                # Worker Insert
                cur.execute('INSERT INTO half_form (worker_key, form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, worker_doc_dtl_doc_id, worker_doc_dtl_type_of_doc, worker_doc_dtl_no_of_doc, worker_doc_dtl_images_path_email, worker_doc_dtl_place_of_issue, worker_doc_dtl_issue_date, worker_doc_dtl_expiry_date, worker_doc_dtl_country_doc_issued, worker_doc_dtl_doc_status, worker_doc_dtl_doc_current_status, worker_doc_dtl_doc_no, form_position, form_status, form_unique_key) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, worker_doc_dtl_doc_id, worker_doc_dtl_type_of_doc, worker_doc_dtl_no_of_doc, worker_doc_dtl_images_path_email, worker_doc_dtl_place_of_issue, worker_doc_dtl_issue_date, worker_doc_dtl_expiry_date, worker_doc_dtl_country_doc_issued, worker_doc_dtl_doc_status, worker_doc_dtl_doc_current_status, worker_doc_dtl_doc_no, form_position, form_status, form_unique_key))
                
                # End Worker Insert
                
                # Insert Workers Document
                for docs in workersDocData:
                    document_link = ''
                    type_of_documents = docs['type_of_documents']
                    document_id = docs['document_id']
                    place_of_issue = docs['place_of_issue']
                    document_issued_date = docs['document_issued_date']
                    document_expiry_date = docs['document_expiry_date']
                    issuing_country = docs['issuing_country']
                    document_status = docs['document_status']
                    status_of_current_document = docs['status_of_current_document']
                    
                    #query
                    cur.execute('INSERT INTO workers_document (worker_key, document_link, type_of_douments, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, document_link, type_of_documents, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document))
                # End Insert Workers Document

                # Insert Worker Family
                '''
                for x in range(0, fmLen+1):
                    
                    cur.execute('INSERT INTO workers_document (worker_key, document_link, type_of_douments, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, document_link, type_of_documents, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document))
                '''    
                # End Insert Worker Family
                
        
                conn.commit()
                cur.close()
                
                
                
                session['save_worker_success'] = 'success'
                #print('success')
                return redirect('/add-worker')
            except Exception as e:
                #print("Error Fl: ", e)
                session['save_worker_error'] = 'error'
                return redirect('/add-worker')
        else:
            #print('method not found')
            return redirect('/add-worker')
    else:
        return redirect('/')
    



# Submit Worker 2nd
# Save Worker
@app.route("/insertWorker", methods=['POST'])
def insertWorker():
    conn = get_db_connection()
    cur = conn.cursor()
    
    if 'username' in session:
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
                        form_created_by = 'static'
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
                        form_unique_key = 'static' 
                    
                    
                    # Find Last Key of Worker
                    cur.execute('SELECT MAX(worker_key) FROM half_form')
                    last_key = cur.fetchone()[0]
                    next_key = last_key + 1
                    #print('Last Key: ', last_key, 'Next Key: ', next_key)
                    

                    
                    # Worker Insert
                    cur.execute('INSERT INTO half_form (worker_key, form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, worker_doc_dtl_doc_id, worker_doc_dtl_type_of_doc, worker_doc_dtl_no_of_doc, worker_doc_dtl_images_path_email, worker_doc_dtl_place_of_issue, worker_doc_dtl_issue_date, worker_doc_dtl_expiry_date, worker_doc_dtl_country_doc_issued, worker_doc_dtl_doc_status, worker_doc_dtl_doc_current_status, worker_doc_dtl_doc_no, form_position, form_status, form_unique_key) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, worker_doc_dtl_doc_id, worker_doc_dtl_type_of_doc, worker_doc_dtl_no_of_doc, worker_doc_dtl_images_path_email, worker_doc_dtl_place_of_issue, worker_doc_dtl_issue_date, worker_doc_dtl_expiry_date, worker_doc_dtl_country_doc_issued, worker_doc_dtl_doc_status, worker_doc_dtl_doc_current_status, worker_doc_dtl_doc_no, form_position, form_status, form_unique_key))
                    
                    # End Worker Insert 
                    
                    # Insert Workers Document
                    
                    for docs in docData:
                        document_link = ''
                        type_of_documents = docs['type_of_documents']
                        document_id = docs['document_id']
                        place_of_issue = docs['place_of_issue']
                        document_issued_date = docs['document_issued_date']
                        document_expiry_date = docs['document_expiry_date']
                        issuing_country = docs['issuing_country']
                        document_status = docs['document_status']
                        status_of_current_document = docs['status_of_current_document']
                    
                        #query
                        cur.execute('INSERT INTO workers_document (worker_key, document_link, type_of_douments, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, document_link, type_of_documents, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document))
                    # End Insert Workers Document
                    
                elif formStatus == 'workerWithFamily':
                    #print(formStatus)
                    # Worker & Family
                
                    # JSON to Obj
                    workerData = json.loads(workerD)
                    docData = json.loads(docD)
                    familyMemberData = json.loads(fmData)
                    '''
                    print('** workerData **')
                    print(workerData)
                    print('** End **')
                    print('** docData **')
                    print(docData)
                    print('** End **')
                    print('** familyMemberData **')
                    print(familyMemberData)
                    print('** End **')
                    '''
                    # Form Data
                    for worker in workerData:
                        form_created_by = 'static'
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
                        form_unique_key = 'static' 
                    
                    
                    # Find Last Key of Worker
                    cur.execute('SELECT MAX(worker_key) FROM half_form')
                    last_key = cur.fetchone()[0]
                    next_key = last_key + 1
                    #print('Last Key: ', last_key, 'Next Key: ', next_key)
                    

                    
                    # Worker Insert
                    cur.execute('INSERT INTO half_form (worker_key, form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, worker_doc_dtl_doc_id, worker_doc_dtl_type_of_doc, worker_doc_dtl_no_of_doc, worker_doc_dtl_images_path_email, worker_doc_dtl_place_of_issue, worker_doc_dtl_issue_date, worker_doc_dtl_expiry_date, worker_doc_dtl_country_doc_issued, worker_doc_dtl_doc_status, worker_doc_dtl_doc_current_status, worker_doc_dtl_doc_no, form_position, form_status, form_unique_key) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, form_created_by, form_created_date, form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status, worker_detail_name_of_worker, worker_detail_family_name, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_detail_email, worker_detail_nok, worker_detail_relationship, worker_detail_nok_contact_no, worker_emp_dtl_job_sector, worker_emp_dtl_job_sub_sector, worker_emp_dtl_emp_sponsorship_status, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state, worker_doc_dtl_doc_id, worker_doc_dtl_type_of_doc, worker_doc_dtl_no_of_doc, worker_doc_dtl_images_path_email, worker_doc_dtl_place_of_issue, worker_doc_dtl_issue_date, worker_doc_dtl_expiry_date, worker_doc_dtl_country_doc_issued, worker_doc_dtl_doc_status, worker_doc_dtl_doc_current_status, worker_doc_dtl_doc_no, form_position, form_status, form_unique_key))
                    
                    # End Worker Insert 
                    
                    # Insert Workers Document
                    
                    for docs in docData:
                        document_link = ''
                        type_of_documents = docs['type_of_documents']
                        document_id = docs['document_id']
                        place_of_issue = docs['place_of_issue']
                        document_issued_date = docs['document_issued_date']
                        document_expiry_date = docs['document_expiry_date']
                        issuing_country = docs['issuing_country']
                        document_status = docs['document_status']
                        status_of_current_document = docs['status_of_current_document']
                    
                        #query
                        cur.execute('INSERT INTO workers_document (worker_key, document_link, type_of_douments, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, document_link, type_of_documents, document_id, place_of_issue, document_issued_date, document_expiry_date, issuing_country, document_status, status_of_current_document))
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
                        cur.execute('INSERT INTO family_form (worker_key, form_created_by, form_created_date, form_unique_key, form_family_reg_no, family_form_worker_name, family_form_relationship, family_form_name_of_family_member, family_form_family_name,family_form_is_family_together, family_form_family_form_poe, family_form_citizenship, family_form_religion,family_form_marital_status, family_form_gender, family_form_address1, family_form_address2, family_form_address3, family_form_postcode, family_form_city, family_form_state, family_form_contact_no, family_form_race, family_form_place_of_birth, family_form_emp_status, family_form_emp_name, family_form_emp_address, family_form_doc_path_email, family_form_doc_image_no) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (next_key, 'created by', current_date, next_key, fm_worker_registration_no, fm_worker_name, fm_relationship, fm_name_of_family_member, fm_family_name, fm_is_family_member_together, fm_point_of_entry, fm_citizenship, fm_religion, fm_marital_status, fm_gender, fm_address1, fm_address2, fm_address3, fm_postcode, fm_city, fm_state, fm_contact_no, fm_race, fm_place_of_birth, fm_employment_status, fm_employer_name, fm_employer_address, 'static email', 'doc image- static'))
                        
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
    
    
# End Submit Worker 2nd



# Worker & Family Member Folder Creation
@app.route("/worker-fm-folderCreator", methods=['GET', 'POST'])
def worker_fm_folderCreator():
    if 'username' in session:
        if(request.method == 'POST'):
            folderData = request.get_json()
            worker_registration_folder_name = folderData.get('worker_registration_folder_name')
            
            fMember_prefix = folderData.get('fMember_prefix')
            fm_last_ID = folderData.get('fm_last_ID')
            total_fMember = folderData.get('total_fMember')
            
            # Final Family member registration number 
            folderCreator(worker_registration_folder_name, 'legal', fMember_prefix, fm_last_ID, total_fMember)
            return ({"status":"success"})
            
            
            


# Set number of Family member
@app.route("/number-of-family-member", methods=['GET', 'POST'])
def setFamilyMember():
    if 'username' in session:
        if(request.method == 'POST'):
            family_member = request.form.get('family_member_number', type=int)
            session['family_member'] = family_member
            return redirect('/add-worker')

    
# Profile    
@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        # Check connection
        connection = check_internet()
        if connection == 'internet_not_connected':
            return render_template('login.html', connection=connection)
        
        
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
        cur.execute("SELECT sector FROM detailed_dd_sector")
        sector = cur.fetchall()

         # for the designation 
        cur.execute("SELECT designation FROM detailed_dd_designation")
        designation = cur.fetchall()

        return render_template('profile.html', licenseCategoryList=licenseCategory, cityList=city, stateList=state, sectorList=sector, designationList=designation)
    else:
        return redirect('/')
    

# Profile Form Data
@app.route("/profile-form-data", methods=['GET', 'POST'])
def profileFormData():
    if 'username' in session:
        #Get DB
        conn = get_db_connection()
        cur = conn.cursor()
    
        cur.execute("SELECT * FROM profile")
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
                    branch_office_mobile_number = request.form.get('branch_office_mobile_number')
                    branch_email = request.form.get('branch_email')
                    branch_name_of_person_in_charge = request.form.get('branch_name_of_person_in_charge')
                    branch_designation = request.form.get('branch_designation')
                    branch_pic_mobile_number = request.form.get('branch_pic_mobile_number')
                    
                    # formData = [{"agency":aps_agency_pekerjaan}, {"license_category":aps_license_category}]
                    
                    #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
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
    if 'username' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM profile")
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
        cur.execute("SELECT sector FROM detailed_dd_sector")
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
    if 'username' in session:
        if request.method == 'POST':
            try:
                # APS Data
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
                branch_office_mobile_number = request.form.get('branch_office_mobile_number')
                branch_email = request.form.get('branch_email')
                branch_name_of_person_in_charge = request.form.get('branch_name_of_person_in_charge')
                branch_designation = request.form.get('branch_designation')
                branch_pic_mobile_number = request.form.get('branch_pic_mobile_number')
                
                # formData = [{"agency":aps_agency_pekerjaan}, {"license_category":aps_license_category}]
                
                #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute('UPDATE profile SET aps_agency_pekerjaan="'+aps_agency_pekerjaan+'", aps_license_category="'+aps_license_category+'", aps_postcode="'+aps_postcode+'", aps_office_telephone_no="'+aps_office_telephone_no+'", aps_new_ssm_number="'+aps_new_ssm_number+'", aps_address1="'+aps_address1+'", aps_city="'+aps_city+'", aps_mobile_number="'+aps_mobile_number+'", aps_old_ssm_number="'+aps_old_ssm_number+'", aps_address2="'+aps_address2+'", aps_state="'+aps_state+'", aps_email="'+aps_email+'", aps_license_no="'+aps_license_no+'", aps_address3="'+aps_address3+'", aps_license_exp_date="'+aps_license_exp_date+'", aps_contact_person="'+aps_contact_person+'", employer_company_name="'+employer_company_name+'", employer_new_ssm_number="'+employer_new_ssm_number+'", employer_old_ssm_number="'+employer_old_ssm_number+'", employer_address1="'+employer_address1+'", employer_address2="'+employer_address2+'", employer_address3="'+employer_address3+'", employer_postcode="'+employer_postcode+'", employer_city="'+employer_city+'", employer_state="'+employer_state+'", employer_office_telephone_no="'+employer_office_telephone_no+'", employer_mobile_no="'+employer_mobile_no+'", employer_fax_number="'+employer_fax_number+'", employer_year_of_commence="'+employer_year_of_commence+'", employer_sector="'+employer_sector+'", employer_name_of_person_in_charge="'+employer_name_of_person_in_charge+'", employer_designation="'+employer_designation+'", employer_pic_mobile_number="'+employer_pic_mobile_number+'", branch_employment_location_name="'+branch_employment_location_name+'", branch_address1="'+branch_address1+'", branch_address2="'+branch_address2+'", branch_address3="'+branch_address3+'", branch_postcode="'+branch_postcode+'", branch_state="'+branch_state+'", branch_city="'+branch_city+'", branch_office_telephone_number="'+branch_office_telephone_number+'", branch_office_mobile_number="'+branch_office_mobile_number+'", branch_email="'+branch_email+'", branch_name_of_person_in_charge="'+branch_name_of_person_in_charge+'", branch_designation="'+branch_designation+'", branch_pic_mobile_number="'+branch_pic_mobile_number+'" WHERE id="'+profile_id+'"')
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
        avatarPath = './static/documents/' + fPath
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
    img = request.args.get('doc')
    return render_template('view-img.html', viewImg=img)


@app.route("/export-form-to-excel", methods=['GET', 'POST'])
def exportExcel():
    if 'username' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        totalWorker = cur.execute("SELECT id, form_worker_reg_no, worker_detail_name_of_worker FROM half_form")
        workerD = cur.fetchall()
        totalWorker = len(workerD)
        return render_template('export-form-to-excel.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')
'''
log = [
    ('login', datetime(2015, 1, 10, 5, 30)),
    ('deposit', datetime(2015, 1, 10, 5, 35)),
    ('order', datetime(2015, 1, 10, 5, 50)),
    ('withdraw', datetime(2015, 1, 10, 6, 10)),
    ('logout', datetime(2015, 1, 10, 6, 15))
]
'''

# Worker Registration List
@app.route("/registration-list", methods=['GET', 'POST'])
def registrationList():
    if 'username' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        totalWorker = cur.execute("SELECT id, form_worker_reg_no, worker_detail_name_of_worker FROM half_form")
        workerD = cur.fetchall()
        totalWorker = len(workerD)
        return render_template('registration-list.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')

# View Registered Worker
@app.route("/view-registered-worker", methods=['GET', 'POST'])
def viewRegisteredWorker():
    if 'username' in session:
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
        
        return render_template('view-registered-worker.html', workerList = workerD, workerDocs=workerDocs, workerFM=workerFM)
    else:
        return redirect('/')

# Worker view-family-member
@app.route("/view-family-member", methods=['GET', 'POST'])
def viewFamilyMember():
    if 'username' in session:
        fmId = request.args.get('fm')
        conn = get_db_connection()
        cur = conn.cursor()

        # fetch workers
        cur.execute("SELECT * FROM family_form where id=?", (fmId,))
        fmData = cur.fetchall()
        
        return render_template('view-family-member.html', fmData=fmData)
    else:
        return redirect('/')
    

# Edit Registered Worker
@app.route("/edit-registered-worker", methods=['GET', 'POST'])
def editRegisteredWorker():
    if 'username' in session:
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
        
        return render_template('edit-registered-worker.html', workerList = workerD, workerDocs=workerDocs, workerFM=workerFM)
    else:
        return redirect('/')
    
# Update Registered Worker
@app.route("/update-registered-worker", methods=['POST'])
def updateRegisteredWorker():
    if 'username' in session:
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
    if 'username' in session:
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
    if 'username' in session:
        fmId = request.args.get('fm')
        conn = get_db_connection()
        cur = conn.cursor()

        # fetch workers
        cur.execute("SELECT * FROM family_form where id=?", (fmId,))
        fmData = cur.fetchall()
        return render_template('edit-family-member.html', fmData=fmData)
    else:
        return redirect('/')
    

# Update Family Member
@app.route("/update-family-member", methods=['POST'])
def updateFamilyMember():
    if 'username' in session:
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
    if 'username' in session:
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
        session['registration_list_delete'] = 'success'
        return redirect('/registration-list')
    else:
        return redirect('/')


@app.route('/download-excel-file', methods=['GET'])
def download_log():
    conn = get_db_connection()
    cur = conn.cursor()
    
    workerData = request.args.get('file')
    workerLen = len(workerData)
    
    if workerData == 'exportAll':
        cur.execute("SELECT form_worker_reg_no, worker_detail_name_of_worker FROM half_form")
        log = cur.fetchall()
    elif workerLen > 1:
        workerId = json.loads(workerData)
        cur.execute("SELECT form_worker_reg_no, worker_detail_name_of_worker FROM half_form where id IN ("+workerId+")")
        log = cur.fetchall()
    elif workerLen == 1:
        workerId = workerData
        cur.execute("SELECT form_worker_reg_no, worker_detail_name_of_worker FROM half_form where id='"+workerId+"'")
        log = cur.fetchall()
    
    def generate():
        data = StringIO()
        w = csv.writer(data)

        # write header
        w.writerow(('form_worker_reg_no', 'worker_detail_name_of_worker'))
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






# registration-log  
@app.route("/registration-log", methods=['GET', 'POST'])
def registrationLog():
    if 'username' in session:
        #cur = mysql.connection.cursor()
        conn = get_db_connection()
        cur = conn.cursor()
        
        previous_7th_date = previous_seventh_date()

        # reg. worker Current Day
        cur.execute('SELECT * FROM half_form where form_created_date="'+current_date+'"')
        regWorkerDay = cur.fetchall()
        regWorkerDay = len(regWorkerDay)
        
        # reg. Family member Current Day
        cur.execute('SELECT * FROM family_form where form_created_date="'+current_date+'"')
        regMemberDay = cur.fetchall()
        regMemberDay = len(regMemberDay)
        regNumber = regWorkerDay + regMemberDay
        
        # reg. worker Current Week
        cur.execute('SELECT * FROM half_form where form_created_date BETWEEN "'+previous_7th_date+'" AND "'+current_date+'"')
        regWorkerWeek = cur.fetchall()
        regWorkerWeek = len(regWorkerWeek)
        
        # reg. Family member Current Week
        cur.execute('SELECT * FROM family_form where form_created_date BETWEEN "'+previous_7th_date+'" AND "'+current_date+'"')
        regMemberWeek = cur.fetchall()
        regMemberWeek = len(regMemberWeek)
        regNumberWeek = regWorkerWeek + regMemberWeek
        

        # Legal status
        cur.execute('SELECT * FROM half_form where worker_detail_worker_legal_status="legal" AND form_created_date BETWEEN "'+previous_7th_date+'" AND "'+current_date+'"') 
        totalLegal = cur.fetchall()
        totalLegal = len(totalLegal)

        # illegal status
        cur.execute('SELECT * FROM half_form where worker_detail_worker_legal_status="illegal" AND form_created_date BETWEEN "'+previous_7th_date+'" AND "'+current_date+'"')
        totalIllegal = cur.fetchall()
        totalIllegal = len(totalIllegal)
        
        return render_template('registration-log.html', regNumber=regNumber, memberReg=regMemberDay, totalWorker=regWorkerDay, grandTotal=regNumberWeek, totalLegal=totalLegal, totalIllegal=totalIllegal)
    else:
        return redirect('/')


# Print QR Code
@app.route("/print-qr-code", methods=['GET', 'POST'])
def printQrCode():
    if 'username' in session:
        #cur = mysql.connection.cursor()
        conn = get_db_connection()
        cur = conn.cursor()
        totalWorker = cur.execute("SELECT id, form_worker_reg_no, worker_detail_name_of_worker, form_status FROM half_form")
        workerD = cur.fetchall()
        totalWorker = len(workerD)
        return render_template('print-qr-code.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')
    

# Worker Details
@app.route("/worker-details", methods=['GET', 'POST'])
def workerDetails():
    if 'username' in session:
        workerId = request.args.get('wrkr')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, form_worker_reg_no, worker_detail_name_of_worker, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state form_status FROM half_form where id='"+workerId+"'")
        workerD = cur.fetchall()
        totalWorker = len(workerD)
        return render_template('worker-details.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')
    

# Print QR
@app.route("/print-qr", methods=['GET', 'POST'])
def printQr():
    if 'username' in session:
        status = request.args.get('status')
        workerName = request.args.get('name')
        workerRegNum = request.args.get('regN')
        
        if status == 'qr':
            return render_template('print-qr.html', workerName=workerName, workerRegNum=workerRegNum)
        elif status == 'qr-3x3':
            return render_template('print-qr-3x3.html', workerName=workerName, workerRegNum=workerRegNum)
    else:
        return redirect('/')
    
    
# 
@app.route("/online-server-sync", methods=['GET', 'POST'])
def onlineServerSync():
    if 'username' in session:
        return render_template('online-server-sync.html')
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
    if 'username' in session:
        #session.pop('username', None)
        session.clear()
        return redirect('/')
    else:
        return redirect('/')




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

        


# End RESTful API > Upload image



def start_server():
    app.run(host=ip_address, port=5000)

if __name__ == '__main__':
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    webview.create_window("Swims Form DeskApp", f"http://{ip_address}:5000")  # Use 0.0.0.0 to bind to all network interfaces
    webview.start()