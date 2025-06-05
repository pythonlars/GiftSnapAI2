from datetime import datetime
from pathlib import Path

# Get user input
relation_to_gift_receiver = input("What is this person to you (e.g. mom, sister, friend): ").strip()
year_of_birth = int(input("Enter the YEAR of birth of the gift receiver: "))
month_of_birth = int(input("Enter the MONTH of birth of the gift receiver: "))
day_of_birth = int(input("Enter the DAY of birth of the gift receiver: "))
hobbies = input("Enter the HOBBIES of the gift receiver: ").strip()
location = input("Enter the LOCATION of the gift receiver: ").strip()
job = input("Enter the JOB of the gift receiver (Optional): ").strip()
social_media = input("Enter the SOCIAL MEDIA info of the gift receiver (Optional): ").strip()


# Calculate age
current_year = datetime.now().year
age = current_year - year_of_birth

# Format the data
formatted_data = f"""Name: {relation_to_gift_receiver}
Year of birth: {year_of_birth}
Month of birth: {month_of_birth}
Day of birth: {day_of_birth}
Age: {age}
Hobbies: {hobbies}
Location: {location}
Job: {job}
Social Media: {social_media}"""

# Create directory structure
base_dir = Path('Data_Base') / 'gifting_profile'
base_dir.mkdir(parents=True, exist_ok=True)

# Create a safe filename from the profile name
safe_filename = "".join(c if c.isalnum() or c in ' -_' else '_' for c in relation_to_gift_receiver).strip()
file_path = base_dir / f"{safe_filename}.txt"

# Save to file
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(formatted_data)

print(f"\nGift profile has been saved to: {file_path}")
print("\nProfile Details:")
print(formatted_data)