import pytest
import numpy as np
import matplotlib

matplotlib.use('agg')


@pytest.fixture
def sample_data():
    np.random.seed(42)
    robots = []
    for robot_id in [1, 2, 3]:
        n = 100
        ts = np.linspace(0, 5, n).tolist()
        robots.append({
            'id': robot_id,
            'timestamp': ts,
            'values': [
                {
                    'name': 'X Position',
                    'alias': 'x',
                    'unit': 'm',
                    'timestamp': ts,
                    'value': np.sin(np.linspace(0, 2 * np.pi, n) * robot_id).tolist(),
                },
                {
                    'name': 'Y Position',
                    'alias': 'y',
                    'unit': 'm',
                    'timestamp': ts,
                    'value': np.cos(np.linspace(0, 2 * np.pi, n) * robot_id).tolist(),
                },
                {
                    'name': 'Yaw Angle',
                    'alias': 'yaw',
                    'unit': 'rad',
                    'timestamp': ts,
                    'value': (np.linspace(0, np.pi, n) * robot_id).tolist(),
                },
                {
                    'name': 'Battery',
                    'alias': 'batt',
                    'unit': 'mV',
                    'timestamp': ts,
                    'value': (4200 - np.linspace(0, 500, n)).tolist(),
                },
            ],
        })
    return robots


@pytest.fixture
def interpreter(sample_data):
    from mr_dapa.helpers.base_interpreter import BaseInterpreter
    return BaseInterpreter(sample_data)


@pytest.fixture
def components_config():
    return {
        'x': {'title': 'X Position', 'class': 'LinesComponent', 'keys': ['x']},
        'y': {'title': 'Y Position', 'class': 'LinesComponent', 'keys': ['y']},
        'xy': {'title': 'X & Y', 'class': 'LinesComponent', 'keys': ['x', 'y']},
        'map': {
            'title': 'Map',
            'class': 'MapComponent',
            'limits': {'x': [-2, 2], 'y': [-2, 2]},
        },
    }
