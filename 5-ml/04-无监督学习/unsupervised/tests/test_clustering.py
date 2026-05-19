"""聚类测试"""

import numpy as np
from app.models.clustering import KMeans, PCA


def test_kmeans():
    X = np.array([[1, 1], [1, 2], [5, 5], [5, 6]])
    model = KMeans(n_clusters=2)
    model.fit(X)
    assert len(model.labels) == 4
    assert len(np.unique(model.labels)) == 2


def test_pca():
    X = np.random.randn(10, 5)
    model = PCA(n_components=2)
    X_transformed = model.fit_transform(X)
    assert X_transformed.shape == (10, 2)