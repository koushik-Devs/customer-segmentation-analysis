"""
Cross-platform launcher for Streamlit app
"""

import os
import sys
import subprocess

def check_and_train():
    """Check if models exist, train if needed"""
    if not os.path.exists('models'):
        print("="*60)
        print("Models not found. Training models first...")
        print("="*60)
        print()
        
        result = subprocess.run([sys.executable, 'run_all_systems.py'])
        if result.returncode != 0:
            print("\n❌ Model training failed!")
            return False
    
    return True

def verify_setup():
    """Verify setup is complete"""
    print("Verifying setup...")
    result = subprocess.run([sys.executable, 'test_streamlit_setup.py'])
    return result.returncode == 0

def launch_streamlit():
    """Launch the Streamlit app"""
    print("\n" + "="*60)
    print("Launching Streamlit App...")
    print("="*60)
    print("\nThe app will open in your browser at:")
    print("http://localhost:8501")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        subprocess.run(['streamlit', 'run', 'streamlit_app.py'])
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    except FileNotFoundError:
        print("\n❌ Streamlit not found!")
        print("Install with: pip install streamlit")
        return False
    
    return True

def main():
    print("="*60)
    print("Customer Segmentation Streamlit App Launcher")
    print("="*60)
    print()
    
    # Check and train models if needed
    if not check_and_train():
        return 1
    
    # Verify setup
    if not verify_setup():
        print("\n❌ Setup verification failed!")
        print("Please fix the issues above and try again.")
        return 1
    
    # Launch app
    if not launch_streamlit():
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
