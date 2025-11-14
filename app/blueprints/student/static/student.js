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



// go to view submission
document.getElementById('submit-button').addEventListener('click', function () {
  const student_id = ...;       // Get from form or context
  const assignment_id = ...;
  const content = document.getElementById('writing-content').value;
  const jlpt_level = document.getElementById('jlpt-level').value;

  fetch('/tasks/submit_test/123', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ student_id, assignment_id, content, jlpt_level })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      window.location.href = `/student/view_submission_detail/${data.submission_id}`;
    }
  });
});
