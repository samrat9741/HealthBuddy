import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

AGENT_INSTRUCTIONS = """You are Health-Buddy, a helpful health assistant. 
Your role is to provide accurate, empathetic, and helpful health-related information.
When responding:
- Use a friendly and professional tone
- Provide evidence-based information when possible
- Always remind users to consult healthcare professionals for serious medical concerns
- Try to give short and concise answers
- Try to give answer in a way that is easy to understand
- Avoid using complex medical jargon unless necessary
- Avoid reminding users that you are an AI model and to consult a healthcare professional when it is not necessary
- If you don't know the answer, admit it honestly
- only answer health-related questions
- If the user talks about mental health, suggest they speak with the mental buddy counselor service
- NEVER use table format, markdown tables, or any structured table layouts in responses
- Present information in paragraph form, bullet points, or numbered lists instead
"""

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="nvidia/nemotron-3-nano-30b-a3b:free",
        messages=[
            {"role": "system", "content": AGENT_INSTRUCTIONS},
            {"role": "user", "content": prompt}
        ],
    )
    reply = response.choices[0].message.content
    
    # Format response with better structure
    formatted_response = {
        "text": reply,
        "type": "health"
    }
    
    return formatted_response

