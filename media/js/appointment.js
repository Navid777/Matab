$(document).ready(function(){
	var $appointmentForm = $("#registerAppointmentModal").find("form");
	var $firstName = $("#registerAppointmentFirstNameInput");
	var $lastName = $("#registerAppointmentLastNameInput");
	var $nationalCode = $("#registerAppointmentNationalCodeInput");
	var $submitButton = $("#registerAppointmentSubmit");
	var $patientList = $("#patient_list");
	var $template = $("#row-template").html();
	
	$submitButton.on('click', function(){
		$.ajax({
    		type: "POST",
    		url: $appointmentForm.attr('action'),
    		data: $appointmentForm.serialize(),
    		dataType: 'json',
    		success: function(data){
    			if(data.success) {
    				$patientList.append($template.replace("###first_name###", data.appointment.first_name)
    						.replace("###last_name###", data.appointment.last_name)
    						.replace("###national_code###", data.appointment.national_code)
    						.replace("###start_time###", data.appointment.start_time));
    						
    				$("#registerAppointmentModal").modal('hide');
    			}
    		}
    		
    	});
	});
	    var update = function() {

        var $template = $("#row-template").html();
        $.ajax({
            type: 'POST',
            url: '/ajax/find_patients_list/',
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    $patientList.html("");
                    for (var i in data.turns) {
                        var t = data.turns[i];
                        $patientList.append($template.replace("###first_name###", t.first_name)
                            .replace("###last_name###", t.last_name)
                            .replace("###national_code###", t.national_code)
                            .replace("###url###", t.url));
                    }
                } else {
                    //TODO
                }
            }
        });
    };
});
