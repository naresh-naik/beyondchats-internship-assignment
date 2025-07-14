# persona_generator.py (Gemini Version with Professional Dossier Prompt)

"""
A command-line tool to generate a professional user persona dossier from a
Reddit profile URL.

This script scrapes a user's recent Reddit activity and uses the Google Gemini API
to analyze the text and generate a highly-structured, professional brief.

Usage:
    python persona_generator.py <reddit_profile_url>
"""

import argparse
import os
import sys
from typing import List, Optional
from urllib.parse import urlparse

import praw
from prawcore.exceptions import NotFound
import google.generativeai as genai

# --- CONFIGURATION ---
# IMPORTANT: Fill in your API credentials below.
# Do not share your keys publicly.
REDDIT_CLIENT_ID = "YOUR_REDDIT_CLIENT_ID_HERE"
REDDIT_CLIENT_SECRET = "YOUR_REDDIT_CLIENT_SECRET_HERE"
REDDIT_USER_AGENT = "PersonaGenerator/0.1 by YourUsername" # Feel free to change YourUsername
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"


# --- Helper & Scraping Functions (Unchanged) ---

def extract_username_from_url(url: str) -> Optional[str]:
    # This function is unchanged
    try:
        parsed_url = urlparse(url)
        if "reddit.com" not in parsed_url.netloc:
            return None
        path_parts = [part for part in parsed_url.path.split("/") if part]
        if len(path_parts) >= 2 and path_parts[0].lower() == "user":
            return path_parts[1]
    except Exception:
        return None
    return None


def scrape_reddit_user(username: str) -> Optional[str]:
    # This function is unchanged
    try:
        reddit = praw.Reddit(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT
        )
        reddit.user.me()
        print("✅ Reddit Authentication successful.")
    except Exception as e:
        print(f"❌ Error: Reddit authentication failed. Details: {e}", file=sys.stderr)
        return None

    collected_data: List[str] = []
    delimiter = "\n\n---\n\n"
    try:
        print(f"🔎 Fetching data for user: /u/{username}...")
        redditor = reddit.redditor(username)
        print("📄 Scraping recent comments...")
        comments = list(redditor.comments.new(limit=100))
        for comment in comments:
            collected_data.append(
                f"COMMENT\nPermalink: https://www.reddit.com{comment.permalink}\n\n{comment.body}"
            )
        print(f"   - Found {len(comments)} comments.")
        print("✍️ Scraping recent submissions...")
        submissions = list(redditor.submissions.new(limit=50))
        for submission in submissions:
            collected_data.append(
                f"SUBMISSION\nTitle: {submission.title}\nPermalink: https://www.reddit.com{submission.permalink}\n\n{submission.selftext or '[No body text]'}"
            )
        print(f"   - Found {len(submissions)} submissions.")
        if not collected_data:
            print(f"🤷 No recent activity found for user /u/{username}.")
            return ""
        return delimiter.join(collected_data)
    except NotFound:
        print(f"❌ Error: Reddit user '{username}' not found.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ An unexpected error occurred during scraping: {e}", file=sys.stderr)
        return None


# --- Core Analysis Function (UPDATED WITH THE NEW SUPER-PROMPT) ---

