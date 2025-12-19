"""
Customer Segmentation - CRM Integration
Export insights and integrate with CRM systems
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime
import csv
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')


class CRMIntegration:
    """Integrate customer segmentation insights with CRM systems"""
    
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
        except FileNotFoundError:
            print("⚠ Data file not found. Please run clustering first.")
            print("   Run: python 2_unsupervised_clustering.py")
            print("   Or execute Part 2 of customer_segmentation_analysis.ipynb")
            self.df = None
    
    def create_crm_export(self):
        """Create comprehensive CRM export file"""
        if self.df is None:
            return
        
        print("\n" + "="*70)
        print("CREATING CRM EXPORT")
        print("="*70)
        
        # Select key fields for CRM
        crm_fields = [
            'ID', 'Year_Birth', 'Education', 'Marital_Status', 'Income',
            'Kidhome', 'Teenhome', 'Dt_Customer', 'Recency',
            'Total_Spending', 'Total_Purchases', 'Total_Campaigns_Accepted',
            'Response_Rate', 'Cluster', 'Age', 'Family_Size'
        ]
        
        available_fields = [f for f in crm_fields if f in self.df.columns]
        crm_export = self.df[available_fields].copy()
        
        # Add segment names
        segment_names = {
            0: "Budget Conscious",
            1: "High Value",
            2: "Average Spender",
            3: "Premium Customer"
        }
        crm_export['Segment_Name'] = crm_export[self.cluster_col].map(
            lambda x: segment_names.get(x, f"Segment {x}")
        )
        
        # Add customer value tier
        spending_quartiles = crm_export['Total_Spending'].quantile([0.25, 0.5, 0.75])
        crm_export['Value_Tier'] = pd.cut(
            crm_export['Total_Spending'],
            bins=[-np.inf, spending_quartiles[0.25], spending_quartiles[0.5], 
                  spending_quartiles[0.75], np.inf],
            labels=['Bronze', 'Silver', 'Gold', 'Platinum']
        )
        
        # Add engagement score
        if 'Response_Rate' in crm_export.columns:
            crm_export['Engagement_Score'] = pd.cut(
                crm_export['Response_Rate'],
                bins=[-np.inf, 0.1, 0.2, 0.3, np.inf],
                labels=['Low', 'Medium', 'High', 'Very High']
            )
        
        # Add recommended actions
        crm_export['Recommended_Action'] = crm_export.apply(
            self._get_recommended_action, axis=1
        )
        
        # Add next best action
        crm_export['Next_Best_Action'] = crm_export.apply(
            self._get_next_best_action, axis=1
        )
        
        # Add campaign priority
        crm_export['Campaign_Priority'] = crm_export.apply(
            self._calculate_priority, axis=1
        )
        
        # Export to CSV
        crm_export.to_csv('crm_export.csv', index=False)
        print(f"✓ CRM export created: {len(crm_export)} customers")
        print(f"✓ Saved to 'crm_export.csv'")
        
        # Create summary statistics
        self._create_export_summary(crm_export)
        
        return crm_export
    
    def _get_recommended_action(self, row):
        """Determine recommended action for customer"""
        if 'Total_Spending' not in row or 'Response_Rate' not in row:
            return "Review Profile"
        
        spending = row['Total_Spending']
        response_rate = row['Response_Rate']
        
        if spending > 1000 and response_rate > 0.3:
            return "VIP Engagement"
        elif spending > 500 and response_rate < 0.1:
            return "Re-engagement Campaign"
        elif spending < 200 and response_rate > 0.2:
            return "Upsell Opportunity"
        elif response_rate < 0.1:
            return "Win-back Campaign"
        else:
            return "Standard Campaign"
    
    def _get_next_best_action(self, row):
        """Determine next best action"""
        if 'Total_Campaigns_Accepted' not in row:
            return "Send Welcome Email"
        
        campaigns_accepted = row['Total_Campaigns_Accepted']
        
        if campaigns_accepted == 0:
            return "Send Personalized Offer"
        elif campaigns_accepted >= 3:
            return "Loyalty Program Invitation"
        else:
            return "Product Recommendation"
    
    def _calculate_priority(self, row):
        """Calculate campaign priority"""
        if 'Total_Spending' not in row or 'Response_Rate' not in row:
            return "Medium"
        
        spending = row['Total_Spending']
        response_rate = row['Response_Rate']
        
        score = (spending / 100) + (response_rate * 100)
        
        if score > 15:
            return "High"
        elif score > 5:
            return "Medium"
        else:
            return "Low"
    
    def _create_export_summary(self, crm_export):
        """Create summary of CRM export"""
        summary = {
            'export_date': datetime.now().isoformat(),
            'total_customers': len(crm_export),
            'segments': crm_export['Segment_Name'].value_counts().to_dict(),
            'value_tiers': crm_export['Value_Tier'].value_counts().to_dict(),
            'campaign_priorities': crm_export['Campaign_Priority'].value_counts().to_dict(),
            'recommended_actions': crm_export['Recommended_Action'].value_counts().to_dict()
        }
        
        with open('crm_export_summary.json', 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print("✓ Export summary saved to 'crm_export_summary.json'")
    
    def create_salesforce_import(self):
        """Create Salesforce-compatible import file"""
        if self.df is None:
            return
        
        print("\n" + "="*70)
        print("CREATING SALESFORCE IMPORT")
        print("="*70)
        
        # Salesforce field mapping
        salesforce_data = pd.DataFrame({
            'Customer_ID__c': self.df['ID'] if 'ID' in self.df else range(len(self.df)),
            'Segment__c': self.df[self.cluster_col],
            'Segment_Name__c': self.df[self.cluster_col].map(
                lambda x: f"Segment_{x}"
            ),
            'Total_Spending__c': self.df['Total_Spending'] if 'Total_Spending' in self.df else 0,
            'Total_Purchases__c': self.df['Total_Purchases'] if 'Total_Purchases' in self.df else 0,
            'Response_Rate__c': self.df['Response_Rate'] if 'Response_Rate' in self.df else 0,
            'Last_Purchase_Days__c': self.df['Recency'] if 'Recency' in self.df else 0,
            'Customer_Since__c': self.df['Dt_Customer'] if 'Dt_Customer' in self.df else '',
            'Lifetime_Value__c': self.df['Total_Spending'] if 'Total_Spending' in self.df else 0,
            'Engagement_Level__c': self._calculate_engagement_level(self.df),
            'Next_Action__c': self.df.apply(self._get_next_best_action, axis=1),
            'Last_Updated__c': datetime.now().strftime('%Y-%m-%d')
        })
        
        salesforce_data.to_csv('salesforce_import.csv', index=False)
        print(f"✓ Salesforce import file created: {len(salesforce_data)} records")
        print(f"✓ Saved to 'salesforce_import.csv'")
        
        return salesforce_data
    
    def create_hubspot_import(self):
        """Create HubSpot-compatible import file"""
        if self.df is None:
            return
        
        print("\n" + "="*70)
        print("CREATING HUBSPOT IMPORT")
        print("="*70)
        
        # HubSpot field mapping
        hubspot_data = pd.DataFrame({
            'Email': self.df['ID'].apply(lambda x: f"customer{x}@example.com") if 'ID' in self.df else '',
            'Customer Segment': self.df[self.cluster_col],
            'Segment Name': self.df[self.cluster_col].map(lambda x: f"Segment_{x}"),
            'Total Spending': self.df['Total_Spending'] if 'Total_Spending' in self.df else 0,
            'Total Purchases': self.df['Total_Purchases'] if 'Total_Purchases' in self.df else 0,
            'Response Rate': self.df['Response_Rate'] if 'Response_Rate' in self.df else 0,
            'Lifecycle Stage': self._determine_lifecycle_stage(self.df),
            'Lead Score': self._calculate_lead_score(self.df),
            'Last Contact Date': datetime.now().strftime('%Y-%m-%d'),
            'Next Follow Up': self._calculate_next_followup(self.df)
        })
        
        hubspot_data.to_csv('hubspot_import.csv', index=False)
        print(f"✓ HubSpot import file created: {len(hubspot_data)} records")
        print(f"✓ Saved to 'hubspot_import.csv'")
        
        return hubspot_data
    
    def _calculate_engagement_level(self, df):
        """Calculate engagement level"""
        if 'Response_Rate' not in df.columns:
            return 'Unknown'
        
        return df['Response_Rate'].apply(
            lambda x: 'High' if x > 0.3 else 'Medium' if x > 0.15 else 'Low'
        )
    
    def _determine_lifecycle_stage(self, df):
        """Determine customer lifecycle stage"""
        if 'Total_Purchases' not in df.columns:
            return 'Lead'
        
        return df['Total_Purchases'].apply(
            lambda x: 'Customer' if x > 5 else 'Opportunity' if x > 0 else 'Lead'
        )
    
    def _calculate_lead_score(self, df):
        """Calculate lead score (0-100)"""
        score = 0
        
        if 'Total_Spending' in df.columns:
            score += (df['Total_Spending'] / 20).clip(0, 40)
        
        if 'Response_Rate' in df.columns:
            score += (df['Response_Rate'] * 100).clip(0, 30)
        
        if 'Total_Purchases' in df.columns:
            score += (df['Total_Purchases'] * 3).clip(0, 30)
        
        return score.round(0).astype(int)
    
    def _calculate_next_followup(self, df):
        """Calculate next follow-up date"""
        if 'Recency' not in df.columns:
            return (datetime.now() + pd.Timedelta(days=7)).strftime('%Y-%m-%d')
        
        return df['Recency'].apply(
            lambda x: (datetime.now() + pd.Timedelta(days=3 if x > 60 else 7 if x > 30 else 14)).strftime('%Y-%m-%d')
        )
    
    def create_email_marketing_lists(self):
        """Create segmented email marketing lists"""
        if self.df is None:
            return
        
        print("\n" + "="*70)
        print("CREATING EMAIL MARKETING LISTS")
        print("="*70)
        
        lists = {}
        
        for segment in sorted(self.df[self.cluster_col].unique()):
            segment_data = self.df[self.df[self.cluster_col] == segment].copy()
            
            # Create email list
            email_list = pd.DataFrame({
                'customer_id': segment_data['ID'] if 'ID' in segment_data else range(len(segment_data)),
                'email': segment_data['ID'].apply(lambda x: f"customer{x}@example.com") if 'ID' in segment_data else '',
                'first_name': 'Customer',
                'segment': segment,
                'total_spending': segment_data['Total_Spending'] if 'Total_Spending' in segment_data else 0,
                'response_rate': segment_data['Response_Rate'] if 'Response_Rate' in segment_data else 0,
                'preferred_channel': self._determine_preferred_channel(segment_data),
                'send_frequency': self._determine_send_frequency(segment_data),
                'best_send_time': '10:00 AM',  # Could be personalized
                'tags': f"segment_{segment},active"
            })
            
            filename = f'email_list_segment_{segment}.csv'
            email_list.to_csv(filename, index=False)
            lists[f'segment_{segment}'] = len(email_list)
            
            print(f"✓ Created email list for Segment {segment}: {len(email_list)} customers")
            print(f"  Saved to '{filename}'")
        
        # Create master list summary
        summary = {
            'created_date': datetime.now().isoformat(),
            'total_lists': len(lists),
            'lists': lists,
            'total_contacts': sum(lists.values())
        }
        
        with open('email_lists_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✓ Created {len(lists)} email marketing lists")
        print(f"✓ Summary saved to 'email_lists_summary.json'")
        
        return lists
    
    def _determine_preferred_channel(self, segment_data):
        """Determine preferred marketing channel"""
        if 'Web_Activity_Score' in segment_data.columns:
            return segment_data['Web_Activity_Score'].apply(
                lambda x: 'Email' if x > 5 else 'Direct Mail'
            )
        return 'Email'
    
    def _determine_send_frequency(self, segment_data):
        """Determine optimal send frequency"""
        if 'Response_Rate' in segment_data.columns:
            return segment_data['Response_Rate'].apply(
                lambda x: 'Weekly' if x > 0.3 else 'Bi-weekly' if x > 0.15 else 'Monthly'
            )
        return 'Bi-weekly'
    
    def create_api_payload(self, customer_id):
        """Create API payload for real-time CRM updates"""
        if self.df is None:
            return None
        
        customer = self.df[self.df['ID'] == customer_id].iloc[0] if 'ID' in self.df.columns else None
        
        if customer is None:
            return None
        
        payload = {
            'customer_id': int(customer_id),
            'segment': int(customer[self.cluster_col]),
            'segment_name': f"Segment_{customer[self.cluster_col]}",
            'profile': {
                'total_spending': float(customer['Total_Spending']) if 'Total_Spending' in customer else 0,
                'total_purchases': int(customer['Total_Purchases']) if 'Total_Purchases' in customer else 0,
                'response_rate': float(customer['Response_Rate']) if 'Response_Rate' in customer else 0,
                'age': int(customer['Age']) if 'Age' in customer else 0,
                'income': float(customer['Income']) if 'Income' in customer else 0
            },
            'recommendations': {
                'next_action': self._get_next_best_action(customer),
                'campaign_priority': self._calculate_priority(customer),
                'preferred_channel': 'Email',
                'optimal_send_time': '10:00 AM'
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return payload
    
    def generate_integration_documentation(self):
        """Generate documentation for CRM integration"""
        print("\n" + "="*70)
        print("GENERATING INTEGRATION DOCUMENTATION")
        print("="*70)
        
        documentation = {
            'title': 'Customer Segmentation CRM Integration Guide',
            'version': '1.0',
            'last_updated': datetime.now().isoformat(),
            'overview': 'This guide explains how to integrate customer segmentation insights into your CRM system.',
            'exports': {
                'crm_export.csv': {
                    'description': 'Comprehensive customer export with segments and recommendations',
                    'fields': [
                        'ID', 'Segment', 'Segment_Name', 'Total_Spending', 
                        'Value_Tier', 'Recommended_Action', 'Campaign_Priority'
                    ],
                    'update_frequency': 'Weekly'
                },
                'salesforce_import.csv': {
                    'description': 'Salesforce-compatible import file',
                    'object': 'Contact',
                    'import_method': 'Data Loader or Import Wizard'
                },
                'hubspot_import.csv': {
                    'description': 'HubSpot-compatible import file',
                    'import_method': 'Contacts > Import'
                },
                'email_list_segment_*.csv': {
                    'description': 'Segmented email marketing lists',
                    'use_case': 'Email campaign targeting'
                }
            },
            'api_integration': {
                'endpoint': '/api/customer-segment',
                'method': 'GET',
                'parameters': ['customer_id'],
                'response_format': 'JSON',
                'example': self.create_api_payload(12345) if self.df is not None else {}
            },
            'automation_workflows': [
                {
                    'name': 'New Customer Segmentation',
                    'trigger': 'New customer created',
                    'action': 'Assign segment and send welcome campaign'
                },
                {
                    'name': 'Segment Migration Alert',
                    'trigger': 'Customer moves to different segment',
                    'action': 'Update CRM and trigger appropriate campaign'
                },
                {
                    'name': 'Re-engagement Campaign',
                    'trigger': 'Customer inactive for 60 days',
                    'action': 'Send personalized re-engagement offer'
                }
            ],
            'best_practices': [
                'Update customer segments weekly',
                'Monitor segment migration patterns',
                'Personalize campaigns based on segment characteristics',
                'Track campaign performance by segment',
                'Adjust strategies based on A/B test results'
            ]
        }
        
        with open('crm_integration_guide.json', 'w') as f:
            json.dump(documentation, f, indent=2)
        
        print("✓ Integration documentation created")
        print("✓ Saved to 'crm_integration_guide.json'")
        
        # Create README
        self._create_readme()
        
        return documentation
    
    def _create_readme(self):
        """Create README file for CRM integration"""
        readme_content = """# Customer Segmentation CRM Integration

