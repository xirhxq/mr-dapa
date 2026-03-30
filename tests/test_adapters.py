import json
import pytest
import numpy as np

from mr_dapa.adapters.json_adapter import JSONAdapter
from mr_dapa.adapters.csv_adapter import CSVAdapter
from mr_dapa.adapters.multi_file_adapter import MultiFileAdapter
from mr_dapa.adapters.numpy_adapter import NumPyAdapter
from mr_dapa.helpers.base_interpreter import BaseInterpreter


class TestJSONAdapter:
    def test_load_from_file(self, tmp_path, sample_data):
        data_file = tmp_path / 'data.json'
        data_file.write_text(json.dumps(sample_data))
        adapter = JSONAdapter()
        result = adapter.load(str(data_file))
        assert result == sample_data

    def test_load_from_list(self, sample_data):
        adapter = JSONAdapter()
        result = adapter.load(sample_data)
        assert result == sample_data

    def test_rejects_invalid_type(self):
        adapter = JSONAdapter()
        with pytest.raises(TypeError):
            adapter.load(42)

    def test_load_produces_valid_data(self, tmp_path, sample_data):
        data_file = tmp_path / 'data.json'
        data_file.write_text(json.dumps(sample_data))
        adapter = JSONAdapter()
        result = adapter.load(str(data_file))
        interp = BaseInterpreter(result)
        assert interp.get_robot_number() == 3


class TestCSVAdapter:
    def test_load_csv(self, tmp_path):
        csv_content = "id,timestamp,x,y\n1,0.0,1.0,2.0\n1,1.0,1.5,2.5\n2,0.0,3.0,4.0\n2,1.0,3.5,4.5\n"
        csv_file = tmp_path / 'data.csv'
        csv_file.write_text(csv_content)
        adapter = CSVAdapter()
        result = adapter.load(str(csv_file))
        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[1]['id'] == 2

    def test_csv_values_structure(self, tmp_path):
        csv_content = "id,timestamp,x,y\n1,0.0,1.0,2.0\n1,1.0,1.5,2.5\n"
        csv_file = tmp_path / 'data.csv'
        csv_file.write_text(csv_content)
        adapter = CSVAdapter()
        result = adapter.load(str(csv_file))
        robot = result[0]
        assert 'values' in robot
        assert len(robot['values']) == 2
        value_names = [v['name'] for v in robot['values']]
        assert 'x' in value_names
        assert 'y' in value_names

    def test_csv_timestamps(self, tmp_path):
        csv_content = "id,timestamp,x\n1,0.0,1.0\n1,1.0,2.0\n1,2.0,3.0\n"
        csv_file = tmp_path / 'data.csv'
        csv_file.write_text(csv_content)
        adapter = CSVAdapter()
        result = adapter.load(str(csv_file))
        robot = result[0]
        x_val = [v for v in robot['values'] if v['name'] == 'x'][0]
        assert x_val['value'] == [1.0, 2.0, 3.0]

    def test_csv_produces_valid_data(self, tmp_path):
        csv_content = "id,timestamp,x,y\n1,0.0,1.0,2.0\n1,1.0,1.5,2.5\n2,0.0,3.0,4.0\n"
        csv_file = tmp_path / 'data.csv'
        csv_file.write_text(csv_content)
        adapter = CSVAdapter()
        result = adapter.load(str(csv_file))
        interp = BaseInterpreter(result)
        assert interp.get_robot_number() == 2

    def test_csv_rejects_non_string(self):
        adapter = CSVAdapter()
        with pytest.raises(TypeError, match="file path"):
            adapter.load([])

    def test_csv_custom_separator(self, tmp_path):
        csv_content = "id;timestamp;x\n1;0.0;1.0\n1;1.0;2.0\n"
        csv_file = tmp_path / 'data.csv'
        csv_file.write_text(csv_content)
        adapter = CSVAdapter(separator=';')
        result = adapter.load(str(csv_file))
        assert len(result) == 1
        assert result[0]['id'] == 1

    def test_csv_custom_columns(self, tmp_path):
        csv_content = "robot,time,pos\n1,0.0,10.0\n1,1.0,20.0\n"
        csv_file = tmp_path / 'data.csv'
        csv_file.write_text(csv_content)
        adapter = CSVAdapter(id_col='robot', timestamp_col='time')
        result = adapter.load(str(csv_file))
        assert len(result) == 1
        pos = [v for v in result[0]['values'] if v['name'] == 'pos'][0]
        assert pos['value'] == [10.0, 20.0]


