"""AI follow-up recommendation engine."""

CHANNELS = ['email', 'phone', 'meeting', 'linkedin']
ACTIONS = {
    'new': {'action': 'Send introduction email', 'channel': 'email', 'timing_days': 0},
    'contacted': {'action': 'Schedule discovery call', 'channel': 'phone', 'timing_days': 2},
    'qualified': {'action': 'Send proposal meeting invite', 'channel': 'meeting', 'timing_days': 1},
    'proposal': {'action': 'Follow up on proposal', 'channel': 'email', 'timing_days': 3},
    'negotiation': {'action': 'Executive check-in call', 'channel': 'phone', 'timing_days': 1},
    'active': {'action': 'Quarterly business review', 'channel': 'meeting', 'timing_days': 7},
    'inactive': {'action': 'Re-engagement email campaign', 'channel': 'email', 'timing_days': 0},
}


def recommend_follow_up(data: dict) -> dict:
    entity_type = data.get('entity_type', 'lead')
    status = data.get('status', 'new')
    last_contact_days = data.get('days_since_last_contact', 7)
    score = int(data.get('score', 50))

    template = ACTIONS.get(status, ACTIONS['new'])

    if last_contact_days > 14:
        timing_days = 0
        urgency = 'high'
    elif last_contact_days > 7:
        timing_days = 1
        urgency = 'medium'
    else:
        timing_days = template['timing_days']
        urgency = 'low'

    if score >= 80:
        channel = 'phone' if template['channel'] == 'email' else template['channel']
        urgency = 'high'
    else:
        channel = template['channel']

    return {
        'recommended_action': template['action'],
        'best_channel': channel,
        'timing_days': timing_days,
        'urgency': urgency,
        'message_template': _get_template(entity_type, status, channel),
        'model': 'recommendation_engine_v1',
    }


def _get_template(entity_type, status, channel):
    templates = {
        ('lead', 'new', 'email'): 'Hi {name}, thank you for your interest in our solutions...',
        ('lead', 'qualified', 'meeting'): 'Hi {name}, I would like to schedule a meeting to discuss your requirements...',
        ('customer', 'active', 'meeting'): 'Hi {name}, I wanted to schedule our quarterly business review...',
        ('customer', 'inactive', 'email'): 'Hi {name}, we miss working with you. Here are some updates...',
    }
    return templates.get(
        (entity_type, status, channel),
        f'Hi {{name}}, following up regarding your {entity_type}...'
    )
