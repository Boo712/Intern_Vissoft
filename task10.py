import csv

csv_file_path = "pokemon.csv"

def export_similar_pokemon():
    query = input("Enter a search term: ").strip().lower()
    output_file = "similar_pokemon.csv"
    
    try:
        with open(csv_file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            matched_pokemon = [
                row for row in reader if query in row["Name"].lower()
            ]
        
        if matched_pokemon:
            with open(output_file, mode="w", encoding="utf-8", newline="") as output:
                writer = csv.DictWriter(output, fieldnames=matched_pokemon[0].keys())
                writer.writeheader()
                writer.writerows(matched_pokemon)
            print(f"Exported {len(matched_pokemon)} Pokemon to {output_file}")
        else:
            print("No Pokemon found with similar names.")
    
    except FileNotFoundError:
        print(f"The file {csv_file_path} was not found.")

if __name__ == "__main__":
    export_similar_pokemon()