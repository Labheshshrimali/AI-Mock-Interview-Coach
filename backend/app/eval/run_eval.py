import json
import os
import sys

# To allow importing from the parent app folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.audio.features import extract_delivery_metrics
from app.evaluation.content_score import evaluate_content
from app.audio.transcribe import transcribe_audio

def run_evaluation():
    """
    Evaluates the automated scoring system against hand-labeled human data.
    This script proves that the AI feedback correlates with actual human judgment.
    """
    eval_file = os.path.join(os.path.dirname(__file__), "labeled_answers.jsonl")
    
    if not os.path.exists(eval_file):
        print("No evaluation data found. Please create 'labeled_answers.jsonl' with sample answers to run the eval.")
        print('Format: {"audio_path": "path/to/file.wav", "question": "...", "human_rating": "good/mediocre/poor"}')
        return

    print("Starting evaluation pipeline...")
    correct_correlations = 0
    total_samples = 0

    with open(eval_file, 'r') as f:
        for line in f:
            if not line.strip():
                continue
                
            sample = json.loads(line)
            audio_path = sample["audio_path"]
            question = sample["question"]
            human_rating = sample["human_rating"] # "good", "mediocre", "poor"
            
            print(f"Evaluating: {audio_path} (Human rating: {human_rating})")
            
            # 1. Transcribe
            transcript = transcribe_audio(audio_path)
            
            # 2. Score
            score = evaluate_content(question, transcript)
            avg_score = (score["relevance_score"] + score["completeness_score"] + score["structure_score"]) / 3.0
            
            # Simple heuristic mapping for correlation
            if avg_score >= 8:
                ai_rating = "good"
            elif avg_score >= 5:
                ai_rating = "mediocre"
            else:
                ai_rating = "poor"
                
            print(f"  AI Transcript: {transcript}")
            print(f"  AI Scores: Relevance={score['relevance_score']}, Completeness={score['completeness_score']}, Structure={score['structure_score']}")
            print(f"  AI Overall Rating: {ai_rating}")
            
            if ai_rating == human_rating:
                print("  MATCH: AI agrees with human.\n")
                correct_correlations += 1
            else:
                print("  MISMATCH: AI disagrees with human.\n")
                
            total_samples += 1
            
    if total_samples > 0:
        accuracy = (correct_correlations / total_samples) * 100
        print(f"Evaluation Complete! Accuracy: {accuracy:.1f}%")
        print("Note: In a real placement interview, you would show how you adjusted the LLM prompt to improve this percentage.")

if __name__ == "__main__":
    run_evaluation()
