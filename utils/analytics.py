"""
Analytics Module - Track and visualize agent performance
Shows metrics like generation time, review pass rate, refinement frequency
"""

import json
import time
from datetime import datetime
from typing import Dict, List
import os

class AnalyticsTracker:
    def __init__(self):
        self.sessions = []
        # Use temp directory for cloud deployment safety
        import tempfile
        import os
        
        # Try to use a writable directory
        try:
            # For cloud deployments, use temp directory
            temp_dir = tempfile.gettempdir()
            self.analytics_file = os.path.join(temp_dir, "analytics_log.json")
        except:
            # Fallback: just keep in memory (won't persist)
            self.analytics_file = None
        
        self.load_history()
    
    def load_history(self):
        """Load previous analytics if available"""
        if not self.analytics_file:
            return
            
        if os.path.exists(self.analytics_file):
            try:
                with open(self.analytics_file, 'r') as f:
                    self.sessions = json.load(f)
            except:
                self.sessions = []
    
    def save_history(self):
        """Save analytics to file"""
        if not self.analytics_file:
            return  # Skip if no file path available
            
        try:
            with open(self.analytics_file, 'w') as f:
                json.dump(self.sessions, f, indent=2)
        except:
            # Silently fail if can't write (read-only filesystem)
            pass
    
    def log_session(self, session_data: Dict):
        """Log a complete generation session"""
        session = {
            "timestamp": datetime.now().isoformat(),
            "grade": session_data.get("grade"),
            "topic": session_data.get("topic"),
            "generation_time": session_data.get("generation_time", 0),
            "review_time": session_data.get("review_time", 0),
            "total_time": session_data.get("total_time", 0),
            "review_status": session_data.get("review_status", "unknown"),
            "feedback_count": session_data.get("feedback_count", 0),
            "refinement_needed": session_data.get("refinement_needed", False),
            "refinement_improved": session_data.get("refinement_improved", None),
            "mcq_count": session_data.get("mcq_count", 0),
            "explanation_length": session_data.get("explanation_length", 0)
        }
        
        self.sessions.append(session)
        self.save_history()
    
    def get_statistics(self) -> Dict:
        """Calculate aggregate statistics"""
        if not self.sessions:
            return {
                "total_generations": 0,
                "pass_rate": 0,
                "avg_generation_time": 0,
                "refinement_rate": 0,
                "most_common_grade": None,
                "total_topics": 0
            }
        
        total = len(self.sessions)
        passed = sum(1 for s in self.sessions if s['review_status'] == 'pass')
        refined = sum(1 for s in self.sessions if s['refinement_needed'])
        
        avg_gen_time = sum(s['generation_time'] for s in self.sessions) / total
        
        # Most common grade
        grades = [s['grade'] for s in self.sessions if s['grade']]
        most_common_grade = max(set(grades), key=grades.count) if grades else None
        
        # Unique topics
        topics = set(s['topic'] for s in self.sessions if s['topic'])
        
        return {
            "total_generations": total,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
            "avg_generation_time": avg_gen_time,
            "refinement_rate": (refined / total * 100) if total > 0 else 0,
            "most_common_grade": most_common_grade,
            "total_topics": len(topics),
            "avg_feedback_count": sum(s['feedback_count'] for s in self.sessions) / total if total > 0 else 0
        }
    
    def get_grade_distribution(self) -> Dict[int, int]:
        """Get distribution of content by grade"""
        distribution = {}
        for session in self.sessions:
            grade = session.get('grade')
            if grade:
                distribution[grade] = distribution.get(grade, 0) + 1
        return distribution
    
    def get_recent_sessions(self, limit: int = 10) -> List[Dict]:
        """Get most recent sessions"""
        return sorted(self.sessions, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def get_performance_trends(self) -> Dict:
        """Get performance trends over time"""
        if len(self.sessions) < 5:
            return {"insufficient_data": True}
        
        recent = self.sessions[-10:]
        older = self.sessions[-20:-10] if len(self.sessions) >= 20 else []
        
        recent_pass_rate = sum(1 for s in recent if s['review_status'] == 'pass') / len(recent) * 100
        older_pass_rate = sum(1 for s in older if s['review_status'] == 'pass') / len(older) * 100 if older else recent_pass_rate
        
        return {
            "improving": recent_pass_rate > older_pass_rate,
            "recent_pass_rate": recent_pass_rate,
            "older_pass_rate": older_pass_rate,
            "trend": "📈 Improving" if recent_pass_rate > older_pass_rate else "📉 Declining" if recent_pass_rate < older_pass_rate else "➡️ Stable"
        }
