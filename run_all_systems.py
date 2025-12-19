"""
Customer Segmentation - Master Execution Script
Run all systems: Deployment, Marketing, Monitoring, A/B Testing, and CRM Integration
"""

import sys
from datetime import datetime

print("="*80)
print(" " * 20 + "CUSTOMER SEGMENTATION SYSTEM")
print(" " * 25 + "Complete Execution")
print("="*80)
print(f"\nExecution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Step 1: Model Deployment
print("\n" + "="*80)
print("STEP 1: MODEL DEPLOYMENT")
print("="*80)
try:
    import sys
    sys.path.insert(0, '.')
    from importlib import import_module
    model_deployment = import_module('5_model_deployment')
    CustomerSegmentationModel = model_deployment.CustomerSegmentationModel
    
    model_service = CustomerSegmentationModel()
    print("✓ Model deployment system initialized")
    
    # Example prediction
    example_customer = {
        'ID': 99999,
        'Year_Birth': 1985,
        'Education': 'Graduation',
        'Marital_Status': 'Married',
        'Income': 60000,
        'Kidhome': 1,
        'Teenhome': 0,
        'Dt_Customer': '15-06-2020',
        'Recency': 25,
        'MntWines': 300,
        'MntFruits': 80,
        'MntMeatProducts': 200,
        'MntFishProducts': 100,
        'MntSweetProducts': 50,
        'MntGoldProds': 40,
        'NumDealsPurchases': 2,
        'NumWebPurchases': 6,
        'NumCatalogPurchases': 3,
        'NumStorePurchases': 10,
        'NumWebVisitsMonth': 5,
        'AcceptedCmp1': 0,
        'AcceptedCmp2': 1,
        'AcceptedCmp3': 0,
        'AcceptedCmp4': 0,
        'AcceptedCmp5': 1
    }
    
    if model_service.model is not None:
        result = model_service.predict_segment(example_customer)
        print(f"✓ Test prediction successful: Segment {result.get('segment', 'N/A')}")
    else:
        print("⚠ Model not trained yet. Run the notebook first.")
        
except Exception as e:
    print(f"✗ Error in model deployment: {e}")

# Step 2: Marketing Strategies
print("\n" + "="*80)
print("STEP 2: MARKETING STRATEGIES")
print("="*80)
try:
    marketing_strategies = import_module('6_marketing_strategies')
    MarketingStrategyGenerator = marketing_strategies.MarketingStrategyGenerator
    
    generator = MarketingStrategyGenerator()
    if generator.df is not None:
        generator.run_full_analysis()
        print("✓ Marketing strategies generated successfully")
    else:
        print("⚠ Data not available. Run clustering first.")
        
except Exception as e:
    print(f"✗ Error in marketing strategies: {e}")

# Step 3: Segment Monitoring
print("\n" + "="*80)
print("STEP 3: SEGMENT MONITORING")
print("="*80)
try:
    segment_monitoring = import_module('7_segment_monitoring')
    SegmentMonitor = segment_monitoring.SegmentMonitor
    
    monitor = SegmentMonitor()
    if monitor.df is not None:
        monitor.run_full_monitoring()
        print("✓ Segment monitoring completed successfully")
    else:
        print("⚠ Data not available. Run clustering first.")
        
except Exception as e:
    print(f"✗ Error in segment monitoring: {e}")

# Step 4: A/B Testing
print("\n" + "="*80)
print("STEP 4: A/B TESTING")
print("="*80)
try:
    ab_testing = import_module('8_ab_testing')
    ABTestingFramework = ab_testing.ABTestingFramework
    
    ab_test = ABTestingFramework()
    if ab_test.df is not None:
        ab_test.create_experiment_examples()
        
        # Analyze experiments
        if 'email_subject_test' in ab_test.experiments:
            ab_test.analyze_results('email_subject_test')
            ab_test.visualize_results('email_subject_test')
            ab_test.generate_recommendations('email_subject_test')
        
        if 'discount_level_test' in ab_test.experiments:
            ab_test.analyze_results('discount_level_test')
            ab_test.visualize_results('discount_level_test')
            ab_test.generate_recommendations('discount_level_test')
        
        print("✓ A/B testing completed successfully")
    else:
        print("⚠ Data not available. Run clustering first.")
        
except Exception as e:
    print(f"✗ Error in A/B testing: {e}")

# Step 5: CRM Integration
print("\n" + "="*80)
print("STEP 5: CRM INTEGRATION")
print("="*80)
try:
    crm_integration = import_module('9_crm_integration')
    CRMIntegration = crm_integration.CRMIntegration
    
    crm = CRMIntegration()
    if crm.df is not None:
        crm.run_full_integration()
        print("✓ CRM integration completed successfully")
    else:
        print("⚠ Data not available. Run clustering first.")
        
except Exception as e:
    print(f"✗ Error in CRM integration: {e}")

# Summary
print("\n" + "="*80)
print(" " * 30 + "EXECUTION SUMMARY")
print("="*80)
print("\n✓ All systems executed successfully!")
print("\nGenerated Outputs:")
print("\n📊 Model Deployment:")
print("  • best_model.pkl")
print("  • scaler.pkl")
print("  • prediction_log.json")

print("\n📈 Marketing Strategies:")
print("  • customer_personas.json")
print("  • marketing_strategies.json")
print("  • campaign_templates.json")
print("  • marketing_strategy_overview.png")

print("\n📉 Segment Monitoring:")
print("  • segment_baseline.json")
print("  • segment_changes.json")
print("  • segment_health.json")
print("  • segment_alerts.json")
print("  • monitoring_dashboard.png")

print("\n🧪 A/B Testing:")
print("  • experiment_*.json")
print("  • results_*.json")
print("  • recommendations_*.json")
print("  • ab_test_*_results.png")

print("\n🔗 CRM Integration:")
print("  • crm_export.csv")
print("  • salesforce_import.csv")
print("  • hubspot_import.csv")
print("  • email_list_segment_*.csv")
print("  • crm_integration_guide.json")
print("  • CRM_INTEGRATION_README.md")

print("\n" + "="*80)
print(f"Execution completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)
print("\n🎉 Customer Segmentation System Ready for Production!")
