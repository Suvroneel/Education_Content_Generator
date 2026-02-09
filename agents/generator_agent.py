"""
Generator Agent - Creates educational content for specified grade and topic
Uses Hugging Face's free inference API (no API key required for rate-limited access)
"""

import requests
import json
import time
from typing import Dict, List

class GeneratorAgent:
    def __init__(self):
        # Using Hugging Face's free inference API
        # These models are free to use without API keys (with rate limits)
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        self.headers = {"Content-Type": "application/json"}
    
    def generate_content(self, grade: int, topic: str, feedback: List[str] = None) -> Dict:
        """
        Generate educational content for a given grade and topic
        
        Args:
            grade: Student grade level (1-12)
            topic: Educational topic to explain
            feedback: Optional feedback from reviewer for refinement
            
        Returns:
            Dictionary with explanation and MCQs
        """
        # Build prompt based on grade level
        prompt = self._build_prompt(grade, topic, feedback)
        
        # Call Hugging Face API
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self._call_hf_api(prompt)
                content = self._parse_response(response)
                return content
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2)  # Wait before retry
                    continue
                else:
                    # Fallback to template-based generation if API fails
                    return self._fallback_generation(grade, topic)
    
    def _build_prompt(self, grade: int, topic: str, feedback: List[str] = None) -> str:
        """Build the prompt for content generation"""
        
        feedback_section = ""
        if feedback:
            feedback_section = f"\n\nIMPORTANT - Address this feedback:\n" + "\n".join([f"- {f}" for f in feedback])
        
        prompt = f"""You are an educational content creator. Create content for Grade {grade} students about "{topic}".

REQUIREMENTS:
- Use simple language appropriate for {grade}-year-old students
- Provide a clear, easy-to-understand explanation
- Create 3 multiple choice questions to test understanding
- Each question should have 4 options (A, B, C, D)
- Include the correct answer for each question

{feedback_section}

Respond ONLY with valid JSON in this exact format:
{{
  "explanation": "Your explanation here in 2-3 simple paragraphs",
  "mcqs": [
    {{
      "question": "First question text?",
      "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
      "answer": "A"
    }},
    {{
      "question": "Second question text?",
      "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
      "answer": "B"
    }},
    {{
      "question": "Third question text?",
      "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
      "answer": "C"
    }}
  ]
}}

Generate the JSON now:"""
        
        return prompt
    
    def _call_hf_api(self, prompt: str) -> str:
        """Call Hugging Face API"""
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 800,
                "temperature": 0.7,
                "top_p": 0.9,
                "return_full_text": False
            }
        }
        
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '')
            return ''
        else:
            raise Exception(f"API call failed: {response.status_code}")
    
    def _parse_response(self, response_text: str) -> Dict:
        """Parse API response to extract JSON"""
        # Try to find JSON in the response
        try:
            # Look for JSON object in the text
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = response_text[start:end]
                content = json.loads(json_str)
                
                # Validate structure
                if 'explanation' in content and 'mcqs' in content:
                    return content
        except:
            pass
        
        # If parsing fails, raise exception to trigger fallback
        raise Exception("Failed to parse response")
    
    def _fallback_generation(self, grade: int, topic: str) -> Dict:
        """
        Fallback content generation using templates when API fails
        This ensures the app always works even without API access
        """
        
        # Grade-appropriate vocabulary
        grade_language = {
            1: "very simple",
            2: "simple", 
            3: "easy",
            4: "clear",
            5: "straightforward"
        }
        
        lang_level = grade_language.get(grade, "clear")
        
        # Template-based content for common topics
        templates = {
            "types of angles": {
                "explanation": f"""Angles are everywhere around us! When two lines meet at a point, they make an angle.

There are different types of angles based on how big they are. A right angle is like the corner of a book - it makes an 'L' shape. An acute angle is smaller than a right angle, like a slice of pizza. An obtuse angle is bigger than a right angle, like when you open a door wide.

Learning about angles helps us understand shapes and spaces better!""",
                "mcqs": [
                    {
                        "question": "What does a right angle look like?",
                        "options": ["A) Like the corner of a book", "B) Like a full circle", "C) Like a straight line", "D) Like the letter Z"],
                        "answer": "A"
                    },
                    {
                        "question": "Which angle is smaller than a right angle?",
                        "options": ["A) Obtuse angle", "B) Straight angle", "C) Acute angle", "D) Full angle"],
                        "answer": "C"
                    },
                    {
                        "question": "An obtuse angle is:",
                        "options": ["A) Smaller than a right angle", "B) Bigger than a right angle", "C) Equal to a right angle", "D) Always 180 degrees"],
                        "answer": "B"
                    }
                ]
            }
        }
        
        # Check if we have a template for this topic
        topic_lower = topic.lower()
        if topic_lower in templates:
            return templates[topic_lower]
        
        # Generic fallback
        return {
            "explanation": f"""Let's learn about {topic}! This is an important topic for Grade {grade} students.

{topic} is something we can see and use in our daily life. Understanding {topic} helps us solve problems and learn new things.

When you study {topic}, remember to practice and ask questions if something is not {lang_level}. Learning is a journey, and every step counts!""",
            "mcqs": [
                {
                    "question": f"What is the main idea of {topic}?",
                    "options": [
                        f"A) {topic} helps us learn",
                        f"B) {topic} is not important",
                        f"C) {topic} is only for older students",
                        "D) None of the above"
                    ],
                    "answer": "A"
                },
                {
                    "question": f"Why should Grade {grade} students learn about {topic}?",
                    "options": [
                        "A) It's too hard",
                        "B) It helps us understand the world better",
                        "C) It's boring",
                        "D) Only teachers need to know"
                    ],
                    "answer": "B"
                },
                {
                    "question": f"When learning {topic}, what should you do if you don't understand?",
                    "options": [
                        "A) Give up",
                        "B) Ask questions and practice",
                        "C) Ignore it",
                        "D) Only memorize without understanding"
                    ],
                    "answer": "B"
                }
            ]
        }
