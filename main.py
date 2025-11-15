import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database import db

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET") or secrets.token_hex(32)

database_url = os.environ.get("DATABASE_URL")
if database_url:
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
else:
    raise RuntimeError(
        "DATABASE_URL environment variable is not set. "
        "Please set it in your Render dashboard or environment variables."
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

db.init_app(app)

with app.app_context():
    import models
    db.create_all()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('exam'))
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin@vcodez' and password == 'admin@123':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        
        user = models.User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('exam'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if models.User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
        else:
            user = models.User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/exam')
def exam():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    existing_responses = models.ExamResponse.query.filter_by(user_id=user_id).first()
    
    if existing_responses:
        flash('You have already completed the exam', 'info')
        return redirect(url_for('exam_completed'))
    
    questions = models.Question.query.all()
    
    duration_setting = models.AdminSettings.query.filter_by(setting_key='exam_duration').first()
    try:
        duration = int(duration_setting.setting_value) if duration_setting else 60
        if duration < 1:
            duration = 60
    except (ValueError, TypeError):
        duration = 60
    
    return render_template('exam.html', questions=questions, duration=duration)

@app.route('/submit_exam', methods=['POST'])
def submit_exam():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    questions = models.Question.query.all()
    
    for question in questions:
        if question.question_type == 'MCQ':
            user_answer = request.form.get(f'question_{question.id}')
            user_answer_text = None
            is_correct = user_answer == question.correct_answer if user_answer else False
            points = question.points if is_correct else 0
        else:
            user_answer = None
            user_answer_text = request.form.get(f'question_{question.id}')
            is_correct = False
            points = 0
        
        response = models.ExamResponse(
            user_id=user_id,
            question_id=question.id,
            user_answer=user_answer,
            user_answer_text=user_answer_text,
            is_correct=is_correct,
            points_earned=points
        )
        db.session.add(response)
    
    db.session.commit()
    flash('Exam submitted successfully!', 'success')
    return redirect(url_for('exam_completed'))

@app.route('/exam_completed')
def exam_completed():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('exam_completed.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('login'))
    
    users = models.User.query.all()
    questions = models.Question.query.all()
    
    user_data = []
    for user in users:
        responses = models.ExamResponse.query.filter_by(user_id=user.id).all()
        total_questions = len(responses)
        correct_answers = sum(1 for r in responses if r.is_correct)
        score = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        user_data.append({
            'user': user,
            'responses': responses,
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'score': score
        })
    
    block_password_setting = models.AdminSettings.query.filter_by(setting_key='block_password').first()
    block_password = block_password_setting.setting_value if block_password_setting else ''
    
    duration_setting = models.AdminSettings.query.filter_by(setting_key='exam_duration').first()
    exam_duration = duration_setting.setting_value if duration_setting else '60'
    
    return render_template('admin_dashboard.html', user_data=user_data, questions=questions, block_password=block_password, exam_duration=exam_duration)

@app.route('/admin/set_block_password', methods=['POST'])
def set_block_password():
    if 'admin' not in session:
        return redirect(url_for('login'))
    
    new_password = request.form.get('block_password')
    setting = models.AdminSettings.query.filter_by(setting_key='block_password').first()
    
    if setting:
        setting.setting_value = new_password
    else:
        setting = models.AdminSettings(setting_key='block_password', setting_value=new_password)
        db.session.add(setting)
    
    db.session.commit()
    flash('Block password updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/set_exam_duration', methods=['POST'])
def set_exam_duration():
    if 'admin' not in session:
        return redirect(url_for('login'))
    
    try:
        new_duration = int(request.form.get('exam_duration', 60))
        if new_duration < 1 or new_duration > 300:
            flash('Duration must be between 1 and 300 minutes!', 'error')
            return redirect(url_for('admin_dashboard'))
    except (ValueError, TypeError):
        flash('Invalid duration value! Please enter a valid number.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    setting = models.AdminSettings.query.filter_by(setting_key='exam_duration').first()
    
    if setting:
        setting.setting_value = str(new_duration)
    else:
        setting = models.AdminSettings(setting_key='exam_duration', setting_value=str(new_duration))
        db.session.add(setting)
    
    db.session.commit()
    flash('Exam duration updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/create_question', methods=['POST'])
def create_question():
    if 'admin' not in session:
        return redirect(url_for('login'))
    
    question_type = request.form.get('question_type')
    question_text = request.form.get('question_text')
    points = int(request.form.get('points', 1))
    
    if question_type == 'MCQ':
        option_a = request.form.get('option_a')
        option_b = request.form.get('option_b')
        option_c = request.form.get('option_c')
        option_d = request.form.get('option_d')
        correct_answer = request.form.get('correct_answer')
        
        question = models.Question(
            question_type='MCQ',
            question_text=question_text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_answer=correct_answer,
            points=points
        )
    elif question_type == 'SHORT_ANSWER':
        correct_answer_text = request.form.get('correct_answer_text', '')
        
        question = models.Question(
            question_type='SHORT_ANSWER',
            question_text=question_text,
            correct_answer_text=correct_answer_text,
            points=points
        )
    elif question_type == 'PARAGRAPH':
        correct_answer_text = request.form.get('correct_answer_text', '')
        
        question = models.Question(
            question_type='PARAGRAPH',
            question_text=question_text,
            correct_answer_text=correct_answer_text,
            points=points
        )
    
    db.session.add(question)
    db.session.commit()
    flash(f'{question_type} question created successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_question/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    if 'admin' not in session:
        return redirect(url_for('login'))
    
    question = models.Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/verify_block_password', methods=['POST'])
def verify_block_password():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    data = request.get_json()
    entered_password = data.get('password', '')
    
    block_password_setting = models.AdminSettings.query.filter_by(setting_key='block_password').first()
    correct_password = block_password_setting.setting_value if block_password_setting else 'exam2024'
    
    if entered_password == correct_password:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Incorrect password'})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
