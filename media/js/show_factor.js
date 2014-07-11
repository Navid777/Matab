$(document).ready(function() {
    var $button = $("#factorPaid");
    var $discount = $("#discount");
    var $totalPayable = $("#totalPayable");
    var $totalPayableWithDiscount = $("#totalPayableWithDiscount");
    var $finalPayable = $("#finalPayable");
    $totalPayableWithDiscount.val($totalPayable.val());
    $finalPayable.val($totalPayable.val());
    $discount.val("0");
    $factors = $(".factorId").map(function(){
    	return $(this).val();
    }).get();

    $discount.on('change', function(){
    	if( Number($discount.val()) > Number($totalPayable.val()) ) {
    		$totalPayableWithDiscount.val("0");
    		$finalPayable.val("0");
    	}
    	else{
    		$totalPayableWithDiscount.val(
    			Number($totalPayable.val()) - Number($discount.val())
    		);
    		$finalPayable.val($totalPayableWithDiscount.val());
    	}
    	$button.focus();	
    });
    
    $button.on('click', function() {
    	alert("ahoy");
    	$.ajax({
            type: "POST",
            url: $button.attr('discount_url'),
            data: { factors: $factors, 
            		discount:$discount.val()
            		},
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                	alert("Hi");
                } else {
                    //TODO error
                    alert(data.errors);
                    alert("Bye");
                }
            }
        });
        $.ajax({
            type: "POST",
            url: $button.attr('data-url'),
            data: {id: $button.attr('data-id')
            		},
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