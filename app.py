"""
Educational Content Generator - Streamlit UI
Multi-Agent System for generating and reviewing educational content
"""

import streamlit as st
import json
from datetime import datetime

from agents.generator_agent import GeneratorAgent
from agents.reviewer_agent import ReviewerAgent
from utils.analytics import AnalyticsTracker
from utils.export import ContentExporter
from utils.validator import AdvancedValidator

# Page config
st.set_page_config(
    page_title="Educational Content Generator",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-box {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        background-color: #f9f9f9;
    }
    .agent-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    .status-pass {
        color: #28a745;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .status-fail {
        color: #dc3545;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .feedback-item {
        background-color: #fff3cd;
        padding: 0.5rem;
        margin: 0.3rem 0;
        border-left: 4px solid #ffc107;
        border-radius: 4px;
    }
    .mcq-box {
        background-color: white;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border: 1px solid #ddd;
    }
    .correct-answer {
        background-color: #d4edda;
        padding: 0.3rem 0.6rem;
        border-radius: 4px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generator' not in st.session_state:
    st.session_state.generator = GeneratorAgent()
if 'reviewer' not in st.session_state:
    st.session_state.reviewer = ReviewerAgent()
if 'analytics' not in st.session_state:
    st.session_state.analytics = AnalyticsTracker()
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = None
if 'review_result' not in st.session_state:
    st.session_state.review_result = None
if 'refined_content' not in st.session_state:
    st.session_state.refined_content = None
if 'refined_review' not in st.session_state:
    st.session_state.refined_review = None
if 'advanced_validation' not in st.session_state:
    st.session_state.advanced_validation = None

def display_content(content, title="Generated Content"):
    """Display generated content in a nice format"""
    st.markdown(f'<div class="agent-title">{title}</div>', unsafe_allow_html=True)
    
    # Display explanation
    st.markdown("**Explanation:**")
    st.write(content['explanation'])
    
    st.markdown("---")
    
    # Display MCQs
    st.markdown("**Multiple Choice Questions:**")
    for i, mcq in enumerate(content['mcqs'], 1):
        st.markdown(f'<div class="mcq-box">', unsafe_allow_html=True)
        st.markdown(f"**Q{i}. {mcq['question']}**")
        
        for option in mcq['options']:
            st.write(f"   {option}")
        
        st.markdown(f'<div class="correct-answer">✓ Correct Answer: {mcq["answer"]}</div>', 
                   unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def display_review(review, title="Review Results"):
    """Display review results"""
    st.markdown(f'<div class="agent-title">{title}</div>', unsafe_allow_html=True)
    
    status = review['status']
    if status == "pass":
        st.markdown(f'<div class="status-pass">Status: PASS</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-fail">Status: FAIL</div>', unsafe_allow_html=True)
    
    st.markdown("**Feedback:**")
    for feedback_item in review['feedback']:
        st.markdown(f'<div class="feedback-item">• {feedback_item}</div>', unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">Educational Content Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Multi-Agent System for Creating Grade-Appropriate Educational Content</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### System Status")
    st.write("🟢 Generator Agent: Ready")
    st.write("🟢 Reviewer Agent: Ready")

# Main interface
st.markdown("### Input Parameters")

col1, col2 = st.columns(2)

with col1:
    grade = st.selectbox(
        "Select Grade Level",
        options=list(range(1, 13)),
        index=3,  # Default to Grade 4
        help="Choose the grade level of target students"
    )

with col2:
    # Dropdown with common topics
    common_topics = [
        "Custom (type your own)",
        "Types of angles",
        "Photosynthesis", 
        "Fractions and decimals",
        "Water cycle",
        "Solar system",
        "Parts of speech",
        "Addition and subtraction",
        "Pythagorean theorem",
        "Food chains"
    ]
    
    selected_topic = st.selectbox(
        "Select Topic",
        options=common_topics,
        help="Choose a pre-defined topic or select 'Custom' to enter your own"
    )
    
    # If custom, show text input
    if selected_topic == "Custom (type your own)":
        topic = st.text_input(
            "Enter Custom Topic",
            value="",
            placeholder="e.g., Types of triangles"
        )
    else:
        topic = selected_topic

st.markdown("---")

# Generate button
if st.button("Generate Content", type="primary", use_container_width=True):
    if not topic.strip():
        st.error("Please enter a topic!")
    else:
        # Start timing
        import time
        start_time = time.time()
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Generate content
        status_text.text("Generator Agent is creating content...")
        progress_bar.progress(25)
        
        gen_start = time.time()
        with st.spinner("Generating content..."):
            generated_content = st.session_state.generator.generate_content(grade, topic)
            st.session_state.generated_content = generated_content
        gen_time = time.time() - gen_start
        
        progress_bar.progress(50)
        
        # Step 2: Review content
        status_text.text("Reviewer Agent is evaluating content...")
        
        review_start = time.time()
        with st.spinner("Reviewing content..."):
            review_result = st.session_state.reviewer.review_content(
                generated_content, grade, topic
            )
            st.session_state.review_result = review_result
        review_time = time.time() - review_start
        
        # Advanced validation
        advanced_val = AdvancedValidator.comprehensive_validation(
            generated_content, grade, topic
        )
        st.session_state.advanced_validation = advanced_val
        
        progress_bar.progress(75)
        
        # Step 3: Refinement if needed
        refinement_needed = review_result['status'] == 'fail'
        refinement_improved = None
        
        if refinement_needed:
            status_text.text("Refining content based on feedback...")
            
            with st.spinner("Refining content..."):
                # Extract feedback for refinement
                feedback_list = review_result['feedback']
                
                # Regenerate with feedback
                refined_content = st.session_state.generator.generate_content(
                    grade, topic, feedback=feedback_list
                )
                st.session_state.refined_content = refined_content
                
                # Review refined content
                refined_review = st.session_state.reviewer.review_content(
                    refined_content, grade, topic
                )
                st.session_state.refined_review = refined_review
                
                # Check if refinement improved
                refinement_improved = refined_review['status'] == 'pass'
        
        progress_bar.progress(100)
        status_text.text("Process complete")
        
        total_time = time.time() - start_time
        
        # Log analytics
        st.session_state.analytics.log_session({
            "grade": grade,
            "topic": topic,
            "generation_time": gen_time,
            "review_time": review_time,
            "total_time": total_time,
            "review_status": review_result['status'],
            "feedback_count": len(review_result.get('feedback', [])),
            "refinement_needed": refinement_needed,
            "refinement_improved": refinement_improved,
            "mcq_count": len(generated_content.get('mcqs', [])),
            "explanation_length": len(generated_content.get('explanation', ''))
        })
        
        st.success(f"Content generation completed in {total_time:.2f}s")

# Display results
if st.session_state.generated_content is not None:
    st.markdown("---")
    st.markdown("## Results")
    
    # Create tabs for better organization
    tab1, tab2, tab3, tab4 = st.tabs([
        "Generated Content", 
        "Review & Feedback", 
        "Refinement",
        "Advanced Validation"
    ])
    
    with tab1:
        st.markdown('<div class="agent-box">', unsafe_allow_html=True)
        display_content(st.session_state.generated_content, "Initial Generated Content")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export options
        st.markdown("### Export Options")
        export_cols = st.columns(4)
        
        exporter = ContentExporter()
        
        with export_cols[0]:
            st.download_button(
                label="📄 JSON",
                data=exporter.to_json(st.session_state.generated_content, {
                    "grade": grade, "topic": topic
                }),
                file_name=f"content_grade{grade}_{topic.replace(' ', '_')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with export_cols[1]:
            st.download_button(
                label="📝 Text",
                data=exporter.to_text(st.session_state.generated_content, grade, topic),
                file_name=f"content_grade{grade}_{topic.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with export_cols[2]:
            st.download_button(
                label="📋 Markdown",
                data=exporter.to_markdown(
                    st.session_state.generated_content, grade, topic,
                    st.session_state.review_result
                ),
                file_name=f"content_grade{grade}_{topic.replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        with export_cols[3]:
            st.download_button(
                label="📚 Study Guide",
                data=exporter.to_study_guide(st.session_state.generated_content, grade, topic),
                file_name=f"study_guide_grade{grade}_{topic.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    with tab2:
        if st.session_state.review_result is not None:
            st.markdown('<div class="agent-box">', unsafe_allow_html=True)
            display_review(st.session_state.review_result, "Initial Review")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        if st.session_state.refined_content is not None:
            st.info("🔄 Content was refined based on reviewer feedback")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="agent-box">', unsafe_allow_html=True)
                display_content(st.session_state.refined_content, "Refined Content")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                if st.session_state.refined_review is not None:
                    st.markdown('<div class="agent-box">', unsafe_allow_html=True)
                    display_review(st.session_state.refined_review, "Final Review")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Download refined version
            st.download_button(
                label="📥 Download Refined JSON",
                data=json.dumps(st.session_state.refined_content, indent=2),
                file_name=f"content_refined_grade{grade}_{topic.replace(' ', '_')}.json",
                mime="application/json"
            )
        else:
            st.success("✅ No refinement needed - initial content passed all quality checks!")
    
    with tab4:
        if st.session_state.advanced_validation is not None:
            st.markdown('<div class="agent-box">', unsafe_allow_html=True)
            st.markdown('<div class="agent-title">🎯 Advanced Quality Validation</div>', unsafe_allow_html=True)
            
            validation = st.session_state.advanced_validation
            
            # Overall status
            if validation['valid']:
                st.success("All advanced validation checks passed")
            else:
                st.warning("Some advanced validation checks have issues")
            
            st.markdown("---")
            
            # Display each check
            checks = validation.get('checks', {})
            
            for check_name, check_data in checks.items():
                # Format check name
                display_name = check_name.replace('_', ' ').title()
                
                if check_data.get('passed', False):
                    st.success(f"✅ {display_name}")
                    if 'message' in check_data:
                        st.caption(check_data['message'])
                else:
                    st.error(f"❌ {display_name}")
                    if 'message' in check_data:
                        st.caption(check_data['message'])
                    if 'issues' in check_data and check_data['issues']:
                        for issue in check_data['issues']:
                            st.markdown(f"  • {issue}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Advanced validation will appear here after generation")

# Analytics section at bottom
if st.session_state.analytics.get_statistics()['total_generations'] > 0:
    st.markdown("---")
    st.markdown("## Analytics")
    
    stats = st.session_state.analytics.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Generations", stats['total_generations'])
    
    with col2:
        st.metric("Pass Rate", f"{stats['pass_rate']:.1f}%")
    
    with col3:
        st.metric("Avg Generation Time", f"{stats['avg_generation_time']:.1f}s")
    
    with col4:
        st.metric("Refinement Rate", f"{stats['refinement_rate']:.1f}%")
    
    # Additional stats
    if stats['most_common_grade']:
        st.caption(f"Most common grade: Grade {stats['most_common_grade']} | Total topics: {stats['total_topics']}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Multi-Agent Educational Content Generator | Built with Streamlit & Hugging Face</p>
    <p>100% Free & Open Source</p>
</div>
""", unsafe_allow_html=True)
