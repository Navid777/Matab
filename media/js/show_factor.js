$(document).ready(function() {
    var $button = $("#payFactor");
    $button.on('click', function() {
        if (!confirm("آیا مطمئن هستید؟")) {
            return;
        }
        $.ajax({
            type: "POST",
            url: $button.attr('data-url'),
            data: {id: $button.attr('data-id')},
            dataType: 'json',
            success: function(data) {

            }
        });
    });
});