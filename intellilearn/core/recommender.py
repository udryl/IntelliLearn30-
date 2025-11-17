"""
Main Recommendation Engine
Combines BKT, Q-Learning, and Clustering
"""

from .bkt import BayesianKnowledgeTracing
from .q_learning import QLearningRecommender
from .clustering import LearningStyleClassifier

class IntelliLearnEngine:
    """Main engine combining all ML techniques"""
    
    def __init__(self, topics):
        """
        Initialize the recommendation engine
        
        Args:
            topics: Dictionary of topics with structure
        """
        self.bkt = BayesianKnowledgeTracing()
        self.q_learner = QLearningRecommender(topics)
        self.style_classifier = LearningStyleClassifier()
        self.topics = topics
        
        # Initialize mastery levels for all topics
        self.mastery_levels = {topic: 0.1 for topic in topics.keys()}
    
    def process_response(self, topic, is_correct, time_spent, attempts):
        """
        Process a student response and update mastery
        
        Args:
            topic: Topic being studied
            is_correct: Whether answer was correct
            time_spent: Time spent on question (seconds)
            attempts: Number of attempts made
            
        Returns:
            dict: Updated mastery information
        """
        # Update mastery using BKT
        current_mastery = self.mastery_levels[topic]
        new_mastery = self.bkt.update_mastery(current_mastery, is_correct)
        self.mastery_levels[topic] = new_mastery
        
        return {
            'topic': topic,
            'previous_mastery': current_mastery,
            'new_mastery': new_mastery,
            'improvement': new_mastery - current_mastery,
            'level': self.bkt.get_mastery_level(new_mastery)
        }
    
    def get_recommendation(self, current_topic, responses):
        """
        Get personalized learning recommendation
        
        Args:
            current_topic: Current topic being studied
            responses: List of all student responses
            
        Returns:
            dict: Recommendation with next topic and learning style
        """
        # Get next topic from Q-Learning
        next_topic = self.q_learner.recommend_next(
            current_topic, 
            self.mastery_levels
        )
        
        # Determine learning style using clustering
        learning_style = self.style_classifier.predict_style(responses)
        style_info = self.style_classifier.get_style_description(learning_style)
        
        # Calculate reward and update Q-Learning
        if next_topic:
            prereqs_met = all(
                self.mastery_levels.get(p, 0) > 0.6 
                for p in self.topics[next_topic]['prereqs']
            )
            
            reward = self.q_learner.get_reward(
                self.mastery_levels.get(next_topic, 0.1),
                self.topics[next_topic]['difficulty'],
                prereqs_met
            )
            
            self.q_learner.update_q_value(
                current_topic,
                next_topic,
                reward,
                next_topic
            )
        
        return {
            'next_topic': next_topic,
            'mastery_level': self.mastery_levels.get(next_topic, 0),
            'learning_style': learning_style,
            'style_info': style_info,
            'all_mastery': self.mastery_levels.copy()
        }
