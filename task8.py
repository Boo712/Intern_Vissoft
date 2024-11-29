import csv
import json
import os

csv_file_path = "pokemon.csv"

output_folder = "pokemon_json_files"
os.makedirs(output_folder, exist_ok=True)

try:
    with open(csv_file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        print("Columns in the CSV file:", reader.fieldnames)

        for row in reader:
            pokemon_dict = {
                "id": int(row.get("id", 0)),
                "name": row.get("Name", "Unknown"),
                "type_1": row.get("Type 1", "Unknown"),
                "type_2": row.get("Type 2", "Unknown"),
            }

            json_file_name = f'{pokemon_dict["id"]}_{pokemon_dict["name"]}.json'
            json_file_path = os.path.join(output_folder, json_file_name)

            with open(json_file_path, mode="w", encoding="utf-8") as json_file:
                json.dump(pokemon_dict, json_file, indent=4)

        print(f"JSON files have been created in the folder: {output_folder}")

except FileNotFoundError:
    print(f"The file {csv_file_path} was not found.")
except KeyError as e:
    print(f"Missing expected column in the CSV file: {e}")
except Exception as e:
    print(f"An error occurred: {e}")