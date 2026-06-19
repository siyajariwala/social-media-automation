"""
content_agent.py

A CLI tool that generates, drafts, and revises social media posts
using the Claude API. Takes a topic, generates 3 post ideas across
different platforms, drafts the selected idea into a full post,
and allows iterative revision before saving to output/posts.json.

Author: Siya Jariwala
"""

#importing required libraries
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

# Getting the API key from environment variables
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

#creating an object of the anthropic class
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

#function to generate post ideas based on the given topic
def generate_post_ideas(topic):
    response = client.messages.create(
        model = "claude-sonnet-4-5-20250929",
        max_tokens=1000,
        system = " <Role> You are an expert and well experienced social media content stratergist. Write plainly and directly, like you're explaining something to a smart friend. Cut anything vague, buzzwordy, or safe. Back claims with specifics, not generalities </Role> ",
        messages=[
    {
    "role": "user", "content": f"""<task>
    Generate 3 post ideas related to the topic: '{topic}'. Format the response EXACTLY as follows, matching this structure:
        1. [LinkedIn] Educational :
        • Concept here 
        2. [Twitter] Provocative :
        • Concept here
        3. [Instagram] Personal :
        • Concept here

    Guidelines:
         - Each idea is a SHORT bullet-style concept — a quick pitch, not a full outline. Keep it brief.
         - Each idea targets a different platform: LinkedIn, Twitter, Instagram.
         - Pick a tone per idea (educational, provocative, personal, etc.) based on what fits the topic.
         - Plain text only — no markdown bold/headers.
    </task>"""
            }
        ]
    )
    return response.content[0].text

# Example usage
if __name__ == "__main__":
    ideas = generate_post_ideas("AI replacing humans in the workforce")
    print(ideas)
