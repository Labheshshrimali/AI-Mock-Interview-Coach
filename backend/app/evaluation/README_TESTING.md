# Testing Strategy: AI Mock Interview Coach

To ensure the reliability of the ML pipeline, we implement a modular testing strategy.

## Pipeline Verification
The `backend/app/evaluation/test_pipeline.py` script acts as an integration test for the core pipeline:
1. **Transcription:** Validates that `faster-whisper` returns a valid string.
2. **Signal Analysis:** Verifies `librosa` extracts all required keys (WPM, filler count, pause count).
3. **Content Evaluation:** Confirms `Ollama` returns valid JSON scores for relevance, completeness, and structure.

## Running Tests
Run this command from the `backend/` directory to verify the pipeline:
```bash
python -m app.evaluation.test_pipeline
```

## Why this matters for interviews
When asked about testing in interviews, you can explain:
> "I built an integration test suite for the ML pipeline. Since ML outputs can be non-deterministic, I focused on validating the output *schema*—ensuring that downstream dashboard components always receive the expected data structures, even if the AI evaluation values fluctuate."
