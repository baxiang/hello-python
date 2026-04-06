"""聚类算法"""

import numpy as np


class KMeans:
    """K-Means 聚类"""
    
    def __init__(self, n_clusters: int = 3, max_iterations: int = 100):
        self.n_clusters = n_clusters
        self.max_iterations = max_iterations
        self.centroids = None
        self.labels = None
    
    def fit(self, X: np.ndarray) -> "KMeans":
        indices = np.random.choice(len(X), self.n_clusters, replace=False)
        self.centroids = X[indices]
        
        for _ in range(self.max_iterations):
            distances = np.sqrt(((X[:, np.newaxis] - self.centroids) ** 2).sum(axis=2))
            self.labels = np.argmin(distances, axis=1)
            
            new_centroids = np.array([
                X[self.labels == k].mean(axis=0) if np.sum(self.labels == k) > 0 else self.centroids[k]
                for k in range(self.n_clusters)
            ])
            
            if np.allclose(self.centroids, new_centroids):
                break
            self.centroids = new_centroids
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        distances = np.sqrt(((X[:, np.newaxis] - self.centroids) ** 2).sum(axis=2))
        return np.argmin(distances, axis=1)


class PCA:
    """主成分分析"""
    
    def __init__(self, n_components: int = 2):
        self.n_components = n_components
        self.components = None
        self.mean = None
    
    def fit(self, X: np.ndarray) -> "PCA":
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean
        cov_matrix = np.cov(X_centered.T)
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        indices = np.argsort(eigenvalues)[::-1]
        self.components = eigenvectors[:, indices[:self.n_components]]
        return self
    
    def transform(self, X: np.ndarray) -> np.ndarray:
        return np.dot(X - self.mean, self.components)
    
    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        return self.fit(X).transform(X)