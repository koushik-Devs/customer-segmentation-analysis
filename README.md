# Customer Personality Segmentation System 🎯

A comprehensive machine learning system for customer segmentation and personality analysis, featuring advanced clustering algorithms, classification models, and an interactive web application for real-time customer predictions.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.2.0+-orange.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28.0+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🚀 Quick Start

### One-Command Setup & Launch
```bash
python setup_and_launch.py
```

This automatically handles everything: dependency installation, model training, and web app launch.

### Alternative: Windows Batch File
```cmd
launch_streamlit.bat
```

## 📋 Project Overview

This system combines unsupervised and supervised machine learning to create actionable customer segments with practical business applications:

- **🔍 Advanced Data Processing**: 17 engineered features from 28 raw attributes
- **🎯 K-Means Clustering**: Optimal segmentation with business interpretability  
- **🤖 Classification Models**: 99.07% accuracy with 6 different algorithms
- **🌐 Interactive Web App**: Real-time predictions with confidence scoring
- **📊 Comprehensive Visualizations**: PCA plots, cluster analysis, performance metrics
- **📈 Marketing Intelligence**: Segment-specific strategies and A/B testing framework
- **🔗 CRM Integration**: Export capabilities for business systems

## 🏆 Key Results

- **2,240 → 2,149** clean customer records (4.06% outlier removal)
- **99.07% classification accuracy** (Logistic Regression)
- **3 optimal customer segments** with clear business interpretation
- **<1 second prediction time** for real-time applications
- **18% campaign improvement** and **25% ROI increase** potential

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Windows OS (batch files included)
- Internet connection

### Dependencies
```bash
pip install -r requirements.txt
```

**Core Libraries:**
- `pandas`, `numpy` - Data manipulation
- `scikit-learn` - Machine learning algorithms
- `matplotlib`, `seaborn`, `plotly` - Visualizations
- `streamlit` - Web application framework
- `jupyter` - Interactive analysis

## 📊 System Architecture

```
Raw Data → Preprocessing → Clustering → Classification → Web App
    ↓           ↓            ↓           ↓            ↓
CSV File → Feature Eng. → K-Means → 6 ML Models → Streamlit
    ↓           ↓            ↓           ↓            ↓
2,240 → 17 Features → 3 Segments → 99.07% Acc → Real-time UI
```

## 🔧 Usage

### Complete Analysis Pipeline
```bash
python run_all_systems.py
```

### Individual Modules
```bash
python 1_data_preprocessing.py      # Data cleaning & feature engineering
python 2_unsupervised_clustering.py # K-Means clustering analysis
python 3_supervised_learning.py     # Classification model training
python 4_visualization.py           # Generate analysis charts
python 5_model_deployment.py        # Model deployment prep
python 6_marketing_strategies.py    # Marketing strategy generation
python 7_segment_monitoring.py      # Segment monitoring setup
python 8_ab_testing.py             # A/B testing framework
python 9_crm_integration.py         # CRM integration tools
```

### Web Application
```bash
streamlit run streamlit_app.py
```
Access at: `http://localhost:8501`

### Jupyter Analysis
```bash
jupyter notebook customer_segmentation_analysis.ipynb
```

## 📁 Project Structure

```
├── 📊 Analysis Modules
│   ├── 1_data_preprocessing.py      # Data cleaning & feature engineering
│   ├── 2_unsupervised_clustering.py # K-Means clustering
│   ├── 3_supervised_learning.py     # Classification models
│   ├── 4_visualization.py           # Chart generation
│   └── 5-9_*.py                    # Deployment & business modules
│
├── 🌐 Web Application
│   ├── streamlit_app.py             # Interactive web interface
│   ├── launch_streamlit.py          # Cross-platform launcher
│   └── launch_streamlit.bat         # Windows batch launcher
│
├── 🤖 Models & Data
│   ├── models/                      # Trained ML models
│   ├── *.csv                       # Processed datasets
│   └── *.png                       # Generated visualizations
│
├── 📚 Documentation
│   ├── README.md                    # This file
│   ├── PROJECT_EXECUTION_GUIDE.md   # Detailed setup guide
│   ├── Team_Contributions.md        # Team member contributions
│   └── *.pdf, *.pptx              # Reports & presentations
│
└── ⚙️ Setup & Testing
    ├── setup_and_launch.py         # Automated setup
    ├── requirements.txt             # Dependencies
    ├── test_modules.py              # Module testing
    └── run_all_systems.py           # Complete pipeline
```

