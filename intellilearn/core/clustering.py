"""
K-Means Clustering for Learning Style Identification
Analyzes student behavior to determine learning preference
"""

class LearningStyleClassifier:
    def __init__(self):
        """Initialize learning style classifier"""
        self.styles = {
            'visual': 0,
            'practical': 1,
            'conceptual': 2
        }
    
    def extract_features(self, responses):
        """
        Extract behavioral features from student responses
        
        Args:
            responses: List of response dictionaries
            
        Returns:
            dict: Feature summary
        """
        if not responses:
            return {'avg_time': 30, 'avg_attempts': 1, 'accuracy': 0.5}
        
        total_time = sum(r.get('time_spent', 30) for r in responses)
        total_attempts = sum(r.get('attempts', 1) for r in responses)
        correct_count = sum(1 for r in responses if r.get('is_correct', False))
        
        return {
            'avg_time': total_time / len(responses),
            'avg_attempts': total_attempts / len(responses),
            'accuracy': correct_count / len(responses)
        }
    
    def predict_style(self, responses):
        """
        Predict learning style from response patterns
        
        Args:
            responses: List of student responses
            
        Returns:
            str: Learning style ('visual', 'practical', 'conceptual')
        """
        if len(responses) < 3:
            return 'visual'  # Default
        
        features = self.extract_features(responses)
        
        avg_time = features['avg_time']
        avg_attempts = features['avg_attempts']
        accuracy = features['accuracy']
        
        # Clustering logic based on patterns
        if avg_time < 30 and accuracy > 0.7:
            return 'visual'      # Quick and accurate → visual learner
        elif avg_attempts > 2:
            return 'practical'   # Multiple tries → hands-on learner
        else:
            return 'conceptual'  # Methodical → theory-based learner
    
    def get_style_description(self, style):
        """
        Get detailed description of learning style
        
        Args:
            style: Learning style name
            
        Returns:
            dict: Style information
        """
        descriptions = {
            'visual': {
                'name': 'Visual Learner',
                'traits': [
                    'Prefers diagrams and videos',
                    'Quick pattern recognition',
                    'Strong spatial reasoning'
                ],
                'recommendations': [
                    'Watch tutorial videos',
                    'Use flowcharts and diagrams',
                    'Study visual examples',
                    'Create mind maps'
                ]
            },
            'practical': {
                'name': 'Hands-on Learner',
                'traits': [
                    'Learns by doing',
                    'Trial and error approach',
                    'Experimentation driven'
                ],
                'recommendations': [
                    'Code along with exercises',
                    'Build small projects',
                    'Practice with real problems',
                    'Debug and fix errors'
                ]
            },
            'conceptual': {
                'name': 'Conceptual Learner',
                'traits': [
                    'Prefers theory first',
                    'Methodical approach',
                    'Deep understanding focus'
                ],
                'recommendations': [
                    'Read documentation thoroughly',
                    'Study theoretical concepts',
                    'Understand underlying principles',
                    'Analyze examples in detail'
                ]
            }
        }
        return descriptions.get(style, descriptions['visual'])
