$(document).ready(function() {
    var $button = $("#factorPaid");
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
                if (data.success) {
                    //TODO: show success and change hard-coded url
                    document.location = "/reception/"
                } else {
                    //TODO error
                    alert(data.errors)
                }
            }
        });
    });
});