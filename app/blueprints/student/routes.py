from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions import db
from app.models import Task, Submission, Question
from . import bp, pipeline, agents
import json


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


@bp.route('/submission_detail/<int:submission_id>')
@login_required
def view_submission_detail(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    feedback_json = json.loads(submission.ai_feedback) if submission.ai_feedback else {}

    # Ensure student owns the submission
    if submission.student_id != current_user.id:
        flash("You are not authorized to view this submission.", "danger")
        return redirect(url_for('student.view_submissions'))
    return render_template('student/view_submission_detail.html',
                           submission=submission,
                           grade=feedback_json.get('grade', 'N/A'),
                           action_plan=feedback_json.get('action_plan', []),
                           practice_exercises=feedback_json.get('practice_exercises', []),
                           detailed_analysis=feedback_json.get('detailed_analysis', {})
                           )


# 🧾 Dashboard: List all submissions by student
@bp.route('/submissions')
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







# NEW ASS UPDATES

@bp.route('/tasks/submit_test/<int:task_id>', methods=['POST'])
@login_required
def submit_test(task_id):
    """
    Expected JSON:
    {
        "student_id": "student_123",
        "assignment_id": "essay_1",
        "content": "Student's writing...",
        "jlpt_level": "N3"
    }
    """
    data = request.get_json()
    student_id = data.get('student_id')
    assignment_id = data.get('assignment_id')
    content = data.get('content', '').strip()
    jlpt_level = data.get('jlpt_level', 'N5')

    if not content:
        return jsonify({"success": False, "message": "Please write something before submitting."}), 400

    task = Task.query.get_or_404(task_id)
    submission = Submission.query.filter_by(task_id=task.id, student_id=current_user.id).first()

    timestamp = datetime.utcnow().isoformat()
    submission_id = f"{student_id}_{assignment_id}_{timestamp}"

    if not submission:
        submission = Submission(
            task_id=task.id,
            student_id=current_user.id,
            content=content,
            status='submitted',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(submission)
        db.session.flush()
    else:
        submission.content = content
        submission.status = 'submitted'
        submission.updated_at = datetime.utcnow()

    task.is_done = True
    db.session.commit()

    # 1. Save to vectorstore
    pipeline.add_submission(
        submission_id=submission_id,
        content=content,
        metadata={
            "student_id": student_id,
            "assignment_id": assignment_id,
            "type": "student_submission",
            "timestamp": timestamp
        }
    )

    # 2. Get reference context
    context = pipeline.get_context_for_submission(
        query=content[:200],
        k=3,
        filter_dict={
            "assignment_id": assignment_id,
            "type": "reference"
        }
    )

    # 3. Run feedback agents
    feedback_results = agents.run_multi_agents(
        text=content,
        context=context,
        jlpt_level=jlpt_level
    )

    # 4. Save AI feedback and score
    submission.ai_feedback = feedback_results['feedback']['feedback_text']
    submission.ai_score = feedback_results['overall_score']
    db.session.commit()

    return jsonify({
        "success": True,
        "submission_id": submission.id,
        "overall_score": feedback_results['overall_score'],
        "grade": feedback_results['scoring'].get('grade_letter'),
        "feedback": feedback_results['feedback']['feedback_text'],
        "action_plan": feedback_results['feedback']['action_plan'],
        "practice_exercises": feedback_results['feedback']['practice_exercises'],
        "detailed_analysis": {
            "grammar": feedback_results['grammar'],
            "vocabulary": feedback_results['vocabulary'],
            "structure": feedback_results['structure'],
            "fluency": feedback_results['fluency'],
            "content": feedback_results['content']
        }
    })