## Overview
This package contains customer segmentation data and integration files for your CRM system.

## Files Included

### 1. crm_export.csv
Comprehensive customer export with segmentation data, value tiers, and recommended actions.

**Key Fields:**
- `ID`: Customer identifier
- `Segment`: Numeric segment ID
- `Segment_Name`: Descriptive segment name
- `Value_Tier`: Customer value classification (Bronze/Silver/Gold/Platinum)
- `Recommended_Action`: Suggested marketing action
- `Campaign_Priority`: Priority level for campaigns

### 2. salesforce_import.csv
Salesforce-compatible import file for Contact object.

**Import Instructions:**
1. Log into Salesforce
2. Go to Setup > Data > Data Loader
3. Select "Insert" or "Update"
4. Choose Contact object
5. Map fields and import

### 3. hubspot_import.csv
HubSpot-compatible import file.

**Import Instructions:**
1. Go to Contacts > Import
2. Upload hubspot_import.csv
3. Map fields to HubSpot properties
4. Complete import

### 4. email_list_segment_*.csv
Segmented email marketing lists for targeted campaigns.

**Usage:**
- Import into your email marketing platform
- Use for segment-specific campaigns
- Respect send frequency recommendations

## API Integration

For real-time segment lookups, use the provided API payload format:

```json
{
  "customer_id": 12345,
  "segment": 2,
  "segment_name": "Segment_2",
  "recommendations": {
    "next_action": "Product Recommendation",
    "campaign_priority": "High"
  }
}
```

