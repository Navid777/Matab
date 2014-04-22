/**
 * @author Navid
 */
$(document).ready(function() {
	$(".paziresh_tab").click(function(){
		$.ajax({
			type:"GET",
			url:"/insurance_categories/?insurance_type=آزاد",
			dataType:"xml",
			success:function(xml) {
				alert("hello") ;
				alert(xml.find('insurance_type').first().text());
			}		
		});
	});
});
