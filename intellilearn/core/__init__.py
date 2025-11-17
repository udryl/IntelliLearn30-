"""
IntelliLearn Core Package
Machine Learning Algorithms
"""

from .bkt import BayesianKnowledgeTracing
from .q_learning import QLearningRecommender
from .clustering import LearningStyleClassifier
from .recommender import IntelliLearnEngine

__all__ = [
    'BayesianKnowledgeTracing',
    'QLearningRecommender',
    'LearningStyleClassifier',
    'IntelliLearnEngine'
]
