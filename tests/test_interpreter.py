import pytest

from mr_dapa.helpers.base_interpreter import BaseInterpreter


class TestBaseInterpreterConstruction:
    def test_valid_data(self, sample_data):
        interp = BaseInterpreter(sample_data)
        assert interp.get_robot_number() == 3
        assert interp.id_list == [1, 2, 3]

    def test_rejects_non_list(self):
        with pytest.raises(AssertionError, match="list"):
            BaseInterpreter({"not": "a list"})

    def test_rejects_missing_id(self, sample_data):
        bad_data = [{'values': []}]
        with pytest.raises(AssertionError, match="id"):
            BaseInterpreter(bad_data)

    def test_rejects_missing_values(self, sample_data):
        bad_data = [{'id': 1}]
        with pytest.raises(AssertionError, match="values"):
            BaseInterpreter(bad_data)

    def test_rejects_values_not_list(self):
        bad_data = [{'id': 1, 'values': 'not a list'}]
        with pytest.raises(AssertionError, match="list"):
            BaseInterpreter(bad_data)

    def test_rejects_missing_name_in_value(self):
        bad_data = [{'id': 1, 'values': [{'alias': 'a', 'unit': 'm', 'value': [1.0]}]}]
        with pytest.raises(AssertionError, match="name"):
            BaseInterpreter(bad_data)

    def test_rejects_missing_alias_in_value(self):
        bad_data = [{'id': 1, 'values': [{'name': 'a', 'unit': 'm', 'value': [1.0]}]}]
        with pytest.raises(AssertionError, match="alias"):
            BaseInterpreter(bad_data)

    def test_rejects_missing_unit_in_value(self):
        bad_data = [{'id': 1, 'values': [{'name': 'a', 'alias': 'a', 'value': [1.0]}]}]
        with pytest.raises(AssertionError, match="unit"):
            BaseInterpreter(bad_data)

    def test_rejects_missing_value_key(self):
        bad_data = [{'id': 1, 'timestamp': [0.0], 'values': [{'name': 'a', 'alias': 'a', 'unit': 'm', 'timestamp': [0.0]}]}]
        with pytest.raises(AssertionError, match="value"):
            BaseInterpreter(bad_data)

    def test_rejects_value_not_list(self):
        bad_data = [{'id': 1, 'timestamp': [0.0], 'values': [{'name': 'a', 'alias': 'a', 'unit': 'm', 'timestamp': [0.0], 'value': 42}]}]
        with pytest.raises(AssertionError, match="list"):
            BaseInterpreter(bad_data)

    def test_rejects_timestamp_value_length_mismatch(self):
        bad_data = [{'id': 1, 'values': [{'name': 'a', 'alias': 'a', 'unit': 'm', 'timestamp': [0.0, 1.0], 'value': [1.0]}]}]
        with pytest.raises(AssertionError, match="same length"):
            BaseInterpreter(bad_data)

    def test_accepts_timestamp_on_robot_level(self):
        data = [{'id': 1, 'timestamp': [0.0, 1.0], 'values': [{'name': 'a', 'alias': 'a', 'unit': 'm', 'value': [1.0, 2.0]}]}]
        interp = BaseInterpreter(data)
        assert interp.get_robot_number() == 1


class TestForRobots:
    def test_returns_filtered_subset(self, interpreter):
        filtered = interpreter.for_robots([1])
        assert filtered.id_list == [1]
        assert filtered.get_robot_number() == 1

    def test_original_unchanged(self, interpreter):
        original_ids = list(interpreter.id_list)
        interpreter.for_robots([2])
        assert interpreter.id_list == original_ids

    def test_multiple_ids(self, interpreter):
        filtered = interpreter.for_robots([1, 3])
        assert set(filtered.id_list) == {1, 3}
        assert filtered.get_robot_number() == 2

    def test_nonexistent_id_ignored(self, interpreter):
        filtered = interpreter.for_robots([1, 99])
        assert filtered.id_list == [1]


class TestForTimeRange:
    def test_clamps_to_valid(self, interpreter):
        filtered = interpreter.for_time_range((1.0, 3.0))
        assert filtered.time_range == (1.0, 3.0)

    def test_clamps_to_earlier_start(self, interpreter):
        filtered = interpreter.for_time_range((-1.0, 2.0))
        assert filtered.time_range[0] == pytest.approx(0.0)

    def test_clamps_to_later_end(self, interpreter):
        filtered = interpreter.for_time_range((3.0, 100.0))
        assert filtered.time_range[1] == pytest.approx(5.0)

    def test_full_range(self, interpreter):
        assert interpreter.time_range[0] == pytest.approx(0.0)
        assert interpreter.time_range[1] == pytest.approx(5.0)

    def test_filtered_data_has_fewer_points(self, sample_data):
        full = BaseInterpreter(sample_data)
        clipped = full.for_time_range((1.0, 2.0))
        for robot in clipped.data:
            for value in robot['values']:
                for ts in value['timestamp']:
                    assert ts >= 1.0 - 0.1
                    assert ts <= 2.0 + 0.1


