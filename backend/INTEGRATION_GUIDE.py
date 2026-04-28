"""
===================================================================
INTEGRATION GUIDE - RECOMMENDATION SYSTEM
===================================================================

This file provides step-by-step instructions to integrate the
recommendation system into your existing Flask backend.

QUICK START:
1. Update requirements.txt (add any missing dependencies)
2. Update your app.py with the blueprint import
3. Test the new endpoints
4. Integrate with your frontend

"""

# ===================================================================
# STEP 1: UPDATE requirements.txt
# ===================================================================

"""
Your current requirements.txt should include:

Flask==2.3.0
Flask-CORS==4.0.0
scikit-learn==1.2.0
pandas==1.5.3
numpy==1.23.5

NO additional packages needed!
The recommendation system uses only: numpy, pandas (already included)
"""

# ===================================================================
# STEP 2: UPDATE YOUR app.py FILE
# ===================================================================

"""
Add this import at the top of your backend/app.py:

    from recommendation_api import recommendations_bp

Then register the blueprint after initializing your Flask app:

    # Initialize Flask app
    app = Flask(__name__)
    CORS(app)
    
    # Initialize database
    init_db()
    
    # === ADD THIS ===
    # Register recommendation system blueprint
    app.register_blueprint(recommendations_bp)
    # ================

This will automatically add all recommendation endpoints to your app.
"""

# ===================================================================
# STEP 3: TEST ENDPOINTS WITH CURL
# ===================================================================

"""
Test the main recommendation endpoint:

curl -X POST http://localhost:5000/api/recommendations/analyze \\
  -H "Content-Type: application/json" \\
  -d '{
    "current_price": 5000,
    "predicted_price": 5300,
    "worker_efficiency": 0.75,
    "stock_level": 1000,
    "daily_usage": 200
  }'

Expected Response:
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

Test enhanced scoring endpoint:

curl -X POST http://localhost:5000/api/recommendations/analyze-with-score \\
  -H "Content-Type: application/json" \\
  -d '{
    "current_price": 5000,
    "predicted_price": 5300,
    "worker_efficiency": 0.75,
    "stock_level": 1000,
    "daily_usage": 200
  }'

Expected Response:
{
  "success": true,
  "data": {
    "buy_decision": "Buy Now",
    "reorder_days": "Reorder Soon",
    "worker_suggestion": "Moderate efficiency – normal workload",
    "risk_level": "Medium",
    "score": 66.1,
    "days_until_stockout": 5.0,
    "price_trend": "Uptrend",
    "timestamp": "2026-04-25T22:50:00.000000"
  },
  "timestamp": "2026-04-25T22:50:00.000000"
}
"""

# ===================================================================
# STEP 4: AVAILABLE ENDPOINTS DOCUMENTATION
# ===================================================================

"""
After integration, you'll have these new endpoints:

1. MAIN ENDPOINTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POST /api/recommendations/analyze
  Purpose: Generate complete recommendations
  Input: current_price, predicted_price, worker_efficiency, stock_level, daily_usage
  Output: buy_decision, reorder_days, worker_suggestion, risk_level
  
POST /api/recommendations/analyze-with-score
  Purpose: Generate recommendations with scoring system
  Input: (same as above)
  Output: (same as above) + score, days_until_stockout, price_trend


2. SPECIFIC DECISION ENDPOINTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POST /api/recommendations/buy-decision
  Purpose: Get buy/wait decision
  Input: current_price, predicted_price
  Output: buy_decision ("Buy Now" or "Wait")

POST /api/recommendations/stock-status
  Purpose: Get stock reorder recommendation
  Input: stock_level, daily_usage
  Output: reorder_status, days_left

POST /api/recommendations/worker-efficiency
  Purpose: Get worker efficiency assessment
  Input: worker_efficiency (0-1 scale)
  Output: assessment, efficiency_score

POST /api/recommendations/risk-assessment
  Purpose: Get overall risk level
  Input: stock_level, daily_usage, predicted_price, current_price, worker_efficiency
  Output: risk_level


3. HEALTH CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GET /api/recommendations/health
  Purpose: Check if recommendation service is running
  Output: status, service, timestamp
"""

# ===================================================================
# STEP 5: FRONTEND INTEGRATION EXAMPLES (JavaScript/React)
# ===================================================================

"""
JavaScript Example - Fetch recommendation:

async function getRecommendations(params) {
  try {
    const response = await fetch('/api/recommendations/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        current_price: params.currentPrice,
        predicted_price: params.predictedPrice,
        worker_efficiency: params.workerEfficiency,
        stock_level: params.stockLevel,
        daily_usage: params.dailyUsage
      })
    });
    
    const data = await response.json();
    if (data.success) {
      return data.data;
    } else {
      console.error('Error:', data.error);
    }
  } catch (error) {
    console.error('Request failed:', error);
  }
}

// Usage in React component:
import React, { useState } from 'react';

function RecommendationComponent() {
  const [recommendation, setRecommendation] = useState(null);
  
  const handleGetRecommendation = async () => {
    const result = await getRecommendations({
      currentPrice: 5000,
      predictedPrice: 5300,
      workerEfficiency: 0.75,
      stockLevel: 1000,
      dailyUsage: 200
    });
    
    setRecommendation(result);
  };
  
  return (
    <div>
      <button onClick={handleGetRecommendation}>Get Recommendation</button>
      {recommendation && (
        <div>
          <p>Buy: {recommendation.buy_decision}</p>
          <p>Reorder: {recommendation.reorder_days}</p>
          <p>Worker: {recommendation.worker_suggestion}</p>
          <p>Risk: {recommendation.risk_level}</p>
        </div>
      )}
    </div>
  );
}
"""

