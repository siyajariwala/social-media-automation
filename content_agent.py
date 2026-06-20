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
import datetime
from dotenv import load_dotenv

load_dotenv()

# Getting the API key from environment variables
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

#creating an object of the anthropic class
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

#function to generate post ideas based on the given topic
def generate_post_ideas(topic):
    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            system="<Role> You are an expert and well experienced social media content strategist. Write plainly and directly, like you're explaining something to a smart friend. Cut anything vague, buzzwordy, or safe. Back claims with specifics, not generalities </Role>",
            messages=[
                {
                    "role": "user",
                    "content": f"""<task>
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
         - Respect the emotional framing of the topic as written
    </task>"""
                }
            ]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error generating ideas: {e}")
        return None


#function to draft a full social media post based on the given idea
def draft_post(idea):
    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            system=" <Role> You are an expert and well experienced social media content stratergist. Write plainly and directly, like you're explaining something to a smart friend. Cut anything vague, buzzwordy, or safe. Back claims with specifics, not generalities </Role> ",
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
    except Exception as e:
        print(f"Error revising post: {e}")
        return None

def revise_post(post, feedback):
    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            system=" <Role> You are an expert and well experienced social media content stratergist. Write plainly and directly, like you're explaining something to a smart friend. Cut anything vague, buzzwordy, or safe. Back claims with specifics, not generalities </Role> ",
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
    except Exception as e:
        print(f"Error revising post: {e}")
        return None




# Helper function to display ideas in a readable format
def display_ideas(ideas_list):
    for i, idea in enumerate(ideas_list, start=1):
        print(f"{i}. [{idea['platform']}] {idea['tone']} — {idea['concept']}")
        print()

def save_post(post, platform):
    entry = {
        "timestamp": str(datetime.datetime.now()),
        "platform": platform,
        "content": post
    }
    
 
    os.makedirs("output", exist_ok=True)
    
    # loading existing posts if the file exists
    if os.path.exists("output/posts.json"):
        with open("output/posts.json", "r") as f:
            posts = json.load(f)
    else:
        posts = []
    
    # adding the new post
    posts.append(entry)

    # writing everything back
    with open("output/posts.json", "w") as f:
        json.dump(posts, f, indent=2)

# Main function to run the CLI tool
def main():
    topic = input("Enter a topic: ")
    print(f"\nGenerating ideas for: {topic}\n")
    
    ideas_json = generate_post_ideas(topic)
    
    if ideas_json is None:
        print("Failed to generate ideas. Exiting.")
        return
    
    ideas_json = ideas_json.strip()
    if ideas_json.startswith("```"):
        ideas_json = ideas_json.split("```")[1]
        if ideas_json.startswith("json"):
            ideas_json = ideas_json[4:]
    
    try:
        ideas_list = json.loads(ideas_json.strip())
    except json.JSONDecodeError:
        print("Failed to parse ideas. Please try again.")
        return
    
    display_ideas(ideas_list)
    
    while True:
        choice = input("\nSelect an idea (1-3): ")
        try:
            choice_index = int(choice) - 1
            selected = ideas_list[choice_index]
            break
        except (ValueError, IndexError):
            print("Please enter 1, 2, or 3.")
    
    print(f"\nYou selected: [{selected['platform']}] {selected['concept']}")
    print(f"\nDrafting post for: {selected['platform']}\n")
    
    post = draft_post(selected["concept"])
    
    if post is None:
        print("Failed to draft post. Exiting.")
        return
    
    print(post)
    
    while True:
        feedback = input("\nApprove or give feedback: ")
        if feedback.lower() == "approve":
            save_post(post, selected["platform"])
            print("\nSaved to output/posts.json")
            break
        revised = revise_post(post, feedback)
        if revised is None:
            print("Failed to revise post. Try again or type 'approve'.")
            continue
        post = revised
        print(f"\n{post}\n")


if __name__ == "__main__":
    main()