$( document ).ready(function() {
	window.objIndex = 0;
	window.frameIndex = 0;
	window.curr_object = null;
	window.curr_frame = null;
	getObjects();
});

function getObjects() {
	$.getJSON(
		'/getObjects',
		{arg: JSON.stringify({})},
		function (response){
			window.objects = response.elements;
			window.curr_object = window.objects[window.objIndex];
			getFrames(window.curr_object);
		}
	)
}

function getFrames(object) {
	$.getJSON(
		'/getFrames',
		{arg: JSON.stringify({'object' : object})},
		function (response){
			window.frames = response.elements;
			window.curr_frame = window.frames[window.frameIndex];
			getBitMap(object, window.curr_frame);
		}
	)
}

function getBitMap(object, frame) {
	$.getJSON(
		'/getBitMap',
		{arg: JSON.stringify({'object' : object, 'frame' : frame})},
		function (response){
			var bitMap = response.elements;
			console.log(bitMap);
		}
	)	
}