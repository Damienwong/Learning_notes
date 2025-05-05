import random


class LiDAR:
    def __init__(self, noise_level=5):
        self.noise_level = noise_level

    def measure_distance(self, true_distance):
        noise = random.uniform(-self.noise_level, self.noise_level)
        return true_distance + noise