## 🎯 Features

### Machine Learning Pipeline
- **Data Preprocessing**: Missing value imputation, outlier detection, feature scaling
- **Feature Engineering**: 17 derived features from customer behavior patterns
- **Clustering Analysis**: K-Means with optimal k=3 determination
- **Classification**: 6 algorithms with hyperparameter tuning
- **Model Validation**: 5-fold cross-validation with performance metrics

### Web Application
- **Interactive Forms**: 26 customer feature inputs with validation
- **Real-time Predictions**: Instant segment classification with confidence scores
- **Visual Analytics**: Probability distributions and segment characteristics
- **Customer Profiles**: Detailed analysis and recommendations

### Business Intelligence
- **Marketing Strategies**: Segment-specific campaign recommendations
- **A/B Testing**: Framework for campaign optimization
- **CRM Integration**: Export formats for business systems
- **Performance Monitoring**: Segment stability and customer migration tracking

## 📈 Model Performance

| Algorithm | Accuracy | Precision | Recall | F1-Score |
|-----------|----------|-----------|--------|----------|
| **Logistic Regression** | **99.07%** | **99.08%** | **99.07%** | **99.07%** |
| Random Forest | 98.84% | 98.85% | 98.84% | 98.84% |
| Gradient Boosting | 98.60% | 98.62% | 98.60% | 98.61% |
| Decision Tree | 97.91% | 97.93% | 97.91% | 97.92% |
| SVM | 97.67% | 97.70% | 97.67% | 97.68% |
| KNN | 96.51% | 96.58% | 96.51% | 96.54% |

## 👥 Team

**Developed by Computer Science & Engineering Students, ADAMAS University**

- **Koushik Mondal** (UG/02/BTCSE/2022/006) - Data Science Lead & Clustering Specialist
- **Kalyan Ghosh** (UG/02/BTCSE/2022/007) - Machine Learning Engineer & Performance Analyst  
- **Imran Nazim Mallik** (UG/03/BTCSE/2022/009) - Full-Stack Developer & Deployment Specialist
- **Bhabajyati Bhattacharjya** (UG/02/BTCSE/2022/011) - Research Lead & Business Analyst

**Supervisor:** Dr. Samik Datta, Assistant Professor

## 🔍 Troubleshooting

### Common Issues

**Missing Data File:**
```bash
# Ensure marketing_campaign_v.csv is in project root
ls marketing_campaign_v.csv
```

**Encoding Errors (Windows):**
```bash
# Set UTF-8 encoding
set PYTHONIOENCODING=utf-8
# Or use PowerShell instead of CMD
```

**Streamlit Won't Start:**
```bash
# Check installation
streamlit --version
# Try different port
streamlit run streamlit_app.py --server.port 8502
```

**Model Training Fails:**
```bash
# Test individual modules
python test_modules.py
# Check memory availability for clustering
```

## 📊 Generated Outputs

### Model Files
- `models/kmeans_model.pkl` - Trained clustering model
- `models/best_classifier.pkl` - Best classification model (99.07% accuracy)
- `models/scaler.pkl` - Feature scaling transformer
- `models/feature_names.pkl` - Feature definitions

### Analysis Results  
- `data_processed.csv` - Cleaned dataset with engineered features
- `data_clustered.csv` - Dataset with cluster assignments
- `cluster_profiles.csv` - Detailed segment characteristics
- Various PNG visualizations (PCA plots, confusion matrices, etc.)

### Business Intelligence
- Marketing strategy JSON files
- A/B testing experiment configurations
- CRM export files
- Customer persona definitions

## 🚀 Deployment

### Local Development
```bash
python setup_and_launch.py
```

### Production Deployment
- Docker containerization available
- Flask API for model serving
- Streamlit cloud deployment ready
- CRM integration endpoints

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ADAMAS University** - Department of Computer Science & Engineering
- **Dr. Samik Datta** - Project supervision and guidance
- **Scikit-learn Community** - Machine learning framework
- **Streamlit Team** - Web application framework

---

**🎯 Ready to segment your customers? Run `python setup_and_launch.py` and start analyzing!**
