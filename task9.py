import json
import os

json_folder = "pokemon_json_files"

def search_pokemon():
    query = input("Enter Pokemon ID or Name: ").strip()
    
    for file_name in os.listdir(json_folder):
        if file_name.endswith(".json"):
            base_name = os.path.splitext(file_name)[0]
            pokemon_id, pokemon_name = base_name.split("_", 1)
            
            if query == pokemon_id or query.lower() == pokemon_name.lower():
                json_file_path = os.path.join(json_folder, file_name)

                with open(json_file_path, "r", encoding="utf-8") as file:
                    pokemon_data = json.load(file)
                    print(json.dumps(pokemon_data, indent=4))
                return
    
    print("No Pokemon found with the given ID or Name.")

if __name__ == "__main__":
    search_pokemon()