# ===================================================================
# STEP 6: PYTHON CLIENT EXAMPLE
# ===================================================================

"""
If you need to call the API from Python:

import requests
import json

BASE_URL = "http://localhost:5000/api/recommendations"

def get_recommendation(current_price, predicted_price, worker_efficiency, 
                      stock_level, daily_usage):
    
    payload = {
        "current_price": current_price,
        "predicted_price": predicted_price,
        "worker_efficiency": worker_efficiency,
        "stock_level": stock_level,
        "daily_usage": daily_usage
    }
    
    response = requests.post(
        f"{BASE_URL}/analyze",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    return response.json()

# Example usage:
result = get_recommendation(5000, 5300, 0.75, 1000, 200)

if result['success']:
    print(f"Buy Decision: {result['data']['buy_decision']}")
    print(f"Reorder: {result['data']['reorder_days']}")
    print(f"Worker Suggestion: {result['data']['worker_suggestion']}")
    print(f"Risk Level: {result['data']['risk_level']}")
"""

# ===================================================================
# STEP 7: DATABASE INTEGRATION (OPTIONAL)
# ===================================================================

"""
If you want to store recommendations in the database, add this to db.py:

def save_recommendation_to_db(recommendation_data, user_id=None):
    '''Save recommendation to database for auditing/history.'''
    
    import sqlite3
    from datetime import datetime
    
    conn = sqlite3.connect('database/db.sqlite3')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            buy_decision TEXT,
            reorder_days TEXT,
            worker_suggestion TEXT,
            risk_level TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        INSERT INTO recommendations 
        (user_id, buy_decision, reorder_days, worker_suggestion, risk_level)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        user_id,
        recommendation_data.get('buy_decision'),
        recommendation_data.get('reorder_days'),
        recommendation_data.get('worker_suggestion'),
        recommendation_data.get('risk_level')
    ))
    
    conn.commit()
    conn.close()

Then in recommendation_api.py, after successful recommendation:

    from db import save_recommendation_to_db
    
    # Save recommendation
    save_recommendation_to_db(recommendations, user_id=request.remote_addr)
"""

# ===================================================================
# STEP 8: ERROR HANDLING & VALIDATION
# ===================================================================

"""
The API includes built-in validation:

1. Missing Fields: Returns 400 with descriptive error
2. Invalid Ranges: Returns 400 (e.g., worker_efficiency > 1)
3. Invalid Types: Returns 400
4. Server Errors: Returns 500 with error message

Example error response:
{
  "success": false,
  "error": "Missing required field: current_price"
}

{
  "success": false,
  "error": "worker_efficiency must be between 0 and 1"
}
"""

# ===================================================================
# STEP 9: DEPLOYMENT NOTES
# ===================================================================

"""
For production deployment:

1. Environment Variables:
   - Store API keys/config in .env file
   - Use python-dotenv to load them
   
2. Rate Limiting:
   - Consider adding Flask-Limiter for API rate limiting
   - Use: pip install Flask-Limiter
   
3. Caching:
   - For frequently requested recommendations, use Flask-Caching
   - Use: pip install Flask-Caching
   
4. Logging:
   - Add logging to track recommendation decisions
   - Example:
   
   import logging
   logger = logging.getLogger(__name__)
   logger.info(f"Recommendation generated: {recommendations}")
   
5. Monitoring:
   - Set up alerting for "High" risk recommendations
   - Consider sending notifications to project managers
   - Log all critical recommendations for audit trail
"""

# ===================================================================
# STEP 10: TESTING YOUR INTEGRATION
# ===================================================================

"""
Test script to verify integration (save as test_recommendations.py):

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    '''Test if service is running.'''
    response = requests.get(f"{BASE_URL}/api/recommendations/health")
    assert response.status_code == 200
    print("✓ Health check passed")

def test_analyze():
    '''Test main analyze endpoint.'''
    payload = {
        "current_price": 5000,
        "predicted_price": 5300,
        "worker_efficiency": 0.75,
        "stock_level": 1000,
        "daily_usage": 200
    }
    
    response = requests.post(
        f"{BASE_URL}/api/recommendations/analyze",
        json=payload
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    assert 'buy_decision' in data['data']
    print("✓ Analyze endpoint passed")

def test_buy_decision():
    '''Test buy decision endpoint.'''
    payload = {
        "current_price": 5000,
        "predicted_price": 5300
    }
    
    response = requests.post(
        f"{BASE_URL}/api/recommendations/buy-decision",
        json=payload
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    print("✓ Buy decision endpoint passed")

if __name__ == "__main__":
    print("Running recommendation system tests...")
    
    try:
        test_health()
        test_analyze()
        test_buy_decision()
        print("\\n✅ All tests passed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
"""

# ===================================================================
# COMPLETE WORKING EXAMPLE
# ===================================================================

if __name__ == "__main__":
    print(__doc__)
    print("\n" + "=" * 80)
    print("INTEGRATION GUIDE LOADED")
    print("=" * 80)
    print("\n✅ Follow the steps above to integrate the recommendation system.")
    print("\n📁 Files created:")
    print("   1. recommendation_system.py    - Core recommendation engine")
    print("   2. recommendation_api.py       - Flask API endpoints")
    print("   3. example_with_real_data.py   - Real data analysis example")
    print("   4. integration_guide.py        - This file (integration instructions)")
