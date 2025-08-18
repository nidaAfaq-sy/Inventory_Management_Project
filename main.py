from dotenv import load_dotenv
import os
import random
from agents import Agent, Runner, function_tool,enable_verbose_stdout_logging,InputGuardrailTripwireTriggered,input_guardrail,OpenAIChatCompletionsModel,AsyncOpenAI
import asyncio
import json
from pydantic import BaseModel
from agents import RunContextWrapper, GuardrailFunctionOutput, RunHooks, Tool
from typing import Any

# enable_verbose_stdout_logging()
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

inventory_file = "inventory.json"


class TestHooks(RunHooks):
    async def on_agent_start(self, context: RunContextWrapper, agent: Agent) -> None:
        print(f"Agent {agent.name} started.")

    async def on_agent_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        print(f"Agent {agent.name} ended.")

    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool: Tool) -> None:
        print(f"Tool {tool.name} started.")

    async def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool: Tool, result: str) -> None:
        print(f"Tool {tool.name} ended.")
    
    

start_hooks = TestHooks()

class safety_check(BaseModel):
    is_safe: bool

safety_check_agent = Agent(
    name="Safety Check",
    instructions="critically check if the user talk about politics, set value True in is_safe field. otherwise return False.",
    output_type=safety_check,
    model=model
)


@input_guardrail
async def safety_check_guardrail(ctx: RunContextWrapper, agent: Agent, input: str) -> GuardrailFunctionOutput:
    """Check if the input is safe"""
    result = await Runner.run(safety_check_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= result.final_output.is_safe
    )

@function_tool
def inventory_manager(action: str, name: str = "", quantity: int = 0, id: str = ""):
    try:
        data = json.load(open(inventory_file))
    except FileNotFoundError:
        data = {}

    if action == "add":
        # Always generate a random numeric ID between 1000 and 9999
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

    else:
        return "Invalid action."

    json.dump(data, open(inventory_file, "w"))
    return {"message": "Done", "id": id}

@function_tool
def get_inventory():
    try:
        return json.load(open(inventory_file))
    except FileNotFoundError:
        return {}

agent = Agent(
    name="Inventory Manager",
    instructions="You are an inventory manager. Use the tools to manage inventory.",
    model=model,
    tools=[inventory_manager, get_inventory],
    input_guardrails=[safety_check_guardrail]
)

async def main():
    query = input("Enter your query: ")
    try:
        result = await Runner.run(
            starting_agent=agent,
            input=query,
            hooks=start_hooks
        )
        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("InputGuardrailTripwireTriggered: ", e)

if __name__ == "__main__":
    asyncio.run(main())