import os
import re
from typing import List, Dict

def tokenize(text: str) -> set:
    """Simple tokenizer that lowers text, removes non-alphanumeric chars, and filters stop words."""
    stop_words = {"a", "an", "the", "and", "or", "but", "is", "are", "was", "were", "to", "in", "on", "for", "with", "as", "by", "of", "it", "this", "that", "i", "you", "he", "she", "write", "create", "make", "how", "what", "where", "when", "why"}
    words = re.findall(r'\b[a-z0-9]+\b', text.lower())
    return {w for w in words if w not in stop_words and len(w) > 1}

def load_documents(kb_dir: str) -> List[Dict[str, str]]:
    """Loads all text/markdown files from the knowledge base directory."""
    documents = []
    if not os.path.exists(kb_dir):
        return documents
        
    for root, _, files in os.walk(kb_dir):
        for file in files:
            if file.endswith(('.txt', '.md', '.py', '.json')):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # converts the content into chunks for better analysis and labels them
                        chunks = [c.strip() for c in content.split('\n\n') if len(c.strip()) > 30]
                        for i, chunk in enumerate(chunks):
                            documents.append({
                                "source": f"{file} (Part {i+1})",
                                "content": chunk
                            })
                except Exception as e:
                    print(f"Failed to read {file}: {e}")
    return documents

def retrieve_context(user_prompt: str, top_k: int = 3) -> str:
    """
    Zero-dependency RAG retriever. 
    Scores document chunks based on keyword overlap with the prompt.
    Returns a formatted string of the most relevant context.
    """
    kb_dir = os.path.join(os.path.dirname(__file__), 'knowledge_base')
    documents = load_documents(kb_dir)
    
    if not documents:
        return ""
        
    prompt_tokens = tokenize(user_prompt)
    if not prompt_tokens:
        return ""
        
    scored_docs = []
    for doc in documents:
        doc_tokens = tokenize(doc["content"])
        # Score is the number of overlapping unique keywords
        score = len(prompt_tokens.intersection(doc_tokens))
        
        # Give a slight boost if the chunk contains exact word matches from prompt
        for p_token in prompt_tokens:
            if p_token in doc["content"].lower():
                score += 0.5
                
        if score > 0:
            scored_docs.append((score, doc))
            
    if not scored_docs:
        return ""
        
    # Sort by score descending
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    
    # top-k ko extract krega
    top_docs = [doc for score, doc in scored_docs[:top_k]]
    
    # Format into a single string to inject into the prompt
    context_str = "=== RETRIEVED KNOWLEDGE BASE CONTEXT ===\n"
    for doc in top_docs:
        context_str += f"[Source: {doc['source']}]\n{doc['content']}\n\n"
    context_str += "========================================\n"
    
    return context_str
