let hoursProgress = document.querySelector("#hours_progress");
let minutesProgress = document.querySelector("#minutes_progress");
let secondsProgress = document.querySelector("#seconds_progress");

let hoursText = document.querySelector("#hours_text");
let minutesText = document.querySelector("#minutes_text");
let secondsText = document.querySelector("#seconds_text");
let ampmText = document.querySelector("#ampm");

let hoursRadius = hoursProgress.r.baseVal.value;
let minutesRadius = minutesProgress.r.baseVal.value;
let secondsRadius = secondsProgress.r.baseVal.value;

let hoursCircumference = 2 * Math.PI * hoursRadius;
let minutesCircumference = 2 * Math.PI * minutesRadius;
let secondsCircumference = 2 * Math.PI * secondsRadius;

hoursProgress.style.strokeDasharray = hoursCircumference + " " + hoursCircumference;
minutesProgress.style.strokeDasharray = minutesCircumference + " " + minutesCircumference;
secondsProgress.style.strokeDasharray = secondsCircumference + " " + secondsCircumference;


let setTime = () => {
	let hours = new Date().getHours() > 12 ? new Date().getHours() - 12 : new Date().getHours();
	let minutes = new Date().getMinutes();
	let seconds = new Date().getSeconds();
	let ampm = new Date().getHours() >= 12 ? 'PM' : 'AM';

	let secondsOffset = secondsCircumference * (1 - (seconds / 60));
	let minutesOffset = minutesCircumference * (1 - (minutes / 60));
	let hoursOffset = hoursCircumference * (1 - (hours / 12));
	
	hoursText.innerHTML = hours < 10 ? '0' + hours : hours;
	minutesText.innerHTML = minutes < 10 ? '0' + minutes : minutes;
	secondsText.innerHTML = seconds < 10 ? '0' + seconds : seconds;
	ampmText.innerHTML = ampm;
	
	hoursProgress.style.strokeDashoffset = hoursOffset;
	minutesProgress.style.strokeDashoffset = minutesOffset;
	secondsProgress.style.strokeDashoffset = secondsOffset;
	
	window.requestAnimationFrame(setTime)
}

setTime();