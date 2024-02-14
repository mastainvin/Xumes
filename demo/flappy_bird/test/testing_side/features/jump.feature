Feature: jumping

  Scenario: Middle and bottom
    Given A game with a player
    And A pipe generator
    When The first pipe is at 50 % and the next pipe is at 100 %
    Then The player should have passed 2 pipes
