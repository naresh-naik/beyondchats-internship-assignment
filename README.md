# AI/LLM Engineer Intern Assignment - User Persona Generator

This project is a Python script that generates a user persona based on a Reddit user's activity. It uses the PRAW library to scrape Reddit data and an LLM to analyze the text and build the persona.

## Features
- Scrapes recent comments and posts from a specified Reddit user.
- Utilizes a Large Language Model for in-depth text analysis.
- Generates a structured user persona including interests, personality, and more.
- Cites the source for each piece of analyzed information.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/beyondchats-internship-assignment.git
    cd beyondchats-internship-assignment
    ```

2.  **Install dependencies:**
    This project requires Python 3. You will also need to install the PRAW and OpenAI libraries.
    ```bash
    pip install praw openai
    ```

3.  **API Credentials:**
    You will need API credentials from both Reddit and OpenAI.
    - Open the `persona_generator.py` script.
    - Fill in your credentials in the placeholder variables at the top of the file:
      - `REDDIT_CLIENT_ID`
      - `REDDIT_CLIENT_SECRET`
      - `OPENAI_API_KEY`

## How to Run the Script

To generate a persona, run the script from your terminal with the user's Reddit profile URL as an argument:

`python persona_generator.py <URL_OF_REDDIT_PROFILE>`

## Sample Output
To demonstrate the script's capability, here is a snippet of the generated persona for the user `kojied`. The full output files for the sample users are included in the repository.

`======================================================================
 USER PERSONA: kojied
 1. AT A GLANCE (EXECUTIVE SUMMARY)
 Category	Deduction
 Identity	A knowledgeable and active custom keyboard enthusiast.
 Primary Role	Hobbyist, Community Contributor, Tech Enthusiast
 Key Trait	Helpful and detail-oriented
 Location (Est.)	Not specified `




