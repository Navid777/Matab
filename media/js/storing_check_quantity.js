$(document).ready(function(){
	var $goodIdSelect = $("#goodIdSelect");
	$goodIdSelect.on('change', function(){
		if(!$goodIdSelect.val()) {
			$("#goodQuantity").html("");
			$("#goodFee").html("");
			$("#goodEditButton").attr("disabled", "disabled");
			return ;
		}
		$("#goodEditButton").removeAttr("disabled");
		$.ajax({
            type: "POST",
            url: "/ajax/find_good/",
            data: {id: $goodIdSelect.val()},
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                	$("#goodQuantity").html(data.good.quantity);
                	$("#goodFee").html(data.good.fee);
                } else {
                    //TODO
                }
            }
        });
	});
	
	$("#editGoodModal").on('shown.bs.modal', function() {
		$("#editGoodNameInput").val($goodIdSelect.find(":selected").text());
		$("#editGoodFeeInput").val($("#goodFee").html());
		$("#editGoodQuantityInput").val($("#goodQuantity").html()) ;
	});
	
	$editGoodForm = $("#editGoodModal").find("form");
    $("#editGoodSubmit").on('click', function() {
        $.ajax({
            type: "POST",
            url: $editGoodForm.attr('action'),
            data: $editGoodForm.serialize(),
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                	$goodIdSelect.trigger('change');
                    $("#editGoodModal").modal('hide');
                } else {
                    //TODO:
                    alert(data.errors);
                }
            }
        });
    });
    var $registerGoodForm = $("#registerGoodModal").find("form");
    $("#registerGoodSubmit").on('click', function() {
        $.ajax({
            type: "POST",
            url: $registerGoodForm.attr('action'),
            data: $registerGoodForm.serialize(),
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                	$goodIdSelect.append("option value='"+data.good.id+"' selected>"+data.good.name+"</option>");
                	$goodIdSelect.trigger('change');
                    $("#registerGoodModal").modal('hide');
                } else {
                    //TODO:
                    alert(data.errors);
                }
            }
        });
    });
});

