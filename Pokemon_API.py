from fastapi import FastAPI, HTTPException, Query, UploadFile, Form
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import csv
import io

# Initialize FastAPI app
app = FastAPI()

# MySQL connection configuration
db_config = {
    'host': '127.0.0.1:3306',  # Địa chỉ của máy chủ MySQL
    'user': 'root',       # Tên người dùng MySQL
    'password': 'MySQL1234@',  # Mật khẩu MySQL
    'database': 'pokemon',  # Tên cơ sở dữ liệu
}

# Helper function to connect to the database
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Models for request/response
class Pokemon(BaseModel):
    name: str
    type1: str
    type2: Optional[str] = None
    hp: int = 0
    attack: int = 0
    defense: int = 0
    spatk: int = 0
    spdef: int = 0
    speed: int = 0
    generation: int
    legendary: bool

@app.get("/pokemon/first10")
def get_first_10_pokemon():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pokemon LIMIT 10")
    pokemons = cursor.fetchall()
    conn.close()
    return [dict(pokemon) for pokemon in pokemons]

@app.get("/pokemon/page")
def get_paginated_pokemon(page: int = 1, page_size: int = 10):
    offset = (page - 1) * page_size
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pokemon LIMIT ? OFFSET ?", (page_size, offset))
    pokemons = cursor.fetchall()
    conn.close()
    return [dict(pokemon) for pokemon in pokemons]

@app.get("/pokemon/search")
def search_pokemon(
    name: Optional[str] = None,
    type1: Optional[str] = None,
    type2: Optional[str] = None,
    generation: Optional[int] = None,
    legendary: Optional[bool] = None,
    page: int = 1,
    page_size: int = 10
):
    offset = (page - 1) * page_size
    query = "SELECT * FROM pokemon WHERE 1=1"
    params = []

    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")
    if type1:
        query += " AND type1 = ?"
        params.append(type1)
    if type2:
        query += " AND type2 = ?"
        params.append(type2)
    if generation:
        query += " AND generation = ?"
        params.append(generation)
    if legendary is not None:
        query += " AND legendary = ?"
        params.append(legendary)

    query += " LIMIT ? OFFSET ?"
    params.extend([page_size, offset])

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    pokemons = cursor.fetchall()
    conn.close()
    return [dict(pokemon) for pokemon in pokemons]

@app.get("/pokemon/export")
def export_pokemon(
    name: Optional[str] = None,
    type1: Optional[str] = None,
    type2: Optional[str] = None,
    generation: Optional[int] = None,
    legendary: Optional[bool] = None
):
    query = "SELECT * FROM pokemon WHERE 1=1"
    params = []

    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")
    if type1:
        query += " AND type1 = ?"
        params.append(type1)
    if type2:
        query += " AND type2 = ?"
        params.append(type2)
    if generation:
        query += " AND generation = ?"
        params.append(generation)
    if legendary is not None:
        query += " AND legendary = ?"
        params.append(legendary)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    pokemons = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([key for key in pokemons[0].keys()]) if pokemons else None
    for row in pokemons:
        writer.writerow(row)

    output.seek(0)
    return output.getvalue()

@app.post("/pokemon/add")
def add_pokemon(pokemon: Pokemon):
    total = pokemon.hp + pokemon.attack + pokemon.defense + pokemon.spatk + pokemon.spdef + pokemon.speed
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO pokemon (name, type1, type2, total, hp, attack, defense, spatk, spdef, speed, generation, legendary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                pokemon.name, pokemon.type1, pokemon.type2, total,
                pokemon.hp, pokemon.attack, pokemon.defense,
                pokemon.spatk, pokemon.spdef, pokemon.speed,
                pokemon.generation, pokemon.legendary
            )
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.close()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
    finally:
        conn.close()
    return {"message": "Pokemon added successfully"}

@app.put("/pokemon/update/{pokemon_id}")
def update_pokemon(pokemon_id: int, pokemon: Pokemon):
    total = pokemon.hp + pokemon.attack + pokemon.defense + pokemon.spatk + pokemon.spdef + pokemon.speed
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE pokemon SET name = ?, type1 = ?, type2 = ?, total = ?, hp = ?, attack = ?, defense = ?, spatk = ?, spdef = ?, speed = ?, generation = ?, legendary = ? WHERE id = ?",
        (
            pokemon.name, pokemon.type1, pokemon.type2, total,
            pokemon.hp, pokemon.attack, pokemon.defense,
            pokemon.spatk, pokemon.spdef, pokemon.speed,
            pokemon.generation, pokemon.legendary, pokemon_id
        )
    )
    conn.commit()
    conn.close()
    return {"message": "Pokemon updated successfully"}

@app.delete("/pokemon/delete/{pokemon_id}")
def delete_pokemon(pokemon_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pokemon WHERE id = ?", (pokemon_id,))
    conn.commit()
    conn.close()
    return {"message": "Pokemon deleted successfully"}

@app.get("/pokemon/{pokemon_id}")
def get_pokemon_by_id(pokemon_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pokemon WHERE id = ?", (pokemon_id,))
    pokemon = cursor.fetchone()
    conn.close()
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return dict(pokemon)

@app.post("/pokemon/import")
def import_pokemon(file: UploadFile):
    conn = get_db_connection()
    cursor = conn.cursor()
    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    for row in reader:
        try:
            cursor.execute(
                "INSERT INTO pokemon (name, type1, type2, total, hp, attack, defense, spatk, spdef, speed, generation, legendary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    row["Name"],
                    row["Type 1"],
                    row["Type 2"],
                    int(row["Total"]),
                    int(row["HP"]),
                    int(row["Attack"]),
                    int(row["Defense"]),
                    int(row["Sp. Atk"]),
                    int(row["Sp. Def"]),
                    int(row["Speed"]),
                    int(row["Generation"]),
                    row["Legendary"].lower() == "true"
                )
            )
        except sqlite3.IntegrityError as e:
            print(f"Skipping duplicate or invalid entry: {row['Name']} - {e}")

    conn.commit()
    conn.close()
    return {"message": "Pokemon imported successfully"}