# 🔧 Technical Documentation

## System Architecture

### Overview
This is a **multi-agent AI system** designed to generate educational content with built-in quality assurance. The system follows a pipeline architecture with three main stages: Generation, Review, and Refinement.

---

## Agent Details

### 1. Generator Agent (`agents/generator_agent.py`)

**Responsibility**: Create educational content tailored to specific grade levels and topics.

**Key Methods**:
```python
generate_content(grade: int, topic: str, feedback: List[str] = None) -> Dict
```

**Process Flow**:
1. Build age-appropriate prompt
2. Call Hugging Face API (Mistral-7B-Instruct)
3. Parse structured JSON response
4. Fallback to template if API fails

**Input Schema**:
```python
{
    "grade": int,        # 1-12
    "topic": str,        # e.g., "Types of angles"
    "feedback": [str]    # Optional refinement hints
}
```

**Output Schema**:
```python
{
    "explanation": str,           # 2-3 paragraph explanation
    "mcqs": [                     # Exactly 3 MCQs
        {
            "question": str,      # Question text with ?
            "options": [str],     # 4 options: A, B, C, D
            "answer": str         # One of: "A", "B", "C", "D"
        }
    ]
}
```

**Design Decisions**:
- **Free API**: Uses Hugging Face's free inference endpoint (no API key needed)
- **Fallback Mode**: Template-based generation ensures system always works
- **Deterministic**: Structured output format guaranteed
- **Grade-Aware**: Adjusts language complexity based on grade level

---

### 2. Reviewer Agent (`agents/reviewer_agent.py`)

**Responsibility**: Evaluate content quality and age-appropriateness.

**Key Methods**:
```python
review_content(content: Dict, grade: int, topic: str) -> Dict
```

**Evaluation Criteria**:

| Criterion | What It Checks |
|-----------|----------------|
| **Structure** | Required fields present and valid |
| **Age-Appropriateness** | Vocabulary and sentence complexity |
| **Clarity** | Explanation quality and engagement |
| **MCQ Quality** | Question relevance and correctness |
| **Topic Relevance** | Content relates to specified topic |

**Review Process**:
1. Check structure (fields present, correct types)
2. Analyze explanation (length, complexity, vocabulary)
3. Evaluate MCQs (format, difficulty, relevance)
4. Aggregate feedback
5. Determine pass/fail status

**Output Schema**:
```python
{
    "status": "pass" | "fail",
    "feedback": [str]              # List of issues/suggestions
}
```

**Pass/Fail Logic**:
- **PASS**: ≤3 minor issues, no critical issues
- **FAIL**: >3 issues OR any critical issues (missing fields, wrong structure)

**Sophistication**:
- Grade-specific vocabulary checks
- Sentence length analysis
- Engagement markers detection
- MCQ distractor quality evaluation

---

## Pipeline Logic

### Standard Flow
```
User Input → Generator Agent → Reviewer Agent → Display Results
```

### Refinement Flow (if review fails)
```
User Input → Generator Agent → Reviewer Agent (FAIL)
           ↓
    Feedback Loop
           ↓
Generator Agent (with feedback) → Reviewer Agent → Display Results
```

**Important**: System performs **maximum 1 refinement iteration** (as per requirements).

---

## UI Layer (`app.py`)

### Technology Stack
- **Framework**: Streamlit 1.31.0
- **Styling**: Custom CSS
- **State Management**: Streamlit session_state

### UI Components

1. **Input Section**
   - Grade selector (1-12 dropdown)
   - Topic text input
   - Generate button

2. **Progress Tracking**
   - Real-time status updates
   - Progress bar
   - Stage indicators

3. **Results Display** (3 tabs)
   - Tab 1: Initial generated content
   - Tab 2: Review feedback
   - Tab 3: Refined content (if applicable)

4. **Export Options**
   - Download as JSON
   - Includes metadata

### Session State Variables
```python
st.session_state.generator          # Generator Agent instance
st.session_state.reviewer           # Reviewer Agent instance
st.session_state.generated_content  # Initial generation
st.session_state.review_result      # Initial review
st.session_state.refined_content    # Refined generation (if needed)
st.session_state.refined_review     # Refined review (if needed)
```

---

## API Integration

