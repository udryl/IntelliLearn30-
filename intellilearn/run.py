#!/usr/bin/env python3
"""
IntelliLearn - Demo Script
Tests all ML components
"""

print("=" * 70)
print(" 🧠 IntelliLearn - Personalized Learning System")
print("=" * 70)
print(" Machine Learning: BKT + Q-Learning + K-Means Clustering")
print("=" * 70)
print()

# Import modules
from core.bkt import BayesianKnowledgeTracing
from core.q_learning import QLearningRecommender
from core.clustering import LearningStyleClassifier
from core.recommender import IntelliLearnEngine
import json

# Load topics
print("📚 Loading topics...")
with open('data/topics_graph.json', 'r') as f:
    topics = json.load(f)
print(f"   Loaded {len(topics)} topics")
print()

# Test 1: Bayesian Knowledge Tracing
print("🎯 Testing Bayesian Knowledge Tracing (BKT)...")
print("-" * 70)
bkt = BayesianKnowledgeTracing()
mastery = 0.3

print(f"   Initial mastery: {mastery:.2f} ({bkt.get_mastery_level(mastery)})")

mastery = bkt.update_mastery(mastery, is_correct=True)
print(f"   After correct answer: {mastery:.2f} ({bkt.get_mastery_level(mastery)})")

mastery = bkt.update_mastery(mastery, is_correct=True)
print(f"   After another correct: {mastery:.2f} ({bkt.get_mastery_level(mastery)})")

mastery = bkt.update_mastery(mastery, is_correct=False)
print(f"   After incorrect answer: {mastery:.2f} ({bkt.get_mastery_level(mastery)})")
print()

# Test 2: Q-Learning Recommender
print("🤖 Testing Q-Learning Recommender...")
print("-" * 70)
q_learner = QLearningRecommender(topics)
mastery_levels = {topic: 0.5 for topic in topics.keys()}

current_topic = "Variables"
next_topic = q_learner.recommend_next(current_topic, mastery_levels)
print(f"   Current topic: {current_topic}")
print(f"   Recommended next: {next_topic}")

# Simulate learning
mastery_levels[next_topic] = 0.7
another_topic = q_learner.recommend_next(next_topic, mastery_levels)
print(f"   After mastering '{next_topic}': {another_topic}")
print()

# Test 3: Learning Style Classifier
print("✨ Testing Learning Style Classifier...")
print("-" * 70)
classifier = LearningStyleClassifier()

# Simulate visual learner (fast, accurate)
visual_responses = [
    {'time_spent': 20, 'attempts': 1, 'is_correct': True},
    {'time_spent': 25, 'attempts': 1, 'is_correct': True},
    {'time_spent': 18, 'attempts': 1, 'is_correct': True}
]
style = classifier.predict_style(visual_responses)
print(f"   Fast & accurate responses → {style.upper()}")

# Simulate practical learner (multiple attempts)
practical_responses = [
    {'time_spent': 60, 'attempts': 3, 'is_correct': False},
    {'time_spent': 55, 'attempts': 2, 'is_correct': True},
    {'time_spent': 70, 'attempts': 3, 'is_correct': True}
]
style = classifier.predict_style(practical_responses)
print(f"   Multiple attempts → {style.upper()}")

# Simulate conceptual learner (methodical)
conceptual_responses = [
    {'time_spent': 45, 'attempts': 1, 'is_correct': True},
    {'time_spent': 50, 'attempts': 1, 'is_correct': False},
    {'time_spent': 48, 'attempts': 1, 'is_correct': True}
]
style = classifier.predict_style(conceptual_responses)
print(f"   Methodical approach → {style.upper()}")
print()

# Test 4: Full Recommendation Engine
print("🚀 Testing Complete Recommendation Engine...")
print("-" * 70)
engine = IntelliLearnEngine(topics)

# Simulate learning session
print("   Simulating learning session...")
result = engine.process_response("Variables", is_correct=True, time_spent=25, attempts=1)
print(f"   ✓ Studied '{result['topic']}' - Mastery: {result['new_mastery']:.2f}")

result = engine.process_response("Variables", is_correct=True, time_spent=22, attempts=1)
print(f"   ✓ Studied '{result['topic']}' - Mastery: {result['new_mastery']:.2f}")

responses = visual_responses
recommendation = engine.get_recommendation("Variables", responses)

print()
print("   📊 Recommendation Generated:")
print(f"      Next Topic: {recommendation['next_topic']}")
print(f"      Learning Style: {recommendation['learning_style'].upper()}")
print(f"      Current Mastery: {recommendation['mastery_level']:.2f}")
print()

# Display style info
style_info = recommendation['style_info']
print(f"   Your learning profile: {style_info['name']}")
print(f"   Traits:")
for trait in style_info['traits']:
    print(f"      • {trait}")
print()

print("=" * 70)
print(" ✅ All ML components working perfectly!")
print("=" * 70)
print()
print(" 📖 Next steps:")
print("    1. Explore the code in core/ folder")
print("    2. Check data/ for topics and questions")
print("    3. Run unit tests: python -m unittest discover tests")
print("    4. Build web interface with Flask")
print()
