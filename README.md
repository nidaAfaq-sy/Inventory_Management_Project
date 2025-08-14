# Inventory Manager with Gemini Integration

A simple command-line tool to manage a small inventory stored in a JSON file, with an option to query Google's **Gemini** model for AI-generated responses.

## Features
- **Add, update, delete, and view** inventory items
- Inventory stored locally in `inventory.json`
- **Unique item IDs** generated automatically
- Integration with **Google Gemini API** for AI-powered prompts

---

## Requirements

- Python 3.8+
- Google Generative AI Python SDK
- `.env` file with your Gemini API key

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/inventory_project.git
   cd inventory_project
Create and activate a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
source venv/bin/activate    # On macOS/Linux
venv\Scripts\activate       # On Windows
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Set up environment variables:
Create a .env file in the root directory:

env
Copy
Edit
GEMINI_API_KEY=your_google_gemini_api_key_here
Usage
Run the script using:

bash
Copy
Edit
python -m inventory_project <command> [options]
Commands
Command	Description
add <name> <quantity>	Add a new item to inventory
update <id> <name> <quantity>	Update an existing item
delete <id>	Remove an item from inventory
get	View all inventory items
gemini <prompt>	Send a prompt to Gemini AI and print the response

Examples
Add an item:

bash
Copy
Edit
python -m inventory_project add "Apples" 50
Update an item:

bash
Copy
Edit
python -m inventory_project update 1234 "Green Apples" 60
Delete an item:

bash
Copy
Edit
python -m inventory_project delete 1234
Get all inventory:

bash
Copy
Edit
python -m inventory_project get
Ask Gemini AI:

bash
Copy
Edit
python -m inventory_project gemini "Give me a short poem about apples"
File Structure
bash
Copy
Edit
inventory_project/
│
├── inventory.json       # Stores inventory data
├── inventory.py         # Main script
├── requirements.txt     # Dependencies
├── .env                 # Environment variables
└── README.md            # This file
