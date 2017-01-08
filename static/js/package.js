function change_package_freight(package){
	console.log("adsda");
	$.ajax({
		url: change,
		method: 'POST',
		beforeSend: function(xhr){
			xhr.setRequestHeader("X-CSRFToken", csrf_token);
		},
		data: {
			'id': package.id,
			'freight': package.value
			},
	}).done(function(html){

	});
};
