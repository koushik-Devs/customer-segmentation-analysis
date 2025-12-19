"""
Customer Segmentation - Segment Evolution Monitoring
Track and monitor how customer segments evolve over time
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import warnings
warnings.filterwarnings('ignore')


class SegmentMonitor:
    """Monitor customer segment evolution and changes over time"""
    
    def __init__(self, data_path='data_clustered.csv'):
        """Initialize with customer data"""
        try:
            self.df = pd.read_csv(data_path)
            self.df['analysis_date'] = datetime.now()
            self.cluster_col = 'Cluster_KMeans'
            
            # Check if Cluster column exists
            if self.cluster_col not in self.df.columns:
                print(f"⚠ '{self.cluster_col}' column not found in data.")
                print("   Please run the clustering analysis first (Part 2 of the notebook).")
                print("   This will create 'data_clustered.csv' with customer segments.")
                self.df = None
            else:
                print(f"✓ Loaded {len(self.df)} customers with {len(self.df[self.cluster_col].unique())} segments")
            
            self.historical_data = []
            self.alerts = []
        except FileNotFoundError:
            print("⚠ Data file not found. Please run clustering first.")
            print("   Run: python 2_unsupervised_clustering.py")
            print("   Or execute Part 2 of customer_segmentation_analysis.ipynb")
            self.df = None
    
    def create_baseline_snapshot(self):
        """Create baseline snapshot of current segments"""
        if self.df is None:
            return
        
        print("\n" + "="*70)
        print("CREATING BASELINE SNAPSHOT")
        print("="*70)
        
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'total_customers': len(self.df),
            'segments': {}
        }
        
        for segment in sorted(self.df[self.cluster_col].unique()):
            segment_data = self.df[self.df[self.cluster_col] == segment]
            
            snapshot['segments'][f'segment_{segment}'] = {
                'size': len(segment_data),
                'percentage': (len(segment_data) / len(self.df)) * 100,
                'metrics': {
                    'avg_spending': float(segment_data['Total_Spending'].mean()) if 'Total_Spending' in segment_data else 0,
                    'avg_income': float(segment_data['Income'].mean()) if 'Income' in segment_data else 0,
                    'avg_purchases': float(segment_data['Total_Purchases'].mean()) if 'Total_Purchases' in segment_data else 0,
                    'response_rate': float(segment_data['Response_Rate'].mean()) if 'Response_Rate' in segment_data else 0,
                    'avg_age': float(segment_data['Age'].mean()) if 'Age' in segment_data else 0,
                }
            }
        
        # Save baseline
        with open('segment_baseline.json', 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        print(f"✓ Baseline snapshot created with {len(snapshot['segments'])} segments")
        print(f"✓ Saved to 'segment_baseline.json'")
        
        return snapshot
    
    def track_segment_changes(self, previous_snapshot_path='segment_baseline.json'):
        """Track changes in segments compared to baseline"""
        if self.df is None:
            return
        
        print("\n" + "="*70)
        print("TRACKING SEGMENT CHANGES")
        print("="*70)
        
        try:
            with open(previous_snapshot_path, 'r') as f:
                baseline = json.load(f)
        except FileNotFoundError:
            print("⚠ No baseline found. Creating new baseline...")
            return self.create_baseline_snapshot()
        
        current_snapshot = self.create_baseline_snapshot()
        
        changes = {
            'analysis_date': datetime.now().isoformat(),
            'baseline_date': baseline['timestamp'],
            'segment_changes': {}
        }
        
        print("\nSegment Changes:")
        print("-" * 70)
        
        for segment_key in baseline['segments'].keys():
            if segment_key in current_snapshot['segments']:
                baseline_seg = baseline['segments'][segment_key]
                current_seg = current_snapshot['segments'][segment_key]
                
                size_change = current_seg['size'] - baseline_seg['size']
                size_change_pct = (size_change / baseline_seg['size']) * 100 if baseline_seg['size'] > 0 else 0
                
                spending_change = current_seg['metrics']['avg_spending'] - baseline_seg['metrics']['avg_spending']
                spending_change_pct = (spending_change / baseline_seg['metrics']['avg_spending']) * 100 if baseline_seg['metrics']['avg_spending'] > 0 else 0
                
                response_change = current_seg['metrics']['response_rate'] - baseline_seg['metrics']['response_rate']
                
                changes['segment_changes'][segment_key] = {
                    'size_change': size_change,
                    'size_change_pct': size_change_pct,
                    'spending_change': spending_change,
                    'spending_change_pct': spending_change_pct,
                    'response_rate_change': response_change
                }
                
                print(f"\n{segment_key.upper()}:")
                print(f"  Size: {baseline_seg['size']} → {current_seg['size']} ({size_change:+d}, {size_change_pct:+.1f}%)")
                print(f"  Avg Spending: ${baseline_seg['metrics']['avg_spending']:.2f} → ${current_seg['metrics']['avg_spending']:.2f} ({spending_change_pct:+.1f}%)")
                print(f"  Response Rate: {baseline_seg['metrics']['response_rate']:.3f} → {current_seg['metrics']['response_rate']:.3f} ({response_change:+.3f})")
                
                # Generate alerts
                if abs(size_change_pct) > 10:
                    self.alerts.append({
                        'type': 'SIZE_CHANGE',
                        'segment': segment_key,
                        'severity': 'HIGH' if abs(size_change_pct) > 20 else 'MEDIUM',
                        'message': f"{segment_key} size changed by {size_change_pct:+.1f}%"
                    })
                
                if abs(spending_change_pct) > 15:
                    self.alerts.append({
                        'type': 'SPENDING_CHANGE',
                        'segment': segment_key,
                        'severity': 'HIGH',
                        'message': f"{segment_key} spending changed by {spending_change_pct:+.1f}%"
                    })
        
        # Save changes
        with open('segment_changes.json', 'w') as f:
            json.dump(changes, f, indent=2)
        
        print(f"\n✓ Changes tracked and saved to 'segment_changes.json'")
        
        return changes
    
    def monitor_customer_migration(self):
        """Monitor customers moving between segments"""
        if self.df is None:
            return
        
        print("\n" + "="*70)
        print("CUSTOMER MIGRATION ANALYSIS")
        print("="*70)
        
        # Simulate historical data (in production, load from database)
        # For demo, we'll create a synthetic previous assignment
        np.random.seed(42)
        self.df['Previous_Cluster'] = self.df[self.cluster_col].copy()
        
        # Simulate some migrations (5% of customers)
        migration_indices = np.random.choice(self.df.index, size=int(len(self.df) * 0.05), replace=False)
        for idx in migration_indices:
            current_cluster = self.df.loc[idx, self.cluster_col]
            possible_clusters = [c for c in self.df[self.cluster_col].unique() if c != current_cluster]
            if possible_clusters:
                self.df.loc[idx, 'Previous_Cluster'] = np.random.choice(possible_clusters)
        
        # Create migration matrix
        migration_matrix = pd.crosstab(
            self.df['Previous_Cluster'],
            self.df[self.cluster_col],
            normalize='index'
        ) * 100
        
        print("\nMigration Matrix (% of customers):")
        print(migration_matrix.round(1))
        
        # Visualize migration
        plt.figure(figsize=(10, 8))
        sns.heatmap(migration_matrix, annot=True, fmt='.1f', cmap='YlOrRd', 
                   cbar_kws={'label': 'Migration %'})
        plt.title('Customer Segment Migration Matrix', fontsize=14, fontweight='bold')
        plt.xlabel('Current Segment')
        plt.ylabel('Previous Segment')
        plt.tight_layout()
        plt.savefig('segment_migration.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("\n✓ Migration analysis complete")
        
        # Identify high-risk migrations
        for prev_seg in migration_matrix.index:
            for curr_seg in migration_matrix.columns:
                if prev_seg != curr_seg and migration_matrix.loc[prev_seg, curr_seg] > 5:
                    self.alerts.append({
                        'type': 'MIGRATION',
                        'severity': 'MEDIUM',
                        'message': f"{migration_matrix.loc[prev_seg, curr_seg]:.1f}% migrated from Segment {prev_seg} to {curr_seg}"
                    })
        
        return migration_matrix
    
    def track_segment_health(self):
        """Calculate and track segment health scores"""
        if self.df is None:
            return
        
        print("\n" + "="*70)
        print("SEGMENT HEALTH MONITORING")
        print("="*70)
        
        health_scores = {}
        
        for segment in sorted(self.df[self.cluster_col].unique()):
            segment_data = self.df[self.df[self.cluster_col] == segment]
            
            # Calculate health metrics (0-100 scale)
            spending_score = min(100, (segment_data['Total_Spending'].mean() / 1000) * 100) if 'Total_Spending' in segment_data else 0
            response_score = segment_data['Response_Rate'].mean() * 100 if 'Response_Rate' in segment_data else 0
            purchase_score = min(100, (segment_data['Total_Purchases'].mean() / 20) * 100) if 'Total_Purchases' in segment_data else 0
            engagement_score = segment_data['Web_Activity_Score'].mean() * 10 if 'Web_Activity_Score' in segment_data else 0
            
            # Overall health score (weighted average)
            health_score = (
                spending_score * 0.35 +
                response_score * 0.25 +
                purchase_score * 0.25 +
                engagement_score * 0.15
            )
            
            health_status = 'Excellent' if health_score >= 75 else 'Good' if health_score >= 60 else 'Fair' if health_score >= 40 else 'Poor'
            
            health_scores[f'segment_{segment}'] = {
                'overall_score': health_score,
                'status': health_status,
                'components': {
                    'spending': spending_score,
                    'response': response_score,
                    'purchase': purchase_score,
                    'engagement': engagement_score
                }
            }
            
            print(f"\nSegment {segment}:")
            print(f"  Overall Health: {health_score:.1f}/100 ({health_status})")
            print(f"  - Spending Score: {spending_score:.1f}")
            print(f"  - Response Score: {response_score:.1f}")
            print(f"  - Purchase Score: {purchase_score:.1f}")
            print(f"  - Engagement Score: {engagement_score:.1f}")
            
            # Generate alerts for poor health
            if health_score < 50:
                self.alerts.append({
                    'type': 'HEALTH',
                    'segment': f'segment_{segment}',
                    'severity': 'HIGH',
                    'message': f"Segment {segment} health is {health_status} ({health_score:.1f}/100)"
                })
        
        # Save health scores
        health_report = {
            'timestamp': datetime.now().isoformat(),
            'scores': health_scores
        }
        
        with open('segment_health.json', 'w') as f:
            json.dump(health_report, f, indent=2)
        
        print(f"\n✓ Health scores saved to 'segment_health.json'")
        
        return health_scores
    
    def generate_alerts_report(self):
        """Generate comprehensive alerts report"""
        if not self.alerts:
            print("\n✓ No alerts to report")
            return
        
        print("\n" + "="*70)
        print("ALERTS REPORT")
        print("="*70)
        
        # Group alerts by severity
        high_alerts = [a for a in self.alerts if a['severity'] == 'HIGH']
        medium_alerts = [a for a in self.alerts if a['severity'] == 'MEDIUM']
        
        if high_alerts:
            print(f"\n🔴 HIGH PRIORITY ALERTS ({len(high_alerts)}):")
            for alert in high_alerts:
                print(f"  • [{alert['type']}] {alert['message']}")
        
        if medium_alerts:
            print(f"\n🟡 MEDIUM PRIORITY ALERTS ({len(medium_alerts)}):")
            for alert in medium_alerts:
                print(f"  • [{alert['type']}] {alert['message']}")
        
        # Save alerts
        alerts_report = {
            'timestamp': datetime.now().isoformat(),
            'total_alerts': len(self.alerts),
            'high_priority': len(high_alerts),
            'medium_priority': len(medium_alerts),
            'alerts': self.alerts
        }
        
        with open('segment_alerts.json', 'w') as f:
            json.dump(alerts_report, f, indent=2)
        
        print(f"\n✓ Alerts saved to 'segment_alerts.json'")
        
        return alerts_report
    
    def create_monitoring_dashboard(self):
        """Create visual monitoring dashboard"""
        if self.df is None:
            return
        
        print("\n" + "="*70)
        print("CREATING MONITORING DASHBOARD")
        print("="*70)
        
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Segment Size Trend
        ax1 = fig.add_subplot(gs[0, :2])
        segment_sizes = self.df[self.cluster_col].value_counts().sort_index()
        ax1.bar(segment_sizes.index, segment_sizes.values, color='steelblue')
        ax1.set_title('Current Segment Sizes', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Segment')
        ax1.set_ylabel('Number of Customers')
        for i, v in enumerate(segment_sizes.values):
            ax1.text(segment_sizes.index[i], v, str(v), ha='center', va='bottom')
        
        # 2. Segment Value
        ax2 = fig.add_subplot(gs[0, 2])
        segment_value = self.df.groupby(self.cluster_col)['Total_Spending'].sum()
        colors = plt.cm.Set3(range(len(segment_value)))
        ax2.pie(segment_value.values, labels=[f'Seg {i}' for i in segment_value.index],
               autopct='%1.1f%%', colors=colors)
        ax2.set_title('Segment Value Distribution', fontweight='bold')
        
        # 3. Response Rate Trend
        ax3 = fig.add_subplot(gs[1, 0])
        response_rate = self.df.groupby(self.cluster_col)['Response_Rate'].mean()
        ax3.bar(response_rate.index, response_rate.values, color='coral')
        ax3.set_title('Response Rate by Segment', fontweight='bold')
        ax3.set_xlabel('Segment')
        ax3.set_ylabel('Response Rate')
        
        # 4. Average Spending
        ax4 = fig.add_subplot(gs[1, 1])
        avg_spending = self.df.groupby(self.cluster_col)['Total_Spending'].mean()
        ax4.bar(avg_spending.index, avg_spending.values, color='green')
        ax4.set_title('Avg Spending by Segment', fontweight='bold')
        ax4.set_xlabel('Segment')
        ax4.set_ylabel('Avg Spending ($)')
        
        # 5. Purchase Frequency
        ax5 = fig.add_subplot(gs[1, 2])
        avg_purchases = self.df.groupby(self.cluster_col)['Total_Purchases'].mean()
        ax5.bar(avg_purchases.index, avg_purchases.values, color='purple')
        ax5.set_title('Avg Purchases by Segment', fontweight='bold')
        ax5.set_xlabel('Segment')
        ax5.set_ylabel('Avg Purchases')
        
        # 6. Age Distribution
        ax6 = fig.add_subplot(gs[2, 0])
        for segment in sorted(self.df[self.cluster_col].unique()):
            segment_data = self.df[self.df[self.cluster_col] == segment]['Age']
            ax6.hist(segment_data, alpha=0.5, label=f'Seg {segment}', bins=15)
        ax6.set_title('Age Distribution by Segment', fontweight='bold')
        ax6.set_xlabel('Age')
        ax6.set_ylabel('Frequency')
        ax6.legend()
        
        # 7. Income Distribution
        ax7 = fig.add_subplot(gs[2, 1])
        self.df.boxplot(column='Income', by=self.cluster_col, ax=ax7)
        ax7.set_title('Income Distribution by Segment', fontweight='bold')
        ax7.set_xlabel('Segment')
        ax7.set_ylabel('Income ($)')
        plt.sca(ax7)
        
        # 8. Engagement Metrics
        ax8 = fig.add_subplot(gs[2, 2])
        web_activity = self.df.groupby(self.cluster_col)['Web_Activity_Score'].mean()
        ax8.bar(web_activity.index, web_activity.values, color='teal')
        ax8.set_title('Web Activity by Segment', fontweight='bold')
        ax8.set_xlabel('Segment')
        ax8.set_ylabel('Web Activity Score')
        
        plt.suptitle('Customer Segment Monitoring Dashboard', fontsize=18, fontweight='bold', y=0.995)
        plt.savefig('monitoring_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✓ Monitoring dashboard created and saved")
    
    def export_monitoring_report(self):
        """Export comprehensive monitoring report"""
        report = {
            'report_date': datetime.now().isoformat(),
            'summary': {
                'total_customers': len(self.df) if self.df is not None else 0,
                'total_segments': len(self.df[self.cluster_col].unique()) if self.df is not None else 0,
                'total_alerts': len(self.alerts)
            },
            'recommendations': self._generate_recommendations()
        }
        
        with open('monitoring_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✓ Monitoring report exported to 'monitoring_report.json'")
        
        return report
    
    def _generate_recommendations(self):
        """Generate actionable recommendations based on monitoring"""
        recommendations = []
        
        if self.df is None:
            return recommendations
        
        # Check for declining segments
        for segment in self.df[self.cluster_col].unique():
            segment_data = self.df[self.df[self.cluster_col] == segment]
            response_rate = segment_data['Response_Rate'].mean() if 'Response_Rate' in segment_data else 0
            
            if response_rate < 0.1:
                recommendations.append({
                    'segment': int(segment),
                    'priority': 'HIGH',
                    'action': 'Re-engagement Campaign',
                    'description': f'Segment {segment} has low response rate. Launch win-back campaign.'
                })
        
        return recommendations
    
    def run_full_monitoring(self):
        """Run complete monitoring analysis"""
        print("\n" + "="*70)
        print("SEGMENT MONITORING SYSTEM")
        print("="*70)
        
        self.create_baseline_snapshot()
        self.track_segment_changes()
        self.monitor_customer_migration()
        self.track_segment_health()
        self.generate_alerts_report()
        self.create_monitoring_dashboard()
        self.export_monitoring_report()
        
        print("\n" + "="*70)
        print("MONITORING COMPLETE!")
        print("="*70)


if __name__ == "__main__":
    monitor = SegmentMonitor()
    if monitor.df is not None:
        monitor.run_full_monitoring()
