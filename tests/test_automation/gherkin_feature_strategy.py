import unittest
from unittest.mock import patch, MagicMock
from src.xumes.test_automation.implementations.features_impl.gherkin_feature_strategy import GherkinFeatureStrategy


class GherkinFeatureStrategyTests(unittest.TestCase):

    def setUp(self):
        self.strategy = GherkinFeatureStrategy()

    @patch('os.listdir')
    @patch('builtins.open', new_callable=MagicMock)
    def test_retrieve_feature_loads_feature_files(self, mock_open, mock_listdir):
        mock_listdir.return_value = ['test1.feature', 'test2.feature', 'test3.txt']
        mock_open.return_value.__enter__.return_value.read.return_value = 'Feature: Test Feature'

        self.strategy.retrieve_feature('./')

        self.assertEqual(len(self.strategy.features), 2)

    @patch.object(GherkinFeatureStrategy, '_find_steps_file')
    @patch.object(GherkinFeatureStrategy, '_process_scenario')
    def test_retrieve_feature_processes_scenarios(self, mock_process_scenario, mock_find_steps_file):
        mock_find_steps_file.return_value = ('test', [], [], [])
        self.strategy._steps = [{'name': 'test', 'given_contents': [], 'when_contents': [], 'then_contents': []}]
        self.strategy.retrieve_feature('./')

        self.assertEqual(mock_process_scenario.call_count, 2)

    def test_steps_matching_returns_parameters(self):
        result = self.strategy._steps_matching(['{param1:d}'], ['5'])
        self.assertEqual(result, [{'param1': 5}])

    def test_steps_matching_returns_false_for_mismatch(self):
        result = self.strategy._steps_matching(['{param1:d}'], ['five'])
        self.assertFalse(result)

    def test_pattern_matching_returns_parameters(self):
        result = self.strategy._pattern_matching('{param1:d}', '5')
        self.assertEqual(result, {'param1': 5})

    def test_pattern_matching_returns_false_for_mismatch(self):
        result = self.strategy._pattern_matching('{param1:d}', 'five')
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
