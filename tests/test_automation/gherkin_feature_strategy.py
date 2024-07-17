import unittest

from unittest.mock import MagicMock
from src.xumes.test_automation.implementations.features_impl.gherkin_feature_strategy import GherkinFeatureStrategy


class TestGherkinFeatureStrategy(unittest.TestCase):
    def setUp(self):
        self.strategy = GherkinFeatureStrategy(features_path="./", steps_path="./")

    def test_has_tags_with_no_selected_tags(self):
        scenario = {'tags': [{'name': '@tag1'}, {'name': '@tag2'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['tag1', 'tag2'])

    def test_has_tags_with_matching_selected_tags(self):
        self.strategy._selected_tags = 'tag1 and tag2'
        scenario = {'tags': [{'name': '@tag1'}, {'name': '@tag2'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['tag1', 'tag2'])

    def test_has_tags_with_non_matching_selected_tags(self):
        self.strategy._selected_tags = 'tag1 and tag3'
        scenario = {'tags': [{'name': '@tag1'}, {'name': '@tag2'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertFalse(has_tag)
        self.assertEqual(scenario_tags, ['tag1', 'tag2'])

    def test_has_tags_with_complex_selected_tags_expression(self):
        self.strategy._selected_tags = 'tag1 and (tag2 or tag3)'
        scenario = {'tags': [{'name': '@tag1'}, {'name': '@tag2'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['tag1', 'tag2'])

    def test_has_tags_with_no_tags_in_scenario(self):
        self.strategy._selected_tags = 'tag1 and tag2'
        scenario = {}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertFalse(has_tag)

    def test_has_tags_with_no_selected_tags_and_no_tags_in_scenario(self):
        scenario = {}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, [])

    def test_has_tags_with_or_and_tags_expression(self):
        self.strategy._selected_tags = 'tag1 or (tag2 and tag3)'
        scenario = {'tags': [{'name': '@tag1'}, {'name': '@tag2'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['tag1', 'tag2'])

        scenario = {'tags': [{'name': '@tag2'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertFalse(has_tag)
        self.assertEqual(scenario_tags, ['tag2'])

        scenario = {'tags': [{'name': '@tag3'}, {'name': '@tag2'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['tag3', 'tag2'])

    def test_has_tags_with_and_or_tags_expression(self):
        self.strategy._selected_tags = 'tag1 and (tag2 or tag3)'
        scenario = {'tags': [{'name': '@tag1'}, {'name': '@tag2'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['tag1', 'tag2'])

        scenario = {'tags': [{'name': '@tag1'}, {'name': '@tag3'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['tag1', 'tag3'])

        scenario = {'tags': [{'name': '@tag1'}, {'name': '@tag2'}, {'name': '@tag3'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['tag1', 'tag2', 'tag3'])

    def test_three_ands(self):
        self.strategy._selected_tags = 'tag1 and tag2 and tag3'
        scenario = {'tags': [{'name': '@tag1'}, {'name': '@tag2'}, {'name': '@tag3'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['tag1', 'tag2', 'tag3'])

    def test_wildcard_start_with(self):
        self.strategy._selected_tags = 'tag.*'
        scenario = {'tags': [{'name': '@tag1'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['tag1'])

        scenario = {'tags': [{'name': '@zzzz'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertFalse(has_tag)
        self.assertEqual(scenario_tags, ['zzzz'])

        scenario = {'tags': [{'name': '@tag1'}, {'name': '@tag2'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['tag1', 'tag2'])

        scenario = {'tags': [{'name': '@ta'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertFalse(has_tag)
        self.assertEqual(scenario_tags, ['ta'])

    def test_wild_end_with(self):
        self.strategy._selected_tags = '.*1'
        scenario = {'tags': [{'name': '@tag1'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['tag1'])

        scenario = {'tags': [{'name': '@zzzz'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertFalse(has_tag)
        self.assertEqual(scenario_tags, ['zzzz'])

        scenario = {'tags': [{'name': '@tag1'}, {'name': '@tag2'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['tag1', 'tag2'])

        scenario = {'tags': [{'name': '@ta'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertFalse(has_tag)
        self.assertEqual(scenario_tags, ['ta'])

    def test_wildcard_contains(self):
        self.strategy._selected_tags = '*a*'
        scenario = {'tags': [{'name': '@tag1'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['tag1'])

        scenario = {'tags': [{'name': '@zzzz'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertFalse(has_tag)
        self.assertEqual(scenario_tags, ['zzzz'])

        scenario = {'tags': [{'name': '@tag1'}, {'name': '@tag2'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['tag1', 'tag2'])

        scenario = {'tags': [{'name': '@ta'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['ta'])

        self.strategy._selected_tags = '*aaa*'
        scenario = {'tags': [{'name': '@tag1'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertFalse(has_tag)
        self.assertEqual(scenario_tags, ['tag1'])

        scenario = {'tags': [{'name': '@zaz'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertFalse(has_tag)
        self.assertEqual(scenario_tags, ['zaz'])

        scenario = {'tags': [{'name': '@zaaaz'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['zaaaz'])

        scenario = {'tags': [{'name': '@aaa'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['aaa'])

    def test_not_expression(self):
        self.strategy._selected_tags = 'not tag1'
        scenario = {'tags': [{'name': '@tag1'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertFalse(has_tag)
        self.assertEqual(scenario_tags, ['tag1'])

        scenario = {'tags': [{'name': '@tag2'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['tag2'])

        self.strategy._selected_tags = 'not (tag1 or tag2)'
        scenario = {'tags': [{'name': '@tag1'}, {'name': '@tag2'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertFalse(has_tag)
        self.assertEqual(scenario_tags, ['tag1', 'tag2'])

        scenario = {'tags': [{'name': '@tag1'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertFalse(has_tag)
        self.assertEqual(scenario_tags, ['tag1'])

        scenario = {'tags': [{'name': '@tag2'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertFalse(has_tag)
        self.assertEqual(scenario_tags, ['tag2'])

        scenario = {'tags': [{'name': '@tag3'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)
        self.assertEqual(scenario_tags, ['tag3'])

        self.strategy._selected_tags = 'not (tag1 and tag2)'
        scenario = {'tags': [{'name': '@tag1'}, {'name': '@tag2'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertFalse(has_tag)
        self.assertEqual(scenario_tags, ['tag1', 'tag2'])

        self.strategy._selected_tags = 'tag1 and not tag2'
        scenario = {'tags': [{'name': '@tag1'}, {'name': '@tag2'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertFalse(has_tag)
        self.assertEqual(scenario_tags, ['tag1', 'tag2'])

        scenario = {'tags': [{'name': '@tag1'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertTrue(has_tag)

        scenario = {'tags': [{'name': '@tag2'}]}
        has_tag, scenario_tags = self.strategy.has_tags(scenario)
        self.assertFalse(has_tag)
        self.assertEqual(scenario_tags, ['tag2'])

