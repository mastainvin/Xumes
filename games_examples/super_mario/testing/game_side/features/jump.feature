Feature: Testing the jump

  @basic
  Scenario: Jump 100:100
    Given A game with a player
    When The first pipe is at 100 % and the next pipe is at 100 %
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipes

  @basic
  Scenario: Jump 80:120
    Given A game with a player
    When The first pipe is at 80 % and the next pipe is at 120 %
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipes

  @basic
  Scenario: Jump 80:100
    Given A game with a player
    When The first pipe is at 80 % and the next pipe is at 100 %
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipes

  @critic
  Scenario: Jump 150:100
    Given A game with a player
    When The first pipe is at 150 % and the next pipe is at 100 %
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipes