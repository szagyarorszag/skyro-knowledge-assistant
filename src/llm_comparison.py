# llm comparison script for skyro knowledge assistant
import os
import time
import json
from typing import Dict, List
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
import requests

from vectorstore import VectorStoreManager

load_dotenv(dotenv_path="../.env", override=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# models to compare
MODELS = {
    "Gemini 2.5 Flash": "gemini-2.5-flash",
    "Gemini 2.5 Pro": "gemini-2.5-pro",
    "Mistral Small 3.2": "mistralai/mistral-small-3.2-24b-instruct:free",
    "Llama 3.3 8B": "meta-llama/llama-3.3-8b-instruct:free"
}

# test questions
TEST_QUESTIONS = [
    "What is our KYC verification process?",
    "How does the fraud detection system work?",
    "What were the Q3 2024 business results?",
    "Explain the payment retry logic",
    "What caused the October incident?",
    "What are our Q4 OKR priorities?",
    "How long does a refund take?",
    "What are the KYC transaction limits?",
    "Describe the database selection decision",
    "What is the incident response procedure?"
]


def get_context_for_question(vectorstore_manager: VectorStoreManager, question: str, k: int = 5) -> tuple:
    # to retrieve context for a question and return both formatted string and raw chunks
    docs_with_scores = vectorstore_manager.similarity_search_with_score(question, k=k)
    documents = [doc for doc, score in docs_with_scores]
    
    context_parts = []
    chunks = []
    
    for i, (doc, score) in enumerate(docs_with_scores, 1):
        source = doc.metadata.get('source', 'Unknown')
        category = doc.metadata.get('category', 'General')
        content = doc.page_content.strip()
        context_parts.append(f"[Document {i} - {source}]\n{content}\n")
        
        chunks.append({
            "rank": i,
            "source": source,
            "category": category,
            "content": content,
            "score": float(score)
        })
    
    return "\n".join(context_parts), chunks


def query_openrouter(model: str, context: str, question: str, max_retries: int = 2) -> Dict:
    # to query openrouter api with retry logic for rate limits
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""You are an assistant for Skyro's internal knowledge base. Answer questions using only the provided documentation context.

CONTEXT:
{context}

QUESTION: {question}

Guidelines:
- Base answers strictly on the provided context
- State clearly if information is insufficient
- Reference specific details and source documents when applicable
- Use professional language
- Structure answers with bullet points or paragraphs as needed

ANSWER:"""
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    start_time = time.time()
    
    for attempt in range(max_retries + 1):
        try:
            response = requests.post(OPENROUTER_BASE_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            elapsed_time = time.time() - start_time
            
            result = response.json()
            answer = result['choices'][0]['message']['content']
            
            return {
                "answer": answer,
                "time": elapsed_time,
                "error": None
            }
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429 and attempt < max_retries:
                wait_time = 30 * (attempt + 1)
                print(f"\n  [rate limit, waiting {wait_time}s...]", flush=True)
                time.sleep(wait_time)
                continue
            else:
                elapsed_time = time.time() - start_time
                try:
                    error_detail = response.json().get('error', {}).get('message', str(e))
                except:
                    error_detail = str(e)
                return {
                    "answer": None,
                    "time": elapsed_time,
                    "error": error_detail
                }
        except requests.exceptions.Timeout:
            elapsed_time = time.time() - start_time
            return {
                "answer": None,
                "time": elapsed_time,
                "error": "Timeout after 30 seconds"
            }
        except Exception as e:
            elapsed_time = time.time() - start_time
            return {
                "answer": None,
                "time": elapsed_time,
                "error": str(e)
            }
    
    elapsed_time = time.time() - start_time
    return {
        "answer": None,
        "time": elapsed_time,
        "error": "Max retries exceeded"
    }


def query_gemini(model_name: str, context: str, question: str) -> Dict:
    # to query gemini api
    prompt = f"""You are an assistant for Skyro's internal knowledge base. Answer questions using only the provided documentation context.

CONTEXT:
{context}

QUESTION: {question}

Guidelines:
- Base answers strictly on the provided context
- State clearly if information is insufficient
- Reference specific details and source documents when applicable
- Use professional language
- Structure answers with bullet points or paragraphs as needed

ANSWER:"""
    
    start_time = time.time()
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        elapsed_time = time.time() - start_time
        
        return {
            "answer": response.text,
            "time": elapsed_time,
            "error": None
        }
    except Exception as e:
        elapsed_time = time.time() - start_time
        return {
            "answer": None,
            "time": elapsed_time,
            "error": str(e)
        }


def run_comparison():
    
    # Load vector store
    print("\nloading vector store...")
    vm = VectorStoreManager(persist_directory="../chroma_db")
    if not vm.load_vectorstore():
        print("ERROR: Failed to load vector store")
        return
    
    print(f"vector store loaded: {vm.get_collection_stats()['total_documents']} documents")
    
    # results storage
    results = []
    
    # test each question
    for q_idx, question in enumerate(TEST_QUESTIONS, 1):
        print(f"\n question {q_idx}/{len(TEST_QUESTIONS)}: {question}")

        
        context, chunks = get_context_for_question(vm, question, k=5)
        
        question_results = {
            "question": question,
            "question_num": q_idx,
            "retrieved_chunks": chunks
        }
        
        # Test each model
        for model_name, model_id in MODELS.items():
            print(f"\n testing {model_name}...", end=" ", flush=True)
            
            # Check if it's a Gemini model (starts with "gemini-")
            if model_id.startswith("gemini-"):
                result = query_gemini(model_id, context, question)
            else:
                result = query_openrouter(model_id, context, question)
            
            if result["error"]:
                print(f"ERROR: {result['error']}", flush=True)
                question_results[f"{model_name}_answer"] = "ERROR"
                question_results[f"{model_name}_time"] = result["time"]
                question_results[f"{model_name}_length"] = 0
            else:
                answer_length = len(result["answer"]) if result["answer"] else 0
                print(f"({result['time']:.2f}s, {answer_length} chars)", flush=True)
                question_results[f"{model_name}_answer"] = result["answer"]
                question_results[f"{model_name}_time"] = result["time"]
                question_results[f"{model_name}_length"] = answer_length
            
            # Wait 20 seconds before next request to avoid rate limiting
            print(f"  [Waiting 20s before next model...]", flush=True)
            time.sleep(20)
        
        results.append(question_results)
    
    # response times
    time_data = []
    for r in results:
        row = {"Question": f"Q{r['question_num']}"}
        for model_name in MODELS.keys():
            row[model_name] = f"{r[f'{model_name}_time']:.2f}s"
        time_data.append(row)
    
    time_df = pd.DataFrame(time_data)
    
    avg_row = {"Question": "Average"}
    for model_name in MODELS.keys():
        avg_time = sum(r[f"{model_name}_time"] for r in results) / len(results)
        avg_row[model_name] = f"{avg_time:.2f}s"
    time_df = pd.concat([time_df, pd.DataFrame([avg_row])], ignore_index=True)
    
    # answer lengths
    length_data = []
    for r in results:
        row = {"Question": f"Q{r['question_num']}"}
        for model_name in MODELS.keys():
            row[model_name] = r[f"{model_name}_length"]
        length_data.append(row)
    
    length_df = pd.DataFrame(length_data)
    
    avg_row = {"Question": "Average"}
    for model_name in MODELS.keys():
        avg_length = sum(r[f"{model_name}_length"] for r in results) / len(results)
        avg_row[model_name] = f"{avg_length:.0f}"
    length_df = pd.concat([length_df, pd.DataFrame([avg_row])], ignore_index=True)
    
    print("responce time comparison (seconds) ")

    print(time_df.to_string(index=False))
    
    print("\n answer length comparison (characters) ")
    print(length_df.to_string(index=False))
    
    with open("../llm_comparison_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    time_df.to_csv("../llm_comparison_time.csv", index=False)
    length_df.to_csv("../llm_comparison_length.csv", index=False)
    
    print("\nresults saved")


if __name__ == "__main__":
    run_comparison()

