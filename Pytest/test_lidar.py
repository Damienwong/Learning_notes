import pytest
from lidar_sensor import LiDAR
import logging


MAX_ERROR = 20

@pytest.fixture
def lidar():
    return LiDAR(noise_level=10)

@pytest.mark.parametrize('true_distance', [1000, 1500, 2000, 2500, 3000])
def test_lidar_precision(lidar, true_distance):
    measured_distance = lidar.measure_distance(true_distance)
    error = abs(measured_distance - true_distance)

    print(f"真实距离: {true_distance}mm, 测试值: {measured_distance:.2f}mm, 误差: {error:.2f}mm")
    assert error <= MAX_ERROR, f'误差超出范围! 误差：{error:.2f}mm'


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.mark.parametrize('true_distance', [1000, 2000, 3000, 4000, 5000])
def test_lidar_precision_with_logging(lidar, true_distance):
    measured_distance = lidar.measure_distance(true_distance)
    error = abs(measured_distance - true_distance)

    logging.info(f'True Distance: {true_distance}mm, Measured Distance: {measured_distance:.2f}mm, error: {error:.2f}mm')
    assert error <= MAX_ERROR, f'error reach limit! Error: {error:.2f}mm'