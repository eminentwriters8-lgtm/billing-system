# AI REVENUE PREDICTION SYSTEM
# Copyright (c) 2025 Martin Mutinda

import json
from datetime import datetime, timedelta
from django.http import JsonResponse

class RevenuePredictor:
    def __init__(self):
        self.historical_data = []
        
    def predict_revenue(self, periods=6):
        """Predict future revenue using trend analysis"""
        # Simple linear regression for prediction
        # In production, replace with ML model
        recent_data = self.get_recent_revenue()
        
        if len(recent_data) < 3:
            return self._get_default_prediction()
            
        # Calculate trend
        growth_rate = self._calculate_growth_rate(recent_data)
        predictions = []
        
        last_amount = recent_data[-1]['amount']
        for i in range(periods):
            predicted_amount = last_amount * (1 + growth_rate) ** (i + 1)
            predictions.append({
                'month': (datetime.now() + timedelta(days=30*(i+1))).strftime('%b %Y'),
                'predicted': round(predicted_amount),
                'confidence': max(0.7 - (i * 0.1), 0.3)  # Decreasing confidence
            })
            
        return predictions
        
    def _calculate_growth_rate(self, data):
        """Calculate average monthly growth rate"""
        if len(data) < 2:
            return 0.05  # Default 5% growth
            
        rates = []
        for i in range(1, len(data)):
            growth = (data[i]['amount'] - data[i-1]['amount']) / data[i-1]['amount']
            rates.append(growth)
            
        return sum(rates) / len(rates)
        
    def get_recent_revenue(self):
        """Get recent revenue data for analysis"""
        # Mock data - replace with actual database queries
        return [
            {'month': 'Jul 2025', 'amount': 485000},
            {'month': 'Aug 2025', 'amount': 512000},
            {'month': 'Sep 2025', 'amount': 538000},
            {'month': 'Oct 2025', 'amount': 562000},
        ]
        
    def _get_default_prediction(self):
        """Fallback prediction"""
        return [
            {'month': 'Nov 2025', 'predicted': 589000, 'confidence': 0.6},
            {'month': 'Dec 2025', 'predicted': 618000, 'confidence': 0.55},
        ]

class ClientChurnPredictor:
    def __init__(self):
        self.risk_factors = ['payment_delays', 'low_usage', 'support_tickets', 'price_sensitivity']
        
    def predict_churn_risk(self, client_data):
        """Predict client churn risk"""
        risk_score = 0
        
        # Analyze payment history
        if client_data.get('late_payments', 0) > 2:
            risk_score += 30
            
        # Usage patterns
        if client_data.get('usage_decline', 0) > 0.4:  # 40% decline
            risk_score += 25
            
        # Support interactions
        if client_data.get('support_tickets', 0) > 5:
            risk_score += 20
            
        # Competitor activity in area
        if client_data.get('competitor_presence', False):
            risk_score += 25
            
        return min(risk_score, 100)

revenue_predictor = RevenuePredictor()
churn_predictor = ClientChurnPredictor()
