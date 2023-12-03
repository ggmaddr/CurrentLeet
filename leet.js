
const canvas = document.getElementById('canvas');  
const ctx = canvas.getContext('2d');  
  
const eyeRadius = 20;  
const eyeCenterX = canvas.width / 2;  
const eyeCenterY = canvas.height / 2;  
const eyeDistance = 50; // Distance between eyes  
  
let mouseX = 0;  
let mouseY = 0;  
 
function drawEyes() {  
ctx.clearRect(0, 0, canvas.width, canvas.height);  

const relativeX = mouseX - eyeCenterX;  
const relativeY = mouseY - eyeCenterY;  

const angle = Math.atan2(relativeY, relativeX);  

const leftEyeX = eyeCenterX - eyeDistance * Math.cos(angle + 0.3);  
const leftEyeY = eyeCenterY - eyeDistance * Math.sin(angle + 0.3);  
const rightEyeX = eyeCenterX + eyeDistance * Math.cos(angle - 0.3);  
const rightEyeY = eyeCenterY + eyeDistance * Math.sin(angle - 0.3);  

drawEye(leftEyeX, leftEyeY, angle + 0.3);  

drawEye(rightEyeX, rightEyeY, angle - 0.3);  
}  

function drawEye(eyeX, eyeY, eyeAngle) {  
ctx.fillStyle = 'black';  
ctx.beginPath();  
ctx.arc(eyeX, eyeY, eyeRadius, 0, 2 * Math.PI);  
ctx.fill();  

ctx.fillStyle = '#2ecc71';  
ctx.beginPath();  
ctx.arc(eyeX, eyeY, eyeRadius * 0.7, 0, 2 * Math.PI);  
ctx.fill();  

ctx.fillStyle = 'black';  
ctx.beginPath();  
ctx.arc(eyeX + eyeRadius * 0.5 * Math.cos(eyeAngle), eyeY + eyeRadius * 0.5 * Math.sin(eyeAngle), eyeRadius * 0.3, 0, 2 * Math.PI);  
ctx.fill();  
}  

canvas.addEventListener('mousemove', (event) => {  
mouseX = event.offsetX;  
mouseY = event.offsetY;  
drawEyes();  
});  

drawEyes();  