def generate_user_persona(user_data_string: str, username: str) -> Optional[str]:
    """
    Uses Google's Gemini model to generate a professional persona dossier.
    """
    if not user_data_string.strip():
        print("⚠️ Cannot generate persona: The provided user data is empty.")
        return "This user has no recent public activity to analyze."

    print("\n🧠 Contacting Google Gemini to generate professional dossier...")
    try:
        genai.configure(api_key='AIzaSyDE8ZjCMijZLLaCls72ZAjnB2bpKdkFcAE')
    except Exception as e:
        print(f"❌ Error: Failed to configure Gemini client. Details: {e}", file=sys.stderr)
        return None

    # The new, highly-detailed "super-prompt"
    full_prompt = f"""
Act as an expert corporate analyst and psychological profiler. Your sole task is to synthesize unstructured data from a Reddit user's posts and comments into a highly structured, professional persona dossier.

You must STRICTLY adhere to the format provided below. Do not deviate from the structure, headers, or formatting rules.

**CRUCIAL FORMATTING RULES:**
1. The entire output must be a single block of text.
2. Use the `|` character to create the table as shown.
3. For the lists in the "Detailed Analysis" section, every bullet point MUST follow this exact pattern: `*   **[Category]:** [Description] (Source: [permalink])`
4. Every single deduction, without exception, must be followed by its citation.
5. Base all deductions strictly on the provided text data. Do not invent information.

---
**[START OF TEMPLATE]**
======================================================================
                  USER PERSONA: {username}
======================================================================

### 1. AT A GLANCE (EXECUTIVE SUMMARY)

| Category          | Deduction                                       |
|-------------------|-------------------------------------------------|
| **Identity**      | [Fill with the user's likely name or online handle] |
| **Primary Role**  | [Fill with the user's most likely profession or role] |
| **Key Trait**     | [Fill with the single most defining personality trait] |
| **Location (Est.)**| [Fill with an estimated location if evidence exists, otherwise state 'Not enough data']  |


### 2. DETAILED ANALYSIS

#### A. Executive Summary
[A concise, one-paragraph summary of the user's identity, communication style, and core motivations. This section synthesizes the most critical findings into a narrative, citing the most important source(s).]

---

#### B. Key Characteristics & Behavioral Patterns
*   **[Trait Name]:** [Description of the trait with a specific example.] (Source: [permalink])
*   **[Trait Name]:** [Description of the trait with a specific example.] (Source: [permalink])

---

#### C. Identified Interests & Hobbies
*   **[Interest Area]:** [Details about the interest.] (Source: [permalink])
*   **[Interest Area]:** [Details about the interest.] (Source: [permalink])

---

#### D. Professional Profile
*   **[Deduced Profession/Field]:** [Details about the profession.] (Source: [permalink])
*   **[Supporting Evidence]:** [Details about the evidence.] (Source: [permalink])

**[END OF TEMPLATE]**
---

Now, analyze the following user data and generate the persona:

{user_data_string}
"""

    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        response = model.generate_content(full_prompt)
        print("✅ Dossier generated successfully.")
        return response.text
    except Exception as e:
        print(f"❌ An unexpected error occurred while contacting Gemini: {e}", file=sys.stderr)
        return None


# --- Main Execution Block (with minor update) ---

def main():
    parser = argparse.ArgumentParser(
        description="Generate a user persona dossier from a Reddit profile URL using Gemini.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("profile_url", type=str, help="The full URL of the Reddit user profile.")
    args = parser.parse_args()

    if "YOUR_CLIENT_ID" in CLIENT_ID or "YOUR_GEMINI_API_KEY" in GEMINI_API_KEY:
        print("🚨 CONFIGURATION ERROR...", file=sys.stderr)
        sys.exit(1)

    username = extract_username_from_url(args.profile_url)
    if not username:
        print(f"❌ Error: Invalid Reddit user URL: '{args.profile_url}'", file=sys.stderr)
        sys.exit(1)

    print("-" * 50 + f"\n🚀 Starting process for user: /u/{username}\n" + "-" * 50)
    user_data = scrape_reddit_user(username)
    if user_data is None:
        sys.exit(1)

    # Pass the username to the persona generator so it can be used in the title
    persona_text = generate_user_persona(user_data, username)
    if persona_text is None:
        sys.exit(1)

    output_filename = f"{username}_persona.txt"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(persona_text)
    except IOError as e:
        print(f"❌ Error: Could not write to file '{output_filename}'. Details: {e}", file=sys.stderr)
        sys.exit(1)

    print("\n" + "=" * 50 + "\n✨ All done! ✨\n" + f"Persona for user '{username}' has been successfully generated and saved to {output_filename}\n" + "=" * 50)


if __name__ == "__main__":
    main()