from typing import List, Dict, Any

class MasterRouter:
    def __init__(self):
        self.routing_rules = {
            'lab_results': ['h3o', 'precision_med'],
            'biomarkers': ['h3o', 'precision_med'],
            'food_photo': ['mha', 'h3o'],
            'meal_logging': ['mha'],
            'workout_video': ['vpc', 'h3o'],
            'training_data': ['vpc'],
            'weekly_checkin': ['dayone', 'h3o'],
            'program_milestone': ['dayone'],
            'medical_question': ['precision_med', 'h3o'],
            'health_concern': ['precision_med', 'h3o'],
            'general_health': ['h3o'],
            'habit_tracking': ['mha', 'dayone']
        }

    def classify_input(self, data: str) -> str:
        data_lower = data.lower()
        if any(term in data_lower for term in ['lab', 'blood', 'cholesterol', 'glucose', 'hba1c']):
            return 'lab_results'
        if any(term in data_lower for term in ['food', 'meal', 'ate', 'calories', 'protein']):
            return 'meal_logging'
        if any(term in data_lower for term in ['workout', 'exercise', 'training', 'gym']):
            return 'training_data'
        if any(term in data_lower for term in ['week', 'progress', 'milestone', 'goal']):
            return 'weekly_checkin'
        if any(term in data_lower for term in ['pain', 'symptom', 'medication', 'doctor']):
            return 'medical_question'
        return 'general_health'

    def get_agents_for_input(self, input_type: str) -> List[str]:
        return self.routing_rules.get(input_type, ['h3o'])
