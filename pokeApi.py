import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from random import randint
import vlc
import os
from threading import Thread
os.environ['SDL_AUDIODRIVER'] = 'pulseaudio'


# Function to fetch Pokémon data
def fetch_pokemon_data(pokemon_id):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data from the PokeAPI.")
        return None
    
def play_cry(url):
    def run():
        player = vlc.MediaPlayer(url)
        player.play()
    Thread(target=run).start()

def search_pokemon(event=None):
    search_query = search_entry.get().lower() 
    if search_query:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{search_query}")
        if response.status_code == 200:
            data = response.json()
            update_gui(data['id'])  # Update the GUI with the new Pokémon data
        else:
            print("Pokémon not found.")

# Function to update the GUI with Pokémon data
def update_gui(pokemon_id):
    data = fetch_pokemon_data(pokemon_id)
    if data:
        # Update image
        image_url = data['sprites']['front_default']
        image_response = requests.get(image_url)
        image_data = Image.open(BytesIO(image_response.content))
        photo = ImageTk.PhotoImage(image_data)
        image_label.config(image=photo)
        image_label.image = photo 


        name_label.config(text=f"Name: {data['name'].title()}")
        number_label.config(text=f"Number: {data['id']}")
        ability_label.config(text=f"Abilities: {', '.join(ability['ability']['name'].title() for ability in data['abilities'])}")

        cry = data["cries"]["latest"]
        play_cry(cry)


# Main window
root = tk.Tk()
root.title("Pokéfinder")

search_frame = tk.Frame(root)
search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT)
search_label= tk.Label(root, text="Please Enter a Pokémon Name or National Dex ID to search")
search_label.pack()
search_button = tk.Button(search_frame, text="Search", command=search_pokemon)
search_button.pack(side=tk.RIGHT)
search_frame.pack()

root.bind('<Return>', search_pokemon)

# Labels for displaying the Pokémon image and information
image_label = tk.Label(root)
image_label.pack()

name_label = tk.Label(root, text="")
name_label.pack()

number_label = tk.Label(root, text="")
number_label.pack()

ability_label = tk.Label(root, text="")
ability_label.pack()

# Button to fetch a random Pokémon
fetch_button = tk.Button(root, text="Fetch Random Pokémon", command=lambda: update_gui(randint(1, 251)))
fetch_button.pack()

root.mainloop()
