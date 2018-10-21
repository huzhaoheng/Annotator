$( document ).ready(function() {
	window.objectPointer = 0;
	window.framePointer = 0;
	window.objects = null;
	window.frames = null;
	window.curr_object = null;
	window.curr_frame = null;
	getObjects();
});

function loadSelections() {
	var options = [];
	window.allClasses.forEach(function (className) {
		options.push({
			name : className
		});
	})
	var $select = $('#classSelector').selectize({
		create: true,
		sortField: 'text',
		valueField: 'name',
		labelField: 'name',
		searchField: 'name',
		options: options,
	});

	window.selector = $select[0].selectize;
}

function getObjects() {
	$.getJSON(
		'/getObjects',
		{arg: JSON.stringify({})},
		function (response){
			var result = response.elements;
			window.objectPointer = result['objectPointer'];
			window.objects = result['objectList'];
			window.curr_object = window.objects[window.objectPointer];
			setTitle();
			loadClasses();
			getFrames();
		}
	)
}

function getFrames() {
	$.getJSON(
		'/getFrames',
		{arg: JSON.stringify({'object' : window.curr_object})},
		function (response){
			window.frames = response.elements;
			window.framePointer = 0;
			window.curr_frame = window.frames[window.framePointer];
			getImageArray();
		}
	)
}

function getImageArray() {
	$.getJSON(
		//'/getImageArray',
		'http://67.173.101.247:5000/getImageArray',
		{arg: JSON.stringify({'object' : window.curr_object, 'frame' : window.curr_frame})},
		function (response){
			var res = response.elements;
			var height = res['height'];
			var width = res['width'];
			var array = res['array'];
			displayImage(width, height, array);
		}
	)	
}

function displayImage(width, height, array) {
	console.log(width);
	console.log(height);
	console.log(array.length);
	console.log(array);
	//var canvas = document.getElementById('canvas');
	var canvas = document.querySelector('canvas'),
	ctx = canvas.getContext('2d');
	fitToContainer(canvas);

	canvas.width = width;
	canvas.height = height;

	var imgData = ctx.getImageData(0, 0, width, height);
	var data = imgData.data;
	data.set(array);

	// update canvas with new data
	ctx.putImageData(imgData, 0, 0);

	var image = new Image();

	// set the img.src to the canvas data url
	image.src = canvas.toDataURL();
}

function fitToContainer(canvas){
	canvas.style.width='100%';
	canvas.style.height='100%';
	canvas.width  = canvas.offsetWidth;
	canvas.height = canvas.offsetHeight;
}

function setTitle() {
	var title = window.curr_object;
	$("#title").text(title);
	return;
}

function nextHandler(tryAnother) {
	window.framePointer += 1;
	if (!(window.framePointer in window.frames)){
		if (tryAnother == true) {
			window.alert("No more frames for this object, re-display from 1st frame.");
			window.framePointer = 0;
			window.curr_frame = window.frames[window.framePointer];
			getImageArray();
			return;
		}
		else {
			window.objectPointer += 1;
			if (!(window.objectPointer in window.objects)) {
				window.alert("No more Objects/Frames");
				return;
			}
			else {
				updateObjectPointer();
				window.curr_object = window.objects[window.objectPointer];
				setTitle();
				getFrames();
			}
		}
	}
	else {
		window.curr_frame = window.frames[window.framePointer];
		getImageArray();
	}

	loadClasses();
	return;
}

function updateObjectPointer() {
	$.getJSON(
		'/updateObjectPointer',
		{arg: JSON.stringify({'objectPointer' : window.objectPointer})},
		function (response){
			var result = response.elements;
			return;
		}
	)
	return;
}

function loadClasses() {
	$.getJSON(
		'/getAllClasses',
		{arg: JSON.stringify({})},
		function (response){
			var result = response.elements;
			window.allClasses = result['classesList'];
			loadSelections();
			loadRecommendationClasses();
			return;
		}
	)
	return;
}

function loadRecommendationClasses() {
	var k = 10;
	// var topKClasses = getTopKClasses(k, window.allClasses, window.curr_object);
	getTopKClasses(k, window.allClasses, window.curr_object);
}

function getTopKClasses(k, classes, curr_object) {
	// var ret = null;
	// //----------TO DO: implement top K classes recommendation algorithm----------------
	// ret = classes.slice(0, k);
	// //---------------------------------------------------------------------------------
	// return ret;
	var ret = null;
	$.getJSON(
		'/getTopKClasses',
		{arg: JSON.stringify({'K':k, 'allClasses':classes, 'curr_object':curr_object})},
		function (response){
			var result = response.elements;
			// ret = result;
			// return;
			createRecommendationButtons(result);
		}
	)
	return;
}

function createRecommendationButtons(topKClasses) {
	$("#classes").empty();
	var code = "";
	topKClasses.forEach(function (className, index) {
		if (index == 0) {
			code = '<div class="row">';
			code += `<div class="col-md-3">
						<button class="btn btn-success btn-block" onClick="classSelectionHandler(this, 'button');">` + 
							className + 
						`</button>
					</div>`;
		}
		else if (index % 4 == 0) {
			code += "</div><hr />"
			$(code).appendTo("#classes");
			code = '<div class="row">';
			code += `<div class="col-md-3">
						<button class="btn btn-success btn-block" onClick="classSelectionHandler(this, 'button');">` + 
							className + 
						`</button>
					</div>`;	
		}
		else {
			code += `<div class="col-md-3">
						<button class="btn btn-success btn-block" onClick="classSelectionHandler(this, 'button');">` + 
							className + 
						`</button>
					</div>`;
		}
	})

	code += "</div>";
	$(code).appendTo("#classes");
}

function classSelectionHandler(element, source) {
	var className = null;
	if (source == 'button') {
		className = $(element).text();	
	}
	else {
		className = window.selector.items[0];
		if (className == undefined) {
			window.alert("Please select a class");
			return;
		}
	}
	$.getJSON(
		'/storeClassSelection',
		{arg: JSON.stringify({'object' : window.curr_object, 'class' : className, 'allClasses' : window.selector.options})},
		function (response){
			var res = response.elements;
			window.framePointer = Object.keys(window.frames).length - 1;
			nextHandler(false);
		}
	)
}