from flask import Flask, render_template, Response, request, redirect, session, jsonify, json
import datetime
#from datetime import datetime
from flask_mysqldb import MySQL
import MySQLdb.cursors
import glob
import io
from io import StringIO
import csv
from werkzeug.wrappers import Response

#from flask_cors import CORS, cross_origin
import webview

app = Flask(__name__)

#CORS(app)

window = webview.create_window('Swims', app)
app.secret_key = 'nkvjbnkjkjkjnskfnkjfbni3w89ufhbbisef89hfknkjn'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'nigella_form'

mysql = MySQL(app)

#app = Flask(__name__, template_folder='templates')

# new code changable

# End > new code changable



@app.route("/api", methods=['GET'])
def api():
    return ('usersCheck = users')


# SignIn Page
@app.route("/")
def login():
    cur = mysql.connection.cursor()
    users = cur.execute("SELECT * FROM users")
    return render_template('login.html', usersCheck = users)

# User Registration
@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if(request.method == 'POST'):
        urn = request.form.get('userr')
        pwd = request.form.get('pwdr')
        currentDate = datetime.datetime.now()
        cDate = str(currentDate.day)+"/"+str(currentDate.month)+"/"+str(currentDate.year)
        cTime = str(currentDate.hour)+":"+str(currentDate.minute)+":"+str(currentDate.second)
        # Query
        cur = mysql.connection.cursor()
        users = cur.execute("INSERT INTO users(username, password, creation_date, creation_time) VALUES('"+urn+"', '"+pwd+"', '"+cDate+"', '"+cTime+"')")
        mysql.connection.commit()
        cur.close()
        session['registration']  = 'success'
        #session.pop('registration', None)

        # End
        return redirect('/')     
    else:
        print('not found')
        return redirect('/')

@app.route("/login", methods=['GET', 'POST'])
def loginCheck():
    if(request.method == 'POST'):
        user = request.form.get('user')
        pwd = request.form.get('pwd')

        cur = mysql.connection.cursor()
        user = cur.execute("SELECT * FROM users WHERE username = '"+user+"' AND password = '"+pwd+"'")
        print(user)
        # Start
        if(user == 1):
            session['username']  = user
            return redirect('/add-worker')    
        else:
            session['login']  = 'error'
            return redirect('/')
        # End     
    else:
        print('not found')
        return redirect('/')


# Add Worker
@app.route("/add-worker")
def addWorker():
    if 'username' in session:
        # check profile data
        cur = mysql.connection.cursor()
        profile = cur.execute("SELECT * FROM profile")
        # End Check profile Data
        gallery_images = glob.glob('./static/img/uploaded-image/legal1/*')
        gallery_images2 = glob.glob('./static/img/uploaded-image/legal2/*')
        gallery_images3 = glob.glob('./static/img/uploaded-image/illegal1/*')
        gallery_images4 = glob.glob('./static/img/uploaded-image/illegal2/*')
        gallery_images5 = glob.glob('./static/img/uploaded-image/illegal3/*')
        gallery_images6 = glob.glob('./static/img/uploaded-image/illegal4/*')
        gallery_images7 = glob.glob('./static/img/uploaded-image/illegal5/*')
        gallery_images8 = glob.glob('./static/img/uploaded-image/illegal6/*')

        # for Date & time
        currentDate = datetime.datetime.now()
        cYear = currentDate.strftime("%y")

        workerNum = '00001'

        print('FW'+cYear+'NS'+workerNum)
        

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

        cur.execute("SELECT job_sub_sector FROM detailed_dd_job_sub_sector")
        job_sub_sector = cur.fetchall()

        cur.execute("SELECT job_status_sponser FROM detailed_dd_job_status_sponsor")
        job_status_sponsor = cur.fetchall()

        return render_template('add-worker.html', profileC = profile, filename=gallery_images, filename2=gallery_images2, filename3=gallery_images3, filename4=gallery_images4, filename5=gallery_images5, filename6=gallery_images6, filename7=gallery_images7, filename8=gallery_images8, citizenshipList=citizenship, maritialList=maritial, poeList=poe, genderList=gender, religionList=religion, raceList=race, relationshipList=relationship, jobSectorList=job_sector, cityList=city, stateList=state, issuingCountryList=issuingCountry, docStatusList=docStatus, curDocStatusList=curDocStatus, typeOfDocList=typeOfDoc, employement_statusList=employement_status, jobSubSectorList=job_sub_sector, jobStatusSponsorList = job_status_sponsor)
    else:
        return redirect('/')


