#!/usr/bin/env python3
"""
IntelliLearn Flask Web Application - Fixed Version
Complete web interface with student dashboard
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.recommender import IntelliLearnEngine
from utils.mastery_state import save_student_progress, load_student_progress, init_database

app = Flask(__name__)
app.secret_key = 'intellilearn_secret_key_2024'  # Change this in production
CORS(app)

# Load topics and questions
with open('data/topics_graph.json', 'r') as f:
    TOPICS = json.load(f)

with open('data/questions.json', 'r') as f:
    QUESTIONS = json.load(f)

# Store student sessions in memory (use database in production)
student_sessions = {}

# Initialize database
try:
    init_database()
except Exception as e:
    print(f"Warning: Could not initialize database: {e}")


@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Student dashboard"""
    student_name = session.get('student_name', 'Guest')
    return render_template('dashboard.html', student_name=student_name)


@app.route('/api/login', methods=['POST'])
def login():
    """Student login/registration"""
    try:
        data = request.json
        student_name = data.get('name', '').strip()
        
        if not student_name:
            return jsonify({'error': 'Name is required'}), 400
        
        # Store in session
        session['student_name'] = student_name
        
        # Create new engine instance for this student
        student_engine = IntelliLearnEngine(TOPICS)
        
        # Load existing progress or create new
        progress = load_student_progress(student_name)
        
        if progress:
            # Existing student - load their data
            student_engine.mastery_levels = progress['mastery_levels']
            student_sessions[student_name] = {
                'engine': student_engine,
                'responses': [],
                'current_topic': 'Variables',
                'learning_style': progress.get('learning_style', 'visual')
            }
            print(f"✓ Loaded existing student: {student_name}")
            return jsonify({
                'message': f'Welcome back, {student_name}!',
                'existing': True,
                'mastery_levels': progress['mastery_levels'],
                'learning_style': progress.get('learning_style')
            })
        else:
            # New student
            student_engine.mastery_levels = {topic: 0.1 for topic in TOPICS.keys()}
            student_sessions[student_name] = {
                'engine': student_engine,
                'responses': [],
                'current_topic': 'Variables',
                'learning_style': 'visual'
            }
            print(f"✓ Created new student: {student_name}")
            return jsonify({
                'message': f'Welcome, {student_name}!',
                'existing': False
            })
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/topics', methods=['GET'])
def get_topics():
    """Get all topics with mastery levels"""
    try:
        student_name = session.get('student_name', 'Guest')
        
        if student_name not in student_sessions:
            return jsonify({'error': 'Please login first'}), 401
        
        student_engine = student_sessions[student_name]['engine']
        
        topics_with_mastery = []
        for topic, info in TOPICS.items():
            topics_with_mastery.append({
                'name': topic,
                'description': info['description'],
                'difficulty': info['difficulty'],
                'prereqs': info['prereqs'],
                'mastery': student_engine.mastery_levels.get(topic, 0.1),
                'mastery_level': student_engine.bkt.get_mastery_level(
                    student_engine.mastery_levels.get(topic, 0.1)
                )
            })
        
        return jsonify({
            'topics': topics_with_mastery,
            'current_topic': student_sessions[student_name]['current_topic']
        })
    except Exception as e:
        print(f"Get topics error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/question', methods=['GET'])
def get_question():
    """Get a question for a specific topic"""
    try:
        student_name = session.get('student_name', 'Guest')
        topic = request.args.get('topic', 'Variables')
        
        if student_name not in student_sessions:
            return jsonify({'error': 'Please login first'}), 401
        
        # Get question for topic
        if topic not in QUESTIONS or not QUESTIONS[topic]:
            return jsonify({'error': 'No questions available for this topic'}), 404
        
        student_engine = student_sessions[student_name]['engine']
        question = QUESTIONS[topic][0]  # For simplicity, return first question
        
        return jsonify({
            'topic': topic,
            'question': question,
            'mastery': student_engine.mastery_levels.get(topic, 0.1)
        })
    except Exception as e:
        print(f"Get question error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/submit_answer', methods=['POST'])
def submit_answer():
    """Submit an answer and get feedback"""
    try:
        student_name = session.get('student_name', 'Guest')
        
        if student_name not in student_sessions:
            return jsonify({'error': 'Please login first'}), 401
        
        data = request.json
        topic = data.get('topic')
        answer = data.get('answer')
        correct = data.get('correct')
        time_spent = data.get('time_spent', 30)
        attempts = data.get('attempts', 1)
        
        student_data = student_sessions[student_name]
        student_engine = student_data['engine']
        
        # Process the response
        result = student_engine.process_response(
            topic, 
            answer == correct,
            time_spent,
            attempts
        )
        
        # Store response for learning style analysis
        student_data['responses'].append({
            'topic': topic,
            'is_correct': answer == correct,
            'time_spent': time_spent,
            'attempts': attempts,
            'timestamp': datetime.now().isoformat()
        })
        
        # Get recommendation for next topic
        recommendation = student_engine.get_recommendation(
            topic,
            student_data['responses']
        )
        
        # Update learning style
        student_data['learning_style'] = recommendation['learning_style']
        student_data['current_topic'] = recommendation['next_topic']
        
        # Save progress
        save_student_progress(
            student_name,
            student_engine.mastery_levels,
            recommendation['learning_style']
        )
        
        return jsonify({
            'correct': answer == correct,
            'result': result,
            'recommendation': recommendation,
            'style_info': recommendation['style_info']
        })
    except Exception as e:
        print(f"Submit answer error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get student statistics"""
    try:
        student_name = session.get('student_name', 'Guest')
        
        if student_name not in student_sessions:
            return jsonify({'error': 'Please login first'}), 401
        
        student_data = student_sessions[student_name]
        student_engine = student_data['engine']
        responses = student_data['responses']
        
        # Calculate statistics
        total_questions = len(responses)
        correct_answers = sum(1 for r in responses if r['is_correct'])
        accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        # Mastery distribution
        mastery_counts = {'Novice': 0, 'Beginner': 0, 'Developing': 0, 'Proficient': 0, 'Expert': 0}
        for mastery in student_engine.mastery_levels.values():
            level = student_engine.bkt.get_mastery_level(mastery)
            mastery_counts[level] += 1
        
        return jsonify({
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'accuracy': round(accuracy, 1),
            'learning_style': student_data['learning_style'],
            'mastery_distribution': mastery_counts,
            'avg_time': sum(r['time_spent'] for r in responses) / len(responses) if responses else 0,
            'topics_mastered': sum(1 for m in student_engine.mastery_levels.values() if m >= 0.8)
        })
    except Exception as e:
        print(f"Get stats error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/learning_path', methods=['GET'])
def get_learning_path():
    """Get recommended learning path"""
    try:
        student_name = session.get('student_name')
        
        print(f"Learning path request from: {student_name}")
        print(f"Active sessions: {list(student_sessions.keys())}")
        
        if not student_name:
            return jsonify({'error': 'Not logged in'}), 401
        
        if student_name not in student_sessions:
            return jsonify({'error': 'Session not found. Please login again.'}), 401
        
        student_data = student_sessions[student_name]
        student_engine = student_data['engine']
        
        # Generate learning path based on current mastery
        path = []
        current = student_data.get('current_topic', 'Variables')
        visited = set()
        
        # Ensure current topic exists
        if current not in TOPICS:
            current = 'Variables'
        
        print(f"Starting path from: {current}")
        
        for i in range(5):  # Get next 5 topics
            if current in visited or current not in TOPICS:
                print(f"Breaking at step {i}: current={current}, visited={visited}")
                break
            
            mastery = student_engine.mastery_levels.get(current, 0.1)
            path.append({
                'topic': current,
                'mastery': round(mastery, 3),
                'level': student_engine.bkt.get_mastery_level(mastery),
                'difficulty': TOPICS[current]['difficulty']
            })
            
            visited.add(current)
            
            # Get next recommendation
            try:
                next_topic = student_engine.q_learner.recommend_next(
                    current,
                    student_engine.mastery_levels
                )
                
                print(f"Step {i+1}: {current} -> {next_topic}")
                
                # Prevent infinite loop
                if not next_topic or next_topic in visited:
                    print(f"No new topic found, stopping")
                    break
                    
                current = next_topic
                
            except Exception as e:
                print(f"Error getting next topic: {e}")
                break
        
        # If path is empty, add starting topic
        if not path:
            print("Path is empty, adding default")
            path.append({
                'topic': 'Variables',
                'mastery': 0.1,
                'level': 'Novice',
                'difficulty': 1
            })
        
        print(f"Final path: {[p['topic'] for p in path]}")
        return jsonify({'path': path})
        
    except Exception as e:
        print(f"ERROR in learning path: {e}")
        import traceback
        traceback.print_exc()
        # Return default path on error
        return jsonify({
            'path': [{
                'topic': 'Variables',
                'mastery': 0.1,
                'level': 'Novice',
                'difficulty': 1
            }]
        })


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    print(f"404 Error: {request.url}")
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    print(f"500 Error: {e}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("=" * 70)
    print(" 🧠 IntelliLearn Web Application Starting...")
    print("=" * 70)
    print(f"\n📁 Working directory: {os.getcwd()}")
    print(f"📊 Loaded {len(TOPICS)} topics")
    print(f"❓ Loaded {sum(len(q) for q in QUESTIONS.values())} questions")
    print("\n📍 Server: http://localhost:5000")
    print("🎓 Open your browser and visit the URL above")
    print("\nPress Ctrl+C to stop the server\n")
    print("=" * 70)
    
    # List all registered routes
    print("\n📝 Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"   {rule.methods} {rule.rule}")
    print("=" * 70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)