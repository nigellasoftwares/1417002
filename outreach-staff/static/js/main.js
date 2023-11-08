$('#awl_worker_legal_status').on('change', function(){
    var status = $(this).val();
    if(status == 'Legal'){
        // Change Worker Docs Value
        $('#workerDocStatus').val('null');

        $('#worker_modal_div').show();
        $('#legal_div').show();
        $('#legal_one').show(); 
    }
    else if(status == 'Illegal'){
        // Change Worker Docs Value
        $('#workerDocStatus').val('null');

        $('#worker_modal_div').show();
        $('#illegal_div').show();
        $('#illegal_one').show();     
    }
})

$('#for_legal_two').on('click', function(){
    $('#legal_one').hide();
    $('#legal_two').show();   
})

$('#for_legal_three').on('click', function(){
    $('#legal_two').hide();
    $('#legal_three').show();   
})


// According to the date
$('#two_links').hide();

$('#legal_before_three_month_one').hide();
$('#legal_before_three_month_two').hide();
/*
function TDate() {
    var UserDate = document.getElementById("userdate").value;
    var ToDate = new Date();

    const threeMonthsBackDate = new Date();
    threeMonthsBackDate.setMonth(currentDate.getMonth() - 3);

    if (new Date(UserDate).getTime() <= ToDate.getTime()) {
        $('#legal_three').hide();
        $('#legal_four').show();        
    } else if (UserDate >= threeMonthsBackDate && UserDate <= ToDate) {
        $('#legal_three').hide();
        alert('You have choosen the future date please click ok button to edit.')
        $('#legal_four').show(); 
    } else if (UserDate < threeMonthsBackDate){
        alert('3 months back Date.')
    }
}
*/
function TDate() {
    const userDate = document.getElementById("userdate");
    const selectedDate = new Date(userDate.value);
    const currentDate = new Date();

    // Calculate the date that is 3 months from the current date
    const threeMonthsBackDate = new Date();
    threeMonthsBackDate.setMonth(currentDate.getMonth() - 3);

    if (selectedDate >= threeMonthsBackDate && selectedDate <= currentDate) {
        $('#legal_three').hide();
        $('#legal_four').show(); 
    } else if (selectedDate.getTime() > currentDate.getTime()) {
        $('#legal_three').hide();
        alert('You have choosen the future date please click ok button to edit.')
        $('#legal_four').show(); 
    } else if (selectedDate <= threeMonthsBackDate) {
        $('#legal_three').hide();
        $('#legal_before_three_month_one').show();
        // It will open illegal documents details
        $('#legal_document_details').hide()
        $('#illegal_document_details').show() 
    }
}
// End According to the date

$('#for_legal_before_three_month_two').on('click', function(){
    // Change Worker Docs Value
    $('#workerDocStatus').val('statusDoc6');

    $('#legal_before_three_month_one').hide();
    $('#legal_before_three_month_two').show();   
})


$('.all_legal_cancel').on('click', function(){
    $('#worker_modal_div').hide();
    $('#legal_div').hide();
    $('#legal_one').hide();
    $('#legal_two').hide();
    $('#legal_three').hide();
    $('#legal_four').hide(); 
    $('#after_date_one').hide();
    $('#after_date_two').hide();
    $('#legal_before_three_month_one').hide();
    $('#legal_before_three_month_two').hide();
})

// other illegal parts 
$('#for_after_date_two').on('click', function(){
    $('#after_date_one').hide();
    $('#after_date_two').show();   
})

$('#for_illegal_two').on('click', function(){
    $('#illegal_one').hide();
    $('#illegal_two').show();   
})

/*
$('#for_illegal_three').on('click', function(){
    $('#illegal_two').hide();
    $('#illegal_three').show();   
})
*/

$('.all_illegal_cancel').on('click', function(){
    $('#worker_modal_div').hide();
    $('#illegal_div').hide();
    $('#illegal_one').hide();
    $('#illegal_two').hide();
    //$('#illegal_three').hide();
})




