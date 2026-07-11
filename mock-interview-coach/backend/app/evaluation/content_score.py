import json
import urllib.request
import urllib.parse

def evaluate_content(question: str, transcript: str) -> dict:
    """
    Sends the question and transcript to a local Ollama instance running Llama 3.2.
    Expects a structured JSON response evaluating relevance, completeness, and structure.
    """
    prompt = f"""
    You are an expert interview coach evaluating a candidate's answer.
    
    Interview Question: "{question}"
    Candidate's Answer: "{transcript}"
    
    Evaluate the candidate's answer based on the following criteria:
    1. Relevance Score (1-10): Does the answer directly address the question?
    2. Completeness Score (1-10): Does the answer provide sufficient detail and context?
    3. Structure Score (1-10): Is the answer logically organized (e.g., STAR method)?
    4. Strengths: A list of 1-2 things they did well.
    5. Improvements: A list of 1-2 things they can improve.
    
    Return ONLY a JSON object with this exact structure (no markdown, no extra text):
    {{
        "relevance_score": int,
        "completeness_score": int,
        "structure_score": int,
        "strengths": ["str", "str"],
        "improvements": ["str", "str"]
    }}
    """
    
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
        "format": "json"  # Force JSON output (Llama 3.2 supports this!)
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            response_text = result.get("response", "{}")
            # Parse the JSON returned by the LLM
            return json.loads(response_text)
    except Exception as e:
        print(f"Ollama Error: {e}")
        # Fallback in case Ollama is not running or fails
        return {
            "relevance_score": 0,
            "completeness_score": 0,
            "structure_score": 0,
            "strengths": ["Failed to connect to Ollama."],
            "improvements": ["Make sure Ollama is running locally with 'ollama run llama3.2'"]
        }
