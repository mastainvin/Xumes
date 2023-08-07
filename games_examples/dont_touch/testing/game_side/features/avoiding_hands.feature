Feature: Avoiding hands

  @left
  Scenario: Avoiding left hand
    Given A game with a player
    And 1 left hand and 0 right hand
    When There is 1 left hand at -80 and 0 right hand at 0
    Then The player should avoid 1 hands

  @right
  Scenario: Avoiding right hand
    Given A game with a player
    And 0 left hand and 1 right hand
    When There is 0 left hand at 0 and 1 right hand at 280
    Then The player should avoid 1 hands

  @both
  Scenario: Avoiding both hands
    Given A game with a player
    And 1 left hand and 1 right hand
    When There is 1 left hand at -80 and 1 right hand at 280
    Then The player should avoid 2 hands