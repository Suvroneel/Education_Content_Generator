"""
Reviewer Agent - Evaluates educational content quality
Checks for age-appropriateness, correctness, and clarity
"""

import re
from typing import Dict, List, Tuple

class ReviewerAgent:
    def __init__(self):
        # Grade-level vocabulary complexity thresholds
        self.max_word_length = {
            1: 8, 2: 9, 3: 10, 4: 11, 5: 12,
            6: 13, 7: 14, 8: 15, 9: 16, 10: 17
        }
        
        # Words too complex for lower grades
        self.complex_words_by_grade = {
            1: ['complex', 'difficult', 'sophisticated', 'intricate'],
            2: ['elaborate', 'comprehensive', 'significant'],
            3: ['fundamental', 'essential', 'particular'],
            4: ['perpendicular', 'parallel', 'symmetrical'],
        }
    
    def review_content(self, content: Dict, grade: int, topic: str) -> Dict:
        """
        Review generated content for quality and appropriateness
        
        Args:
            content: Generated content dictionary
            grade: Target grade level
            topic: Educational topic
            
        Returns:
            Dictionary with status (pass/fail) and feedback list
        """
        feedback = []
        
        # Check structure
        structure_feedback = self._check_structure(content)
        feedback.extend(structure_feedback)
        
        # Check explanation quality
        explanation_feedback = self._check_explanation(
            content.get('explanation', ''), 
            grade, 
            topic
        )
        feedback.extend(explanation_feedback)
        
        # Check MCQs quality
        mcq_feedback = self._check_mcqs(
            content.get('mcqs', []), 
            grade, 
            topic
        )
        feedback.extend(mcq_feedback)
        
        # Determine pass/fail
        critical_issues = [f for f in feedback if 'must' in f.lower() or 'missing' in f.lower()]
        status = "fail" if len(feedback) > 3 or len(critical_issues) > 0 else "pass"
        
        return {
            "status": status,
            "feedback": feedback if feedback else ["Content looks good!"]
        }
    
    def _check_structure(self, content: Dict) -> List[str]:
        """Check if content has required structure"""
        feedback = []
        
        if 'explanation' not in content:
            feedback.append("Missing 'explanation' field - must include explanation")
        
        if 'mcqs' not in content:
            feedback.append("Missing 'mcqs' field - must include questions")
        elif not isinstance(content['mcqs'], list):
            feedback.append("MCQs must be a list")
        elif len(content['mcqs']) < 3:
            feedback.append(f"Need at least 3 MCQs, found only {len(content['mcqs'])}")
        
        return feedback
    
    def _check_explanation(self, explanation: str, grade: int, topic: str) -> List[str]:
        """Check explanation for age-appropriateness and clarity"""
        feedback = []
        
        if not explanation or len(explanation.strip()) < 50:
            feedback.append("Explanation is too short - needs more detail")
            return feedback
        
        # Check sentence length (age-appropriate)
        sentences = re.split(r'[.!?]+', explanation)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        max_words_per_sentence = {
            1: 8, 2: 10, 3: 12, 4: 15, 5: 18,
            6: 20, 7: 22, 8: 25, 9: 28, 10: 30
        }
        
        max_words = max_words_per_sentence.get(grade, 20)
        
        for i, sentence in enumerate(sentences, 1):
            word_count = len(sentence.split())
            if word_count > max_words + 5:
                feedback.append(
                    f"Sentence {i} is too long ({word_count} words) for Grade {grade} - "
                    f"try breaking it into shorter sentences"
                )
        
        # Check for overly complex words
        words = explanation.lower().split()
        max_length = self.max_word_length.get(grade, 12)
        
        complex_words_found = []
        for word in words:
            # Clean word
            clean_word = re.sub(r'[^a-z]', '', word)
            if len(clean_word) > max_length + 3:
                complex_words_found.append(clean_word)
        
        if complex_words_found and grade <= 5:
            feedback.append(
                f"Some words may be too complex for Grade {grade}: {', '.join(set(complex_words_found[:3]))}"
            )
        
        # Check for grade-inappropriate vocabulary
        if grade in self.complex_words_by_grade:
            inappropriate = []
            for complex_word in self.complex_words_by_grade[grade]:
                if complex_word in explanation.lower():
                    inappropriate.append(complex_word)
            
            if inappropriate:
                feedback.append(
                    f"These words might be too advanced for Grade {grade}: {', '.join(inappropriate)}"
                )
        
        # Check if topic is mentioned
        if topic.lower() not in explanation.lower():
            feedback.append(f"Explanation should clearly mention the topic '{topic}'")
        
        # Check for engagement (questions, examples, relatable content)
        engagement_markers = ['?', 'example', 'like', 'imagine', 'think about', 'we can']
        has_engagement = any(marker in explanation.lower() for marker in engagement_markers)
        
        if not has_engagement and grade <= 5:
            feedback.append("Consider adding examples or questions to make it more engaging for young students")
        
        return feedback
    
    def _check_mcqs(self, mcqs: List[Dict], grade: int, topic: str) -> List[str]:
        """Check MCQ quality and appropriateness"""
        feedback = []
        
        for i, mcq in enumerate(mcqs, 1):
            # Check structure
            if 'question' not in mcq:
                feedback.append(f"Question {i} is missing the 'question' field")
                continue
            
            if 'options' not in mcq:
                feedback.append(f"Question {i} is missing the 'options' field")
                continue
            
            if 'answer' not in mcq:
                feedback.append(f"Question {i} is missing the 'answer' field")
                continue
            
            # Check options count
            if len(mcq['options']) != 4:
                feedback.append(f"Question {i} must have exactly 4 options (A, B, C, D)")
            
            # Check answer validity
            valid_answers = ['A', 'B', 'C', 'D']
            if mcq['answer'] not in valid_answers:
                feedback.append(f"Question {i} has invalid answer '{mcq['answer']}' - must be A, B, C, or D")
            
            # Check question clarity
            question_text = mcq['question']
            if len(question_text.split()) > 20 and grade <= 5:
                feedback.append(f"Question {i} is too wordy for Grade {grade} students")
            
            if not question_text.endswith('?'):
                feedback.append(f"Question {i} should end with a question mark")
            
            # Check if question tests understanding of the topic
            topic_words = set(topic.lower().split())
            question_words = set(question_text.lower().split())
            
            if not topic_words.intersection(question_words) and i == 1:
                # At least first question should relate to topic
                feedback.append(f"Question {i} should relate more directly to '{topic}'")
            
            # Check for trivial questions
            trivial_patterns = ['what is', 'define', 'meaning of']
            if any(pattern in question_text.lower() for pattern in trivial_patterns) and i > 1:
                feedback.append(f"Question {i} seems too basic - try testing deeper understanding")
            
            # Check options for reasonable distractors
            options_text = ' '.join(mcq['options']).lower()
            if 'none of the above' in options_text and 'all of the above' in options_text:
                feedback.append(f"Question {i} shouldn't have both 'none' and 'all' of the above")
        
        return feedback
    
    def get_refinement_hints(self, feedback: List[str]) -> str:
        """Convert feedback into actionable hints for refinement"""
        if not feedback or feedback == ["Content looks good!"]:
            return ""
        
        hints = "Please address the following:\n"
        for item in feedback:
            hints += f"- {item}\n"
        
        return hints
