$(document).ready(function() {
    $("#insuranceTypeSelect").on('change',function() {
        $("#insuranceCategorySelect").html('<option value=""></option>')
            .attr('disabled', 'disabled');
        $.ajax({
            type: "POST",
            url: "/ajax/find_insurance_categories_by_type/",
            data: "type="+$("#insuranceTypeSelect").val(),
            dataType: "json",
            success: function(data) {
                //TODO: complete below
                if(data.success) {
                    if (data.count === 0) {

                    } else if(data.count === 1) {

                    } else {
                        for (var i in data.categories) {
                            $("#insuranceCategorySelect").append(
                                '<option value="' + data.categories[i] + '">'
                                + data.categories[i] + '</option>'
                            );
                        }
                    }
                    $("#insuranceCategorySelect").removeAttr("disabled");
                }
            }
        });
    });
});
