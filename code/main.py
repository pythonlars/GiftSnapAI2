
from pathlib import Path
import sys
import os
import subprocess
import time

# Function to get the project root directory
def get_project_root():
    current_file = Path(__file__).resolve()
    # Navigate up from code/ directory to root
    return current_file.parent.parent

# Get the project root path
project_root = get_project_root()
# Change the working directory to the project root
os.chdir(project_root)

def find_gift_receiver(gift_receiver):
    """This function looks for a gift receiver in the gifting_profiles folder.
    If it can't find it, it asks the user to input a different contact.
    Returns a tuple of (gift_receiver, file_path)"""
    file_path = Path('Data_Base') / 'gifting_profile' / f"{gift_receiver}.txt"
    if not file_path.is_file():
        print(f"No profile found for '{gift_receiver}'")
        new_gift_receiver = input("Please try a different contact: ")
        return find_gift_receiver(new_gift_receiver)
    return gift_receiver, file_path

# Get user input
print("=== GiftSnap Gift Suggestion Generator ===")
print("This tool will help you generate personalized gift suggestions.\n")

gift_receiver = input("For who do you want to find a gift: ").strip()
crativ_level = int(input("How creative do you want the gift to be? (1-10): "))
budget = int(input("How much do you want to spend? "))

user_data_path = Path('Data_Base') / 'UserData.txt'

# Get the gift receiver and file path
print("\nLooking for profile...")
found_receiver, gift_profile_path = find_gift_receiver(gift_receiver)
print(f"Found profile for: {found_receiver}\n")

# Read profile data and generate prompt
try:
    # Read gift receiver's profile
    with open(gift_profile_path, 'r', encoding='utf-8') as file:
        gift_profile_data = file.read()
    
    # Read user data
    with open(user_data_path, 'r', encoding='utf-8') as user_file:
        user_data = user_file.read()
    
    # Create the prompt
    print("Generating prompt...")
    with open('Prompt.txt', 'w', encoding='utf-8') as prompt_file:
        prompt_file.write(f"This is my GiftSnap Profile: \n{user_data}\n\n")
        prompt_file.write(f"My budget is: {budget}\n")
        prompt_file.write(f"I need {crativ_level}/10 creative gift ideas for: \n\n")
        prompt_file.write(f"Profile for {found_receiver}:\n")
        prompt_file.write("-" * 30 + "\n")
        prompt_file.write(gift_profile_data)
    
    print("Prompt generated successfully!\n")
    
    # Call main.py to generate the AI response
    print("Generating gift suggestions...")
    print("(This may take a few moments)\n")
    
    # Run main.py (use python or python3 as needed for your system)
    result = subprocess.run(
        [sys.executable, "main.py"],
        capture_output=True,
        text=True,
        check=True
    )
    
    print(result.stdout)
    
    # Check if output.txt was created and display the results
    output_path = Path("output.txt")
    if output_path.exists():
        print("=== Gift Suggestions ===\n")
        with open(output_path, 'r', encoding='utf-8') as output_file:
            suggestions = output_file.read()
            print(suggestions)
        print("\n=== End of Suggestions ===\n")
        print(f"These suggestions have been saved to: {output_path}")
    else:
        print("Could not find output file. Something went wrong with the AI response.")
        
except FileNotFoundError as e:
    print(f"Error: Could not find required file: {e}")
except subprocess.CalledProcessError as e:
    print(f"Error running AI: {e}\n{e.stderr}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print("\nThank you for using GiftSnap! Press Enter to exit.")
input()