// If Staying together 'Yes'
$('#fm_is_family_member_together').on('change', function(){
    var opVal = $(this).val();
    var wAddress1 = $('#awl_address1').val();
    var wAddress2 = $('#awl_address2').val();
    var wAddress3 = $('#awl_address3').val();

    console.log(wAddress1+wAddress2+wAddress3)

    if(opVal == 'Yes'){
        $('#fm_address1').val(wAddress1);
        $('#fm_address2').val(wAddress2);
        $('#fm_address3').val(wAddress3);
        
        $('#fm_address1').attr('disabled', 'disabled');
        $('#fm_address2').attr('disabled', 'disabled');
        $('#fm_address3').attr('disabled', 'disabled');
    }
})


  // Function to handle button click
  function handleButtonClick() {
    const memberId = $(this).attr('id');
    //alert(`Clicked on ${memberId}`);

    // For member1
    if (memberId == 'member1'){
        $('#worker_registrationCon').hide()
        $('#family_member2').hide()
        $('#family_member3').hide()
        $('#family_member4').hide()
        $('#family_member5').hide()
        $('#family_member6').hide()
        $('#family_member7').hide()
        $('#family_member8').hide()
        $('#family_member9').hide()
        $('#family_member10').hide()
        
        $('#familyMemberContainer').show()
        $('#family_member1').show()

        $('#member1').removeClass('btn-primary')
        $('#member1').addClass('btn-secondary')
        $('#member2').removeClass('btn-secondary')
        $('#member2').addClass('btn-primary')
        $('#member3').removeClass('btn-secondary')
        $('#member3').addClass('btn-primary')
        $('#member4').removeClass('btn-secondary')
        $('#member4').addClass('btn-primary')
        $('#member5').removeClass('btn-secondary')
        $('#member5').addClass('btn-primary')
        $('#member6').removeClass('btn-secondary')
        $('#member6').addClass('btn-primary')
        $('#member7').removeClass('btn-secondary')
        $('#member7').addClass('btn-primary')
        $('#member8').removeClass('btn-secondary')
        $('#member8').addClass('btn-primary')
        $('#member9').removeClass('btn-secondary')
        $('#member9').addClass('btn-primary')
        $('#member10').removeClass('btn-secondary')
        $('#member10').addClass('btn-primary')
        $('#worker_registrationConBtn').removeClass('btn-secondary')
        $('#worker_registrationConBtn').addClass('btn-dark')
    }
  

    // for member2
    if (memberId == 'member2'){ 
        $('#worker_registrationCon').hide()
        $('#family_member1').hide()
        $('#family_member3').hide()
        $('#family_member4').hide()
        $('#family_member5').hide()
        $('#family_member6').hide()
        $('#family_member7').hide()
        $('#family_member8').hide()
        $('#family_member9').hide()
        $('#family_member10').hide()

        $('#familyMemberContainer').show()
        $('#family_member2').show()


        $('#member1').removeClass('btn-secondary')
        $('#member1').addClass('btn-primary')
        $('#member2').removeClass('btn-primary')
        $('#member2').addClass('btn-secondary')
        $('#member3').removeClass('btn-secondary')
        $('#member3').addClass('btn-primary')
        $('#member4').removeClass('btn-secondary')
        $('#member4').addClass('btn-primary')
        $('#member5').removeClass('btn-secondary')
        $('#member5').addClass('btn-primary')
        $('#member6').removeClass('btn-secondary')
        $('#member6').addClass('btn-primary')
        $('#member7').removeClass('btn-secondary')
        $('#member7').addClass('btn-primary')
        $('#member8').removeClass('btn-secondary')
        $('#member8').addClass('btn-primary')
        $('#member9').removeClass('btn-secondary')
        $('#member9').addClass('btn-primary')
        $('#member10').removeClass('btn-secondary')
        $('#member10').addClass('btn-primary')
        $('#worker_registrationConBtn').removeClass('btn-secondary')
        $('#worker_registrationConBtn').addClass('btn-dark')
    }

    // for member3
    if (memberId == 'member3'){ 
        $('#worker_registrationCon').hide()
        $('#family_member1').hide()
        $('#family_member2').hide()
        $('#family_member4').hide()
        $('#family_member5').hide()
        $('#family_member6').hide()
        $('#family_member7').hide()
        $('#family_member8').hide()
        $('#family_member9').hide()
        $('#family_member10').hide()

        $('#familyMemberContainer').show()
        $('#family_member3').show()

        $('#member1').removeClass('btn-secondary')
        $('#member1').addClass('btn-primary')
        $('#member2').removeClass('btn-secondary')
        $('#member2').addClass('btn-primary')
        $('#member3').removeClass('btn-primary')
        $('#member3').addClass('btn-secondary')
        $('#member4').removeClass('btn-secondary')
        $('#member4').addClass('btn-primary')
        $('#member5').removeClass('btn-secondary')
        $('#member5').addClass('btn-primary')
        $('#member6').removeClass('btn-secondary')
        $('#member6').addClass('btn-primary')
        $('#member7').removeClass('btn-secondary')
        $('#member7').addClass('btn-primary')
        $('#member8').removeClass('btn-secondary')
        $('#member8').addClass('btn-primary')
        $('#member9').removeClass('btn-secondary')
        $('#member9').addClass('btn-primary')
        $('#member10').removeClass('btn-secondary')
        $('#member10').addClass('btn-primary')
        $('#worker_registrationConBtn').removeClass('btn-secondary')
        $('#worker_registrationConBtn').addClass('btn-dark')
    }

    // for member4
    if (memberId == 'member4'){ 
        $('#worker_registrationCon').hide()
        $('#family_member1').hide()
        $('#family_member3').hide()
        $('#family_member2').hide()
        $('#family_member5').hide()
        $('#family_member6').hide()
        $('#family_member7').hide()
        $('#family_member8').hide()
        $('#family_member9').hide()
        $('#family_member10').hide()

        $('#familyMemberContainer').show()
        $('#family_member4').show()


        $('#member1').removeClass('btn-secondary')
        $('#member1').addClass('btn-primary')
        $('#member2').removeClass('btn-secondary')
        $('#member2').addClass('btn-primary')
        $('#member3').removeClass('btn-secondary')
        $('#member3').addClass('btn-primary')
        $('#member4').removeClass('btn-primary')
        $('#member4').addClass('btn-secondary')
        $('#member5').removeClass('btn-secondary')
        $('#member5').addClass('btn-primary')
        $('#member6').removeClass('btn-secondary')
        $('#member6').addClass('btn-primary')
        $('#member7').removeClass('btn-secondary')
        $('#member7').addClass('btn-primary')
        $('#member8').removeClass('btn-secondary')
        $('#member8').addClass('btn-primary')
        $('#member9').removeClass('btn-secondary')
        $('#member9').addClass('btn-primary')
        $('#member10').removeClass('btn-secondary')
        $('#member10').addClass('btn-primary')
        $('#worker_registrationConBtn').removeClass('btn-secondary')
        $('#worker_registrationConBtn').addClass('btn-dark')
    }

    // for member5
    if (memberId == 'member5'){ 
        $('#worker_registrationCon').hide()
        $('#family_member1').hide()
        $('#family_member3').hide()
        $('#family_member4').hide()
        $('#family_member2').hide()
        $('#family_member6').hide()
        $('#family_member7').hide()
        $('#family_member8').hide()
        $('#family_member9').hide()
        $('#family_member10').hide()

        $('#familyMemberContainer').show()
        $('#family_member5').show()


        $('#member1').removeClass('btn-secondary')
        $('#member1').addClass('btn-primary')
        $('#member2').removeClass('btn-secondary')
        $('#member2').addClass('btn-primary')
        $('#member3').removeClass('btn-secondary')
        $('#member3').addClass('btn-primary')
        $('#member4').removeClass('btn-secondary')
        $('#member4').addClass('btn-primary')
        $('#member5').removeClass('btn-primary')
        $('#member5').addClass('btn-secondary')
        $('#member6').removeClass('btn-secondary')
        $('#member6').addClass('btn-primary')
        $('#member7').removeClass('btn-secondary')
        $('#member7').addClass('btn-primary')
        $('#member8').removeClass('btn-secondary')
        $('#member8').addClass('btn-primary')
        $('#member9').removeClass('btn-secondary')
        $('#member9').addClass('btn-primary')
        $('#member10').removeClass('btn-secondary')
        $('#member10').addClass('btn-primary')
        $('#worker_registrationConBtn').removeClass('btn-secondary')
        $('#worker_registrationConBtn').addClass('btn-dark')
    }

    // for member6
    if (memberId == 'member6'){ 
        $('#worker_registrationCon').hide()
        $('#family_member1').hide()
        $('#family_member3').hide()
        $('#family_member4').hide()
        $('#family_member5').hide()
        $('#family_member2').hide()
        $('#family_member7').hide()
        $('#family_member8').hide()
        $('#family_member9').hide()
        $('#family_member10').hide()

        $('#familyMemberContainer').show()
        $('#family_member6').show()

        $('#member1').removeClass('btn-secondary')
        $('#member1').addClass('btn-primary')
        $('#member2').removeClass('btn-secondary')
        $('#member2').addClass('btn-primary')
        $('#member3').removeClass('btn-secondary')
        $('#member3').addClass('btn-primary')
        $('#member4').removeClass('btn-secondary')
        $('#member4').addClass('btn-primary')
        $('#member5').removeClass('btn-secondary')
        $('#member5').addClass('btn-primary')
        $('#member6').removeClass('btn-primary')
        $('#member6').addClass('btn-secondary')
        $('#member7').removeClass('btn-secondary')
        $('#member7').addClass('btn-primary')
        $('#member8').removeClass('btn-secondary')
        $('#member8').addClass('btn-primary')
        $('#member9').removeClass('btn-secondary')
        $('#member9').addClass('btn-primary')
        $('#member10').removeClass('btn-secondary')
        $('#member10').addClass('btn-primary')
        $('#worker_registrationConBtn').removeClass('btn-secondary')
        $('#worker_registrationConBtn').addClass('btn-dark')
    }

    // for member7
    if (memberId == 'member7'){ 
        $('#worker_registrationCon').hide()
        $('#family_member1').hide()
        $('#family_member3').hide()
        $('#family_member4').hide()
        $('#family_member5').hide()
        $('#family_member6').hide()
        $('#family_member2').hide()
        $('#family_member8').hide()
        $('#family_member9').hide()
        $('#family_member10').hide()

        $('#familyMemberContainer').show()
        $('#family_member7').show()


        $('#member1').removeClass('btn-secondary')
        $('#member1').addClass('btn-primary')
        $('#member2').removeClass('btn-secondary')
        $('#member2').addClass('btn-primary')
        $('#member3').removeClass('btn-secondary')
        $('#member3').addClass('btn-primary')
        $('#member4').removeClass('btn-secondary')
        $('#member4').addClass('btn-primary')
        $('#member5').removeClass('btn-secondary')
        $('#member5').addClass('btn-primary')
        $('#member6').removeClass('btn-secondary')
        $('#member6').addClass('btn-primary')
        $('#member7').removeClass('btn-primary')
        $('#member7').addClass('btn-secondary')
        $('#member8').removeClass('btn-secondary')
        $('#member8').addClass('btn-primary')
        $('#member9').removeClass('btn-secondary')
        $('#member9').addClass('btn-primary')
        $('#member10').removeClass('btn-secondary')
        $('#member10').addClass('btn-primary')
        $('#worker_registrationConBtn').removeClass('btn-secondary')
        $('#worker_registrationConBtn').addClass('btn-dark')
    }

    // for member8
    if (memberId == 'member8'){ 
        $('#worker_registrationCon').hide()
        $('#family_member1').hide()
        $('#family_member3').hide()
        $('#family_member4').hide()
        $('#family_member5').hide()
        $('#family_member6').hide()
        $('#family_member7').hide()
        $('#family_member2').hide()
        $('#family_member9').hide()
        $('#family_member10').hide()

        $('#familyMemberContainer').show()
        $('#family_member8').show()


        $('#member1').removeClass('btn-secondary')
        $('#member1').addClass('btn-primary')
        $('#member2').removeClass('btn-secondary')
        $('#member2').addClass('btn-primary')
        $('#member3').removeClass('btn-secondary')
        $('#member3').addClass('btn-primary')
        $('#member4').removeClass('btn-secondary')
        $('#member4').addClass('btn-primary')
        $('#member5').removeClass('btn-secondary')
        $('#member5').addClass('btn-primary')
        $('#member6').removeClass('btn-secondary')
        $('#member6').addClass('btn-primary')
        $('#member7').removeClass('btn-secondary')
        $('#member7').addClass('btn-primary')
        $('#member8').removeClass('btn-primary')
        $('#member8').addClass('btn-secondary')
        $('#member9').removeClass('btn-secondary')
        $('#member9').addClass('btn-primary')
        $('#member10').removeClass('btn-secondary')
        $('#member10').addClass('btn-primary')
        $('#worker_registrationConBtn').removeClass('btn-secondary')
        $('#worker_registrationConBtn').addClass('btn-dark')  
    }

    // for member9
    if (memberId == 'member9'){ 
        $('#worker_registrationCon').hide()
        $('#family_member1').hide()
        $('#family_member3').hide()
        $('#family_member4').hide()
        $('#family_member5').hide()
        $('#family_member6').hide()
        $('#family_member7').hide()
        $('#family_member8').hide()
        $('#family_member2').hide()
        $('#family_member10').hide()

        $('#familyMemberContainer').show()
        $('#family_member9').show()

        $('#member1').removeClass('btn-secondary')
        $('#member1').addClass('btn-primary')
        $('#member2').removeClass('btn-secondary')
        $('#member2').addClass('btn-primary')
        $('#member3').removeClass('btn-secondary')
        $('#member3').addClass('btn-primary')
        $('#member4').removeClass('btn-secondary')
        $('#member4').addClass('btn-primary')
        $('#member5').removeClass('btn-secondary')
        $('#member5').addClass('btn-primary')
        $('#member6').removeClass('btn-secondary')
        $('#member6').addClass('btn-primary')
        $('#member7').removeClass('btn-secondary')
        $('#member7').addClass('btn-primary')
        $('#member8').removeClass('btn-secondary')
        $('#member8').addClass('btn-primary')
        $('#member9').removeClass('btn-primary')
        $('#member9').addClass('btn-secondary')
        $('#member10').removeClass('btn-secondary')
        $('#member10').addClass('btn-primary')
        $('#worker_registrationConBtn').removeClass('btn-secondary')
        $('#worker_registrationConBtn').addClass('btn-dark')
    }

    // for member10
    if (memberId == 'member10'){ 
        $('#worker_registrationCon').hide()
        $('#family_member1').hide()
        $('#family_member3').hide()
        $('#family_member4').hide()
        $('#family_member5').hide()
        $('#family_member6').hide()
        $('#family_member7').hide()
        $('#family_member8').hide()
        $('#family_member9').hide()
        $('#family_member2').hide()
        
        $('#familyMemberContainer').show()
        $('#family_member10').show()

        $('#member1').removeClass('btn-secondary')
        $('#member1').addClass('btn-primary')
        $('#member2').removeClass('btn-secondary')
        $('#member2').addClass('btn-primary')
        $('#member3').removeClass('btn-secondary')
        $('#member3').addClass('btn-primary')
        $('#member4').removeClass('btn-secondary')
        $('#member4').addClass('btn-primary')
        $('#member5').removeClass('btn-secondary')
        $('#member5').addClass('btn-primary')
        $('#member6').removeClass('btn-secondary')
        $('#member6').addClass('btn-primary')
        $('#member7').removeClass('btn-secondary')
        $('#member7').addClass('btn-primary')
        $('#member8').removeClass('btn-secondary')
        $('#member8').addClass('btn-primary')
        $('#member9').removeClass('btn-secondary')
        $('#member9').addClass('btn-primary')
        $('#member10').removeClass('btn-primary')
        $('#member10').addClass('btn-secondary')
        $('#worker_registrationConBtn').removeClass('btn-secondary')
        $('#worker_registrationConBtn').addClass('btn-dark')
    }
}
// Function to handle button click


  // Event listener for dynamically added buttons
  $(document).on('click', '[id^="member"]', handleButtonClick);



