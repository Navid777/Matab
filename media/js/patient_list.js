$(document).ready(function() {
    var intervalHandle = null;

    var startUpdating = function() {
        var update = function() {
            var $patientList = $("#patient_list");
            $.ajax({
                type: 'POST',
                url: '/ajax/find_patients_list/',
                dataType: 'json',
                success: function(data) {
                    if (data.success) {
                        $patientList.html("");
                        for (var i in data.patient_turns) {
                            $patientList.append(
                                '<tr><td>'+data.patient_turns[i].first_name+'</td>'
                                +'<td>'+data.patient_turns[i].last_name+'</td>'
                                +'<td>'+data.patient_turns[i].national_code+'</td>'
                                +'<td><button class="enter" data-id="'+data.patient_turns[i].id
                                +'">'+'ثبت ورود'+'</button></td></tr>'
                            );
                        }
                    } else {
                        //TODO
                    }
                }
            });
        };
        update();
        intervalHandle = setInterval(update, 10000);
    };

    $("#patient_list").on('click', "button.enter", function() {
        if (intervalHandle) {
            clearInterval(intervalHandle);
            intervalHandle = null;
        }
        var $self = $(this);
        var patient_id = $self.attr('data-id');
        $.ajax({
            type: "POST",
            url: "/ajax/set_entered_patient/",
            data: {id: patient_id},
            dataType: 'json',
            success: startUpdating,
            error: startUpdating
        });
    });

    startUpdating();
});