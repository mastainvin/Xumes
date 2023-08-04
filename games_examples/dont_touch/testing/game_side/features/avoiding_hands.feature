Feature: Avoiding hands

  @left
  Scenario: Avoiding left hand
    Given A game with 0 right hand and 1 left hand
    When There is a hand in 260 position
    Then The player should avoid 1 hands

  @right
  Scenario: Avoiding right hand
    Given A game with 1 right hand and 0 left hand
    When There is a hand in -50 position
    Then The player should avoid 1 hands

  @both
  Scenario: Avoiding both hands
    Given A game with 1 right hand and 1 left hand
    When There is a hand in -50 position
    Then The player should avoid 2 hands