// Worker Registration worker_registrationConBtn
$(document).ready(function() {
    $('#worker_registrationConBtn').on('click', function(){
        $('#family_member1').hide()
        $('#family_member2').hide()
        $('#family_member3').hide()
        $('#family_member4').hide()
        $('#family_member5').hide()
        $('#family_member6').hide()
        $('#family_member7').hide()
        $('#family_member8').hide()
        $('#family_member9').hide()
        $('#family_member10').hide()

        $('#worker_registrationCon').show()

        $('#member1').removeClass('btn-secondary')
        $('#member1').addClass('btn-primary')
        $('#member2').removeClass('btn-secondary')
        $('#member2').addClass('btn-primary')
        $('#member3').removeClass('btn-secondary')
        $('#member3').addClass('btn-primary')
        $('#member4').removeClass('btn-secondary')
        $('#member4').addClass('btn-primary')
        $('#member5').removeClass('btn-secondary')
        $('#member5').addClass('btn-primary')
        $('#member6').removeClass('btn-secondary')
        $('#member6').addClass('btn-primary')
        $('#member7').removeClass('btn-secondary')
        $('#member7').addClass('btn-primary')
        $('#member8').removeClass('btn-secondary')
        $('#member8').addClass('btn-primary')
        $('#member9').removeClass('btn-secondary')
        $('#member9').addClass('btn-primary')
        $('#member10').removeClass('btn-secondary')
        $('#member10').addClass('btn-primary')
        $('#worker_registrationConBtn').removeClass('btn-dark')
        $('#worker_registrationConBtn').addClass('btn-secondary')
    });
});



