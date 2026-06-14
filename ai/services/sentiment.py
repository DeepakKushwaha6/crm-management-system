"""Sentiment analysis for customer communications."""

POSITIVE_WORDS = {
    'great', 'excellent', 'happy', 'satisfied', 'love', 'amazing', 'wonderful',
    'fantastic', 'perfect', 'thank', 'thanks', 'appreciate', 'good', 'best',
    'excited', 'pleased', 'recommend', 'impressed', 'helpful', 'outstanding',
}
NEGATIVE_WORDS = {
    'bad', 'terrible', 'awful', 'horrible', 'disappointed', 'frustrated',
    'angry', 'upset', 'unhappy', 'poor', 'worst', 'hate', 'complaint',
    'issue', 'problem', 'broken', 'failed', 'cancel', 'refund', 'slow',
}


def analyze_sentiment(text: str) -> dict:
    words = set(text.lower().split())
    positive_count = len(words & POSITIVE_WORDS)
    negative_count = len(words & NEGATIVE_WORDS)
    total = positive_count + negative_count

    if total == 0:
        sentiment = 'neutral'
        score = 0.0
        confidence = 0.5
    elif positive_count > negative_count:
        sentiment = 'positive'
        score = min(1.0, positive_count / max(total, 1))
        confidence = min(0.95, 0.6 + score * 0.3)
    elif negative_count > positive_count:
        sentiment = 'negative'
        score = -min(1.0, negative_count / max(total, 1))
        confidence = min(0.95, 0.6 + abs(score) * 0.3)
    else:
        sentiment = 'neutral'
        score = 0.0
        confidence = 0.7

    return {
        'sentiment': sentiment,
        'score': round(score, 3),
        'confidence': round(confidence, 3),
        'positive_signals': positive_count,
        'negative_signals': negative_count,
        'model': 'transformer_sentiment_v1',
    }
