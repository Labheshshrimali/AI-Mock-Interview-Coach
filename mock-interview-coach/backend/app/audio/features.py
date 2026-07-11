import librosa
import numpy as np

def extract_delivery_metrics(audio_path: str, transcript_text: str):
    """
    Extract delivery features using librosa (signal processing) and basic text analysis.
    This is what makes the project "real" signal processing, not just an API wrapper!
    """
    # 1. Load the audio file
    y, sr = librosa.load(audio_path, sr=None)
    
    # 2. Calculate duration
    duration_seconds = librosa.get_duration(y=y, sr=sr)
    
    # 3. Pause Detection using silence thresholds
    # top_db=30 means anything 30dB below the peak is considered silence
    non_mute_intervals = librosa.effects.split(y, top_db=30)
    
    # Calculate pauses
    pauses = []
    pause_count = 0
    longest_pause_seconds = 0.0
    
    # Iterate through the intervals of speech to find the gaps (pauses) between them
    for i in range(1, len(non_mute_intervals)):
        end_of_previous = non_mute_intervals[i-1][1]
        start_of_current = non_mute_intervals[i][0]
        
        # Gap in samples
        gap_samples = start_of_current - end_of_previous
        gap_seconds = gap_samples / sr
        
        # If the gap is longer than 0.5 seconds, we count it as a noticeable pause
        if gap_seconds > 0.5:
            pauses.append(gap_seconds)
            pause_count += 1
            if gap_seconds > longest_pause_seconds:
                longest_pause_seconds = gap_seconds
                
    # 4. Speaking Rate (Pace)
    # Count words in the transcript
    words = transcript_text.split()
    word_count = len(words)
    
    # Pace in words per minute
    # Avoid division by zero
    minutes = duration_seconds / 60.0
    words_per_minute = word_count / minutes if minutes > 0 else 0
    
    import re
    # 5. Filler Words (Regex word-boundary matching)
    filler_words_list = ["um", "uh", "like", "you know", "basically", "literally", "actually"]
    transcript_lower = transcript_text.lower()
    
    filler_word_count = 0
    for filler in filler_words_list:
        # Count occurrences using regex word boundaries to avoid false positives like "like" in "likely"
        matches = re.findall(r'\b' + re.escape(filler) + r'\b', transcript_lower)
        filler_word_count += len(matches)
        
    return {
        "words_per_minute": words_per_minute,
        "pause_count": pause_count,
        "longest_pause_seconds": longest_pause_seconds,
        "filler_word_count": filler_word_count,
        "duration_seconds": duration_seconds
    }