$('#awl_name_of_worker').mouseleave(function(){
    var thisV = $(this).val()
    if(thisV == "" || thisV == null){
        $('#awl_name_of_worker').css({"background-color":"#FF6347"})
    }else { 
        $('#awl_name_of_worker').css({"background-color":"white"})   
    } 
})




function addDiv() {
    var div = document.createElement('div');
    div.innerHTML = 'New Div';
    document.getElementById('container').appendChild(div);
}
  
function removeDiv() {
    var container = document.getElementById('container');
    var divs = container.getElementsByTagName('div');
    if (divs.length > 0) {
        container.removeChild(divs[divs.length - 1]);
    }
}



// ------- Worker Data -------------
// =================================
function workerData(){
    let workerDataArr = []
    
    const workerDataObj = {
        awl_worker_registration_no: $('#awl_worker_registration_no').val(),
        no_of_family_member: $('#familyMemberLen').val(),
        awl_worker_legal_status: $('#awl_worker_legal_status').val(),
        awl_name_of_worker: $('#awl_name_of_worker').val(),
        awl_family_name: $('#awl_family_name').val(),
        awl_gender: $('#awl_gender').val(),
        awl_d_o_b: $('#awl_d_o_b').val(),
        awl_place_of_birth: $('#awl_place_of_birth').val(),
        awl_citizenship: $('#awl_citizenship').val(),
        awl_maritial_status: $('#awl_maritial_status').val(),
        awl_point_of_entry: $('#awl_point_of_entry').val(),
        awl_religion: $('#awl_religion').val(),
        awl_race: $('#awl_race').val(),
        awl_worker_contact_no: $('#awl_worker_contact_no').val(),
        awl_worker_email: $('#awl_worker_email').val(),
        awl_name_of_next_kin: $('#awl_name_of_next_kin').val(),
        awl_relationship: $('#awl_relationship').val(),
        awl_nok_contact_no: $('#awl_nok_contact_no').val(),
        awl_employement_details: $('#awl_employement_details').val(),
        awl_job_sector: $('#awl_job_sector').val(),
        awl_job_sub_sector: $('#awl_job_sub_sector').val(),
        awl_employement_sponsorship_status: $('#awl_employement_sponsorship_status').val(),
        awl_address1: $('#awl_address1').val(),
        awl_address2: $('#awl_address2').val(),
        awl_address3: $('#awl_address3').val(),
        awl_city: $('#awl_city').val(),
        awl_state: $('#awl_state').val(),
        awl_working_status: $('#awl_working_status').val()
    }

    workerDataArr.push(workerDataObj)
    $('#workerData').val(JSON.stringify(workerDataArr))
}
// ------- End Worker Data ---------
// =================================



