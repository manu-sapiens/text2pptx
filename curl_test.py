import json
import requests

PORT = "8501"

# read md from ./temp/markdown.md

# check file exists
md_filename = "./temp/markdown.md"
try:
    with open(md_filename, 'r') as f:
        md = f.read()
except FileNotFoundError:
    print(f"File {md_filename} not found")
    exit(1)
#

md234 = """ 
# Dungeons & Dragons
An introduction to the world of role-playing games

## What is Dungeons & Dragons?
░░░░░░░░░░░░░░░░░░░░░░░░░

### Key Points
*Dungeons and Dragons is a fantasy tabletop role-playing game.
**Players create characters and embark on adventures in a fantasy world filled with magic and monsters.
**The game is guided by a Dungeon Master who narrates the story and controls the non-player characters.
**Players use dice rolls to determine the outcomes of their actions, adding an element of chance to the game.

# Dungeons & Dragons Adventurers League
Contribution to Reviving Interest

## What is Dungeons & Dragons Adventurers League?
An organized play program for 5th Edition D&D

### Key Features of Adventurers & League
*Structured play with consistent rules
*Accessible to all players globally
*Uses official D&D content and adventures

#### How it Renewed Interest
*Fostered community among players
*Encouraged in-person and online play

#### Impact & the Game
* Revitalized player engagement 
* & boosted sales

#### & Other important things
* like brushing your teeth!
"""

md334 = """
# Dungeons and Dragons
An overview of the popular tabletop role-playing game

## History of Dungeons and Dragons
Tracing the development and evolution of the game

### Key Components of D&D
*Role-playing
*Character Creation
*Storytelling
*Combat Mechanics

#### Gameplay Mechanics
*Dice Rolling
*Rules and Guidelines
*Game Master Role
*Skills and Abilities

# Dungeons And Dragons Adventurers League
Contribution to the Renewal of Interest

## History of Dungeons And Dragons Adventurers League
An Overview

### Key Features of D&D Adventurers League
*Organized play events at game stores and conventions
*Structured campaign with official adventures
*Accessible for new and experienced players

### Impact on Dungeons And Dragons Community
*Increased participation and engagement
*Fostered a sense of community among players
*Promoted inclusivity and diversity in gaming

#### Conclusion
*Revitalized interest in the game
*Provided opportunities for social interaction through gaming
"""

md44 = """
# Dungeons & Dragons
A Brief Overview

## And D🫰D
"""

md_bad = """ 
# Dungeons & Dragons
A Brief Overview

### What is Dungeons and Dragons?
*Dungeons and Dragons (D&D) is a fantasy tabletop role-playing game (RPG)
*It was first published in 1974 by Gary Gygax and Dave Arneson
*Players create characters and embark on adventures in a fantasy world filled with magic, monsters, and quests

## Gameplay Elements
░░░░░░░░░░░░░░░░░░░░░░░░░

### Character Creation
*Players create unique characters with different races, classes, and abilities
*Characters progress through levels, gaining new skills and powers

### Adventure and Quests
*Game Master (GM) creates a story and guides players through adventures
*Players work together to solve puzzles, defeat enemies, and complete quests

### Combat and Role-Playing
*Combat is resolved through dice rolls and strategic decisions
*Role-playing allows players to interact with NPCs, make choices, and shape the story

## Benefits of Playing D&D
"""
 
