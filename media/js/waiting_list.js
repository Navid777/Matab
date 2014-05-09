$(document).ready(function() {

    var update = function() {
        var $patientList = $("#patient_list");
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
    setInterval(update, 10000);
});