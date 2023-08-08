Feature: Avoiding one hand

  @left
  Scenario: Avoiding left hand
    Given A game with a player
    And 1 left hand
    When There is 1 left hand at 0
    Then The player should avoid 1 hands

  @right
  Scenario: Avoiding right hand
    Given A game with a player
    And 1 right hand
    When There is 1 right hand at 280
    Then The player should avoid 1 hands