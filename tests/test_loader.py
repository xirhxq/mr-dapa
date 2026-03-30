import json
import pytest

from mr_dapa.helpers.loader import DataLoader


class TestDataLoaderJSON:
    def test_loads_json_file(self, tmp_path, sample_data):
        data_file = tmp_path / 'data.json'
        data_file.write_text(json.dumps(sample_data))
        loader = DataLoader(str(data_file))
        assert loader.data == sample_data

    def test_file_attribute(self, tmp_path, sample_data):
        data_file = tmp_path / 'data.json'
        data_file.write_text(json.dumps(sample_data))
        loader = DataLoader(str(data_file))
        assert loader.file == str(data_file)

    def test_folder_attribute(self, tmp_path, sample_data):
        data_file = tmp_path / 'data.json'
        data_file.write_text(json.dumps(sample_data))
        loader = DataLoader(str(data_file))
        assert loader.folder == str(tmp_path)

    def test_single_file_as_string(self, tmp_path, sample_data):
        data_file = tmp_path / 'data.json'
        data_file.write_text(json.dumps(sample_data))
        loader = DataLoader(str(data_file))
        assert isinstance(loader.datas, list)
        assert len(loader.datas) == 1

    def test_multiple_files(self, tmp_path, sample_data):
        f1 = tmp_path / 'a.json'
        f2 = tmp_path / 'b.json'
        f1.write_text(json.dumps([sample_data[0]]))
        f2.write_text(json.dumps([sample_data[1]]))
        loader = DataLoader([str(f1), str(f2)])
        assert len(loader.datas) == 2

    def test_file_handle_closed(self, tmp_path, sample_data):
        data_file = tmp_path / 'data.json'
        data_file.write_text(json.dumps(sample_data))
        loader = DataLoader(str(data_file))
        data_file.write_text(json.dumps(sample_data))
