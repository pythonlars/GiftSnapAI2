from datetime import datetime
from pathlib import Path

# Collect user data
Name = input("Enter your name: ")
Year_of_Birth = int(input("Enter your year of birth: "))
Month_of_Birth = int(input("Enter your month of birth: "))
Day_of_Birth = int(input("Enter your day of birth: "))
Hobbies = input("Enter your hobbies: ")
Location = input("Enter your location: ")

# Calculate age
current_year = datetime.now().year
Age = current_year - Year_of_Birth

# Format the data
formatted_data = f"""Name: {Name}
Year of birth: {Year_of_Birth}
Month of birth: {Month_of_Birth}
Day of birth: {Day_of_Birth}
Hobbies: {Hobbies}
Location: {Location}
Age: {Age}"""

# Create Data_Base directory if it doesn't exist
data_dir = Path('Data_Base')
data_dir.mkdir(exist_ok=True)

# Save to file in Data_Base folder
file_path = data_dir / 'UserData.txt'
with open(file_path, 'w') as file:
    file.write(formatted_data)

print(f"\nYour information has been saved to {file_path}")

