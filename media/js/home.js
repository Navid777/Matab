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
                        $patientFirstName.removeClass('success');
                        $patientLastName.removeClass('success');
                        $patientNationalCode.removeClass('success').addClass('error');
                        $patientFirstName.val("");
                        $patientLastName.val("");
                    } else {
                        $patientFirstName.removeClass('error');
                        $patientLastName.removeClass('error');
                        $patientNationalCode.removeClass('error').addClass('success');
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
                        $patientFirstName.removeClass('success').addClass('error');
                        $patientLastName.removeClass('success').addClass('error');
                        $patientNationalCode.val("");
                    } else if(data.count === 1) {
                        $patientFirstName.removeClass('error').addClass('success');
                        $patientLastName.removeClass('error').addClass('success');
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
    var $insuranceComplementary = $("#insuranceComplementarySelect");

    $insuranceType.on('change', function() {
        $insuranceCategory.html("<option value='' selected></option>");
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
        $insuranceComplementary.html("<option value='' selected></option>");
        $.ajax({
            type: "POST",
            url: "/ajax/find_insurances/",
            data: {type: $insuranceType.val(), category: $insuranceCategory.val()},
            dataType: 'json',
            success: function(data) {
                if (data.success) {
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
                        $therapistFirstName.removeClass('success');
                        $therapistLastName.removeClass('success');
                        $therapistMedicalNumber.removeClass('success').addClass('error');
                        $therapistFirstName.val("");
                        $therapistLastName.val("");
                    } else {
                        $therapistFirstName.removeClass('error');
                        $therapistLastName.removeClass('error');
                        $therapistMedicalNumber.removeClass('error').addClass('success');
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
                        $therapistFirstName.removeClass('success').addClass('error');
                        $therapistLastName.removeClass('success').addClass('error');
                    } else if(data.count === 1) {
                        $therapistFirstName.removeClass('error').addClass('success');
                        $therapistLastName.removeClass('error').addClass('success');
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
});
