"""
===================================================================
PRACTICAL EXAMPLE - RECOMMENDATION SYSTEM WITH REAL DATA
===================================================================

This module demonstrates how to use the recommendation system with
your actual datasets (cement.csv, supply_chain.csv, and 
construction_project_performance_dataset.csv).

It includes:
1. Loading and analyzing real data
2. Computing metrics from the datasets
3. Generating recommendations based on real scenarios
4. Batch processing for historical analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Import the recommendation system
from recommendation_system import RecommendationSystem


class DataAnalyzer:
    """
    Analyzes construction project datasets for recommendation system.
    """
    
    def __init__(self, base_path: str):
        """
        Initialize the data analyzer.
        
        Args:
            base_path (str): Path to the project root directory
        """
        self.base_path = Path(base_path)
        self.cement_df = None
        self.supply_chain_df = None
        self.performance_df = None
        
    def load_all_datasets(self) -> bool:
        """
        Load all three datasets.
        
        Returns:
            bool: True if all datasets loaded successfully
        """
        try:
            # Load cement price data
            cement_path = self.base_path / "cement data.csv"
            if cement_path.exists():
                self.cement_df = pd.read_csv(cement_path)
                print(f"✓ Loaded cement data: {len(self.cement_df)} records")
            else:
                print(f"✗ Cement data file not found: {cement_path}")
            
            # Load supply chain data
            supply_path = self.base_path / "supply_chain.csv"
            if supply_path.exists():
                self.supply_chain_df = pd.read_csv(supply_path)
                print(f"✓ Loaded supply chain data: {len(self.supply_chain_df)} records")
            else:
                print(f"✗ Supply chain data file not found: {supply_path}")
            
            # Load performance data
            perf_path = self.base_path / "construction_project_performance_dataset.csv"
            if perf_path.exists():
                self.performance_df = pd.read_csv(perf_path)
                print(f"✓ Loaded performance data: {len(self.performance_df)} records")
            else:
                print(f"✗ Performance data file not found: {perf_path}")
            
            return all([self.cement_df is not None, 
                       self.supply_chain_df is not None,
                       self.performance_df is not None])
            
        except Exception as e:
            print(f"Error loading datasets: {e}")
            return False
    
    def analyze_cement_prices(self) -> dict:
        """
        Analyze cement price trends from the dataset.
        
        Returns:
            dict: Price analysis metrics
        """
        if self.cement_df is None:
            return {}
        
        try:
            # Clean data
            df = self.cement_df.copy()
            
            # Try to extract sales as price indicator (if not explicit price column)
            sales_col = 'Sales ' if 'Sales ' in df.columns else 'Sales'
            
            if sales_col in df.columns:
                prices = df[sales_col].dropna()
                
                analysis = {
                    'current_price': float(prices.iloc[-1]),
                    'average_price': float(prices.mean()),
                    'min_price': float(prices.min()),
                    'max_price': float(prices.max()),
                    'price_std': float(prices.std()),
                    'price_trend': 'Uptrend' if prices.iloc[-1] > prices.mean() else 'Downtrend',
                    'records': len(prices)
                }
                
                # Simple prediction: linear extrapolation
                x = np.arange(len(prices))
                y = prices.values
                z = np.polyfit(x, y, 1)
                predicted = z[0] + z[1] * (len(prices) + 1)
                analysis['predicted_price'] = float(predicted)
                
                return analysis
            
        except Exception as e:
            print(f"Error analyzing cement prices: {e}")
        
        return {}
    
    def analyze_supply_chain(self) -> dict:
        """
        Analyze supply chain metrics from the dataset.
        
        Returns:
            dict: Supply chain metrics
        """
        if self.supply_chain_df is None:
            return {}
        
        try:
            df = self.supply_chain_df.copy()
            
            analysis = {
                'total_inventory_level': int(df['Inventory_Level'].sum()),
                'avg_inventory_level': float(df['Inventory_Level'].mean()),
                'min_inventory_level': int(df['Inventory_Level'].min()),
                'max_inventory_level': int(df['Inventory_Level'].max()),
                'total_units_sold': int(df['Units_Sold'].sum()),
                'avg_units_sold_daily': float(df['Units_Sold'].mean()),
                'avg_lead_time_days': float(df['Supplier_Lead_Time_Days'].mean()),
                'stockout_incidents': int(df['Stockout_Flag'].sum()),
                'records': len(df)
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing supply chain: {e}")
        
        return {}
    
    def analyze_worker_performance(self) -> dict:
        """
        Analyze worker performance and efficiency from the dataset.
        
        Returns:
            dict: Worker performance metrics
        """
        if self.performance_df is None:
            return {}
        
        try:
            df = self.performance_df.copy()
            
            # Calculate average metrics
            avg_worker_count = float(df['Worker_Count'].mean())
            avg_task_progress = float(df['Task_Progress (%)'].mean()) / 100  # Convert to 0-1 scale
            avg_resource_util = float(df['Resource_Utilization (%)'].mean()) / 100
            total_safety_incidents = int(df['Safety_Incidents'].sum())
            avg_risk_score = float(df['Risk_Score'].mean())
            
            # Estimate worker efficiency (higher progress = higher efficiency)
            # Normalized to 0-1 scale
            worker_efficiency = min(1.0, max(0.0, avg_task_progress))
            
            analysis = {
                'avg_worker_count': int(avg_worker_count),
                'avg_task_progress': round(avg_task_progress * 100, 2),
                'avg_resource_utilization': round(avg_resource_util * 100, 2),
                'worker_efficiency_score': round(worker_efficiency, 2),
                'total_safety_incidents': total_safety_incidents,
                'avg_risk_score': round(avg_risk_score, 2),
                'records': len(df)
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing worker performance: {e}")
        
        return {}


def demonstrate_real_data_analysis():
    """
    Demonstrate the recommendation system using real project data.
    """
    
    print("=" * 80)
    print("RECOMMENDATION SYSTEM - REAL DATA ANALYSIS")
    print("=" * 80)
    
    # Get the project base path
    base_path = Path(__file__).parent.parent
    
    print(f"\n📂 Loading data from: {base_path}")
    
    # Initialize analyzer
    analyzer = DataAnalyzer(str(base_path))
    
    # Load datasets
    print("\n📥 Loading datasets...")
    if not analyzer.load_all_datasets():
        print("\n⚠️  Could not load all datasets. Some analysis may be limited.")
    
    # Analyze datasets
    print("\n" + "=" * 80)
    print("📊 DATASET ANALYSIS")
    print("=" * 80)
    
    cement_analysis = analyzer.analyze_cement_prices()
    supply_analysis = analyzer.analyze_supply_chain()
    worker_analysis = analyzer.analyze_worker_performance()
    
    # Display cement price analysis
    if cement_analysis:
        print("\n💰 CEMENT PRICE ANALYSIS:")
        print(f"  • Current Price: ₹{cement_analysis['current_price']:.2f}")
        print(f"  • Predicted Price: ₹{cement_analysis['predicted_price']:.2f}")
        print(f"  • Average Price: ₹{cement_analysis['average_price']:.2f}")
        print(f"  • Price Range: ₹{cement_analysis['min_price']:.2f} - ₹{cement_analysis['max_price']:.2f}")
        print(f"  • Trend: {cement_analysis['price_trend']}")
        print(f"  • Historical Records: {cement_analysis['records']}")
    
    # Display supply chain analysis
    if supply_analysis:
        print("\n📦 SUPPLY CHAIN ANALYSIS:")
        print(f"  • Current Inventory: {supply_analysis['total_inventory_level']} units")
        print(f"  • Average Inventory: {supply_analysis['avg_inventory_level']:.0f} units")
        print(f"  • Average Daily Sales: {supply_analysis['avg_units_sold_daily']:.2f} units")
        print(f"  • Supplier Lead Time: {supply_analysis['avg_lead_time_days']:.1f} days")
        print(f"  • Stockout Incidents: {supply_analysis['stockout_incidents']}")
        print(f"  • Historical Records: {supply_analysis['records']}")
    
    # Display worker performance analysis
    if worker_analysis:
        print("\n👷 WORKER PERFORMANCE ANALYSIS:")
        print(f"  • Average Worker Count: {worker_analysis['avg_worker_count']} workers")
        print(f"  • Efficiency Score: {worker_analysis['worker_efficiency_score']:.1%}")
        print(f"  • Task Progress: {worker_analysis['avg_task_progress']:.2f}%")
        print(f"  • Resource Utilization: {worker_analysis['avg_resource_utilization']:.2f}%")
        print(f"  • Safety Incidents: {worker_analysis['total_safety_incidents']}")
        print(f"  • Average Risk Score: {worker_analysis['avg_risk_score']:.2f}/100")
        print(f"  • Historical Records: {worker_analysis['records']}")
    
    # Generate recommendations based on real data
    print("\n" + "=" * 80)
    print("🎯 RECOMMENDATIONS BASED ON REAL DATA")
    print("=" * 80)
    
    if cement_analysis and supply_analysis and worker_analysis:
        # Initialize recommendation system
        rec_system = RecommendationSystem()
        
        # Prepare inputs
        current_price = cement_analysis.get('current_price', 5000)
        predicted_price = cement_analysis.get('predicted_price', 5000)
        stock_level = supply_analysis.get('total_inventory_level', 5000)
        daily_usage = supply_analysis.get('avg_units_sold_daily', 200)
        worker_efficiency = worker_analysis.get('worker_efficiency_score', 0.7)
        
        print(f"\n📥 Input Parameters (from real data):")
        print(f"  • Current Price: ₹{current_price:.2f}")
        print(f"  • Predicted Price: ₹{predicted_price:.2f}")
        print(f"  • Stock Level: {stock_level} units")
        print(f"  • Daily Usage: {daily_usage:.2f} units")
        print(f"  • Worker Efficiency: {worker_efficiency:.2%}")
        
        # Generate recommendations
        recommendations = rec_system.generate_recommendations_with_score(
            current_price, predicted_price, worker_efficiency, stock_level, int(daily_usage)
        )
        
        print(f"\n📋 RECOMMENDATION REPORT:")
        print(f"  • Buy Decision: {recommendations['buy_decision']}")
        print(f"  • Reorder Status: {recommendations['reorder_days']}")
        print(f"  • Worker Suggestion: {recommendations['worker_suggestion']}")
        print(f"  • Risk Level: {recommendations['risk_level']}")
        print(f"  • Urgency Score: {recommendations['score']}/100")
        print(f"  • Days Until Stockout: {recommendations['days_until_stockout']:.1f} days")
        print(f"  • Price Trend: {recommendations['price_trend']}")
        
        # Action items based on risk level
        print(f"\n⚡ ACTION ITEMS:")
        risk_level = recommendations['risk_level']
        
        if risk_level == 'High':
            print("  🔴 IMMEDIATE ACTION REQUIRED:")
            print("     - Place emergency cement order immediately")
            print("     - Review worker allocation and training")
            print("     - Activate contingency supply chain protocols")
        
        elif risk_level == 'Medium':
            print("  🟡 CAREFUL MONITORING REQUIRED:")
            print("     - Schedule cement order for next week")
            print("     - Monitor price movements closely")
            print("     - Conduct worker efficiency review")
            print("     - Prepare contingency plans")
        
        else:  # Low risk
            print("  🟢 SITUATION STABLE:")
            print("     - Continue normal operations")
            print("     - Monitor price trends for buying opportunities")
            print("     - Maintain current worker allocation")
            print("     - Schedule routine maintenance")
    
    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 80)


def batch_analysis_example():
    """
    Example of batch processing for historical analysis.
    """
    print("\n\n" + "=" * 80)
    print("BATCH ANALYSIS - HISTORICAL RECOMMENDATIONS")
    print("=" * 80)
    
    rec_system = RecommendationSystem()
    
    # Simulate multiple scenarios
    scenarios = [
        {
            'name': 'Week 1 - Normal Operations',
            'current_price': 5000,
            'predicted_price': 5050,
            'stock_level': 2000,
            'daily_usage': 150,
            'worker_efficiency': 0.8
        },
        {
            'name': 'Week 2 - Price Increase Alert',
            'current_price': 5050,
            'predicted_price': 5500,
            'stock_level': 1200,
            'daily_usage': 150,
            'worker_efficiency': 0.75
        },
        {
            'name': 'Week 3 - Stock Critical',
            'current_price': 5500,
            'predicted_price': 5450,
            'stock_level': 400,
            'daily_usage': 150,
            'worker_efficiency': 0.65
        },
        {
            'name': 'Week 4 - Recovery',
            'current_price': 5450,
            'predicted_price': 5300,
            'stock_level': 3000,
            'daily_usage': 150,
            'worker_efficiency': 0.85
        }
    ]
    
    print("\nProcessing 4 weeks of historical data:\n")
    
    for scenario in scenarios:
        print(f"📅 {scenario['name']}")
        print("-" * 70)
        
        rec = rec_system.generate_recommendations_with_score(
            scenario['current_price'],
            scenario['predicted_price'],
            scenario['worker_efficiency'],
            scenario['stock_level'],
            scenario['daily_usage']
        )
        
        print(f"  Price: ₹{scenario['current_price']} → ₹{scenario['predicted_price']} ({rec['price_trend']})")
        print(f"  Stock: {scenario['stock_level']} units ({rec['days_until_stockout']} days)")
        print(f"  Efficiency: {scenario['worker_efficiency']:.0%}")
        print(f"  📊 Score: {rec['score']}/100 | Risk: {rec['risk_level']}")
        print(f"  ✓ {rec['buy_decision']} | {rec['reorder_days']}")
        print()


if __name__ == "__main__":
    # Run real data analysis
    demonstrate_real_data_analysis()
    
    # Run batch analysis example
    batch_analysis_example()
