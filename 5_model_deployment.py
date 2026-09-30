"""
Customer Segmentation - Model Deployment
Real-time customer segmentation API and prediction service
"""

import pandas as pd
import numpy as np
import joblib
from datetime import datetime
from typing import Dict, List, Union
import json
from pathlib import Path


class CustomerSegmentationModel:
    """Production-ready model for real-time customer segmentation"""
    
    def __init__(self, model_path=None, scaler_path=None, feature_names_path=None,
                 reference_date_path=None):
        """Load the model and the preprocessing metadata produced by training."""
        model_dir = Path(__file__).resolve().parent / "models"
        model_path = Path(model_path) if model_path else model_dir / "best_classifier.pkl"
        scaler_path = Path(scaler_path) if scaler_path else model_dir / "scaler.pkl"
        feature_names_path = Path(feature_names_path) if feature_names_path else model_dir / "feature_names.pkl"
        reference_date_path = Path(reference_date_path) if reference_date_path else model_dir / "reference_date.pkl"
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.feature_cols = joblib.load(feature_names_path)
            self.reference_date = pd.Timestamp(joblib.load(reference_date_path))
            print(f"✓ Model loaded successfully from {model_path}")
        except FileNotFoundError:
            print("⚠ Model artifacts not found. Run the supervised training pipeline first.")
            self.model = None
            self.scaler = None
            self.feature_cols = None
            self.reference_date = None
    
    def preprocess_customer_data(self, customer_data: Dict) -> pd.DataFrame:
        """
        Preprocess raw customer data into features
        
        Args:
            customer_data: Dictionary with customer information
            
        Returns:
            DataFrame with engineered features
        """
        # Create DataFrame from input
        df = pd.DataFrame([customer_data])
        
        # Feature Engineering
        current_year = 2024
        
        # Age
        if 'Year_Birth' in df.columns:
            df['Age'] = current_year - df['Year_Birth']
        
        # Total Spending
        spending_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 
                        'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
        if all(col in df.columns for col in spending_cols):
            df['Total_Spending'] = df[spending_cols].sum(axis=1)
        
        # Total Children
        if 'Kidhome' in df.columns and 'Teenhome' in df.columns:
            df['Total_Children'] = df['Kidhome'] + df['Teenhome']
        
        # Family Size
        if 'Total_Children' in df.columns:
            df['Family_Size'] = df['Total_Children'] + 1
            if 'Marital_Status' in df.columns:
                if df['Marital_Status'].iloc[0] in ['Married', 'Together']:
                    df['Family_Size'] += 1
        
        # Total Purchases
        purchase_cols = ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']
        if all(col in df.columns for col in purchase_cols):
            df['Total_Purchases'] = df[purchase_cols].sum(axis=1)
        
        # Total Campaigns Accepted
        campaign_cols = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 
                        'AcceptedCmp4', 'AcceptedCmp5']
        if all(col in df.columns for col in campaign_cols):
            df['Total_Campaigns_Accepted'] = df[campaign_cols].sum(axis=1)
        
        # Customer Days
        if 'Dt_Customer' in df.columns:
            df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], format='%d-%m-%Y')
            customer_date = pd.to_datetime(df['Dt_Customer'], format='%d-%m-%Y')
            df['Customer_Days'] = (self.reference_date - customer_date).dt.days.clip(lower=0)
        
        # Derived Features
        if 'Total_Spending' in df.columns and 'Total_Purchases' in df.columns:
            df['Avg_Purchase_Value'] = df['Total_Spending'] / (df['Total_Purchases'] + 1)
        
        if 'Total_Spending' in df.columns and 'Customer_Days' in df.columns:
            df['Spending_Per_Day'] = df['Total_Spending'] / (df['Customer_Days'] + 1)
        
        if 'Income' in df.columns and 'Family_Size' in df.columns:
            df['Income_Per_Member'] = df['Income'] / df['Family_Size']
        
        # Education Level
        if 'Education' in df.columns:
            education_map = {'Basic': 1, '2n Cycle': 2, 'Graduation': 3, 'Master': 4, 'PhD': 5}
            df['Education_Level'] = df['Education'].map(education_map)
        
        # Has Partner
        if 'Marital_Status' in df.columns:
            df['Has_Partner'] = df['Marital_Status'].isin(['Married', 'Together']).astype(int)
        
        # Web Activity Score
        if 'NumWebPurchases' in df.columns and 'NumWebVisitsMonth' in df.columns:
            df['Web_Activity_Score'] = (df['NumWebPurchases'] * 2 + df['NumWebVisitsMonth']) / 3
        
        # Deal Sensitivity
        if 'NumDealsPurchases' in df.columns and 'Total_Purchases' in df.columns:
            df['Deal_Sensitivity'] = df['NumDealsPurchases'] / (df['Total_Purchases'] + 1)
        
        # Product Diversity
        if all(col in df.columns for col in spending_cols):
            df['Product_Diversity'] = (df[spending_cols] > 0).sum(axis=1)
        
        # Response Rate
        if 'Total_Campaigns_Accepted' in df.columns:
            df['Response_Rate'] = df['Total_Campaigns_Accepted'] / 5
        
        return df
    
    def predict_segment(self, customer_data: Dict) -> Dict:
        """
        Predict customer segment with confidence scores
        
        Args:
            customer_data: Dictionary with customer information
            
        Returns:
            Dictionary with segment prediction and probabilities
        """
        if self.model is None or self.scaler is None:
            return {"error": "Model not loaded"}
        
        # Preprocess data
        df = self.preprocess_customer_data(customer_data)
        
        # Select features for prediction
        # Use the exact feature ordering captured during model training.
        X = df[self.feature_cols].fillna(0)
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Predict
        segment = self.model.predict(X_scaled)[0]
        probabilities = self.model.predict_proba(X_scaled)[0]
        
        # Get segment name
        segment_names = {
            0: "Budget Conscious",
            1: "High Value",
            2: "Average Spender",
            3: "Premium Customer"
        }
        
        result = {
            "customer_id": customer_data.get('ID', 'Unknown'),
            "segment": int(segment),
            "segment_name": segment_names.get(segment, f"Segment {segment}"),
            "confidence": float(probabilities[segment]),
            "probabilities": {f"Segment {i}": float(prob) for i, prob in enumerate(probabilities)},
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def batch_predict(self, customers_data: List[Dict]) -> List[Dict]:
        """
        Predict segments for multiple customers
        
        Args:
            customers_data: List of customer dictionaries
            
        Returns:
            List of prediction results
        """
        results = []
        for customer in customers_data:
            result = self.predict_segment(customer)
            results.append(result)
        return results
    
    def save_prediction_log(self, predictions: List[Dict], filepath='prediction_log.json'):
        """Save predictions to log file"""
        with open(filepath, 'a') as f:
            for pred in predictions:
                f.write(json.dumps(pred) + '\n')
        print(f"✓ Predictions logged to {filepath}")


# Flask API for deployment (optional)
def create_api():
    """Create Flask API for model deployment"""
    try:
        from flask import Flask, request, jsonify
        
        app = Flask(__name__)
        model_service = CustomerSegmentationModel()
        
        @app.route('/predict', methods=['POST'])
        def predict():
            """Endpoint for single customer prediction"""
            try:
                customer_data = request.json
                result = model_service.predict_segment(customer_data)
                return jsonify(result)
            except Exception as e:
                return jsonify({"error": str(e)}), 400
        
        @app.route('/batch_predict', methods=['POST'])
        def batch_predict():
            """Endpoint for batch predictions"""
            try:
                customers_data = request.json
                results = model_service.batch_predict(customers_data)
                return jsonify(results)
            except Exception as e:
                return jsonify({"error": str(e)}), 400
        
        @app.route('/health', methods=['GET'])
        def health():
            """Health check endpoint"""
            return jsonify({"status": "healthy", "model_loaded": model_service.model is not None})
        
        return app
    
    except ImportError:
        print("Flask not installed. Install with: pip install flask")
        return None


if __name__ == "__main__":
    # Example usage
    print("="*70)
    print("CUSTOMER SEGMENTATION MODEL DEPLOYMENT")
    print("="*70)
    
    # Initialize model
    model_service = CustomerSegmentationModel()
    
    # Example customer data
    example_customer = {
        'ID': 12345,
        'Year_Birth': 1980,
        'Education': 'Graduation',
        'Marital_Status': 'Married',
        'Income': 50000,
        'Kidhome': 1,
        'Teenhome': 1,
        'Dt_Customer': '01-01-2020',
        'Recency': 30,
        'MntWines': 200,
        'MntFruits': 50,
        'MntMeatProducts': 150,
        'MntFishProducts': 80,
        'MntSweetProducts': 40,
        'MntGoldProds': 30,
        'NumDealsPurchases': 3,
        'NumWebPurchases': 5,
        'NumCatalogPurchases': 2,
        'NumStorePurchases': 8,
        'NumWebVisitsMonth': 6,
        'AcceptedCmp1': 0,
        'AcceptedCmp2': 0,
        'AcceptedCmp3': 0,
        'AcceptedCmp4': 0,
        'AcceptedCmp5': 1
    }
    
    # Make prediction
    if model_service.model is not None:
        result = model_service.predict_segment(example_customer)
        print("\nPrediction Result:")
        print(json.dumps(result, indent=2))
        
        # To start Flask API (uncomment):
        # app = create_api()
        # if app:
        #     app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("\n⚠ Please train the model first by running the notebook.")
