"""
ML Model for price prediction and recommendations
"""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import json


class PricePredictor:
    """Predicts cement prices using linear regression"""
    
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def train(self, historical_prices):
        """
        Train the model on historical price data
        Args:
            historical_prices: list of past prices
        """
        if len(historical_prices) < 2:
            return False
            
        X = np.array([[i] for i in range(len(historical_prices))])
        y = np.array(historical_prices)
        
        self.model.fit(X, y)
        self.is_trained = True
        return True
    
    def predict_next_7_days(self, historical_prices):
        """
        Predict next 7 days of cement prices
        Args:
            historical_prices: list of past prices (at least 2 values)
        Returns:
            list of 7 predicted prices
        """
        if len(historical_prices) < 2:
            # Return sample predictions if insufficient data
            current_price = historical_prices[0] if historical_prices else 5000
            return [current_price + i * 50 for i in range(7)]
        
        self.train(historical_prices)
        
        # Predict next 7 days
        future_days = np.array([[len(historical_prices) + i] for i in range(7)])
        predictions = self.model.predict(future_days)
        
        return predictions.tolist()


class RecommendationEngine:
    """Generates buy/wait decisions and resource allocation suggestions"""
    
    @staticmethod
    def analyze_price_trend(current_price, predicted_prices):
        """
        Analyze if price will increase or decrease
        Returns: 'uptrend', 'downtrend', or 'stable'
        """
        avg_predicted = np.mean(predicted_prices)
        
        if avg_predicted > current_price * 1.05:
            return 'uptrend'
        elif avg_predicted < current_price * 0.95:
            return 'downtrend'
        else:
            return 'stable'
    
    @staticmethod
    def calculate_risk_level(stock_level, daily_usage, efficiency_score, price_trend):
        """
        Calculate risk level based on multiple factors
        Returns: 'Low', 'Medium', 'High'
        """
        risk_score = 0
        
        # Stock risk (0-50 points)
        days_of_stock = stock_level / (daily_usage + 0.01)
        if days_of_stock < 7:
            risk_score += 50
        elif days_of_stock < 14:
            risk_score += 30
        elif days_of_stock < 30:
            risk_score += 10
        
        # Worker efficiency risk (0-30 points)
        if efficiency_score < 50:
            risk_score += 30
        elif efficiency_score < 70:
            risk_score += 15
        
        # Price trend risk (0-20 points)
        if price_trend == 'uptrend':
            risk_score += 20
        elif price_trend == 'downtrend':
            risk_score -= 5
        
        # Normalize risk score
        risk_score = max(0, min(100, risk_score))
        
        if risk_score > 60:
            return 'High'
        elif risk_score > 30:
            return 'Medium'
        else:
            return 'Low'
    
    @staticmethod
    def get_buy_decision(current_price, predicted_prices, stock_level, daily_usage, price_trend):
        """
        Decide whether to buy cement now or wait
        Returns: 'Buy Now', 'Wait', or 'Emergency Buy'
        """
        days_of_stock = stock_level / (daily_usage + 0.01)
        avg_predicted = np.mean(predicted_prices)
        
        # Emergency situation
        if days_of_stock < 3:
            return 'Emergency Buy'
        
        # Price going up and low stock
        if price_trend == 'uptrend' and days_of_stock < 14:
            return 'Buy Now'
        
        # Downtrend - can wait
        if price_trend == 'downtrend' and days_of_stock > 14:
            return 'Wait'
        
        # Stock is good and prices stable
        if days_of_stock > 21:
            return 'Wait'
        
        # Stock running low regardless of price
        if days_of_stock < 10:
            return 'Buy Now'
        
        return 'Wait'
    
    @staticmethod
    def get_reorder_suggestion(stock_level, daily_usage, current_price, predicted_prices):
        """
        Calculate optimal reorder level and timing
        Returns: suggestion string
        """
        days_of_stock = stock_level / (daily_usage + 0.01)
        avg_predicted = np.mean(predicted_prices)
        
        # Calculate safe stock level (15 days of usage)
        safe_stock_level = daily_usage * 15
        
        if stock_level < safe_stock_level:
            reorder_days = max(1, int((safe_stock_level - stock_level) / daily_usage))
            return f"Reorder in {reorder_days} day(s). Target level: {int(safe_stock_level)} units"
        else:
            return f"Stock is adequate. Current level: {int(stock_level)} units. Can use for ~{int(days_of_stock)} days"
    
    @staticmethod
    def get_worker_allocation(efficiency_scores, num_workers):
        """
        Suggest worker allocation based on efficiency
        Returns: suggestion string
        """
        if not efficiency_scores:
            return f"Allocate all {num_workers} workers to ongoing projects"
        
        avg_efficiency = np.mean(efficiency_scores)
        
        if avg_efficiency < 50:
            return f"Allocate {num_workers} skilled workers. Current efficiency is low - prioritize training"
        elif avg_efficiency < 70:
            return f"Allocate {max(1, num_workers - 2)} experienced + {min(2, num_workers)} trainee workers"
        else:
            return f"Allocate all {num_workers} workers. Efficiency is good - consider increasing workload"
    
    @classmethod
    def generate_recommendation(cls, current_price, predicted_prices, stock_level, 
                              daily_usage, efficiency_scores, num_workers):
        """
        Generate complete recommendation
        Returns: dict with all recommendations
        """
        price_trend = cls.analyze_price_trend(current_price, predicted_prices)
        avg_efficiency = np.mean(efficiency_scores) if efficiency_scores else 60
        
        risk_level = cls.calculate_risk_level(
            stock_level, daily_usage, avg_efficiency, price_trend
        )
        
        buy_decision = cls.get_buy_decision(
            current_price, predicted_prices, stock_level, daily_usage, price_trend
        )
        
        reorder_suggestion = cls.get_reorder_suggestion(
            stock_level, daily_usage, current_price, predicted_prices
        )
        
        worker_suggestion = cls.get_worker_allocation(efficiency_scores, num_workers)
        
        return {
            'buy_decision': buy_decision,
            'reorder_suggestion': reorder_suggestion,
            'worker_plan': worker_suggestion,
            'risk': risk_level,
            'price_trend': price_trend,
            'avg_efficiency': round(avg_efficiency, 2),
            'days_of_stock': round(stock_level / (daily_usage + 0.01), 1)
        }
