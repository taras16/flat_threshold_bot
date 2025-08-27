import pandas as pd
import numpy as np

def detect_zones(df, tolerance=0.005, min_tests=3):
    closes = df["close"].tolist()
    zones = []
    for i, price in enumerate(closes):
        tests = sum(1 for c in closes if abs(c - price) / price < tolerance)
        if tests >= min_tests:
            zones.append(round(price, 4))
    return sorted(list(set(zones)))
