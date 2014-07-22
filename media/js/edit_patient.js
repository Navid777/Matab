$(document).ready(function(){
	$submit = $("#editPatientSubmit");
	$form = $("#editPatientForm");
	$submit.on('click', function(){
        $.ajax({
            type: 'POST',
            url: $form.attr('action'),
            data: $form.serialize(),
            dataType: 'json',
            success: function(data) {
            	//TODO: yek raveshte dorost peida shavad!
            	if(data.success){
            		//alert("تغییرات با موفقیت انجام شد.");
            		window.location.replace($("#chooseLink").attr("href"));
            	}
            }
        });
	});
});
