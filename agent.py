# agent.py
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Using 2.5 to demonstrate that even the latest models need orchestration for deep dependency analysis
MODEL_NAME = 'gemini-2.5-flash'


def v1_naive(chat_log):
    # V1: Zero-shot attempt. Usually misses the late-breaking blocker.
    config = genai.GenerationConfig(response_mime_type="application/json")
    model = genai.GenerativeModel(MODEL_NAME, generation_config=config)

    prompt = f"""
    You are a Technical Program Manager. Extract all planned engineering tasks from this chat.
    Return a JSON list of objects. Each object MUST have these exact 4 keys:
    - 'task' (string summary)
    - 'owner' (person or team responsible)
    - 'due_date' (specific date or 'N/A' if none)
    - 'status' (MUST be one of: 'active', 'blocked', 'cancelled')

    Chat Log:
    {chat_log}
    """
    try:
        return json.loads(model.generate_content(prompt).text)
    except Exception as e:
        return [{"error": "V1 Failed", "details": str(e)}]

def v2_orchestrated(chat_log):
    model_thinker = genai.GenerativeModel(MODEL_NAME)
    model_formatter = genai.GenerativeModel(MODEL_NAME, generation_config={"response_mime_type": "application/json"})

    # REASONING PROMPT - Updated for "Fire Drills"
    reasoning_prompt = f"""
    Analyze this engineering chat as an experienced TPM.
    1. Identify initial commitments (e.g., Mike committed to X by Thursday).
    2. DETECT HIJACKS: Did a new, urgent P0 issue interrupt the plan?
    3. ANALYZE RESOURCE CONTENTION: If Mike is 100% focused on a P0 fire, can he still meet his previous P1 deadline? (Usually NO -> mark P1 as blocked/at-risk).
    4. Determine FINAL status for all tasks based on this re-prioritization.
    Chat Log:
    {chat_log}
    """
    reasoning = model_thinker.generate_content(reasoning_prompt).text

    # (Keep the same final_prompt and return logic as before)
    final_prompt = f"""
    Based ONLY on the dependency analysis below, generate the final JSON task list.
    RULES:
    - If a task was de-prioritized due to a P0 fire, mark it as 'blocked' or 'cancelled'.
    - Ensure the P0 fire is listed as an 'active' task.

    Dependency Analysis: {reasoning}
    Original Chat: {chat_log}

    Return a JSON list of objects with these exact 4 keys: 'task', 'owner', 'due_date', 'status'.
    """
    # ... (rest of the function is the same try/except block)
    try:
        tasks = json.loads(model_formatter.generate_content(final_prompt).text)
        return {"reasoning": reasoning, "tasks": tasks}
    except Exception as e:
        return {"error": "V2 Failed", "details": str(e), "reasoning": reasoning}