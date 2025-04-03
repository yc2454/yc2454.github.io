import geopandas as gpd
import matplotlib.pyplot as plt
import folium
import os

# Load a shapefile of the U.S. states
gdf = gpd.read_file("https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json")

# Ensure state identifiers match full state names
gdf["id"] = gdf["name"]

# Define electoral votes per state
electoral_votes = {
    "Alabama": 9, "Alaska": 3, "Arizona": 11, "Arkansas": 6, "California": 55, "Colorado": 9, "Connecticut": 7,
    "Delaware": 3, "Florida": 29, "Georgia": 16, "Hawaii": 4, "Idaho": 4, "Illinois": 20, "Indiana": 11,
    "Iowa": 6, "Kansas": 6, "Kentucky": 8, "Louisiana": 8, "Maine": 4, "Maryland": 10, "Massachusetts": 11,
    "Michigan": 16, "Minnesota": 10, "Mississippi": 6, "Missouri": 10, "Montana": 3, "Nebraska": 5, "Nevada": 6,
    "New Hampshire": 4, "New Jersey": 14, "New Mexico": 5, "New York": 29, "North Carolina": 15, "North Dakota": 3,
    "Ohio": 18, "Oklahoma": 7, "Oregon": 7, "Pennsylvania": 20, "Rhode Island": 4, "South Carolina": 9,
    "South Dakota": 3, "Tennessee": 11, "Texas": 38, "Utah": 6, "Vermont": 3, "Virginia": 13, "Washington": 12,
    "West Virginia": 5, "Wisconsin": 10, "Wyoming": 3
}

# Define election results
results = {
    "Biden": {
        "states": ["California", "New York", "Illinois", "Washington", "South Carolina", 
                   "Massachusetts", "Michigan", "Minnesota", "Colorado", "North Carolina", 
                   "Oregon", "Virginia", "Nevada", "New Mexico", "Hawaii", 
                   "Connecticut", "Delaware", "Maryland", "New Jersey", "Rhode Island", 
                   "Vermont", "Maine", "Arizona", "Indiana", "Florida", "Pennsylvania", "Wisconsin", 
                   "Texas", "Tennessee", "New Hampshire"],
        "photo": "bluecat.jpg"
    },
    "Trump": {
        "states": ["Ohio", 
                   "Georgia", "Alabama", "Mississippi", 
                   "Kentucky", "Missouri", 
                   "Louisiana", "Arkansas", "Oklahoma", "West Virginia", 
                   "North Dakota", "South Dakota", "Montana", "Wyoming", 
                   "Idaho", "Alaska", "Nebraska", "Iowa", "Utah", "Kansas"],
        "photo": "trump.jpg"
    }
}

photo_urls = {
    "bluecat.jpg": "https://raw.githubusercontent.com/yc2454/yc2454.github.io/main/bluecat.jpg",
    "trump.jpg": "https://raw.githubusercontent.com/yc2454/yc2454.github.io/main/trump.jpg"
}

# Compute total votes for each candidate
biden_votes = sum(electoral_votes[state] for state in results["Biden"]["states"])
trump_votes = sum(electoral_votes[state] for state in results["Trump"]["states"])
total_votes = biden_votes + trump_votes
biden_percentage = (biden_votes / total_votes) * 100
trump_percentage = (trump_votes / total_votes) * 100
needle_position = (270 / 538) * 100

# Assign colors to candidates
colors = {
    "Biden": "blue",
    "Trump": "red",
}

def get_color(state):
    """Returns the color associated with the candidate who won the state."""
    for candidate, data in results.items():
        if state in data["states"]:
            return colors[candidate]
    return "gray"

def get_photo(state):
    """Returns the local photo filename of the candidate who won the state."""
    for candidate, data in results.items():
        if state in data["states"]:
            return data["photo"]
    return "bluecat.jpg"

# Create a map centered on the US
m = folium.Map(location=[37.8, -96], zoom_start=4)

# Add states to the map
gdf["color"] = gdf["id"].apply(get_color)
for _, row in gdf.iterrows():
    state_photo = get_photo(row["id"])
    popup_content = f'<img src="{photo_urls[state_photo]}" width="100px"><br><b>{row["name"]}</b>'
    # print(popup_content)
    
    folium.GeoJson(
        row["geometry"],
        name=row["name"],
        style_function=lambda feature, color=row["color"]: {
            "fillColor": color,
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.6,
        },
        tooltip=folium.Tooltip(row["name"]),
        popup=folium.Popup(popup_content, max_width=200)
    ).add_to(m)

