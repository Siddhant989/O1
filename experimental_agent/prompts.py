"""
This module contains all the prompts used by the agent.
"""

def generate_dynamic_prompt(question, file_type=None, content_type=None):
    """
    Generate a simple, focused prompt based on the question and file type.
    """
    # Clean and normalize the question
    question = question.lower().strip()
    
    # Check if it's a summary request
    if any(word in question for word in ['summary', 'summarize', 'summarise', 'brief', 'overview', 'tell me about']):
        if file_type:
            if file_type.startswith("application/pdf"):
                return """
                Read through this PDF document and provide a clear, engaging summary:

                1. Key Points (3-5 bullet points):
                   - What are the main takeaways?
                   - What are the most important findings?
                   - What are the key conclusions?

                2. Quick Overview:
                   - What is the main topic?
                   - Who is the intended audience?
                   - What is the document's purpose?

                3. Interesting Insights:
                   - What unique or surprising information stands out?
                   - What makes this document noteworthy?
                   - What are the innovative ideas or approaches?

                4. Practical Applications:
                   - How can this information be used?
                   - What are the real-world implications?
                   - What actions can be taken based on this?

                Be concise, engaging, and focus on what matters most to the reader.

                Content to analyze:
                {content}
                """
            elif file_type in ["application/vnd.ms-excel", "text/csv"]:
                return """
                Analyze this data and provide an insightful summary:

                1. Quick Stats:
                   - What are the key numbers?
                   - What are the notable trends?
                   - What patterns emerge?

                2. Data Story:
                   - What story does this data tell?
                   - What are the most interesting findings?
                   - What surprises or anomalies appear?

                3. Business Impact:
                   - What are the practical implications?
                   - What decisions could this data inform?
                   - What opportunities or challenges does it reveal?

                4. Next Steps:
                   - What further analysis might be useful?
                   - What actions should be considered?
                   - What should be monitored going forward?

                Keep it practical and actionable. Focus on insights rather than raw numbers.

                Content to analyze:
                {content}
                """
            elif file_type.startswith("image"):
                return """
                Look at this image and provide an engaging description:

                1. First Impression:
                   - What immediately catches the eye?
                   - What's the main subject or focus?
                   - What's the overall mood or tone?

                2. Key Elements:
                   - What important details are present?
                   - What's happening in the image?
                   - What's the composition like?

                3. Deeper Meaning:
                   - What story does this image tell?
                   - What message does it convey?
                   - What context is important?

                4. Technical Aspects:
                   - How is color used?
                   - What about lighting and composition?
                   - What techniques are employed?

                Make it vivid and engaging, helping the reader visualize what you're describing.

                Content to analyze:
                {content}
                """
            else:
                return """
                Provide an engaging summary of this content:

                1. Main Points:
                   - What are the key takeaways?
                   - What's most important to understand?
                   - What are the core messages?

                2. Context:
                   - What's the background?
                   - Why is this important?
                   - Who is this relevant for?

                3. Highlights:
                   - What stands out?
                   - What's unique or interesting?
                   - What deserves special attention?

                4. Value:
                   - Why does this matter?
                   - How can this be used?
                   - What actions can be taken?

                Keep it clear, engaging, and focused on what matters most.

                Content to analyze:
                {content}
                """
    
    # For non-summary requests, use a focused prompt based on question type
    base_prompt = f"Answer this specific question about the content: {question}\n\n"
    
    # Add minimal context based on file type
    if file_type:
        if file_type.startswith("application/pdf"):
            base_prompt += "This is a PDF document. "
        elif file_type in ["application/vnd.ms-excel", "text/csv"]:
            base_prompt += "This is tabular data. "
        elif file_type.startswith("image"):
            base_prompt += "This is an image. "
    
    # Add focused instructions based on question type
    if "compare" in question or "difference" in question:
        base_prompt += "Focus only on the comparison aspects mentioned in the question."
    elif "why" in question or "how" in question:
        base_prompt += "Provide a direct explanation addressing the specific question."
    elif "list" in question or "what are" in question:
        base_prompt += "Provide a concise list of relevant items."
    
    # Add data-specific guidance for Excel/CSV files if relevant
    if file_type in ["application/vnd.ms-excel", "text/csv"] and any(term in question for term in ["average", "mean", "sum", "total", "calculate"]):
        base_prompt += "Include relevant numerical calculations in your answer."
    
    base_prompt += """
    
    Important:
    1. Answer ONLY the specific question asked
    2. Do not provide unnecessary additional information
    3. Be concise and direct
    4. If the question is unclear, ask for clarification
    
    Content to analyze:
    {content}
    """
    
    return base_prompt

# File type specific prompts for special cases only
FILE_PROMPTS = {
    "application/pdf": {
        "summary": "Provide a brief summary of this PDF document focusing on: {content}",
        "analysis": "Analyze this PDF document focusing specifically on: {content}"
    },
    "application/vnd.ms-excel": {
        "summary": "Provide a brief summary of this data focusing on: {content}",
        "analysis": "Analyze this data focusing specifically on: {content}"
    }
}

# Simplified conversational chain prompt
CONVERSATIONAL_CHAIN_PROMPT = '''
You are an AI assistant. Your task is to provide direct, focused answers to questions about the content.

Previous Context:
{memory_context}

Guidelines:
1. Answer ONLY what is asked
2. Be concise and specific
3. If unsure, ask for clarification
4. Use bullet points for lists
5. Include relevant examples when needed

Context: {context}
Web Search Results: {web_search}
Question: {question}

Answer:
''' 