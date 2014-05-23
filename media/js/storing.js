$(document).ready(function(){
	var $goodIdSelect = $("#goodIdSelect");
	$goodIdSelect.on('change', function(){
		if(!$goodIdSelect.val()) {
			$("#goodQuantity").val("");
			$("#goodFee").val("");
			$("#goodEditButton").attr("disabled", "disabled");
			$("#addGoodToStoreButton").attr("disabled", "disabled");
			$("#storingDetailedButton").attr("disabled", "disabled");
			return ;
		}
		$("#goodEditButton").removeAttr("disabled");
		$("#addGoodToStoreButton").removeAttr("disabled");	
		$("#storingDetailedButton").removeAttr("disabled");
		$.ajax({
            type: "POST",
            url: "/ajax/find_good/",
            data: {id: $goodIdSelect.val()},
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                	$("#goodQuantity").val(data.good.quantity);
                	$("#goodFee").val(data.good.fee);
                } else {
                    //TODO
                }
            }
        });
	});
	
	$("#editGoodModal").on('shown.bs.modal', function() {
		$("#editGoodNameInput").val($goodIdSelect.find(":selected").text());
		$("#editGoodFeeInput").val($("#goodFee").val());
		$("#editGoodQuantityInput").val($("#goodQuantity").val()) ;
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
    
   	$addGoodToStoreForm = $("#addGoodToStoreModal").find("form");
    $("#addGoodToStoreSubmit").on('click', function() {
        $.ajax({
            type: "POST",
            url: $addGoodToStoreForm.attr('action'),
            data: $addGoodToStoreForm.serialize(),
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                	$goodIdSelect.trigger('change');
                    $("#addGoodToStoreModal").modal('hide');
                } else {
                    //TODO:
                    alert(data.errors);
                }
            }
        });

    });
        
	$("#addGoodToStoreModal").on('shown.bs.modal', function(){
		$("#addGoodToStoreNameInput").val($goodIdSelect.find(":selected").text());
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
                	$goodIdSelect.find("option:selected").prop('selected', false);
                	//TODO: goh nakhor chera eshtebah mishe?!
                	$goodIdSelect.append("<option value='"+data.good.id+"' selected>"+data.good.name+"</option>");
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

