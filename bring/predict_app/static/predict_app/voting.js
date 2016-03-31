console.log("hello bitch")



document.getElementById('bout_vote').addEventListener('submit', votingSubmission);




function votingSubmission(event){
	event.preventDefault();

	var form = document.getElementById('bout_vote');

	var data = form.querySelector("[name='fighter_choice']:checked");

	console.log (data.value);

	var method = document.getElementById('method').value;

	var confidence = document.getElementById('confidence').value;

	var attachment = document.getElementById('attachment').value;

	var excitement = document.getElementById('excitement').value;

	var bout_id = document.getElementById('bout_id').value;

	var ring_user_id = document.getElementById('ring_user_id').value;

	console.log (method, confidence, attachment, excitement);

	var jsonData = JSON.stringify({ 
		'method':method, 
		'fighter_id':data.value, 
		'confidence':confidence,
		'attachment':attachment,
		'excitement':excitement,
		'ring_user_id':ring_user_id,
		'bout_id':bout_id		
	});

	//build an xhttp request
	var csrfToken = form.querySelector("[name='csrfmiddlewaretoken']").value;
	var xhr = new XMLHttpRequest();
	xhr.open('POST', 'submit_vote', true);
	xhr.onload = votingSuccess;
	
	xhr.setRequestHeader('X-CSRFToken', csrfToken);

	console.log(jsonData);
	xhr.send(jsonData);

}

function votingSuccess(response) {

	if (response.target.status === 200){
		//get data from response
		var data_json = response.target.response;
		
		//translate data from json
		var data = JSON.parse(data_json);
		console.log(response.target.response);
		console.log("data",data)
		url="http://127.0.0.1:8000/fightcard/" + data.data.toString();
		 
		document.location.assign(url)

		//Post the voting results!!
		//postResults(data.data)
	}

}

/*
function postResults(data){
	//Get the div that had the poll in it and clear everything
	//making way for voting results
	var divThing = document.getElementById('question_things');
	divThing.innerHTML = "";

	var h3 = document.createElement('h3');

	h3.textContent = "Current Results!";

	var list = document.createElement('ul');
	list.id = 'results';

	//loop  through the returned results and display them
	for (var i = 0; i < data.length; i++) {
		var choice = "'" + data[i].text + "' has " + data[i].votes + " votes";
		var item = document.createElement('li');
		item.textContent = choice;
		list.appendChild(item);
	};

	divThing.appendChild(h3);
	divThing.appendChild(list);

}*/