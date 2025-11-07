from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions import db
from app.models import Task, Question, Teacher
from . import bp

# --- Create a task (with multiple questions) ---
@bp.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    # Only allow teachers
    if current_user.role != 'teacher':
        flash('Access denied. Teachers only.', 'danger')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        difficulty = request.form.get('difficulty')
        due_date_str = request.form.get('due_date')

        # Convert date string to datetime
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        except (ValueError, TypeError):
            due_date = None

        # Validation
        if not title:
            flash('Title is required.', 'danger')
            return redirect(url_for('teacher.create_task'))

        # --- Create the Task ---
        new_task = Task(
            title=title,
            description=description,
            difficulty=difficulty,
            due_date=due_date,
            created_by=current_user.id,
            created_at=datetime.utcnow()
        )
        db.session.add(new_task)
        db.session.commit()

        # --- Handle multiple Questions ---
        # Expecting fields like question_text_1, question_text_2, ...
        question_index = 1
        added_count = 0

        while True:
            q_text = request.form.get(f'question_text_{question_index}')
            q_type = request.form.get(f'question_type_{question_index}')
            q_hint = request.form.get(f'question_hint_{question_index}')
            q_answer = request.form.get(f'question_answer_{question_index}')

            if not q_text:  # Stop when no more questions
                break

            new_question = Question(
                task_id=new_task.id,
                question_text=q_text,
                question_type=q_type or 'writing',
                hint=q_hint,
                sample_answer=q_answer
            )
            db.session.add(new_question)
            added_count += 1
            question_index += 1

        db.session.commit()

        flash(f'Task created successfully with {added_count} questions!', 'success')
        return redirect(url_for('teacher.view_tasks'))

    return render_template('teacher/create_task.html')

# --- View all tasks ---
@bp.route('/view_tasks')
@login_required
def view_tasks():
    if current_user.role != 'teacher':
        flash('Access denied. Teachers only.', 'danger')
        return redirect(url_for('main.index'))

    tasks = Task.query.filter_by(created_by=current_user.id).all()
    return render_template('teacher/view_tasks.html', tasks=tasks)

# --- View single task detail (with questions) ---
@bp.route('/task/<int:task_id>')
@login_required
def view_task_detail(task_id):
    # Chỉ cho phép teacher
    if current_user.role != 'teacher':
        flash('Access denied. Teachers only.', 'danger')
        return redirect(url_for('main.index'))

    # Lấy thông tin teacher hiện tại (nếu cần)
    teacher = Teacher.query.get(current_user.id)

    # Lấy task
    task = Task.query.get_or_404(task_id)

    return render_template('teacher/view_task_detail.html',
                           teacher=teacher,
                           task=task,
                           questions=task.questions)


# --- Edit task ---
@bp.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    if current_user.role != 'teacher':
        flash('Access denied. Teachers only.', 'danger')
        return redirect(url_for('main.index'))

    task = Task.query.get_or_404(task_id)

    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.difficulty = request.form.get('difficulty')
        due_date_str = request.form.get('due_date')
        try:
            task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        except (ValueError, TypeError):
            task.due_date = None

        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('teacher.view_tasks'))

    return render_template('teacher/edit_task.html', task=task)

# --- Delete task ---
@bp.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    if current_user.role != 'teacher':
        flash('Access denied. Teachers only.', 'danger')
        return redirect(url_for('main.index'))

    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully.', 'success')
    return redirect(url_for('teacher.view_tasks'))
