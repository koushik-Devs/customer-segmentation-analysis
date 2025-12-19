#!/usr/bin/env python3
"""
Complete setup and launch script for Customer Segmentation System
This script handles everything: checking dependencies, training models, and launching the app
"""

import os
import sys
import subprocess
import time

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_step(step_num, text):
    """Print a step indicator"""
    print(f"\n{'='*70}")
    print(f"STEP {step_num}: {text}")
    print(f"{'='*70}\n")

def check_python_version():
    """Check if Python version is adequate"""
    print_step(1, "Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    
    print("✅ Python version is adequate")
    return True

def check_data_file():
    """Check if data file exists"""
    print_step(2, "Checking Data File")
    
    if os.path.exists('marketing_campaign_v.csv'):
        print("✅ Data file found: marketing_campaign_v.csv")
        return True
    else:
        print("❌ Data file not found: marketing_campaign_v.csv")
        print("\nPlease ensure the data file is in the current directory.")
        return False

def install_dependencies():
    """Install required dependencies"""
    print_step(3, "Installing Dependencies")
    
    print("Installing packages from requirements.txt...")
    print("This may take a few minutes...\n")
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ All dependencies installed successfully!")
            return True
        else:
            print("❌ Failed to install dependencies")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def train_models():
    """Train all models"""
    print_step(4, "Training Models")
    
    if os.path.exists('models') and all(os.path.exists(f'models/{f}') for f in 
        ['kmeans_model.pkl', 'best_classifier.pkl', 'scaler.pkl', 'feature_names.pkl']):
        
        print("Models already exist!")
        response = input("Do you want to retrain? (y/N): ").strip().lower()
        
        if response != 'y':
            print("✅ Using existing models")
            return True
    
    print("Training models... This will take 5-10 minutes.")
    print("Please wait...\n")
    
    try:
        result = subprocess.run(
            [sys.executable, 'run_all_systems.py'],
            capture_output=False
        )
        
        if result.returncode == 0:
            print("\n✅ Models trained successfully!")
            return True
        else:
            print("\n❌ Model training failed")
            return False
    except Exception as e:
        print(f"\n❌ Error training models: {e}")
        return False

def verify_setup():
    """Verify the complete setup"""
    print_step(5, "Verifying Setup")
    
    try:
        result = subprocess.run(
            [sys.executable, 'test_streamlit_setup.py'],
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            print("✅ Setup verification passed!")
            return True
        else:
            print("❌ Setup verification failed")
            return False
    except Exception as e:
        print(f"❌ Error verifying setup: {e}")
        return False

def launch_streamlit():
    """Launch the Streamlit application"""
    print_step(6, "Launching Streamlit App")
    
    print("Starting Streamlit server...")
    print("\nThe app will open in your browser at:")
    print("🌐 http://localhost:8501")
    print("\nPress Ctrl+C to stop the server\n")
    
    time.sleep(2)
    
    try:
        subprocess.run(['streamlit', 'run', 'streamlit_app.py'])
        return True
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped by user")
        return True
    except FileNotFoundError:
        print("\n❌ Streamlit not found!")
        print("Try installing: pip install streamlit")
        return False
    except Exception as e:
        print(f"\n❌ Error launching Streamlit: {e}")
        return False

def main():
    """Main execution flow"""
    print_header("Customer Segmentation System - Complete Setup")
    
    print("This script will:")
    print("  1. Check Python version")
    print("  2. Verify data file exists")
    print("  3. Install dependencies")
    print("  4. Train machine learning models")
    print("  5. Verify setup")
    print("  6. Launch Streamlit web app")
    
    input("\nPress Enter to continue...")
    
    # Step 1: Check Python version
    if not check_python_version():
        return 1
    
    # Step 2: Check data file
    if not check_data_file():
        return 1
    
    # Step 3: Install dependencies
    if not install_dependencies():
        print("\n⚠️  You can try installing manually:")
        print("   pip install -r requirements.txt")
        return 1
    
    # Step 4: Train models
    if not train_models():
        print("\n⚠️  You can try training manually:")
        print("   python run_all_systems.py")
        return 1
    
    # Step 5: Verify setup
    if not verify_setup():
        print("\n⚠️  Please check the errors above and try again")
        return 1
    
    # Step 6: Launch app
    print_header("Setup Complete! 🎉")
    print("Everything is ready!")
    
    response = input("\nLaunch Streamlit app now? (Y/n): ").strip().lower()
    
    if response in ['', 'y', 'yes']:
        if not launch_streamlit():
            return 1
    else:
        print("\n✅ Setup complete!")
        print("\nTo launch the app later, run:")
        print("   streamlit run streamlit_app.py")
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
