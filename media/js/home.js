$(document).ready(function() {
    var $firstName = $("#firstNameInput");
    var $lastName = $("#lastNameInput");
    var $nationalCode = $("#nationalCodeInput");

    $nationalCode.on('blur', function() {
        if (!$nationalCode.val()) return;
        $.ajax({
            type: "POST",
            url: "/ajax/find_patients/",
            data: {national_code: $nationalCode.val()},
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    if (data.count === 0) {
                        $firstName.removeClass('success');
                        $lastName.removeClass('success');
                        $nationalCode.removeClass('success').addClass('error');
                        $firstName.val("");
                        $lastName.val("");
                    } else {
                        $firstName.removeClass('error');
                        $lastName.removeClass('error');
                        $nationalCode.removeClass('error').addClass('success');
                        $firstName.val(data.patients[0].first_name);
                        $lastName.val(data.patients[0].last_name);
                    }
                } else {
                    //TODO
                }
            }
        });
    });

    $("#firstNameInput, #lastNameInput").on('blur', function() {
        if (!$firstName.val() || !$lastName.val()) return;
        $.ajax({
            type: "POST",
            url: "/ajax/find_patients/",
            data: {first_name: $firstName.val(), last_name: $lastName.val()},
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    if (data.count === 0) {
                        $firstName.removeClass('success').addClass('error');
                        $lastName.removeClass('success').addClass('error');
                        $nationalCode.val("");
                    } else if(data.count === 1) {
                        $firstName.removeClass('error').addClass('success');
                        $lastName.removeClass('error').addClass('success');
                        $nationalCode.val(data.patients[0].national_code);
                    } else {
                        //TODO: modal
                    }
                } else {
                    //TODO
                }
            }
        });
    });

    var $type = $("#insuranceTypeSelect");
    var $category = $("#insuranceCategorySelect");
    var $complementary = $("#insuranceComplementarySelect");
    $type.on('change', function() {
        $category.html("<option value='' selected></option>");
        $complementary.html("<option value='' selected></option>");
        $.ajax({
            type: "POST",
            url: "/ajax/find_insurances/",
            data: {type: $type.val()},
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    for (var i in data.categories) {
                        $category.append(
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
    $category.on('change', function() {
        $complementary.html("<option value='' selected></option>");
        $.ajax({
            type: "POST",
            url: "/ajax/find_insurances/",
            data: {type: $type.val(), category: $category.val()},
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    for(var i in data.complementaries) {
                        $complementary.append(
                            '<option value="' + data.complementaries[i] + '">'
                                + data.complementaries[i] + '</option>'
                        );
                    }
                }
            }
        });
    });
});
