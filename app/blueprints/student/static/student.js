



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











