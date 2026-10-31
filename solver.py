
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key from .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "Gemini API key not found. Please check your .env file."
    )

# Create Gemini client
client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(
        timeout=120000,
        retry_options=types.HttpRetryOptions(
            attempts=1
        )
    )
)


# Function to solve DSA questions
def solve_question(question, context=""):

    prompt = f"""
You are an expert Data Structures and Algorithms tutor.

Answer the student's question in simple English.

Follow these instructions:

For theory questions:
1. Give a clear definition.
2. Explain the concept.
3. Give a simple example.
4. Mention applications.

For programming questions:
1. Explain the approach.
2. Provide complete Python code.
3. Explain the code briefly.
4. Give time complexity.
5. Give space complexity.

For comparison questions:
Use a clear comparison table.

Use the uploaded PDF context when relevant.
Do not invent information that is not supported by the context.

PDF Context:
{context[:1500]}

Student Question:
{question}

Give a clear, accurate and well-structured answer.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=700,
                thinking_config=types.ThinkingConfig(
                    thinking_level="minimal"
                )
            )
        )

        if response.text:
            return response.text

        return "Gemini returned an empty response. Please try again."

    except Exception as e:

        error = str(e)

        if "503" in error or "UNAVAILABLE" in error:
            return (
                "Gemini is temporarily busy. "
                "Please try again after some time."
            )

        elif "504" in error or "DEADLINE_EXCEEDED" in error:
            return (
                "Gemini response timed out. "
                "Please try again."
            )

        elif "429" in error:
            return (
                "Gemini API request limit reached. "
                "Please try again later."
            )

        else:
            return f"Gemini API Error: {error}"
