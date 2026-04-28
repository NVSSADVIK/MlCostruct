"""
===================================================================
FLASK API INTEGRATION - RECOMMENDATION SYSTEM
===================================================================

This module provides Flask API endpoints for the recommendation system.
Integrate these endpoints into your existing Flask app.py

Usage:
    1. Import this module in your app.py
    2. Register the blueprint with your Flask app
    3. Use the endpoints to get recommendations
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import numpy as np
import os
import sys

# Import the recommendation system
from recommendation_system import RecommendationSystem

# Create Blueprint
recommendations_bp = Blueprint(
    'recommendations',
    __name__,
    url_prefix='/api/recommendations'
)

# Initialize recommendation system
rec_system = RecommendationSystem()


# ===================================================================
# ENDPOINTS
# ===================================================================

@recommendations_bp.route('/analyze', methods=['POST'])
def analyze_recommendation():
    """
    Main endpoint to generate recommendations.
    
    Expected JSON Input:
    {
        "current_price": 5000,
        "predicted_price": 5300,
        "worker_efficiency": 0.75,
        "stock_level": 1000,
        "daily_usage": 200
    }
    
    Returns:
    {
        "success": true,
        "data": {
            "buy_decision": "Buy Now",
            "reorder_days": "Reorder Soon",
            "worker_suggestion": "Moderate efficiency – normal workload",
            "risk_level": "Medium"
        },
        "timestamp": "2026-04-25T22:50:00.000000"
    }
    """
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['current_price', 'predicted_price', 'worker_efficiency', 
                         'stock_level', 'daily_usage']
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Extract parameters
        current_price = float(data['current_price'])
        predicted_price = float(data['predicted_price'])
        worker_efficiency = float(data['worker_efficiency'])
        stock_level = int(data['stock_level'])
        daily_usage = int(data['daily_usage'])
        
        # Validate ranges
        if worker_efficiency < 0 or worker_efficiency > 1:
            return jsonify({
                'success': False,
                'error': 'worker_efficiency must be between 0 and 1'
            }), 400
        
        if daily_usage <= 0:
            return jsonify({
                'success': False,
                'error': 'daily_usage must be positive'
            }), 400
        
        # Generate recommendations
        recommendations = rec_system.generate_recommendations(
            current_price,
            predicted_price,
            worker_efficiency,
            stock_level,
            daily_usage
        )
        
        return jsonify({
            'success': True,
            'data': recommendations,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@recommendations_bp.route('/analyze-with-score', methods=['POST'])
def analyze_recommendation_with_score():
    """
    Enhanced endpoint with recommendation scoring.
    
    Expected JSON Input: (same as /analyze endpoint)
    {
        "current_price": 5000,
        "predicted_price": 5300,
        "worker_efficiency": 0.75,
        "stock_level": 1000,
        "daily_usage": 200
    }
    
    Returns:
    {
        "success": true,
        "data": {
            "buy_decision": "Buy Now",
            "reorder_days": "Reorder Soon",
            "worker_suggestion": "Moderate efficiency – normal workload",
            "risk_level": "Medium",
            "score": 66.1,
            "days_until_stockout": 5.0,
            "price_trend": "Uptrend"
        },
        "timestamp": "2026-04-25T22:50:00.000000"
    }
    """
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['current_price', 'predicted_price', 'worker_efficiency', 
                         'stock_level', 'daily_usage']
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Extract parameters
        current_price = float(data['current_price'])
        predicted_price = float(data['predicted_price'])
        worker_efficiency = float(data['worker_efficiency'])
        stock_level = int(data['stock_level'])
        daily_usage = int(data['daily_usage'])
        
        # Validate ranges
        if worker_efficiency < 0 or worker_efficiency > 1:
            return jsonify({
                'success': False,
                'error': 'worker_efficiency must be between 0 and 1'
            }), 400
        
        if daily_usage <= 0:
            return jsonify({
                'success': False,
                'error': 'daily_usage must be positive'
            }), 400
        
        # Generate recommendations with score
        recommendations = rec_system.generate_recommendations_with_score(
            current_price,
            predicted_price,
            worker_efficiency,
            stock_level,
            daily_usage
        )
        
        return jsonify({
            'success': True,
            'data': recommendations,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@recommendations_bp.route('/buy-decision', methods=['POST'])
def get_buy_decision():
    """
    Get only buy/wait decision.
    
    Expected JSON Input:
    {
        "current_price": 5000,
        "predicted_price": 5300
    }
    
    Returns:
    {
        "success": true,
        "buy_decision": "Buy Now"
    }
    """
    try:
        data = request.json
        
        if not data or 'current_price' not in data or 'predicted_price' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing current_price or predicted_price'
            }), 400
        
        current_price = float(data['current_price'])
        predicted_price = float(data['predicted_price'])
        
        decision = rec_system.analyze_buy_decision(current_price, predicted_price)
        
        return jsonify({
            'success': True,
            'buy_decision': decision
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@recommendations_bp.route('/stock-status', methods=['POST'])
def get_stock_status():
    """
    Get stock reorder recommendation.
    
    Expected JSON Input:
    {
        "stock_level": 1000,
        "daily_usage": 200
    }
    
    Returns:
    {
        "success": true,
        "reorder_status": "Reorder Soon",
        "days_left": 5.0
    }
    """
    try:
        data = request.json
        
        if not data or 'stock_level' not in data or 'daily_usage' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing stock_level or daily_usage'
            }), 400
        
        stock_level = int(data['stock_level'])
        daily_usage = int(data['daily_usage'])
        
        if daily_usage <= 0:
            return jsonify({
                'success': False,
                'error': 'daily_usage must be positive'
            }), 400
        
        status = rec_system.analyze_stock_level(stock_level, daily_usage)
        days_left = stock_level / daily_usage if daily_usage > 0 else 0
        
        return jsonify({
            'success': True,
            'reorder_status': status,
            'days_left': round(days_left, 2)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@recommendations_bp.route('/worker-efficiency', methods=['POST'])
def get_worker_assessment():
    """
    Get worker efficiency assessment.
    
    Expected JSON Input:
    {
        "worker_efficiency": 0.75
    }
    
    Returns:
    {
        "success": true,
        "assessment": "Moderate efficiency – normal workload"
    }
    """
    try:
        data = request.json
        
        if not data or 'worker_efficiency' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing worker_efficiency'
            }), 400
        
        worker_efficiency = float(data['worker_efficiency'])
        
        if worker_efficiency < 0 or worker_efficiency > 1:
            return jsonify({
                'success': False,
                'error': 'worker_efficiency must be between 0 and 1'
            }), 400
        
        assessment = rec_system.analyze_worker_efficiency(worker_efficiency)
        
        return jsonify({
            'success': True,
            'assessment': assessment,
            'efficiency_score': round(worker_efficiency * 100, 1)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@recommendations_bp.route('/risk-assessment', methods=['POST'])
def get_risk_assessment():
    """
    Get overall risk level assessment.
    
    Expected JSON Input:
    {
        "stock_level": 1000,
        "daily_usage": 200,
        "predicted_price": 5300,
        "current_price": 5000,
        "worker_efficiency": 0.75
    }
    
    Returns:
    {
        "success": true,
        "risk_level": "Medium"
    }
    """
    try:
        data = request.json
        
        required_fields = ['stock_level', 'daily_usage', 'predicted_price', 
                         'current_price', 'worker_efficiency']
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        stock_level = int(data['stock_level'])
        daily_usage = int(data['daily_usage'])
        predicted_price = float(data['predicted_price'])
        current_price = float(data['current_price'])
        worker_efficiency = float(data['worker_efficiency'])
        
        if worker_efficiency < 0 or worker_efficiency > 1:
            return jsonify({
                'success': False,
                'error': 'worker_efficiency must be between 0 and 1'
            }), 400
        
        risk_level = rec_system.analyze_risk_level(
            stock_level, daily_usage, predicted_price, current_price, worker_efficiency
        )
        
        return jsonify({
            'success': True,
            'risk_level': risk_level
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@recommendations_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for recommendation system.
    """
    return jsonify({
        'status': 'OK',
        'service': 'Recommendation System',
        'timestamp': datetime.now().isoformat()
    }), 200


# ===================================================================
# HOW TO INTEGRATE INTO YOUR FLASK APP
# ===================================================================

"""
In your main app.py file, add:

    from recommendation_api import recommendations_bp
    
    # Register the blueprint
    app.register_blueprint(recommendations_bp)

This will add the following endpoints to your Flask application:

GET  /api/recommendations/health
POST /api/recommendations/analyze
POST /api/recommendations/analyze-with-score
POST /api/recommendations/buy-decision
POST /api/recommendations/stock-status
POST /api/recommendations/worker-efficiency
POST /api/recommendations/risk-assessment
"""
