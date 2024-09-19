# Note: This file is hardcoded to scrape data from a singular CSV file (SEC_Jamboree_1_Womens_5000_Meters_Junior_Varsity_24.csv)
# It displays the event title, top 3 team scores and top 3 individual performances in photobook style
# Credit: ChatGPT, UM-GPT, Sample 339 Code

import os

# Path to the CSV file
file_path = 'SEC_Jamboree_1_Womens_5000_Meters_Junior_Varsity_24.csv'

# Reading the file manually as it contains inconsistent formatting
with open(file_path, 'r') as file:
    lines = file.readlines()

# Variables to store team scores and individual results
team_scores = []
individual_results = []

# Flags to detect sections
in_team_scores = False
in_individual_results = False

# Loop through lines to capture the relevant data
for line in lines:
    line = line.strip()

    if line.startswith("Place,Team,Score"):
        in_team_scores = True
        in_individual_results = False
        continue
    elif line.startswith("Place,Grade,Name,Athlete Link,Time,Team,Team Link,Profile Pic"):
        in_team_scores = False
        in_individual_results = True
        continue
    elif not line:  # Ignore empty lines
        continue

    if in_team_scores and len(team_scores) < 3:
        team_scores.append(line.split(','))
    elif in_individual_results and len(individual_results) < 3:
        individual_results.append(line.split(','))

# HTML content to be constructed directly
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Results</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        div.athlete {
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <h1>SEC Jamboree #1 Womens 5000 Meters Junior Varsity</h1>
    <h2>Team Scores</h2>
    <table>
        <thead>
            <tr>
                <th>Place</th>
                <th>Team</th>
                <th>Score</th>
            </tr>
        </thead>
        <tbody>
"""

# Add team scores to the HTML content
for score in team_scores:
    if len(score) >= 3:
        html_content += f"""
            <tr>
                <td>{score[0]}</td>
                <td>{score[1]}</td>
                <td>{score[2]}</td>
            </tr>
        """

# Closing the team scores table tag
html_content += """
        </tbody>
    </table>
    <h2>Top 3 Results</h2>
"""

# Create the HTML content for athletes
for result in individual_results:
    if len(result) >= 7:  # Ensure all required data is present
        html_content += f"""
        <div class="athlete">
            <h3>{result[2]}</h3>
            <p>Place: {result[0]}</p>
            <p>Grade: {result[1]}</p>
            <p>Time: {result[4]}</p>
            <p>Team: {result[5]}</p>
            <img src="{result[6]}" alt="Profile Picture" width="150">
        </div>
        <hr>
        """

# Closing the HTML tags
html_content += """
</body>
</html>
"""

# Save the HTML content to a file
html_file_path = 'results.html'
with open(html_file_path, 'w') as file:
    file.write(html_content)

print(f'HTML file generated: {html_file_path}')