md2 = """
# Dungeons and Dragons
A Brief Overview

### What is Dungeons and Dragons?
*Dungeons and Dragons (D&D) is a fantasy tabletop role-playing game (RPG)
*It was first published in 1974 by Gary Gygax and Dave Arneson
*Players create characters and embark on adventures in a fantasy world filled with magic, monsters, and quests

## Gameplay Elements
░░░░░░░░░░░░░░░░░░░░░░░░░

### Character Creation
*Players create unique characters with different races, classes, and abilities
*Characters progress through levels, gaining new skills and powers

### Adventure and Quests
*Game Master (GM) creates a story and guides players through adventures
*Players work together to solve puzzles, defeat enemies, and complete quests

### Combat and Role-Playing
*Combat is resolved through dice rolls and strategic decisions
*Role-playing allows players to interact with NPCs, make choices, and shape the story

## Benefits of Playing D&D
░░░░░░░░░░░░░░░░░░░░░░░░░

### ░░░░░░░░░░░░░░░░░░░░░░░░░

#### Creativity and Imagination
*Players develop storytelling skills and creative thinking
*Imagining different scenarios and outcomes enhances problem-solving abilities

#### Social Skills and Teamwork
*Collaboration with other players fosters teamwork and communication
*Negotiation and conflict resolution are key in group dynamics

#### Critical Thinking and Decision-Making
*Players must make decisions based on their character's abilities and the situation
*Analyzing risks and rewards helps develop strategic thinking

# Dungeons And Dragons Adventurers League
Contributions to Renewal of Interest in the Game

## Overview of Dungeons And Dragons Adventurers League
░░░░░░░░░░░░░░░░░░░░░░░░░

### Unique features of Adventurers League
*Structured play with organized events
*Inclusive environment for all skill levels
*Shared world experience with interconnected adventures

### Impact on Dungeons And Dragons Community
*Increased accessibility for new players
*Promotion of local game stores through event hosting
*Encouragement of creativity and social interaction

### BLANK

#### Renewal of Interest in the Game
*Revitalization of tabletop gaming culture
*Expanding player base and diverse representation
*Rekindling nostalgia and fostering community bonds

"""

md_good = """
# Dungeons And Dragons
An Introduction

## What is Dungeons And Dragons?
░░░░░░░░░░░░░░░░░░░░░░░░░

### Key Aspects of Dungeons And Dragons
*Role-playing game involving storytelling, decision-making, and dice rolling
*Set in a fantasy world filled with magic, monsters, and heroes
*Players create characters and embark on adventures guided by a Dungeon Master

### Game Mechanics
*Uses polyhedral dice for resolving actions and determining outcomes
*Character attributes include strength, dexterity, wisdom, and charisma
*Players progress through levels, gaining skills and abilities

### Community and Culture
*Extensive fan base with conventions, online forums, and streamed games
*Encourages creativity, teamwork, problem-solving, and storytelling
*Inclusive environment welcoming players from diverse backgrounds

# Dungeons And Dragons Adventurers League
Renewing Interest in the Game

## Overview of Dungeons And Dragons Adventurers League
░░░░░░░░░░░░░░░░░░░░░░░░░

### Key Features of Adventurers League
*Structured play events held in game stores, conventions, and online
*Official campaigns and adventures created by Wizards of the Coast
*Utilizes standardized rules and guidelines for character creation and progression

#### Community Engagement
*Encourages collaboration and team play
*Fosters a welcoming and inclusive environment for all players

## Impact on Dungeons And Dragons Community
░░░░░░░░░░░░░░░░░░░░░░░░░

### Contributions to Renewal of Interest
*Increased accessibility to organized play for new and veteran players
*Promoted social interactions and networking among players
*Led to the growth of local gaming communities and events


"""

data = {
    "filename": 'dnd3.pptx',
    "markdown": md,
    "template": "md_Bespoke.pptx",
    "options": {"sectionsExpand":"yes"}
}

url = f'http://localhost:{PORT}/pptx/from_md'
print("requesting to ", url)

headers = {'Content-Type': 'application/json'}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Get the presentation name from the response headers
    presentation_name = response.headers.get('Content-Disposition',"default.pptx").split("filename=")[-1].strip('"' + "'")
    print(f"Presentation name: {presentation_name}")
    
    # Save the response content to a file
    output_path = './test/'+presentation_name
    with open(output_path, 'wb') as f:
        f.write(response.content)
    print(f"Presentation saved to {output_path}")

except requests.exceptions.RequestException as e:
    print(f"Error during request: {e}")
#
#

#curl -X POST http://localhost:8501/generate_presentation -H 'Content-Type: application/json' -d '{"template":"Urban_monochrome","filename":"dnd.pptx","title":"Dungeons & Dragons: A Billion-Dollar Franchise","subtitle":"Uncovering the Commercial Success of D&D", "slides":[{"heading":"Dungeons & Dragons: A Billion-Dollar Franchise","bullet_points":["Revenue: $822 million (2021)","Market Share: 75% of tabletop RPG market","Community: 50 million+ players worldwide","Partnerships: Netflix, Amazon, Paramount Pictures, and more","Cultural Impact: Featured in The New York Times, Forbes, NPR, and more"]}]}' -o ./test/output.pptx
#curl -X POST http://localhost:8501/ -H 'Content-Type: application/json' -d json_string -o ./test/output.pptx