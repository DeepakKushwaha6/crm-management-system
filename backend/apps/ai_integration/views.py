import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ai'))

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.permissions import IsReadOnlyOrAbove
from core.thread_locals import get_current_organization
from apps.crm.models import Lead, Customer, Opportunity
from apps.crm.serializers import LeadSerializer, CustomerSerializer


class LeadScoreView(APIView):
    permission_classes = [IsReadOnlyOrAbove]

    def post(self, request):
        from services.lead_scoring import score_lead

        lead_id = request.data.get('lead_id')
        org = get_current_organization()

        if lead_id:
            try:
                lead = Lead.objects.get(id=lead_id, organization=org)
                features = {
                    'source': lead.source,
                    'status': lead.status,
                    'has_email': bool(lead.email),
                    'has_phone': bool(lead.phone),
                    'has_company': bool(lead.company),
                }
                result = score_lead(features)
                lead.score = result['score']
                lead.save(update_fields=['score'])
                return Response({**result, 'lead': LeadSerializer(lead).data})
            except Lead.DoesNotExist:
                return Response({'error': 'Lead not found'}, status=404)

        features = request.data.get('features', request.data)
        result = score_lead(features)
        return Response(result)


class ChurnPredictView(APIView):
    permission_classes = [IsReadOnlyOrAbove]

    def post(self, request):
        from services.churn_prediction import predict_churn

        customer_id = request.data.get('customer_id')
        org = get_current_organization()

        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id, organization=org)
                opp_count = Opportunity.objects.filter(customer=customer).count()
                won_count = Opportunity.objects.filter(customer=customer, stage='won').count()
                features = {
                    'lifetime_value': float(customer.lifetime_value),
                    'status': customer.status,
                    'opportunity_count': opp_count,
                    'won_deals': won_count,
                    'days_since_created': (customer.updated_at - customer.created_at).days,
                }
                result = predict_churn(features)
                customer.churn_risk = result['churn_risk']
                customer.save(update_fields=['churn_risk'])
                return Response({**result, 'customer': CustomerSerializer(customer).data})
            except Customer.DoesNotExist:
                return Response({'error': 'Customer not found'}, status=404)

        result = predict_churn(request.data.get('features', request.data))
        return Response(result)


class RevenueForecastView(APIView):
    permission_classes = [IsReadOnlyOrAbove]

    def post(self, request):
        from services.revenue_forecast import forecast_revenue
        from django.db.models import Sum
        from django.utils import timezone
        from datetime import timedelta

        org = get_current_organization()
        period = request.data.get('period', 'monthly')

        historical = []
        now = timezone.now()
        for i in range(12):
            month = now.month - i
            year = now.year
            while month <= 0:
                month += 12
                year -= 1
            start = now.replace(year=year, month=month, day=1)
            revenue = Opportunity.objects.filter(
                organization=org, stage='won', won_at__gte=start,
            ).aggregate(total=Sum('amount'))['total'] or 0
            historical.append(float(revenue))

        pipeline = float(
            Opportunity.objects.filter(organization=org)
            .exclude(stage__in=['won', 'lost'])
            .aggregate(total=Sum('amount'))['total'] or 0
        )

        result = forecast_revenue(historical, pipeline, period)
        return Response(result)


class FollowUpRecommendationView(APIView):
    permission_classes = [IsReadOnlyOrAbove]

    def post(self, request):
        from services.follow_up import recommend_follow_up

        result = recommend_follow_up(request.data)
        return Response(result)


class EmailGeneratorView(APIView):
    permission_classes = [IsReadOnlyOrAbove]

    def post(self, request):
        from services.email_generator import generate_email

        email_type = request.data.get('type', 'follow_up')
        context = request.data.get('context', {})
        result = generate_email(email_type, context)
        return Response(result)


class SentimentAnalysisView(APIView):
    permission_classes = [IsReadOnlyOrAbove]

    def post(self, request):
        from services.sentiment import analyze_sentiment

        text = request.data.get('text', '')
        if not text:
            return Response({'error': 'Text is required'}, status=400)
        result = analyze_sentiment(text)
        return Response(result)
