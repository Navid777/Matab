$(document).ready(function() {
    var $button = $("#factorPaid");
    $button.on('click', function() {
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
    
    $form = $("#payFactorModal").find('form');
    $modal = $("#payFactorModal");
    $('#payFactorSubmit').on('click', function(){
    	$.ajax({
    		type: "POST",
    		url: $form.attr('action'),
    		data: $form.serialize(),
    		dataType:'json',
    		success: function(data) {
    			if (data.success){
    				$button.hide();
    				$("#return").removeClass('hide');
    				$modal.modal('hide');
    				window.print();
    			}
    			else{
    				alert(data.errors);
    			}
    		}
    	});
    });
});