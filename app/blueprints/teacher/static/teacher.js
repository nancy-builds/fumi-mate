let questionCount = 0;

const container = document.getElementById('questionsContainer');
const addBtn = document.getElementById('addQuestionBtn');

addBtn.addEventListener('click', () => {
  questionCount++;
  const questionDiv = document.createElement('div');
  questionDiv.className = 'question-item border rounded-3 p-3 mb-3 bg-light position-relative fade-in';
  questionDiv.innerHTML = `
    <button type="button" class="btn-close position-absolute top-0 end-0 me-2 mt-2" onclick="removeQuestion(this)"></button>
    <h6 class="fw-semibold mb-2">Question ${questionCount}</h6>

    <div class="mb-2">
      <label class="form-label">Question Text</label>
      <textarea name="question_text_${questionCount}" class="form-control" rows="2" placeholder="e.g. Write the kanji for 'mountain'"></textarea>
    </div>

    <div class="row">
      <div class="col-md-6 mb-2">
        <label class="form-label">Type</label>
        <select name="question_type_${questionCount}" class="form-select">
          <option value="writing">Writing</option>
          <option value="kanji">Kanji</option>
          <option value="vocabulary">Vocabulary</option>
          <option value="translation">Translation</option>
        </select>
      </div>
      <div class="col-md-6 mb-2">
        <label class="form-label">Hint</label>
        <input type="text" name="question_hint_${questionCount}" class="form-control" placeholder="Hint (optional)">
      </div>
    </div>

    <div class="mb-2">
      <label class="form-label">Sample Answer</label>
      <textarea name="question_answer_${questionCount}" class="form-control" rows="2" placeholder="Example answer (optional)"></textarea>
    </div>
  `;

  container.appendChild(questionDiv);
  updateQuestionNumbers();
});

function removeQuestion(btn) {
  btn.parentElement.remove();
  updateQuestionNumbers();
}

function updateQuestionNumbers() {
  const questionItems = container.querySelectorAll('.question-item');
  questionCount = questionItems.length;

  questionItems.forEach((item, index) => {
    item.querySelector('h6').textContent = `Question ${index + 1}`;
    item.querySelectorAll('textarea, select, input').forEach(el => {
      const name = el.name.replace(/\d+$/, index + 1);
      el.name = name;
    });
  });
}
