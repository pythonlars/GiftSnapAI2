from fastapi import FastAPI, Query, HTTPException
from groq import Groq
import os
from dotenv import load_dotenv
from pathlib import Path
import sys

# Load environment variables from Data_Base/.env
env_path = Path('Data_Base') / '.env'
load_dotenv(dotenv_path=env_path)

# Initialize FastAPI app
app = FastAPI(title="GiftSnapGiftingAI Backend")

# Initialize Groq client with API key from Data_Base/.env
api_key = os.getenv("GIFTSNAP_API_KEY")
if not api_key:
    raise ValueError("Missing GIFTSNAP_API_KEY environment variable in Data_Base/.env")

client = Groq(api_key=api_key)

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

def generate_gift_recommendation(save_to_file=True):
    """Generate a response using Groq API with GiftSnapAI persona using Prompt.txt as input"""
    try:
        # Read prompt from Prompt.txt
        prompt_path = Path("Prompt.txt")
        
        if not prompt_path.exists():
            raise FileNotFoundError("Prompt.txt file not found")
            
        with open(prompt_path, "r", encoding="utf-8") as file:
            prompt_content = file.read()
            
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
