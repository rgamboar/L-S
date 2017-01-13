function change_package_freight(package){
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

function change_freight_state(package, state){
	$.ajax({
	url: changePackageState,
	method: 'POST',
	beforeSend: function(xhr){
		xhr.setRequestHeader("X-CSRFToken", csrf_token);
	},
	data: {
		'id': package,
		'state': state
		},
	}).done(function(html){
		location.reload(true);
	});
};