class TestMultiFileAdapter:
    def test_load_multiple_files(self, tmp_path, sample_data):
        f1 = tmp_path / 'r1.json'
        f2 = tmp_path / 'r2.json'
        f1.write_text(json.dumps([sample_data[0]]))
        f2.write_text(json.dumps([sample_data[1]]))
        adapter = MultiFileAdapter()
        result = adapter.load([str(f1), str(f2)])
        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[1]['id'] == 2

    def test_merges_multiple_robots_per_file(self, tmp_path, sample_data):
        f1 = tmp_path / 'all.json'
        f1.write_text(json.dumps(sample_data))
        adapter = MultiFileAdapter()
        result = adapter.load([str(f1)])
        assert len(result) == 3

    def test_rejects_non_path_list(self):
        adapter = MultiFileAdapter()
        with pytest.raises(TypeError):
            adapter.load("single_path")

    def test_produces_valid_data(self, tmp_path, sample_data):
        f1 = tmp_path / 'a.json'
        f2 = tmp_path / 'b.json'
        f1.write_text(json.dumps([sample_data[0]]))
        f2.write_text(json.dumps([sample_data[1]]))
        adapter = MultiFileAdapter()
        result = adapter.load([str(f1), str(f2)])
        interp = BaseInterpreter(result)
        assert interp.get_robot_number() == 2


class TestNumPyAdapter:
    def test_load_dict(self):
        np.random.seed(42)
        source = {
            1: {
                'timestamp': [0.0, 1.0, 2.0],
                'values': {
                    'x': np.array([1.0, 2.0, 3.0]),
                    'y': np.array([4.0, 5.0, 6.0]),
                },
                'units': {'x': 'm', 'y': 'm'},
            }
        }
        adapter = NumPyAdapter()
        result = adapter.load(source)
        assert len(result) == 1
        assert result[0]['id'] == 1
        x_vals = [v for v in result[0]['values'] if v['name'] == 'x'][0]
        assert x_vals['value'] == [1.0, 2.0, 3.0]
        assert x_vals['unit'] == 'm'

    def test_multiple_robots(self):
        source = {
            1: {
                'timestamp': [0.0, 1.0],
                'values': {'x': np.array([1.0, 2.0])},
            },
            2: {
                'timestamp': [0.0, 1.0],
                'values': {'x': np.array([3.0, 4.0])},
            },
        }
        adapter = NumPyAdapter()
        result = adapter.load(source)
        assert len(result) == 2

    def test_no_timestamp_generates_indices(self):
        source = {
            1: {
                'values': {'x': np.array([10.0, 20.0, 30.0])},
            }
        }
        adapter = NumPyAdapter()
        result = adapter.load(source)
        x_val = [v for v in result[0]['values'] if v['name'] == 'x'][0]
        assert x_val['timestamp'] == [0, 1, 2]

    def test_rejects_non_dict(self):
        adapter = NumPyAdapter()
        with pytest.raises(TypeError, match="dict"):
            adapter.load([1, 2, 3])

    def test_produces_valid_data(self):
        source = {
            1: {
                'timestamp': [0.0, 1.0],
                'values': {'x': np.array([1.0, 2.0])},
                'units': {'x': 'm'},
            }
        }
        adapter = NumPyAdapter()
        result = adapter.load(source)
        interp = BaseInterpreter(result)
        assert interp.get_robot_number() == 1
