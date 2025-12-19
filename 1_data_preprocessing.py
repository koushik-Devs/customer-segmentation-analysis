"""
Customer Personality Segmentation - Data Preprocessing & Feature Engineering
This module handles data cleaning, feature engineering, and preparation
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DataPreprocessor:
    """Handles all data preprocessing and feature engineering"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.df_processed = None
        
    def load_data(self):
        """Load the dataset"""
        print("Loading data...")
        self.df = pd.read_csv(self.filepath, sep='\t')
        print(f"Data loaded: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        return self.df
    
    def explore_data(self):
        """Basic data exploration"""
        print("\n" + "="*50)
        print("DATA EXPLORATION")
        print("="*50)
        print(f"\nDataset Shape: {self.df.shape}")
        print(f"\nColumn Names:\n{self.df.columns.tolist()}")
        print(f"\nData Types:\n{self.df.dtypes}")
        print(f"\nMissing Values:\n{self.df.isnull().sum()}")
        print(f"\nBasic Statistics:\n{self.df.describe()}")
        
    def handle_missing_values(self):
        """Handle missing values intelligently"""
        print("\n" + "="*50)
        print("HANDLING MISSING VALUES")
        print("="*50)
        
        # Income: Fill with median
        if self.df['Income'].isnull().sum() > 0:
            median_income = self.df['Income'].median()
            self.df['Income'].fillna(median_income, inplace=True)
            print(f"Filled {self.df['Income'].isnull().sum()} missing Income values with median: {median_income}")
        
        print("Missing values handled successfully!")
        
    def create_features(self):
        """Create new meaningful features"""
        print("\n" + "="*50)
        print("FEATURE ENGINEERING")
        print("="*50)
        
        # 1. Age from Year_Birth
        current_year = 2024
        self.df['Age'] = current_year - self.df['Year_Birth']
        print("✓ Created 'Age' feature")
        
        # 2. Total Spending
        spending_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 
                        'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
        self.df['Total_Spending'] = self.df[spending_cols].sum(axis=1)
        print("✓ Created 'Total_Spending' feature")
        
        # 3. Total Children
        self.df['Total_Children'] = self.df['Kidhome'] + self.df['Teenhome']
        print("✓ Created 'Total_Children' feature")
        
        # 4. Family Size
        self.df['Family_Size'] = self.df['Total_Children'] + 1  # +1 for the person
        # Add partner if married/together
        self.df.loc[self.df['Marital_Status'].isin(['Married', 'Together']), 'Family_Size'] += 1
        print("✓ Created 'Family_Size' feature")
        
        # 5. Is Parent
        self.df['Is_Parent'] = (self.df['Total_Children'] > 0).astype(int)
        print("✓ Created 'Is_Parent' feature")
        
        # 6. Total Purchases
        purchase_cols = ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']
        self.df['Total_Purchases'] = self.df[purchase_cols].sum(axis=1)
        print("✓ Created 'Total_Purchases' feature")
        
        # 7. Total Campaigns Accepted
        campaign_cols = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 
                        'AcceptedCmp4', 'AcceptedCmp5']
        self.df['Total_Campaigns_Accepted'] = self.df[campaign_cols].sum(axis=1)
        print("✓ Created 'Total_Campaigns_Accepted' feature")
        
        # 8. Customer Tenure (days since enrollment)
        self.df['Dt_Customer'] = pd.to_datetime(self.df['Dt_Customer'], format='%d-%m-%Y')
        reference_date = self.df['Dt_Customer'].max()
        self.df['Customer_Days'] = (reference_date - self.df['Dt_Customer']).dt.days
        print("✓ Created 'Customer_Days' feature")
        
        # 9. Average Purchase Value
        self.df['Avg_Purchase_Value'] = self.df['Total_Spending'] / (self.df['Total_Purchases'] + 1)
        print("✓ Created 'Avg_Purchase_Value' feature")
        
        # 10. Spending per Day
        self.df['Spending_Per_Day'] = self.df['Total_Spending'] / (self.df['Customer_Days'] + 1)
        print("✓ Created 'Spending_Per_Day' feature")
        
        # 11. Income per Family Member
        self.df['Income_Per_Member'] = self.df['Income'] / self.df['Family_Size']
        print("✓ Created 'Income_Per_Member' feature")
        
        # 12. Education Level (Ordinal)
        education_map = {
            'Basic': 1,
            '2n Cycle': 2,
            'Graduation': 3,
            'Master': 4,
            'PhD': 5
        }
        self.df['Education_Level'] = self.df['Education'].map(education_map)
        print("✓ Created 'Education_Level' feature")
        
        # 13. Relationship Status (Binary)
        self.df['Has_Partner'] = self.df['Marital_Status'].isin(['Married', 'Together']).astype(int)
        print("✓ Created 'Has_Partner' feature")
        
        # 14. Age Groups
        self.df['Age_Group'] = pd.cut(self.df['Age'], 
                                       bins=[0, 30, 40, 50, 60, 100],
                                       labels=['<30', '30-40', '40-50', '50-60', '60+'])
        print("✓ Created 'Age_Group' feature")
        
        # 15. Income Groups
        self.df['Income_Group'] = pd.qcut(self.df['Income'], 
                                           q=4, 
                                           labels=['Low', 'Medium', 'High', 'Very High'])
        print("✓ Created 'Income_Group' feature")
        
        # 16. Spending Groups
        self.df['Spending_Group'] = pd.qcut(self.df['Total_Spending'], 
                                             q=4, 
                                             labels=['Low', 'Medium', 'High', 'Very High'],
                                             duplicates='drop')
        print("✓ Created 'Spending_Group' feature")
        
        # 17. Web Activity Score
        self.df['Web_Activity_Score'] = (self.df['NumWebPurchases'] * 2 + 
                                          self.df['NumWebVisitsMonth']) / 3
        print("✓ Created 'Web_Activity_Score' feature")
        
        # 18. Deal Sensitivity
        self.df['Deal_Sensitivity'] = self.df['NumDealsPurchases'] / (self.df['Total_Purchases'] + 1)
        print("✓ Created 'Deal_Sensitivity' feature")
        
        # 19. Product Diversity (number of product categories purchased)
        product_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 
                       'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
        self.df['Product_Diversity'] = (self.df[product_cols] > 0).sum(axis=1)
        print("✓ Created 'Product_Diversity' feature")
        
        # 20. Response Rate
        self.df['Response_Rate'] = self.df['Total_Campaigns_Accepted'] / 5  # 5 campaigns total
        print("✓ Created 'Response_Rate' feature")
        
        print(f"\nTotal features created: 20")
        print(f"New dataset shape: {self.df.shape}")
        
    def remove_outliers(self):
        """Remove extreme outliers"""
        print("\n" + "="*50)
        print("OUTLIER REMOVAL")
        print("="*50)
        
        initial_rows = len(self.df)
        
        # Remove extreme age outliers
        self.df = self.df[(self.df['Age'] >= 18) & (self.df['Age'] <= 100)]
        
        # Remove extreme income outliers (using IQR method)
        Q1 = self.df['Income'].quantile(0.01)
        Q3 = self.df['Income'].quantile(0.99)
        self.df = self.df[(self.df['Income'] >= Q1) & (self.df['Income'] <= Q3)]
        
        # Remove extreme spending outliers
        Q1_spend = self.df['Total_Spending'].quantile(0.01)
        Q3_spend = self.df['Total_Spending'].quantile(0.99)
        self.df = self.df[(self.df['Total_Spending'] >= Q1_spend) & 
                          (self.df['Total_Spending'] <= Q3_spend)]
        
        removed_rows = initial_rows - len(self.df)
        print(f"Removed {removed_rows} outlier rows ({removed_rows/initial_rows*100:.2f}%)")
        print(f"Remaining rows: {len(self.df)}")
        
    def save_processed_data(self, output_path='data_processed.csv'):
        """Save the processed dataset"""
        self.df.to_csv(output_path, index=False)
        print(f"\n✓ Processed data saved to '{output_path}'")
        
    def get_feature_summary(self):
        """Print summary of all features"""
        print("\n" + "="*50)
        print("FEATURE SUMMARY")
        print("="*50)
        
        feature_groups = {
            'Demographic': ['Age', 'Education_Level', 'Marital_Status', 'Has_Partner', 
                           'Income', 'Income_Per_Member', 'Age_Group', 'Income_Group'],
            'Family': ['Total_Children', 'Is_Parent', 'Family_Size'],
            'Spending': ['Total_Spending', 'Avg_Purchase_Value', 'Spending_Per_Day',
                        'Spending_Group', 'Product_Diversity'],
            'Purchase Behavior': ['Total_Purchases', 'NumWebPurchases', 'NumCatalogPurchases',
                                 'NumStorePurchases', 'Deal_Sensitivity'],
            'Engagement': ['Customer_Days', 'Recency', 'Total_Campaigns_Accepted',
                          'Response_Rate', 'Web_Activity_Score', 'NumWebVisitsMonth'],
            'Product Preferences': ['MntWines', 'MntFruits', 'MntMeatProducts',
                                   'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
        }
        
        for group, features in feature_groups.items():
            print(f"\n{group}:")
            for feature in features:
                if feature in self.df.columns:
                    print(f"  - {feature}")
        
    def run_preprocessing(self):
        """Run the complete preprocessing pipeline"""
        print("\n" + "="*70)
        print(" "*15 + "CUSTOMER PERSONALITY SEGMENTATION")
        print(" "*20 + "Data Preprocessing Pipeline")
        print("="*70)
        
        self.load_data()
        self.explore_data()
        self.handle_missing_values()
        self.create_features()
        self.remove_outliers()
        self.get_feature_summary()
        self.save_processed_data()
        
        print("\n" + "="*70)
        print(" "*20 + "PREPROCESSING COMPLETE!")
        print("="*70)
        
        return self.df


if __name__ == "__main__":
    # Run preprocessing
    preprocessor = DataPreprocessor('marketing_campaign_v.csv')
    df_processed = preprocessor.run_preprocessing()
    
    print(f"\n✓ Final dataset shape: {df_processed.shape}")
    print(f"✓ Ready for machine learning!")