// Workers Document Data
function workerDocs() {
    //$('#submit_worker').click(function(){
    let workersDocArr = []
    let workerDocsLen = $('#workerDocsLen').val();

    for (docsNum=1; docsNum <= workerDocsLen; docsNum++){
        var type_of_documents = $('#type_of_documents' + docsNum).val()
        var document_id = $('#document_id' + docsNum).val()
        var awl_place_of_issue = $('#awl_place_of_issue' + docsNum).val()
        var awl_document_issued_date = $('#awl_document_issued_date' + docsNum).val() 
        var awl_document_expiry_date = $('#awl_document_expiry_date' + docsNum).val() 
        var awl_issuing_country = $('#awl_issuing_country' + docsNum).val()
        var awl_document_status = $('#awl_document_status' + docsNum).val()
        var awl_status_of_current_document = $('#awl_status_of_current_document' + docsNum).val()

        
        docObj = {
            document_link: 'doc' + docsNum,
            type_of_documents: type_of_documents,
            document_id: document_id,
            place_of_issue: awl_place_of_issue,
            document_issued_date: awl_document_issued_date,
            document_expiry_date: awl_document_expiry_date,
            issuing_country: awl_issuing_country,
            document_status: awl_document_status,  
            status_of_current_document: awl_status_of_current_document
        }
        workersDocArr.push(docObj)
    }
    // Add to input box
    $('#docData').val(JSON.stringify(workersDocArr))  
    console.log(workersDocArr) 
} // End Function Of workerDocs
// End Workers Document Data


