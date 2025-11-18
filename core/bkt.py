"""
Bayesian Knowledge Tracing (BKT) Implementation
Estimates student mastery probability for each topic
"""

class BayesianKnowledgeTracing:
    def __init__(self, p_init=0.1, p_learn=0.3, p_slip=0.1, p_guess=0.25):
        """
        Initialize BKT with parameters
        
        Args:
            p_init: Initial knowledge probability
            p_learn: Learning rate per question
            p_slip: Probability of mistake despite knowing
            p_guess: Probability of correct guess without knowing
        """
        self.p_init = p_init
        self.p_learn = p_learn
        self.p_slip = p_slip
        self.p_guess = p_guess
    
    def update_mastery(self, current_mastery, is_correct):
        """
        Update mastery probability based on student response
        
        Args:
            current_mastery: Current mastery level (0-1)
            is_correct: Whether the answer was correct
            
        Returns:
            float: Updated mastery probability (0-1)
        """
        p_know = current_mastery
        
        if is_correct:
            # Bayes' rule: P(Know | Correct)
            p_correct = p_know * (1 - self.p_slip) + (1 - p_know) * self.p_guess
            if p_correct > 0:
                new_p_know = (p_know * (1 - self.p_slip)) / p_correct
            else:
                new_p_know = p_know
        else:
            # Bayes' rule: P(Know | Incorrect)
            p_incorrect = p_know * self.p_slip + (1 - p_know) * (1 - self.p_guess)
            if p_incorrect > 0:
                new_p_know = (p_know * self.p_slip) / p_incorrect
            else:
                new_p_know = p_know
        
        # Apply learning effect
        updated = new_p_know + self.p_learn * (1 - new_p_know)
        
        # Bound between 0 and 1
        return max(0.0, min(1.0, updated))
    
    def get_mastery_level(self, mastery):
        """Get descriptive mastery level"""
        if mastery >= 0.8:
            return "Expert"
        elif mastery >= 0.6:
            return "Proficient"
        elif mastery >= 0.4:
            return "Developing"
        elif mastery >= 0.2:
            return "Beginner"
        else:
            return "Novice"
