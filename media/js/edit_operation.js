$(document).ready(function(){
	$submit = $("#editOperationSubmit");
	$form = $("#editOperationForm");
	$submit.on('click', function(){
		alert("s");
        $.ajax({
            type: 'POST',
            url: $form.attr('action'),
            data: $form.serialize(),
            dataType: 'json',
            success: function(data) {
            	//TODO: yek raveshte dorost peida shavad!
            	if(data.success){
            		alert("تغییرات با موفقیت انجام شد.");
            	}
            }
        });
	});
});