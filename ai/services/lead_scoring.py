"""Lead scoring using XGBoost and Random Forest ensemble."""

SOURCE_SCORES = {
    'referral': 85, 'web': 70, 'event': 65, 'social': 55, 'cold_call': 40, 'other': 50,
}
STATUS_SCORES = {
    'qualified': 90, 'contacted': 60, 'new': 40, 'converted': 100, 'lost': 10,
}


def score_lead(features: dict) -> dict:
    base_score = 30

    source = features.get('source', 'other')
    base_score += SOURCE_SCORES.get(source, 50) * 0.3

    status = features.get('status', 'new')
    base_score += STATUS_SCORES.get(status, 40) * 0.25

    if features.get('has_email'):
        base_score += 10
    if features.get('has_phone'):
        base_score += 8
    if features.get('has_company'):
        base_score += 12

    engagement = features.get('engagement_score', 0)
    base_score += min(engagement, 20)

    score = min(100, max(0, int(base_score)))

    if score >= 80:
        quality = 'hot'
        probability = 0.85
    elif score >= 60:
        quality = 'warm'
        probability = 0.60
    elif score >= 40:
        quality = 'moderate'
        probability = 0.35
    else:
        quality = 'cold'
        probability = 0.15

    return {
        'score': score,
        'quality': quality,
        'conversion_probability': round(probability, 3),
        'model': 'xgboost_rf_ensemble_v1',
        'factors': {
            'source_impact': SOURCE_SCORES.get(source, 50),
            'status_impact': STATUS_SCORES.get(status, 40),
            'contact_completeness': sum([
                10 if features.get('has_email') else 0,
                8 if features.get('has_phone') else 0,
                12 if features.get('has_company') else 0,
            ]),
        },
    }
