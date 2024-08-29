import ast
import os
import re
from typing import Dict, List

from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner

from xumes.core.registry import get_content_from_registry
from xumes.test_automation.feature_strategy import FeatureStrategy, Feature, Scenario


class GherkinFeatureStrategy(FeatureStrategy):
    """
    Gherkin language implementation of FeatureStrategy.
    Using the .feature files, we can get all features and scenarios.
    It also implements a way to filter the features and scenarios that we want to run.
    """
    def __init__(self, alpha: float = 0.001, features_names: List[str] = None, scenarios_names: List[str] = None,
                 tags: str = None, steps_path: str = None, features_path: str = "./"):
        super().__init__(alpha, steps_path, features_path)
        self._selected_features: List[str] = features_names
        self._selected_scenarios: List[str] = scenarios_names
        self._selected_tags: str = tags
        self._steps = []

    def retrieve_features(self):
        """
        Get features and scenarios from every feature file ".feature" in the "./features" directory.
        """

        # Convert steps files to list of gherkin steps
        self._convert_steps_files_to_gherkin_steps()

        # Get all feature files
        feature_files = os.listdir(self._features_path)
        feature_files = [file for file in feature_files if file.endswith(".feature")]

        # If there are no feature files, raise an exception
        if len(feature_files) == 0:
            raise Exception("Feature files not found.")

        # Initialize parser
        parser = Parser()

        # Iterate over feature files
        for feature_file in feature_files:
            if self._selected_features is None or feature_file[:-8] in self._selected_features:
                # We open the feature file and parse it
                feature_path = os.path.join(self._features_path, feature_file)

                with open(feature_path, 'r') as file:
                    feature = parser.parse(TokenScanner(file.read()))['feature']

                    # Create a Feature object
                    feature_obj = Feature(name=feature_file[:-8])

                    # Iterate over every scenario in the feature file
                    for element in feature['children']:
                        if 'scenario' in element:
                            scenario = element['scenario']
                            if scenario['keyword'] == 'Scenario Outline':
                                # Handle Scenario Outline
                                self._process_scenario_outline(scenario, feature_obj)
                            elif scenario['keyword'] == 'Scenario':
                                # Handle regular Scenario
                                self._process_scenario(scenario, feature_obj)

                    # Append the feature to the list of features
                    self.features.append(feature_obj)

    def _process_scenario_outline(self, scenario_outline: Dict, feature_obj: Feature):
        """
        Process a Scenario Outline and generate scenarios for each example row.
        """
        examples = scenario_outline['examples']
        example_count = 0  # Initialize example counter for this scenario outline
        for example in examples:
            headers = [cell['value'] for cell in example['tableHeader']['cells']]
            for row in example['tableBody']:
                example_values = {headers[i]: cell['value'] for i, cell in enumerate(row['cells'])}
                example_description = ', '.join([f"{key}={value}" for key, value in example_values.items()])
                scenario_name = f"{scenario_outline['name']} [{example_count}] - ({example_description})"
                example_count += 1  # Increment example counter for this scenario outline
                scenario_copy = self._create_scenario_from_outline(scenario_outline, example_values, scenario_name)
                if self._selected_scenarios is None or scenario_copy['name'] in self._selected_scenarios:
                    self._process_scenario(scenario_copy, feature_obj, is_outline=True)

    def _create_scenario_from_outline(self, scenario_outline: Dict, example_values: Dict[str, str], scenario_name: str) -> Dict:
        """
        Create a scenario from a scenario outline by replacing placeholders with example values.
        """
        scenario_copy = {
            'name': scenario_name,
            'steps': [],
            'tags': scenario_outline.get('tags', [])
        }
        for step in scenario_outline['steps']:
            step_text = step['text']
            for placeholder, value in example_values.items():
                step_text = step_text.replace(f"<{placeholder}>", value)
            scenario_copy['steps'].append({
                'keyword': step['keyword'],
                'keywordType': step['keywordType'],
                'text': step_text
            })
        return scenario_copy

    def _process_scenario(self, scenario: Dict, feature_obj: Feature, is_outline: bool = False):
        """
        Process a single scenario and add it to the feature object.
        """
        has_tag, scenario_tags = self.has_tags(scenario)

        # Check if the scenario name matches the selected scenarios
        if (self._selected_scenarios is None or scenario['name'] in self._selected_scenarios) and has_tag:
            # Find the steps file for the scenario using pattern matching
            steps_file, given_params, when_params, then_params = self._find_steps_file(scenario, feature_obj.name)

            # Fill parameters
            for i in range(len(given_params)):
                self.given.all[steps_file][i].add_params(scenario['name'], given_params[i])
            for i in range(len(when_params)):
                self.when.all[steps_file][i].add_params(scenario['name'], when_params[i])
            for i in range(len(then_params)):
                self.then.all[steps_file][i].add_params(scenario['name'], then_params[i])

            # Create a Scenario object
            scenario_obj = Scenario(scenario['name'], steps_file, feature_obj, scenario_tags)
            feature_obj.scenarios.append(scenario_obj)

    def has_tags(self, scenario):
        scenario_tags = [tag['name'][1:] for tag in scenario.get('tags', [])]  # Remove '@' from tags

        if not self._selected_tags:
            return True, scenario_tags

        expression = self._selected_tags

        # Handle wildcard expressions
        if expression.startswith('.*'):
            suffix = expression[2:]
            has_tag = any(tag.endswith(suffix) for tag in scenario_tags)
            return has_tag, scenario_tags

        if expression.startswith('*') and expression.endswith('*'):
            contains = expression[1:-1]
            has_tag = any(contains in tag for tag in scenario_tags)
            return has_tag, scenario_tags

        if expression.endswith('.*'):
            prefix = expression[:-2]
            has_tag = any(tag.startswith(prefix) for tag in scenario_tags)
            return has_tag, scenario_tags

        # Replace logical operators
        expression = expression.replace("and", "&&").replace("or", "||").replace("not ", "!")

        # Replace simple tag names with presence check in scenario_tags
        expression = re.sub(r'(\b\w+\b)', r'"\1" in scenario_tags', expression)

        # Replace logical operators back to Python syntax
        expression = expression.replace("&&", "and").replace("||", "or").replace("!", "not ")

        try:
            has_tag = eval(expression)
        except Exception as e:
            has_tag = False

        return has_tag, scenario_tags

    def _convert_steps_files_to_gherkin_steps(self):
        """
        Convert steps files to list of gherkin steps
        Just taking the content of the steps files and putting in the gherkin steps list
        """
        self._steps.clear()
        for name in self.given.all:
            try:
                given = self.given.all[name]
            except IndexError:
                raise Exception("Given steps not found.")
            try:
                when = self.when.all[name]
            except IndexError:
                raise Exception("When steps not found.")
            try:
                then = self.then.all[name]
            except IndexError:
                raise Exception("Then steps not found.")

            given_contents = get_content_from_registry(given)
            when_contents = get_content_from_registry(when)
            then_contents = get_content_from_registry(then)

            self._steps.append({
                "name": name,
                "given_contents": given_contents,
                "when_contents": when_contents,
                "then_contents": then_contents
            })

    def _find_steps_file(self, scenario: Dict, feature_name: str):
        """
        Find the steps file for the scenario using pattern matching.
        """
        # Get scenario name
        previous_type = None
        scenario_givens = []
        scenario_whens = []
        scenario_thens = []

        # Iterate over steps
        # And convert the steps to a list of gherkin steps
        # Check the gherkin-official package for more information
        for step in scenario['steps']:
            if step['keywordType'] == "Context" or (
                    step['keywordType'] == "Conjunction" and previous_type == "Context"):
                scenario_givens.append(step['text'])
                previous_type = "Context"
            elif step['keywordType'] == "Action" or (
                    step['keywordType'] == "Conjunction" and previous_type == "Action"):
                scenario_whens.append(step['text'])
                previous_type = "Action"
            elif step['keywordType'] == "Outcome" or (
                    step['keywordType'] == "Conjunction" and previous_type == "Outcome"):
                scenario_thens.append(step['text'])
                previous_type = "Outcome"
            else:
                raise Exception("Keyword type not found.")

        # Iterate over steps files
        for steps_file in self._steps:
            # Get steps file name
            steps_file_name = steps_file['name']
            steps_file_givens = steps_file['given_contents']
            steps_file_whens = steps_file['when_contents']
            steps_file_thens = steps_file['then_contents']

            # Check if the scenario contents corresponds to the steps file contents
            given_parameters = self._steps_matching(steps_file_givens, scenario_givens)
            when_parameters = self._steps_matching(steps_file_whens, scenario_whens)
            then_parameters = self._steps_matching(steps_file_thens, scenario_thens)

            if given_parameters != False and when_parameters != False and then_parameters != False:
                return steps_file_name, given_parameters, when_parameters, then_parameters
        # If no steps file was found, raise an exception
        raise Exception(f"Steps file for scenario: {feature_name}/{scenario['name']} not found.")

    @staticmethod
    def _steps_matching(step_files_steps, scenario_steps):
        # Check if the step files steps corresponds to the scenario steps
        # And return parameters if it does
        if len(step_files_steps) == len(scenario_steps):
            tmp = []
            for i in range(len(step_files_steps)):
                param = GherkinFeatureStrategy._pattern_matching(step_files_steps[i], scenario_steps[i])
                # noinspection PySimplifyBooleanCheck
                if param != False:
                    tmp.append(param)
                else:
                    tmp = False
                    break
            return tmp
        else:
            return False

    @staticmethod
    def _pattern_matching(step: str, scenario: str):
        # Check if the step str corresponds to the scenario str
        # And return parameters if it does

        # Pattern to match parameters with type
        param_pattern = re.compile(r'\{(\w+):(\w+)\}')

        # Split step and scenario
        step_parts = step.split(" ")
        scenario_parts = scenario.split(" ")

        # If the length of the step is different from the length of the scenario, return False
        if len(step_parts) != len(scenario_parts):
            return False

        # Iterate over step and scenario
        parameters = {}
        for i in range(len(step_parts)):
            match = param_pattern.match(step_parts[i])
            if match:
                param_name, param_type = match.groups()
                param_value = scenario_parts[i]

                # Convert the parameter value to the appropriate type
                if param_type == 'd':
                    param_value = int(param_value)
                elif param_type == 'f':
                    param_value = float(param_value)
                elif param_type == 's':
                    param_value = str(param_value)
                elif param_type == 'b':
                    param_value = param_value.lower() == 'true'
                elif param_type in ['array', 'list']:
                    param_value= ast.literal_eval(param_value)
                else:
                    return False

                parameters[param_name] = param_value
            elif step_parts[i] != scenario_parts[i]:
                return False

        # If the step and scenario are equal, return the parameters those can be empty
        return parameters
