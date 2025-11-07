# llm answer evaluation script

import os
import sys
import json
import time
from typing import Dict, List
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
import requests
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

sys.path.append(str(Path(__file__).parent))

from vectorstore import VectorStoreManager

load_dotenv(dotenv_path="../.env", override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
JUDGE_MODEL = "gemini-2.5-pro"

print("loading embedding model...")
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print("embedding model loaded")


def retrieve_chunks_for_question(vectorstore_manager: VectorStoreManager, question: str, k: int = 5) -> List[Dict]:
    # to retrieve chunks for a question using the same method as the rag system
    docs_with_scores = vectorstore_manager.similarity_search_with_score(question, k=k)
    
    chunks = []
    for i, (doc, score) in enumerate(docs_with_scores, 1):
        source = doc.metadata.get('source', 'Unknown')
        category = doc.metadata.get('category', 'General')
        content = doc.page_content.strip()
        
        chunks.append({
            "rank": i,
            "source": source,
            "category": category,
            "content": content,
            "score": float(score)
        })
    
    return chunks


def calculate_semantic_similarity(answer: str, chunks: List[Dict]) -> Dict:
    # to calculate semantic similarity between answer and retrieved chunks
    if not answer or answer == "ERROR":
        return {
            "max_similarity": 0.0,
            "avg_similarity": 0.0,
            "min_similarity": 0.0,
            "weighted_similarity": 0.0
        }
    
    answer_embedding = embedding_model.encode([answer])[0]
    
    chunk_texts = [chunk["content"] for chunk in chunks]
    chunk_embeddings = embedding_model.encode(chunk_texts)
    
    similarities = []
    for chunk_emb, chunk in zip(chunk_embeddings, chunks):
        # cosine similarity
        similarity = np.dot(answer_embedding, chunk_emb) / (
            np.linalg.norm(answer_embedding) * np.linalg.norm(chunk_emb)
        )
        similarities.append(float(similarity))
    
    # weighted similarity (higher weight for top-ranked chunks)
    weights = [1.0 / (i + 1) for i in range(len(similarities))]
    total_weight = sum(weights)
    weighted_sim = sum(s * w for s, w in zip(similarities, weights)) / total_weight if total_weight > 0 else 0.0
    
    return {
        "max_similarity": max(similarities) if similarities else 0.0,
        "avg_similarity": np.mean(similarities) if similarities else 0.0,
        "min_similarity": min(similarities) if similarities else 0.0,
        "weighted_similarity": weighted_sim
    }


def query_gemini_judge(chunks: List[Dict], question: str, answer: str, max_retries: int = 2) -> Dict:
    # to use gemini 2.5 pro as a judge to evaluate answer quality against chunks
    if not answer or answer == "ERROR":
        return {
            "faithfulness_score": 0,
            "coverage_score": 0,
            "has_hallucinations": True,
            "judge_explanation": "No answer provided",
            "error": None
        }
    
    chunks_text = "\n\n".join([
        f"CHUNK {i+1} (from {chunk['source']}):\n{chunk['content']}"
        for i, chunk in enumerate(chunks)
    ])
    
    prompt = f"""You are an expert evaluator for RAG (Retrieval-Augmented Generation) systems. Your task is to evaluate whether an AI assistant's answer is faithful to the retrieved source chunks.

QUESTION:
{question}

RETRIEVED CHUNKS FROM KNOWLEDGE BASE:
{chunks_text}

ASSISTANT'S ANSWER TO EVALUATE:
{answer}

EVALUATION CRITERIA:

1. **Faithfulness Score (0-10)**: Can ALL statements in the answer be traced back to the chunks?
   - 10 = Every claim is directly supported by chunks
   - 7-9 = Most claims supported, minor inferences acceptable
   - 4-6 = Some claims supported, some unsupported
   - 0-3 = Many unsupported claims or contradictions

2. **Coverage Score (0-10)**: How much relevant information from the chunks is included in the answer?
   - 10 = All relevant information included
   - 7-9 = Most key information included
   - 4-6 = Some key information missing
   - 0-3 = Major gaps in coverage

3. **Hallucination Detection**: Does the answer contain information NOT present in the chunks?
   - YES = Contains information not in chunks
   - NO = All information traceable to chunks

Please respond in the following JSON format ONLY (no other text):
{{
  "faithfulness_score": <0-10>,
  "coverage_score": <0-10>,
  "has_hallucinations": <true/false>,
  "explanation": "<brief explanation of your scores>"
}}"""
    
    for attempt in range(max_retries + 1):
        try:
            model = genai.GenerativeModel(JUDGE_MODEL)
            response = model.generate_content(prompt)
            judge_response = response.text
            
            try:
                start_idx = judge_response.find('{')
                end_idx = judge_response.rfind('}') + 1
                if start_idx != -1 and end_idx > start_idx:
                    json_str = judge_response[start_idx:end_idx]
                    evaluation = json.loads(json_str)
                    
                    return {
                        "faithfulness_score": evaluation.get("faithfulness_score", 0),
                        "coverage_score": evaluation.get("coverage_score", 0),
                        "has_hallucinations": evaluation.get("has_hallucinations", True),
                        "judge_explanation": evaluation.get("explanation", ""),
                        "error": None
                    }
                else:
                    return {
                        "faithfulness_score": 0,
                        "coverage_score": 0,
                        "has_hallucinations": True,
                        "judge_explanation": judge_response[:200],
                        "error": "Could not parse JSON from response"
                    }
            except json.JSONDecodeError as e:
                return {
                    "faithfulness_score": 0,
                    "coverage_score": 0,
                    "has_hallucinations": True,
                    "judge_explanation": judge_response[:200] if judge_response else "",
                    "error": f"JSON parse error: {str(e)}"
                }
                
        except Exception as e:
            if attempt < max_retries:
                wait_time = 5 * (attempt + 1)
                print(f"\n  [error, waiting {wait_time}s...]", flush=True)
                time.sleep(wait_time)
                continue
            else:
                return {
                    "faithfulness_score": 0,
                    "coverage_score": 0,
                    "has_hallucinations": True,
                    "judge_explanation": "",
                    "error": str(e)
                }
    
    return {
        "faithfulness_score": 0,
        "coverage_score": 0,
        "has_hallucinations": True,
        "judge_explanation": "",
        "error": "Max retries exceeded"
    }


def evaluate_all_answers():
    # main evaluation function
    
    results_path = "../llm_comparison_results.json"
    print(f"\nloading results from {results_path}...")
    
    try:
        with open(results_path, 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print(f"error: {results_path} not found")
        print("please run llm_comparison.py first")
        return
    
    print(f"loaded {len(results)} questions with answers")
    
    needs_chunk_retrieval = not results[0].get("retrieved_chunks")
    
    if needs_chunk_retrieval:
        print("\nretrieved chunks not found in results")
        print("loading vector store...")
        
        try:
            vectorstore_manager = VectorStoreManager(persist_directory="../chroma_db")
            if not vectorstore_manager.load_vectorstore():
                print("error: failed to load vector store")
                return
            print(f"vector store loaded: {vectorstore_manager.get_collection_stats()['total_documents']} documents")
        except Exception as e:
            print(f"error: failed to load vector store: {str(e)}")
            return
    else:
        vectorstore_manager = None
        print("chunks already present in results")
    
    model_names = [key.replace("_answer", "") for key in results[0].keys() 
                   if key.endswith("_answer")]
    
    print(f"\nfound {len(model_names)} models: {', '.join(model_names)}")
    
    evaluation_results = []
    
    total_evaluations = len(results) * len(model_names)
    current = 0
    
    for result in results:
        question = result["question"]
        question_num = result["question_num"]
        
        if needs_chunk_retrieval:
            print(f"\nquestion {question_num}/{len(results)}: {question}")
            print("retrieving chunks...", end=" ", flush=True)
            chunks = retrieve_chunks_for_question(vectorstore_manager, question, k=5)
            print(f"({len(chunks)} chunks retrieved)", flush=True)
            result["retrieved_chunks"] = chunks
        else:
            chunks = result["retrieved_chunks"]
            print(f"\nevaluating question {question_num}/{len(results)}: {question}")
        
        question_eval = {
            "question": question,
            "question_num": question_num
        }
        
        for model_name in model_names:
            current += 1
            answer = result.get(f"{model_name}_answer")
            
            print(f"\n[{current}/{total_evaluations}] evaluating {model_name}...", flush=True)
            
            if not answer or answer == "ERROR":
                print("  skipping (no answer)", flush=True)
                question_eval[f"{model_name}_semantic_sim"] = 0.0
                question_eval[f"{model_name}_faithfulness"] = 0
                question_eval[f"{model_name}_coverage"] = 0
                question_eval[f"{model_name}_hallucinations"] = True
                continue
            
            print("  computing semantic similarity...", end=" ", flush=True)
            semantic_scores = calculate_semantic_similarity(answer, chunks)
            print(f"(weighted: {semantic_scores['weighted_similarity']:.3f})", flush=True)
            
            question_eval[f"{model_name}_semantic_max"] = semantic_scores["max_similarity"]
            question_eval[f"{model_name}_semantic_avg"] = semantic_scores["avg_similarity"]
            question_eval[f"{model_name}_semantic_weighted"] = semantic_scores["weighted_similarity"]
            
            print("  querying gemini 2.5 pro judge...", end=" ", flush=True)
            judge_scores = query_gemini_judge(chunks, question, answer)
            
            if judge_scores.get("error"):
                print(f"error: {judge_scores['error']}", flush=True)
            else:
                print(f"(F:{judge_scores['faithfulness_score']}, C:{judge_scores['coverage_score']})", flush=True)
            
            question_eval[f"{model_name}_faithfulness"] = judge_scores["faithfulness_score"]
            question_eval[f"{model_name}_coverage"] = judge_scores["coverage_score"]
            question_eval[f"{model_name}_hallucinations"] = judge_scores["has_hallucinations"]
            question_eval[f"{model_name}_judge_explanation"] = judge_scores.get("judge_explanation", "")
            
            if current < total_evaluations:
                time.sleep(3)
        
        evaluation_results.append(question_eval)
    
    if needs_chunk_retrieval:
        updated_results_path = "../llm_comparison_results.json"
        with open(updated_results_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nupdated comparison results saved to {updated_results_path}")
    
    eval_json_path = "../llm_evaluation_results.json"
    with open(eval_json_path, 'w') as f:
        json.dump(evaluation_results, f, indent=2)
    print(f"detailed evaluation saved to {eval_json_path}")
    
    # semantic similarity
    semantic_data = []
    for eval_result in evaluation_results:
        row = {"Question": f"Q{eval_result['question_num']}"}
        for model in model_names:
            score = eval_result.get(f"{model}_semantic_weighted", 0.0)
            row[model] = f"{score:.3f}"
        semantic_data.append(row)
    
    semantic_df = pd.DataFrame(semantic_data)
    
    avg_row = {"Question": "Average"}
    for model in model_names:
        avg_score = np.mean([eval_result.get(f"{model}_semantic_weighted", 0.0) 
                            for eval_result in evaluation_results])
        avg_row[model] = f"{avg_score:.3f}"
    semantic_df = pd.concat([semantic_df, pd.DataFrame([avg_row])], ignore_index=True)
    
    # faithfulness score
    faithfulness_data = []
    for eval_result in evaluation_results:
        row = {"Question": f"Q{eval_result['question_num']}"}
        for model in model_names:
            score = eval_result.get(f"{model}_faithfulness", 0)
            row[model] = score
        faithfulness_data.append(row)
    
    faithfulness_df = pd.DataFrame(faithfulness_data)
    
    avg_row = {"Question": "Average"}
    for model in model_names:
        avg_score = np.mean([eval_result.get(f"{model}_faithfulness", 0) 
                            for eval_result in evaluation_results])
        avg_row[model] = f"{avg_score:.1f}"
    faithfulness_df = pd.concat([faithfulness_df, pd.DataFrame([avg_row])], ignore_index=True)
    
    # coverage score
    coverage_data = []
    for eval_result in evaluation_results:
        row = {"Question": f"Q{eval_result['question_num']}"}
        for model in model_names:
            score = eval_result.get(f"{model}_coverage", 0)
            row[model] = score
        coverage_data.append(row)
    
    coverage_df = pd.DataFrame(coverage_data)
    
    avg_row = {"Question": "Average"}
    for model in model_names:
        avg_score = np.mean([eval_result.get(f"{model}_coverage", 0) 
                            for eval_result in evaluation_results])
        avg_row[model] = f"{avg_score:.1f}"
    coverage_df = pd.concat([coverage_df, pd.DataFrame([avg_row])], ignore_index=True)
    
    # hallucination count
    hallucination_data = []
    for eval_result in evaluation_results:
        row = {"Question": f"Q{eval_result['question_num']}"}
        for model in model_names:
            has_halluc = eval_result.get(f"{model}_hallucinations", True)
            row[model] = "YES" if has_halluc else "NO"
        hallucination_data.append(row)
    
    hallucination_df = pd.DataFrame(hallucination_data)
    
    total_row = {"Question": "Total YES"}
    for model in model_names:
        total_yes = sum(1 for eval_result in evaluation_results 
                       if eval_result.get(f"{model}_hallucinations", True))
        total_row[model] = total_yes
    hallucination_df = pd.concat([hallucination_df, pd.DataFrame([total_row])], ignore_index=True)
    
    print("\nsemantic similarity (weighted, 0-1 scale, higher is better)")
    print(semantic_df.to_string(index=False))
    
    print("\nfaithfulness score (0-10 scale, higher is better)")
    print(faithfulness_df.to_string(index=False))
    
    print("\ncoverage score (0-10 scale, higher is better)")
    print(coverage_df.to_string(index=False))
    
    print("\nhallucination detection (fewer is better)")
    print(hallucination_df.to_string(index=False))
    
    semantic_df.to_csv("../llm_evaluation_semantic_similarity.csv", index=False)
    faithfulness_df.to_csv("../llm_evaluation_faithfulness.csv", index=False)
    coverage_df.to_csv("../llm_evaluation_coverage.csv", index=False)
    hallucination_df.to_csv("../llm_evaluation_hallucinations.csv", index=False)
    
    summary_data = {
        "Model": model_names,
        "Avg Semantic Sim": [
            np.mean([er.get(f"{m}_semantic_weighted", 0.0) for er in evaluation_results])
            for m in model_names
        ],
        "Avg Faithfulness": [
            np.mean([er.get(f"{m}_faithfulness", 0) for er in evaluation_results])
            for m in model_names
        ],
        "Avg Coverage": [
            np.mean([er.get(f"{m}_coverage", 0) for er in evaluation_results])
            for m in model_names
        ],
        "Hallucinations": [
            sum(1 for er in evaluation_results if er.get(f"{m}_hallucinations", True))
            for m in model_names
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    summary_df = summary_df.round({"Avg Semantic Sim": 3, "Avg Faithfulness": 1, "Avg Coverage": 1})

    print("\nsummary:")
    print(summary_df.to_string(index=False))
    
    summary_df.to_csv("../llm_evaluation_summary.csv", index=False)


if __name__ == "__main__":
    evaluate_all_answers()
