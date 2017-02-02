function change_package_freight(a){
	$.ajax({
		url: change,
		method: 'POST',
		beforeSend: function(xhr){
			xhr.setRequestHeader("X-CSRFToken", csrf_token);
		},
		data: {
			'id': a.getAttribute('package'),
			'freight': a.getAttribute('freight')
			},
	}).done(function(html){
		if (a.parentNode.parentNode.parentNode.id == 'own'){
			a.parentNode.parentNode.parentNode.removeChild(a.parentNode.parentNode);
			$("#not_own").append(a.parentNode.parentNode);
			var icon = $("#" + a.id);
			icon.attr('freight' , freight)
		}
		else{
			a.parentNode.parentNode.parentNode.removeChild(a.parentNode.parentNode);
			$("#own").append(a.parentNode.parentNode);
			var icon = $("#" + a.id);
			icon.attr('freight' , '-')
		}
		var icon = $("#" + a.id);
		icon.toggleClass("fa-plus");
		icon.toggleClass("fa-times");
	});
};


function change_freight_truck(freight, freight_id){
	$.ajax({
		url: changeTruck,
		method: 'POST',
		beforeSend: function(xhr){
			xhr.setRequestHeader("X-CSRFToken", csrf_token);
		},
		data: {
			'id': freight_id,
			'truck': freight.value
			},
	}).done(function(html){

	});
};

function change_freight_driver(freight, freight_id){
	$.ajax({
		url: changeDriver,
		method: 'POST',
		beforeSend: function(xhr){
			xhr.setRequestHeader("X-CSRFToken", csrf_token);
		},
		data: {
			'id': freight_id,
			'driver': freight.value
			},
	}).done(function(html){

	});
};


function change_freight_load(freight_id, package_finish){
	console.log(package_finish);
	$.ajax({
		url: freightLoad,
		method: 'POST',
		beforeSend: function(xhr){
			xhr.setRequestHeader("X-CSRFToken", csrf_token);
		},
		data: {
			'id': freight_id,
			'finish': package_finish
			},
	}).done(function(html){
		location.reload(true);
	});
};


function change_freight_state(freight, state){
	if ($("#selectDriver").val() == '-' || $("#selectTruck").val() == '-'){
		console.log("Logrado");
	}
	else {
		$.ajax({
		url: changeFreightState,
		method: 'POST',
		beforeSend: function(xhr){
			xhr.setRequestHeader("X-CSRFToken", csrf_token);
		},
		data: {
			'id': freight,
			'state': state
			},
		}).done(function(html){
			location.reload(true);
		});
	};
};