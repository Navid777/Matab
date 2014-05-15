$(document).ready(function(){
	$('table').on('click', '.delete', function(event){
		var index = $(this).parent().index()+1;
		$('#factors_table td', event.delegateTarger).remove(":nth-child("+index+")" );
	});
	$("#factorsPrint").on('click', function(){
	});
});
