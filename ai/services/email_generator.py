"""AI email generation service."""

TEMPLATES = {
    'follow_up': {
        'subject': 'Following up on our conversation',
        'body': '''Dear {name},

I hope this email finds you well. I wanted to follow up on our recent conversation regarding {topic}.

{custom_message}

Please let me know if you have any questions or if there is a convenient time for us to connect.

Best regards,
{sender}''',
    },
    'sales': {
        'subject': 'Transform your {industry} operations with CRM AI PRO',
        'body': '''Dear {name},

I noticed that {company} is doing great work in the {industry} space. I believe our AI-powered CRM platform could help you:

• Increase conversion rates by up to 40%
• Reduce manual data entry with intelligent automation
• Predict customer churn before it happens

Would you be open to a 15-minute demo this week?

Best regards,
{sender}''',
    },
    'meeting_request': {
        'subject': 'Meeting Request: {topic}',
        'body': '''Dear {name},

I would like to schedule a meeting to discuss {topic}.

Proposed times:
• {time_option_1}
• {time_option_2}

Please let me know which works best for you, or suggest an alternative.

Best regards,
{sender}''',
    },
    'proposal': {
        'subject': 'Proposal for {company} - CRM AI PRO',
        'body': '''Dear {name},

Thank you for the opportunity to present our proposal for {company}.

Please find attached our detailed proposal outlining:
• Implementation timeline
• Pricing and packages
• Expected ROI

I am available to walk through the proposal at your convenience.

Best regards,
{sender}''',
    },
}


def generate_email(email_type: str, context: dict) -> dict:
    template = TEMPLATES.get(email_type, TEMPLATES['follow_up'])

    defaults = {
        'name': 'Valued Customer',
        'company': 'your organization',
        'industry': 'your industry',
        'topic': 'our partnership',
        'sender': 'Sales Team',
        'custom_message': 'I wanted to check in and see how things are progressing.',
        'time_option_1': 'Tuesday at 2:00 PM',
        'time_option_2': 'Thursday at 10:00 AM',
    }
    defaults.update(context)

    try:
        subject = template['subject'].format(**defaults)
        body = template['body'].format(**defaults)
    except KeyError:
        subject = template['subject']
        body = template['body']

    return {
        'type': email_type,
        'subject': subject,
        'body': body,
        'model': 'email_generator_v1',
    }
