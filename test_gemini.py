
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(
        timeout=120000,
        retry_options=types.HttpRetryOptions(
            attempts=1
        )
    )
)

print("Testing Gemini 3.5 Flash-Lite...")

start = time.perf_counter()

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Reply with only the word HELLO.",
        config=types.GenerateContentConfig(
            max_output_tokens=10,
            thinking_config=types.ThinkingConfig(
                thinking_level="minimal"
            )
        )
    )

    print("Response:", response.text)

except Exception as e:
    print("API ERROR:")
    print(type(e).__name__)
    print(str(e))

finally:
    print(
        "Total API time:",
        round(time.perf_counter() - start, 2),
        "seconds"
    )
