function change_package_client(package_id){
	var client = $("#select" + package_id);
	var icon = $("#icon" + package_id);
	$.ajax({
		url: changeClient,
		method: 'POST',
		beforeSend: function(xhr){
			xhr.setRequestHeader("X-CSRFToken", csrf_token);
		},
		data: {
			'package_id': package_id,
			'client': client.val()
			},
	}).done(function(html){
		icon.removeClass("hidden");
	});
};