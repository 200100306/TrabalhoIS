import json
import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI

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

@strawberry.type
class Item:
    id: str
    name: str
    description: str

@strawberry.type
class Query:
    @strawberry.field
    def get_items(self) -> list[Item]:
        data = load_data()
        return [Item(id=k, **v) for k, v in data.items()]

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_item(self, name: str, description: str) -> Item:
        data = load_data()
        item_id = str(len(data) + 1)
        new_item = {"name": name, "description": description}
        data[item_id] = new_item
        save_data(data)
        return Item(id=item_id, **new_item)

    @strawberry.mutation
    def delete_item(self, id: str) -> str:
        data = load_data()
        if id in data:
            del data[id]
            save_data(data)
            return "Item deletado com sucesso"
        return "Item não encontrado"

schema = strawberry.Schema(query=Query, mutation=Mutation)
app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)