## Automation Workflows

### Recommended Workflows:
1. **New Customer**: Automatically assign segment on creation
2. **Segment Migration**: Alert when customers change segments
3. **Re-engagement**: Trigger campaigns for inactive customers

## Best Practices

1. **Update Frequency**: Refresh segments weekly
2. **Campaign Personalization**: Tailor messaging by segment
3. **Performance Tracking**: Monitor KPIs by segment
4. **A/B Testing**: Test strategies within segments
5. **Continuous Improvement**: Iterate based on results

## Support

For questions or issues, refer to the integration guide or contact your data team.

---
Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open('CRM_INTEGRATION_README.md', 'w') as f:
            f.write(readme_content)
        
        print("✓ README created: 'CRM_INTEGRATION_README.md'")
    
    def run_full_integration(self):
        """Run complete CRM integration process"""
        print("\n" + "="*70)
        print("CRM INTEGRATION SYSTEM")
        print("="*70)
        
        self.create_crm_export()
        self.create_salesforce_import()
        self.create_hubspot_import()
        self.create_email_marketing_lists()
        self.generate_integration_documentation()
        
        print("\n" + "="*70)
        print("CRM INTEGRATION COMPLETE!")
        print("="*70)
        print("\nGenerated Files:")
        print("  • crm_export.csv")
        print("  • salesforce_import.csv")
        print("  • hubspot_import.csv")
        print("  • email_list_segment_*.csv")
        print("  • crm_integration_guide.json")
        print("  • CRM_INTEGRATION_README.md")
        print("\n✓ All files ready for CRM import")


if __name__ == "__main__":
    crm = CRMIntegration()
    if crm.df is not None:
        crm.run_full_integration()
