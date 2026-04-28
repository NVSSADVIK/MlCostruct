"""
Flask Backend for Smart Construction Recommendation System
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

from model import PricePredictor, RecommendationEngine
from db import (
    init_db, save_price_history, get_recent_prices, 
    save_recommendation, get_recommendation_history, 
    save_metrics, get_latest_metrics
)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize database
init_db()

# Initialize ML models
price_predictor = PricePredictor()


# ============== UTILITY ROUTES ==============

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'OK', 'message': 'Backend is running'})


# ============== PRICE PREDICTION ROUTES ==============

@app.route('/api/predict_price', methods=['POST'])
def predict_price():
    """
    Predict next 7 days of cement prices
    Expected input: { "historical_prices": [5000, 5100, 5050, ...] }
    """
    try:
        data = request.json
        historical_prices = data.get('historical_prices', [])
        
        if not historical_prices:
            return jsonify({'error': 'Historical prices required'}), 400
        
        # Convert to float
        historical_prices = [float(p) for p in historical_prices]
        
        # Get predictions
        predictions = price_predictor.predict_next_7_days(historical_prices)
        
        # Create response with dates
        today = datetime.now()
        forecast = []
        for i, price in enumerate(predictions):
            date = (today + timedelta(days=i)).strftime('%Y-%m-%d')
            forecast.append({
                'date': date,
                'predicted_price': round(float(price), 2)
            })
        
        return jsonify({
            'status': 'success',
            'current_price': round(float(historical_prices[-1]), 2),
            'forecast': forecast,
            'average_predicted': round(np.mean(predictions), 2)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/get_price_history', methods=['GET'])
def get_price_history():
    """Get recent price history"""
    try:
        prices = get_recent_prices(days=30)
        
        # If no data in DB, return sample data
        if not prices:
            prices = [5000 + i * 50 for i in range(20)]
        
        # Create dates
        today = datetime.now()
        history = []
        for i, price in enumerate(prices[-20:]):  # Last 20 days
            date = (today - timedelta(days=20-i)).strftime('%Y-%m-%d')
            history.append({'date': date, 'price': price})
        
        return jsonify({
            'status': 'success',
            'history': history,
            'current_price': round(prices[-1], 2)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============== RECOMMENDATION ROUTES ==============

@app.route('/api/recommend', methods=['POST'])
def get_recommendation():
    """
    Generate recommendations
    Expected input: {
        "current_price": 5000,
        "historical_prices": [4900, 5000, 5050],
        "stock_level": 10000,
        "daily_usage": 500,
        "worker_efficiency": [65, 70, 75],
        "num_workers": 15
    }
    """
    try:
        data = request.json
        
        # Validate required fields
        required_fields = [
            'current_price', 'historical_prices', 'stock_level', 
            'daily_usage', 'num_workers'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Extract and validate data
        current_price = float(data['current_price'])
        historical_prices = [float(p) for p in data['historical_prices']]
        stock_level = float(data['stock_level'])
        daily_usage = float(data['daily_usage'])
        num_workers = int(data['num_workers'])
        
        # Worker efficiency - can be array or single value
        efficiency_data = data.get('worker_efficiency', [60, 70, 65])
        if isinstance(efficiency_data, (int, float)):
            worker_efficiency = [float(efficiency_data)]
        else:
            worker_efficiency = [float(e) for e in efficiency_data]
        
        # Predict prices
        predicted_prices = price_predictor.predict_next_7_days(historical_prices)
        
        # Generate recommendation
        recommendation = RecommendationEngine.generate_recommendation(
            current_price=current_price,
            predicted_prices=predicted_prices,
            stock_level=stock_level,
            daily_usage=daily_usage,
            efficiency_scores=worker_efficiency,
            num_workers=num_workers
        )
        
        # Save to database
        save_recommendation({
            'current_price': current_price,
            'stock_level': stock_level,
            'daily_usage': daily_usage,
            'buy_decision': recommendation['buy_decision'],
            'risk_level': recommendation['risk'],
            'worker_plan': recommendation['worker_plan'],
            'reorder_suggestion': recommendation['reorder_suggestion']
        })
        
        # Save metrics
        avg_efficiency = np.mean(worker_efficiency)
        save_metrics(avg_efficiency, num_workers, 'Active')
        
        # Add predicted prices to response
        recommendation['predicted_prices'] = [round(p, 2) for p in predicted_prices]
        
        return jsonify({
            'status': 'success',
            'recommendation': recommendation
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/recommendation_history', methods=['GET'])
def recommendation_history():
    """Get recommendation history"""
    try:
        history = get_recommendation_history(limit=10)
        return jsonify({
            'status': 'success',
            'history': history
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============== DASHBOARD ROUTES ==============

@app.route('/api/dashboard_summary', methods=['GET'])
def dashboard_summary():
    """Get dashboard summary data"""
    try:
        # Get price data
        prices = get_recent_prices(days=30)
        if not prices:
            prices = [5000 + i * 50 for i in range(20)]
        
        current_price = prices[-1]
        
        # Predict next 7 days
        predicted_prices = price_predictor.predict_next_7_days(prices[-7:])
        avg_predicted = np.mean(predicted_prices)
        
        # Get latest metrics
        metrics = get_latest_metrics()
        if not metrics:
            metrics = {
                'worker_efficiency': 68,
                'num_workers': 15,
                'project_status': 'Active'
            }
        
        # Sample stock levels (in real app, would get from DB)
        stock_level = 15000
        daily_usage = 500
        days_of_stock = stock_level / daily_usage
        
        return jsonify({
            'status': 'success',
            'current_price': round(current_price, 2),
            'predicted_price_7d': round(avg_predicted, 2),
            'price_trend': 'up' if avg_predicted > current_price else 'down',
            'worker_efficiency': round(metrics['worker_efficiency'], 1),
            'num_workers': metrics['num_workers'],
            'stock_level': stock_level,
            'daily_usage': daily_usage,
            'days_of_stock': round(days_of_stock, 1),
            'project_status': metrics['project_status']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============== ERROR HANDLERS ==============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='127.0.0.1', port=5000)
