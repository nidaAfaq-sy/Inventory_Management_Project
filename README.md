🗂️ Inventory Manager Agent
📌 Description

Ye project ek AI-powered Inventory Management System hai jo agents framework aur Google Gemini API ka use karke bana hai.
Isme guardrails aur tools implement kiye gaye hain jisse:

Inventory items add/update/delete kiye ja sakte hain

Complete inventory fetch kiya ja sakta hai

Input guardrail ensure karta hai ke unsafe queries (jaise politics related) filter ho jayein

🚀 Features

✅ Add, update aur delete inventory items

✅ Get complete inventory in JSON format

✅ Safety guardrails (politics input detection)

✅ Custom hooks for logging agent aur tools execution

🛠️ Installation

Clone repository

git clone https://github.com/username/inventory-manager-agent.git
cd inventory-manager-agent


Create & activate virtual environment

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows


Install dependencies

pip install -r requirements.txt


.env file banaiye aur apna Gemini API key add kijiye:

GEMINI_API_KEY=your_api_key_here

▶️ Usage

Run the program:

python main.py


Aapko prompt milega:

Enter your query: add item


Example queries:

"Add a new item with name 'Laptop' and quantity 10"

"Update item with id 1234 to quantity 20"

"Delete item with id 5678"

"Show me the inventory"

📂 Folder Structure
inventory-manager-agent/
│-- main.py
│-- inventory.json
│-- .env
│-- requirements.txt
│-- README.md
