CLASSIFIER_TASK_DESCRIPTION = """
Classify this employee question.

Allowed categories:
- Leave Policy
- Attendance
- Payroll
- Travel
- Insurance
- Employee Benefits
- Performance
- Recruitment
- Learning
- Onboarding
- Exit
- OutOfScope

Allowed intents:
- Information
- Eligibility
- Procedure
- Comparison
- Policy
- Document
- Unknown

Rules:
- Choose only one category.
- Choose only one intent.
- If unrelated to HR, use OutOfScope and Unknown.
- Never invent a category or intent.
- Return ONLY valid JSON.
- Do not return markdown.
- Do not explain your decision.

Required JSON:
{{"category":"...","intent":"..."}}

Question:
{question}
"""
