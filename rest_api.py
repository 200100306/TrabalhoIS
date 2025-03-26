from fastapi import FastAPI
import json

app = FastAPI()

# Carregar dados do JSON
DATABASE = "database.json"
def load_data():
    try:
        with open(DATABASE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATABASE, "w") as file:
        json.dump(data, file, indent=4)

@app.get("/items")
def get_items():
    return load_data()

@app.post("/items")
def create_item(item: dict):
    data = load_data()
    item_id = str(len(data) + 1)
    data[item_id] = item
    save_data(data)
    return {"id": item_id, "item": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    data = load_data()
    if item_id in data:
        del data[item_id]
        save_data(data)
        return {"message": "Item deletado"}
    return {"error": "Item não encontrado"}
