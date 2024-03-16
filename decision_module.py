import random

# Define a DecisionMaker class
class DecisionModule:
    def __init__(self, decisions=None):
        self.decisions = decisions or []

    def add_decision(self, name, probability):
        if not any(decision['name'] == name for decision in self.decisions):
            self.decisions.append({'name': name, 'probability': probability})

    def remove_decision(self, name):
        self.decisions = [decision for decision in self.decisions if decision['name'] != name]

    def update_probability(self, name, new_probability):
        for decision in self.decisions:
            if decision['name'] == name:
                decision['probability'] = new_probability
                
    def make_decision(self):
        # Calculate probabilities
        probabilities = [decision['probability'] for decision in self.decisions]
        total_probability = sum(probabilities)
        normalized_probabilities = [prob / total_probability for prob in probabilities]
        # Make a decision based on probabilities
        decision = random.choices([decision['name'] for decision in self.decisions], weights=normalized_probabilities)[0]
        return decision