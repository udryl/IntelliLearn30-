"""
Q-Learning Implementation for Learning Path Recommendation
Uses Reinforcement Learning to optimize topic sequencing
"""

import random
import json

class QLearningRecommender:
    def __init__(self, topics, alpha=0.1, gamma=0.9, epsilon=0.2):
        """
        Initialize Q-Learning recommender
        
        Args:
            topics: Dictionary of topics with prerequisites and difficulty
            alpha: Learning rate (0-1)
            gamma: Discount factor (0-1)
            epsilon: Exploration rate (0-1)
        """
        self.topics = list(topics.keys())
        self.topic_info = topics
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        
        # Initialize Q-table: Q[state][action] = value
        self.q_table = {}
        for topic in self.topics:
            self.q_table[topic] = {t: 0.0 for t in self.topics}
    
    def get_reward(self, mastery_level, difficulty, prereqs_met):
        """
        Calculate reward for choosing a topic
        
        Args:
            mastery_level: Current mastery (0-1)
            difficulty: Topic difficulty (1-5)
            prereqs_met: Whether prerequisites are satisfied
            
        Returns:
            float: Reward value
        """
        if not prereqs_met:
            return -10  # Strong penalty for skipping prerequisites
        
        # Calculate difficulty-mastery gap
        normalized_difficulty = difficulty / 5.0
        gap = abs(normalized_difficulty - mastery_level)
        
        # Reward based on Zone of Proximal Development
        if gap < 0.2:
            return 10  # Perfect match - optimal challenge
        elif gap < 0.4:
            return 5   # Good match
        elif gap < 0.6:
            return 0   # Acceptable
        else:
            return -5  # Poor match (too easy or too hard)
    
    def recommend_next(self, current_topic, mastery_levels):
        """
        Recommend next topic using epsilon-greedy strategy
        
        Args:
            current_topic: Current topic being studied
            mastery_levels: Dictionary of mastery levels for all topics
            
        Returns:
            str: Recommended next topic
        """
        # Filter available topics (prerequisites met)
        available = [
            t for t in self.topics 
            if self._prereqs_met(t, mastery_levels)
        ]
        
        if not available:
            return self.topics[0]  # Default to first topic
        
        # Epsilon-greedy: explore vs exploit
        if random.random() < self.epsilon:
            return random.choice(available)  # Explore
        
        # Exploit: choose best Q-value
        q_values = {
            t: self.q_table[current_topic].get(t, 0) 
            for t in available
        }
        
        best_topic = max(q_values, key=q_values.get)
        return best_topic
    
    def update_q_value(self, state, action, reward, next_state):
        """
        Update Q-table using Q-Learning formula
        Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]
        
        Args:
            state: Current topic
            action: Next topic chosen
            reward: Reward received
            next_state: Resulting topic
        """
        current_q = self.q_table[state][action]
        max_next_q = max(self.q_table[next_state].values())
        
        new_q = current_q + self.alpha * (
            reward + self.gamma * max_next_q - current_q
        )
        
        self.q_table[state][action] = new_q
    
    def _prereqs_met(self, topic, mastery_levels):
        """Check if prerequisites are sufficiently mastered"""
        prereqs = self.topic_info[topic].get('prereqs', [])
        return all(mastery_levels.get(p, 0) > 0.6 for p in prereqs)
    
    def save_model(self, filepath):
        """Save Q-table to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.q_table, f, indent=2)
    
    def load_model(self, filepath):
        """Load Q-table from JSON file"""
        with open(filepath, 'r') as f:
            self.q_table = json.load(f)
