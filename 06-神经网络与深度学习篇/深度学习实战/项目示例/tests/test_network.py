"""神经网络测试"""

import numpy as np
from app.models.layers import Dense, Activation, NeuralNetwork


def test_dense_layer():
    layer = Dense(2, 3)
    x = np.array([[1, 2]])
    output = layer.forward(x)
    assert output.shape == (1, 3)


def test_neural_network():
    layers = [
        Dense(2, 4),
        Activation("relu"),
        Dense(4, 1),
        Activation("sigmoid")
    ]
    model = NeuralNetwork(layers)
    
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])
    
    model.fit(X, y, epochs=10, learning_rate=0.1)
    assert len(model.history["loss"]) == 10