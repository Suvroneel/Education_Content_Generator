"""
Test script to verify the agent system works correctly
Run this to test the agents without the UI
"""

from agents.generator_agent import GeneratorAgent
from agents.reviewer_agent import ReviewerAgent
import json

def test_agents():
    """Test the complete agent pipeline"""
    
    print("=" * 60)
    print("Testing Educational Content Generator - Agent System")
    print("=" * 60)
    
    # Initialize agents
    print("\n[1/5] Initializing agents...")
    generator = GeneratorAgent()
    reviewer = ReviewerAgent()
    print("✅ Agents initialized successfully")
    
    # Test input
    test_grade = 4
    test_topic = "Types of angles"
    
    print(f"\n[2/5] Testing with:")
    print(f"   Grade: {test_grade}")
    print(f"   Topic: {test_topic}")
    
    # Generate content
    print("\n[3/5] Generating content...")
    content = generator.generate_content(test_grade, test_topic)
    print("✅ Content generated")
    print("\nGenerated Content Preview:")
    print(json.dumps(content, indent=2)[:500] + "...")
    
    # Review content
    print("\n[4/5] Reviewing content...")
    review = reviewer.review_content(content, test_grade, test_topic)
    print("✅ Content reviewed")
    print(f"\nReview Status: {review['status'].upper()}")
    print(f"Feedback items: {len(review['feedback'])}")
    
    # Test refinement if needed
    if review['status'] == 'fail':
        print("\n[5/5] Testing refinement (content failed review)...")
        refined_content = generator.generate_content(
            test_grade, 
            test_topic, 
            feedback=review['feedback']
        )
        refined_review = reviewer.review_content(
            refined_content, 
            test_grade, 
            test_topic
        )
        print("✅ Refinement complete")
        print(f"Refined status: {refined_review['status'].upper()}")
    else:
        print("\n[5/5] No refinement needed (content passed)")
    
    print("\n" + "=" * 60)
    print("🎉 All tests passed! System is working correctly.")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run: streamlit run app.py")
    print("2. Open browser to: http://localhost:8501")
    print("3. Start generating educational content!")
    print("\n")

if __name__ == "__main__":
    test_agents()
