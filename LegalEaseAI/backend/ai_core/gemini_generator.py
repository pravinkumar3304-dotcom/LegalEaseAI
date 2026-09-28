from google import genai
import os
import time
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class GeminiDocumentGenerator:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in .env file"
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def generate_document(self, data):

        document_type = data.get(
            "document_type",
            "Document"
        )

        jurisdiction = data.get(
            "jurisdiction",
            ""
        )

        parties = data.get(
            "parties",
            []
        )

        terms = data.get(
            "terms",
            ""
        )

        effective_date = data.get(
            "effective_date",
            ""
        )

        language = data.get(
            "language",
            "English"
        )

        prompt = f"""
Create a professional draft {document_type}.

Jurisdiction:
{jurisdiction}

Parties:
{parties}

Terms:
{terms}

Effective Date:
{effective_date}

Language:
{language}

Use only the information provided.

Do not invent missing names,
addresses, dates, or amounts.

Create a clear and properly structured document.

Mention that this is a draft
requiring legal review.
"""

        model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        )

        # Retry if Gemini temporarily returns 503 / UNAVAILABLE
        for attempt in range(3):

            try:

                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                return response.text

            except Exception as e:

                error_message = str(e)

                if (
                    "503" in error_message
                    or "UNAVAILABLE" in error_message
                    or "high demand" in error_message.lower()
                ):

                    if attempt < 2:
                        wait_time = 2 ** attempt
                        time.sleep(wait_time)
                        continue

                raise e