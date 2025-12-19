"""
Customer Personality Segmentation - Unsupervised Learning (Clustering)
This module performs customer segmentation using multiple clustering algorithms
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from scipy.cluster.hierarchy import dendrogram, linkage
import warnings
warnings.filterwarnings('ignore')

class CustomerSegmentation:
    """Performs customer segmentation using various clustering algorithms"""
    
    def __init__(self, data_path='data_processed.csv'):
        self.df = pd.read_csv(data_path)
        self.X_scaled = None
        self.scaler = None
        self.pca = None
        self.X_pca = None
        self.best_n_clusters = None
        self.cluster_labels = None
        
    def prepare_features(self):
        """Prepare features for clustering"""
        print("\n" + "="*70)
        print("FEATURE PREPARATION FOR CLUSTERING")
        print("="*70)
        
        # Select numerical features for clustering
        clustering_features = [
            'Age', 'Income', 'Total_Spending', 'Total_Children',
            'Family_Size', 'Total_Purchases', 'Customer_Days',
            'Avg_Purchase_Value', 'Spending_Per_Day', 'Income_Per_Member',
            'Education_Level', 'Has_Partner', 'Total_Campaigns_Accepted',
            'Web_Activity_Score', 'Deal_Sensitivity', 'Product_Diversity',
            'Response_Rate', 'Recency', 'NumWebVisitsMonth',
            'MntWines', 'MntFruits', 'MntMeatProducts',
            'MntFishProducts', 'MntSweetProducts', 'MntGoldProds'
        ]
        
        # Filter available features
        available_features = [f for f in clustering_features if f in self.df.columns]
        print(f"Using {len(available_features)} features for clustering")
        
        X = self.df[available_features].copy()
        
        # Handle any remaining missing values
        X = X.fillna(X.median())
        
        # Standardize features
        self.scaler = StandardScaler()
        self.X_scaled = self.scaler.fit_transform(X)
        
        print(f"✓ Features scaled: {self.X_scaled.shape}")
        
        return self.X_scaled
    
    def perform_pca(self, n_components=0.95):
        """Perform PCA for dimensionality reduction"""
        print("\n" + "="*70)
        print("PRINCIPAL COMPONENT ANALYSIS (PCA)")
        print("="*70)
        
        self.pca = PCA(n_components=n_components)
        self.X_pca = self.pca.fit_transform(self.X_scaled)
        
        print(f"Original dimensions: {self.X_scaled.shape[1]}")
        print(f"Reduced dimensions: {self.X_pca.shape[1]}")
        print(f"Explained variance: {self.pca.explained_variance_ratio_.sum():.4f}")
        
        # Plot explained variance
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, len(self.pca.explained_variance_ratio_) + 1),
                np.cumsum(self.pca.explained_variance_ratio_), 'bo-')
        plt.xlabel('Number of Components')
        plt.ylabel('Cumulative Explained Variance')
        plt.title('PCA - Explained Variance')
        plt.grid(True)
        plt.savefig('pca_variance.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ PCA variance plot saved")
        
        return self.X_pca
    
    def find_optimal_clusters(self, max_clusters=10):
        """Find optimal number of clusters using multiple methods"""
        print("\n" + "="*70)
        print("FINDING OPTIMAL NUMBER OF CLUSTERS")
        print("="*70)
        
        inertias = []
        silhouette_scores = []
        davies_bouldin_scores = []
        calinski_harabasz_scores = []
        
        K_range = range(2, max_clusters + 1)
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(self.X_scaled)
            
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(self.X_scaled, labels))
            davies_bouldin_scores.append(davies_bouldin_score(self.X_scaled, labels))
            calinski_harabasz_scores.append(calinski_harabasz_score(self.X_scaled, labels))
        
        # Plot metrics
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Elbow Method
        axes[0, 0].plot(K_range, inertias, 'bo-')
        axes[0, 0].set_xlabel('Number of Clusters')
        axes[0, 0].set_ylabel('Inertia')
        axes[0, 0].set_title('Elbow Method')
        axes[0, 0].grid(True)
        
        # Silhouette Score
        axes[0, 1].plot(K_range, silhouette_scores, 'go-')
        axes[0, 1].set_xlabel('Number of Clusters')
        axes[0, 1].set_ylabel('Silhouette Score')
        axes[0, 1].set_title('Silhouette Analysis')
        axes[0, 1].grid(True)
        
        # Davies-Bouldin Index
        axes[1, 0].plot(K_range, davies_bouldin_scores, 'ro-')
        axes[1, 0].set_xlabel('Number of Clusters')
        axes[1, 0].set_ylabel('Davies-Bouldin Index')
        axes[1, 0].set_title('Davies-Bouldin Index (Lower is Better)')
        axes[1, 0].grid(True)
        
        # Calinski-Harabasz Score
        axes[1, 1].plot(K_range, calinski_harabasz_scores, 'mo-')
        axes[1, 1].set_xlabel('Number of Clusters')
        axes[1, 1].set_ylabel('Calinski-Harabasz Score')
        axes[1, 1].set_title('Calinski-Harabasz Score (Higher is Better)')
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.savefig('optimal_clusters.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Optimal clusters plot saved")
        
        # Determine best k based on silhouette score
        best_k = 3  # Fixed to 3 clusters
        self.best_n_clusters = best_k
        
        print(f"\n✓ Optimal number of clusters: {best_k} (fixed)")
        print(f"  - Silhouette Score for k={best_k}: {silhouette_scores[list(K_range).index(best_k)]:.4f}")
        
        return best_k
    
    def perform_kmeans(self, n_clusters=None):
        """Perform K-Means clustering"""
        print("\n" + "="*70)
        print("K-MEANS CLUSTERING")
        print("="*70)
        
        if n_clusters is None:
            n_clusters = self.best_n_clusters
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.cluster_labels = kmeans.fit_predict(self.X_scaled)
        self.kmeans_model = kmeans  # Store the model
        
        # Add cluster labels to dataframe
        self.df['Cluster_KMeans'] = self.cluster_labels
        
        # Calculate metrics
        silhouette = silhouette_score(self.X_scaled, self.cluster_labels)
        davies_bouldin = davies_bouldin_score(self.X_scaled, self.cluster_labels)
        calinski_harabasz = calinski_harabasz_score(self.X_scaled, self.cluster_labels)
        
        print(f"Number of clusters: {n_clusters}")
        print(f"Silhouette Score: {silhouette:.4f}")
        print(f"Davies-Bouldin Index: {davies_bouldin:.4f}")
        print(f"Calinski-Harabasz Score: {calinski_harabasz:.4f}")
        
        # Save the model
        import os
        os.makedirs('models', exist_ok=True)
        joblib.dump(kmeans, 'models/kmeans_model.pkl')
        print("✓ KMeans model saved to 'models/kmeans_model.pkl'")
        
        return self.cluster_labels
    
    def perform_hierarchical(self, n_clusters=None):
        """Perform Hierarchical clustering"""
        print("\n" + "="*70)
        print("HIERARCHICAL CLUSTERING")
        print("="*70)
        
        if n_clusters is None:
            n_clusters = self.best_n_clusters
        
        # Perform clustering
        hierarchical = AgglomerativeClustering(n_clusters=n_clusters)
        labels = hierarchical.fit_predict(self.X_scaled)
        
        self.df['Cluster_Hierarchical'] = labels
        
        # Create dendrogram
        plt.figure(figsize=(15, 7))
        linkage_matrix = linkage(self.X_scaled[:500], method='ward')  # Use subset for visualization
        dendrogram(linkage_matrix)
        plt.title('Hierarchical Clustering Dendrogram')
        plt.xlabel('Sample Index')
        plt.ylabel('Distance')
        plt.savefig('dendrogram.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Dendrogram saved")
        
        silhouette = silhouette_score(self.X_scaled, labels)
        print(f"Silhouette Score: {silhouette:.4f}")
        
        return labels
    
    def perform_gmm(self, n_components=None):
        """Perform Gaussian Mixture Model clustering"""
        print("\n" + "="*70)
        print("GAUSSIAN MIXTURE MODEL (GMM)")
        print("="*70)
        
        if n_components is None:
            n_components = self.best_n_clusters
        
        gmm = GaussianMixture(n_components=n_components, random_state=42)
        labels = gmm.fit_predict(self.X_scaled)
        
        self.df['Cluster_GMM'] = labels
        
        silhouette = silhouette_score(self.X_scaled, labels)
        print(f"Silhouette Score: {silhouette:.4f}")
        print(f"BIC: {gmm.bic(self.X_scaled):.2f}")
        print(f"AIC: {gmm.aic(self.X_scaled):.2f}")
        
        return labels
    
    def visualize_clusters_2d(self):
        """Visualize clusters in 2D using PCA"""
        print("\n" + "="*70)
        print("CLUSTER VISUALIZATION")
        print("="*70)
        
        # Use first 2 PCA components for visualization
        pca_2d = PCA(n_components=2)
        X_2d = pca_2d.fit_transform(self.X_scaled)
        
        fig, axes = plt.subplots(1, 3, figsize=(20, 5))
        
        # K-Means
        scatter1 = axes[0].scatter(X_2d[:, 0], X_2d[:, 1], 
                                   c=self.df['Cluster_KMeans'], 
                                   cmap='viridis', alpha=0.6)
        axes[0].set_title('K-Means Clustering', fontsize=14, fontweight='bold')
        axes[0].set_xlabel(f'PC1 ({pca_2d.explained_variance_ratio_[0]:.2%})')
        axes[0].set_ylabel(f'PC2 ({pca_2d.explained_variance_ratio_[1]:.2%})')
        plt.colorbar(scatter1, ax=axes[0])
        
        # Hierarchical
        scatter2 = axes[1].scatter(X_2d[:, 0], X_2d[:, 1], 
                                   c=self.df['Cluster_Hierarchical'], 
                                   cmap='plasma', alpha=0.6)
        axes[1].set_title('Hierarchical Clustering', fontsize=14, fontweight='bold')
        axes[1].set_xlabel(f'PC1 ({pca_2d.explained_variance_ratio_[0]:.2%})')
        axes[1].set_ylabel(f'PC2 ({pca_2d.explained_variance_ratio_[1]:.2%})')
        plt.colorbar(scatter2, ax=axes[1])
        
        # GMM
        scatter3 = axes[2].scatter(X_2d[:, 0], X_2d[:, 1], 
                                   c=self.df['Cluster_GMM'], 
                                   cmap='coolwarm', alpha=0.6)
        axes[2].set_title('Gaussian Mixture Model', fontsize=14, fontweight='bold')
        axes[2].set_xlabel(f'PC1 ({pca_2d.explained_variance_ratio_[0]:.2%})')
        axes[2].set_ylabel(f'PC2 ({pca_2d.explained_variance_ratio_[1]:.2%})')
        plt.colorbar(scatter3, ax=axes[2])
        
        plt.tight_layout()
        plt.savefig('clusters_visualization.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Cluster visualization saved")
    
    def analyze_clusters(self):
        """Analyze and profile each cluster"""
        print("\n" + "="*70)
        print("CLUSTER PROFILING")
        print("="*70)
        
        # Use K-Means clusters for profiling
        cluster_col = 'Cluster_KMeans'
        
        # Key features for profiling
        profile_features = [
            'Age', 'Income', 'Total_Spending', 'Total_Children',
            'Education_Level', 'Total_Purchases', 'Response_Rate',
            'Product_Diversity', 'Deal_Sensitivity'
        ]
        
        available_features = [f for f in profile_features if f in self.df.columns]
        
        cluster_profiles = self.df.groupby(cluster_col)[available_features].mean()
        
        print("\nCluster Profiles (Mean Values):")
        print(cluster_profiles.round(2))
        
        # Save cluster profiles
        cluster_profiles.to_csv('cluster_profiles.csv')
        print("\n✓ Cluster profiles saved to 'cluster_profiles.csv'")
        
        # Cluster sizes
        print("\nCluster Sizes:")
        print(self.df[cluster_col].value_counts().sort_index())
        
        return cluster_profiles
    
    def save_results(self):
        """Save clustered data"""
        self.df.to_csv('data_clustered.csv', index=False)
        print("\n✓ Clustered data saved to 'data_clustered.csv'")
    
    def run_clustering(self):
        """Run complete clustering pipeline"""
        print("\n" + "="*70)
        print(" "*15 + "UNSUPERVISED LEARNING - CLUSTERING")
        print("="*70)
        
        self.prepare_features()
        self.perform_pca()
        self.find_optimal_clusters()
        self.perform_kmeans()
        self.perform_hierarchical()
        self.perform_gmm()
        self.visualize_clusters_2d()
        self.analyze_clusters()
        self.save_results()
        
        print("\n" + "="*70)
        print(" "*20 + "CLUSTERING COMPLETE!")
        print("="*70)
        
        return self.df


if __name__ == "__main__":
    segmentation = CustomerSegmentation()
    df_clustered = segmentation.run_clustering()
    print(f"\n✓ Customers segmented into {segmentation.best_n_clusters} clusters")
