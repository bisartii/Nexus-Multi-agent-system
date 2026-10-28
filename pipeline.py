import json
import requests
import os
from rag_retriever import retrieve_context

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_text(system_prompt, user_prompt, config, temperature=0.7):
    url = config['ollama']['base_url']
    model = config['ollama']['model']

    # Using Ollama's generate API
    payload = {
        "model": model,
        "prompt": f"System Guidelines:\n{system_prompt}\n\nUser Input:\n{user_prompt}\n\nResponse:",
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_ctx": 4096 # Limit context to avoid OOM on 4GB VRAM
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        result = response.json()
        return result.get('response', '')
    except requests.exceptions.RequestException as e:
        return f"Error: Failed to communicate with Ollama. Make sure it is running. Details: {str(e)}"

def run_pipeline(domain, user_prompt, temperature=0.7, status_callback=None, output_callback=None):
    """
    Executes the 3-agent pipeline sequentially to minimize VRAM usage.
    """
    config = load_config()
    
    if domain not in config['domains']:
        return {"error": f"Domain '{domain}' not found in configuration."}
        
    domain_prompts = config['domains'][domain]
    outputs = {}
    
    # RAG Retrieval Phase

    if status_callback:
        status_callback("Scanning local Knowledge Base for relevant context...")
        
    retrieved_context = retrieve_context(user_prompt)
    outputs['rag_context'] = retrieved_context
    

    # Agent 1: The Planner / Researcher

    if status_callback:
        status_callback("Agent 1 (Planner) is analyzing the request and retrieved knowledge...")
    
    # retrieved context ko user prompt k sath attach 
    augmented_prompt = user_prompt
    if retrieved_context:
        augmented_prompt = f"{retrieved_context}\n\nPlease strictly follow the above context/guidelines when fulfilling the request:\n{user_prompt}"
    
    plan = generate_text(domain_prompts['planner'], augmented_prompt, config, temperature=temperature)
    
    # y terminal pr print krega bro
    print(f"\n{'='*20} 🧠 AGENT 1 (PLANNER) OUTPUT {'='*20}")
    print(plan)
    
    # app pr show karega
    if output_callback:
        output_callback(1, plan)
        
    outputs['plan'] = plan
    
    if plan.startswith("Error"):
        return outputs
        
    # Agent 2: The Creator / Producer

    if status_callback:
        status_callback("Agent 2 (Creator) is generating the draft...")
        
    creator_prompt = f"Original Request: {user_prompt}\n\nPlan to strictly follow:\n{plan}"
    draft = generate_text(domain_prompts['creator'], creator_prompt, config, temperature=temperature)
    
    # terminal pr print krega
    print(f"\n{'='*20} ✍️ AGENT 2 (CREATOR) OUTPUT {'='*20}")
    print(draft)
    
    # app print
    if output_callback:
        output_callback(2, draft)
        
    outputs['draft'] = draft
    
    if draft.startswith("Error"):
        return outputs
        
    # Agent 3: The Reviewer / QA

    if status_callback:
        status_callback("Agent 3 (Reviewer) is polishing the output...")
        
    reviewer_prompt = f"Original Request: {user_prompt}\n\nDraft to review and polish:\n{draft}"
    final_output = generate_text(domain_prompts['reviewer'], reviewer_prompt, config, temperature=temperature)
    
    # Print to Terminal
    print(f"\n{'='*20} 🧐 AGENT 3 (REVIEWER) OUTPUT {'='*20}")
    print(final_output)
    print("\n" + "="*60 + "\n")
    
    # Send to App 
    if output_callback:
        output_callback(3, final_output)
        
    outputs['final'] = final_output
    
    if status_callback:
        status_callback("Pipeline complete!")
        
    return outputs
