// Staff Connection
$(document).ready(function(){
    var loginContr = $('#loginContr')
    var serverContr = $('#serverContr')

    $('#staffSettingsBtn').click(function(){
       loginContr.hide()
       serverContr.show() 
    })

})


$('#newRegWorNum').hide();
$('#newRegistrationNumBtn').on('click', function(){
    function genNumber() {
        const min = 100000; // Minimum 6-digit number (100000)
        const max = 999999; // Maximum 6-digit number (999999)
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
    var newNum = genNumber();
    var newNum = `TEMP${newNum}`
    $('#newRegWorNum').val(newNum);
    $('#newRegWorNum').show()
});

