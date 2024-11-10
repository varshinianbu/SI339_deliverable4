import csv
import os
import re

folder_path = './meets'
meet_links = []  # List to store meet names and links
skyline_comments = []  # List to store comments about Ann Arbor Skyline

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
                    <a href="{sanitize_filename(meet_name)}"><button class="active">Meet Results</button></a>
                    <a href="{sanitize_filename(meet_name + '_ann_arbor_skyline')}"><button>Skyline Results</button></a>
                    <a href="{sanitize_filename(meet_name + '_team_placements')}"><button id = "sky-r">Team Placements</button></a>
                    <a href="{sanitize_filename(meet_name + '_skyline_gallery')}"><button>Skyline Gallery</button></a>
                </header>
                <main>
                    <section id="meet-results">
                        <h2>Meet Results</h2>
                        <section id="search">
                            <label for="searchInput" id="searchLabel">Search Athletes:</label>
                            <input type="text" id="searchInput" placeholder="Search by name...">
                        </section>
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

            # Extract team placement information starting from row 7 (index 6)
            team_placement_content = f'''<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="css/style.css">
                <title>{meet_name} Team Placements</title>
            </head>
            <body>
                <header class="header" id="myHeader">
                    <h1>{meet_name}</h1>
                    <h2>{date}</h2>
                    <a href="meets_overview.html"><button id="Home">Home</button></a>
                    <a href="{sanitize_filename(meet_name)}"><button>Meet Results</button></a>
                    <a href="{sanitize_filename(meet_name + '_ann_arbor_skyline')}"><button>Skyline Results</button></a>
                    <a href="{sanitize_filename(meet_name + '_team_placements')}"><button id = "sky-r" class="active">Team Placements</button></a>
                    <a href="{sanitize_filename(meet_name + '_skyline_gallery')}"><button>Skyline Gallery</button></a>
                </header>
                <main>
                    <section id="meet-results" class="meet-results">
                        <h2>Team Placement Results</h2>
                        <table id="athlete-table">
                            <thead>
                                <tr>
                                    <th>Place</th>
                                    <th>Team</th>
                                    <th>Score</th>
                                </tr>
                            </thead>
                            <tbody>
            '''

            # Start reading from row 7 (index 6)
            first_row = True
            for row in data[6:]:
                if len(row) < 3:
                    continue
                
                if len(row) >= 3 and row[0] == "Place" and row[1] == "Grade" and row[2] == "Name":
                    break  

                # Skip the header row for team placements
                if first_row:
                    first_row = False
                    continue
                
                if len(row) >= 3:
                    place = row[0].rstrip('.')
                    team = row[1]
                    score = row[2]
                    
                    team_row = f'''
                    <tr>
                        <td>{place}</td>
                        <td>{team}</td>
                        <td>{score}</td>
                    </tr>
                    '''
                    team_placement_content += team_row

            team_placement_content += '''
                            </tbody>
                        </table>
                    </section>
                </main>
            </body>
            </html>
            '''

            # Write the team placement page to a file
            team_placement_filename = sanitize_filename(f"{meet_name}_team_placements")
            with open(team_placement_filename, 'w', encoding='utf-8') as f:
                f.write(team_placement_content)

            skyline_content = html_content.replace(
                "<h2>Meet Results</h2>",
                "<h2>Ann Arbor Skyline Results</h2>"
            ).replace(
                "<th>Image</th>",
                "<th>Skyline Indivdual Placement</th><th>Image</th>"
            ).replace(
                '<button>Skyline Results</button></a>',
                '<button class="active">Skyline Results</button></a>'
            ).replace(
                '<button class="active">Meet Results</button></a>',
                '<button>Meet Results</button></a>'
            ).replace(
                '<table id="athlete-table">',
                '<table id="athlete-table" class="skyline-table">'
            )

            comments_row = data[3]
            comments = " ".join([comment for comment in comments_row if comment.strip()])
            skyline_comments.append((meet_name, comments))

            skyline_content += f'''
                    <section id="skyline-comments">
                        <p id=sky-r>{comments}</p>
                    </section>
            '''

            skyline_athletes = []  
            skyline_team_position = 1  

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
                    
                    if not os.path.isfile(profile_pic): 
                        profile_pic = "./AthleteImages/anonymous.jpg"

                    athlete_row = f'''
                    <tr>
                        <td>{place}</td>
                        <td><img src="{profile_pic}" alt="{name}" class="imageform"/></td>
                        <td><a href="{athlete_link}">{name}</a></td>
                        <td>
                            <details>
                                <summary id="ellipsis">...</summary>
                                <div>Grade:</div> 
                                <div class="sumLabel">{grade}</div>
                                <div>Team:</div>
                                <div class="sumLabel">{team}</div>
                                <div>Time:</div>
                                <div class="sumLabel">{time}</div>
                            </details>
                        </td>
                    </tr>
                    '''

                    html_content += athlete_row

                    if team == "Ann Arbor Skyline":
                        skyline_athlete_row = f'''
                        <tr>
                            <td>{place}</td>
                            <td>{skyline_team_position}</td>
                            <td><img src="{profile_pic}" alt="{name}" class="imageform"/></td>
                            <td><a href="{athlete_link}">{name}</a></td>
                            <td>
                                <details>
                                    <summary id="ellipsis">...</summary>
                                    <div>Grade:</div> 
                                    <div class="sumLabel">{grade}</div>
                                    <div>Team:</div>
                                    <div class="sumLabel">{team}</div>
                                </details>
                            </td>
                        </tr>
                        '''
                        skyline_athletes.append(skyline_athlete_row)
                        skyline_team_position += 1

            html_content += '''
                            </tbody>
                        </table>
                    </section>
                </main>
                <script src="search.js"></script>
            </body>
            </html>
            '''

            with open(sanitized_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)

            if skyline_athletes:
                skyline_content += ''.join(skyline_athletes) + '''
                            </tbody>
                        </table>
                    </section>
                </main>
                <script src="skyline_search.js"></script>
            </body>
            </html>
                '''

                skyline_filename = sanitize_filename(f"{meet_name}_ann_arbor_skyline")
                with open(skyline_filename, 'w', encoding='utf-8') as f:
                    f.write(skyline_content)

            # Create a page with only Skyline student images for CSS grid styling
            skyline_images_content = f'''<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link href="dist/css/lightbox.css" rel="stylesheet" />
                <link rel="stylesheet" href="css/style.css">
                <title>{meet_name} Skyline Student Gallery</title>
            </head>
            <body>
                <header class="header" id="myHeader">
                    <h1>{meet_name}</h1>
                    <h2>{date}</h2>
                    <a href="meets_overview.html"><button id="Home">Home</button></a>
                    <a href="{sanitize_filename(meet_name)}"><button>Meet Results</button></a>
                    <a href="{sanitize_filename(meet_name + '_ann_arbor_skyline')}"><button>Skyline Results</button></a>
                    <a href="{sanitize_filename(meet_name + '_team_placements')}"><button id = "sky-r">Team Placements</button></a>
                    <a href="{sanitize_filename(meet_name + '_skyline_gallery')}"><button class="active">Skyline Gallery</button></a>
                </header>
                <main>
                    <section id="skyline-gallery" class="gallery">
            '''

            # Add images of each Skyline student
            for row in data[6:]:
                if len(row) >= 7 and row[5] == "Ann Arbor Skyline":
                    profile_pic = "./AthleteImages/" + row[7]
                    
                    # Skip if the image is anonymous.jpg
                    if not os.path.isfile(profile_pic) or "anonymous.jpg" in profile_pic: 
                        continue
                    
                    skyline_images_content += f'''
                        <div class="gallery-item">
                            <a href="{profile_pic}" data-lightbox="skyline-gallery" data-title="{row[2]}" data-alt="{row[2]}">
                                <img src="{profile_pic}" alt="{row[2]}" class="gallery-image">
                            </a>
                        </div>
                    '''

            skyline_images_content += '''
                    </section>
                </main>
                <script src="dist/js/lightbox-plus-jquery.js"></script>
            </body>
            </html>
            '''

            # Write the Skyline student gallery page to a file
            skyline_gallery_filename = sanitize_filename(f"{meet_name}_skyline_gallery")
            with open(skyline_gallery_filename, 'w', encoding='utf-8') as f:
                f.write(skyline_images_content)

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
            <h2>All Meets</h2>
            <ul>
'''

# Add links to all meets
for meet_name, sanitized_filename in meet_links:
    summary_content += f'<li><a href="{sanitized_filename}">{meet_name}</a></li>\n'

with open('meets_overview.html', 'w', encoding='utf-8') as f:
    f.write(summary_content)