// Family member & Docs Data
// =========================
function familyMemberData() {
    let fmArr = []
    let familyMemberLen = $('#familyMemberLen').val();

    //alert(familyMemberLen)

    for (fmNum=1; fmNum <= familyMemberLen; fmNum++){

        // Family member Data
        var fm_worker_registration_no = $('#fm_worker_registration_no'+fmNum).val()
        var fm_worker_name = $('#fm_worker_name'+fmNum).val()
        var fm_relationship = $('#fm_relationship'+fmNum).val()

        var fm_name_of_family_member = $('#fm_name_of_family_member'+fmNum).val()
        var fm_family_name = $('#fm_family_name'+fmNum).val()
        var fm_is_family_member_together = $('#fm_is_family_member_together'+fmNum).val()
        var fm_point_of_entry = $('#fm_point_of_entry'+fmNum).val()

        var fm_citizenship = $('#fm_citizenship'+fmNum).val()
        var fm_religion = $('#fm_religion'+fmNum).val()
        var fm_marital_status = $('#fm_marital_status'+fmNum).val()
        var fm_gender = $('#fm_gender'+fmNum).val()

        var fm_address1 = $('#fm_address1'+fmNum).val()
        var fm_address2 = $('#fm_address2'+fmNum).val()
        var fm_address3 = $('#fm_address3'+fmNum).val()
        var fm_postcode = $('#fm_postcode'+fmNum).val()

        var fm_city = $('#fm_city'+fmNum).val()
        var fm_state = $('#fm_state'+fmNum).val()
        var fm_contact_no = $('#fm_contact_no'+fmNum).val()
        var fm_race = $('#fm_race'+fmNum).val()

        var fm_place_of_birth = $('#fm_place_of_birth'+fmNum).val()
        var fm_dob = $('#fm_dob'+fmNum).val()
        var fm_employment_status = $('#fm_employment_status'+fmNum).val()
        var fm_same_employer_as_worker = $('#fm_same_employer_as_worker'+fmNum).val()

        var fm_employer_name = $('#fm_employer_name'+fmNum).val()
        var fm_employer_address = $('#fm_employer_address'+fmNum).val()

        fmObj = {
            fm_worker_registration_no : fm_worker_registration_no,
            fm_worker_name : fm_worker_name,
            fm_relationship : fm_relationship,
            fm_name_of_family_member : fm_name_of_family_member,
            fm_family_name : fm_family_name,
            fm_is_family_member_together : fm_is_family_member_together,
            fm_point_of_entry : fm_point_of_entry,
            fm_citizenship : fm_citizenship,
            fm_religion : fm_religion,
            fm_marital_status : fm_marital_status,
            fm_gender : fm_gender,
            fm_address1 : fm_address1,
            fm_address2 : fm_address2,
            fm_address3 : fm_address3,
            fm_postcode : fm_postcode,
            fm_city : fm_city,
            fm_state : fm_state,
            fm_contact_no : fm_contact_no,
            fm_race : fm_race,
            fm_place_of_birth : fm_place_of_birth,
            fm_dob : fm_dob,
            fm_employment_status : fm_employment_status,
            fm_same_employer_as_worker : fm_same_employer_as_worker,
            fm_employer_name : fm_employer_name,
            fm_employer_address : fm_employer_address
        }

        fmArr.push(fmObj);
    }
    
    $('#familyMemberData').val(JSON.stringify(fmArr));  
    //alert(JSON.stringify(fmArr));
}
// End Family member & Docs Data
// =============================

// ================
// FM Document Data
// ================
function fm_docs() {
    //$('#submit_worker').click(function(){
    let fm_docArr = []
    let familyMemberLen = $('#familyMemberLen').val();
    
    for (fm=1; fm <= familyMemberLen; fm++){
        // fm docs len
        let fm_docsLen = $('#fMember_docsLen'+ fm).val();

        for (let fm_dCount=1; fm_dCount <= fm_docsLen; fm_dCount++){

            var type_of_documents = $('#fm_type_of_documents' + fm + fm_dCount).val()
            var document_id = $('#fm_document_id' + fm + fm_dCount).val()
            var awl_place_of_issue = $('#fm_place_of_issue' + fm+ fm_dCount).val()
            var awl_document_issued_date = $('#fm_document_issued_date' + fm+ fm_dCount).val() 
            var awl_document_expiry_date = $('#fm_document_expiry_date' + fm+ fm_dCount).val() 
            var awl_issuing_country = $('#fm_issuing_country' + fm+ fm_dCount).val()
            var awl_document_status = $('#fm_document_status' + fm+ fm_dCount).val()
            var awl_status_of_current_document = $('#fm_status_of_current_document' + fm+ fm_dCount).val()
            var fm_reg_no = $('#fm_worker_registration_no'+ fm).val()
            
            docObj = {
                document_link: 'doc' + fm_dCount,
                type_of_documents: type_of_documents,
                document_id: document_id,
                place_of_issue: awl_place_of_issue,
                document_issued_date: awl_document_issued_date,
                document_expiry_date: awl_document_expiry_date,
                issuing_country: awl_issuing_country,
                document_status: awl_document_status,  
                status_of_current_document: awl_status_of_current_document,
                fm_reg_no: fm_reg_no
            }
            fm_docArr.push(docObj)
        }
        
    }
    // Add to input box
    $('#familyMemberDocs').val(JSON.stringify(fm_docArr))  
    console.log(fm_docArr)
}
// ====================
// End FM Document Data
// ====================



function insertWorker(){
    workerData();
    workerDocs();
    familyMemberData();
    fm_docs();
}

function insertWorkerWithFamily(){
    workerData();
    workerDocs();
    familyMemberData();
    fm_docs();
}



