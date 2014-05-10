$(document).ready(function(){
	var $firstName = $("#logPatientInFirstNameInput");
	var $lastName = $("#logPatientInLastNameInput");
	var $nationalCode = $("#logPatientInNationalCodeInput");
	var $loginButton = $("#logPatientInSubmitButton");
	
	$("#logPatientInFirstNameInput, #logPatientInLastNameInput").on('blur', function() {
		if( !$firstName.val() || !$lastName.val()) { 
			$loginButton.attr('disabled', 'disabled');	
			$firstName.parent().removeClass('has-success');
			$lastName.parent().removeClass('has-success');
			$nationalCode.parent().removeClass('has-success');
			return ;
			}
		$.ajax({
			type: "POST",
			url: "/ajax/find_patients/",
			data: {first_name:$firstName.val(), last_name:$lastName.val()},
			dataType: 'json',
			success: function(data){
				if(data.success) {
					if (data.count === 0) {
						$firstName.parent().removeClass('has-success').addClass('has-error');
						$lastName.parent().removeClass('has-success').addClass('has-error');
						$nationalCode.val("");
						$nationalCode.parent().removeClass('has-success');
						$loginButton.attr('disabled', 'disabled');	
					}
					else if(data.count === 1) {
						$firstName.parent().removeClass('has-error').addClass('has-success');
						$lastName.parent().removeClass('has-error').addClass('has-success');
						$nationalCode.parent().removeClass('has-error').addClass('has-success');
						$nationalCode.val(data.patients[0].national_code);
						$loginButton.removeAttr("disabled");
						
					}
					else {
						//TODO: Modal
					}
				}
				else {
					//TODO:
				}
			}
		});
	});
	
	$nationalCode.on('blur', function(){
		if( !$nationalCode.val()) return ;
		$.ajax({
			type: "POST", 
			url: "/ajax/find_patients/",
			data: {national_code: $nationalCode.val()},
			dataType: 'json',
			success: function(data) {
				if(data.success) {
					if(data.count === 0) {
						$nationalCode.parent().removeClass('has-success').addClass('has-error');
						$firstName.parent().removeClass('has-success');
						$lastName.parent().removeClass('has-success');
						$firstName.val("");
						$lastName.val("");
						$loginButton.attr("disabled", "disabled");
					}
					else {
						$nationalCode.parent().removeClass('has-error').addClass('has-success');
						$firstName.parent().removeClass('has-error').addClass('has-success') ;
						$lastName.parent().removeClass('has-error').addClass('has-success');
						$firstName.val(data.patients[0].first_name);
						$lastName.val(data.patients[0].last_name);
						$loginButton.removeAttr("disabled");
					}
				}
				else {
					//TODO: 
				}
			}
			
			
		});
	});
});
