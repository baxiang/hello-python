# 无监督学习示例

"""
无监督学习示例
包含：K-Means、层次聚类、PCA
"""

import numpy as np
from typing import Optional


# 1. K-Means 聚类
class KMeans:
    """K-Means 聚类"""
    
    def __init__(self, n_clusters: int = 3, max_iterations: int = 100):
        self.n_clusters = n_clusters
        self.max_iterations = max_iterations
        self.centroids = None
        self.labels = None
    
    def fit(self, X: np.ndarray) -> "KMeans":
        # 随机初始化质心
        indices = np.random.choice(len(X), self.n_clusters, replace=False)
        self.centroids = X[indices]
        
        for _ in range(self.max_iterations):
            # 分配样本到最近的质心
            distances = np.sqrt(((X[:, np.newaxis] - self.centroids) ** 2).sum(axis=2))
            self.labels = np.argmin(distances, axis=1)
            
            # 更新质心
            new_centroids = np.array([
                X[self.labels == k].mean(axis=0) if np.sum(self.labels == k) > 0 else self.centroids[k]
                for k in range(self.n_clusters)
            ])
            
            # 检查收敛
            if np.allclose(self.centroids, new_centroids):
                break
            self.centroids = new_centroids
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        distances = np.sqrt(((X[:, np.newaxis] - self.centroids) ** 2).sum(axis=2))
        return np.argmin(distances, axis=1)


# 2. 层次聚类
class HierarchicalClustering:
    """层次聚类（凝聚式）"""
    
    def __init__(self, n_clusters: int = 2):
        self.n_clusters = n_clusters
        self.labels = None
    
    def _euclidean_distance(self, a: np.ndarray, b: np.ndarray) -> float:
        return np.sqrt(np.sum((a - b) ** 2))
    
    def fit(self, X: np.ndarray) -> "HierarchicalClustering":
        n_samples = len(X)
        clusters = [[i] for i in range(n_samples)]
        
        while len(clusters) > self.n_clusters:
            # 找到最近的两个簇
            min_distance = float('inf')
            merge_i, merge_j = 0, 1
            
            for i in range(len(clusters)):
                for j in range(i + 1, len(clusters)):
                    # 计算簇间距离（单链接）
                    distance = min(
                        self._euclidean_distance(X[a], X[b])
                        for a in clusters[i]
                        for b in clusters[j]
                    )
                    if distance < min_distance:
                        min_distance = distance
                        merge_i, merge_j = i, j
            
            # 合并簇
            clusters[merge_i].extend(clusters[merge_j])
            clusters.pop(merge_j)
        
        # 分配标签
        self.labels = np.zeros(n_samples, dtype=int)
        for label, cluster in enumerate(clusters):
            for idx in cluster:
                self.labels[idx] = label
        
        return self


# 3. PCA 降维
class PCA:
    """主成分分析"""
    
    def __init__(self, n_components: int = 2):
        self.n_components = n_components
        self.components = None
        self.mean = None
        self.explained_variance_ratio = None
    
    def fit(self, X: np.ndarray) -> "PCA":
        # 标准化
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean
        
        # 计算协方差矩阵
        cov_matrix = np.cov(X_centered.T)
        
        # 特征值分解
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        
        # 排序
        indices = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[indices]
        eigenvectors = eigenvectors[:, indices]
        
        # 选择主成分
        self.components = eigenvectors[:, :self.n_components]
        
        # 解释方差比例
        total_variance = np.sum(eigenvalues)
        self.explained_variance_ratio = eigenvalues[:self.n_components] / total_variance
        
        return self
    
    def transform(self, X: np.ndarray) -> np.ndarray:
        X_centered = X - self.mean
        return np.dot(X_centered, self.components)
    
    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        return self.fit(X).transform(X)


# 4. DBSCAN
class DBSCAN:
    """DBSCAN 密度聚类"""
    
    def __init__(self, eps: float = 0.5, min_samples: int = 5):
        self.eps = eps
        self.min_samples = min_samples
        self.labels = None
    
    def fit(self, X: np.ndarray) -> "DBSCAN":
        n_samples = len(X)
        self.labels = np.full(n_samples, -1)  # -1 表示噪声
        
        cluster_id = 0
        
        for i in range(n_samples):
            if self.labels[i] != -1:
                continue
            
            # 找到邻居
            neighbors = self._get_neighbors(X, i)
            
            if len(neighbors) < self.min_samples:
                continue  # 噪声点
            
            # 开始新簇
            self.labels[i] = cluster_id
            seed_set = list(neighbors)
            
            for j in seed_set:
                if self.labels[j] == -1:
                    self.labels[j] = cluster_id
                    new_neighbors = self._get_neighbors(X, j)
                    if len(new_neighbors) >= self.min_samples:
                        seed_set.extend(new_neighbors)
                elif self.labels[j] == -1:
                    self.labels[j] = cluster_id
            
            cluster_id += 1
        
        return self
    
    def _get_neighbors(self, X: np.ndarray, i: int) -> list:
        distances = np.sqrt(np.sum((X - X[i]) ** 2, axis=1))
        return np.where(distances <= self.eps)[0].tolist()


if __name__ == "__main__":
    print("=" * 40)
    print("无监督学习示例")
    print("=" * 40)
    
    # 生成示例数据
    np.random.seed(42)
    X = np.vstack([
        np.random.randn(20, 2) + [0, 0],
        np.random.randn(20, 2) + [5, 5],
        np.random.randn(20, 2) + [0, 5]
    ])
    
    # K-Means
    print("\n【K-Means 聚类】")
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(X)
    print(f"质心:\n{kmeans.centroids}")
    print(f"标签分布: {np.bincount(kmeans.labels)}")
    
    # 层次聚类
    print("\n【层次聚类】")
    hc = HierarchicalClustering(n_clusters=3)
    hc.fit(X[:30])  # 使用较少样本
    print(f"标签: {hc.labels}")
    
    # PCA
    print("\n【PCA 降维】")
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    print(f"解释方差比例: {pca.explained_variance_ratio}")
    print(f"降维后形状: {X_pca.shape}")
    
    # DBSCAN
    print("\n【DBSCAN】")
    dbscan = DBSCAN(eps=1.0, min_samples=3)
    dbscan.fit(X)
    print(f"标签: {np.unique(dbscan.labels)}")
    print(f"噪声点: {np.sum(dbscan.labels == -1)}")