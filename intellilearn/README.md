# 🧠 IntelliLearn

**Personalized Learning Navigation System using Machine Learning**

A college thesis project demonstrating:
- **Bayesian Knowledge Tracing (BKT)** - Probabilistic mastery estimation
- **Q-Learning** - Reinforcement learning for optimal sequencing
- **K-Means Clustering** - Learning style identification

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the demo
python run.py

# 3. Initialize database (optional)
python -c "from utils.mastery_state import init_database; init_database()"
```

## 📁 Project Structure

```
intellilearn/
├── core/              # ML algorithms
│   ├── bkt.py         # Bayesian Knowledge Tracing
│   ├── q_learning.py  # Q-Learning Recommender
│   ├── clustering.py  # K-Means Classifier
│   └── recommender.py # Main engine
├── data/              # Topics and questions
├── utils/             # Database utilities
└── run.py             # Demo script
```

## 🎓 ML Techniques

### 1. Bayesian Knowledge Tracing
Estimates probability that a student has mastered a topic based on their responses.

### 2. Q-Learning
Optimizes the sequence of topics to maximize long-term learning outcomes.

### 3. K-Means Clustering
Identifies learning style (visual, practical, conceptual) from behavior patterns.

## 📊 Features

- Real-time mastery tracking
- Adaptive topic sequencing
- Learning style identification
- SQLite database for progress storage
- Extensible architecture

## 🧪 Testing

Run the demo to see all components in action:
```bash
cd intellilearn
python run.py
```

## 📝 License

MIT License - Free for educational use

## 👨‍🎓 Author

College Thesis Project - Machine Learning for Education
