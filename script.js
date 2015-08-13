function onFormSubmit(event){
	var data= $(event.target).serializeArray();
	var thesis={}
	for (var i=0; i< data.length; i++){
		thesis[data[i].name] = data[i].value;
	}

	var list_element= $('<li>');
	list_element.html(thesis.year + thesis.title1);


	var thesis_create_api = '/api/thesis';
	$.post(thesis_create_api, thesis, function(response){
		if(response.status = 'OK') {
			var full_thesis = response.data.year+''+ response.data.title1
			$('.thesis-list').prepend('<li>' + full_thesis + '<li>')
		}else {
			prompt("Error.")
		}
	});
	return false;
}

function loadAllThesis(){
	var thesis_list_api = '/api/thesis';
	$.get(thesis_list_api, {}, function(response){
		console.log('thesis list', response)
		response.data.forEach(function(thesis) {
			var full_thesis = thesis.year + ' ' + thesis.title1;
			$('.thesis-list').append('<li>' + full_thesis + '</li>' )
		});
	});
}

$('.form-section').submit(onFormSubmit);
loadAllThesis();
