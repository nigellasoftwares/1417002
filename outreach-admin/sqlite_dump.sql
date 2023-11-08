PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE student (name TEXT,     addr TEXT, city TEXT, pin TEXT);
CREATE TABLE students (name TEXT,     addr TEXT, city TEXT, pin TEXT);
INSERT INTO students VALUES('Arun','fghrh','dfgdf','dfgf');
INSERT INTO students VALUES('Arun','ojoij','ojoij','oijo');
INSERT INTO students VALUES('njnkj','njknjk','njkn','jkn');
INSERT INTO students VALUES('John','lko','lko','vjidvi');
INSERT INTO students VALUES('hello','Addres','City new john','DEFKDFJVNKNkf');
CREATE TABLE posts (title TEXT,         content TEXT);
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
INSERT INTO posts VALUES('First Post','Content for the first post');
INSERT INTO posts VALUES('Second Post','Content for the second post');
CREATE TABLE `category_list` (
  `id` int NOT NULL,
  `categories` varchar(255) NOT NULL
);
INSERT INTO category_list VALUES(1,'License Category');
INSERT INTO category_list VALUES(2,'City');
INSERT INTO category_list VALUES(3,'State');
INSERT INTO category_list VALUES(4,'Sector');
INSERT INTO category_list VALUES(5,'Gender');
INSERT INTO category_list VALUES(6,'Citizenship');
INSERT INTO category_list VALUES(7,'Maritial Status');
INSERT INTO category_list VALUES(8,'Point of Entry');
INSERT INTO category_list VALUES(9,'Religion');
INSERT INTO category_list VALUES(10,'Race');
INSERT INTO category_list VALUES(11,'Relationship');
INSERT INTO category_list VALUES(12,'Job Sector');
INSERT INTO category_list VALUES(13,'Job status&sponsor');
INSERT INTO category_list VALUES(14,'Job Status');
INSERT INTO category_list VALUES(15,'Document Status');
INSERT INTO category_list VALUES(16,'Country of issued document');
INSERT INTO category_list VALUES(17,'Current Status of document');
INSERT INTO category_list VALUES(18,'Is dependent together');
INSERT INTO category_list VALUES(19,'Type of document');
INSERT INTO category_list VALUES(21,'Employment Status');
INSERT INTO category_list VALUES(22,'Worker legal Status');
INSERT INTO category_list VALUES(23,'Designation');
INSERT INTO category_list VALUES(24,'Job Sub Sector');
CREATE TABLE `detailed_dd_doc_status` (
  `id` int NOT NULL,
  `doc_status` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
);
INSERT INTO detailed_dd_doc_status VALUES(1,'Sah','Document Status','1');
INSERT INTO detailed_dd_doc_status VALUES(5,'Tidak sah','Document Status','gmiti');
INSERT INTO detailed_dd_doc_status VALUES(6,'Tamat tempoh','Document Status','mpi^^');
INSERT INTO detailed_dd_doc_status VALUES(8,'Tamat tempoh (Diperbaharui)','Document Status','kq[c[');
INSERT INTO detailed_dd_doc_status VALUES(9,'Tidak diperakui','Document Status','owxgy');
INSERT INTO detailed_dd_doc_status VALUES(10,'Permohonan baru','Document Status','jfpa^');
INSERT INTO detailed_dd_doc_status VALUES(11,'Permohonan baru(Regu)','Document Status','f[]]k');
INSERT INTO detailed_dd_doc_status VALUES(12,'Tiada','Document Status','skxbx');
CREATE TABLE `detailed_dd_is_dependent_together` (
  `id` int NOT NULL,
  `is_dep_together` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
);
INSERT INTO detailed_dd_is_dependent_together VALUES(4,'Ya','Is dependent together','`lhlk');
INSERT INTO detailed_dd_is_dependent_together VALUES(5,'Tidak','Is dependent together','oemc_');
CREATE TABLE `detailed_dd_job_status_sponsor` (
  `id` int NOT NULL,
  `job_status_sponser` varchar(255) NOT NULL,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL
);
INSERT INTO detailed_dd_job_status_sponsor VALUES(7,'Majikan','Job status&sponsor','m[rfk');
INSERT INTO detailed_dd_job_status_sponsor VALUES(8,'Sendiri','Job status&sponsor','sulpu');
CREATE TABLE `form_image` (
  `id` int NOT NULL,
  `image_email` varchar(255) NOT NULL,
  `image_path` varchar(255) NOT NULL,
  `image_store_date` varchar(255) NOT NULL,
  `image_store_time` varchar(255) NOT NULL,
  `form_unique_key` varchar(255) NOT NULL
);
INSERT INTO form_image VALUES(1,'image_email','image_path','image_store_date','image_store_time','form_unique_key');
INSERT INTO form_image VALUES(2,'image_email','image_path','image_store_date','image_store_time','form_unique_key1');
CREATE TABLE `form_worker_registration_no` (
  `id` int NOT NULL,
  `worker_email` varchar(255) NOT NULL,
  `worker_no` varchar(255) NOT NULL,
  `worker_no_reg_date` varchar(255) NOT NULL,
  `worker_no_reg_time` varchar(255) NOT NULL
);
INSERT INTO form_worker_registration_no VALUES(1,'amsonlyfarhan19@gmail.com','W000001','17-03-2023','06:36');
INSERT INTO form_worker_registration_no VALUES(2,'nigellainfotech.com@gmail.com','W000001','18-03-2023','12:34');
INSERT INTO form_worker_registration_no VALUES(3,'yeoh.2007@gmail.com','W000001','30-03-2023','03:49');
CREATE TABLE `full_form` (
  `id` int NOT NULL,
  `form_id` varchar(255) NOT NULL,
  `created_by` varchar(255) NOT NULL,
  `created_time` varchar(255) NOT NULL,
  `completed_at` varchar(255) NOT NULL,
  `form_status` varchar(255) NOT NULL,
  `form_made_on_platform` varchar(255) NOT NULL,
  `form_fill_start_time` varchar(255) NOT NULL,
  `form_fill_end_time` varchar(255) NOT NULL,
  `form_fill_date_start` varchar(255) NOT NULL,
  `form_fill_date_end` varchar(255) NOT NULL,
  `form_last_fill_position` varchar(255) NOT NULL,
  `is_aps_completed` varchar(255) NOT NULL,
  `is_add_employer_completed` varchar(255) NOT NULL,
  `is_add_branch_loc_completed` varchar(255) NOT NULL,
  `is_add_worker_list_completed` varchar(255) NOT NULL,
  `is_add_dependent_completed` varchar(255) NOT NULL,
  `agensi_pekerjaan_aps` varchar(255) NOT NULL,
  `license_category_aps` varchar(255) NOT NULL,
  `postcode_aps` varchar(255) NOT NULL,
  `office_telephone_no_aps` varchar(255) NOT NULL,
  `new_ssm_number_aps` varchar(255) NOT NULL,
  `address_1_aps` varchar(255) NOT NULL,
  `city_aps` varchar(255) NOT NULL,
  `mobile_number_aps` varchar(255) NOT NULL,
  `old_ssm_number_aps` varchar(255) NOT NULL,
  `address_2_aps` varchar(255) NOT NULL,
  `state_aps` varchar(255) NOT NULL,
  `email_aps` varchar(255) NOT NULL,
  `aps_license_no` varchar(255) NOT NULL,
  `address_3_aps` varchar(255) NOT NULL,
  `license_expr_date_aps` varchar(255) NOT NULL,
  `contact_person_aps` varchar(255) NOT NULL,
  `company_name_employer` varchar(255) NOT NULL,
  `new_ssm_number_employer` varchar(255) NOT NULL,
  `old_ssm_number_employer` varchar(255) NOT NULL,
  `address_1_employer` varchar(255) NOT NULL,
  `address_2_employer` varchar(255) NOT NULL,
  `address_3_employer` varchar(255) NOT NULL,
  `postcode__employer` varchar(255) NOT NULL,
  `city_employer` varchar(255) NOT NULL,
  `state_employer` varchar(255) NOT NULL,
  `office_telephone_no_employer` varchar(255) NOT NULL,
  `mobile_no_employer` varchar(255) NOT NULL,
  `fax_no_employer` varchar(255) NOT NULL,
  `yr_of_buss_comm_employer` varchar(255) NOT NULL,
  `sector_employer` varchar(255) NOT NULL,
  `name_of_pes_incharge_employer` varchar(255) NOT NULL,
  `designation_employer` varchar(255) NOT NULL,
  `pic_mob_no_employer` varchar(255) NOT NULL,
  `employment_loc_name_location` varchar(255) NOT NULL,
  `address_1_location` varchar(255) NOT NULL,
  `address_2_location` varchar(255) NOT NULL,
  `address_3_location` varchar(255) NOT NULL,
  `postcode_location` varchar(255) NOT NULL,
  `state_location` varchar(255) NOT NULL,
  `city_location` varchar(255) NOT NULL,
  `office_telephpone_no_location` varchar(255) NOT NULL,
  `office_mob_no_location` varchar(255) NOT NULL,
  `email_location` varchar(255) NOT NULL,
  `name_of_pers_incharge_location` varchar(255) NOT NULL,
  `designation_location` varchar(255) NOT NULL,
  `pic_mob_no_location` varchar(255) NOT NULL,
  `name_of_worker_WorkerList` varchar(255) NOT NULL,
  `family_name_WorkerList` text NOT NULL,
  `gender_WorkerList` text NOT NULL,
  `d_o_b_WorkerList` text NOT NULL,
  `place_of_birth_WorkerList` text NOT NULL,
  `citizenship_WorkerList` text NOT NULL,
  `maritial_status_WorkerList` text NOT NULL,
  `p_o_e_WorkerList` text NOT NULL,
  `religion_WorkerList` text NOT NULL,
  `race_WorkerList` text NOT NULL,
  `worker_contact_no_WorkerList` text NOT NULL,
  `worker_email_WorkerList` text NOT NULL,
  `nok__WorkerList` text NOT NULL,
  `relationship_WorkerList` text NOT NULL,
  `nok_contact_no_WorkerList` text NOT NULL,
  `job_sector_employmentdetails` text NOT NULL,
  `job_sub_sector_employmentdetails` text NOT NULL,
  `job_status_sponsor_employmentdetails` text NOT NULL,
  `address1_employmentdetails` text NOT NULL,
  `address2_employmentdetails` text NOT NULL,
  `address3_employmentdetails` text NOT NULL,
  `postcode_employmentdetails` text NOT NULL,
  `city_employmentdetails` text NOT NULL,
  `state_employmentdetails` text NOT NULL,
  `document_id_doc_details` text NOT NULL,
  `type_of_doc_doc_details` text NOT NULL,
  `doc_img_doc_details` text NOT NULL,
  `place_of_issue_doc_details` text NOT NULL,
  `doc_issued_date_doc_details` text NOT NULL,
  `doc_exp_date_doc_details` text NOT NULL,
  `country_of_issuing_doc_doc_details` text NOT NULL,
  `doc_status_doc_details` text NOT NULL,
  `status_of_current_doc_doc_details` text NOT NULL,
  `document_no_doc_details` text NOT NULL,
  `worker_name_family_member` text NOT NULL,
  `relationship_family_member` text NOT NULL,
  `name_of_family_member` text NOT NULL,
  `family_name_family_member` text NOT NULL,
  `is_family_member_together_family_member` text NOT NULL,
  `poe_family_member` text NOT NULL,
  `citizenship_family_member` text NOT NULL,
  `religion_family_member` text NOT NULL,
  `maritial_status_family_member` text NOT NULL,
  `gender_family_member` text NOT NULL,
  `address_1_family_member` text NOT NULL,
  `address_2_family_member` text NOT NULL,
  `address_3_family_member` text NOT NULL,
  `postcode_family_member` text NOT NULL,
  `city_family_member` text NOT NULL,
  `state_family_member` text NOT NULL,
  `contact_no_family_member` text NOT NULL,
  `race_family_member` text NOT NULL,
  `place_of_birth_family_member` text NOT NULL,
  `emplyement_status_family_member` text NOT NULL,
  `employement_name_family_member` text NOT NULL,
  `employement_address_family_member` text NOT NULL
);
INSERT INTO full_form VALUES(1,'swims-bio-111','amsonlyfarhan19@gmail.com','05:58','27-02-2023','filling','android','05:58','','27-02-2023','','1/2','yes','no','no','no','no','demo name','License A','226020','05226525140','123456','tedhi pulia ring road','lucknow','9795331109','098786','tedhi pulia ring road','uttar pradesh','mohdfarhantahir@gmail.com','1417','tedhi pulia ring road','22-02-2025','9839076240','nigella softwares','1417','42342','tedhi pulia ring road','tedhi pulia ring road','tedhi pulia ring road','226020','lko','up','0522-897989','9839271417','055-2222','2023','plantation','yeoh em ling','suervisor','99799989','lko','tedhi pulia ring road','tedhi pulia ring road','tedhi pulia ring road','226020','up','lko','0633431','3425443','someemail@demo.com','syaiful','malaysia','+61-224242-24242','demo name','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','');
INSERT INTO full_form VALUES(2,'swims-bio-222','Mohd Rais Siddiqui','04:42','01-03-2023','Completed','Windows','04:43','NA','01-03-2023','NA','1/4','NA','NA','NA','NA','NA','mohd rais','plantation','226021','0522-6525140','0001111','my address 1','my city','000000000','11111111','my address 2','lucknow','raissiddqiui721@gmail.com','1234456678','my address 3','02-03-2025','9898989898','000000099999','121212121','12213312312','my address 1 emp','my address 2 emp','my adddress 3 emp','776767','lucknow','uttar pradesh','0522-121212','9909090909','','','','','','','','','','','','','','','','','','','','Mohd Rais','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','');
INSERT INTO full_form VALUES(3,'swims-bio-333','some random','05:29','NA','NA','','','','','','','','','','','','yeoh','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','yeoh','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','');
INSERT INTO full_form VALUES(131,'1231wq1q12323','Mohd Farhan Tahir 12','01:45','NA','pending','android','01:46','NA','04-03-2023','NA','APS','No','No','No','No','No','NiGELLA SOFTWARES','checking','22222','0522-232323','98232323','tedhi puliya','lko','999999','ewrr','NiGELLA SOFTWARES 1','NiGELLA SOFTWARES 2','NiGELLA SOFTWARES 3','NiGELLA SOFTWARES 4','NiGELLA SOFTWARES 5','NiGELLA SOFTWARES 6','NiGELLA SOFTWARES 7','NiGELLA SOFTWARES 8','NiGELLA SOFTWARES 9','NiGELLA SOFTWARES 10','NiGELLA SOFTWARES 12','NiGELLA SOFTWARES 13','NiGELLA SOFTWARES 14','NiGELLA SOFTWARES 15','NiGELLA SOFTWARES 16','NiGELLA SOFTWARES 17','NiGELLA SOFTWARES 18','NiGELLA SOFTWARES 19','NiGELLA SOFTWARES 20','NiGELLA SOFTWARES 21','NiGELLA SOFTWARES 22','NiGELLA SOFTWARES 23','NiGELLA SOFTWARES 24','NiGELLA SOFTWARES 25','NiGELLA SOFTWARES 26','NiGELLA SOFTWARES 27','NiGELLA SOFTWARES 28','NiGELLA SOFTWARES 29','NiGELLA SOFTWARES 30','NiGELLA SOFTWARES 31','NiGELLA SOFTWARES 32','NiGELLA SOFTWARES 33','NiGELLA SOFTWARES 34','NiGELLA SOFTWARES 35','NiGELLA SOFTWARES 36','dsdsd','dsdswewew','sds','postmane 14','postmane 13','postmane 12','postmane 11','postmane 10','postmane 9','postmane 8','postmane 7','postmane 6','postmane 5','postmane 4','postmane 3','postmane 2','postmane 1','POSTMAN 1','POSTMAN 2','POSTMAN 3','POSTMAN 4','POSTMAN 5','POSTMAN 6','POSTMAN 7','POSTMAN 8','POSTMAN 9','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','');
INSERT INTO full_form VALUES(132,'1231wq1q123231212','Mohd Farhan Tahir 12','01:45','NA','pending','android','01:46','NA','04-03-2023','NA','APS','No','No','No','No','No','NiGELLA SOFTWARES','checking','22222','0522-232323','98232323','tedhi puliya','lko','999999','ewrr','NiGELLA SOFTWARES 1','NiGELLA SOFTWARES 2','NiGELLA SOFTWARES 3','NiGELLA SOFTWARES 4','NiGELLA SOFTWARES 5','NiGELLA SOFTWARES 6','NiGELLA SOFTWARES 7','NiGELLA SOFTWARES 8','NiGELLA SOFTWARES 9','NiGELLA SOFTWARES 10','NiGELLA SOFTWARES 12','NiGELLA SOFTWARES 13','NiGELLA SOFTWARES 14','NiGELLA SOFTWARES 15','NiGELLA SOFTWARES 16','NiGELLA SOFTWARES 17','NiGELLA SOFTWARES 18','NiGELLA SOFTWARES 19','NiGELLA SOFTWARES 20','NiGELLA SOFTWARES 21','NiGELLA SOFTWARES 22','NiGELLA SOFTWARES 23','NiGELLA SOFTWARES 24','NiGELLA SOFTWARES 25','NiGELLA SOFTWARES 26','NiGELLA SOFTWARES 27','NiGELLA SOFTWARES 28','NiGELLA SOFTWARES 29','NiGELLA SOFTWARES 30','NiGELLA SOFTWARES 31','NiGELLA SOFTWARES 32','NiGELLA SOFTWARES 33','NiGELLA SOFTWARES 34','NiGELLA SOFTWARES 35','NiGELLA SOFTWARES 36','dsdsd','dsdswewew','sds','postmane 14','postmane 13','postmane 12','postmane 11','postmane 10','postmane 9','postmane 8','postmane 7','postmane 6','postmane 5','postmane 4','postmane 3','postmane 2','postmane 1','POSTMAN 1','POSTMAN 2','POSTMAN 3','POSTMAN 4','POSTMAN 5','POSTMAN 6','POSTMAN 7','POSTMAN 8','POSTMAN 9','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','');
INSERT INTO full_form VALUES(133,'1231wq1q123231212-900','Mohd Farhan Tahir 12','01:45','NA','pending','android','01:46','NA','04-03-2023','NA','APS','No','No','No','No','No','NiGELLA SOFTWARES','checking','22222','0522-232323','98232323','tedhi puliya','lko','999999','ewrr','NiGELLA SOFTWARES 1','NiGELLA SOFTWARES 2','NiGELLA SOFTWARES 3','NiGELLA SOFTWARES 4','NiGELLA SOFTWARES 5','NiGELLA SOFTWARES 6','NiGELLA SOFTWARES 7','NiGELLA SOFTWARES 8','NiGELLA SOFTWARES 9','NiGELLA SOFTWARES 10','NiGELLA SOFTWARES 12','NiGELLA SOFTWARES 13','NiGELLA SOFTWARES 14','NiGELLA SOFTWARES 15','NiGELLA SOFTWARES 16','NiGELLA SOFTWARES 17','NiGELLA SOFTWARES 18','NiGELLA SOFTWARES 19','NiGELLA SOFTWARES 20','NiGELLA SOFTWARES 21','NiGELLA SOFTWARES 22','NiGELLA SOFTWARES 23','NiGELLA SOFTWARES 24','NiGELLA SOFTWARES 25','NiGELLA SOFTWARES 26','NiGELLA SOFTWARES 27','NiGELLA SOFTWARES 28','NiGELLA SOFTWARES 29','NiGELLA SOFTWARES 30','NiGELLA SOFTWARES 31','NiGELLA SOFTWARES 32','NiGELLA SOFTWARES 33','NiGELLA SOFTWARES 34','NiGELLA SOFTWARES 35','NiGELLA SOFTWARES 36','dsdsd','dsdswewew','sds','postmane 14','postmane 13','postmane 12','postmane 11','postmane 10','postmane 9','postmane 8','postmane 7','postmane 6','postmane 5','postmane 4','postmane 3','postmane 2','postmane 1','POSTMAN 1','POSTMAN 2','POSTMAN 3','POSTMAN 4','POSTMAN 5','POSTMAN 6','POSTMAN 7','POSTMAN 8','POSTMAN 9','POSTMAN 11','POSTMAN 12','POSTMAN 13','POSTMAN 14','POSTMAN 15','POSTMAN 16','POSTMAN 17','POSTMAN 18','POSTMAN 19','POSTMAN 20','POSTMAN 21','POSTMAN 22','POSTMAN 23','POSTMAN 24','POSTMAN 25','POSTMAN 26','POSTMAN 27','POSTMAN 28','POSTMAN 29','POSTMAN 30','POSTMAN 31','POSTMAN 32','POSTMAN 33','POSTMAN 34','POSTMAN 35','POSTMAN 36','POSTMAN 37','POSTMAN 38','POSTMAN 39','POSTMAN 40','POSTMAN 41','POSTMAN 42');
INSERT INTO full_form VALUES(145,'tvyfn','amsonlyfarhan19@gmail.com','4:56 PM','N/A','Started','Android','4:56 PM','N/A','09-03-2023','N/A','4/5','Yes','N/A','N/A','N/A','N/A','dfff','53','225','5525','555','fcggv','city 3','9795331125866','99988','ccc.    hhh','state!','dvvv','ghhbb','ghbbbb','fvbbb','hhh bhh j','ghhh','ghgh','55555','vbbbbbggggg','vvvvhgg','vvvvbbbvbbh','2586080','city 3','state!','ghhh','97953311090','ghhhh','ggggg','Pertanian','vbbhh','ghghh','979543223456678','ghhhhgghhh','ghhhgggg','bbbbb bhh','hhhhh hhh','999998','state!','city 1','85588','979533110899','dggg','gggg','ghh','97953311090','demo nameggg','gggg','PEREMPUAN','ghh','ggggg','Afghanistan','BUJANG','KOTA KINABALU','ISLAM','TIDA MAKLUMAT','979533110895','dfgg','vhghh','Suami','979533110665','Pertanian','hhh','Jaminan Majikah','hhhh','gggggg','gghhhh','66988','city 2','ada','X]G^Ti@wYTTT+?=>','Passport','/data/user/0/com.nigellaform.nigellafrom/cache/scaled_06a748f0-5ecc-408e-a2fa-774f6e4160045725904554953342162.jpg','tyyh','hhh','yyyy','Afghanistan','Passport','Passport','ghhhh','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A');
INSERT INTO full_form VALUES(146,'o^_xY','amsonlyfarhan19@gmail.com','5:18 PM','N/A','Started','Android','5:18 PM','N/A','09-03-2023','N/A','4/5','Yes','N/A','N/A','N/A','N/A','ghhh','58','2558','9966','2255','ghhh hhh','city 4','9795331109','258','ghhh','ada','fggg','ghh','gggg','ghyh','ghhh','gggg','gggg','6666','cvvv','fgggg','gygg','3633','city 1','ada','ghh','97953311098','ggg','tyy','Pertanian','gggg','tttt','97953311098','tyyh','tyyyy','yyyy','fgghgf','5588','ada','city 1','55588','979533110888','fgg','ccgf','gyyy','Oiouttrrffvv','fggvv','ghhh','LELAKI','gggg','yhyy','Afghanistan','BUJANG','KOTA KINABALU','ISLAM','TIDA MAKLUMAT','979533118550','fghhghgghhggfffddfffffffffffffff','ghgfdgg','Suami','9795331108505','Pertanian','ghgv','Jaminan Majikah','ggggggg','gggggg','gggggg','55588','city 1','ada','?yDi+glW%m@e5W1=','Marriage cerificate','/data/user/0/com.nigellaform.nigellafrom/cache/scaled_b7c5aaa0-685b-44e6-ae1e-b2c67ba19cc84090251206080213096.jpg','tggg','vhhg','ggggg','Afghanistan','Marriage cerificate','Marriage cerificate','hhhhhhh','hhhhh','Isteri','ghhh','bhhh','no 2','SABDAKAN','Australia','KRITIAN','BUJANG','PEREMPUAN','gggg','fgggg','gyggg','666588','city 3','ada','979655444444','MELAYU','yhhhh','Employment status 2','yuhhhg','ghgggg');
INSERT INTO full_form VALUES(147,'yel`x','amsonlyfarhan19@gmail.com','5:28 PM','N/A','Started','Android','5:28 PM','N/A','09-03-2023','N/A','4/5','Yes','N/A','N/A','N/A','N/A','agendi hjj','license @','2226820','0822655','36985','hello how are you?','city 1','9795331109','31248','my address 2 ','ada','email','577ni','&++( address 3 ','688 license no','contact person ','company name','new SSM number','369988','adreless 1','address 2\n\nhjjj','adreless 3 ','226650','city 2','ada','office telephone no','979533110899','fax no','yuii','Pertanian','name of person in charge ','designation ','979533110899','employment location name','address 1','address 2','address 23','3668','ada','city 4','97953656664','9869856943799','anmsm','nnnn','nnmnn','089899777930304','name of erolrr','jjjj','PEREMPUAN','hjjk','hjjj','Afghanistan','BUJANG','KOTA KINABALU','ISLAM','TIDA MAKLUMAT','98999855699885','ghbb','vhbbbnn hjjnn. hjjn. hj','Suami','566699999999999','Pertanian','hhjxjj','Jaminan Majikah','address 1 ','address 2 ','adreless 3 ','66999','city 2','state!',']AJ=[@pe[u#k@j=k','Marriage cerificate','/data/user/0/com.nigellaform.nigellafrom/cache/scaled_faae8b9d-3542-4b3b-bc2b-9d8c56a18fa37987443900892156566.jpg','bhbb','hj','yuuu','Australia','Marriage cerificate','Marriage cerificate','hjjj','worker namem','Suami','njdkmd','jjjk','no 2','KOTA KINABALU','Afghanistan','KRITIAN','BUJANG','LELAKI','address 1 ','address 2 ','address 3 ','55888','city 4','state!','9796331178899','MELAYU','hjjj','Employement status 1','bbbb','hhjjjj');
INSERT INTO full_form VALUES(148,'orwch','amsonlyfarhan19@gmail.com','6:08 PM','N/A','Started','Android','6:08 PM','N/A','09-03-2023','N/A','4/5','Yes','N/A','N/A','N/A','N/A','Tariq Masood','test 8','2558','9666','9666','ghggh','city 2','9898555555','6999','hhhjjj','state!','hhjj','uuiii','uijj','jikkk','hijkk','hjjjj','iioo','63','hhjjj','jijjj','uiik','3666','city 2','state!','jjjkk','jhjjjjjjjjjjjj','kkkkkk','jjjj','Pertanian','kkkkk','iiooo','jkkkkkjkjjjjjkkkk','jjjkkkk','jkkkkk','iiiiok','ioooo','33','state!','city 1','669999','99999999999999988','hhjjj','uiiii','ioopok','jjjjjjjjjjjjkkk','hhjjj','kikkkkk','LELAKI','kkkj','uuuuu','Australia','BERKAHWIN','SABDAKAN','KRITIAN','TIDA MAKLUMAT','999999999999996','ghjjj','hjjjjj','Suami','999999999999999','Pertanian','iiiii','Berkerja Sendiri','jjjjjk','iiiook','iooooko','66666','city 3','state!','k%K72N5oJ?Fi#CC@','Passport','/data/user/0/com.nigellaform.nigellafrom/cache/scaled_1dfd060b-ff5b-40f1-b357-47d27a92bfee564540287394040930.jpg','hjjjj','kkkk','uiiii','Australia','Passport','Passport','mmmkk','iiiii','Suami','jjkkk','iiioo','no 2','SABDAKAN','Australia','KRITIAN','BERKAHWIN','PEREMPUAN','jjkk','kkkkk','iopool','3','city 3','state!','jjjkkkkkkkkkkk','MELAYU','kooooooo','Employment status 2','iioo','kkkkkk');
INSERT INTO full_form VALUES(149,'kse[a','amsonlyfarhan19@gmail.com','6:31 PM','N/A','Started','Android','6:31 PM','N/A','09-03-2023','N/A','4/5','Yes','N/A','N/A','N/A','N/A','riyaz','test 7','3699','999','9999','my address ','city 3','9795331109','366','ghnnn','ada','son','hjjj','bnnnn','nnnn','nnnnnnnn','my company name ','hjn','699999999','bbnbb','bnnn','bnnn','6666','city 2','state!','bbbb','hhjjjjjjjjjjjjj','hhhn','nnn','Perladangan','bbnn','nnn','nnnnnnnnnhujvgg','bbbn','nnnn','nnnn','nnnn','9999','state!','city 1','999','9999995568559','vhbnn','bbbn','bbnn','bbnnhyxvnhcnm','bbnn','nnnn','PEREMPUAN','bnn','hhh','Afghanistan','BUJANG','KOTA KINABALU','ISLAM','TIDA MAKLUMAT','999856956855','gnnn','bbb','Suami','9985685688568','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A');
INSERT INTO full_form VALUES(150,'rcbwZ','amsonlyfarhan19@gmail.com','5:56 PM','N/A','Started','Android','5:56 PM','N/A','10-03-2023','N/A','4/5','Yes','N/A','N/A','N/A','N/A','aitraaz','test 15','225022','053358866','36988','alamat 1','city 2','052265280588','3688','alamat 2','state!','amsonlyfarhan19@gmail.com','no lesen aps','alamat 3','tarikh tamat lesen','orang yang boleh dihubungi','nama syarikat','no SSM baharu','280','alamat 1','alamat 2','alamat 3','25509','city 2','ada','no telefon pejabat','no telefon bimbit','no faxa','tarikh Mila operasi','Perladangan','nama pegawai','jawatan','no tel pegawi','nama syarikat ','alamat 1 ','alamat 2 ','alamat 3 ','poskod','state!','city 1','no telefon pejabat','no telefon bimbit','emel','nama pegawai ','jawatan','no tel pegawai','nama pekerja','nama keluaraga','LELAKI','16/02/1990','tempat lahir','Australia','BUJANG','KOTA KINABALU','ISLAM','TIDA MAKLUMAT','699836698055','emel pekerja','nama saudara','Isteri','nok hubungi no','Pertanian','sub sektor pekerjaan','Jaminan Majikah','alamat 1 ','alamat 2 ','alamat 3 ','poskod','city 2','state!','=/aaF?53^R6Gp^OR','Passport','/data/user/0/com.nigellaform.nigellafrom/cache/scaled_b9b7ce9d-2f80-4752-8ede-bd2f551eb2a18076600303082348458.jpg','tempat isu','tarikh dikeluarkan','tarikh luput dokumen','Australia','Passport','Passport','dokumen no','nama pekerja ','Isteri','nama ahki keluarga','nama keluaraga','yes 1','KOTA KINABALU','Afghanistan','ISLAM','BUJANG','LELAKI','alamat 2 ','alamat 2 ','alamat 3 ','poskod','city 2','state!','nombor perhubungan','TIDA MAKLUMAT','tempat lahir','Employement status 1','nama pekerjaan','alamat perkerjaan');
INSERT INTO full_form VALUES(151,'Y[tfj','amsonlyfarhan19@gmail.com','6:28 PM','N/A','Started','Android','6:28 PM','N/A','12-03-2023','N/A','3/5','Yes','N/A','N/A','N/A','N/A','mohd rais ','fefedf','226021','0522651890','369258','puraniya','city 2','9839076240','369525','baari enclave ','updated by mobile','raissiddiqui721@gmail.com','nig1416','tedhi puliya ','10/12/2024','Mr yeoh','NiGELLA SOFTWARES ','nig1417','9388','tedhi puliya ','n/a','n/a','226024','city 2','updated by mobile','05333678','9839271417','n/a','2024','sector 22','Mr mohd rais','co-owner','9839076420','n/a','n/a','n/a','n/a','n/a','updated by mobile','city 1','n/a','077567884777','n/a','n/a','n/a','9839078994','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A');
CREATE TABLE `profile_new` (
  `id` int NOT NULL,
  `is_profile_completed` varchar(255) NOT NULL,
  `profile_registered_email` varchar(255) NOT NULL,
  `profile_registered_password` varchar(255) NOT NULL,
  `profile_registration_date` varchar(255) NOT NULL,
  `device_status_online` varchar(255) NOT NULL,
  `user_status` varchar(255) NOT NULL,
  `platform` varchar(255) NOT NULL,
  `push_token` varchar(255) NOT NULL,
  `user_guid` varchar(255) NOT NULL,
  `aps_agensi_pekerjaan` varchar(255) NOT NULL,
  `aps_license_category` varchar(255) NOT NULL,
  `aps_new_ssm_no` varchar(255) NOT NULL,
  `aps_old_ssm_no` varchar(255) NOT NULL,
  `aps_licence_no` varchar(255) NOT NULL,
  `aps_lic_exp_date` varchar(255) NOT NULL,
  `aps_email` varchar(255) NOT NULL,
  `aps_address1` varchar(255) NOT NULL,
  `aps_address2` varchar(255) NOT NULL,
  `aps_address3` varchar(255) NOT NULL,
  `aps_postcode` varchar(255) NOT NULL,
  `aps_city` varchar(255) NOT NULL,
  `aps_state` varchar(255) NOT NULL,
  `aps_mobile_no` varchar(255) NOT NULL,
  `aps_office_tele_no` varchar(255) NOT NULL,
  `emp_company_name` varchar(255) NOT NULL,
  `emp_new_ssm_no` varchar(255) NOT NULL,
  `emp_old_ssm_no` varchar(255) NOT NULL,
  `emp_address1` varchar(255) NOT NULL,
  `emp_address2` varchar(255) NOT NULL,
  `emp_address3` varchar(255) NOT NULL,
  `emp_postcode` varchar(255) NOT NULL,
  `emp_city` varchar(255) NOT NULL,
  `emp_state` varchar(255) NOT NULL,
  `emp_office_tele_no` varchar(255) NOT NULL,
  `emp_mobile_no` varchar(255) NOT NULL,
  `emp_fax_no` varchar(255) NOT NULL,
  `emp_year_of_commence` varchar(255) NOT NULL,
  `emp_sector` varchar(255) NOT NULL,
  `emp_name_of_person_incharge` varchar(255) NOT NULL,
  `emp_designation` varchar(255) NOT NULL,
  `emp_pic_mobile_no` varchar(255) NOT NULL,
  `branch_emp_loc_name` varchar(255) NOT NULL,
  `branch_address1` varchar(255) NOT NULL,
  `branch_address2` varchar(255) NOT NULL,
  `branch_address3` varchar(255) NOT NULL,
  `branch_postcode` varchar(255) NOT NULL,
  `branch_state` varchar(255) NOT NULL,
  `branch_city` varchar(255) NOT NULL,
  `branch_office_tele_no` varchar(255) NOT NULL,
  `branch_office_mob_no` varchar(255) NOT NULL,
  `branch_email` varchar(255) NOT NULL,
  `branch_name_of_person_incharge` varchar(255) NOT NULL,
  `branch_designation` varchar(255) NOT NULL,
  `branch_pic_mob_no` varchar(255) NOT NULL
);
INSERT INTO profile_new VALUES(1,'Yes','amsonlyfarhan19@gmail.com','kata laun','','Online','','Android','eJQqhZCWRhCK5NpZnkTG-r:APA91bHS7FSuF_gsGYs3Whgk2ozYwhU_PguI53qSJk4FtJdeuJWrCY3aCwuZJ4MOw6--ihnpelDrLxycUe152tf2MOCIZjw2suXps-PdB_e-tnv9WGQzA4mhwrkr_1Dt_JhMc5_39LiN','/data/user/0/com.nigellaform.nigellafrom/cache/scaled_b88a5c26-cd71-418d-9b18-ff3deb82994f5622688721089142422.jpg','Yeoh nama agency pekerjaan ','sdsds','no SSM baharu yeoh','no SSM lama yeoh','no lesen aps yeoh','undefined','email Yeoh aps','alamat 1 aps yeoh','alamat 2 aps yeoh ','alamat 3 aps yeoh ','poskod aps yeoh ','city 2','updated by mobile','no telefon aps bimbit yeoh','no telefon pejabat aps yeoh ','mohd farhan','no SSM baharu majikan yeoh ','no SSM lama majikan yeoh ','alamat 1 majikan yeoh ','alamat 2 majikan yeoh ','alamat 3 majikan yeoh ','poskod majikan yeoh ','city 2','state!','no telefon pejabat majikan yeoh ','no telefon bimbit majikan yeoh ','no fax majikan yeoh ','tarikh mula operasi majikan yeoh ','sector 22','nama pegawai majikan yeoh ','jawatan majikan yeoh ','telefon bimbit pegawaip majikan yeoh ','nama syarikat cawangan yeoh','alamat 1 cawangan yeoh ','alamat 2 cawangan yeoh ','alamat 3 cawangan yeoh ','poskod cawangan yeoh ','state!','city 2','no telefon pejabat cawangan yeoh ','no telefon bimbit pejabat cawangan yeoh ','email cawangan yeoh ','nama pegawai cawangan yeoh ','jawatan cawangan yeoh ','no telefon bimbit pegawai cawangan yeoh ');
INSERT INTO profile_new VALUES(2,'Yes','nigellainfotech.com@gmail.com','yakeen','','Online','','Android','eJQqhZCWRhCK5NpZnkTG-r:APA91bG6BnFkKOcKxUdXn6hz3WcT-PC50FUml4jGkRf3u-nB2XYCABPdOsedJi1W-JQwsziwgPFR9okugfAvjKLyje09yr3FjSVtQHNIyzTo-ZAPnwiDL9h0ZqnkLigkkWN40evsVfny','/data/user/0/com.nigellaform.nigellafrom/cache/scaled_18c49f8b-cd22-4d75-bb7e-ac5b0d1ef7d73749634445620252892.jpg','ggg','sdsds','ghgg','ghhh','ghh','undefined','ghgg','yuhh','uuh','hhhh','ghg','city 2','updated by mobile','bbhhjjjjjjjjjjj','hhhh','Syaiful Bahri','hhhh','yhhh','yyyy','hhhh','yhhh','ggh','city 1','state!','hhhh','gggg','hhhhh','ggghhh','sector 3','gghhh','hhhh','ghhhh','hhhhh','yuyu','yuuuu','hjjj','hhjjh','updated by mobile','city 1','ccgg','cvvvv','vvggg','ffgfg','hhhhhh','fggggg');
INSERT INTO profile_new VALUES(3,'Yes','yeoh.2007@gmail.com','my password','','Online','','Android','eJQqhZCWRhCK5NpZnkTG-r:APA91bHS7FSuF_gsGYs3Whgk2ozYwhU_PguI53qSJk4FtJdeuJWrCY3aCwuZJ4MOw6--ihnpelDrLxycUe152tf2MOCIZjw2suXps-PdB_e-tnv9WGQzA4mhwrkr_1Dt_JhMc5_39LiN','/data/user/0/com.nigellaform.nigellafrom/cache/scaled_a7edc107-a8d4-4e56-b6a3-dba3ec7d54d21687703706219259048.jpg','yeoh','sdsds','yeoh','yeoh','yeoh','undefined','yeoh','yeoh','yeoh','yeoh','yeoh','city 2','updated by mobile','yeoh','yeoh','Yeoh Plantation','Yeoh 1','Yeoh 1','Yeoh 1','Yeoh 1','Yeoh 1','Yeoh 1','city 3','state!','Yeoh 1','Yeoh 1','Yeoh 1','Yeoh 1','sector 22','Yeoh 1','Yeoh 1','Yeoh 1','Yeoh 2','Yeoh 2','Yeoh 2','Yeoh 2','Yeoh 2','state!','city 1','Yeoh 2','Yeoh 2','Yeoh 2','Yeoh 2','Yeoh 2','Yeoh 2');
INSERT INTO profile_new VALUES(4,'No','rais19@gmail.com','2331','30-03-2023','Offline','','N/A','N/A','N/A','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','');
CREATE TABLE `profile` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `aps_agency_pekerjaan` varchar(255) NULL,
  `aps_license_category` varchar(255) NULL,
  `aps_postcode` varchar(255) NULL,
  `aps_office_telephone_no` varchar(20) NULL,
  `aps_new_ssm_number` varchar(255) NULL,
  `aps_address1` text NULL,
  `aps_city` varchar(255) NULL,
  `aps_mobile_number` varchar(20) NULL,
  `aps_old_SSM_number` varchar(20) NULL,
  `aps_address2` text NULL,
  `aps_state` varchar(255) NULL,
  `aps_email` varchar(100) NOT NULL UNIQUE,
  `aps_license_no` varchar(20) NULL,
  `aps_address3` text NULL,
  `aps_license_exp_date` varchar(20) NULL,
  `aps_contact_person` varchar(255) NULL,
  `employer_company_name` varchar(255) NULL,
  `employer_new_ssm_number` varchar(255) NULL,
  `employer_old_ssm_number` varchar(20) NULL,
  `employer_address1` text NULL,
  `employer_address2` text NULL,
  `employer_address3` text NULL,
  `employer_postcode` varchar(20) NULL,
  `employer_city` varchar(255) NULL,
  `employer_state` varchar(255) NULL,
  `employer_office_telephone_no` varchar(20) NULL,
  `employer_mobile_no` varchar(20) NULL,
  `employer_fax_number` varchar(20) NULL,
  `employer_year_of_commence` varchar(20) NULL,
  `employer_sector` varchar(255) NULL,
  `employer_name_of_person_in_charge` text NULL,
  `employer_designation` varchar(255) NULL,
  `employer_pic_mobile_number` varchar(20) NULL,
  `branch_employment_location_name` varchar(255) NULL,
  `branch_address1` text NULL,
  `branch_address2` text NULL,
  `branch_address3` text NULL,
  `branch_postcode` varchar(20) NULL,
  `branch_state` varchar(255) NULL,
  `branch_city` varchar(255) NULL,
  `branch_office_telephone_number` varchar(20) NULL,
  `branch_office_mobile_number` varchar(20) NULL,
  `branch_email` varchar(100) NULL,
  `branch_name_of_person_in_charge` varchar(255) NULL,
  `branch_designation` varchar(255) NULL,
  `branch_pic_mobile_number` varchar(20) NULL
);
INSERT INTO profile VALUES(1,'bjbj','B','jh','jbh','jb','hjb','Bongawan','9009009000','jhb','hj','Sabah','john@g','b','bhjb','2023-09-07','Contact Person',' Nigella Softwares Pvt Ltd','bhj','bh','jbhj','bj','hb','jhb','Beluran','Sabah','hjb','hjb','hjb','hj','Berorientasi Eksport','bh','1231231','hjb','hjb','hjb','jb','jhb','jhb','Sabah','Beaufort','bhj','none','bhj@fd','bjb','my designation','pic num');
INSERT INTO profile VALUES(2,'Swims','A','000000','900000000','Swims','Swims add1','Nabawan','Swims pic','Swims','Swims add2','Sabah','swims@user','Swims','Swims add3','2023-09-08','90000000000','Swims Form','099099','9909','Swims Emp. add 1','Swims Emp. add2','Swims Emp. add 3','90000','Papar','Sabah','99000900000','90000000000','89900','2023','Restoran','pic','my designation','9000000090000','LKO','Swims Branch Add 1','Swims Branch Add 2','Swims Branch Add 3','000000','Sabah','Lamag','00000900000','none','Swims@Branch','branch pic','my designation','90009000000');
INSERT INTO profile VALUES(3,'tata pvt','Category one','2260','0522-777777777','1417500','address employment agency 1','Kudat','ratan tata','1417100','address employment agency 2','Sabah','alex@gmail.com','up32','address employment agency 3','2023-09-30','77777777','tata docomo','202020','1111','register emp add 1','register emp add 2','register emp add 3','2260','Kunak','Sabah','0522-763686','9889987657','022','5','Pembinaan','ranjeet','Designation 1','9839271417','tata indicom ','branch add 1','branch add 2','branch add 3','2245','Sabah','Likas','0522-765645','none','demo@gmail.com','demo name','Designation 2','9839076240');
INSERT INTO profile VALUES(4,'uyt','Category one','tuy','9800089000','tuy009','uyt','Kota Marudu','MoxPiC','tuy','uy','Sabah','mox@gmail.com','tyu898','tuy','2023-09-30','10000100010','tyu','tyu','tuy','tuy','tuy','tuy','t','Bongawan','Sabah','uyt','ut','uyt','uy','Perladangan','MoxPiC2','Designation 1','88800008990','fghf LKO','ghf','ghf','hgf','ghf90','Sabah','Nabawan','55575756','none','mox@mos.com','MoxPiC3','Designation 1','870007899');
INSERT INTO profile VALUES(5,'Hit kj','Category one','bj','9909909900','jnjhb','hjb','Keningau','890089008900','jhbjhb','hjb','Sabah','hitman@gmail.com','hjbhjbjhb','hjbhj','2023-10-01','Hit PIC','bhj','bjhb','jhb','hjb','hjb','hjb','hjb','Beluran','Sabah','hjbhj','bhj','bhj','bjh','Pembinaan','bhj','Designation 1','bjhb','jh','bhj','bjh','b','jb','Sabah','Bongawan','jhb','none','jhb@oijhoi','jb','Designation 1','jhb');
CREATE TABLE `half_form` (
  `id` integer NOT NULL primary key AUTOINCREMENT,
  `worker_key` integer NOT NULL,
  `form_created_by` varchar(255) NOT NULL,
  `form_created_date` varchar(255) NOT NULL,
  `form_worker_reg_no` varchar(255) NOT NULL,
  `no_family_mem` varchar(255) NOT NULL,
  `worker_detail_worker_legal_status` varchar(255) NOT NULL,
  `worker_detail_name_of_worker` varchar(255) NOT NULL,
  `worker_detail_family_name` varchar(255) NOT NULL,
  `worker_detail_gender` varchar(255) NOT NULL,
  `worker_detail_DOB` varchar(255) NOT NULL,
  `worker_detail_place_birth` varchar(255) NOT NULL,
  `worker_detail_citizenship` varchar(255) NOT NULL,
  `worker_detail_marital_status` varchar(255) NOT NULL,
  `worker_detail_poe` varchar(255) NOT NULL,
  `worker_detail_religion` varchar(255) NOT NULL,
  `worker_detail_race` varchar(255) NOT NULL,
  `worker_detail_contact_no` varchar(255) NOT NULL,
  `worker_detail_email` varchar(255) NOT NULL,
  `worker_detail_nok` varchar(255) NOT NULL,
  `worker_detail_relationship` varchar(255) NOT NULL,
  `worker_detail_nok_contact_no` varchar(255) NOT NULL,
  `worker_emp_dtl_job_sector` varchar(255) NOT NULL,
  `worker_emp_dtl_job_sub_sector` varchar(255) NOT NULL,
  `worker_emp_dtl_emp_sponsorship_status` varchar(255) NOT NULL,
  `worker_emp_dtl_address1` varchar(255) NOT NULL,
  `worker_emp_dtl_address2` varchar(255) NOT NULL,
  `worker_emp_dtl_address3` varchar(255) NOT NULL,
  `worker_emp_dtl_postcode` varchar(255) NOT NULL,
  `worker_emp_dtl_city` varchar(255) NOT NULL,
  `worker_emp_dtl_state` varchar(255) NOT NULL,
  `worker_doc_dtl_doc_id` varchar(255) NOT NULL,
  `worker_doc_dtl_type_of_doc` varchar(255) NOT NULL,
  `worker_doc_dtl_no_of_doc` varchar(255) NOT NULL,
  `worker_doc_dtl_images_path_email` varchar(255) NOT NULL,
  `worker_doc_dtl_place_of_issue` varchar(255) NOT NULL,
  `worker_doc_dtl_issue_date` varchar(255) NOT NULL,
  `worker_doc_dtl_expiry_date` varchar(255) NOT NULL,
  `worker_doc_dtl_country_doc_issued` varchar(255) NOT NULL,
  `worker_doc_dtl_doc_status` varchar(255) NOT NULL,
  `worker_doc_dtl_doc_current_status` varchar(255) NOT NULL,
  `worker_doc_dtl_doc_no` varchar(255) NOT NULL,
  `form_position` varchar(255) NOT NULL,
  `form_status` varchar(255) NOT NULL,
  `form_unique_key` varchar(255) NOT NULL UNIQUE
);
INSERT INTO half_form VALUES(2,2,'john@g','08/09/2023','FW23NSPL000002','2','Illegal','Dev Nagar','bhhjb','Perempuan','2023-09-08','hjkh','Philippines','Bujang','Tawau','Buddha','Boyan','jhjhj','jhjhjhj@hhjj','hjjhj','Isteri','jhb','l_nwZ','Ladang Koko','Majikan','hjb','jb','jhb','postcode - static','Beluran','Sabah','document_id-123456','type_of_documents','static','static','static','static','static','static','static','static','static','static','static','DT08092023N94571');
INSERT INTO half_form VALUES(3,3,'swims@user','08/09/2023','FW23SF000003','0','Legal','Swims','Swims Family','Lelaki','2023-09-08','LKO','Philippines','Bercerai','Kota Kinabalu','Buddha','Melayu','900900990','swims@g','0','Isteri','0099898','dkhce','Tapak Semaian Lain','Majikan','Swims Branch Add 1','Swims Branch Add 2','Swims Branch Add 3','postcode - static','Bongawan','Sabah','document_id-123456','type_of_documents','static','static','static','static','static','static','static','static','static','static','static','DT08092023N28502');
INSERT INTO half_form VALUES(5,5,'john@g','20/09/2023','FW23NSPL000005','','Legal','oihh','oih','Lelaki','2023-09-20','hiu','Indonesia','Berkawhin','Kuala Sipitang','Hindu','Boyan','hiu','hih','ih','rel','hiu','Pembinaan','Job SS 1','Majikan','hiuhjb','hiujb','hijhb','postcode - static','Bongawan','Sabah','document_id-123456','type_of_documents','static','static','static','static','static','static','static','static','static','static','static','DT20092023N57962');
INSERT INTO half_form VALUES(6,6,'john@g','23/09/2023','FW23NSPL000006','','Legal','Test','Test','Lelaki','2023-09-23','Test','Indonesia','Bercerai','Kuala Sipitang','Buddha','Boyan','09','Test@d','0','rel','908890','Pembinaan','Job SS 1','Sendiri','hjb','jb','jhb','postcode - static','Beluran','Sabah','document_id-123456','type_of_documents','static','static','static','static','static','static','static','static','static','static','static','DT23092023N12409');
INSERT INTO half_form VALUES(7,7,'john@g','25/09/2023','FW23NSPL000007','','Legal','Joe','Devid','Lelaki','2023-09-25','LKO','Indonesia','Bercerai','Kota Kinabalu','Hindu','Bisaya','9000009000','joe@joe','1','rel','9009009000','Pembinaan','Job SS 1','Majikan','hjb','jb','jhb','postcode - static','Beluran','Sabah','document_id-123456','type_of_documents','static','static','static','static','static','static','static','static','static','static','static','DT25092023N74222');
INSERT INTO half_form VALUES(8,8,'john@g','25/09/2023','FW23NSPL000008','1','Legal','dfghgdf','bhhjb','Lelaki','2023-09-25','hjb','Indonesia','Bercerai','Kota Kinabalu','Islam','Bisaya','889','jb@df','jhbj','rel','jhb','Perkilangan','Job SS 3','Majikan','hjb','jb','jhb','postcode - static','Beaufort','Sabah','document_id-123456','type_of_documents','static','static','static','static','static','static','static','static','static','static','static','DT25092023N10041');
INSERT INTO half_form VALUES(10,10,'john@g','29/09/2023','FW23NSPL000010','','Legal','New WorX','ugu','Lelaki','2023-09-27','uyg','Indonesia','Berkawhin','Kuala Sipitang','Hindu','Bisaya','yu','guy','guy','rel','gyu','Pembinaan','Job SS 1','Sendiri','uyghjb','uygjb','yugjhb','postcode - static','Beaufort','Sabah','document_id-123456','type_of_documents','static','static','static','static','static','static','static','static','static','static','static','DT27092023N10860');
INSERT INTO half_form VALUES(11,11,'alex@gmail.com','30/09/2023','FW23TD000011','','Legal','WR 1','wrfamily name','Lelaki','2023-09-20','kotakinabalu','Indonesia','Bercerai','Kota Kinabalu','Buddha','Banjar','9999 88 9999','wr1@gmail.com','wrnok','rel','777 666 6677','Pembinaan','Job SS 2','Majikan','branch add 1','branch add 2','branch add 3','postcode - static','Kudat','Sabah','document_id-123456','type_of_documents','static','static','static','static','static','static','static','static','static','static','static','DT30092023N76094');
INSERT INTO half_form VALUES(12,12,'alex@gmail.com','30/09/2023','FW23TD000012','1','Legal','Arun','agarwal family','Perempuan','2000-02-01','lucknow','Philippines','Tinggal berasingan','Tawau','Kristian','Timor','9839 78 3456','arun@gmail.com','siraj','rel','98767 5 7777','Pertanian','Job SS 4','Sendiri','branch add 1','branch add 2','branch add 3','postcode - static','Kinabatangan','Sabah','document_id-123456','type_of_documents','static','static','static','static','static','static','static','static','static','static','static','DT30092023N62651');
INSERT INTO half_form VALUES(13,13,'alex@gmail.com','30/09/2023','FW23TD000013','1','Illegal','illegal wN','illegal Fn','Perempuan','2023-09-15','new basti ','Indonesia','Berkawhin','Kuala Sipitang','Hindu','Bisaya','67987','illegal@gmail.com','illegalNOK','rel','87808231434','Pembinaan','Job SS 1','Majikan','branch add 1','branch add 2','branch add 3','postcode - static','Lamag','Sabah','document_id-123456','type_of_documents','static','static','static','static','static','static','static','static','static','static','static','DT30092023N36210');
CREATE TABLE `workers_document` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `worker_key` integer NOT NULL,
  `document_link` varchar(255) DEFAULT NULL,
  `type_of_douments` varchar(255) DEFAULT NULL,
  `document_id` varchar(50) DEFAULT NULL,
  `place_of_issue` text,
  `document_issued_date` varchar(20) DEFAULT NULL,
  `document_expiry_date` varchar(20) DEFAULT NULL,
  `issuing_country` varchar(255) DEFAULT NULL,
  `document_status` varchar(255) DEFAULT NULL,
  `status_of_current_document` varchar(255) DEFAULT NULL,
  `form_unique_key` varchar(100) NOT NULL
);
INSERT INTO workers_document VALUES(3,2,'','Biodata Siswa','','LOKO','','','None','None','None','DT08092023N94571');
INSERT INTO workers_document VALUES(4,2,'','Formulir Peserta Didik','','Varanasi','','','None','None','None','DT08092023N94571');
INSERT INTO workers_document VALUES(5,3,'','Kartu TP','1212','','','',NULL,NULL,NULL,'DT08092023N28502');
INSERT INTO workers_document VALUES(6,3,'','PLS (Jaminan Suami)','900','','','',NULL,NULL,NULL,'DT08092023N28502');
INSERT INTO workers_document VALUES(9,5,'doc1','typ Doc','Adh0890','iu','2023-09-20','2023-09-20','test1','Tamat tempoh (Diperbaharui)','test','DT20092023N57962');
INSERT INTO workers_document VALUES(10,5,'doc2','typ Doc','PN9089','iuh','2023-09-20','2023-09-20','test1','Tidak sah','test','DT20092023N57962');
INSERT INTO workers_document VALUES(11,6,'doc1','typ Doc','','','','',NULL,'Tidak sah','test','DT23092023N12409');
INSERT INTO workers_document VALUES(12,7,'doc1','typ Doc','ID0090','VNS','2023-09-25','2023-09-25','test1','Sah','test','DT25092023N74222');
INSERT INTO workers_document VALUES(13,7,'doc2','typ Doc','NewIDo009','LKO','2023-09-25','2023-09-25','test1','Tidak sah','test','DT25092023N74222');
INSERT INTO workers_document VALUES(14,8,'doc1','typ Doc','909991','bhj','2023-09-25','2023-09-25','test1','Sah','test','DT25092023N10041');
INSERT INTO workers_document VALUES(15,8,'doc2','typ Doc','909991','bhj','2023-09-26','2023-09-13','test1','Sah','test','DT25092023N10041');
INSERT INTO workers_document VALUES(18,10,'doc1','typ Doc','uyg','uyg','2023-09-27','2023-09-27','test1','Tidak sah','test','DT27092023N10860');
INSERT INTO workers_document VALUES(19,10,'doc2','typ Doc','uyg','yu','2023-09-27','2023-09-27','test1','Tidak sah','test','DT27092023N10860');
INSERT INTO workers_document VALUES(20,11,'doc1','typ Doc','1417522','loo','2023-07-05','2023-09-21','test1','Tidak sah','test','DT30092023N76094');
INSERT INTO workers_document VALUES(21,11,'doc2','typ Doc','123','Manoj','2023-08-02','2023-11-10','test1','Sah','test','DT30092023N76094');
INSERT INTO workers_document VALUES(22,12,'doc1','typ Doc','151515','lkonew','2023-07-05','2023-09-30','test1','Tiada','test','DT30092023N62651');
INSERT INTO workers_document VALUES(23,12,'doc2','typ Doc','565656','lko','2023-03-10','2023-10-20','test1','Tiada','test','DT30092023N62651');
INSERT INTO workers_document VALUES(24,12,'doc3','typ Doc','787878','new lko','2023-02-10','2023-11-10','test1','Tidak diperakui','test','DT30092023N62651');
INSERT INTO workers_document VALUES(25,12,'doc4','typ Doc','65689','new a','2023-01-10','2023-09-08','test1','Tidak diperakui','test','DT30092023N62651');
INSERT INTO workers_document VALUES(26,12,'doc5','typ Doc','232323','lko','2022-10-10','2023-09-15','test1','Tidak diperakui','test','DT30092023N62651');
INSERT INTO workers_document VALUES(27,12,'doc6','typ Doc','989898','lko','2022-06-08','2023-10-12','test1','Permohonan baru','test','DT30092023N62651');
INSERT INTO workers_document VALUES(28,13,'doc1','typ Doc','3r453','sods','2023-09-01','2023-12-28','test1','Tidak sah','test','DT30092023N36210');
INSERT INTO workers_document VALUES(29,13,'doc2','typ Doc','890980','ko','2023-12-15','2023-09-08','test1','Tidak sah','test','DT30092023N36210');
CREATE TABLE `family_form` (
  `id` integer NOT NULL primary key autoincrement,
  `form_created_by` varchar(255) NOT NULL,
  `form_created_date` varchar(255) NULL,
  `form_unique_key` varchar(255) NOT NULL,
  `form_family_reg_no` varchar(255) NULL,
  `family_form_worker_name` varchar(255) NULL,
  `family_form_relationship` varchar(255) NULL,
  `family_form_name_of_family_member` varchar(255) NULL,
  `family_form_family_name` varchar(255) NULL,
  `family_form_is_famliy_togther` varchar(255) NULL,
  `family_form_family_form_poe` varchar(255) NULL,
  `family_form_citizenship` varchar(255) NULL,
  `family_form_religion` varchar(255) NULL,
  `family_form_marital_status` varchar(255) NULL,
  `family_form_gender` varchar(255) NULL,
  `family_form_address1` varchar(255) NULL,
  `family_form_address2` varchar(255) NULL,
  `family_form_address3` varchar(255) NULL,
  `family_form_postcode` varchar(255) NULL,
  `family_form_city` varchar(255) NULL,
  `family_form_state` varchar(255) NULL,
  `family_form_contact_no` varchar(255) NULL,
  `family_form_race` varchar(255) NULL,
  `family_form_place_of_birth` varchar(255) NULL,
  `family_form_emp_status` varchar(255) NULL,
  `family_form_emp_name` varchar(255) NULL,
  `family_form_emp_address` varchar(255) NULL,
  `family_form_doc_path_email` varchar(255) NULL,
  `family_form_doc_image_no` varchar(255) NULL,
  `worker_key` integer(11) NULL,
  `fmDoc1_type_of_documents` text,
  `fmDoc1_document_id` varchar(20) DEFAULT NULL,
  `fmDoc1_place_of_issue` varchar(20) DEFAULT NULL,
  `fmDoc1_document_issued_date` varchar(20) DEFAULT NULL,
  `fmDoc1_document_expiry_date` varchar(20) DEFAULT NULL,
  `fmDoc1_issuing_country` varchar(100) DEFAULT NULL,
  `fmDoc1_document_status` varchar(50) DEFAULT NULL,
  `fmDoc1_status_of_current_document` varchar(50) DEFAULT NULL,
  `fmDoc2_type_of_documents` text,
  `fmDoc2_document_id` varchar(20) DEFAULT NULL,
  `fmDoc2_place_of_issue` text,
  `fmDoc2_document_issued_date` varchar(20) DEFAULT NULL,
  `fmDoc2_document_expiry_date` varchar(20) DEFAULT NULL,
  `fmDoc2_issuing_country` varchar(150) DEFAULT NULL,
  `fmDoc2_document_status` varchar(50) DEFAULT NULL,
  `fmDoc2_status_of_current_document` varchar(50) DEFAULT NULL
);
INSERT INTO family_form VALUES(1,'john@g','29/09/2023','DT27092023N10860','FM23NSPL000001','dfghgdf','Isteri','nnkjn','dfgdf','yes','None','None','None','None','None','hjb','jb','jhb','','New City','None','','None','','None','','','static email','doc image- static',2,'None','','','','','None','None','None','None','','','','','None','None','None');
INSERT INTO family_form VALUES(2,'john@g','29/09/2023','DT27092023N10860','FM23NSPL000002','dfghgdf','Ayah','','','no','None','None','None','None','None','a 1','a2','a. 3','','F city','None','','None','','None','','','static email','doc image- static',2,'None','','lok.   oioi ','','','None','None','None','None','','ldfgfdlkj','','','None','None','None');
INSERT INTO family_form VALUES(3,'john@g','25/09/2023','DT27092023N10860','FM23NSPL000003','dfghgdf','rel','nnkjn','ZX','yes','Kota Kinabalu','Philippines','Islam','Bercerai','Lelaki','hjb','jb','jhb','224','Beluran','Sabah','7676','Banjar','6555','Tidak sah','dfghgdf','hjb','static email','doc image- static',8,'typ Doc','jh','bhj','2023-09-28','2023-08-30','test1','Sah','test','typ Doc','jh','bhj','2023-09-12','2023-09-28','test1','Sah','test');
INSERT INTO family_form VALUES(4,'alex@gmail.com','30/09/2023','DT30092023N62651','FM23TD000004','Arun','rel','arun ku','arun kumar','yes','Sandakan','Philippines','Islam','Tinggal berasingan','Lelaki','branch add 1','branch add 2','branch add 3','223','Inanam','Sabah','98989 6726','Timor','Kanpur','Sah/Aktif','77777777','branch add 1','static email','doc image- static',12,'typ Doc','121212','kan','2023-08-10','2023-09-28','test1','Tidak diperakui','test','typ Doc','414141','kan1','2023-08-09','2023-09-15','test1','Tiada','test');
INSERT INTO family_form VALUES(5,'alex@gmail.com','30/09/2023','DT30092023N36210','FM23TD000005','illegal wN','rel','illegalFamily mem','illegalFamily name','yes','Kuala Sipitang','Indonesia','Buddha','Berkawhin','Perempuan','branch add 1','branch add 2','branch add 3','e134243','Bongawan','Sabah','353453','Boyan','fsfsf','Tidak sah','77777777','branch add 1','static email','doc image- static',13,'typ Doc','232423','lko kaput','2023-09-01','2023-09-02','test1','Tidak sah','test','typ Doc','e21213123','ndewzead','2023-09-02','2023-09-09','test1','Tidak sah','test');
CREATE TABLE `users`(
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL UNIQUE,
  `password` varchar(255) NOT NULL,
  `device_status_online` varchar(255) NULL,
  `user_status` varchar(255) NULL,
  `created_at` varchar(255) NULL,
  `created_time` varchar(255) NULL,
  `worker_registration_prefix` varchar(500) NOT NULL UNIQUE
);
INSERT INTO users VALUES(1,'John New','john@g','123456',NULL,NULL,'11/09/2023','13:01:31','John Company');
INSERT INTO users VALUES(4,'Debid','debit@g','123456',NULL,NULL,'13/09/2023','16:31:33','Debit Com');
INSERT INTO users VALUES(5,'xRoot','x@root','123456',NULL,NULL,'26/09/2023','15:18:03','XRoot');
INSERT INTO users VALUES(6,'alex','alex@gmail.com','1234',NULL,NULL,'30/09/2023','19:53:08','FW23000001');
INSERT INTO users VALUES(7,'MoX','mox@gmail.com','12345',NULL,NULL,'30/09/2023','19:53:08','MoX Pvt Lmt');
INSERT INTO users VALUES(8,'Hitman','hitman@gmail.com','123',NULL,NULL,'01/10/2023','04:29:33','Hitman Products');
CREATE TABLE `admin` (
  `id` integer NOT NULL,
  `name` text NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(20) NOT NULL,
  `profile_path` text NULL,
  `last_signin` varchar(20) DEFAULT NULL,
  `last_signout` varchar(20) DEFAULT NULL,
  `session_time` varchar(30) DEFAULT NULL
);
INSERT INTO admin VALUES(1,'Admin O','admin@g','123456','static/img/admin/testing.avif',NULL,NULL,NULL);
CREATE TABLE `sub_admin` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL UNIQUE,
  `password` varchar(20) NOT NULL,
  `status` varchar(255) NULL,
  `created_at` varchar(255) NULL,
  `created_time` varchar(255) NULL,
  `profile_path` text NULL,
  `last_signin` varchar(50) DEFAULT NULL,
  `last_signout` varchar(50) DEFAULT NULL,
  `session_time` varchar(50) DEFAULT NULL
);
INSERT INTO sub_admin VALUES(1,'Sub Admin','sub@admin','123456','Active','15/09/2023','18:55:25','static/img/subAdmin/16092023236768_blank_profile.jpg',NULL,NULL,NULL);
CREATE TABLE `detailed_dd_city` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `city` varchar(255) NOT NULL UNIQUE,
  `category_list` varchar(255) NULL,
  `uuid` varchar(255) NULL
);
INSERT INTO detailed_dd_city VALUES(1,'Beaufort','City','uYc^y');
INSERT INTO detailed_dd_city VALUES(2,'Beluran','City','kYrce');
INSERT INTO detailed_dd_city VALUES(3,'Bongawan','City','[gwxf');
INSERT INTO detailed_dd_city VALUES(4,'Inanam','City','kbp\\f');
INSERT INTO detailed_dd_city VALUES(5,'Keningau','City','aiebu');
INSERT INTO detailed_dd_city VALUES(6,'Kota Belud','City','rZ_sY');
INSERT INTO detailed_dd_city VALUES(7,'Kota Kinabalu','City','Y[vyy');
INSERT INTO detailed_dd_city VALUES(8,'Kota Marudu','City','ud_je');
INSERT INTO detailed_dd_city VALUES(9,'Kuala Penyu','City','vg\\gY');
INSERT INTO detailed_dd_city VALUES(10,'Kudat','City','nclbn');
INSERT INTO detailed_dd_city VALUES(11,'Kunak','City','deswm');
INSERT INTO detailed_dd_city VALUES(12,'Lahad Datu','City','vb`pg');
INSERT INTO detailed_dd_city VALUES(13,'Lamag','City','d`y__');
INSERT INTO detailed_dd_city VALUES(14,'Likas','City','\\ymys');
INSERT INTO detailed_dd_city VALUES(15,'Membakut','City','gpi^n');
INSERT INTO detailed_dd_city VALUES(16,'Menumbok','City','Z`]hf');
INSERT INTO detailed_dd_city VALUES(17,'Nabawan','City','\\xxZd');
INSERT INTO detailed_dd_city VALUES(18,'Papar','City','sw^tc');
INSERT INTO detailed_dd_city VALUES(19,'Penampang','City','Yj\\ai');
INSERT INTO detailed_dd_city VALUES(20,'Ranau','City','^ge\\_');
INSERT INTO detailed_dd_city VALUES(21,'Sandakan','City','_ie^o');
INSERT INTO detailed_dd_city VALUES(22,'Semporna','City','vY`Ys');
INSERT INTO detailed_dd_city VALUES(23,'Sipitang','City',']dj\\`');
INSERT INTO detailed_dd_city VALUES(24,'Tambunan','City','juprp');
INSERT INTO detailed_dd_city VALUES(25,'Tamparuli','City','Yyhse');
INSERT INTO detailed_dd_city VALUES(26,'Tg. Aru','City','ejhkj');
INSERT INTO detailed_dd_city VALUES(27,'Tawau','City','hk[Zk');
INSERT INTO detailed_dd_city VALUES(28,'Tenom','City','py\\[u');
INSERT INTO detailed_dd_city VALUES(29,'Tuaran','City','^Z`nb');
INSERT INTO detailed_dd_city VALUES(30,'Kinabatangan','City','v_[ph');
INSERT INTO detailed_dd_city VALUES(31,'Pamol','City','k]cm\\');
INSERT INTO detailed_dd_city VALUES(32,'Putatan','City','xqk`t');
CREATE TABLE `detailed_dd_state` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `state` varchar(255) NOT NULL UNIQUE,
  `category_list` varchar(255) NOT NULL,
  `uuid` varchar(255) NULL
);
INSERT INTO detailed_dd_state VALUES(1,'Sabah','State','im]kj');
CREATE TABLE `detailed_dd_gender` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `gender` varchar(255) NOT NULL UNIQUE,
  `category_list` varchar(255) NULL,
  `uuid` varchar(255) NULL
);
INSERT INTO detailed_dd_gender VALUES(1,'Perempuan','Gender','1');
INSERT INTO detailed_dd_gender VALUES(2,'Lelaki','Gender','2');
CREATE TABLE `detailed_dd_citizenship` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `citizenship` varchar(255) NOT NULL UNIQUE,
  `category_list` varchar(255) NULL,
  `uuid` varchar(255) NULL
);
INSERT INTO detailed_dd_citizenship VALUES(1,'Indonesia','Citizenship','ue\\t]');
INSERT INTO detailed_dd_citizenship VALUES(2,'Philippines','Citizenship','qllfx');
CREATE TABLE `detailed_dd_designation` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `designation` varchar(255) NOT NULL UNIQUE,
  `category_list` varchar(255) NULL,
  `uuid` varchar(255) NULL
);
INSERT INTO detailed_dd_designation VALUES(3,'Designation 1','Designation',NULL);
INSERT INTO detailed_dd_designation VALUES(4,'Designation 2','Designation',NULL);
CREATE TABLE `detailed_dd_maritail_status` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `maritial_status` varchar(255) NOT NULL UNIQUE,
  `category_list` varchar(255) NULL,
  `uuid` varchar(255) NULL
);
INSERT INTO detailed_dd_maritail_status VALUES(1,'Berkawhin','Maritial Status','sgihe');
INSERT INTO detailed_dd_maritail_status VALUES(2,'Bujang','Maritial Status','lkitw');
INSERT INTO detailed_dd_maritail_status VALUES(3,'Bercerai','Maritial Status','ooqyt');
INSERT INTO detailed_dd_maritail_status VALUES(4,'Duda/Janda','Maritial Status','_mi]r');
INSERT INTO detailed_dd_maritail_status VALUES(5,'Tinggal berasingan','Maritial Status','rshmh');
CREATE TABLE `detailed_dd_poe` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `poe` varchar(255) NOT NULL UNIQUE,
  `category_list` varchar(255) NULL,
  `uuid` varchar(255)  NULL
);
INSERT INTO detailed_dd_poe VALUES(1,'Sandakan','Point of Entry','1');
INSERT INTO detailed_dd_poe VALUES(2,'Tawau','Point of Entry','dt[va');
INSERT INTO detailed_dd_poe VALUES(3,'Kota Kinabalu','Point of Entry','qntfu');
INSERT INTO detailed_dd_poe VALUES(4,'Kuala Sipitang','Point of Entry','wvnij');
INSERT INTO detailed_dd_poe VALUES(5,'Semporna','Point of Entry','`oyih');
INSERT INTO detailed_dd_poe VALUES(6,'Kudat','Point of Entry','qgle\\');
INSERT INTO detailed_dd_poe VALUES(7,'Lahad Datu','Point of Entry','loyrn');
INSERT INTO detailed_dd_poe VALUES(8,'Pulau Bangi','Point of Entry','bplbm');
INSERT INTO detailed_dd_poe VALUES(9,'Menumbok','Point of Entry','x]Zj`');
INSERT INTO detailed_dd_poe VALUES(10,'Lain-lain','Point of Entry','\\\\jc[');
CREATE TABLE `detailed_dd_religion` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `religion` varchar(255) NOT NULL UNIQUE,
  `category_list` varchar(255) NULL,
  `uuid` varchar(255) NULL
);
INSERT INTO detailed_dd_religion VALUES(1,'Islam','Religion','1');
INSERT INTO detailed_dd_religion VALUES(2,'Kristian','Religion','2');
INSERT INTO detailed_dd_religion VALUES(3,'Buddha','Religion','sn_t^');
INSERT INTO detailed_dd_religion VALUES(4,'Hindu','Religion','r^leu');
INSERT INTO detailed_dd_religion VALUES(5,'Tiada','Religion','nhcb`');
INSERT INTO detailed_dd_religion VALUES(6,'Lain-lain','Religion','w[b^f');
CREATE TABLE `detailed_dd_race` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `race` varchar(255) NOT NULL UNIQUE,
  `category_list` varchar(255) NULL,
  `uuid` varchar(255) NULL
);
INSERT INTO detailed_dd_race VALUES(1,'Lain-Lain','Race','1');
INSERT INTO detailed_dd_race VALUES(2,'Melayu','Race','2');
INSERT INTO detailed_dd_race VALUES(5,'Bugis','Race','yla_l');
INSERT INTO detailed_dd_race VALUES(6,'Boyan','Race','vu\\pZ');
INSERT INTO detailed_dd_race VALUES(7,'Banjar','Race','ni`ru');
INSERT INTO detailed_dd_race VALUES(8,'Jawa','Race','Z\\uin');
INSERT INTO detailed_dd_race VALUES(9,'Minangkabau','Race','jr\\gh');
INSERT INTO detailed_dd_race VALUES(10,'India Muslim','Race','bbYhy');
INSERT INTO detailed_dd_race VALUES(11,'Tamil','Race','oyisp');
INSERT INTO detailed_dd_race VALUES(12,'India','Race','s\\ws`');
INSERT INTO detailed_dd_race VALUES(13,'Bisaya','Race','fybp\\');
INSERT INTO detailed_dd_race VALUES(14,'Timor','Race','og\\f`');
INSERT INTO detailed_dd_race VALUES(15,'Tator','Race','xZk_\\');
CREATE TABLE `detailed_dd_sector` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `sector` varchar(255) NOT NULL UNIQUE,
  `category_list` varchar(255) NULL,
  `uuid` varchar(255) NULL
);
INSERT INTO detailed_dd_sector VALUES(1,'Tanaman','Sector','dxva]');
INSERT INTO detailed_dd_sector VALUES(2,'Akuakultur','Sector','k]bxY');
INSERT INTO detailed_dd_sector VALUES(3,'Ternakan','Sector','d_xin');
INSERT INTO detailed_dd_sector VALUES(4,'Ladang Kelapa Sawit','Sector','yonvy');
INSERT INTO detailed_dd_sector VALUES(5,'Ladang Getah','Sector','\\exey');
INSERT INTO detailed_dd_sector VALUES(6,'Ladang Koko','Sector','t^rYo');
INSERT INTO detailed_dd_sector VALUES(7,'Ladang Hutan','Sector','tnxc[');
INSERT INTO detailed_dd_sector VALUES(8,'Ladang Jati / Sentang','Sector','auget');
INSERT INTO detailed_dd_sector VALUES(9,'Semaian Ladang Sawit','Sector','tluhv');
INSERT INTO detailed_dd_sector VALUES(10,'Tapak Semaian Lain','Sector','[`ala');
INSERT INTO detailed_dd_sector VALUES(11,'Berorientasi Eksport','Sector','_bdcr');
INSERT INTO detailed_dd_sector VALUES(12,'Bukan Berorientasi Eksport','Sector','t\\r[n');
INSERT INTO detailed_dd_sector VALUES(13,'Sektor Elektrik dan Elektronik','Sector','f]exn');
INSERT INTO detailed_dd_sector VALUES(14,'Restoran','Sector','r_\\no');
INSERT INTO detailed_dd_sector VALUES(15,'Dobi','Sector','htdpt');
INSERT INTO detailed_dd_sector VALUES(16,'Rumah Kebajikan','Sector','ffnvh');
INSERT INTO detailed_dd_sector VALUES(17,'Spa dan Refleksologi','Sector','[hton');
INSERT INTO detailed_dd_sector VALUES(18,'Pusat Peranginan','Sector','r[ngl');
INSERT INTO detailed_dd_sector VALUES(19,'Borong dan Runcit','Sector','_sjwj');
INSERT INTO detailed_dd_sector VALUES(20,'Hotel','Sector','gtl\\c');
INSERT INTO detailed_dd_sector VALUES(21,'Bangunan','Sector','aYc`\\');
INSERT INTO detailed_dd_sector VALUES(22,'Infrastruktur','Sector','lZZa_');
INSERT INTO detailed_dd_sector VALUES(23,'Lanskap','Sector','cy^o\\');
INSERT INTO detailed_dd_sector VALUES(24,'Perlombongan','Sector','a\\ep`');
INSERT INTO detailed_dd_sector VALUES(25,'Pengkuarian','Sector','jkixZ');
CREATE TABLE `detailed_dd_job_sector` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `job_sector` varchar(255) NOT NULL UNIQUE,
  `category_list` varchar(255) NULL
);
INSERT INTO detailed_dd_job_sector VALUES(1,'Pertanian','Job Sector');
INSERT INTO detailed_dd_job_sector VALUES(2,'Perladangan','Job Sector');
INSERT INTO detailed_dd_job_sector VALUES(3,'Perkilangan','Job Sector');
INSERT INTO detailed_dd_job_sector VALUES(4,'Perkhidmatan','Job Sector');
INSERT INTO detailed_dd_job_sector VALUES(5,'Pembinaan','Job Sector');
INSERT INTO detailed_dd_job_sector VALUES(6,'Perlombongan','Job Sector');
CREATE TABLE `detailed_dd_job_sub_sector` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `job_sub_sector` varchar(255)  NOT NULL UNIQUE,
  `job_sector` varchar(255) NOT NULL
);
INSERT INTO detailed_dd_job_sub_sector VALUES(1,'Job SS 1','Pembinaan');
INSERT INTO detailed_dd_job_sub_sector VALUES(2,'Job SS 2','Pembinaan');
INSERT INTO detailed_dd_job_sub_sector VALUES(3,'Job SS 3','Perkilangan');
INSERT INTO detailed_dd_job_sub_sector VALUES(4,'Job SS 4','Pertanian');
CREATE TABLE `detailed_dd_employement_status` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `employement_status` varchar(255) NOT NULL UNIQUE
);
INSERT INTO detailed_dd_employement_status VALUES(1,'Sah/Aktif');
INSERT INTO detailed_dd_employement_status VALUES(2,'Tidak sah');
INSERT INTO detailed_dd_employement_status VALUES(3,'Tidak berkerja');
INSERT INTO detailed_dd_employement_status VALUES(4,'Kerja sambilan');
CREATE TABLE `detailed_dd_license_category` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `license_list` varchar(255) NOT NULL UNIQUE
);
INSERT INTO detailed_dd_license_category VALUES(1,'Category one');
CREATE TABLE `detailed_dd_relationship` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `relationship` varchar(255) NOT NULL UNIQUE
);
INSERT INTO detailed_dd_relationship VALUES(1,'rel');
CREATE TABLE `detailed_dd_type_of_doc` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `type_of_doc` varchar(255) NOT NULL UNIQUE
);
INSERT INTO detailed_dd_type_of_doc VALUES(2,'typ Doc');
CREATE TABLE `detailed_dd_country_issued_doc` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `country_issued_doc` varchar(255) NOT NULL UNIQUE
);
INSERT INTO detailed_dd_country_issued_doc VALUES(5,'test1');
CREATE TABLE `detailed_dd_current_status_doc` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `current_status_doc` varchar(255) NOT NULL UNIQUE
);
INSERT INTO detailed_dd_current_status_doc VALUES(2,'test');
CREATE TABLE `detailed_dd_worker_legal_status` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `legal_status` varchar(255) NOT NULL UNIQUE
);
INSERT INTO detailed_dd_worker_legal_status VALUES(3,'Legal');
INSERT INTO detailed_dd_worker_legal_status VALUES(4,'Illegal');
INSERT INTO detailed_dd_worker_legal_status VALUES(5,'Another 1');
INSERT INTO detailed_dd_worker_legal_status VALUES(6,'Another 2');
INSERT INTO detailed_dd_worker_legal_status VALUES(7,'Another 3');
INSERT INTO detailed_dd_worker_legal_status VALUES(8,'Another 4');
CREATE TABLE `half_form_time` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `worker_reg_no` varchar(255) NOT NULL UNIQUE,
  `reg_date` varchar(25) NULL,
  `reg_time` varchar(25) NULL
);
INSERT INTO half_form_time VALUES(1,'FW23NSPL000004','20/09/2023','08:04:38');
INSERT INTO half_form_time VALUES(2,'FW23NSPL000005','20/09/2023','14:23:14');
INSERT INTO half_form_time VALUES(3,'FW23NSPL000006','23/09/2023','18:04:28');
INSERT INTO half_form_time VALUES(4,'FW23NSPL000007','25/09/2023','15:11:54');
INSERT INTO half_form_time VALUES(5,'FW23NSPL000008','25/09/2023','15:34:28');
INSERT INTO half_form_time VALUES(6,'FW23NSPL000009','26/09/2023','17:42:09');
INSERT INTO half_form_time VALUES(7,'FW23NSPL000010','27/09/2023','01:12:20');
INSERT INTO half_form_time VALUES(8,'FW23TD000011','30/09/2023','20:31:16');
INSERT INTO half_form_time VALUES(9,'FW23TD000012','30/09/2023','20:54:17');
INSERT INTO half_form_time VALUES(10,'FW23TD000013','30/09/2023','21:07:03');
CREATE TABLE `outreach` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `date_for` varchar(25) NULL,
  `plantation_name` varchar(255) NULL,
  `total_legal_worker` varchar(25) NULL,
  `total_undocumented_worker` varchar(25) NULL,
  `total_legal_fm` varchar(25) NULL,
  `total_undocumented_fm` varchar(25) NULL,
  `total_pati_imm` varchar(25) NULL,
  `creation_date` varchar(25) NULL,
  `creation_time` varchar(25) NULL
);
INSERT INTO outreach VALUES(5,'2023-09-22','Plantation AAA','100','50','560','450','1005','22/09/2023','17:36:10');
INSERT INTO outreach VALUES(6,'2023-09-23','Plantation AAA','140','80','670','340','230','23/09/2023','13:45:26');
CREATE TABLE `sub_users` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `name` varchar(255) NULL,
  `username` varchar(100) NOT NULL UNIQUE,
  `password` varchar(50) NULL,
  `creator` varchar(255) NULL,
  `creation_date` varchar(25) NULL,
  `creation_time` varchar(25) NULL
);
INSERT INTO sub_users VALUES(1,'hii','user@sub','123456','john@g','26/09/2023','00:13:25');
INSERT INTO sub_users VALUES(2,'hey','joe@joe','1212','john@g','26/09/2023','06:46:16');
INSERT INTO sub_users VALUES(4,'New Sub User','new_sub@user','123456','john@g','26/09/2023','19:27:52');
INSERT INTO sub_users VALUES(6,'sub user ','sub@demo.com','123','alex@gmail.com','30/09/2023','20:18:39');
INSERT INTO sub_users VALUES(7,'Hit Sub','hit@subu','1234','hitman@gmail.com','02/10/2023','05:19:09');
CREATE TABLE `sub_users_datalog` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `creator` varchar(255) NULL,
  `parent` varchar(255) NULL,
  `worker_reg_no` varchar(255) NOT NULL UNIQUE,
  `form_unique_key` varchar(255) NOT NULL UNIQUE,
  `creation_date` varchar(25) NULL,
  `creation_time` varchar(25) NULL
);
INSERT INTO sub_users_datalog VALUES(2,'user@sub','john@g','FW23NSPL000010','DT27092023N10860','29/09/2023','01:12:20');
INSERT INTO sub_users_datalog VALUES(3,'sub@demo.com','alex@gmail.com','FW23TD000011','DT30092023N76094','30/09/2023','20:31:16');
INSERT INTO sub_users_datalog VALUES(4,'sub@demo.com','alex@gmail.com','FW23TD000012','DT30092023N62651','30/09/2023','20:54:17');
INSERT INTO sub_users_datalog VALUES(5,'sub@demo.com','alex@gmail.com','FW23TD000013','DT30092023N36210','30/09/2023','21:07:03');
CREATE TABLE `reg_num_tracking` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `tracking_id` varchar(11) NOT NULL,
  `user` varchar(255) NOT NULL,
  `creator` varchar(255) NOT NULL,
  `worker_reg_no` varchar(255) NOT NULL UNIQUE,
  `status` varchar(20) NOT NULL,
  `creation_date` varchar(25) NULL,
  `creation_time` varchar(25) NULL
);
CREATE TABLE `fm_reg_num_tracking` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `tracking_id` varchar(11) NOT NULL,
  `user` varchar(255) NOT NULL,
  `creator` varchar(255) NOT NULL,
  `worker_reg_no` varchar(255) NOT NULL,
  `fm_reg_no` varchar(255) NOT NULL UNIQUE,
  `status` varchar(20) NOT NULL,
  `creation_date` varchar(25) NULL,
  `creation_time` varchar(25) NULL
);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('profile',5);
INSERT INTO sqlite_sequence VALUES('half_form',13);
INSERT INTO sqlite_sequence VALUES('workers_document',29);
INSERT INTO sqlite_sequence VALUES('family_form',5);
INSERT INTO sqlite_sequence VALUES('users',8);
INSERT INTO sqlite_sequence VALUES('sub_admin',2);
INSERT INTO sqlite_sequence VALUES('detailed_dd_city',34);
INSERT INTO sqlite_sequence VALUES('detailed_dd_state',4);
INSERT INTO sqlite_sequence VALUES('detailed_dd_gender',4);
INSERT INTO sqlite_sequence VALUES('detailed_dd_citizenship',4);
INSERT INTO sqlite_sequence VALUES('detailed_dd_designation',4);
INSERT INTO sqlite_sequence VALUES('detailed_dd_maritail_status',7);
INSERT INTO sqlite_sequence VALUES('detailed_dd_poe',12);
INSERT INTO sqlite_sequence VALUES('detailed_dd_religion',7);
INSERT INTO sqlite_sequence VALUES('detailed_dd_race',16);
INSERT INTO sqlite_sequence VALUES('detailed_dd_sector',27);
INSERT INTO sqlite_sequence VALUES('detailed_dd_job_sector',7);
INSERT INTO sqlite_sequence VALUES('detailed_dd_job_sub_sector',4);
INSERT INTO sqlite_sequence VALUES('detailed_dd_employement_status',6);
INSERT INTO sqlite_sequence VALUES('detailed_dd_license_category',2);
INSERT INTO sqlite_sequence VALUES('detailed_dd_relationship',2);
INSERT INTO sqlite_sequence VALUES('detailed_dd_type_of_doc',2);
INSERT INTO sqlite_sequence VALUES('detailed_dd_country_issued_doc',6);
INSERT INTO sqlite_sequence VALUES('detailed_dd_current_status_doc',2);
INSERT INTO sqlite_sequence VALUES('detailed_dd_worker_legal_status',8);
INSERT INTO sqlite_sequence VALUES('half_form_time',10);
INSERT INTO sqlite_sequence VALUES('outreach',6);
INSERT INTO sqlite_sequence VALUES('sub_users',7);
INSERT INTO sqlite_sequence VALUES('sub_users_datalog',5);
COMMIT;