### Hugging Face Inference API

**Endpoint**: `https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2`

**Model**: Mistral-7B-Instruct-v0.2
- Open-source instruction-following model
- Good balance of quality and speed
- Free tier available (rate-limited)

**Request Format**:
```python
{
    "inputs": "<prompt>",
    "parameters": {
        "max_new_tokens": 800,
        "temperature": 0.7,
        "top_p": 0.9,
        "return_full_text": False
    }
}
```

**Rate Limits**:
- Free tier: ~100 requests/hour
- No authentication required
- Subject to change

**Fallback Strategy**:
- If API fails/unavailable: Use template-based generation
- Ensures 100% uptime
- No degradation in user experience

---

## Data Flow

```
┌─────────────┐
│ User Input  │
│ grade=4     │
│ topic="..." │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Generator Agent    │
│  1. Build prompt    │
│  2. Call HF API     │
│  3. Parse JSON      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Generated Content   │
│ {explanation, mcqs} │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Reviewer Agent     │
│  1. Check structure │
│  2. Analyze content │
│  3. Validate MCQs   │
└──────┬──────────────┘
       │
       ▼
   ┌───┴───┐
   │Status?│
   └───┬───┘
       │
   ┌───┴────────┬────────────┐
   │            │            │
 PASS         FAIL       CRITICAL
   │            │            │
   ▼            ▼            ▼
Display    Refinement    Display
Results    + Re-review   Error
```

---

## Error Handling

### API Failures
```python
try:
    response = call_hf_api(prompt)
except Exception:
    return fallback_generation(grade, topic)
```

### Invalid JSON
```python
try:
    content = json.loads(response_text)
    validate_structure(content)
except:
    raise Exception("Trigger fallback")
```

### Missing Fields
- Reviewer catches and reports
- Triggers refinement if critical

---

## Performance Considerations

### Response Times
- **API call**: 2-5 seconds (depends on load)
- **Review**: <1 second (local computation)
- **Total pipeline**: 3-10 seconds

### Optimization Strategies
1. **Caching**: Streamlit auto-caches agent instances
2. **Lazy loading**: Agents initialized once per session
3. **Fallback**: No retry loops on API failures

---

## Testing

### Manual Testing
Run `test_agents.py`:
```bash
python test_agents.py
```

Tests:
- ✅ Agent initialization
- ✅ Content generation
- ✅ Review process
- ✅ Refinement logic

### Unit Test Coverage (Future)
```python
# Suggested test cases
test_generator_output_structure()
test_reviewer_pass_criteria()
test_reviewer_fail_criteria()
test_refinement_with_feedback()
test_api_fallback()
```

---

## Extension Points

### Adding New Models
Modify `generator_agent.py`:
```python
self.api_url = "https://api-inference.huggingface.co/models/YOUR_MODEL"
```

### Custom Evaluation Criteria
Extend `reviewer_agent.py`:
```python
def _check_custom_criteria(self, content):
    # Your logic here
    pass
```

### Additional Output Formats
Add to `app.py`:
```python
# Export as PDF, Word, etc.
st.download_button("Export as PDF", pdf_data, ...)
```

---

## Security Considerations

### No Sensitive Data
- No API keys stored
- No user data collected
- No authentication required

### Safe API Calls
- Timeout limits (30s)
- No eval() or exec()
- Input sanitization

### Content Safety
- Family-friendly content only
- Educational context enforced
- Age-appropriate language

---

## Scalability

### Current Limitations
- Single-user design
- Synchronous processing
- No database/persistence

### Future Scalability
- Add request queue
- Database for content storage
- User accounts (optional)
- Batch processing

---

## Maintenance

### Regular Updates Needed
- ☑️ Hugging Face API changes
- ☑️ Streamlit version updates
- ☑️ Python security patches

### Monitoring
- Check Streamlit Cloud logs
- Monitor API availability
- User feedback via GitHub issues

---

## Support & Contributing

### Getting Help
1. Check this documentation
2. Read README.md
3. Open GitHub issue
4. Contact maintainers

### Contributing Guidelines
1. Fork repository
2. Create feature branch
3. Write tests
4. Submit pull request
5. Follow code style

---

**Last Updated**: February 2024
**Version**: 1.0.0
