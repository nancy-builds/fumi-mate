from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions import db
from app.models import Task, Submission, Question
from . import bp



# 📘 Student Writing Test Page
@bp.route('/writing_test/<int:task_id>', methods=['GET', 'POST'])
@login_required
def writing_test(task_id):
    task = Task.query.get_or_404(task_id)
    submission = Submission.query.filter_by(task_id=task.id, student_id=current_user.id).first()

    if request.method == 'POST':
        content = request.form.get('content', '')
        action = request.form.get('action')  # "save" or "submit"

        if not submission:
            submission = Submission(
                task_id=task.id,
                student_id=current_user.id,
                content=content,
                status='draft',
            )
            db.session.add(submission)
        else:
            submission.content = content

        # Handle save vs submit
        if action == 'submit':
            submission.status = 'submitted'
            flash('✅ Your test has been submitted successfully!', 'success')
            db.session.commit()
            return redirect(url_for('student.view_submissions'))  # Redirect to dashboard
        else:
            submission.status = 'draft'
            flash('💾 Draft saved.', 'info')

        submission.updated_at = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('student.view_submissions', task_id=task.id))

    return render_template('student/writing_test.html', task=task, submission=submission)


@bp.route('/submission/<int:submission_id>')
@login_required
def view_submission_detail(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    # Ensure student owns the submission
    if submission.student_id != current_user.id:
        flash("You are not authorized to view this submission.", "danger")
        return redirect(url_for('student.view_submissions'))
    return render_template('student/view_submission_detail.html', submission=submission)


# 🧾 Dashboard: List all submissions by student
@bp.route('/view_submissions')
@login_required
def view_submissions():
    submissions = (
        Submission.query.filter_by(student_id=current_user.id)
        .order_by(Submission.updated_at.desc())
        .all()
    )
    return render_template('student/view_submissions.html', submissions=submissions)


@bp.route('/tasks')
@login_required
def view_tasks():
    # You can filter by student if needed
    tasks = Task.query.all()
    return render_template('student/view_tasks.html', tasks=tasks)

@bp.route('/tasks/submit_test/<int:task_id>', methods=['POST'])
@login_required
def submit_test(task_id):
    task = Task.query.get_or_404(task_id)
    content = request.form.get('content', '').strip()

    if not content:
        flash('Please write something before submitting.', 'warning')
        return redirect(url_for('student.writing_test', task_id=task.id))

    # Tạo bài nộp mới
    submission = Submission(
        task_id=task.id,
        student_id=current_user.id,
        content=content,
        status='submitted',
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(submission)
    db.session.flush()  # 👈 Lấy được submission.id trước khi commit

    # Đánh dấu task đã hoàn thành
    task.is_done = True

    db.session.commit()

    flash('Your test has been submitted successfully!', 'success')
    return redirect(url_for('student.view_submission_detail', submission_id=submission.id))