# Save Worker
@app.route("/save-worker", methods=['GET', 'POST'])
def saveWorker():
    if 'username' in session:
        if request.method == 'POST':
            try:
                # Form Data
                worker_registration_no = request.form.get('worker_registration_no')
                no_of_family_member = request.form.get('no_of_family_member')
                worker_legal_status = request.form.get('worker_legal_status')
                name_of_worker = request.form.get('name_of_worker')
                family_name = request.form.get('family_name')
                
                print(worker_registration_no)
                print(no_of_family_member)
                # save Worker data
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO half_form(form_worker_reg_no, no_family_mem, worker_detail_worker_legal_status,worker_detail_name_of_worker, worker_detail_family_name) VALUES("'+worker_registration_no+'", "'+no_of_family_member+'", "'+worker_legal_status+'", "'+name_of_worker+'", "'+family_name+'")')
                mysql.connection.commit()
                cursor.close()  
                session['save_worker_success'] = 'success'
                return redirect('/add-worker')
            except Exception as e:
                print(e)
                session['save_worker_error'] = 'error'
                return redirect('/add-worker')
        else:
            return redirect('/add-worker')
    else:
        return redirect('/')
    

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
        
        cur = mysql.connection.cursor()

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

        cur = mysql.connection.cursor()
        checkPro = cur.execute("SELECT * FROM profile")
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
                    
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('INSERT INTO profile(aps_agency_pekerjaan, aps_license_category, aps_postcode, aps_office_telephone_no, aps_new_ssm_number, aps_address1, aps_city, aps_mobile_number, aps_old_ssm_number, aps_address2, aps_state, aps_email, aps_license_no, aps_address3, aps_license_exp_date, aps_contact_person, employer_company_name, employer_new_ssm_number, employer_old_ssm_number, employer_address1, employer_address2, employer_address3, employer_postcode, employer_city, employer_state, employer_office_telephone_no, employer_mobile_no, employer_fax_number, employer_year_of_commence, employer_sector, employer_name_of_person_in_charge, employer_designation, employer_pic_mobile_number, branch_employment_location_name, branch_address1, branch_address2, branch_address3, branch_postcode, branch_state, branch_city, branch_office_telephone_number, branch_office_mobile_number, branch_email, branch_name_of_person_in_charge, branch_designation, branch_pic_mobile_number) VALUES("'+aps_agency_pekerjaan+'", "'+aps_license_category+'", "'+aps_postcode+'", "'+aps_office_telephone_no+'", "'+aps_new_ssm_number+'", "'+aps_address1+'", "'+aps_city+'", "'+aps_mobile_number+'", "'+aps_old_ssm_number+'", "'+aps_address2+'", "'+aps_state+'", "'+aps_email+'", "'+aps_license_no+'", "'+aps_address3+'", "'+aps_license_exp_date+'", "'+aps_contact_person+'", "'+employer_company_name+'", "'+employer_new_ssm_number+'", "'+employer_old_ssm_number+'", "'+employer_address1+'", "'+employer_address2+'", "'+employer_address3+'", "'+employer_postcode+'", "'+employer_city+'", "'+employer_state+'", "'+employer_office_telephone_no+'", "'+employer_mobile_no+'", "'+employer_fax_number+'", "'+employer_year_of_commence+'", "'+employer_sector+'", "'+employer_name_of_person_in_charge+'", "'+employer_designation+'", "'+employer_pic_mobile_number+'", "'+branch_employment_location_name+'", "'+branch_address1+'", "'+branch_address2+'", "'+branch_address3+'", "'+branch_postcode+'", "'+branch_state+'", "'+branch_city+'", "'+branch_office_telephone_number+'", "'+branch_office_mobile_number+'", "'+branch_email+'", "'+branch_name_of_person_in_charge+'", "'+branch_designation+'", "'+branch_pic_mobile_number+'")')
                    mysql.connection.commit()
                    cursor.close()  
                    session['profile_success'] = 'success'
                    return redirect('/profile') 
                except Exception as e:
                    print(e)
                    session['profile_error'] = 'error'
                    return redirect('/profile')
        # end the profile check
    else:
        return redirect('/')


