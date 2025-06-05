from fastapi import FastAPI, Query, HTTPException
from groq import Groq
import os
from dotenv import load_dotenv
from pathlib import Path
import sys

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="GiftSnapGiftingAI Backend")

# Initialize Groq client if available
api_key = os.getenv("GIFTSNAP_API_KEY")

# Flag to track if we're using the real API or mock responses
using_mock = False

if api_key:
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        print(f"Warning: Could not initialize Groq client: {e}")
        using_mock = True
else:
    print("GIFTSNAP_API_KEY not found. Using mock responses.")
    using_mock = True

# Define system prompt for gift recommendation assistant
GIFTSNAP_SYSTEM_PROMPT = """
You are GiftSnapAI, an intelligent, creative, and personalized gift recommendation assistant. 
Your job is to help users find the perfect gift based on detailed input such as budget, recipient's age, 
hobbies, interests, location, and social media information. 

You are empathetic, concise, and always suggest thoughtful, unique, and feasible gift ideas. 
When a user clicks on a gift idea, you help find gift cards or create personalized gift cards if none exist.

You MUST ONLY discuss topics related to gift recommendations. If asked about other topics, politely redirect 
the conversation back to helping find the perfect gift.

For each gift recommendation, include:
1. Gift name and brief description
2. Approximate price range
3. Why it would be a good match for the recipient
4. Where to purchase it

If you don't have enough information to make good recommendations, ask clarifying questions.
"""

def generate_mock_response(prompt_content):
    """Generate a mock response when no API key is available"""
    import random
    from datetime import datetime
    
    # Simple gift idea templates
    templates = [
        "A personalized {item} that celebrates their love for {hobby}.",
        "A subscription box for {hobby} enthusiasts, delivered monthly.",
        "A high-quality {item} that would enhance their {hobby} experience.",
        "A {hobby}-themed weekend getaway or experience day."
    ]
    
    # Extract hobbies from the prompt (basic parsing)
    hobbies = []
    for line in prompt_content.split('\n'):
        if line.startswith("Hobbies:"):
            hobby_text = line.replace("Hobbies:", "").strip()
            hobbies = [h.strip() for h in hobby_text.split(',')]
            break
    
    # Common gift items
    items = ["book", "course", "toolkit", "digital assistant", "membership", "gadget", "workshop"]
    
    # Select hobbies and items
    selected_hobbies = random.sample(hobbies, min(3, len(hobbies))) if hobbies else ["favorite activity"]
    selected_items = random.sample(items, min(4, len(items)))
    
    response = f"# Gift Recommendations\n\nThank you for using GiftSnapAI! Here are some personalized gift ideas:\n\n"
    
    # Generate 3-4 gift ideas
    for i in range(4):
        hobby = selected_hobbies[i % len(selected_hobbies)]
        item = selected_items[i % len(selected_items)]
        template = random.choice(templates)
        
        gift_idea = template.format(hobby=hobby, item=item)
        price_range = f"${random.randint(25, 100)}-${random.randint(100, 200)}"
        
        response += f"### Gift Idea {i+1}: {item.title()} for {hobby.title()}\n\n"
        response += f"**Description:** {gift_idea}\n\n"
        response += f"**Price Range:** {price_range}\n\n"
        response += f"**Why it's perfect:** This gift aligns with their passion for {hobby} and would be a thoughtful way to show you care.\n\n"
        response += f"**Where to purchase:** Specialty {hobby} stores or online retailers like Amazon, Etsy, or dedicated {hobby} websites.\n\n"
    
    response += "\nI hope these suggestions help you find the perfect gift!"
    return response

def generate_gift_recommendation(save_to_file=True):
    """Generate a response using Groq API with GiftSnapAI persona using Prompt.txt as input"""
    try:
        # Read prompt from Prompt.txt
        prompt_path = Path("Prompt.txt")
        
        if not prompt_path.exists():
            raise FileNotFoundError("Prompt.txt file not found")
            
        with open(prompt_path, "r", encoding="utf-8") as file:
            prompt_content = file.read()
            
        # Use mock response or real API
        if using_mock:
            response = generate_mock_response(prompt_content)
        else:
            # Call Groq API with system prompt and Prompt.txt content
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": GIFTSNAP_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt_content}
                ],
                model="llama3-70b-8192",  # Default to Llama 3 70B model
            )
            
            # Extract the response
            response = chat_completion.choices[0].message.content
        
        # Save to output.txt if requested
        if save_to_file:
            output_path = Path("output.txt")
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(response)
            print(f"\nAI response saved to: {output_path}\n")
            
        return response
            
    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(error_message)
        if save_to_file:
            with open("output.txt", "w", encoding="utf-8") as file:
                file.write(error_message)
        return error_message


@app.get("/generate")
@app.post("/generate")
async def generate():
    """FastAPI endpoint for generating gift recommendations"""
    try:
        response = generate_gift_recommendation(save_to_file=False)
        return {"response": response}
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Allow script to be run directly or imported
if __name__ == "__main__":
    # If run as a script, generate recommendation and save to file
    generate_gift_recommendation()
    print("Done! Check output.txt for AI recommendations.")
