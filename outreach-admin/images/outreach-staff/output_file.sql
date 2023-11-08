/*
CREATE TABLE `reg_num_tracking` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `tracking_id` integer(11) NOT NULL,
  `user` varchar(255) NOT NULL,
  `creator` varchar(255) NOT NULL,
  `worker_reg_no` varchar(255) NOT NULL UNIQUE,
  `status` varchar(20) NOT NULL,
  `creation_date` varchar(25) NULL,
  `creation_time` varchar(25) NULL
);


CREATE TABLE `dermalog_ip` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `dermalog_ip` integer(11) NOT NULL,
  `creator` varchar(255) NOT NULL,
  `updated_date` varchar(25) NULL,
  `updated_time` varchar(25) NULL
);


CREATE TABLE `fm_biodata` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `fm_reg_no` integer(11) NOT NULL UNIQUE,
  `docId` integer(11) NOT NULL,
  `faceImage` text,
  `fingerRemarks1` varchar (255) NULL,
  `fingerImage1` text,
  `fingerRemarks2` varchar (255) NULL,
  `fingerImage2` text,
  `fingerRemarks3` varchar (255) NULL,
  `fingerImage3` text,
  `fingerRemarks4` varchar (255) NULL,
  `fingerImage4` text,
  `fingerRemarks5` varchar (255) NULL,
  `fingerImage5` text,
  `fingerRemarks6` varchar (255) NULL,
  `fingerImage6` text,
  `fingerRemarks7` varchar (255) NULL,
  `fingerImage7` text,
  `fingerRemarks8` varchar (255) NULL,
  `fingerImage8` text,
  `fingerRemarks9` varchar (255) NULL,
  `fingerImage9` text,
  `fingerRemarks10` varchar (255) NULL,
  `fingerImage10` text,
  `updated_date` varchar(25) NULL,
  `updated_time` varchar(25) NULL
);



CREATE TABLE `half_form` (
  `id` integer NOT NULL primary key AUTOINCREMENT,
  `worker_key` integer NOT NULL,
  `form_created_by` varchar(255) NOT NULL,
  `form_created_date` varchar(255) NOT NULL,
  `form_worker_reg_no` varchar(255) NOT NULL,
  `no_family_mem` varchar(255) NOT NULL,
  `worker_detail_worker_legal_status` varchar(255) NULL,
  `worker_detail_name_of_worker` varchar(255) NULL,
  `worker_detail_family_name` varchar(255) NULL,
  `worker_detail_gender` varchar(255) NULL,
  `worker_detail_DOB` varchar(255) NULL,
  `worker_detail_place_birth` varchar(255) NULL,
  `worker_detail_citizenship` varchar(255) NULL,
  `worker_detail_marital_status` varchar(255) NULL,
  `worker_detail_poe` varchar(255) NULL,
  `worker_detail_religion` varchar(255) NULL,
  `worker_detail_race` varchar(255) NULL,
  `worker_detail_contact_no` varchar(255) NULL,
  `worker_detail_email` varchar(255) NULL,
  `worker_detail_nok` varchar(255) NULL,
  `worker_detail_relationship` varchar(255) NULL,
  `worker_detail_nok_contact_no` varchar(255) NULL,
  `worker_emp_dtl_job_sector` varchar(255) NULL,
  `worker_emp_dtl_job_sub_sector` varchar(255) NULL,
  `worker_emp_dtl_emp_sponsorship_status` varchar(255) NULL,
  `worker_emp_dtl_address1` varchar(255) NULL,
  `worker_emp_dtl_address2` varchar(255) NULL,
  `worker_emp_dtl_address3` varchar(255) NULL,
  `worker_emp_dtl_postcode` varchar(255) NULL,
  `worker_emp_dtl_city` varchar(255) NULL,
  `worker_emp_dtl_state` varchar(255) NULL,
  `form_position` varchar(255) NULL,
  `form_status` varchar(255) NULL,
  `form_unique_key` varchar(255) NULL UNIQUE
);


CREATE TABLE `workers_document` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `worker_key` integer NULL,
  `document_link` varchar(255) DEFAULT NULL,
  `type_of_douments` varchar(255) DEFAULT NULL,
  `document_id` varchar(50) DEFAULT NULL,
  `place_of_issue` text,
  `document_issued_date` varchar(20) DEFAULT NULL,
  `document_expiry_date` varchar(20) DEFAULT NULL,
  `issuing_country` varchar(255) DEFAULT NULL,
  `document_status` varchar(255) DEFAULT NULL,
  `status_of_current_document` varchar(255) DEFAULT NULL,
  `form_unique_key` varchar(100) NULL,
  `worker_reg_no` varchar(100) NULL,
  `document_image` text NULL
);


CREATE TABLE `fm_document` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `worker_key` integer NULL,
  `document_link` varchar(255) DEFAULT NULL,
  `type_of_douments` varchar(255) DEFAULT NULL,
  `document_id` varchar(50) DEFAULT NULL,
  `place_of_issue` text,
  `document_issued_date` varchar(20) DEFAULT NULL,
  `document_expiry_date` varchar(20) DEFAULT NULL,
  `issuing_country` varchar(255) DEFAULT NULL,
  `document_status` varchar(255) DEFAULT NULL,
  `status_of_current_document` varchar(255) DEFAULT NULL,
  `form_unique_key` varchar(100) NULL,
  `fm_reg_no` varchar(100) NULL,
  `document_image` text NULL
);
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
  `worker_key` integer(11) NULL
);

*/


CREATE TABLE `staff_status` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `staff_username` varchar(255) DEFAULT NULL,
  `admin_server_ip` varchar(255) DEFAULT NULL,
  `connection_date` varchar(20) DEFAULT NULL,
  `connection_time` varchar(20) DEFAULT NULL
);