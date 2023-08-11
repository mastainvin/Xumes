Feature: Avoiding two hands

  @both
  Scenario: Avoiding both hands
    Given A game with a player
    And 1 left hand and 1 right hand
    When There is 1 left hand at 0 and 1 right hand at 280
    Then The player should avoid 2 hands