"use strict";

// ---- Populate clock face ----
// 12, 3, 6, 9 → big numbers   |   all others → neon tick lines
const face = document.querySelector(".clock-face");

for (let i = 0; i < 12; i++) {
  const hour  = i + 1;                   // 1..12
  const deg   = -90 + 30 * hour;         // angle to position on circle
  const label = hour === 12 ? "12" : hour;

  if (hour % 3 === 0) {
    // cardinal: upright text, rotated to position then counter-rotated to stay readable
    face.innerHTML += `
      <text font-size="9" filter="url(#f-glow)"
        transform="rotate(${deg}) translate(31 0) rotate(${-deg})">${label}</text>`;
  } else {
    // non-cardinal: radial neon line (no counter-rotation = stays radial)
    face.innerHTML += `
      <line transform="rotate(${30 * hour})"
        x1="0" y1="-30" x2="0" y2="-40" stroke-width="1.3" filter="url(#f-glow)" />`;
  }
}

// ---- Clock hands ----
const arcHand  = document.querySelector(".arc-hand");
const handHr   = document.querySelector(".hand-hr");
const handMn   = document.querySelector(".hand-mn");
const handSc   = document.querySelector(".hand-sc");

function tick() {
  const now  = new Date();
  const h12  = now.getHours() % 12 || 12;  // 1–12
  const m    = now.getMinutes();
  const s    = now.getSeconds();

  // arc mask: reveals how many hours have passed in the current 12h cycle
  const arcDeg = -15 + h12 * 30 + m * 0.5;

  // hour hand: smooth motion accounting for minutes + seconds
  const hrDeg  = h12 * 30 + m * 0.5 + s * (0.5 / 60);

  // minute hand: smooth motion accounting for seconds
  const mnDeg  = m * 6 + s * 0.1;

  // second hand: simple 6° per second
  const scDeg  = s * 6;

  arcHand.setAttribute("transform", `rotate(${arcDeg})`);
  handHr.setAttribute("transform",  `rotate(${hrDeg})`);
  handMn.setAttribute("transform",  `rotate(${mnDeg})`);
  handSc.setAttribute("transform",  `rotate(${scDeg})`);
}

tick();
setInterval(tick, 1000);