# Profile    
@app.route("/edit-profile", methods=['GET', 'POST'])
def editProfile():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM profile")
        profile = cur.fetchall()
        return render_template('edit-profile.html', profileData = profile)
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
                
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE profile SET aps_agency_pekerjaan="'+aps_agency_pekerjaan+'", aps_license_category="'+aps_license_category+'", aps_postcode="'+aps_postcode+'", aps_office_telephone_no="'+aps_office_telephone_no+'", aps_new_ssm_number="'+aps_new_ssm_number+'", aps_address1="'+aps_address1+'", aps_city="'+aps_city+'", aps_mobile_number="'+aps_mobile_number+'", aps_old_ssm_number="'+aps_old_ssm_number+'", aps_address2="'+aps_address2+'", aps_state="'+aps_state+'", aps_email="'+aps_email+'", aps_license_no="'+aps_license_no+'", aps_address3="'+aps_address3+'", aps_license_exp_date="'+aps_license_exp_date+'", aps_contact_person="'+aps_contact_person+'", employer_company_name="'+employer_company_name+'", employer_new_ssm_number="'+employer_new_ssm_number+'", employer_old_ssm_number="'+employer_old_ssm_number+'", employer_address1="'+employer_address1+'", employer_address2="'+employer_address2+'", employer_address3="'+employer_address3+'", employer_postcode="'+employer_postcode+'", employer_city="'+employer_city+'", employer_state="'+employer_state+'", employer_office_telephone_no="'+employer_office_telephone_no+'", employer_mobile_no="'+employer_mobile_no+'", employer_fax_number="'+employer_fax_number+'", employer_year_of_commence="'+employer_year_of_commence+'", employer_sector="'+employer_sector+'", employer_name_of_person_in_charge="'+employer_name_of_person_in_charge+'", employer_designation="'+employer_designation+'", employer_pic_mobile_number="'+employer_pic_mobile_number+'", branch_employment_location_name="'+branch_employment_location_name+'", branch_address1="'+branch_address1+'", branch_address2="'+branch_address2+'", branch_address3="'+branch_address3+'", branch_postcode="'+branch_postcode+'", branch_state="'+branch_state+'", branch_city="'+branch_city+'", branch_office_telephone_number="'+branch_office_telephone_number+'", branch_office_mobile_number="'+branch_office_mobile_number+'", branch_email="'+branch_email+'", branch_name_of_person_in_charge="'+branch_name_of_person_in_charge+'", branch_designation="'+branch_designation+'", branch_pic_mobile_number="'+branch_pic_mobile_number+'" WHERE id="'+profile_id+'"')
                mysql.connection.commit()
                cursor.close()  
                session['edit_profile_success'] = 'success'
                return redirect('/edit-profile') 
            except Exception as e:
                print(e)
                session['edit_profile_error'] = 'error'
                return redirect('/edit-profile')
    else:
        return redirect('/')

