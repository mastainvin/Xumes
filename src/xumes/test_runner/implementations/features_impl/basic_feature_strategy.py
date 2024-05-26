import os

from xumes.test_runner.feature_strategy import FeatureStrategy, Feature, Scenario


class BasicFeatureStrategy(FeatureStrategy):

    def retrieve_feature(self):
        """
        Get features and scenarios from a feature file ".feature" in the test directory.
        The feature file must be in the following format:
        Feature: <feature_name>
            Scenario: <scenario_name>
            Scenario: <scenario_name>
        Feature: <feature_name>
            Scenario: <scenario_name>
            Scenario: <scenario_name>
        """
        # Clear features
        self.features.clear()

        # Check if feature file exists
        if not os.path.exists(".features"):
            raise Exception("Feature file not found.")

        # Open feature file
        with open(".features", 'r') as feature_file:
            # Read all lines
            lines = feature_file.readlines()
            # Initialize feature
            feature = None
            # Iterate over lines
            for line in lines:
                # Remove spaces and \n
                line = line.strip()

                if line.startswith("Feature:"):

                    # Save the previous feature
                    if feature is not None:
                        self.features.append(feature)

                    # If line starts with "Feature:" then create a new feature
                    feature_name = line.replace("Feature:", "").strip()
                    feature = Feature(name=feature_name)
                elif line.startswith("Scenario:"):
                    # If line starts with "Scenario:" then create a new scenario
                    scenario_name = line.replace("Scenario:", "").strip()
                    scenario = Scenario(name=scenario_name, steps=scenario_name, feature=feature)
                    feature.scenarios.append(scenario)

            if feature is not None:
                self.features.append(feature)
