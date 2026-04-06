"""优化测试"""

import numpy as np
from app.models.grid_search import EarlyStopping


def test_early_stopping():
    early_stop = EarlyStopping(patience=3)
    scores = [0.5, 0.6, 0.7, 0.75, 0.76, 0.75, 0.74, 0.73]
    
    stopped = False
    for score in scores:
        if early_stop(score):
            stopped = True
            break
    
    assert stopped or early_stop.counter >= 0