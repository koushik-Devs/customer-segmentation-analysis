"""
Customer Personality Segmentation - Supervised Learning
This module builds classification models to predict customer segments
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (classification_report, confusion_matrix, 
                            accuracy_score, precision_score, recall_score, 
                            f1_score, roc_auc_score, roc_curve)
from sklearn.tree import plot_tree
import joblib
import warnings
warnings.filterwarnings('ignore')

class SupervisedSegmentation:
    """Builds supervised models to predict customer segments"""
    
    def __init__(self, data_path='data_clustered.csv'):
        self.df = pd.read_csv(data_path)
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = None
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        
    def prepare_data(self, target_col='Cluster_KMeans'):
        """Prepare data for supervised learning"""
        print("\n" + "="*70)
        print("DATA PREPARATION FOR SUPERVISED LEARNING")
        print("="*70)
        
        # Features for modeling
        feature_cols = [
            'Age', 'Income', 'Total_Spending', 'Total_Children',
            'Family_Size', 'Total_Purchases', 'Customer_Days',
            'Avg_Purchase_Value', 'Spending_Per_Day', 'Income_Per_Member',
            'Education_Level', 'Has_Partner', 'Total_Campaigns_Accepted',
            'Web_Activity_Score', 'Deal_Sensitivity', 'Product_Diversity',
            'Response_Rate', 'Recency', 'NumWebVisitsMonth',
            'MntWines', 'MntFruits', 'MntMeatProducts',
            'MntFishProducts', 'MntSweetProducts', 'MntGoldProds'
        ]
        
        # Filter available features
        available_features = [f for f in feature_cols if f in self.df.columns]
        self.feature_cols = available_features  # Store as instance attribute
        
        X = self.df[available_features].copy()
        y = self.df[target_col].copy()
        
        # Handle missing values
        X = X.fillna(X.median())
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        self.scaler = StandardScaler()
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
        
        print(f"Training set: {self.X_train.shape}")
        print(f"Test set: {self.X_test.shape}")
        print(f"Number of classes: {len(np.unique(y))}")
        print(f"Class distribution:\n{y.value_counts()}")
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def train_models(self):
        """Train multiple classification models"""
        print("\n" + "="*70)
        print("TRAINING CLASSIFICATION MODELS")
        print("="*70)
        
        # Define models
        models = {
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
            'Decision Tree': DecisionTreeClassifier(random_state=42),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
            'Support Vector Machine': SVC(kernel='rbf', probability=True, random_state=42)
        }
        
        results = []
        
        for name, model in models.items():
            print(f"\nTraining {name}...")
            
            # Train model
            model.fit(self.X_train, self.y_train)
            
            # Predictions
            y_pred = model.predict(self.X_test)
            
            # Metrics
            accuracy = accuracy_score(self.y_test, y_pred)
            precision = precision_score(self.y_test, y_pred, average='weighted')
            recall = recall_score(self.y_test, y_pred, average='weighted')
            f1 = f1_score(self.y_test, y_pred, average='weighted')
            
            # Cross-validation
            cv_scores = cross_val_score(model, self.X_train, self.y_train, cv=5)
            
            results.append({
                'Model': name,
                'Accuracy': accuracy,
                'Precision': precision,
                'Recall': recall,
                'F1-Score': f1,
                'CV Mean': cv_scores.mean(),
                'CV Std': cv_scores.std()
            })
            
            # Store model
            self.models[name] = model
            
            print(f"  Accuracy: {accuracy:.4f}")
            print(f"  F1-Score: {f1:.4f}")
            print(f"  CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        # Create results dataframe
        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values('F1-Score', ascending=False)
        
        print("\n" + "="*70)
        print("MODEL COMPARISON")
        print("="*70)
        print(results_df.to_string(index=False))
        
        # Save results
        results_df.to_csv('model_comparison.csv', index=False)
        print("\n✓ Model comparison saved to 'model_comparison.csv'")
        
        # Select best model
        best_idx = results_df['F1-Score'].idxmax()
        self.best_model_name = results_df.loc[best_idx, 'Model']
        self.best_model = self.models[self.best_model_name]
        
        print(f"\n✓ Best Model: {self.best_model_name}")
        
        return results_df
    
    def optimize_best_model(self):
        """Hyperparameter tuning for best model"""
        print("\n" + "="*70)
        print(f"HYPERPARAMETER TUNING - {self.best_model_name}")
        print("="*70)
        
        if self.best_model_name == 'Random Forest':
            param_grid = {
                'n_estimators': [100, 200],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5],
                'min_samples_leaf': [1, 2]
            }
            model = RandomForestClassifier(random_state=42)
            
        elif self.best_model_name == 'Gradient Boosting':
            param_grid = {
                'n_estimators': [100, 200],
                'learning_rate': [0.01, 0.1],
                'max_depth': [3, 5],
                'min_samples_split': [2, 5]
            }
            model = GradientBoostingClassifier(random_state=42)
            
        else:
            print("Using default best model without tuning")
            return self.best_model
        
        print("Performing Grid Search...")
        grid_search = GridSearchCV(model, param_grid, cv=3, scoring='f1_weighted', n_jobs=-1)
        grid_search.fit(self.X_train, self.y_train)
        
        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Best CV score: {grid_search.best_score_:.4f}")
        
        self.best_model = grid_search.best_estimator_
        
        return self.best_model
    
    def evaluate_best_model(self):
        """Detailed evaluation of best model"""
        print("\n" + "="*70)
        print(f"DETAILED EVALUATION - {self.best_model_name}")
        print("="*70)
        
        # Predictions
        y_pred = self.best_model.predict(self.X_test)
        y_pred_proba = self.best_model.predict_proba(self.X_test)
        
        # Classification Report
        print("\nClassification Report:")
        print(classification_report(self.y_test, y_pred))
        
        # Confusion Matrix
        cm = confusion_matrix(self.y_test, y_pred)
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True)
        plt.title(f'Confusion Matrix - {self.best_model_name}', fontsize=14, fontweight='bold')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("\n✓ Confusion matrix saved")
        
        # Feature Importance (if available)
        if hasattr(self.best_model, 'feature_importances_'):
            self.plot_feature_importance()
    
    def plot_feature_importance(self):
        """Plot feature importance"""
        print("\nPlotting feature importance...")
        
        # Get feature names
        feature_cols = [
            'Age', 'Income', 'Total_Spending', 'Total_Children',
            'Family_Size', 'Total_Purchases', 'Customer_Days',
            'Avg_Purchase_Value', 'Spending_Per_Day', 'Income_Per_Member',
            'Education_Level', 'Has_Partner', 'Total_Campaigns_Accepted',
            'Web_Activity_Score', 'Deal_Sensitivity', 'Product_Diversity',
            'Response_Rate', 'Recency', 'NumWebVisitsMonth',
            'MntWines', 'MntFruits', 'MntMeatProducts',
            'MntFishProducts', 'MntSweetProducts', 'MntGoldProds'
        ]
        available_features = [f for f in feature_cols if f in self.df.columns]
        
        importances = self.best_model.feature_importances_
        indices = np.argsort(importances)[::-1][:15]  # Top 15 features
        
        plt.figure(figsize=(12, 8))
        plt.title('Top 15 Feature Importances', fontsize=14, fontweight='bold')
        plt.barh(range(len(indices)), importances[indices], color='steelblue')
        plt.yticks(range(len(indices)), [available_features[i] for i in indices])
        plt.xlabel('Importance')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Feature importance plot saved")
    
    def save_model(self):
        """Save the best model"""
        import os
        os.makedirs('models', exist_ok=True)
        
        joblib.dump(self.best_model, 'models/best_classifier.pkl')
        joblib.dump(self.scaler, 'models/scaler.pkl')
        joblib.dump(self.feature_cols, 'models/feature_names.pkl')
        
        print(f"\n✓ Best model saved to 'models/best_classifier.pkl'")
        print(f"✓ Scaler saved to 'models/scaler.pkl'")
        print(f"✓ Feature names saved to 'models/feature_names.pkl'")
    
    def predict_new_customer(self, customer_data):
        """Predict segment for new customer"""
        # Scale data
        customer_scaled = self.scaler.transform(customer_data)
        
        # Predict
        prediction = self.best_model.predict(customer_scaled)
        probabilities = self.best_model.predict_proba(customer_scaled)
        
        return prediction[0], probabilities[0]
    
    def run_supervised_learning(self):
        """Run complete supervised learning pipeline"""
        print("\n" + "="*70)
        print(" "*15 + "SUPERVISED LEARNING - CLASSIFICATION")
        print("="*70)
        
        self.prepare_data()
        self.train_models()
        self.optimize_best_model()
        self.evaluate_best_model()
        self.save_model()
        
        print("\n" + "="*70)
        print(" "*15 + "SUPERVISED LEARNING COMPLETE!")
        print("="*70)
        
        return self.best_model


if __name__ == "__main__":
    supervised = SupervisedSegmentation()
    best_model = supervised.run_supervised_learning()
    print(f"\n✓ Best model: {supervised.best_model_name}")
    print(f"✓ Model ready for deployment!")
