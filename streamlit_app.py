import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Customer Segmentation Predictor",
    page_icon="👥",
    layout="wide"
)

# Title and description
st.title("🎯 Customer Segmentation Predictor")
st.markdown("Enter customer details to predict which segment they belong to")

# Check if models exist
if not os.path.exists('models'):
    st.error("⚠️ Models not found! Please run the training pipeline first.")
    st.info("Run: `python run_all_systems.py` to train the models")
    st.stop()

# Load models and scalers
@st.cache_resource
def load_models():
    try:
        scaler = joblib.load('models/scaler.pkl')
        kmeans = joblib.load('models/kmeans_model.pkl')
        classifier = joblib.load('models/best_classifier.pkl')
        feature_names = joblib.load('models/feature_names.pkl')
        return scaler, kmeans, classifier, feature_names
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None, None, None

scaler, kmeans, classifier, feature_names = load_models()

if scaler is None:
    st.stop()

# Sidebar for input
st.sidebar.header("📝 Customer Information")

# Create two columns for better layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Demographics")
    year_birth = st.number_input("Year of Birth", min_value=1940, max_value=2006, value=1980)
    education = st.selectbox("Education Level", ["Basic", "2n Cycle", "Graduation", "Master", "PhD"])
    marital_status = st.selectbox("Marital Status", ["Single", "Married", "Together", "Divorced", "Widow", "Alone", "Absurd", "YOLO"])
    income = st.number_input("Annual Income ($)", min_value=0, max_value=200000, value=50000, step=1000)
    
    st.subheader("Family")
    kidhome = st.number_input("Number of Kids at Home", min_value=0, max_value=5, value=0)
    teenhome = st.number_input("Number of Teenagers at Home", min_value=0, max_value=5, value=0)

with col2:
    st.subheader("Purchase Behavior")
    recency = st.number_input("Days Since Last Purchase", min_value=0, max_value=365, value=30)
    num_web_purchases = st.number_input("Web Purchases", min_value=0, max_value=50, value=5)
    num_catalog_purchases = st.number_input("Catalog Purchases", min_value=0, max_value=50, value=2)
    num_store_purchases = st.number_input("Store Purchases", min_value=0, max_value=50, value=5)
    num_web_visits = st.number_input("Website Visits per Month", min_value=0, max_value=30, value=5)
    num_deals_purchases = st.number_input("Deals Purchases", min_value=0, max_value=50, value=2)

st.subheader("💰 Product Spending (Last 2 Years)")
col3, col4, col5 = st.columns(3)

with col3:
    mnt_wines = st.number_input("Wines ($)", min_value=0, max_value=2000, value=300)
    mnt_fruits = st.number_input("Fruits ($)", min_value=0, max_value=200, value=20)

with col4:
    mnt_meat = st.number_input("Meat Products ($)", min_value=0, max_value=2000, value=150)
    mnt_fish = st.number_input("Fish Products ($)", min_value=0, max_value=300, value=40)

with col5:
    mnt_sweets = st.number_input("Sweet Products ($)", min_value=0, max_value=300, value=25)
    mnt_gold = st.number_input("Gold Products ($)", min_value=0, max_value=500, value=50)

st.subheader("📢 Campaign Response")
col6, col7 = st.columns(2)

with col6:
    accepted_cmp1 = st.checkbox("Accepted Campaign 1")
    accepted_cmp2 = st.checkbox("Accepted Campaign 2")
    accepted_cmp3 = st.checkbox("Accepted Campaign 3")

with col7:
    accepted_cmp4 = st.checkbox("Accepted Campaign 4")
    accepted_cmp5 = st.checkbox("Accepted Campaign 5")

# Customer tenure
customer_date = st.date_input("Customer Since", value=datetime(2013, 1, 1))

