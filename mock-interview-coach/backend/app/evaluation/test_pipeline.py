import json
from app.audio.transcribe import transcribe_audio
from app.audio.features import extract_delivery_metrics
from app.evaluation.content_score import evaluate_content
import os

def run_test_pipeline(audio_path, question):
    """Runs the pipeline and validates output structure."""
    print(f"--- Running Test Pipeline for: {question} ---")
    
    # 1. Transcribe
    transcript = transcribe_audio(audio_path)
    assert isinstance(transcript, str), "Transcript must be a string"
    print(f"✅ Transcript: {transcript[:50]}...")
    
    # 2. Metrics
    metrics = extract_delivery_metrics(audio_path, transcript)
    required_metrics = ['words_per_minute', 'filler_word_count', 'pause_count']
    for m in required_metrics:
        assert m in metrics, f"Missing metric: {m}"
    print(f"✅ Metrics: {metrics}")
    
    # 3. Content
    score = evaluate_content(question, transcript)
    required_scores = ['relevance_score', 'completeness_score', 'structure_score']
    for s in required_scores:
        assert s in score, f"Missing score: {s}"
    print(f"✅ Score: {score}")
    
    print("--- Test Complete: Pipeline Verified ---")

if __name__ == "__main__":
    # Ensure dummy_test.wav exists
    test_audio = os.path.join(os.path.dirname(__file__), "../dummy_test.wav")
    if os.path.exists(test_audio):
        run_test_pipeline(test_audio, "Tell me about a time you disagreed with a teammate.")
    else:
        print(f"Error: Test file not found at {test_audio}")
