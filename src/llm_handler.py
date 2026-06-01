import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import re 

def configure_llm():
    """
    Loads the API key from .env and configures the Google Generative AI model.
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")
    genai.configure(api_key=api_key)

def generate_question_from_context(vector_store, marks, difficulty, topic):
    """
    Generates a single question by retrieving context from the vector store
    and prompting the LLM.
    """
    
    results = vector_store.query(query_texts=[topic], n_results=3)
    context = " ".join(results['documents'][0])

    # --- DYNAMIC PROMPT ENGINEERING BASED ON MARKS ---
    creative_instruction = ""
    marks_instruction = ""

    if marks <= 2:
        creative_instruction = "The question should be a direct, factual recall or definition question."
        marks_instruction = f"Provide a concise, one or two-sentence answer suitable for {marks} marks."
    elif marks <= 4:
        creative_instruction = "The question should require a brief explanation, listing of points, or a simple example."
        marks_instruction = f"Provide a short paragraph or a few bullet points as an answer, suitable for {marks} marks."
    elif marks <= 5:
        creative_instruction = "This question MUST require critical thinking, application, or comparison. Do NOT ask simple 'What is...' or 'Define...' questions. Ask a 'Why...', 'How...', or 'Compare...' question that uses the context."
        marks_instruction = f"Provide a detailed, multi-point answer suitable for a {marks}-mark marking scheme."
    else:  # For 10 marks
        creative_instruction = "This is a high-value essay question. It MUST require in-depth analysis, synthesis of multiple concepts from the context, or an evaluation of a topic. Ask a comprehensive question that demands a structured, detailed response."
        marks_instruction = f"Provide a comprehensive, multi-paragraph answer with a clear structure (introduction, body, conclusion) suitable for a detailed {marks}-mark marking scheme. Break down the marks allocation in the answer."
    
    prompt_template = f"""
    You are an expert educator and question paper setter.
    Your task is to generate ONE single question based on the following context.
    
    ---
    Context:
    "{context}"
    ---
    
    Task:
    1. Generate one question that fits the Marks ({marks}) and Difficulty ({difficulty}).
    2. The question itself MUST NOT include phrases like "Based on the text" or "According to the context".
    3. {creative_instruction}
    4. {marks_instruction}
    
    Format:
    Return the output strictly in the following JSON format. Do not include any other text.
    {{
      "question": "Your generated question here",
      "answer": "Your detailed answer/marking scheme here"
    }}
    """
    
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(prompt_template)
        
        # Robust JSON parsing
        match = re.search(r"\{.*\}", response.text, re.DOTALL)
        if match:
            json_str = match.group(0)
            question_data = json.loads(json_str)
            if "question" not in question_data or "answer" not in question_data:
                raise ValueError("LLM response did not contain 'question' or 'answer' keys.")
            return question_data
        else:
            raise ValueError(f"Could not find a valid JSON object in the LLM response: {response.text}")
        
    except Exception as e:
        print(f"Error during LLM call or JSON parsing: {e}")
        return {
            "question": f"Error generating question: {e}",
            "answer": "N/A"
        }