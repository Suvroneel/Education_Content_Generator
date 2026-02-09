"""
Advanced Content Validator
Additional validation checks beyond basic reviewer
"""

import re
from typing import Dict, List, Tuple

class AdvancedValidator:
    """Advanced validation for educational content"""
    
    # Common educational topics by grade
    GRADE_TOPICS = {
        1: ['counting', 'addition', 'subtraction', 'shapes', 'colors'],
        2: ['multiplication', 'time', 'money', 'measurement'],
        3: ['division', 'fractions', 'area', 'perimeter'],
        4: ['decimals', 'angles', 'geometry', 'factors'],
        5: ['percentages', 'volume', 'coordinates', 'equations'],
    }
    
    @staticmethod
    def check_reading_level(text: str, grade: int) -> Tuple[bool, str]:
        """
        Check if text reading level matches grade
        Uses simplified Flesch-Kincaid approximation
        """
        if not text:
            return False, "Empty text"
        
        # Count sentences
        sentences = len(re.split(r'[.!?]+', text))
        if sentences == 0:
            sentences = 1
        
        # Count words
        words = len(text.split())
        if words == 0:
            return False, "No words in text"
        
        # Count syllables (simplified)
        syllables = sum(AdvancedValidator._count_syllables(word) for word in text.split())
        
        # Flesch-Kincaid Grade Level formula (simplified)
        avg_words_per_sentence = words / sentences
        avg_syllables_per_word = syllables / words if words > 0 else 0
        
        reading_level = (0.39 * avg_words_per_sentence) + (11.8 * avg_syllables_per_word) - 15.59
        
        # Allow ±2 grade levels
        if abs(reading_level - grade) <= 2:
            return True, f"Reading level appropriate (~Grade {reading_level:.1f})"
        else:
            return False, f"Reading level mismatch: text is Grade {reading_level:.1f}, target is Grade {grade}"
    
    @staticmethod
    def _count_syllables(word: str) -> int:
        """Count syllables in a word (simplified)"""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Adjust for silent 'e'
        if word.endswith('e'):
            syllable_count -= 1
        
        # At least one syllable
        return max(1, syllable_count)
    
    @staticmethod
    def check_mcq_quality(mcqs: List[Dict]) -> Tuple[bool, List[str]]:
        """Advanced MCQ validation"""
        issues = []
        
        for i, mcq in enumerate(mcqs, 1):
            question = mcq.get('question', '')
            options = mcq.get('options', [])
            answer = mcq.get('answer', '')
            
            # Check for question quality
            if len(question.split()) < 5:
                issues.append(f"Q{i}: Question is too short (< 5 words)")
            
            if question.endswith('.'):
                issues.append(f"Q{i}: Question should end with '?' not '.'")
            
            # Check options
            if len(options) != 4:
                issues.append(f"Q{i}: Should have exactly 4 options")
                continue
            
            # Check for similar options
            option_texts = [opt.split(') ', 1)[1] if ') ' in opt else opt for opt in options]
            for j, opt1 in enumerate(option_texts):
                for k, opt2 in enumerate(option_texts[j+1:], j+1):
                    if AdvancedValidator._are_similar(opt1, opt2):
                        issues.append(f"Q{i}: Options {j+1} and {k+1} are too similar")
            
            # Check answer validity
            if answer not in ['A', 'B', 'C', 'D']:
                issues.append(f"Q{i}: Invalid answer '{answer}'")
            
            # Check for "all/none of the above"
            all_none_count = sum(1 for opt in option_texts if 'all of the above' in opt.lower() or 'none of the above' in opt.lower())
            if all_none_count > 1:
                issues.append(f"Q{i}: Has multiple 'all/none of above' options")
        
        return len(issues) == 0, issues
    
    @staticmethod
    def _are_similar(text1: str, text2: str, threshold: float = 0.8) -> bool:
        """Check if two texts are too similar"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return False
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        similarity = intersection / union if union > 0 else 0
        return similarity >= threshold
    
    @staticmethod
    def check_explanation_structure(explanation: str, grade: int) -> Tuple[bool, List[str]]:
        """Check if explanation has good structure"""
        issues = []
        
        # Check length
        word_count = len(explanation.split())
        min_words = 30 + (grade * 5)  # Higher grades need more detail
        max_words = 150 + (grade * 10)
        
        if word_count < min_words:
            issues.append(f"Explanation too brief ({word_count} words, need ~{min_words})")
        elif word_count > max_words:
            issues.append(f"Explanation too long ({word_count} words, max ~{max_words})")
        
        # Check for paragraphs
        paragraphs = explanation.split('\n\n')
        if len(paragraphs) < 2 and word_count > 100:
            issues.append("Long explanation should be split into paragraphs")
        
        # Check for examples (good for learning)
        example_markers = ['example', 'like', 'such as', 'for instance', 'imagine']
        has_example = any(marker in explanation.lower() for marker in example_markers)
        
        if not has_example and grade <= 6:
            issues.append("Consider adding examples for better understanding")
        
        # Check for engagement
        questions = explanation.count('?')
        if questions == 0 and grade <= 5:
            issues.append("Could use questions to engage younger students")
        
        return len(issues) == 0, issues
    
    @staticmethod
    def validate_topic_appropriateness(topic: str, grade: int) -> Tuple[bool, str]:
        """Check if topic is appropriate for grade level"""
        topic_lower = topic.lower()
        
        # Check if it's too advanced
        advanced_topics = {
            'calculus', 'derivatives', 'integrals', 'quantum', 'molecular',
            'biochemistry', 'thermodynamics', 'electromagnetism'
        }
        
        if grade < 9 and any(adv in topic_lower for adv in advanced_topics):
            return False, f"Topic '{topic}' may be too advanced for Grade {grade}"
        
        # Check if it's too basic
        if grade > 8 and any(basic in topic_lower for basic in ['counting', 'colors', 'shapes']):
            return False, f"Topic '{topic}' may be too basic for Grade {grade}"
        
        return True, "Topic appropriateness OK"
    
    @staticmethod
    def comprehensive_validation(content: Dict, grade: int, topic: str) -> Dict:
        """Run all validation checks"""
        results = {
            "valid": True,
            "checks": {}
        }
        
        explanation = content.get('explanation', '')
        mcqs = content.get('mcqs', [])
        
        # Reading level check
        reading_ok, reading_msg = AdvancedValidator.check_reading_level(explanation, grade)
        results["checks"]["reading_level"] = {
            "passed": reading_ok,
            "message": reading_msg
        }
        
        # Topic appropriateness
        topic_ok, topic_msg = AdvancedValidator.validate_topic_appropriateness(topic, grade)
        results["checks"]["topic_appropriateness"] = {
            "passed": topic_ok,
            "message": topic_msg
        }
        
        # MCQ quality
        mcq_ok, mcq_issues = AdvancedValidator.check_mcq_quality(mcqs)
        results["checks"]["mcq_quality"] = {
            "passed": mcq_ok,
            "issues": mcq_issues
        }
        
        # Explanation structure
        struct_ok, struct_issues = AdvancedValidator.check_explanation_structure(explanation, grade)
        results["checks"]["explanation_structure"] = {
            "passed": struct_ok,
            "issues": struct_issues
        }
        
        # Overall validity
        results["valid"] = all(check["passed"] for check in results["checks"].values())
        
        return results
