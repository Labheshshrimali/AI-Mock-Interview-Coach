def calculate_analytics(sessions):
    if not sessions:
        return {
            "avg_score": 0,
            "best_score": 0,
            "worst_score": 0,
            "total_sessions": 0
        }
    
    scores = []
    for s in sessions:
        # Calculate overall score (average of content components * 10)
        overall = (s["scores"]["relevance_score"] + s["scores"]["completeness_score"] + s["scores"]["structure_score"]) / 3 * 10
        scores.append(overall)
        
    return {
        "avg_score": round(sum(scores) / len(scores), 1),
        "best_score": round(max(scores), 1),
        "worst_score": round(min(scores), 1),
        "total_sessions": len(sessions)
    }