# Predict button
if st.button("🔮 Predict Customer Segment", type="primary"):
    # Calculate derived features
    current_year = 2024
    age = current_year - year_birth
    total_spending = mnt_wines + mnt_fruits + mnt_meat + mnt_fish + mnt_sweets + mnt_gold
    total_children = kidhome + teenhome
    family_size = total_children + 1
    if marital_status in ['Married', 'Together']:
        family_size += 1
    
    is_parent = 1 if total_children > 0 else 0
    total_purchases = num_web_purchases + num_catalog_purchases + num_store_purchases
    total_campaigns_accepted = sum([accepted_cmp1, accepted_cmp2, accepted_cmp3, accepted_cmp4, accepted_cmp5])
    
    # Calculate customer days
    reference_date = datetime(2014, 7, 1)
    customer_days = (reference_date - datetime.combine(customer_date, datetime.min.time())).days
    
    avg_purchase_value = total_spending / (total_purchases + 1)
    spending_per_day = total_spending / (customer_days + 1)
    income_per_member = income / family_size
    
    education_map = {'Basic': 1, '2n Cycle': 2, 'Graduation': 3, 'Master': 4, 'PhD': 5}
    education_level = education_map.get(education, 3)
    
    has_partner = 1 if marital_status in ['Married', 'Together'] else 0
    web_activity_score = (num_web_purchases * 2 + num_web_visits) / 3
    deal_sensitivity = num_deals_purchases / (total_purchases + 1)
    product_diversity = sum([mnt_wines > 0, mnt_fruits > 0, mnt_meat > 0, 
                            mnt_fish > 0, mnt_sweets > 0, mnt_gold > 0])
    response_rate = total_campaigns_accepted / 5
    
    # Create feature dictionary
    features = {
        'Age': age,
        'Income': income,
        'Total_Spending': total_spending,
        'Total_Children': total_children,
        'Family_Size': family_size,
        'Total_Purchases': total_purchases,
        'Customer_Days': customer_days,
        'Avg_Purchase_Value': avg_purchase_value,
        'Spending_Per_Day': spending_per_day,
        'Income_Per_Member': income_per_member,
        'Education_Level': education_level,
        'Has_Partner': has_partner,
        'Total_Campaigns_Accepted': total_campaigns_accepted,
        'Web_Activity_Score': web_activity_score,
        'Deal_Sensitivity': deal_sensitivity,
        'Product_Diversity': product_diversity,
        'Response_Rate': response_rate,
        'Recency': recency,
        'NumWebVisitsMonth': num_web_visits,
        'MntWines': mnt_wines,
        'MntFruits': mnt_fruits,
        'MntMeatProducts': mnt_meat,
        'MntFishProducts': mnt_fish,
        'MntSweetProducts': mnt_sweets,
        'MntGoldProds': mnt_gold
    }
    
    # Create DataFrame with correct feature order
    input_df = pd.DataFrame([features])
    input_df = input_df[feature_names]
    
    # Scale features
    input_scaled = scaler.transform(input_df)
    
    # Predict cluster
    cluster = classifier.predict(input_scaled)[0]
    cluster_proba = classifier.predict_proba(input_scaled)[0]
    
    # Display results
    st.success("✅ Prediction Complete!")
    
    # Create result columns
    res_col1, res_col2, res_col3 = st.columns([2, 2, 3])
    
    with res_col1:
        st.metric("Predicted Cluster", f"Cluster {cluster}")
        st.metric("Confidence", f"{cluster_proba[cluster]*100:.1f}%")
    
    with res_col2:
        st.metric("Total Spending", f"${total_spending:,.0f}")
        st.metric("Total Purchases", total_purchases)
    
    with res_col3:
        st.subheader("Cluster Probabilities")
        for i, prob in enumerate(cluster_proba):
            st.progress(prob, text=f"Cluster {i}: {prob*100:.1f}%")
    
    # Cluster descriptions
    st.subheader("📊 Cluster Characteristics")
    
    cluster_descriptions = {
        0: {
            "name": "Budget Conscious",
            "description": "Customers with lower spending, price-sensitive, prefer deals and discounts",
            "characteristics": ["Lower income", "Higher deal sensitivity", "Moderate web activity"]
        },
        1: {
            "name": "Premium Customers",
            "description": "High-value customers with significant spending across categories",
            "characteristics": ["Higher income", "High spending", "Low deal sensitivity", "Diverse product purchases"]
        },
        2: {
            "name": "Standard Customers",
            "description": "Average customers with moderate spending and engagement",
            "characteristics": ["Moderate income", "Balanced spending", "Average response rate"]
        }
    }
    
    if cluster in cluster_descriptions:
        desc = cluster_descriptions[cluster]
        st.info(f"**{desc['name']}**: {desc['description']}")
        st.write("**Key Characteristics:**")
        for char in desc['characteristics']:
            st.write(f"• {char}")
    
    # Show customer profile
    with st.expander("📋 View Complete Customer Profile"):
        profile_df = pd.DataFrame({
            'Feature': list(features.keys()),
            'Value': list(features.values())
        })
        st.dataframe(profile_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("💡 **Tip**: Adjust the customer details above to see how different characteristics affect segment prediction")