class TestForFirstLastSeconds:
    def test_first_seconds(self, interpreter):
        first = interpreter.for_first_seconds(2.0)
        assert first.time_range[0] == pytest.approx(0.0)
        assert first.time_range[1] == pytest.approx(2.0)

    def test_first_seconds_exceeds_duration(self, interpreter):
        first = interpreter.for_first_seconds(999.0)
        assert first.time_range[1] == pytest.approx(5.0)

    def test_last_seconds(self, interpreter):
        last = interpreter.for_last_seconds(2.0)
        assert last.time_range[0] == pytest.approx(3.0)
        assert last.time_range[1] == pytest.approx(5.0)

    def test_last_seconds_exceeds_duration(self, interpreter):
        last = interpreter.for_last_seconds(999.0)
        assert last.time_range[0] == pytest.approx(0.0)


class TestGetUnits:
    def test_single_key(self, interpreter):
        units = interpreter.get_units(['x'])
        assert units == ['m']

    def test_multiple_keys_same_unit(self, interpreter):
        units = interpreter.get_units(['x', 'y'])
        assert 'm' in units

    def test_different_units(self, interpreter):
        units = interpreter.get_units(['x', 'batt'])
        assert len(units) == 2
        assert 'm' in units
        assert 'mV' in units

    def test_nonexistent_key(self, interpreter):
        units = interpreter.get_units(['nonexistent'])
        assert units == []


class TestGetSuffixes:
    def test_title_suffix_all(self, interpreter):
        assert interpreter.get_title_suffix() == ', All Robots'

    def test_title_suffix_single(self, interpreter):
        filtered = interpreter.for_robots([1])
        assert filtered.get_title_suffix() == ', Robot #1'

    def test_title_suffix_multiple(self, interpreter):
        filtered = interpreter.for_robots([1, 3])
        suffix = filtered.get_title_suffix()
        assert 'Robots' in suffix
        assert '#1' in suffix
        assert '#3' in suffix

    def test_id_suffix_default(self, interpreter):
        assert interpreter.get_id_suffix() == ''

    def test_id_suffix_with_time_range(self, interpreter):
        filtered = interpreter.for_time_range((1.0, 3.0))
        suffix = filtered.get_id_suffix()
        assert '1.00s' in suffix
        assert '3.00s' in suffix

    def test_id_suffix_with_robot_filter(self, interpreter):
        filtered = interpreter.for_robots([2])
        suffix = filtered.get_id_suffix()
        assert '#2' in suffix


class TestChainedFiltering:
    def test_chain_robots_then_time(self, interpreter):
        chained = interpreter.for_robots([1]).for_time_range((0, 2))
        assert chained.id_list == [1]
        assert chained.time_range == (0.0, 2.0)
        assert chained.get_robot_number() == 1

    def test_chain_time_then_robots(self, interpreter):
        chained = interpreter.for_time_range((1, 3)).for_robots([2, 3])
        assert set(chained.id_list) == {2, 3}
        assert chained.time_range == (1.0, 3.0)

    def test_chain_all_three(self, interpreter):
        chained = interpreter.for_robots([1, 2]).for_first_seconds(1.0)
        assert set(chained.id_list) == {1, 2}
        assert chained.time_range[1] == pytest.approx(1.0)


class TestMiscMethods:
    def test_get_full_id_list(self, interpreter):
        full_ids = interpreter.get_full_id_list()
        assert full_ids == [1, 2, 3]

    def test_get_full_id_list_unchanged_by_filter(self, interpreter):
        filtered = interpreter.for_robots([1])
        assert filtered.get_full_id_list() == [1, 2, 3]

    def test_get_full_time_range(self, interpreter):
        tr = interpreter.get_full_time_range()
        assert tr[0] == pytest.approx(0.0)
        assert tr[1] == pytest.approx(5.0)

    def test_get_fps(self, interpreter):
        fps = interpreter.get_fps()
        assert fps > 0

    def test_empty_timestamps(self):
        data = [{'id': 1, 'timestamp': [], 'values': []}]
        interp = BaseInterpreter(data)
        assert interp.time_range == (0.0, 0.0)
