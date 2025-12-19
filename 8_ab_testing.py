"""
Customer Segmentation - A/B Testing Framework
Design and analyze A/B tests for personalized campaigns
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime, timedelta
import json
import warnings
warnings.filterwarnings('ignore')


class ABTestingFramework:
    """A/B testing framework for personalized marketing campaigns"""
    
    def __init__(self, data_path='data_clustered.csv'):
        """Initialize with customer data"""
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
            
            self.experiments = {}
            self.results = {}
        except FileNotFoundError:
            print("⚠ Data file not found. Please run clustering first.")
            print("   Run: python 2_unsupervised_clustering.py")
            print("   Or execute Part 2 of customer_segmentation_analysis.ipynb")
            self.df = None
    
    def design_experiment(self, segment, test_name, variants, sample_size_per_variant=None):
        """
        Design an A/B test experiment
        
        Args:
            segment: Target customer segment
            test_name: Name of the experiment
            variants: List of variant descriptions
            sample_size_per_variant: Number of customers per variant
        """
        if self.df is None:
            return
        
        print("\n" + "="*70)
        print(f"DESIGNING EXPERIMENT: {test_name}")
        print("="*70)
        
        # Get segment customers
        segment_customers = self.df[self.df[self.cluster_col] == segment].copy()
        
        if len(segment_customers) == 0:
            print(f"⚠ No customers found in segment {segment}")
            return
        
        # Calculate sample size if not provided
        if sample_size_per_variant is None:
            # Use 20% of segment for testing
            total_test_size = int(len(segment_customers) * 0.2)
            sample_size_per_variant = total_test_size // len(variants)
        
        # Ensure we have enough customers
        total_needed = sample_size_per_variant * len(variants)
        if total_needed > len(segment_customers):
            sample_size_per_variant = len(segment_customers) // len(variants)
            print(f"⚠ Adjusted sample size to {sample_size_per_variant} per variant")
        
        # Randomly assign customers to variants
        segment_customers = segment_customers.sample(frac=1, random_state=42).reset_index(drop=True)
        
        assignments = []
        for i, variant in enumerate(variants):
            start_idx = i * sample_size_per_variant
            end_idx = start_idx + sample_size_per_variant
            variant_customers = segment_customers.iloc[start_idx:end_idx].copy()
            variant_customers['variant'] = variant['name']
            variant_customers['experiment'] = test_name
            assignments.append(variant_customers)
        
        experiment_df = pd.concat(assignments, ignore_index=True)
        
        experiment = {
            'name': test_name,
            'segment': segment,
            'variants': variants,
            'sample_size_per_variant': sample_size_per_variant,
            'total_sample_size': len(experiment_df),
            'start_date': datetime.now().isoformat(),
            'status': 'designed',
            'customers': experiment_df
        }
        
        self.experiments[test_name] = experiment
        
        print(f"\n✓ Experiment designed successfully")
        print(f"  Segment: {segment}")
        print(f"  Variants: {len(variants)}")
        print(f"  Sample size per variant: {sample_size_per_variant}")
        print(f"  Total customers: {len(experiment_df)}")
        
        # Save experiment design
        experiment_summary = {k: v for k, v in experiment.items() if k != 'customers'}
        with open(f'experiment_{test_name}.json', 'w') as f:
            json.dump(experiment_summary, f, indent=2, default=str)
        
        # Save customer assignments
        experiment_df.to_csv(f'experiment_{test_name}_assignments.csv', index=False)
        
        print(f"\n✓ Experiment saved to 'experiment_{test_name}.json'")
        print(f"✓ Assignments saved to 'experiment_{test_name}_assignments.csv'")
        
        return experiment
    
    def simulate_experiment_results(self, test_name, conversion_rates, avg_order_values):
        """
        Simulate experiment results (for demonstration)
        In production, this would come from actual campaign data
        
        Args:
            test_name: Name of the experiment
            conversion_rates: Dict of variant_name: conversion_rate
            avg_order_values: Dict of variant_name: avg_order_value
        """
        if test_name not in self.experiments:
            print(f"⚠ Experiment '{test_name}' not found")
            return
        
        experiment = self.experiments[test_name]
        customers_df = experiment['customers'].copy()
        
        print(f"\n{'='*70}")
        print(f"SIMULATING RESULTS: {test_name}")
        print(f"{'='*70}")
        
        # Simulate results for each variant
        for variant_name, conv_rate in conversion_rates.items():
            variant_mask = customers_df['variant'] == variant_name
            variant_customers = customers_df[variant_mask]
            
            # Simulate conversions
            n_customers = len(variant_customers)
            conversions = np.random.binomial(1, conv_rate, n_customers)
            customers_df.loc[variant_mask, 'converted'] = conversions
            
            # Simulate order values for converted customers
            avg_value = avg_order_values[variant_name]
            order_values = np.random.normal(avg_value, avg_value * 0.2, n_customers)
            order_values = np.maximum(order_values, 0)  # No negative values
            customers_df.loc[variant_mask, 'order_value'] = order_values * conversions
        
        experiment['customers'] = customers_df
        experiment['status'] = 'completed'
        experiment['end_date'] = datetime.now().isoformat()
        
        print(f"✓ Results simulated for {len(customers_df)} customers")
        
        return customers_df
    
    def analyze_results(self, test_name, confidence_level=0.95):
        """
        Analyze A/B test results with statistical significance
        
        Args:
            test_name: Name of the experiment
            confidence_level: Confidence level for statistical tests
        """
        if test_name not in self.experiments:
            print(f"⚠ Experiment '{test_name}' not found")
            return
        
        experiment = self.experiments[test_name]
        
        if experiment['status'] != 'completed':
            print(f"⚠ Experiment '{test_name}' not completed yet")
            return
        
        customers_df = experiment['customers']
        
        print(f"\n{'='*70}")
        print(f"ANALYZING RESULTS: {test_name}")
        print(f"{'='*70}")
        
        results = {
            'experiment': test_name,
            'segment': experiment['segment'],
            'analysis_date': datetime.now().isoformat(),
            'variants': {}
        }
        
        # Calculate metrics for each variant
        print("\nVariant Performance:")
        print("-" * 70)
        
        variant_stats = []
        
        for variant in experiment['variants']:
            variant_name = variant['name']
            variant_data = customers_df[customers_df['variant'] == variant_name]
            
            n_customers = len(variant_data)
            n_conversions = int(variant_data['converted'].sum()) if 'converted' in variant_data.columns else 0
            conversion_rate = n_conversions / n_customers if n_customers > 0 else 0
            
            total_revenue = float(variant_data['order_value'].sum()) if 'order_value' in variant_data.columns else 0
            converted_data = variant_data[variant_data['converted'] == 1]['order_value'] if 'converted' in variant_data.columns and 'order_value' in variant_data.columns else pd.Series([])
            avg_order_value = float(converted_data.mean()) if len(converted_data) > 0 and not converted_data.isna().all() else 0
            revenue_per_customer = total_revenue / n_customers if n_customers > 0 else 0
            
            variant_results = {
                'name': variant_name,
                'description': variant['description'],
                'customers': n_customers,
                'conversions': n_conversions,
                'conversion_rate': float(conversion_rate),
                'total_revenue': float(total_revenue),
                'avg_order_value': float(avg_order_value),
                'revenue_per_customer': float(revenue_per_customer)
            }
            
            results['variants'][variant_name] = variant_results
            variant_stats.append(variant_results)
            
            print(f"\n{variant_name}:")
            print(f"  Customers: {n_customers}")
            print(f"  Conversions: {n_conversions} ({conversion_rate:.2%})")
            print(f"  Avg Order Value: ${avg_order_value:.2f}")
            print(f"  Revenue per Customer: ${revenue_per_customer:.2f}")
            print(f"  Total Revenue: ${total_revenue:.2f}")
        
        # Statistical significance testing
        print(f"\n{'='*70}")
        print("STATISTICAL SIGNIFICANCE TESTS")
        print(f"{'='*70}")
        
        # Compare all variants pairwise
        variant_names = [v['name'] for v in experiment['variants']]
        
        if len(variant_names) >= 2:
            control = variant_names[0]
            
            for variant_name in variant_names[1:]:
                self._compare_variants(
                    customers_df, control, variant_name, 
                    confidence_level, results
                )
        
        # Determine winner
        best_variant = max(variant_stats, key=lambda x: x['revenue_per_customer'])
        results['winner'] = best_variant['name']
        results['winner_lift'] = self._calculate_lift(variant_stats, best_variant['name'])
        
        print(f"\n{'='*70}")
        print(f"🏆 WINNER: {best_variant['name']}")
        print(f"{'='*70}")
        print(f"  Conversion Rate: {best_variant['conversion_rate']:.2%}")
        print(f"  Revenue per Customer: ${best_variant['revenue_per_customer']:.2f}")
        print(f"  Lift vs Control: {results['winner_lift']:.1f}%")
        
        self.results[test_name] = results
        
        # Save results
        with open(f'results_{test_name}.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n✓ Results saved to 'results_{test_name}.json'")
        
        return results
    
    def _compare_variants(self, df, control_name, variant_name, confidence_level, results):
        """Compare two variants statistically"""
        control_data = df[df['variant'] == control_name]
        variant_data = df[df['variant'] == variant_name]
        
        # Conversion rate comparison (Chi-square test)
        control_conversions = int(control_data['converted'].sum()) if 'converted' in control_data.columns else 0
        control_total = len(control_data)
        variant_conversions = int(variant_data['converted'].sum()) if 'converted' in variant_data.columns else 0
        variant_total = len(variant_data)
        
        contingency_table = np.array([
            [control_conversions, control_total - control_conversions],
            [variant_conversions, variant_total - variant_conversions]
        ])
        
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        is_significant = p_value < (1 - confidence_level)
        
        control_rate = control_conversions / control_total if control_total > 0 else 0
        variant_rate = variant_conversions / variant_total if variant_total > 0 else 0
        lift = ((variant_rate - control_rate) / control_rate * 100) if control_rate > 0 else 0
        
        print(f"\n{control_name} vs {variant_name}:")
        print(f"  Conversion Rate: {control_rate:.2%} vs {variant_rate:.2%}")
        print(f"  Lift: {lift:+.1f}%")
        print(f"  P-value: {p_value:.4f}")
        print(f"  Statistically Significant: {'✓ YES' if is_significant else '✗ NO'}")
        
        # Revenue comparison (T-test)
        control_revenue = control_data['order_value'] if 'order_value' in control_data.columns else pd.Series([0])
        variant_revenue = variant_data['order_value'] if 'order_value' in variant_data.columns else pd.Series([0])
        
        if len(control_revenue) > 1 and len(variant_revenue) > 1:
            t_stat, t_pvalue = stats.ttest_ind(control_revenue, variant_revenue)
            revenue_significant = t_pvalue < (1 - confidence_level)
        else:
            revenue_significant = False
        
        print(f"  Revenue Difference Significant: {'✓ YES' if revenue_significant else '✗ NO'}")
        
        # Store comparison
        comparison_key = f"{control_name}_vs_{variant_name}"
        results[comparison_key] = {
            'lift': float(lift),
            'p_value': float(p_value),
            'is_significant': bool(is_significant),
            'confidence_level': float(confidence_level)
        }
    
    def _calculate_lift(self, variant_stats, winner_name):
        """Calculate lift of winner vs control"""
        control = variant_stats[0]
        winner = next(v for v in variant_stats if v['name'] == winner_name)
        
        if control['revenue_per_customer'] > 0:
            lift = ((winner['revenue_per_customer'] - control['revenue_per_customer']) / 
                   control['revenue_per_customer'] * 100)
        else:
            lift = 0
        
        return lift
    
    def visualize_results(self, test_name):
        """Create visualizations for A/B test results"""
        if test_name not in self.results:
            print(f"⚠ No results found for '{test_name}'")
            return
        
        results = self.results[test_name]
        experiment = self.experiments[test_name]
        customers_df = experiment['customers']
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'A/B Test Results: {test_name}', fontsize=16, fontweight='bold')
        
        variants = list(results['variants'].keys())
        
        # 1. Conversion Rate Comparison
        conv_rates = [results['variants'][v]['conversion_rate'] * 100 for v in variants]
        colors = ['steelblue' if v != results['winner'] else 'gold' for v in variants]
        axes[0, 0].bar(variants, conv_rates, color=colors)
        axes[0, 0].set_title('Conversion Rate by Variant', fontweight='bold')
        axes[0, 0].set_ylabel('Conversion Rate (%)')
        axes[0, 0].set_xlabel('Variant')
        for i, v in enumerate(conv_rates):
            axes[0, 0].text(i, v, f'{v:.1f}%', ha='center', va='bottom')
        
        # 2. Revenue per Customer
        revenue_per_cust = [results['variants'][v]['revenue_per_customer'] for v in variants]
        axes[0, 1].bar(variants, revenue_per_cust, color=colors)
        axes[0, 1].set_title('Revenue per Customer', fontweight='bold')
        axes[0, 1].set_ylabel('Revenue ($)')
        axes[0, 1].set_xlabel('Variant')
        for i, v in enumerate(revenue_per_cust):
            axes[0, 1].text(i, v, f'${v:.2f}', ha='center', va='bottom')
        
        # 3. Total Revenue
        total_revenue = [results['variants'][v]['total_revenue'] for v in variants]
        axes[1, 0].bar(variants, total_revenue, color=colors)
        axes[1, 0].set_title('Total Revenue by Variant', fontweight='bold')
        axes[1, 0].set_ylabel('Total Revenue ($)')
        axes[1, 0].set_xlabel('Variant')
        
        # 4. Order Value Distribution
        for variant in variants:
            if 'variant' in customers_df.columns and 'converted' in customers_df.columns and 'order_value' in customers_df.columns:
                variant_data = customers_df[
                    (customers_df['variant'] == variant) & 
                    (customers_df['converted'] == 1)
                ]['order_value']
                if len(variant_data) > 0:
                    axes[1, 1].hist(variant_data, alpha=0.6, label=variant, bins=20)
        axes[1, 1].set_title('Order Value Distribution', fontweight='bold')
        axes[1, 1].set_xlabel('Order Value ($)')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].legend()
        
        plt.tight_layout()
        plt.savefig(f'ab_test_{test_name}_results.png', dpi=300, bbox_inches='tight')
        try:
            plt.show()
        except:
            plt.close()
        
        print(f"✓ Visualization saved to 'ab_test_{test_name}_results.png'")
    
    def generate_recommendations(self, test_name):
        """Generate actionable recommendations based on test results"""
        if test_name not in self.results:
            print(f"⚠ No results found for '{test_name}'")
            return
        
        results = self.results[test_name]
        
        print(f"\n{'='*70}")
        print(f"RECOMMENDATIONS: {test_name}")
        print(f"{'='*70}")
        
        recommendations = []
        
        winner = results['winner']
        lift = results['winner_lift']
        
        # Primary recommendation
        if lift > 10:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'IMPLEMENT',
                'description': f"Roll out '{winner}' to entire segment. Expected lift: {lift:.1f}%"
            })
        elif lift > 0:
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'CONSIDER',
                'description': f"'{winner}' shows positive results. Consider broader testing."
            })
        else:
            recommendations.append({
                'priority': 'LOW',
                'action': 'ITERATE',
                'description': "No clear winner. Design new variants and retest."
            })
        
        # Additional insights
        winner_data = results['variants'][winner]
        if winner_data['conversion_rate'] < 0.15:
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'OPTIMIZE',
                'description': "Conversion rate is low. Consider improving offer or targeting."
            })
        
        if winner_data['avg_order_value'] > 100:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'UPSELL',
                'description': "High order values detected. Implement upsell strategies."
            })
        
        print("\nActionable Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. [{rec['priority']}] {rec['action']}")
            print(f"   {rec['description']}")
        
        # Save recommendations
        results['recommendations'] = recommendations
        with open(f'recommendations_{test_name}.json', 'w') as f:
            json.dump(recommendations, f, indent=2)
        
        print(f"\n✓ Recommendations saved to 'recommendations_{test_name}.json'")
        
        return recommendations
    
    def create_experiment_examples(self):
        """Create example A/B test experiments"""
        print("\n" + "="*70)
        print("CREATING EXAMPLE A/B TESTS")
        print("="*70)
        
        if self.df is None:
            return
        
        # Example 1: Email Subject Line Test
        segments = self.df[self.cluster_col].unique()
        if len(segments) > 0:
            test1 = self.design_experiment(
                segment=segments[0],
                test_name="email_subject_test",
                variants=[
                    {'name': 'Control', 'description': 'Standard subject line'},
                    {'name': 'Personalized', 'description': 'Personalized with name'},
                    {'name': 'Urgency', 'description': 'Limited time offer'}
                ],
                sample_size_per_variant=100
            )
            
            # Simulate results
            self.simulate_experiment_results(
                'email_subject_test',
                conversion_rates={'Control': 0.12, 'Personalized': 0.18, 'Urgency': 0.15},
                avg_order_values={'Control': 85, 'Personalized': 95, 'Urgency': 80}
            )
        
        # Example 2: Discount Level Test
        if len(segments) > 1:
            test2 = self.design_experiment(
                segment=segments[1],
                test_name="discount_level_test",
                variants=[
                    {'name': 'No_Discount', 'description': 'No discount'},
                    {'name': 'Discount_10', 'description': '10% discount'},
                    {'name': 'Discount_20', 'description': '20% discount'}
                ],
                sample_size_per_variant=100
            )
            
            # Simulate results
            self.simulate_experiment_results(
                'discount_level_test',
                conversion_rates={'No_Discount': 0.10, 'Discount_10': 0.16, 'Discount_20': 0.22},
                avg_order_values={'No_Discount': 100, 'Discount_10': 90, 'Discount_20': 80}
            )
        
        print("\n✓ Example experiments created")


if __name__ == "__main__":
    ab_test = ABTestingFramework()
    
    if ab_test.df is not None:
        # Create and analyze example experiments
        ab_test.create_experiment_examples()
        
        # Analyze first experiment
        if 'email_subject_test' in ab_test.experiments:
            ab_test.analyze_results('email_subject_test')
            ab_test.visualize_results('email_subject_test')
            ab_test.generate_recommendations('email_subject_test')
        
        # Analyze second experiment
        if 'discount_level_test' in ab_test.experiments:
            ab_test.analyze_results('discount_level_test')
            ab_test.visualize_results('discount_level_test')
            ab_test.generate_recommendations('discount_level_test')
