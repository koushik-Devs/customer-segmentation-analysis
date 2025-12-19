"""
Test script to verify Streamlit app setup
Run this before launching the Streamlit app
"""

import os
import sys

def check_dependencies():
    """Check if all required packages are installed"""
    print("Checking dependencies...")
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'joblib',
        'sklearn'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("\n✓ All dependencies installed!")
    return True

def check_models():
    """Check if trained models exist"""
    print("\nChecking models...")
    
    if not os.path.exists('models'):
        print("✗ models/ directory not found")
        print("\n⚠️  Please train models first:")
        print("   python run_all_systems.py")
        return False
    
    required_files = [
        'models/kmeans_model.pkl',
        'models/best_classifier.pkl',
        'models/scaler.pkl',
        'models/feature_names.pkl'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            missing.append(file)
    
    if missing:
        print(f"\n⚠️  Missing model files: {len(missing)}")
        print("Train models with: python run_all_systems.py")
        return False
    
    print("\n✓ All model files found!")
    return True

def check_data():
    """Check if data file exists"""
    print("\nChecking data...")
    
    if os.path.exists('marketing_campaign_v.csv'):
        print("✓ marketing_campaign_v.csv found")
        return True
    else:
        print("✗ marketing_campaign_v.csv - MISSING")
        print("\n⚠️  Data file required for training")
        return False

def main():
    print("="*60)
    print("STREAMLIT APP SETUP VERIFICATION")
    print("="*60)
    
    deps_ok = check_dependencies()
    data_ok = check_data()
    models_ok = check_models()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    if deps_ok and models_ok:
        print("✅ Setup complete! Ready to run Streamlit app")
        print("\nRun the app with:")
        print("   streamlit run streamlit_app.py")
        return 0
    else:
        print("❌ Setup incomplete")
        
        if not deps_ok:
            print("\n1. Install dependencies:")
            print("   pip install -r requirements.txt")
        
        if not data_ok:
            print("\n2. Ensure data file exists:")
            print("   marketing_campaign_v.csv")
        
        if not models_ok:
            print("\n3. Train models:")
            print("   python run_all_systems.py")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
