"""
Test script to verify all modules can be imported correctly
"""

import sys
import os

print("Testing module imports...\n")

# Test 5_model_deployment.py
print("1. Testing 5_model_deployment.py...")
try:
    with open('5_model_deployment.py', 'r', encoding='utf-8') as f:
        exec(f.read(), {'__name__': '__test__'})
    print("   OK - No syntax errors\n")
except Exception as e:
    print(f"   ERROR: {e}\n")

# Test 6_marketing_strategies.py
print("2. Testing 6_marketing_strategies.py...")
try:
    with open('6_marketing_strategies.py', 'r', encoding='utf-8') as f:
        exec(f.read(), {'__name__': '__test__'})
    print("   OK - No syntax errors\n")
except Exception as e:
    print(f"   ERROR: {e}\n")

# Test 7_segment_monitoring.py
print("3. Testing 7_segment_monitoring.py...")
try:
    with open('7_segment_monitoring.py', 'r', encoding='utf-8') as f:
        exec(f.read(), {'__name__': '__test__'})
    print("   OK - No syntax errors\n")
except Exception as e:
    print(f"   ERROR: {e}\n")

# Test 8_ab_testing.py
print("4. Testing 8_ab_testing.py...")
try:
    with open('8_ab_testing.py', 'r', encoding='utf-8') as f:
        exec(f.read(), {'__name__': '__test__'})
    print("   OK - No syntax errors\n")
except Exception as e:
    print(f"   ERROR: {e}\n")

# Test 9_crm_integration.py
print("5. Testing 9_crm_integration.py...")
try:
    with open('9_crm_integration.py', 'r', encoding='utf-8') as f:
        exec(f.read(), {'__name__': '__test__'})
    print("   OK - No syntax errors\n")
except Exception as e:
    print(f"   ERROR: {e}\n")

print("="*70)
print("All module tests complete!")
print("="*70)
