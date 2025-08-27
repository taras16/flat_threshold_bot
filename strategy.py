def breakout_signal(price, zones):
    for z in zones:
        if abs(price - z) / z < 0.002:  # якщо близько до рівня
            return z
    return None
