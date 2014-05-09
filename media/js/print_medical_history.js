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
                    $button.hide();
                    $("#return").removeClass('hide');
                    window.print();
                } else {
                    //TODO error
                    alert(data.errors);
                }
            }
        });
    });

    $("#print").on('click',function() {
        window.print();
    });
});