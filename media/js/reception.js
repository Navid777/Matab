$(document).ready(function() {
	var $patientFirstName = $("#patientFirstNameInput");
	var $patientLastName = $("#patientLastNameInput");
	var $patientNationalCode = $("#patientNationalCodeInput");
	$patientNationalCode.on('blur', function() {
		if (!$patientNationalCode.val())
			return;
		$.ajax({
			type : "POST",
			url : "/ajax/find_patients/",
			data : {
				national_code : $patientNationalCode.val()
			},
			dataType : 'json',
			success : function(data) {
				if (data.success) {
					if (data.count === 0) {
						$patientFirstName.parent().removeClass('has-success');
						$patientLastName.parent().removeClass('has-success');
						$patientNationalCode.parent().removeClass('has-success').addClass('has-error');
						$("#registerPatientModal").modal('show');
					} else {
						$patientFirstName.parent().removeClass('has-error');
						$patientLastName.parent().removeClass('has-error');
						$patientNationalCode.parent().removeClass('has-error').addClass('has-success');
						$patientFirstName.val(data.patients[0].first_name);
						$patientLastName.val(data.patients[0].last_name);
						$("#insuranceTypeSelect").focus();
					}
				} else {
					//TODO
				}
			}
		});
	});

	$("#patientFirstNameInput, #patientLastNameInput").on('blur', function() {
		if (!$patientFirstName.val() || !$patientLastName.val())
			return;
		$.ajax({
			type : "POST",
			url : "/ajax/find_patients/",
			data : {
				first_name : $patientFirstName.val(),
				last_name : $patientLastName.val()
			},
			dataType : 'json',
			success : function(data) {
				if (data.success) {
					if (data.count === 0) {
						$patientFirstName.parent().removeClass('has-success').addClass('has-error');
						$patientLastName.parent().removeClass('has-success').addClass('has-error');
						$patientNationalCode.val("");
					} else if (data.count === 1) {
						$patientFirstName.parent().removeClass('has-error').addClass('has-success');
						$patientLastName.parent().removeClass('has-error').addClass('has-success');
						$patientNationalCode.val(data.patients[0].national_code);
					} else {
						//TODO: modal
					}
				} else {
					//TODO
				}
			}
		});
	});

	var $insuranceType = $("#insuranceTypeSelect");
	var $insuranceCategory = $("#insuranceCategorySelect");
	var $insuranceHasComplementary = $("#insuranceHasComplementaryCheckbox");
	var $insuranceComplementary = $("#insuranceComplementarySelect");

	$insuranceType.on('change', function() {
		$insuranceCategory.html("<option value='' selected></option>");
		$insuranceHasComplementary.prop('checked', false);
		$.ajax({
			type : "POST",
			url : "/ajax/find_insurances/",
			data : {
				type : $insuranceType.val()
			},
			dataType : 'json',
			success : function(data) {
				if (data.success) {
					for (var i in data.categories) {
						$insuranceCategory.append('<option value="' + data.categories[i] + '">' + data.categories[i] + '</option>');
					}
				} else {
					//TODO
				}
			}
		});
	});
	/*    $insuranceCategory.on('change', function() {
	 $insuranceComplementary.attr('disabled', 'disabled');
	 $insuranceComplementary.html("<option value='' selected></option>");
	 $insuranceHasComplementary.prop('checked', false);
	 $.ajax({
	 type: "POST",
	 url: "/ajax/find_insurances/",
	 data: {type: $insuranceType.val(), category: $insuranceCategory.val()},
	 dataType: 'json',
	 success: function(data) {
	 if (data.success) {
	 if (data.has_complementaries.length == 1) {
	 if (data.has_complementaries[0] === "False") {
	 $insuranceHasComplementary.prop('checked', false);
	 $insuranceHasComplementary.attr('disabled', 'disabled');
	 } else {
	 $insuranceHasComplementary.prop('checked', true);
	 $insuranceHasComplementary.attr('disabled', 'disabled');
	 $insuranceComplementary.removeAttr('disabled');
	 }
	 } else {
	 $insuranceHasComplementary.removeAttr('disabled');
	 }
	 for(var i in data.complementaries) {
	 $insuranceComplementary.append(
	 '<option value="' + data.complementaries[i] + '">'
	 + data.complementaries[i] + '</option>'
	 );
	 }
	 }
	 }
	 });
	 });
	 */
	$insuranceHasComplementary.on('change', function() {
		if (!$insuranceHasComplementary.prop('checked')) {
			$insuranceComplementary.attr('disabled', 'disabled');
		} else {
			$insuranceComplementary.removeAttr('disabled');
		}
	});

	var $therapistFirstName = $("#therapistFirstNameInput");
	var $therapistLastName = $("#therapistLastNameInput");
	var $therapistMedicalNumber = $("#therapistMedicalNumberInput");

	$therapistMedicalNumber.on('blur', function() {
		if (!$therapistMedicalNumber.val())
			return;
		$.ajax({
			type : "POST",
			url : "/ajax/find_therapists/",
			data : {
				medical_number : $therapistMedicalNumber.val()
			},
			dataType : 'json',
			success : function(data) {
				if (data.success) {
					if (data.count === 0) {
						$therapistFirstName.parent().removeClass('has-success');
						$therapistLastName.parent().removeClass('has-success');
						$therapistMedicalNumber.parent().removeClass('has-success').addClass('has-error');
						$therapistModal.modal('show');
						$("#registerTherapistMedicalNumber").val($therapistMedicalNumber.val());
						$therapistFirstName.val("");
						$therapistLastName.val("");
					} else {
						$therapistFirstName.parent().removeClass('has-error');
						$therapistLastName.parent().removeClass('has-error');
						$therapistMedicalNumber.parent().removeClass('has-error').addClass('has-success');
						$therapistFirstName.val(data.therapists[0].first_name);
						$therapistLastName.val(data.therapists[0].last_name);
						$("#therapistVisitDateDisplay").focus();
					}
				} else {
					//TODO
				}
			}
		});
	});

	$("#therapistFirstNameInput, #therapistLastNameInput").on('blur', function() {
		if (!$therapistFirstName.val() || !$therapistLastName.val())
			return;
		$.ajax({
			type : "POST",
			url : "/ajax/find_therapists/",
			data : {
				first_name : $therapistFirstName.val(),
				last_name : $therapistLastName.val()
			},
			dataType : 'json',
			success : function(data) {
				if (data.success) {
					if (data.count === 0) {
						$therapistFirstName.parent().removeClass('has-success').addClass('has-error');
						$therapistLastName.parent().removeClass('has-success').addClass('has-error');
					} else if (data.count === 1) {
						$therapistFirstName.parent().removeClass('has-error').addClass('has-success');
						$therapistLastName.parent().removeClass('has-error').addClass('has-success');
						$therapistMedicalNumber.val(data.therapists[0].medical_number);
					} else {
						//TODO: modal
					}
				} else {
					//TODO
				}
			}
		});
	});

	var $operationType = $("#operationTypeSelect");
	var $operationCodeography = $("#operationCodeographyInput");
	var $operationName = $("#operationNameSelect");
	$operationName.select2();

	$operationType.on('change', function() {
		$operationName.html("<option value='' selected></option>");
		$operationCodeography.val("");
		$.ajax({
			type : "POST",
			url : "/ajax/find_operations/",
			data : {
				type : $operationType.val()
			},
			dataType : 'json',
			success : function(data) {
				if (data.success) {
					for (var i in data.names) {
						$operationName.append('<option value="' + data.names[i] + '">' + data.names[i] + '</option>');
					}
				} else {
					//TODO
				}
			}
		});
	});

	var map = $operationName.on("change",function(){
	    var comp = $("#operationNameSelect option:selected").map(function() {
	    		var result = {
	    				id: $(this).attr('value'),
	    				governmental: $(this).attr("governmental_fee"),
	    				individual: $(this).attr("individual_fee"),
	    				medical: $(this).attr("medical_fee")
	    		};
	            return result;
	        }).get(),
	        set1 = map.filter(function(i) {
	            //return comp.indexOf(i) < 0;
	            var result = true;
	            for(j=0; j<comp.length; j++)
	            {
	            	if (i['id'] == comp[j]['id']) result=false;
	            }
	            return result;
	        }),
	        set2 = comp.filter(function(i) {
	            //return map.indexOf(i) < 0;
	            var result = true;
	            for(j=0; j<map.length; j++)
	            {
	            	if (i['id'] == map[j]['id']) result=false;
	            }
	            return result;
	        }),
	    	last = (set1.length > set2.length ? set1 : set2)[0];
	    map = comp;
	    var current_governmental = $("#dashboard_governmental").text();
	    var current_individual = $("#dashboard_individual").text();
	    var current_medical = $("#dashboard_medical").text();
	    if (set1.length > set2.length){
	    	$("#dashboard_governmental").text(parseFloat(current_governmental)-parseFloat(last['governmental']));
	    	$("#dashboard_individual").text(parseFloat(current_individual)-parseFloat(last['individual']));
	    	$("#dashboard_medical").text(parseFloat(current_medical)-parseFloat(last['medical']));
	    }
	    else {
	    	$("#dashboard_governmental").text(parseFloat(current_governmental)+parseFloat(last['governmental']));
	    	$("#dashboard_individual").text(parseFloat(current_individual)+parseFloat(last['individual']));
	    	$("#dashboard_medical").text(parseFloat(current_medical)+parseFloat(last['medical'])); 
	    }
	
	    // "last" contains the last one selected /unselected
	
	}).find('option:selected').map(function() {var result = {
						id: $(this).attr('value'),
	    				governmental: $(this).attr("governmental_fee"),
	    				individual: $(this).attr("individual_fee"),
	    				medical: $(this).attr("medical_fee")
	    		};
	            return result;});

	$operationCodeography.on('keypress', function(e) {
		if (e.keyCode == 13) {
			$(".calendar").css("display","none");
			if (!$operationCodeography.val())
				return;
			$.ajax({
				type : "POST",
				url : "/ajax/find_operations/",
				data : {
					codeography : $operationCodeography.val()
				},
				dataType : 'json',
				success : function(data) {
					if (data.success) {
						if (data.count === 0) {
							$operationCodeography.val("");
						} else {
							//if ($operationType.find("option[value='" + data.operation.type + "']").length > 0) {
							//	$operationType.find("option[value='" + data.operation.type + "']").prop("selected", true);
							//}
							if ($operationName.find("option[value='" + data.operation.id + "']").length > 0) {
								$operationName.find("option[value='" + data.operation.id + "']").prop("selected", true);
							}
							$operationCodeography.val("");
							// else {
							//	$operationName.append("<option value='" + data.operation.name + "'>" + data.operation.name + "</option>");
							//	$operationName.find("option[value='" + data.operation.name + "']").prop('selected', true);
							//}
							//$("#operationCommentInput").focus();
						}
					} else {
						//TODO
					}
				}
			});
		}
	});
	
	$operationCodeography.on("blur", function(){
		$("#operationCommentInput").focus();
	});

	var $patientForm = $("#registerPatientModal").find('form');
	var $patientModal = $("#registerPatientModal");
	$patientModal.on('shown.bs.modal', function() {
		$patientModal.find("#registerPatientFirstNameInput").val($patientFirstName.val());
		$patientModal.find("#registerPatientLastNameInput").val($patientLastName.val());
		$patientModal.find("#registerPatientNationalCodeInput").val($patientNationalCode.val());
		$patientModal.find("#registerPatientFirstNameInput").focus();
	});
	$("#registerPatientSubmit").on('click', function() {
		$.ajax({
			type : "POST",
			url : $patientForm.attr('action'),
			data : $patientForm.serialize(),
			dataType : 'json',
			success : function(data) {
				if (data.success) {
					$patientFirstName.val(data.patient.first_name);
					$patientLastName.val(data.patient.last_name);
					$patientNationalCode.val(data.patient.national_code);
					$("#registerPatientModal").modal('hide');
					$insuranceType.focus();
				} else {
					//TODO:
					alert(data.errors);
				}
			}
		});
	});

	var $complementaryInsuranceModal = $("#registerComplementaryInsuranceModal");
	var $complementaryInsuranceForm = $complementaryInsuranceModal.find('form');
	$complementaryInsuranceModal.on("show.bs.modal", function() {
		$complementaryInsuranceModal.find("#registerComplementaryInsuranceTypeInput").focus();
	});
	$("#registerComplementaryInsuranceSubmit").on('click', function() {
		$.ajax({
			type : "POST",
			url : $complementaryInsuranceForm.attr('action'),
			data : $complementaryInsuranceForm.serialize(),
			dataType : 'json',
			success : function(data) {
				if (data.success) {
					$insuranceComplementary.find("option:selected").prop("selected", false);
					if ($insuranceComplementary.find("option[value='" + data.complementary_insurance.type + "']").length > 0) {
						$insuranceComplementary.find("option[value='" + data.complementary_insurance.type + "']").prop("selected", true);
					} else {
						$insuranceComplementary.append("<option value='" + data.complementary_insurance.type + "' selected>" + data.complementary_insurance.type + "</option>");
						$insuranceComplementary.focus();
						$insuranceComplementary.removeAttr('disabled');
						$insuranceHasComplementary.prop('checked', true);
						$("#registerComplementaryInsuranceModal").modal('hide');
					}
				}
			}
		});
	});

	var $insuranceModal = $("#registerInsuranceModal");
	var $insuranceForm = $insuranceModal.find('form');
	$insuranceModal.on('shown.bs.modal', function() {
		$insuranceModal.find("#registerInsuranceTypeInput").focus();
	});
	$("#registerInsuranceSubmit").on('click', function() {
		$.ajax({
			type : "POST",
			url : $insuranceForm.attr('action'),
			data : $insuranceForm.serialize(),
			dataType : 'json',
			success : function(data) {
				if (data.success) {
					$insuranceType.find("option:selected").prop("selected", false);
					if ($insuranceType.find("option[value='" + data.insurance.type + "']").length > 0) {
						$insuranceType.find("option[value='" + data.insurance.type + "']").prop("selected", true);
					} else {
						$insuranceType.append("<option value='" + data.insurance.type + "' selected>" + data.insurance.type + "</option>");
					}
					$insuranceType.trigger('change');
					$insuranceType.focus();
					$("#registerInsuranceModal").modal('hide');
					//TODO: FILL OTHER FIELDS
				} else {
					//TODO
					alert(data.errors);
				}
			}
		});
	});

	var $therapistModal = $("#registerTherapistModal");
	var $therapistForm = $therapistModal.find('form');
	$therapistModal.on('shown.bs.modal', function() {
		$therapistModal.find("#registerTherapistFirstNameInput").focus();
	});
	$("#registerTherapistSubmit").on('click', function() {
		$.ajax({
			type : "POST",
			url : $therapistForm.attr('action'),
			data : $therapistForm.serialize(),
			dataType : 'json',
			success : function(data) {
				if (data.success) {
					$therapistFirstName.val(data.therapist.first_name);
					$therapistLastName.val(data.therapist.last_name);
					$therapistMedicalNumber.val(data.therapist.medical_number);
					$("#registerTherapistModal").modal('hide');
				} else {
					//TODO:
					alert(data.errors);
				}
			}
		});
	});

	var $operationModal = $("#registerOperationModal");
	var $operationForm = $operationModal.find('form');
	$operationModal.on('shown.bs.modal', function() {
		$operationModal.find("#registerOperationTypeInput").focus();
	});
	$("#registerOperationSubmit").on('click', function() {
		$.ajax({
			type : "POST",
			url : $operationForm.attr('action'),
			data : $operationForm.serialize(),
			dataType : 'json',
			success : function(data) {
				if (data.success) {
					$("#registerOperationModal").modal('hide');
				} else {
					//TODO:
					alert(data.errors);
				}
			}
		});
	});
	$("#therapistVisitDateDisplay").on('focus', function() {
		$("#therapistVisitDateDisplay").trigger('click');
	});
	$("#insuranceExpDateDisplay").on('focus', function() {
		$("#insuranceExpDateDisplay").trigger('click');
	});
});
