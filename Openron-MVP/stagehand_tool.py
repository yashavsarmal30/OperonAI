import os
from stagehand import Stagehand, StagehandConfig

import nest_asyncio
import asyncio

# Allow nested loops in async (for environments like Jupyter or already-running loops)
nest_asyncio.apply()


def browser_automation(task_description: str, website_url: str) -> str:
    """
    B2A Translation Layer: Bridges the gap between legacy web interfaces 
    and deterministic agentic logic.
    """

    async def _execute_automation():
        stagehand = None

        try:
            # Dynamic configuration from environment
            provider = os.getenv("STAGEHAND_PROVIDER", "openai")
            model_name = os.getenv("STAGEHAND_MODEL", "gpt-4o")
            api_key = os.getenv("STAGEHAND_API_KEY", os.getenv("OPENAI_API_KEY"))

            config = StagehandConfig(
                env="LOCAL",
                model_name=model_name,
                self_heal=True,
                system_prompt="You are a B2A Engine agent. Your goal is to translate human intent into deterministic actions on legacy web interfaces.",
                model_client_options={"apiKey": api_key} if api_key else {},
                verbose=1,
            )

            stagehand = Stagehand(config)
            await stagehand.init()

            # Create a B2A-aligned agent
            agent = stagehand.agent(
                model=model_name,
                provider=provider,
                instructions=(
                    "You are a B2A Engine execution assistant. "
                    "Navigate the web interface to achieve the objective. "
                    "Prioritize high-signal data extraction and autonomous completion. "
                    "Do not ask follow-up questions."
                ),
                options={"apiKey": api_key} if api_key else {},
            )

            await stagehand.page.goto(website_url)

            # Execute the planned workflow
            agent_result = await agent.execute(
                instruction=task_description,
                max_steps=20,
                auto_screenshot=True,
            )

            result_message = (
                agent_result.message or "B2A execution completed without a specific status message."
            )
            return f"B2A Execution Result:\n{result_message}"

        except Exception as e:
            return f"B2A Actionable Error: Encountered {type(e).__name__} during execution. Details: {str(e)}"

        finally:
            if stagehand:
                await stagehand.close()

    # Run async in a sync context to maintain tool compatibility
    return asyncio.run(_execute_automation())

