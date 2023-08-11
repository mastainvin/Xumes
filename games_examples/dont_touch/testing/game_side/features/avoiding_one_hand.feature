Feature: Avoiding one hand

  @left50
  Scenario: Avoiding left hand at -50
    Given A game with a player
    And 1 left hand
    When There is 1 left hand at -50
    Then The player should avoid 1 hands

  @left0
  Scenario: Avoiding left hand at 0
    Given A game with a player
    And 1 left hand
    When There is 1 left hand at 0
    Then The player should avoid 1 hands

  @left119
  Scenario: Avoiding left hand at 119
    Given A game with a player
    And 1 left hand
    When There is 1 left hand at 119
    Then The player should avoid 1 hands

  @right260
  Scenario: Avoiding right hand at 260
    Given A game with a player
    And 1 right hand
    When There is 1 right hand at 260
    Then The player should avoid 1 hands

  @tight300
  Scenario: Avoiding right hand at 300
    Given A game with a player
    And 1 right hand
    When There is 1 right hand at 300
    Then The player should avoid 1 hands

  @right359
  Scenario: Avoiding right hand at 359
    Given A game with a player
    And 1 right hand
    When There is 1 right hand at 359
    Then The player should avoid 1 hands