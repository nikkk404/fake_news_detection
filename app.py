from markupsafe import escape
from flask import Flask, render_template, request, url_for
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()
# Initialize Flask app
app = Flask(__name__)

# Set up the Google API Key
os.environ["GOOGLE_API_KEY"] = os.getenv("API_KEY")
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

MAX_TEXT_LENGTH = 1000
VALID_NEWS_CLASS = ["true", "fake"]

def fake_news_detection(text):
    prompt = f"""
    You are an advanced AI model specializing in text analysis. Analyze the given text and classify it as one of the following categories:

    1. True**: The information is accurate and verified.
    2. Fake**: The information is false or misleading.

    **Example Texts and Classifications:**
    - **True**: "The Earth revolves around the Sun."
    - **Fake**: "The Earth is flat."

    **Input Text:** {text}

    **Output Format:**
    - Return only a string class name
    - Example output for fake news:

    Analyze the text and return the correct classification (Only name in lowercase such as true or fake).
    Note: Don't return empty or null, at any cost return the corrected class
    """
    # prompt = f"""
    # You are an advanced AI model specializing in fact-checking and detecting misinformation in news articles and other text. Your analysis must be highly accurate and objective. Because your knowledge is limited to your training data, you must be conservative in your classifications and prioritize identifying claims that contradict well-established knowledge or lack supporting evidence from reputable sources.

    # **Key Considerations for Classification:**

    # *   **Verifiable Facts:**  Identify specific claims within the text that can be verified against reliable sources (e.g., reputable news organizations, government agencies, scientific studies, established encyclopedias).
    # *   **Source Reliability:** Assess the credibility and reputation of the source of the information. Is it a well-known and trusted news organization, or a website known for spreading misinformation?  If the source is not explicitly provided, consider the plausibility of the claims and whether they align with information from trusted sources.
    # *   **Sensationalism and Bias:** Be wary of sensational headlines, emotionally charged language, and obvious biases. These are often indicators of misinformation.
    # *   **Lack of Evidence:**  Pay close attention to claims that lack supporting evidence, such as citations, data, or expert opinions. Extraordinary claims require extraordinary evidence.
    # *   **Contradictions:** Identify any contradictions within the text itself or between the text and well-established facts.
    # *   **Date of Publication:** If the text refers to past events, consider whether the information is consistent with historical records and established timelines.

    # **Classification Categories:**

    # 1.  **True:** The information is accurate and supported by evidence from reliable sources. The claims are verifiable and consistent with established knowledge.
    # 2.  **Fake:** The information is demonstrably false, misleading, or based on fabricated claims. The claims contradict well-established facts or lack credible supporting evidence.
    # 3.  **Requires Verification:** The information is potentially questionable or lacks sufficient evidence to be classified as either true or fake. The claims may be plausible but require further investigation and verification from reliable sources.  This category should be used when the model's knowledge is insufficient to make a definitive determination.

    # **Example Texts and Classifications:**

    # *   **True:** "The Earth revolves around the Sun." (Well-established scientific fact)
    # *   **True:** "The President announced a new economic policy today, according to a statement from the White House." (Verifiable claim with a clear source)
    # *   **Fake:** "Vaccines cause autism." (Debunked conspiracy theory)
    # *   **Fake:** "The Earth is flat." (Contradicts scientific evidence)
    # *   **Requires Verification:** "A new study claims that drinking coffee cures cancer." (Extraordinary claim that requires careful scrutiny of the study's methodology and findings)
    # *   **Requires Verification:** "Aliens landed on Earth yesterday." (Extraordinary claim lacking credible evidence)
    # *   **Requires Verification:** "A local website claims that the mayor is secretly embezzling funds, but provides no evidence." (Unverified claim from a potentially unreliable source)

    # **Input Text:** {text}

    # **Output Format:**

    # -   Return only a single string representing the classification (e.g., "true", "fake", "requires verification").
    # -   Always return a classification, even if uncertain. If the information requires further investigation, return "requires verification". Return in lowercase.

    # Analyze the text and return the most accurate classification based on the criteria above. Prioritize accuracy and objectivity. When in doubt, classify as "requires verification". Note: Don't return empty or null, at any cost return the corrected class
    # """
    try:
        response = model.generate_content(prompt)
        if response and hasattr(response, 'text') and response.text:
            # Extract classification using regex
            classification = re.search(r'\b(true|fake)\b', response.text.strip().lower())
            if classification:
                return classification.group(1)
            else:
                logging.warning(f"Unexpected News classification: {response.text.strip()}")
                return "classification_invalid"  # Explicitly handle unexpected responses
        else:
            logging.warning("Gemini API returned an empty or invalid response.")
            return "detection_failed"

    except Exception as e:
        logging.exception(f"Error during fake news detection: {e}")
        return "detection_failed"

@app.route('/', methods=['GET', 'POST'])
def detect_fake_news():
    if request.method == 'POST':
        text = request.form.get('text', '').strip()

        # Input validation and sanitization
        if not text:
            return render_template("index.html", message="Text cannot be empty.")

        if len(text) > MAX_TEXT_LENGTH:
            return render_template("index.html", message=f"Text is too long (maximum {MAX_TEXT_LENGTH} characters).")

        text = escape(text)  # Sanitize for XSS protection

        try:
            classification = fake_news_detection(text)
            if classification == "detection_failed":
                return render_template("index.html", message="Detection failed. Please try again later.", input_text=text)
            elif classification == "classification_invalid":
                return render_template("index.html", message="Unexpected classification result. Please try again.", input_text=text)
            else:
                return render_template("index.html", input_text=text, predicted_class=classification)
        except Exception as e:
            logging.error(f"Error during fake news detection: {e}")
            return render_template("index.html", message="An error occurred during fake news detection.", input_text=text)
    return render_template("index.html")  # Render the form initially

if __name__ == '__main__':
    app.run(debug=True)