# HTML content for the electoral bar
html_content = f'''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
    
    .election-title {{
        text-align: center;
        margin-bottom: 30px;
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        position: relative;
        padding: 15px 0;
    }}
    
    .election-title h1 {{
        font-size: 36px;
        margin: 0;
        background: linear-gradient(to right, #3b82f6, #ef4444);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        position: relative;
        z-index: 2;
    }}
    
    .election-title::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 150px;
        height: 5px;
        background: linear-gradient(to right, #3b82f6, #ef4444);
        border-radius: 5px;
    }}
    
    .election-title::after {{
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 150px;
        height: 5px;
        background: linear-gradient(to right, #3b82f6, #ef4444);
        border-radius: 5px;
    }}

    .election-container {{
        width: 80%;
        margin: 20px auto;
        position: relative;
    }}

    .candidates-row {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 50px;
    }}

    .vote-bar-container {{
        width: 100%;
        height: 50px;
        position: relative;
        border: 3px solid black;
        display: flex;
        align-items: center;
        font-weight: bold;
        font-size: 20px;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }}

    .biden-bar {{
        width: {biden_percentage}%;
        background: linear-gradient(to right, #1e40af, #3b82f6);
        height: 100%;
        display: flex;
        align-items: center;
        padding-left: 15px;
        color: white;
        justify-content: flex-start;
    }}

    .trump-bar {{
        width: {trump_percentage}%;
        background: linear-gradient(to left, #b91c1c, #ef4444);
        height: 100%;
        display: flex;
        align-items: center;
        padding-right: 15px;
        color: white;
        justify-content: flex-end;
    }}

    .needle {{
        position: absolute;
        left: {needle_position}%;
        top: -5px;
        width: 3px;
        height: 60px;
        background-color: black;
        z-index: 2;
    }}

    .candidate-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        flex: 0 0 auto;
    }}
    
    .candidate-photo {{
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 3px solid white;
        background-color: white;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
    }}
    
    .candidate-info {{
        font-weight: bold;
        font-size: 18px;
    }}
    
    .democrat {{
        color: #3b82f6;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }}
    
    .republican {{
        color: #ef4444;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }}

    /* Stars animation in background */
    .stars {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
    }}

    .star {{
        position: absolute;
        background: white;
        border-radius: 50%;
        animation: twinkle 3s infinite both alternate;
        opacity: 0.5;
    }}

    @keyframes twinkle {{
        0% {{ opacity: 0.2; }}
        100% {{ opacity: 0.7; }}
    }}

    .support-olivia {{
        text-align: center;
        background: linear-gradient(to bottom, #ff0000, #ffffff, #0000ff);
        padding: 20px;
        border: 5px solid gold;
        border-radius: 15px;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.7);
        font-family: "Impact", sans-serif;
        text-transform: uppercase;
        color: white;
        text-shadow: 2px 2px 5px black;
    }}

    .support-olivia h2 {{
        font-size: 28px;
        color: gold;
        text-shadow: 3px 3px 8px black;
    }}

    .support-olivia input {{
        width: 80%;
        padding: 12px;
        margin: 10px;
        border: 3px solid #ffcc00;
        border-radius: 8px;
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        background: white;
        color: black;
    }}

    .support-olivia input:focus {{
        background-color: #ffcc00;
        border-color: red;
        color: black;
    }}

    .support-olivia button {{
        background: #ff0000;
        color: white;
        border: 2px solid gold;
        padding: 12px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 25px;
        cursor: pointer;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        transition: transform 0.2s ease-in-out;
    }}

    .support-olivia button:hover {{
        transform: scale(1.1);
        background: #cc0000;
    }}
</style>

<div class="election-title">
    <div class="stars">
        <span class="star" style="top: 10%; left: 10%; width: 2px; height: 2px; animation-delay: 0.1s;"></span>
        <span class="star" style="top: 20%; left: 25%; width: 3px; height: 3px; animation-delay: 0.5s;"></span>
        <span class="star" style="top: 15%; left: 60%; width: 2px; height: 2px; animation-delay: 1.2s;"></span>
        <span class="star" style="top: 30%; left: 80%; width: 3px; height: 3px; animation-delay: 0.8s;"></span>
        <span class="star" style="top: 25%; left: 45%; width: 2px; height: 2px; animation-delay: 1.5s;"></span>
    </div>
    <h1>2036 Presidential Election</h1>
</div>

<div class="election-container">
    <!-- Separate row for candidates -->
    <div class="candidates-row">
        <!-- Biden container -->
        <div class="candidate-container">
            <img src="{results["Biden"]["photo"]}" class="candidate-photo">
            <div class="candidate-info">
                <div class="democrat">Olivia Fei</div>
                <div class="democrat">Independent</div>
            </div>
        </div>
        
        <!-- Trump container -->
        <div class="candidate-container">
            <img src="{results["Trump"]["photo"]}" class="candidate-photo">
            <div class="candidate-info">
                <div class="republican">Donald Trump</div>
                <div class="republican">Republican</div>
            </div>
        </div>
    </div>
    
    <!-- Separate bar container -->
    <div class="vote-bar-container">
        <div class="biden-bar">{biden_votes}</div>
        <div class="trump-bar">{trump_votes}</div>
        <div class="needle"></div>
    </div>
</div>

<div class="support-olivia">
    <h2>Support Olivia to Make America Great!</h2>
    <p>Your generous contribution will help Olivia on her quest!</p>
    
    <label for="galactic-credit">Enter your Credit Card Number:</label>
    <input type="text" id="galactic-credit">
    
    <label for="social-security">Provide your Social Security Number:</label>
    <input type="text" id="social-security" placeholder="###-##-####">

    <br></br>
    
    <label for="monopoly-money">Pledge Your Support with Money:</label>
    <input type="number" id="monopoly-money">
    
    <button onclick="alert('Thank you for your support!')">Donate Funds</button>
</div>

'''


# Save the map to an HTML file
with open("election_map.html", "w") as f:
    f.write(html_content)
    f.write(m._repr_html_())

print("Election map with vote bar and candidate photos saved as election_map.html")