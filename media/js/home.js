$(document).ready(function() {
    var $patientFirstName = $("#patientFirstNameInput");
    var $patientLastName = $("#patientLastNameInput");
    var $patientNationalCode = $("#patientNationalCodeInput");
    $patientNationalCode.on('blur', function() {
        if (!$patientNationalCode.val()) return;
        $.ajax({
            type: "POST",
            url: "/ajax/find_patients/",
            data: {national_code: $patientNationalCode.val()},
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    if (data.count === 0) {
                        $patientFirstName.parent().removeClass('has-success');
                        $patientLastName.parent().removeClass('has-success');
                        $patientNationalCode.parent().removeClass('has-success').addClass('has-error');
                        $patientFirstName.val("");
                        $patientLastName.val("");
                    } else {
                        $patientFirstName.parent().removeClass('has-error');
                        $patientLastName.parent().removeClass('has-error');
                        $patientNationalCode.parent().removeClass('has-error').addClass('has-success');
                        $patientFirstName.val(data.patients[0].first_name);
                        $patientLastName.val(data.patients[0].last_name);
                    }
                } else {
                    //TODO
                }
            }
        });
    });

    $("#patientFirstNameInput, #patientLastNameInput").on('blur', function() {
        if (!$patientFirstName.val() || !$patientLastName.val()) return;
        $.ajax({
            type: "POST",
            url: "/ajax/find_patients/",
            data: {first_name: $patientFirstName.val(), last_name: $patientLastName.val()},
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    if (data.count === 0) {
                        $patientFirstName.parent().removeClass('has-success').addClass('has-error');
                        $patientLastName.parent().removeClass('has-success').addClass('has-error');
                        $patientNationalCode.val("");
                    } else if(data.count === 1) {
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
        $insuranceHasComplementary.attr('disabled', 'disabled');
        $insuranceComplementary.attr('disabled', 'disabled');
        $insuranceComplementary.html("<option value='' selected></option>");
        $.ajax({
            type: "POST",
            url: "/ajax/find_insurances/",
            data: {type: $insuranceType.val()},
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    for (var i in data.categories) {
                        $insuranceCategory.append(
                            '<option value="' + data.categories[i] + '">'
                                + data.categories[i] + '</option>'
                        );
                    }
                } else {
                    //TODO
                }
            }
        });
    });
    $insuranceCategory.on('change', function() {
        $insuranceComplementary.attr('disabled', 'disabled');
        $insuranceComplementary.html("<option value='' selected></option>");
        $insuranceHasComplementary.prop('checked', false);
        $insuranceHasComplementary.attr('disabled', 'disabled');
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
        if (!$therapistMedicalNumber.val()) return;
        $.ajax({
            type: "POST",
            url: "/ajax/find_therapists/",
            data: {medical_number: $therapistMedicalNumber.val()},
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    if(data.count === 0) {
                        $therapistFirstName.parent().removeClass('has-success');
                        $therapistLastName.parent().removeClass('has-success');
                        $therapistMedicalNumber.parent().removeClass('has-success').addClass('has-error');
                        $therapistFirstName.val("");
                        $therapistLastName.val("");
                    } else {
                        $therapistFirstName.parent().removeClass('has-error');
                        $therapistLastName.parent().removeClass('has-error');
                        $therapistMedicalNumber.parent().removeClass('has-error').addClass('has-success');
                        $therapistFirstName.val(data.therapists[0].first_name);
                        $therapistLastName.val(data.therapists[0].last_name);
                    }
                } else {
                    //TODO
                }
            }
        })
    });

    $("#therapistFirstNameInput, #therapistLastNameInput").on('blur', function() {
        if (!$therapistFirstName.val() || !$therapistLastName.val()) return;
        $.ajax({
            type: "POST",
            url: "/ajax/find_therapists/",
            data: {first_name: $therapistFirstName.val(), last_name: $therapistLastName.val()},
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    if (data.count === 0) {
                        $therapistFirstName.parent().removeClass('has-success').addClass('has-error');
                        $therapistLastName.parent().removeClass('has-success').addClass('has-error');
                    } else if(data.count === 1) {
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
    var $operationCodeography = $("#operationCodeographySelect");

    $operationType.on('change', function() {
        $operationCodeography.html("<option value='' selected></option>");
        $.ajax({
            type: "POST",
            url: "/ajax/find_operations/",
            data: {type: $operationType.val()},
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    for (var i in data.codeographies) {
                        $operationCodeography.append(
                            '<option value="' + data.codeographies[i] + '">'
                                + data.codeographies[i] + '</option>'
                        );
                    }
                } else {
                    //TODO
                }
            }
        });
    });
    var $patientModal = $("#registerPatientModal");
    $("#registerPatientSubmit").on('click', function() {
        $patientModal.find('form').submit();
    })
});
