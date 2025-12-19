"""
Customer Segmentation - Targeted Marketing Strategies
Develop personalized marketing strategies for each customer segment
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json


class MarketingStrategyGenerator:
    """Generate targeted marketing strategies for customer segments"""
    
    def __init__(self, data_path='data_clustered.csv'):
        """Initialize with clustered customer data"""
        try:
            self.df = pd.read_csv(data_path)
            self.cluster_col = 'Cluster_KMeans'
            
            # Check if Cluster column exists
            if self.cluster_col not in self.df.columns:
                print(f"⚠ '{self.cluster_col}' column not found in data.")
                print("   Please run the clustering analysis first (Part 2 of the notebook).")
                print("   This will create 'data_clustered.csv' with customer segments.")
                self.df = None
            else:
                print(f"✓ Loaded {len(self.df)} customers with {len(self.df[self.cluster_col].unique())} segments")
            
            self.strategies = {}
            self.segment_profiles = None
        except FileNotFoundError:
            print("⚠ Clustered data not found. Please run clustering first.")
            print("   Run: python 2_unsupervised_clustering.py")
            print("   Or execute Part 2 of customer_segmentation_analysis.ipynb")
            self.df = None
    
    def analyze_segments(self):
        """Deep analysis of each customer segment"""
        if self.df is None:
            return
        
        print("\n" + "="*70)
        print("CUSTOMER SEGMENT ANALYSIS")
        print("="*70)
        
        # Key metrics for analysis
        metrics = [
            'Age', 'Income', 'Total_Spending', 'Total_Children',
            'Family_Size', 'Total_Purchases', 'Response_Rate',
            'Product_Diversity', 'Deal_Sensitivity', 'Web_Activity_Score',
            'Avg_Purchase_Value', 'Customer_Days'
        ]
        
        available_metrics = [m for m in metrics if m in self.df.columns]
        
        # Calculate segment profiles
        self.segment_profiles = self.df.groupby(self.cluster_col)[available_metrics].agg([
            'mean', 'median', 'std'
        ]).round(2)
        
        # Segment sizes
        segment_sizes = self.df[self.cluster_col].value_counts().sort_index()
        
        print("\nSegment Sizes:")
        for segment, size in segment_sizes.items():
            percentage = (size / len(self.df)) * 100
            print(f"  Segment {segment}: {size} customers ({percentage:.1f}%)")
        
        # Detailed profiles
        print("\nSegment Profiles (Mean Values):")
        segment_means = self.df.groupby(self.cluster_col)[available_metrics].mean()
        print(segment_means.round(2))
        
        return self.segment_profiles
    
    def generate_segment_personas(self):
        """Create detailed personas for each segment"""
        if self.df is None:
            return
        
        print("\n" + "="*70)
        print("CUSTOMER SEGMENT PERSONAS")
        print("="*70)
        
        personas = {}
        
        for segment in sorted(self.df[self.cluster_col].unique()):
            segment_data = self.df[self.df[self.cluster_col] == segment]
            
            persona = {
                'segment_id': int(segment),
                'size': len(segment_data),
                'percentage': (len(segment_data) / len(self.df)) * 100,
                'demographics': {
                    'avg_age': segment_data['Age'].mean() if 'Age' in segment_data else None,
                    'avg_income': segment_data['Income'].mean() if 'Income' in segment_data else None,
                    'avg_family_size': segment_data['Family_Size'].mean() if 'Family_Size' in segment_data else None,
                },
                'behavior': {
                    'avg_spending': segment_data['Total_Spending'].mean() if 'Total_Spending' in segment_data else None,
                    'avg_purchases': segment_data['Total_Purchases'].mean() if 'Total_Purchases' in segment_data else None,
                    'response_rate': segment_data['Response_Rate'].mean() if 'Response_Rate' in segment_data else None,
                    'deal_sensitivity': segment_data['Deal_Sensitivity'].mean() if 'Deal_Sensitivity' in segment_data else None,
                    'web_activity': segment_data['Web_Activity_Score'].mean() if 'Web_Activity_Score' in segment_data else None,
                },
                'preferences': {
                    'wines': segment_data['MntWines'].mean() if 'MntWines' in segment_data else None,
                    'fruits': segment_data['MntFruits'].mean() if 'MntFruits' in segment_data else None,
                    'meat': segment_data['MntMeatProducts'].mean() if 'MntMeatProducts' in segment_data else None,
                    'fish': segment_data['MntFishProducts'].mean() if 'MntFishProducts' in segment_data else None,
                    'sweets': segment_data['MntSweetProducts'].mean() if 'MntSweetProducts' in segment_data else None,
                    'gold': segment_data['MntGoldProds'].mean() if 'MntGoldProds' in segment_data else None,
                }
            }
            
            personas[f"Segment_{segment}"] = persona
            
            # Print persona
            print(f"\n{'='*70}")
            print(f"SEGMENT {segment} PERSONA")
            print(f"{'='*70}")
            print(f"Size: {persona['size']} customers ({persona['percentage']:.1f}%)")
            print(f"\nDemographics:")
            print(f"  Average Age: {persona['demographics']['avg_age']:.1f} years")
            print(f"  Average Income: ${persona['demographics']['avg_income']:.2f}")
            print(f"  Average Family Size: {persona['demographics']['avg_family_size']:.1f}")
            print(f"\nBehavior:")
            print(f"  Average Spending: ${persona['behavior']['avg_spending']:.2f}")
            print(f"  Average Purchases: {persona['behavior']['avg_purchases']:.1f}")
            print(f"  Response Rate: {persona['behavior']['response_rate']:.2%}")
            print(f"  Deal Sensitivity: {persona['behavior']['deal_sensitivity']:.2f}")
            print(f"  Web Activity Score: {persona['behavior']['web_activity']:.2f}")
        
        # Save personas
        with open('customer_personas.json', 'w') as f:
            json.dump(personas, f, indent=2)
        print(f"\n✓ Personas saved to 'customer_personas.json'")
        
        return personas
    
    def create_marketing_strategies(self):
        """Generate specific marketing strategies for each segment"""
        if self.df is None:
            return
        
        print("\n" + "="*70)
        print("TARGETED MARKETING STRATEGIES")
        print("="*70)
        
        strategies = {}
        
        for segment in sorted(self.df[self.cluster_col].unique()):
            segment_data = self.df[self.df[self.cluster_col] == segment]
            
            # Calculate key metrics
            avg_spending = segment_data['Total_Spending'].mean() if 'Total_Spending' in segment_data else 0
            avg_income = segment_data['Income'].mean() if 'Income' in segment_data else 0
            response_rate = segment_data['Response_Rate'].mean() if 'Response_Rate' in segment_data else 0
            deal_sensitivity = segment_data['Deal_Sensitivity'].mean() if 'Deal_Sensitivity' in segment_data else 0
            web_activity = segment_data['Web_Activity_Score'].mean() if 'Web_Activity_Score' in segment_data else 0
            
            # Determine segment characteristics
            is_high_spender = avg_spending > self.df['Total_Spending'].median()
            is_high_income = avg_income > self.df['Income'].median()
            is_responsive = response_rate > self.df['Response_Rate'].median()
            is_deal_sensitive = deal_sensitivity > self.df['Deal_Sensitivity'].median()
            is_web_active = web_activity > self.df['Web_Activity_Score'].median()
            
            # Generate strategy
            strategy = {
                'segment_id': int(segment),
                'segment_name': self._get_segment_name(segment, is_high_spender, is_high_income),
                'priority': self._calculate_priority(avg_spending, response_rate),
                'channels': self._recommend_channels(is_web_active, deal_sensitivity),
                'messaging': self._create_messaging(is_high_spender, is_deal_sensitive),
                'offers': self._recommend_offers(is_high_spender, is_deal_sensitive, segment_data),
                'frequency': self._recommend_frequency(response_rate),
                'budget_allocation': self._calculate_budget(avg_spending, len(segment_data)),
                'kpis': self._define_kpis(segment)
            }
            
            strategies[f"Segment_{segment}"] = strategy
            
            # Print strategy
            print(f"\n{'='*70}")
            print(f"SEGMENT {segment}: {strategy['segment_name']}")
            print(f"{'='*70}")
            print(f"Priority: {strategy['priority']}")
            print(f"\nRecommended Channels:")
            for channel in strategy['channels']:
                print(f"  • {channel}")
            print(f"\nMessaging Strategy:")
            for msg in strategy['messaging']:
                print(f"  • {msg}")
            print(f"\nRecommended Offers:")
            for offer in strategy['offers']:
                print(f"  • {offer}")
            print(f"\nCampaign Frequency: {strategy['frequency']}")
            print(f"Budget Allocation: {strategy['budget_allocation']}")
            print(f"\nKey Performance Indicators:")
            for kpi, target in strategy['kpis'].items():
                print(f"  • {kpi}: {target}")
        
        self.strategies = strategies
        
        # Save strategies
        with open('marketing_strategies.json', 'w') as f:
            json.dump(strategies, f, indent=2)
        print(f"\n✓ Strategies saved to 'marketing_strategies.json'")
        
        return strategies
    
    def _get_segment_name(self, segment, is_high_spender, is_high_income):
        """Generate descriptive segment name"""
        names = {
            (True, True): "Premium Customers",
            (True, False): "Value Seekers",
            (False, True): "Potential Growth",
            (False, False): "Budget Conscious"
        }
        return names.get((is_high_spender, is_high_income), f"Segment {segment}")
    
    def _calculate_priority(self, avg_spending, response_rate):
        """Calculate segment priority (High/Medium/Low)"""
        score = (avg_spending / 1000) + (response_rate * 100)
        if score > 2:
            return "High"
        elif score > 1:
            return "Medium"
        else:
            return "Low"
    
    def _recommend_channels(self, is_web_active, deal_sensitivity):
        """Recommend marketing channels"""
        channels = []
        if is_web_active:
            channels.extend(["Email Marketing", "Social Media Ads", "Website Personalization"])
        else:
            channels.extend(["Direct Mail", "Catalog", "In-Store Promotions"])
        
        if deal_sensitivity:
            channels.append("SMS Deals & Alerts")
        
        return channels
    
    def _create_messaging(self, is_high_spender, is_deal_sensitive):
        """Create messaging strategy"""
        messages = []
        if is_high_spender:
            messages.extend([
                "Emphasize premium quality and exclusivity",
                "Highlight new and luxury products",
                "Focus on personalized service"
            ])
        else:
            messages.extend([
                "Emphasize value and savings",
                "Highlight product benefits",
                "Focus on practical solutions"
            ])
        
        if is_deal_sensitive:
            messages.append("Include clear discount information")
        
        return messages
    
    def _recommend_offers(self, is_high_spender, is_deal_sensitive, segment_data):
        """Recommend specific offers"""
        offers = []
        
        if is_high_spender:
            offers.extend([
                "VIP loyalty program with exclusive benefits",
                "Early access to new products",
                "Free premium shipping",
                "Personalized product recommendations"
            ])
        else:
            offers.extend([
                "Volume discounts (Buy More, Save More)",
                "Seasonal sales notifications",
                "Loyalty points program"
            ])
        
        if is_deal_sensitive:
            offers.extend([
                "Flash sales and limited-time offers",
                "Bundle deals",
                "Referral discounts"
            ])
        
        # Product-specific offers
        if 'MntWines' in segment_data.columns:
            top_product = segment_data[['MntWines', 'MntMeatProducts', 'MntFishProducts']].mean().idxmax()
            product_name = top_product.replace('Mnt', '')
            offers.append(f"Special promotions on {product_name}")
        
        return offers
    
    def _recommend_frequency(self, response_rate):
        """Recommend campaign frequency"""
        if response_rate > 0.3:
            return "Weekly campaigns"
        elif response_rate > 0.15:
            return "Bi-weekly campaigns"
        else:
            return "Monthly campaigns"
    
    def _calculate_budget(self, avg_spending, segment_size):
        """Calculate recommended budget allocation"""
        total_value = avg_spending * segment_size
        budget_percentage = min(15, max(5, (avg_spending / 1000) * 10))
        return f"{budget_percentage:.1f}% of marketing budget (Est. ${total_value:,.0f} segment value)"
    
    def _define_kpis(self, segment):
        """Define KPIs for segment"""
        return {
            "Conversion Rate": "Increase by 15%",
            "Average Order Value": "Increase by 10%",
            "Customer Retention": "Maintain 85%+",
            "Campaign Response Rate": "Achieve 20%+",
            "Customer Lifetime Value": "Increase by 20%"
        }
    
    def visualize_strategies(self):
        """Create visualizations for marketing strategies"""
        if self.df is None or not self.strategies:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Marketing Strategy Overview', fontsize=16, fontweight='bold')
        
        # 1. Segment Value
        segment_value = self.df.groupby(self.cluster_col)['Total_Spending'].sum()
        axes[0, 0].bar(segment_value.index, segment_value.values, color='steelblue')
        axes[0, 0].set_title('Total Segment Value', fontweight='bold')
        axes[0, 0].set_xlabel('Segment')
        axes[0, 0].set_ylabel('Total Spending ($)')
        
        # 2. Response Rate by Segment
        response_rate = self.df.groupby(self.cluster_col)['Response_Rate'].mean()
        axes[0, 1].bar(response_rate.index, response_rate.values, color='coral')
        axes[0, 1].set_title('Average Response Rate', fontweight='bold')
        axes[0, 1].set_xlabel('Segment')
        axes[0, 1].set_ylabel('Response Rate')
        
        # 3. Segment Size
        segment_sizes = self.df[self.cluster_col].value_counts().sort_index()
        axes[1, 0].pie(segment_sizes.values, labels=[f'Segment {i}' for i in segment_sizes.index],
                      autopct='%1.1f%%', startangle=90)
        axes[1, 0].set_title('Segment Distribution', fontweight='bold')
        
        # 4. Average Purchase Value
        avg_purchase = self.df.groupby(self.cluster_col)['Avg_Purchase_Value'].mean()
        axes[1, 1].bar(avg_purchase.index, avg_purchase.values, color='green')
        axes[1, 1].set_title('Average Purchase Value', fontweight='bold')
        axes[1, 1].set_xlabel('Segment')
        axes[1, 1].set_ylabel('Avg Purchase Value ($)')
        
        plt.tight_layout()
        plt.savefig('marketing_strategy_overview.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✓ Strategy visualization saved")
    
    def export_campaign_templates(self):
        """Export campaign templates for each segment"""
        if not self.strategies:
            return
        
        templates = {}
        
        for segment_key, strategy in self.strategies.items():
            template = {
                'campaign_name': f"{strategy['segment_name']} Campaign",
                'target_segment': strategy['segment_id'],
                'channels': strategy['channels'],
                'subject_lines': self._generate_subject_lines(strategy),
                'email_template': self._generate_email_template(strategy),
                'timing': strategy['frequency'],
                'offers': strategy['offers']
            }
            templates[segment_key] = template
        
        with open('campaign_templates.json', 'w') as f:
            json.dump(templates, f, indent=2)
        print("✓ Campaign templates saved to 'campaign_templates.json'")
        
        return templates
    
    def _generate_subject_lines(self, strategy):
        """Generate email subject lines"""
        if "Premium" in strategy['segment_name']:
            return [
                "Exclusive: Your VIP Access Awaits",
                "Handpicked Just for You",
                "Premium Collection Now Available"
            ]
        elif "Budget" in strategy['segment_name']:
            return [
                "Save Big: Limited Time Offer Inside",
                "Your Weekly Deals Are Here!",
                "More Value, Less Spend"
            ]
        else:
            return [
                "Special Offer Just for You",
                "Don't Miss Out on These Deals",
                "New Products You'll Love"
            ]
    
    def _generate_email_template(self, strategy):
        """Generate email template structure"""
        return {
            'header': f"Hello {'{customer_name}'},",
            'body': f"As one of our valued {strategy['segment_name']}, we have something special for you...",
            'cta': "Shop Now",
            'footer': "Thank you for being a loyal customer!"
        }
    
    def run_full_analysis(self):
        """Run complete marketing strategy analysis"""
        print("\n" + "="*70)
        print("MARKETING STRATEGY GENERATOR")
        print("="*70)
        
        self.analyze_segments()
        self.generate_segment_personas()
        self.create_marketing_strategies()
        self.visualize_strategies()
        self.export_campaign_templates()
        
        print("\n" + "="*70)
        print("MARKETING STRATEGY GENERATION COMPLETE!")
        print("="*70)


if __name__ == "__main__":
    generator = MarketingStrategyGenerator()
    if generator.df is not None:
        generator.run_full_analysis()
