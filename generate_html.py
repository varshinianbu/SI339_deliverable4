import csv
import os
import re

folder_path = './meets'
meet_links = []  # List to store meet names and links

# Helper function to generate valid filenames
def sanitize_filename(name):
    # Convert to lowercase, replace spaces with underscores, remove invalid characters
    return re.sub(r'[^a-zA-Z0-9_]', '', name.lower().replace(" ", "_")) + '.html'

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        csv_file = os.path.join(folder_path, filename)

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)

            # Extract meet details
            meet_name = data[0][0]
            sanitized_filename = sanitize_filename(meet_name)  # Use sanitized filename
            meet_links.append((meet_name, sanitized_filename))  # Store meet name and link

            # Get the date
            date = data[1][0]
            
            # Initialize HTML content for the meet page (without Team Placement)
            html_content = f'''<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="css/style.css">
                <title>{meet_name} Country Meet</title>
            </head>
            <body>
                <header class="header" id="myHeader">
                    <h1>{meet_name}</h1>
                    <h2>{date}</h2>
                    <a href="meets_overview.html"><button id="Home">Home</button></a>
                </header>
                <main>
                    <section id="meet-results">
                        <h2>Meet Results</h2>
                        <table id="athlete-table">
                            <thead>
                                <tr>
                                    <th>Overall Placement</th>
                                    <th>Image</th>
                                    <th>Name</th>
                                    <th>Details</th>
                                </tr>
                            </thead>
                            <tbody>
            '''

            # Initialize content for Ann Arbor Skyline results (with Team Placement)
            skyline_content = html_content.replace(
                "<h2>Meet Results</h2>",
                "<h2>Ann Arbor Skyline Results</h2>"
            ).replace(
                "<th>Image</th>",
                "<th>Team Placement</th><th>Image</th>"  # Add Team Placement column for Skyline page
            )
            skyline_athletes = []  # List to store HTML rows for Ann Arbor Skyline athletes
            skyline_team_position = 1  # Counter for team placement within Ann Arbor Skyline

            # Start reading from the 7th row (index 6)
            first_row = True
        
            for row in data[6:]:
                if len(row) >= 7:
                    if first_row:
                        first_row = False
                        continue

                    place = row[0].rstrip('.')
                    grade = row[1]
                    name = row[2]
                    athlete_link = row[3]
                    time = row[4]
                    team = row[5]
                    profile_pic = "./AthleteImages/" + row[7]
                    
                    # Check if the profile picture exists or not
                    if not os.path.isfile(profile_pic): 
                        profile_pic = "./AthleteImages/anonymous.jpg"

                    # Build athlete HTML row for the main meet page (without Team Placement)
                    athlete_row = f'''
                    <tr>
                        <td>{place}</td>
                        <td><img src="{profile_pic}" alt="{name}" class="imageform"/></td>
                        <td><a href="{athlete_link}">{name}</a></td>
                        <td>
                            <details>
                                <summary id="ellipsis">...</summary>
                                <div class="sumLabel">Grade:</div> 
                                <div>{grade}</div>
                                <div class="sumLabel">Team:</div>
                                <div>{team}</div>
                                <div class="sumLabel">Time:</div>
                                <div>{time}</div>
                            </details>
                        </td>
                    </tr>
                    '''

                    # Append to main meet content
                    html_content += athlete_row

                    # Append to Ann Arbor Skyline content with team placement if team matches
                    if team == "Ann Arbor Skyline":
                        skyline_athlete_row = f'''
                        <tr>
                            <td>{place}</td>
                            <td>{skyline_team_position}</td>  <!-- Team Placement Column -->
                            <td><img src="{profile_pic}" alt="{name}" class="imageform"/></td>
                            <td><a href="{athlete_link}">{name}</a></td>
                            <td>
                                <details>
                                    <summary id="ellipsis">...</summary>
                                    <div class="sumLabel">Grade:</div> 
                                    <div>{grade}</div>
                                    <div class="sumLabel">Team:</div>
                                    <div>{team}</div>
                                    <div class="sumLabel">Time:</div>
                                    <div>{time}</div>
                                </details>
                            </td>
                        </tr>
                        '''
                        skyline_athletes.append(skyline_athlete_row)
                        skyline_team_position += 1  # Increment team placement for each Skyline athlete

            # Close the table and HTML tags for the main meet page
            html_content += '''
                            </tbody>
                        </table>
                    </section>
                </main>
            </body>
            </html>
            '''

            # Write the individual meet page to a file
            with open(sanitized_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # If there are Ann Arbor Skyline athletes, create a separate page
            if skyline_athletes:
                # Add each Ann Arbor Skyline athlete to the separate HTML content
                skyline_content += ''.join(skyline_athletes) + '''
                            </tbody>
                        </table>
                    </section>
                </main>
            </body>
            </html>
                '''

                # Write the Ann Arbor Skyline results page to a file
                skyline_filename = sanitize_filename(f"{meet_name}_ann_arbor_skyline")
                with open(skyline_filename, 'w', encoding='utf-8') as f:
                    f.write(skyline_content)

# Create a summary HTML page
summary_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="css/style.css">
    <title>Meets Overview</title>
</head>
<body>
    <header>
        <h1>Meets Overview</h1>
    </header>
    <main>
        <section id="meets-list">
            <h2>Available Meets</h2>
            <ul>
'''

# Add each meet to the summary
for meet_name, link in meet_links:
    summary_content += f'                <li><a href="{link}">{meet_name}</a></li>\n'

# Close the HTML tags for the summary page
summary_content += '''
            </ul>
        </section>
    </main>
</body>
</html>
'''

# Write the summary page to a file
with open('meets_overview.html', 'w', encoding='utf-8') as f:
    f.write(summary_content)