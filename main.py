from dotenv import load_dotenv
import os
import random
import asyncio
import json
import google.generativeai as genai
import sys

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

gemini_model = "gemini-2.0-flash"
inventory_file = "inventory.json"

def inventory_manager(action: str, name: str = "", quantity: int = 0, id: str = ""):
    try:
        data = json.load(open(inventory_file))
    except FileNotFoundError:
        data = {}

    if action == "add":
        id = str(random.randint(1000, 9999))
        data[id] = {"name": name, "quantity": quantity}
    elif action == "update":
        if id in data:
            data[id] = {"name": name, "quantity": quantity}
        else:
            return "Item not found."
    elif action == "delete":
        if id in data:
            del data[id]
        else:
            return "Item not found."
    elif action == "get":
        return data
    else:
        return "Invalid action."

    json.dump(data, open(inventory_file, "w"))
    return {"message": "Done", "id": id}

def get_inventory():
    try:
        return json.load(open(inventory_file))
    except FileNotFoundError:
        return {}

async def run_gemini(prompt: str):
    model = genai.GenerativeModel(gemini_model)
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m inventory_project <command> [options]")
        print("Commands: add <name> <quantity>, update <id> <name> <quantity>, delete <id>, get, gemini <prompt>")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "add" and len(sys.argv) == 4:
        name = sys.argv[2]
        quantity = int(sys.argv[3])
        result = inventory_manager("add", name=name, quantity=quantity)
        print(result)
    elif cmd == "update" and len(sys.argv) == 5:
        item_id = sys.argv[2]
        name = sys.argv[3]
        quantity = int(sys.argv[4])
        result = inventory_manager("update", name=name, quantity=quantity, id=item_id)
        print(result)
    elif cmd == "delete" and len(sys.argv) == 3:
        item_id = sys.argv[2]
        result = inventory_manager("delete", id=item_id)
        print(result)
    elif cmd == "get":
        print(get_inventory())
    elif cmd == "gemini" and len(sys.argv) >= 3:
        prompt = " ".join(sys.argv[2:])
        output = asyncio.run(run_gemini(prompt))
        print("Gemini Output:", output)
    else:
        print("Invalid command or wrong arguments.")
