Feature: Testing the jump 2

  Scenario: Top and bottom
    Given A game with a player and a pipe generator
    When The first pipe is at 50 % and the next pipe is at 100 %
    Then The player should have passed two pipes

  Scenario: Bottom and top
    Given A game with a player and a pipe generator
    When The first pipe is at 100 % and the next pipe is at 50 %
    Then The player should have passed two pipes
