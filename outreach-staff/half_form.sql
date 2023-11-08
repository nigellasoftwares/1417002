

CREATE TABLE `half_form` (
  `id` integer NOT NULL primary key AUTOINCREMENT,
  `worker_key` integer NOT NULL UNIQUE,
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
  `form_unique_key` varchar(255) NOT NULL
);

--
-- Dumping data for table `half_form`
--

INSERT INTO `half_form` (`id`, `worker_key`, `form_created_by`, `form_created_date`, `form_worker_reg_no`, `no_family_mem`, `worker_detail_worker_legal_status`, `worker_detail_name_of_worker`, `worker_detail_family_name`, `worker_detail_gender`, `worker_detail_DOB`, `worker_detail_place_birth`, `worker_detail_citizenship`, `worker_detail_marital_status`, `worker_detail_poe`, `worker_detail_religion`, `worker_detail_race`, `worker_detail_contact_no`, `worker_detail_email`, `worker_detail_nok`, `worker_detail_relationship`, `worker_detail_nok_contact_no`, `worker_emp_dtl_job_sector`, `worker_emp_dtl_job_sub_sector`, `worker_emp_dtl_emp_sponsorship_status`, `worker_emp_dtl_address1`, `worker_emp_dtl_address2`, `worker_emp_dtl_address3`, `worker_emp_dtl_postcode`, `worker_emp_dtl_city`, `worker_emp_dtl_state`, `worker_doc_dtl_doc_id`, `worker_doc_dtl_type_of_doc`, `worker_doc_dtl_no_of_doc`, `worker_doc_dtl_images_path_email`, `worker_doc_dtl_place_of_issue`, `worker_doc_dtl_issue_date`, `worker_doc_dtl_expiry_date`, `worker_doc_dtl_country_doc_issued`, `worker_doc_dtl_doc_status`, `worker_doc_dtl_doc_current_status`, `worker_doc_dtl_doc_no`, `form_position`, `form_status`, `form_unique_key`) VALUES
(1, 1, '2423', '21/05/2023', '000003', '252fdgs', 'illegal', 'Akash', '2rewwr', 'worker_detail_gender', '11/05/1998', 'UP', 'citizenship', 'worker_detail_marital_status', 'worker_detail_poe', 'worker_detail_religion', 'worker_detail_race', 'worker_detail_contact_no', 'worker_detail_email', 'worker_detail_nok', 'worker_detail_relationship', 'worker_detail_nok_contact_no', 'worker_emp_dtl_job_sector', 'worker_emp_dtl_job_sub_sector', 'worker_emp_dtl_emp_sponsorship_status', 'worker_emp_dtl_address1', 'worker_emp_dtl_address2', 'worker_emp_dtl_address3', 'worker_emp_dtl_postcode', 'worker_emp_dtl_city', 'worker_emp_dtl_state', 'worker_doc_dtl_doc_id', 'worker_doc_dtl_type_of_doc', 'worker_doc_dtl_no_of_doc', 'worker_doc_dtl_images_path_email', 'worker_doc_dtl_place_of_issue', 'worker_doc_dtl_issue_date', 'worker_doc_dtl_expiry_date', 'worker_doc_dtl_country_doc_issued', 'worker_doc_dtl_doc_status', 'worker_doc_dtl_doc_current_status', 'worker_doc_dtl_doc_no', 'form_position', 'form_status', 'form_unique_key'),
(2, 2, '2423', '21/05/2023', '000001', '252fdgs', 'legal', 'Vijay', '2rewwr', 'worker_detail_gender', 'worker_detail_DOB', 'worker_detail_place_birth', 'worker_detail_citizenship', 'worker_detail_marital_status', 'worker_detail_poe', 'worker_detail_religion', 'worker_detail_race', 'worker_detail_contact_no', 'worker_detail_email', 'worker_detail_nok', 'worker_detail_relationship', 'worker_detail_nok_contact_no', 'worker_emp_dtl_job_sector', 'worker_emp_dtl_job_sub_sector', 'worker_emp_dtl_emp_sponsorship_status', 'worker_emp_dtl_address1', 'worker_emp_dtl_address2', 'worker_emp_dtl_address3', 'worker_emp_dtl_postcode', 'worker_emp_dtl_city', 'worker_emp_dtl_state', 'worker_doc_dtl_doc_id', 'worker_doc_dtl_type_of_doc', 'worker_doc_dtl_no_of_doc', 'worker_doc_dtl_images_path_email', 'worker_doc_dtl_place_of_issue', 'worker_doc_dtl_issue_date', 'worker_doc_dtl_expiry_date', 'worker_doc_dtl_country_doc_issued', 'worker_doc_dtl_doc_status', 'worker_doc_dtl_doc_current_status', 'worker_doc_dtl_doc_no', 'form_position', 'form_status', 'vbn'),
(3, 3, '2423', '21/05/2023', '0000002', '252fdgs', 'illegal', 'Alakh', '2rewwr', 'worker_detail_gender', 'worker_detail_DOB', 'worker_detail_place_birth', 'worker_detail_citizenship', 'worker_detail_marital_status', 'worker_detail_poe', 'worker_detail_religion', 'worker_detail_race', 'worker_detail_contact_no', 'worker_detail_email', 'worker_detail_nok', 'worker_detail_relationship', 'worker_detail_nok_contact_no', 'worker_emp_dtl_job_sector', 'worker_emp_dtl_job_sub_sector', 'worker_emp_dtl_emp_sponsorship_status', 'worker_emp_dtl_address1', 'worker_emp_dtl_address2', 'worker_emp_dtl_address3', 'worker_emp_dtl_postcode', 'worker_emp_dtl_city', 'worker_emp_dtl_state', 'worker_doc_dtl_doc_id', 'worker_doc_dtl_type_of_doc', 'worker_doc_dtl_no_of_doc', 'worker_doc_dtl_images_path_email', 'worker_doc_dtl_place_of_issue', 'worker_doc_dtl_issue_date', 'worker_doc_dtl_expiry_date', 'worker_doc_dtl_country_doc_issued', 'worker_doc_dtl_doc_status', 'worker_doc_dtl_doc_current_status', 'worker_doc_dtl_doc_no', 'form_position', 'form_status', 'vbn1');

