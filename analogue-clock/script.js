"use strict";

const clockSeconds = document.getElementById("sec");
const clockMinutes = document.getElementById("min");
const clockHours = document.getElementById("hr");

function getTime() {
  const date = new Date();
  const seconds = date.getSeconds();
  const minutes = date.getMinutes();
  const hours = date.getHours();

  const degSeconds = (seconds * 360) / 60;
  const degMinutes = ((minutes + seconds / 60) * 360) / 60;
  const degHours = ((hours + minutes / 60 + seconds / 3600) * 360) / 12;

  clockSeconds.style.transform = `rotate(${degSeconds}deg)`;
  clockMinutes.style.transform = `rotate(${degMinutes}deg)`;
  clockHours.style.transform = `rotate(${degHours}deg)`;
}

getTime();
setInterval(getTime, 1000);
