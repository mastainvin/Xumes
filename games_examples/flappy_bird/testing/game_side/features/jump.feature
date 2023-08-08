Feature: Testing the jump

  @basic
  @one
  Scenario: Middle and middle
    Given A game with a player
    And A pipe generator
    When The first pipe is at 50 % and the next pipe is at 50 %
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipes

  @basic
  Scenario: Middle and bottom
    Given A game with a player
    And A pipe generator
    When The first pipe is at 50 % and the next pipe is at 100 %
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipes

  @basic
  Scenario: Bottom and middle
    Given A game with a player
    And A pipe generator
    When The first pipe is at 100 % and the next pipe is at 50 %
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipes

  @basic
  Scenario: Middle and top
    Given A game with a player
    And A pipe generator
    When The first pipe is at 50 % and the next pipe is at 0 %
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipes

  @basic
  Scenario: Top and middle
    Given A game with a player
    And A pipe generator
    When The first pipe is at 0 % and the next pipe is at 50 %
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipes

  @critic
  Scenario: Bottom and top
    Given A game with a player
    And A pipe generator
    When The first pipe is at 100 % and the next pipe is at 0 %
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipes

  @critic
  Scenario: Top and bottom
    Given A game with a player
    And A pipe generator
    When The first pipe is at 0 % and the next pipe is at 100 %
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipes