# 深度学习示例

"""
深度学习示例
演示神经网络训练和预测
"""

import numpy as np
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Dense, Activation, NeuralNetwork, create_mlp
from utils import generate_xor_data, generate_circle_data, one_hot_encode, train_test_split


def example_xor():
    """XOR 分类示例"""
    print("=" * 40)
    print("XOR 分类示例")
    print("=" * 40)
    
    # 生成数据
    X, y = generate_xor_data(200)
    
    # 创建模型
    model = create_mlp(
        input_size=2,
        hidden_sizes=[8, 8],
        output_size=1,
        activation="relu"
    )
    
    # 训练
    model.fit(X, y.reshape(-1, 1), epochs=100, batch_size=32, learning_rate=0.1, verbose=0)
    
    # 预测
    y_pred = model.predict(X[:5])
    print(f"\n预测结果:")
    for i in range(5):
        print(f"  输入: {X[i]}, 真实: {y[i]}, 预测: {y_pred[i][0]:.4f}")
    
    print(f"\n最终准确率: {model.history['accuracy'][-1]:.4f}")


def example_circle():
    """圆形分类示例"""
    print("\n" + "=" * 40)
    print("圆形分类示例")
    print("=" * 40)
    
    # 生成数据
    X, y = generate_circle_data(300)
    
    # 创建模型
    model = create_mlp(
        input_size=2,
        hidden_sizes=[16, 16],
        output_size=1,
        activation="relu"
    )
    
    # 训练
    model.fit(X, y.reshape(-1, 1), epochs=150, batch_size=32, learning_rate=0.05, verbose=0)
    
    print(f"\n最终损失: {model.history['loss'][-1]:.4f}")
    print(f"最终准确率: {model.history['accuracy'][-1]:.4f}")


def example_multiclass():
    """多分类示例"""
    print("\n" + "=" * 40)
    print("多分类示例")
    print("=" * 40)
    
    # 生成模拟数据
    np.random.seed(42)
    n_samples = 300
    n_features = 4
    n_classes = 3
    
    X = np.random.randn(n_samples, n_features)
    y = np.random.randint(0, n_classes, n_samples)
    y_onehot = one_hot_encode(y, n_classes)
    
    # 划分数据
    X_train, X_test, y_train, y_test = train_test_split(X, y_onehot, test_size=0.2)
    
    # 创建模型
    model = create_mlp(
        input_size=n_features,
        hidden_sizes=[16, 8],
        output_size=n_classes,
        activation="relu"
    )
    
    # 训练
    model.fit(X_train, y_train, epochs=100, batch_size=32, learning_rate=0.01, verbose=0)
    
    # 预测
    y_pred = model.predict_classes(X_test)
    y_true = np.argmax(y_test, axis=1)
    accuracy = np.mean(y_pred == y_true)
    
    print(f"\n测试集准确率: {accuracy:.4f}")


def example_custom_network():
    """自定义网络示例"""
    print("\n" + "=" * 40)
    print("自定义网络示例")
    print("=" * 40)
    
    # 创建自定义网络
    layers = [
        Dense(2, 16),
        Activation("relu"),
        Dense(16, 8),
        Activation("tanh"),
        Dense(8, 1),
        Activation("sigmoid")
    ]
    
    model = NeuralNetwork(layers)
    
    # 生成数据
    X, y = generate_xor_data(100)
    
    # 训练
    model.fit(X, y.reshape(-1, 1), epochs=50, learning_rate=0.5, verbose=0)
    
    print(f"\n最终准确率: {model.history['accuracy'][-1]:.4f}")


if __name__ == "__main__":
    example_xor()
    example_circle()
    example_multiclass()
    example_custom_network()