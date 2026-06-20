"""
content_agent.py

A CLI tool that generates, drafts, and revises social media posts
using the Claude API. Takes a topic, generates 3 post ideas across
different platforms, drafts the selected idea into a full post,
and allows iterative revision before saving to output/posts.json.

Author: Siya Jariwala
"""

#importing required libraries

import json
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
    Generate 3 post ideas related to the topic: '{topic}'.
    Return ONLY valid JSON in this exact format, nothing else — no explanation, no markdown code fences:
[
    {{"platform": "LinkedIn", "tone": "Educational", "concept": "short concept here"}},
    {{"platform": "Twitter", "tone": "Provocative", "concept": "short concept here"}},
    {{"platform": "Instagram", "tone": "Personal", "concept": "short concept here"}}
]


    Guidelines:
         - Each idea is a SHORT bullet-style concept — a quick pitch, not a full outline. Keep it brief.
         - Each idea targets a different platform: LinkedIn, Twitter, Instagram.
         - Pick a tone per idea (educational, provocative, personal, etc.) based on what fits the topic.
    </task>"""
            }
        ]
    )
    return response.content[0].text

#function to draft a full social media post based on the given idea
def draft_post(idea):
    response = client.messages.create(
        model = "claude-sonnet-4-5-20250929",
        max_tokens=1000,            
        system = " <Role> You are an expert and well experienced social media content stratergist. Write plainly and directly, like you're explaining something to a smart friend. Cut anything vague, buzzwordy, or safe. Back claims with specifics, not generalities </Role> ",
        messages=[
    {
    "role": "user", "content": f"""<task>
    Draft a full social media post based on the following idea: '{idea}'. 
    The idea text above specifies the platform in brackets (e.g. [LinkedIn]). Write the post ONLY for that one platform — do not draft multiple versions.
    
    Guidelines:
         - Write in a tone that matches the idea (educational, provocative, personal, etc.).
         - Make it engaging and clear for the target platform (LinkedIn, Twitter, Instagram).
         - Include specific details or examples to support the main point.
         - Keep it concise and impactful — no fluff.
         - Do not use markdown symbols like ** for bold or # for headers — write in plain text.
         - Do not add a title, header, or label like "Social Media Post" — start directly with the post content.
         - Use short bullet points.
    </task>"""
            }
        ]
    )
    return response.content[0].text

def revise_post(post, feedback):
    response = client.messages.create(
        model = "claude-sonnet-4-5-20250929",
        max_tokens=1000,            
        system = " <Role> You are an expert and well experienced social media content stratergist. Write plainly and directly, like you're explaining something to a smart friend. Cut anything vague, buzzwordy, or safe. Back claims with specifics, not generalities </Role> ",
        messages=[
            {"role": "user", "content": f"""<task>
    Revise the following social media post based on this feedback: '{feedback}'. 
    Original Post: '{post}'
    Guidelines:
         - Address the specific feedback points while maintaining the original tone and intent of the post.
         - Make improvements that enhance clarity, engagement, and impact without adding unnecessary fluff.
         - After revising, Return the post with the revised change without explaining what you changed.
         - Keep the revised post concise and focused on the main message.
         - Do not use markdown symbols like ** for bold or # for headers — write in plain text. Emojis are fine if they fit the platform and tone.
         - Use short bullet points if appropriate.
    </task>"""
            }
        ]
    )
    return response.content[0].text




# Helper function to display ideas in a readable format
def display_ideas(ideas_list):
    for i, idea in enumerate(ideas_list, start=1):
        print(f"{i}. [{idea['platform']}] {idea['tone']} — {idea['concept']}")
        print()

    
# Example usage
if __name__ == "__main__":
    topic = "AI replacing humans in the workforce"
    
    ideas_json = generate_post_ideas(topic)
    
    ideas_json = ideas_json.strip()
    if ideas_json.startswith("```"):
        ideas_json = ideas_json.split("```")[1]
        if ideas_json.startswith("json"):
            ideas_json = ideas_json[4:]
    
    ideas_list = json.loads(ideas_json.strip())
    
    display_ideas(ideas_list)
    
    selected = ideas_list[0]  # hardcode picking #1 for this test
    print(f"\nDrafting post for: {selected['platform']}\n")
    
    post = draft_post(selected["concept"])
    print(post)
    
    print("\n--- Testing revision ---\n")
    revised = revise_post(post, "make it punchier")
    print(revised)