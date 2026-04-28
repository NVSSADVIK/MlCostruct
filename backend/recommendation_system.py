"""
===================================================================
RECOMMENDATION SYSTEM MODULE
Smart Construction Management - Intelligent Decision Making
===================================================================

This module provides intelligent recommendations for construction
management based on cement pricing, worker efficiency, and stock levels.

Features:
- Buy/Wait decision based on price trends
- Optimal reorder timing and quantities
- Worker efficiency insights
- Risk assessment and scoring
- Integrated scoring system for refined recommendations
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional


class RecommendationSystem:
    """
    Core recommendation engine for construction management.
    
    Provides intelligent recommendations for:
    - Cement purchasing decisions
    - Stock reordering
    - Worker allocation
    - Risk assessment
    """
    
    def __init__(self, price_sensitivity: float = 0.05, 
                 min_safe_stock_days: int = 7):
        """
        Initialize the recommendation system.
        
        Args:
            price_sensitivity (float): Percentage change threshold for price trends (default 0.05 = 5%)
            min_safe_stock_days (int): Minimum days of stock to maintain (default 7)
        """
        self.price_sensitivity = price_sensitivity
        self.min_safe_stock_days = min_safe_stock_days
    
    # ===========================
    # 1. BUY DECISION LOGIC
    # ===========================
    
    def analyze_buy_decision(self, 
                           current_price: float, 
                           predicted_price: float) -> str:
        """
        Determine whether to buy cement now or wait.
        
        Logic:
        - IF predicted_price > current_price: "Buy Now"
        - ELSE: "Wait"
        
        Args:
            current_price (float): Current cement price
            predicted_price (float): Predicted future cement price
            
        Returns:
            str: "Buy Now" or "Wait"
        """
        if predicted_price > current_price:
            return "Buy Now"
        else:
            return "Wait"
    
    # ===========================
    # 2. STOCK REORDER LOGIC
    # ===========================
    
    def analyze_stock_level(self, 
                          stock_level: int, 
                          daily_usage: int) -> str:
        """
        Determine optimal reorder timing based on stock level.
        
        Logic:
        - days_left = stock_level / daily_usage
        - IF days_left < 3: "Urgent Reorder"
        - ELIF days_left < 7: "Reorder Soon"
        - ELSE: "Stock is Sufficient"
        
        Args:
            stock_level (int): Current stock quantity
            daily_usage (int): Average daily consumption
            
        Returns:
            str: Reorder recommendation
        """
        # Avoid division by zero
        if daily_usage <= 0:
            return "Stock is Sufficient"
        
        days_left = stock_level / daily_usage
        
        if days_left < 3:
            return "Urgent Reorder"
        elif days_left < 7:
            return "Reorder Soon"
        else:
            return "Stock is Sufficient"
    
    # ===========================
    # 3. WORKER EFFICIENCY LOGIC
    # ===========================
    
    def analyze_worker_efficiency(self, worker_efficiency: float) -> str:
        """
        Evaluate worker efficiency and provide recommendations.
        
        Logic:
        - IF efficiency > 0.8: "High efficiency team – assign critical tasks"
        - ELIF efficiency > 0.5: "Moderate efficiency – normal workload"
        - ELSE: "Low efficiency – training recommended"
        
        Args:
            worker_efficiency (float): Efficiency score (0-1 scale)
            
        Returns:
            str: Worker recommendation
        """
        if worker_efficiency > 0.8:
            return "High efficiency team – assign critical tasks"
        elif worker_efficiency > 0.5:
            return "Moderate efficiency – normal workload"
        else:
            return "Low efficiency – training recommended"
    
    # ===========================
    # 4. RISK LEVEL LOGIC
    # ===========================
    
    def analyze_risk_level(self, 
                         stock_level: int, 
                         daily_usage: int,
                         predicted_price: float,
                         current_price: float,
                         worker_efficiency: float) -> str:
        """
        Calculate overall risk level using multiple factors.
        
        Risk Assessment:
        - High risk: low stock AND rising price
        - Medium risk: moderate stock OR moderate efficiency
        - Low risk: good stock AND stable price
        
        Args:
            stock_level (int): Current stock quantity
            daily_usage (int): Average daily consumption
            predicted_price (float): Predicted future price
            current_price (float): Current price
            worker_efficiency (float): Worker efficiency (0-1 scale)
            
        Returns:
            str: Risk level ("Low", "Medium", or "High")
        """
        # Calculate days of stock remaining
        days_left = stock_level / daily_usage if daily_usage > 0 else float('inf')
        
        # Determine price trend
        is_price_rising = predicted_price > current_price
        
        # High Risk Conditions
        if days_left < 3 and is_price_rising:
            return "High"
        
        if days_left < 5 and worker_efficiency < 0.5:
            return "High"
        
        # Medium Risk Conditions
        if (days_left < 7 and is_price_rising) or \
           (days_left < 10 and worker_efficiency < 0.6) or \
           (3 <= days_left < 10 and is_price_rising):
            return "Medium"
        
        # Low Risk - otherwise
        return "Low"
    
    # ===========================
    # 5. SCORING SYSTEM
    # ===========================
    
    def calculate_recommendation_score(self,
                                      current_price: float,
                                      predicted_price: float,
                                      stock_level: int,
                                      daily_usage: int,
                                      worker_efficiency: float) -> float:
        """
        Calculate a composite recommendation score (0-100 scale).
        
        Scoring Formula:
        score = (predicted_price - current_price) * 0.5
              + (1 / days_left) * 0.3
              + (1 - worker_efficiency) * 0.2
        
        Normalized to 0-100 scale where:
        - Higher score = higher urgency for action
        
        Args:
            current_price (float): Current cement price
            predicted_price (float): Predicted cement price
            stock_level (int): Current stock quantity
            daily_usage (int): Average daily consumption
            worker_efficiency (float): Worker efficiency (0-1 scale)
            
        Returns:
            float: Recommendation score (0-100)
        """
        # Price component (50% weight)
        # Normalized by current price to make it scale-invariant
        price_component = ((predicted_price - current_price) / max(current_price, 1)) * 0.5
        
        # Stock component (30% weight)
        # Reciprocal of days left normalized
        days_left = max(1, stock_level / max(daily_usage, 1))
        stock_component = (1 / days_left) * 0.3
        
        # Efficiency component (20% weight)
        efficiency_component = (1 - worker_efficiency) * 0.2
        
        # Calculate raw score
        raw_score = price_component + stock_component + efficiency_component
        
        # Normalize to 0-100 scale
        # Using a sigmoid-like normalization
        normalized_score = 50 + (raw_score * 100)
        normalized_score = max(0, min(100, normalized_score))
        
        return round(normalized_score, 2)
    
    # ===========================
    # 6. MAIN RECOMMENDATION ENGINE
    # ===========================
    
    def generate_recommendations(self,
                               current_price: float,
                               predicted_price: float,
                               worker_efficiency: float,
                               stock_level: int,
                               daily_usage: int) -> Dict[str, str]:
        """
        Generate complete set of recommendations.
        
        This is the main entry point for the recommendation system.
        It analyzes all factors and returns structured recommendations.
        
        Args:
            current_price (float): Current cement price
            predicted_price (float): Predicted cement price
            worker_efficiency (float): Worker efficiency (0-1 scale)
            stock_level (int): Current stock quantity
            daily_usage (int): Average daily consumption
            
        Returns:
            Dict[str, str]: Dictionary containing:
                - buy_decision (str): "Buy Now" or "Wait"
                - reorder_days (str): Reorder timing recommendation
                - worker_suggestion (str): Worker allocation recommendation
                - risk_level (str): Overall risk assessment
        """
        # Input validation
        if daily_usage <= 0:
            raise ValueError("daily_usage must be positive")
        if worker_efficiency < 0 or worker_efficiency > 1:
            raise ValueError("worker_efficiency must be between 0 and 1")
        
        # Generate individual recommendations
        buy_decision = self.analyze_buy_decision(current_price, predicted_price)
        reorder_days = self.analyze_stock_level(stock_level, daily_usage)
        worker_suggestion = self.analyze_worker_efficiency(worker_efficiency)
        risk_level = self.analyze_risk_level(
            stock_level, daily_usage, predicted_price, current_price, worker_efficiency
        )
        
        # Return structured recommendation
        recommendation = {
            "buy_decision": buy_decision,
            "reorder_days": reorder_days,
            "worker_suggestion": worker_suggestion,
            "risk_level": risk_level
        }
        
        return recommendation
    
    def generate_recommendations_with_score(self,
                                           current_price: float,
                                           predicted_price: float,
                                           worker_efficiency: float,
                                           stock_level: int,
                                           daily_usage: int) -> Dict:
        """
        Generate recommendations with enhanced scoring system.
        
        This extends generate_recommendations() by adding a scoring
        mechanism for refined decision making.
        
        Args:
            current_price (float): Current cement price
            predicted_price (float): Predicted cement price
            worker_efficiency (float): Worker efficiency (0-1 scale)
            stock_level (int): Current stock quantity
            daily_usage (int): Average daily consumption
            
        Returns:
            Dict: Extended recommendation dictionary including score
        """
        # Get base recommendations
        recommendations = self.generate_recommendations(
            current_price, predicted_price, worker_efficiency, stock_level, daily_usage
        )
        
        # Calculate recommendation score
        score = self.calculate_recommendation_score(
            current_price, predicted_price, stock_level, daily_usage, worker_efficiency
        )
        
        # Add additional context metrics
        days_left = stock_level / daily_usage if daily_usage > 0 else 0
        price_trend = "Uptrend" if predicted_price > current_price else "Downtrend"
        
        # Add metadata
        recommendations["score"] = score
        recommendations["days_until_stockout"] = round(days_left, 2)
        recommendations["price_trend"] = price_trend
        recommendations["timestamp"] = datetime.now().isoformat()
        
        return recommendations
    
    # ===========================
    # 7. DATA LOADING UTILITIES
    # ===========================
    
    @staticmethod
    def load_cement_data(filepath: str) -> Optional[pd.DataFrame]:
        """
        Load cement pricing data from CSV.
        
        Args:
            filepath (str): Path to cement data CSV file
            
        Returns:
            pd.DataFrame: Loaded cement data or None if error
        """
        try:
            df = pd.read_csv(filepath)
            return df
        except Exception as e:
            print(f"Error loading cement data: {e}")
            return None
    
    @staticmethod
    def load_supply_chain_data(filepath: str) -> Optional[pd.DataFrame]:
        """
        Load supply chain data from CSV.
        
        Args:
            filepath (str): Path to supply chain CSV file
            
        Returns:
            pd.DataFrame: Loaded supply chain data or None if error
        """
        try:
            df = pd.read_csv(filepath)
            return df
        except Exception as e:
            print(f"Error loading supply chain data: {e}")
            return None
    
    @staticmethod
    def load_performance_data(filepath: str) -> Optional[pd.DataFrame]:
        """
        Load project performance data from CSV.
        
        Args:
            filepath (str): Path to performance dataset CSV file
            
        Returns:
            pd.DataFrame: Loaded performance data or None if error
        """
        try:
            df = pd.read_csv(filepath)
            return df
        except Exception as e:
            print(f"Error loading performance data: {e}")
            return None


# ===================================================================
# SAMPLE TEST CASES
# ===================================================================

def test_recommendation_system():
    """
    Comprehensive test suite for the recommendation system.
    
    Tests all major functions with various scenarios.
    """
    
    print("=" * 70)
    print("RECOMMENDATION SYSTEM - TEST SUITE")
    print("=" * 70)
    
    # Initialize the system
    rec_system = RecommendationSystem()
    
    # =============================================
    # TEST CASE 1: Price Rising - Low Stock
    # =============================================
    print("\n[TEST 1] Price Rising - Low Stock (High Risk Scenario)")
    print("-" * 70)
    
    current_price_1 = 5000.0
    predicted_price_1 = 5500.0  # Price rising
    worker_efficiency_1 = 0.75
    stock_level_1 = 500  # Low stock
    daily_usage_1 = 200
    
    print(f"Current Price: ₹{current_price_1}")
    print(f"Predicted Price: ₹{predicted_price_1}")
    print(f"Worker Efficiency: {worker_efficiency_1} (75%)")
    print(f"Stock Level: {stock_level_1} units")
    print(f"Daily Usage: {daily_usage_1} units")
    print(f"Days Left: {stock_level_1 / daily_usage_1:.1f} days")
    
    rec_1 = rec_system.generate_recommendations(
        current_price_1, predicted_price_1, worker_efficiency_1, stock_level_1, daily_usage_1
    )
    
    print("\nRecommendations:")
    print(f"  • Buy Decision: {rec_1['buy_decision']}")
    print(f"  • Reorder Status: {rec_1['reorder_days']}")
    print(f"  • Worker Suggestion: {rec_1['worker_suggestion']}")
    print(f"  • Risk Level: {rec_1['risk_level']}")
    
    # =============================================
    # TEST CASE 2: Price Stable - Good Stock
    # =============================================
    print("\n[TEST 2] Price Stable - Good Stock (Low Risk Scenario)")
    print("-" * 70)
    
    current_price_2 = 5000.0
    predicted_price_2 = 5000.0  # Price stable
    worker_efficiency_2 = 0.9
    stock_level_2 = 3000  # Good stock
    daily_usage_2 = 200
    
    print(f"Current Price: ₹{current_price_2}")
    print(f"Predicted Price: ₹{predicted_price_2}")
    print(f"Worker Efficiency: {worker_efficiency_2} (90%)")
    print(f"Stock Level: {stock_level_2} units")
    print(f"Daily Usage: {daily_usage_2} units")
    print(f"Days Left: {stock_level_2 / daily_usage_2:.1f} days")
    
    rec_2 = rec_system.generate_recommendations(
        current_price_2, predicted_price_2, worker_efficiency_2, stock_level_2, daily_usage_2
    )
    
    print("\nRecommendations:")
    print(f"  • Buy Decision: {rec_2['buy_decision']}")
    print(f"  • Reorder Status: {rec_2['reorder_days']}")
    print(f"  • Worker Suggestion: {rec_2['worker_suggestion']}")
    print(f"  • Risk Level: {rec_2['risk_level']}")
    
    # =============================================
    # TEST CASE 3: Price Falling - Moderate Stock
    # =============================================
    print("\n[TEST 3] Price Falling - Moderate Stock (Medium Risk Scenario)")
    print("-" * 70)
    
    current_price_3 = 5000.0
    predicted_price_3 = 4500.0  # Price falling
    worker_efficiency_3 = 0.65
    stock_level_3 = 1000
    daily_usage_3 = 200
    
    print(f"Current Price: ₹{current_price_3}")
    print(f"Predicted Price: ₹{predicted_price_3}")
    print(f"Worker Efficiency: {worker_efficiency_3} (65%)")
    print(f"Stock Level: {stock_level_3} units")
    print(f"Daily Usage: {daily_usage_3} units")
    print(f"Days Left: {stock_level_3 / daily_usage_3:.1f} days")
    
    rec_3 = rec_system.generate_recommendations(
        current_price_3, predicted_price_3, worker_efficiency_3, stock_level_3, daily_usage_3
    )
    
    print("\nRecommendations:")
    print(f"  • Buy Decision: {rec_3['buy_decision']}")
    print(f"  • Reorder Status: {rec_3['reorder_days']}")
    print(f"  • Worker Suggestion: {rec_3['worker_suggestion']}")
    print(f"  • Risk Level: {rec_3['risk_level']}")
    
    # =============================================
    # TEST CASE 4: SCORING SYSTEM TEST
    # =============================================
    print("\n[TEST 4] Scoring System Comparison")
    print("-" * 70)
    
    scenarios = [
        ("Critical", 5000, 5500, 0.3, 300, 200),
        ("Urgent", 5000, 5300, 0.6, 500, 200),
        ("Moderate", 5000, 5000, 0.7, 1500, 200),
        ("Comfortable", 5000, 4800, 0.85, 3000, 200),
    ]
    
    print(f"{'Scenario':<15} {'Price Trend':<15} {'Stock Days':<15} {'Score':<10} {'Interpretation':<20}")
    print("-" * 75)
    
    for scenario_name, curr_p, pred_p, eff, stock, daily in scenarios:
        score = rec_system.calculate_recommendation_score(curr_p, pred_p, stock, daily, eff)
        price_trend = "↑ Rising" if pred_p > curr_p else ("→ Stable" if pred_p == curr_p else "↓ Falling")
        days = f"{stock/daily:.1f}"
        
        if score > 70:
            interpretation = "CRITICAL ACTION"
        elif score > 50:
            interpretation = "URGENT REVIEW"
        elif score > 30:
            interpretation = "MONITOR CLOSELY"
        else:
            interpretation = "STABLE"
        
        print(f"{scenario_name:<15} {price_trend:<15} {days:<15} {score:<10.1f} {interpretation:<20}")
    
    # =============================================
    # TEST CASE 5: WITH SCORE ENHANCEMENT
    # =============================================
    print("\n[TEST 5] Full Recommendation with Enhanced Scoring")
    print("-" * 70)
    
    current_price_5 = 5000.0
    predicted_price_5 = 5300.0
    worker_efficiency_5 = 0.72
    stock_level_5 = 800
    daily_usage_5 = 200
    
    rec_5 = rec_system.generate_recommendations_with_score(
        current_price_5, predicted_price_5, worker_efficiency_5, stock_level_5, daily_usage_5
    )
    
    print(f"Current Price: ₹{current_price_5}")
    print(f"Predicted Price: ₹{predicted_price_5}")
    print(f"Worker Efficiency: {worker_efficiency_5} (72%)")
    print(f"Stock Level: {stock_level_5} units")
    print(f"Daily Usage: {daily_usage_5} units")
    
    print("\n📊 Comprehensive Recommendation Report:")
    print(f"  • Buy Decision: {rec_5['buy_decision']}")
    print(f"  • Reorder Status: {rec_5['reorder_days']}")
    print(f"  • Worker Suggestion: {rec_5['worker_suggestion']}")
    print(f"  • Risk Level: {rec_5['risk_level']}")
    print(f"  • Recommendation Score: {rec_5['score']}/100")
    print(f"  • Days Until Stockout: {rec_5['days_until_stockout']} days")
    print(f"  • Price Trend: {rec_5['price_trend']}")
    print(f"  • Generated: {rec_5['timestamp']}")
    
    # =============================================
    # TEST CASE 6: EDGE CASES
    # =============================================
    print("\n[TEST 6] Edge Cases Testing")
    print("-" * 70)
    
    print("\n6a. Very Low Efficiency (0.2)")
    rec_6a = rec_system.generate_recommendations(5000, 5000, 0.2, 1000, 200)
    print(f"  Worker Suggestion: {rec_6a['worker_suggestion']}")
    print(f"  Risk Level: {rec_6a['risk_level']}")
    
    print("\n6b. Critical Stock (1 day left)")
    rec_6b = rec_system.generate_recommendations(5000, 5000, 0.8, 200, 200)
    print(f"  Reorder Status: {rec_6b['reorder_days']}")
    print(f"  Risk Level: {rec_6b['risk_level']}")
    
    print("\n6c. Price Spike (20% increase)")
    rec_6c = rec_system.generate_recommendations(5000, 6000, 0.7, 1500, 200)
    print(f"  Buy Decision: {rec_6c['buy_decision']}")
    print(f"  Risk Level: {rec_6c['risk_level']}")
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    # Run comprehensive tests
    test_recommendation_system()
