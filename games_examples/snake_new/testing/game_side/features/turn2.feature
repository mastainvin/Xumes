Feature: Convert Reward Function

  Scenario: Calculate reward based on distance and game state
    Given the snake entity exists
    And the fruit entity exists
    When the distance between the fruit and snake head decreases
    Then the distance is stored

    When the game state is "fruit_ate"
    Then the reward is 10

    When the game state is "lose"
    Then the reward is -100

    When the game state is neither "fruit_ate" nor "lose"
    Then the close reward is calculated based on the distance

  Scenario: Calculate close reward based on distance
    Given the snake entity exists
    And the fruit entity exists
    And the distance between the fruit and snake head is stored
    When the distance is less than the stored distance
    Then the close reward is 1

    When the distance is greater than the stored distance
    Then the close reward is -1

    When the distance is equal to the stored distance
    Then the close reward is 0