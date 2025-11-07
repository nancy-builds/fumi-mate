// Simple 30-minute countdown timer
let timeLeft = 30 * 60;
const timerEl = document.getElementById("timer");

function updateTimer() {
  const mins = Math.floor(timeLeft / 60);
  const secs = timeLeft % 60;
  timerEl.textContent = `${mins}:${secs.toString().padStart(2, "0")}`;
  if (timeLeft <= 0) {
    clearInterval(timer);
    alert("Time’s up! Please submit your test.");
    document.querySelector("form").submit();
  }
  timeLeft--;
}

const timer = setInterval(updateTimer, 1000);