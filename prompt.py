prompt_template = """
Analyze the following social media post.

Return ONLY valid JSON in this format:

{{
    "tone": "",
    "intent": "",
    "communication_style": "",
    "summary": ""
}}

Social Media Post:
{post}
"""