function tPass() {
    var passwordInput = document.getElementById("pwd");
    var showPasswordCheckbox = document.getElementById("showPassword");

    if (showPasswordCheckbox.checked) {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}


// Add worker Form Validator
function validateWorker() {
    awl_worker_registration_no = $('#awl_worker_registration_no').val(),
    awl_worker_legal_status = $('#awl_worker_legal_status').val(),
    awl_name_of_worker = $('#awl_name_of_worker').val(),
    awl_family_name = $('#awl_family_name').val(),
    awl_gender = $('#awl_gender').val(),
    awl_d_o_b = $('#awl_d_o_b').val(),
    awl_place_of_birth = $('#awl_place_of_birth').val(),
    awl_citizenship = $('#awl_citizenship').val(),
    awl_maritial_status = $('#awl_maritial_status').val(),
    awl_point_of_entry = $('#awl_point_of_entry').val(),
    awl_religion = $('#awl_religion').val(),
    awl_race = $('#awl_race').val(),
    //awl_worker_contact_no = $('#awl_worker_contact_no').val(),
    awl_worker_email = $('#awl_worker_email').val(),
    //awl_name_of_next_kin = $('#awl_name_of_next_kin').val(),
    //awl_relationship = $('#awl_relationship').val(),
    //awl_nok_contact_no = $('#awl_nok_contact_no').val(),
    awl_employement_details = $('#awl_employement_details').val(),
    awl_job_sector = $('#awl_job_sector').val(),
    //awl_job_sub_sector = $('#awl_job_sub_sector').val(),
    awl_employement_sponsorship_status = $('#awl_employement_sponsorship_status').val(),
    awl_address1 = $('#awl_address1').val(),
    awl_address2 = $('#awl_address2').val(),
    awl_address3 = $('#awl_address3').val(),
    awl_city = $('#awl_city').val(),
    awl_state = $('#awl_state').val(),
    awl_working_status = $('#awl_working_status').val()


    const fieldsToCheck = [
        { value: awl_worker_registration_no, name: 'Worker Registration No' },
        { value: awl_worker_legal_status, name: 'Legal Status' },
        { value: awl_name_of_worker, name: 'Name of Worker' },
        { value: awl_family_name, name: 'Family Name' },
        { value: awl_gender, name: 'Gender' },
        { value: awl_d_o_b, name: 'Date of Birth' },
        { value: awl_place_of_birth, name: 'Place of Birth' },
        { value: awl_citizenship, name: 'Citizenship' },
        { value: awl_maritial_status, name: 'Marital Status' },
        { value: awl_point_of_entry, name: 'Point of Entry' },
        { value: awl_religion, name: 'Religion' },
        { value: awl_race, name: 'Race' },
        //{ value: awl_worker_contact_no, name: 'Worker Contact No' },
        { value: awl_worker_email, name: 'Worker E-mail' },
        //{ value: awl_name_of_next_kin, name: 'Name of Next KIN' },
        //{ value: awl_relationship, name: 'Relationship' },
        //{ value: awl_nok_contact_no, name: 'NOK Contact No' },
        { value: awl_employement_details, name: 'Employment Details' },
        { value: awl_job_sector, name: 'Sector' },
        //{ value: awl_job_sub_sector, name: 'Sub Sector' },
        { value: awl_employement_sponsorship_status, name: 'Employment Sponsorship Status' },
        { value: awl_address1, name: 'Address 1' },
        { value: awl_address2, name: 'Address 2' },
        { value: awl_address3, name: 'Address 3' },
        { value: awl_city, name: 'City' },
        { value: awl_state, name: 'State' },
        { value: awl_working_status, name: 'Working Status' }
    ];

    for (const field of fieldsToCheck) {
        if (field.value === '' || field.value === null) {
            alert(field.name + ' is blank');
            return false;
        }
    }
    return true;
}

// End * Worker Form Validator


// ===========================
// Workers Document Validation
// ===========================

function validateWorkerDocs() {
    let workersDocArr = []

    const workerDocsLen = $('#workerDocsLen').val()

    // Check Docs Status
    for (docsNum=1; docsNum <= workerDocsLen; docsNum++) {
        
        // Worker Docs
        var type_of_documents = $('#type_of_documents' + docsNum).val()
        var document_id = $('#document_id' + docsNum).val()
        var awl_place_of_issue = $('#awl_place_of_issue' + docsNum).val()
        var awl_document_issued_date = $('#awl_document_issued_date' + docsNum).val() 
        var awl_document_expiry_date = $('#awl_document_expiry_date' + docsNum).val() 
        var awl_issuing_country = $('#awl_issuing_country' + docsNum).val()
        var awl_document_status = $('#awl_document_status' + docsNum).val()
        var awl_status_of_current_document = $('#awl_status_of_current_document' + docsNum).val()

        
        docObj = [
            {value: 'doc ' + docsNum, name: docsNum + ', Document'+ docsNum},
            {value: type_of_documents, name: docsNum + ', Type of Document'},
            {value: document_id, name: docsNum + ', Document ID'},
            {value: awl_place_of_issue, name: docsNum + ', Place of Issue'},
            {value: awl_document_issued_date, name: docsNum + ', Document Issued Date'},
            {value: awl_document_expiry_date, name: docsNum + ', Document Expiry Date'},
            {value: awl_issuing_country, name: docsNum + ', Issuing Country'},
            {value: awl_document_status, name: docsNum + ', Document Status'},  
            {value: awl_status_of_current_document, name: docsNum + ', Status of Current Document'}
        ]
        
        workersDocArr.push(docObj)
        
    } 
    // End * Check Docs Status
    
    for (const field of workersDocArr) {
        // Inner
        for (const inner of field){
            if (inner.value === '' || inner.value === null) {
                alert('In Worker Document ' + inner.name + ' is blank');
                return false;
            }
        }
        // End Inner
    }

    return true
} // End Function Of workerDocs

// ==================================
// End *  Workers Document Validation
// ==================================


// ======================================
// Validation * Family member & Docs Data
// ======================================
function validateFamilyMemberData() {
    let fmArr = []
    let familyMemberLen = $('#familyMemberLen').val();

    //alert(familyMemberLen)

    for (fmNum=1; fmNum <= familyMemberLen; fmNum++){

        // Family member Data
        var fm_worker_registration_no = $('#fm_worker_registration_no'+fmNum).val()
        var fm_worker_name = $('#fm_worker_name'+fmNum).val()
        var fm_relationship = $('#fm_relationship'+fmNum).val()

        var fm_name_of_family_member = $('#fm_name_of_family_member'+fmNum).val()
        var fm_family_name = $('#fm_family_name'+fmNum).val()
        var fm_is_family_member_together = $('#fm_is_family_member_together'+fmNum).val()
        var fm_point_of_entry = $('#fm_point_of_entry'+fmNum).val()

        var fm_citizenship = $('#fm_citizenship'+fmNum).val()
        var fm_religion = $('#fm_religion'+fmNum).val()
        var fm_marital_status = $('#fm_marital_status'+fmNum).val()
        var fm_gender = $('#fm_gender'+fmNum).val()

        var fm_address1 = $('#fm_address1'+fmNum).val()
        var fm_address2 = $('#fm_address2'+fmNum).val()
        var fm_address3 = $('#fm_address3'+fmNum).val()
        var fm_postcode = $('#fm_postcode'+fmNum).val()

        var fm_city = $('#fm_city'+fmNum).val()
        var fm_state = $('#fm_state'+fmNum).val()
        var fm_contact_no = $('#fm_contact_no'+fmNum).val()
        var fm_race = $('#fm_race'+fmNum).val()

        var fm_place_of_birth = $('#fm_place_of_birth'+fmNum).val()
        var fm_dob = $('#fm_dob'+fmNum).val()
        var fm_employment_status = $('#fm_employment_status'+fmNum).val()
        //var fm_same_employer_as_worker = $('#fm_same_employer_as_worker'+fmNum).val()

        //var fm_employer_name = $('#fm_employer_name'+fmNum).val()
        //var fm_employer_address = $('#fm_employer_address'+fmNum).val() 


        fmObj = [
            {value : fm_worker_registration_no, name: fmNum + 'Sorry, we did not find Registration No of Family Member ' + fmNum },
            {value : fm_worker_name, name: 'In Family Member ' + fmNum + ', Worker Name is blank!'},
            {value : fm_relationship, name: 'In Family Member ' + fmNum + ', Relationship is blank!'},
            {value : fm_name_of_family_member, name: 'In Family Member ' + fmNum + ', Name of Family Member is blank!'},
            {value : fm_family_name, name: 'In Family Member ' + fmNum + ', Family Name is blank!'},
            {value : fm_is_family_member_together, name: 'In Family Member ' + fmNum + ', is Family Member Together is blank!'},
            {value : fm_point_of_entry, name: 'In Family Member ' + fmNum + ', Point of Entry is blank!'},
            {value : fm_citizenship, name: 'In Family Member ' + fmNum + ', Citizenship is blank!'},
            {value : fm_religion, name: 'In Family Member ' + fmNum + ', Religion is blank!'},
            {value : fm_marital_status, name: 'In Family Member ' + fmNum + ', Marital Status is blank!'},
            {value : fm_gender, name: 'In Family Member ' + fmNum + ', Gender is blank!'},
            {value : fm_address1 , name: 'In Family Member ' + fmNum + ', Address 1 is blank!'},
            {value : fm_address2, name: 'In Family Member ' + fmNum + ', Address 2 is blank!'},
            {value : fm_address3, name: 'In Family Member ' + fmNum + ', Address 3 is blank!'},
            {value : fm_postcode, name: 'In Family Member ' + fmNum + ', Postcode is blank!'},
            {value : fm_city, name: 'In Family Member ' + fmNum + ', City is blank!'},
            {value : fm_state, name: 'In Family Member ' + fmNum + ', State is blank!'},
            {value : fm_contact_no, name: 'In Family Member ' + fmNum + ', Contact No is blank!'},
            {value : fm_race, name: 'In Family Member ' + fmNum + ', Race is blank!'},
            {value : fm_place_of_birth, name: 'In Family Member ' + fmNum + ', Place of Birth is blank!'},
            {value : fm_dob, name: 'In Family Member ' + fmNum + ', Date of Birth is blank!'},
            {value : fm_employment_status, name: 'In Family Member ' + fmNum + ', Employment Status is blank!'}
            //{value : fm_same_employer_as_worker, name: 'In Family Member ' + fmNum + ', Same Employer as Worker is blank!'},
            //{value : fm_employer_name, name: 'In Family Member ' + fmNum + ', Employer Name is blank!'},
            //{value : fm_employer_address, name: 'In Family Member ' + fmNum + ', Employer Address is blank!'}
        ]

        fmArr.push(fmObj);
    }

    for (const field of fmArr) {
        // Inner
        for (const inner of field){
            if (inner.value === '' || inner.value === null) {
                alert(inner.name);
                return false;
            }
        }
        // End Inner
    }

    if (familyMemberLen >= 1){
        return true;
    }else {
        return false
    }
}
// ==========================================
// End * Validation Family member & Docs Data
// ==========================================



// For date format
