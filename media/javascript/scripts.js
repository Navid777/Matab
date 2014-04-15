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
				$x = $xml.find("django-objects");
				alert($x.text());
			}		
		});
	});
});
