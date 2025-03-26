from flask import Flask, request
from flask_soap import Soap
import json

app = Flask(__name__)
soap = Soap(app)

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

@soap.method("getItems")
def get_items():
    return load_data()

@soap.method("createItem")
def create_item(item):
    data = load_data()
    item_id = str(len(data) + 1)
    data[item_id] = item
    save_data(data)
    return {"id": item_id, "item": item}

@soap.method("deleteItem")
def delete_item(item_id):
    data = load_data()
    if item_id in data:
        del data[item_id]
        save_data(data)
        return {"message": "Item deletado"}
    return {"error": "Item não encontrado"}

if __name__ == "__main__":
    app.run(port=5001)
