import os
from typing import Dict, Any
from dotenv import load_dotenv
from pydantic import BaseModel
from crewai import Agent, Task, Crew
from crewai import LLM
from crewai.tools import tool
from crewai.flow.flow import Flow, start, listen
from stagehand_tool import browser_automation


load_dotenv()

# Define our LLMs for providing to agents using environment variables
planner_model = os.getenv("PLANNER_MODEL", "ollama/gpt-oss")
automation_model = os.getenv("AUTOMATION_MODEL", "openai/gpt-4o")
response_model = os.getenv("RESPONSE_MODEL", "ollama/gpt-oss")

planner_llm = LLM(model=planner_model)
automation_llm = LLM(model=automation_model)
response_llm = LLM(model=response_model)


@tool("B2A Execution Tool")
def b2a_execution_tool(task_description: str, website_url: str) -> str:
    """
    A B2A tool that allows an agent to interact with legacy web interfaces.
    It translates high-level intent into deterministic browser actions using Stagehand.

    Args:
        task_description (str): The specific action or extraction to perform.
        website_url (str): The URL of the target business interface.

    Returns:
        str: Schema-aligned result of the B2A execution.
    """
    return browser_automation(task_description, website_url)


class B2AEngineFlowState(BaseModel):
    query: str = ""
    result: str = ""


class B2AExecutionPlan(BaseModel):
    task_description: str
    website_url: str


class B2AEngineFlow(Flow[B2AEngineFlowState]):
    """
    B2A Engine: A translation layer that turns legacy web workflows into 
    deterministic, agent-executable tools.
    """

    @start()
    def start_engine(self) -> Dict[str, Any]:
        print(f"B2A Engine started with intent: {self.state.query}")
        return {"query": self.state.query}

    @listen(start_engine)
    def generate_schema_plan(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        print("--- B2A Schema Planner: Interpreting intent into execution schema ---")

        planner_agent = Agent(
            role="B2A Schema Planner",
            goal="Translate human natural language into a structured B2A execution plan.",
            backstory="You are an expert at mapping ambiguous user requests to specific web-based business workflows and schemas.",
            llm=planner_llm,
        )

        plan_task = Task(
            description=f"Analyze the following user query and generate a structured B2A execution plan (URL and task): '{inputs['query']}'.",
            agent=planner_agent,
            output_pydantic=B2AExecutionPlan,
            expected_output=(
                "A structured JSON plan matching the B2AExecutionPlan schema."
            ),
        )

        crew = Crew(agents=[planner_agent], tasks=[plan_task], verbose=True)
        result = crew.kickoff()

        # Fallback to ensure target availability
        website_url = result.pydantic.website_url
        if not website_url or website_url.lower() in ["", "none", "null", "n/a"]:
            website_url = "https://www.google.com"

        return {
            "task_description": result.pydantic.task_description,
            "website_url": website_url,
        }

    @listen(generate_schema_plan)
    def execute_b2a_workflow(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        print("--- B2A Execution Agent: Running autonomous browser machinery ---")

        execution_agent = Agent(
            role="B2A Execution Agent",
            goal="Execute the planned business workflow using the B2A Execution Tool.",
            backstory="You specialize in autonomous navigation and deterministic data extraction from complex web environments.",
            tools=[b2a_execution_tool],
            llm=automation_llm,
        )

        execution_task = Task(
            description=(
                f"Execute the B2A workflow for:\n"
                f"Target: {inputs['website_url']}\n"
                f"Schema Objective: {inputs['task_description']}\n\n"
                f"Use the B2A Execution Tool to interface with the web autonomously."
            ),
            agent=execution_agent,
            expected_output="Deterministic output from the web-to-agent translation layer.",
            markdown=True,
        )

        crew = Crew(agents=[execution_agent], tasks=[execution_task], verbose=True)
        result = crew.kickoff()
        return {"result": str(result)}

    @listen(execute_b2a_workflow)
    def synthesize_agent_response(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        print("--- B2A Data Synthesizer: Finalizing token-efficient response ---")

        synthesis_agent = Agent(
            role="B2A Data Synthesizer",
            goal="Convert raw B2A execution logs into a clean, agent-readable or human-friendly response.",
            backstory="Expert in summarizing complex technical execution results into high-signal information.",
            llm=response_llm,
        )

        synthesis_task = Task(
            description=(
                f"Synthesize the B2A execution result into a concise response:\n\n"
                f"{inputs['result']}"
            ),
            expected_output="A high-signal, actionable summary of the B2A workflow outcome.",
            agent=synthesis_agent,
        )

        crew = Crew(agents=[synthesis_agent], tasks=[synthesis_task], verbose=True)
        final_result = crew.kickoff()
        return {"result": str(final_result)}


# Usage example
async def main():
    flow = B2AEngineFlow()
    flow.state.query = "Extract the top contributor's username from this GitHub repository: https://github.com/browserbase/stagehand"
    result = await flow.kickoff_async()

    print(f"\n{'='*50}")
    print(f"B2A ENGINE FINAL RESULT")
    print(f"{'='*50}")
    print(result["result"])


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

