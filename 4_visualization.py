"""
Customer Personality Segmentation - Advanced Visualizations
This module creates comprehensive visualizations for customer segments
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

class SegmentationVisualizer:
    """Creates comprehensive visualizations for customer segmentation"""
    
    def __init__(self, data_path='data_clustered.csv'):
        self.df = pd.read_csv(data_path)
        self.cluster_col = 'Cluster_KMeans'
        
    def create_cluster_overview(self):
        """Create overview dashboard of clusters"""
        print("\n" + "="*70)
        print("CREATING CLUSTER OVERVIEW DASHBOARD")
        print("="*70)
        
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle('Customer Segment Overview Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Cluster Distribution
        cluster_counts = self.df[self.cluster_col].value_counts().sort_index()
        axes[0, 0].bar(cluster_counts.index, cluster_counts.values, color='steelblue')
        axes[0, 0].set_title('Cluster Size Distribution', fontweight='bold')
        axes[0, 0].set_xlabel('Cluster')
        axes[0, 0].set_ylabel('Number of Customers')
        for i, v in enumerate(cluster_counts.values):
            axes[0, 0].text(cluster_counts.index[i], v, str(v), ha='center', va='bottom')
        
        # 2. Age Distribution by Cluster
        self.df.boxplot(column='Age', by=self.cluster_col, ax=axes[0, 1])
        axes[0, 1].set_title('Age Distribution by Cluster', fontweight='bold')
        axes[0, 1].set_xlabel('Cluster')
        axes[0, 1].set_ylabel('Age')
        plt.sca(axes[0, 1])
        plt.xticks(rotation=0)
        
        # 3. Income Distribution by Cluster
        self.df.boxplot(column='Income', by=self.cluster_col, ax=axes[0, 2])
        axes[0, 2].set_title('Income Distribution by Cluster', fontweight='bold')
        axes[0, 2].set_xlabel('Cluster')
        axes[0, 2].set_ylabel('Income')
        plt.sca(axes[0, 2])
        plt.xticks(rotation=0)
        
        # 4. Total Spending by Cluster
        spending_by_cluster = self.df.groupby(self.cluster_col)['Total_Spending'].mean()
        axes[1, 0].bar(spending_by_cluster.index, spending_by_cluster.values, color='coral')
        axes[1, 0].set_title('Average Spending by Cluster', fontweight='bold')
        axes[1, 0].set_xlabel('Cluster')
        axes[1, 0].set_ylabel('Average Spending ($)')
        for i, v in enumerate(spending_by_cluster.values):
            axes[1, 0].text(spending_by_cluster.index[i], v, f'${v:.0f}', ha='center', va='bottom')
        
        # 5. Education Level Distribution
        education_cluster = pd.crosstab(self.df[self.cluster_col], self.df['Education'], normalize='index') * 100
        education_cluster.plot(kind='bar', stacked=True, ax=axes[1, 1], colormap='Set3')
        axes[1, 1].set_title('Education Distribution by Cluster (%)', fontweight='bold')
        axes[1, 1].set_xlabel('Cluster')
        axes[1, 1].set_ylabel('Percentage')
        axes[1, 1].legend(title='Education', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.sca(axes[1, 1])
        plt.xticks(rotation=0)
        
        # 6. Marital Status Distribution
        marital_cluster = pd.crosstab(self.df[self.cluster_col], self.df['Marital_Status'], normalize='index') * 100
        marital_cluster.plot(kind='bar', stacked=True, ax=axes[1, 2], colormap='Pastel1')
        axes[1, 2].set_title('Marital Status Distribution by Cluster (%)', fontweight='bold')
        axes[1, 2].set_xlabel('Cluster')
        axes[1, 2].set_ylabel('Percentage')
        axes[1, 2].legend(title='Marital Status', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.sca(axes[1, 2])
        plt.xticks(rotation=0)
        
        plt.tight_layout()
        plt.savefig('cluster_overview_dashboard.png', dpi=300, bbox_inches='tight')
        print("✓ Cluster overview dashboard saved as 'cluster_overview_dashboard.png'")
        plt.show()
        
    def create_spending_analysis(self):
        """Analyze spending patterns across clusters"""
        print("\n" + "="*70)
        print("CREATING SPENDING ANALYSIS")
        print("="*70)
        
        # Spending columns
        spending_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 
                        'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
        
        fig, axes = plt.subplots(2, 2, figsize=(18, 12))
        fig.suptitle('Customer Spending Analysis by Segment', fontsize=16, fontweight='bold')
        
        # 1. Average spending by category and cluster
        spending_by_cluster = self.df.groupby(self.cluster_col)[spending_cols].mean()
        spending_by_cluster.plot(kind='bar', ax=axes[0, 0], colormap='viridis')
        axes[0, 0].set_title('Average Spending by Product Category', fontweight='bold')
        axes[0, 0].set_xlabel('Cluster')
        axes[0, 0].set_ylabel('Average Spending ($)')
        axes[0, 0].legend(title='Product Category', bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[0, 0].tick_params(axis='x', rotation=0)
        
        # 2. Total spending distribution
        for cluster in sorted(self.df[self.cluster_col].unique()):
            cluster_data = self.df[self.df[self.cluster_col] == cluster]['Total_Spending']
            axes[0, 1].hist(cluster_data, alpha=0.6, label=f'Cluster {cluster}', bins=30)
        axes[0, 1].set_title('Total Spending Distribution by Cluster', fontweight='bold')
        axes[0, 1].set_xlabel('Total Spending ($)')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].legend()
        
        # 3. Spending heatmap
        spending_pivot = self.df.groupby(self.cluster_col)[spending_cols].mean()
        sns.heatmap(spending_pivot.T, annot=True, fmt='.0f', cmap='YlOrRd', ax=axes[1, 0], cbar_kws={'label': 'Average Spending ($)'})
        axes[1, 0].set_title('Spending Heatmap by Category and Cluster', fontweight='bold')
        axes[1, 0].set_xlabel('Cluster')
        axes[1, 0].set_ylabel('Product Category')
        
        # 4. Spending share by cluster
        total_spending_by_cluster = self.df.groupby(self.cluster_col)['Total_Spending'].sum()
        axes[1, 1].pie(total_spending_by_cluster.values, labels=[f'Cluster {i}' for i in total_spending_by_cluster.index],
                      autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set2'))
        axes[1, 1].set_title('Total Spending Share by Cluster', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('spending_analysis.png', dpi=300, bbox_inches='tight')
        print("✓ Spending analysis saved as 'spending_analysis.png'")
        plt.show()
        
    def create_purchase_behavior_analysis(self):
        """Analyze purchase behavior patterns"""
        print("\n" + "="*70)
        print("CREATING PURCHASE BEHAVIOR ANALYSIS")
        print("="*70)
        
        purchase_cols = ['NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases',
                        'NumStorePurchases', 'NumWebVisitsMonth']
        
        fig, axes = plt.subplots(2, 2, figsize=(18, 12))
        fig.suptitle('Purchase Behavior Analysis by Segment', fontsize=16, fontweight='bold')
        
        # 1. Purchase channel preferences
        channel_cols = ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']
        channel_by_cluster = self.df.groupby(self.cluster_col)[channel_cols].mean()
        channel_by_cluster.plot(kind='bar', ax=axes[0, 0], colormap='Set2')
        axes[0, 0].set_title('Average Purchases by Channel', fontweight='bold')
        axes[0, 0].set_xlabel('Cluster')
        axes[0, 0].set_ylabel('Average Number of Purchases')
        axes[0, 0].legend(title='Channel', labels=['Web', 'Catalog', 'Store'])
        axes[0, 0].tick_params(axis='x', rotation=0)
        
        # 2. Deal purchases vs regular purchases
        deal_data = self.df.groupby(self.cluster_col)['NumDealsPurchases'].mean()
        axes[0, 1].bar(deal_data.index, deal_data.values, color='lightcoral')
        axes[0, 1].set_title('Average Deal Purchases by Cluster', fontweight='bold')
        axes[0, 1].set_xlabel('Cluster')
        axes[0, 1].set_ylabel('Average Deal Purchases')
        for i, v in enumerate(deal_data.values):
            axes[0, 1].text(deal_data.index[i], v, f'{v:.1f}', ha='center', va='bottom')
        
        # 3. Web visits vs web purchases
        for cluster in sorted(self.df[self.cluster_col].unique()):
            cluster_data = self.df[self.df[self.cluster_col] == cluster]
            axes[1, 0].scatter(cluster_data['NumWebVisitsMonth'], cluster_data['NumWebPurchases'],
                             alpha=0.5, label=f'Cluster {cluster}', s=50)
        axes[1, 0].set_title('Web Visits vs Web Purchases', fontweight='bold')
        axes[1, 0].set_xlabel('Web Visits per Month')
        axes[1, 0].set_ylabel('Web Purchases')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Recency analysis
        recency_by_cluster = self.df.groupby(self.cluster_col)['Recency'].mean()
        axes[1, 1].barh(recency_by_cluster.index, recency_by_cluster.values, color='skyblue')
        axes[1, 1].set_title('Average Recency by Cluster (Days Since Last Purchase)', fontweight='bold')
        axes[1, 1].set_ylabel('Cluster')
        axes[1, 1].set_xlabel('Average Recency (Days)')
        for i, v in enumerate(recency_by_cluster.values):
            axes[1, 1].text(v, recency_by_cluster.index[i], f'{v:.0f}', ha='left', va='center')
        
        plt.tight_layout()
        plt.savefig('purchase_behavior_analysis.png', dpi=300, bbox_inches='tight')
        print("✓ Purchase behavior analysis saved as 'purchase_behavior_analysis.png'")
        plt.show()
        
    def create_campaign_response_analysis(self):
        """Analyze campaign response patterns"""
        print("\n" + "="*70)
        print("CREATING CAMPAIGN RESPONSE ANALYSIS")
        print("="*70)
        
        campaign_cols = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 
                        'AcceptedCmp4', 'AcceptedCmp5', 'Response_Rate']
        
        fig, axes = plt.subplots(2, 2, figsize=(18, 12))
        fig.suptitle('Campaign Response Analysis by Segment', fontsize=16, fontweight='bold')
        
        # 1. Campaign acceptance rates
        campaign_by_cluster = self.df.groupby(self.cluster_col)[campaign_cols].mean() * 100
        campaign_by_cluster.plot(kind='bar', ax=axes[0, 0], colormap='coolwarm')
        axes[0, 0].set_title('Campaign Acceptance Rates (%)', fontweight='bold')
        axes[0, 0].set_xlabel('Cluster')
        axes[0, 0].set_ylabel('Acceptance Rate (%)')
        axes[0, 0].legend(title='Campaign', bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[0, 0].tick_params(axis='x', rotation=0)
        
        # 2. Total campaign acceptance
        self.df['Total_Campaigns_Accepted'] = self.df[campaign_cols].sum(axis=1)
        total_acceptance = self.df.groupby(self.cluster_col)['Total_Campaigns_Accepted'].mean()
        axes[0, 1].bar(total_acceptance.index, total_acceptance.values, color='mediumseagreen')
        axes[0, 1].set_title('Average Total Campaigns Accepted', fontweight='bold')
        axes[0, 1].set_xlabel('Cluster')
        axes[0, 1].set_ylabel('Average Campaigns Accepted')
        for i, v in enumerate(total_acceptance.values):
            axes[0, 1].text(total_acceptance.index[i], v, f'{v:.2f}', ha='center', va='bottom')
        
        # 3. Campaign response heatmap
        campaign_pivot = self.df.groupby(self.cluster_col)[campaign_cols].mean() * 100
        sns.heatmap(campaign_pivot.T, annot=True, fmt='.1f', cmap='RdYlGn', ax=axes[1, 0], 
                   cbar_kws={'label': 'Acceptance Rate (%)'})
        axes[1, 0].set_title('Campaign Response Heatmap', fontweight='bold')
        axes[1, 0].set_xlabel('Cluster')
        axes[1, 0].set_ylabel('Campaign')
        
        # 4. Response rate distribution
        response_counts = self.df.groupby([self.cluster_col, 'Total_Campaigns_Accepted']).size().unstack(fill_value=0)
        response_counts.plot(kind='bar', stacked=True, ax=axes[1, 1], colormap='viridis')
        axes[1, 1].set_title('Distribution of Campaign Responses', fontweight='bold')
        axes[1, 1].set_xlabel('Cluster')
        axes[1, 1].set_ylabel('Number of Customers')
        axes[1, 1].legend(title='Campaigns Accepted', bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[1, 1].tick_params(axis='x', rotation=0)
        
        plt.tight_layout()
        plt.savefig('campaign_response_analysis.png', dpi=300, bbox_inches='tight')
        print("✓ Campaign response analysis saved as 'campaign_response_analysis.png'")
        plt.show()
        
    def create_demographic_analysis(self):
        """Analyze demographic patterns"""
        print("\n" + "="*70)
        print("CREATING DEMOGRAPHIC ANALYSIS")
        print("="*70)
        
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle('Demographic Analysis by Segment', fontsize=16, fontweight='bold')
        
        # 1. Age distribution
        for cluster in sorted(self.df[self.cluster_col].unique()):
            cluster_data = self.df[self.df[self.cluster_col] == cluster]['Age']
            axes[0, 0].hist(cluster_data, alpha=0.6, label=f'Cluster {cluster}', bins=20)
        axes[0, 0].set_title('Age Distribution by Cluster', fontweight='bold')
        axes[0, 0].set_xlabel('Age')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].legend()
        
        # 2. Income distribution
        for cluster in sorted(self.df[self.cluster_col].unique()):
            cluster_data = self.df[self.df[self.cluster_col] == cluster]['Income']
            axes[0, 1].hist(cluster_data, alpha=0.6, label=f'Cluster {cluster}', bins=20)
        axes[0, 1].set_title('Income Distribution by Cluster', fontweight='bold')
        axes[0, 1].set_xlabel('Income ($)')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].legend()
        
        # 3. Children at home
        children_by_cluster = self.df.groupby(self.cluster_col)['Kidhome'].mean()
        axes[0, 2].bar(children_by_cluster.index, children_by_cluster.values, color='lightblue')
        axes[0, 2].set_title('Average Children at Home', fontweight='bold')
        axes[0, 2].set_xlabel('Cluster')
        axes[0, 2].set_ylabel('Average Number of Children')
        for i, v in enumerate(children_by_cluster.values):
            axes[0, 2].text(children_by_cluster.index[i], v, f'{v:.2f}', ha='center', va='bottom')
        
        # 4. Teenagers at home
        teens_by_cluster = self.df.groupby(self.cluster_col)['Teenhome'].mean()
        axes[1, 0].bar(teens_by_cluster.index, teens_by_cluster.values, color='lightgreen')
        axes[1, 0].set_title('Average Teenagers at Home', fontweight='bold')
        axes[1, 0].set_xlabel('Cluster')
        axes[1, 0].set_ylabel('Average Number of Teenagers')
        for i, v in enumerate(teens_by_cluster.values):
            axes[1, 0].text(teens_by_cluster.index[i], v, f'{v:.2f}', ha='center', va='bottom')
        
        # 5. Customer tenure
        tenure_by_cluster = self.df.groupby(self.cluster_col)['Customer_Days'].mean()
        axes[1, 1].bar(tenure_by_cluster.index, tenure_by_cluster.values, color='salmon')
        axes[1, 1].set_title('Average Customer Tenure (Days)', fontweight='bold')
        axes[1, 1].set_xlabel('Cluster')
        axes[1, 1].set_ylabel('Average Days as Customer')
        for i, v in enumerate(tenure_by_cluster.values):
            axes[1, 1].text(tenure_by_cluster.index[i], v, f'{v:.0f}', ha='center', va='bottom')
        
        # 6. Complain rate
        complain_by_cluster = self.df.groupby(self.cluster_col)['Complain'].mean() * 100
        axes[1, 2].bar(complain_by_cluster.index, complain_by_cluster.values, color='indianred')
        axes[1, 2].set_title('Complaint Rate by Cluster (%)', fontweight='bold')
        axes[1, 2].set_xlabel('Cluster')
        axes[1, 2].set_ylabel('Complaint Rate (%)')
        for i, v in enumerate(complain_by_cluster.values):
            axes[1, 2].text(complain_by_cluster.index[i], v, f'{v:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('demographic_analysis.png', dpi=300, bbox_inches='tight')
        print("✓ Demographic analysis saved as 'demographic_analysis.png'")
        plt.show()
        
    def create_interactive_3d_plot(self):
        """Create interactive 3D visualization using plotly"""
        print("\n" + "="*70)
        print("CREATING INTERACTIVE 3D VISUALIZATION")
        print("="*70)
        
        fig = px.scatter_3d(self.df, 
                           x='Income', 
                           y='Total_Spending', 
                           z='Age',
                           color=self.cluster_col,
                           size='NumWebPurchases',
                           hover_data=['Education', 'Marital_Status', 'Recency'],
                           title='Interactive 3D Customer Segmentation',
                           labels={'Income': 'Income ($)', 
                                  'Total_Spending': 'Total Spending ($)',
                                  'Age': 'Age (years)'},
                           color_continuous_scale='viridis')
        
        fig.update_layout(
            scene=dict(
                xaxis_title='Income ($)',
                yaxis_title='Total Spending ($)',
                zaxis_title='Age (years)'
            ),
            width=1000,
            height=800
        )
        
        fig.write_html('interactive_3d_clusters.html')
        print("✓ Interactive 3D visualization saved as 'interactive_3d_clusters.html'")
        fig.show()
        
    def create_cluster_profiles(self):
        """Create detailed cluster profile summary"""
        print("\n" + "="*70)
        print("CREATING CLUSTER PROFILES")
        print("="*70)
        
        profiles = []
        
        for cluster in sorted(self.df[self.cluster_col].unique()):
            cluster_data = self.df[self.df[self.cluster_col] == cluster]
            
            profile = {
                'Cluster': cluster,
                'Size': len(cluster_data),
                'Avg_Age': cluster_data['Age'].mean(),
                'Avg_Income': cluster_data['Income'].mean(),
                'Avg_Spending': cluster_data['Total_Spending'].mean(),
                'Avg_Recency': cluster_data['Recency'].mean(),
                'Avg_Web_Visits': cluster_data['NumWebVisitsMonth'].mean(),
                'Avg_Campaigns_Accepted': cluster_data[['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 
                                                        'AcceptedCmp4', 'AcceptedCmp5', 'Response_Rate']].sum(axis=1).mean(),
                'Most_Common_Education': cluster_data['Education'].mode()[0],
                'Most_Common_Marital_Status': cluster_data['Marital_Status'].mode()[0],
                'Avg_Children': cluster_data['Kidhome'].mean(),
                'Avg_Teenagers': cluster_data['Teenhome'].mean(),
                'Complaint_Rate': cluster_data['Complain'].mean() * 100
            }
            profiles.append(profile)
        
        profile_df = pd.DataFrame(profiles)
        profile_df.to_csv('cluster_profiles.csv', index=False)
        
        print("\n" + "="*70)
        print("CLUSTER PROFILES SUMMARY")
        print("="*70)
        print(profile_df.to_string(index=False))
        print("\n✓ Cluster profiles saved as 'cluster_profiles.csv'")
        
        return profile_df
        
    def run_all_visualizations(self):
        """Run all visualization methods"""
        print("\n" + "="*80)
        print(" "*20 + "CUSTOMER SEGMENTATION VISUALIZATION SUITE")
        print("="*80)
        
        self.create_cluster_overview()
        self.create_spending_analysis()
        self.create_purchase_behavior_analysis()
        self.create_campaign_response_analysis()
        self.create_demographic_analysis()
        self.create_interactive_3d_plot()
        profile_df = self.create_cluster_profiles()
        
        print("\n" + "="*80)
        print("ALL VISUALIZATIONS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nGenerated Files:")
        print("  • cluster_overview_dashboard.png")
        print("  • spending_analysis.png")
        print("  • purchase_behavior_analysis.png")
        print("  • campaign_response_analysis.png")
        print("  • demographic_analysis.png")
        print("  • interactive_3d_clusters.html")
        print("  • cluster_profiles.csv")
        print("\n" + "="*80)
        
        return profile_df


def main():
    """Main execution function"""
    print("\n" + "="*80)
    print(" "*15 + "CUSTOMER PERSONALITY SEGMENTATION - VISUALIZATION")
    print("="*80)
    
    # Initialize visualizer
    visualizer = SegmentationVisualizer('data_clustered.csv')
    
    # Run all visualizations
    profile_df = visualizer.run_all_visualizations()
    
    print("\n✓ Visualization module completed successfully!")
    print("="*80)


if __name__ == "__main__":
    main()