# Upload Worker Avatar
@app.route("/upload-image", methods=['GET', 'POST'])
def uploadAvatar():
    res = {}
    avatarPath = 'static/img/uploaded-image/'
    avatar = request.files['avatar']
    avatar.save(avatarPath+avatar.filename) 
    print(avatar)
    res['status'] = 'success'
    return (jsonify(res))


# Document link image view
@app.route("/view-img", methods=['GET'])
def imgView():
    img = request.args.get('doc')
    return render_template('view-img.html', viewImg=img)


@app.route("/export-form-to-excel", methods=['GET', 'POST'])
def exportExcel():
    if 'username' in session:
        cur = mysql.connection.cursor()
        totalWorker = cur.execute("SELECT id, form_worker_reg_no, worker_detail_name_of_worker FROM half_form")
        workerD = cur.fetchall()
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



@app.route('/download-excel-file', methods=['GET'])
def download_log():
    cur = mysql.connection.cursor()
    cur.execute("SELECT form_worker_reg_no, worker_detail_name_of_worker FROM half_form")
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
    response.headers.set("Content-Disposition", "attachment", filename="log.csv")
    return response






# registration-log  
@app.route("/registration-log", methods=['GET', 'POST'])
def registrationLog():
    if 'username' in session:
        cur = mysql.connection.cursor()
        currentDate = datetime.datetime.now()
        cDate = str(currentDate.day)+"/"+str(currentDate.month)+"/"+str(currentDate.year)

        print(cDate)

        regNumber1 = cur.execute('SELECT * FROM half_form')
        regNumber2 = cur.execute('SELECT * FROM family_form')
        regNumber = regNumber1+regNumber2
        memberReg = cur.execute("SELECT * FROM family_form")

        totalWorker = cur.execute('SELECT * FROM half_form') 

        totalLegal = cur.execute('SELECT * FROM half_form where worker_detail_worker_legal_status="legal"') 

        totalIllegal = cur.execute('SELECT * FROM half_form where worker_detail_worker_legal_status="illegal"')
        
        return render_template('registration-log.html', regNumber=regNumber, memberReg=memberReg, totalWorker=totalWorker, totalLegal=totalLegal, totalIllegal=totalIllegal, grandTotal=regNumber)
    else:
        return redirect('/')


# Print QR Code
@app.route("/print-qr-code", methods=['GET', 'POST'])
def printQrCode():
    if 'username' in session:
        cur = mysql.connection.cursor()
        totalWorker = cur.execute("SELECT id, form_worker_reg_no, worker_detail_name_of_worker, form_status FROM half_form")
        workerD = cur.fetchall()
        return render_template('print-qr-code.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')
    

# Worker Details
@app.route("/worker-details", methods=['GET', 'POST'])
def workerDetails():
    if 'username' in session:
        workerId = request.args.get('wrkr')
        cur = mysql.connection.cursor()
        totalWorker = cur.execute("SELECT id, form_worker_reg_no, worker_detail_name_of_worker, worker_detail_gender, worker_detail_DOB, worker_detail_place_birth, worker_detail_citizenship, worker_detail_marital_status, worker_detail_poe, worker_detail_religion, worker_detail_race, worker_detail_contact_no, worker_emp_dtl_address1, worker_emp_dtl_address2, worker_emp_dtl_address3, worker_emp_dtl_postcode, worker_emp_dtl_city, worker_emp_dtl_state form_status FROM half_form where id='"+workerId+"'")
        workerD = cur.fetchall()
        return render_template('worker-details.html', workerList = workerD, totalForm=totalWorker)
    else:
        return redirect('/')
    

# Print QR
@app.route("/print-qr", methods=['GET', 'POST'])
def printQr():
    if 'username' in session:
        workerName = request.args.get('name')
        workerRegNum = request.args.get('regN')
        return render_template('print-qr.html', workerName=workerName, workerRegNum=workerRegNum)
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


#app.run(host='127.0.0.1', port=5010, debug=True)

webview.start()