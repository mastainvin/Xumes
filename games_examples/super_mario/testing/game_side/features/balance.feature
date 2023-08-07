Feature: Testing balance

  @pipe
  Scenario: Jump over 1 pipe
    Given A game with a player, 1 pipes, 0 goombas and 0 holes
    When There is 1 pipes, 0 goombas and 0 holes
    Then The player should have passed 1 pipes at x 320
    And The player should have killed 0 enemies
    And The player should have passed 0 holes at x 1024

  @enemy
  Scenario: Jump over 1 pipe and kill 1 enemy
    Given A game with a player, 1 pipes, 1 goombas and 0 holes
    When There is 1 pipes, 1 goombas and 0 holes
    Then The player should have passed 1 pipes at x 320
    And The player should have killed 1 enemies
    And The player should have passed 0 holes at x 1024

  @hole
  Scenario: Jump 1 pipe, kill 1 enemy and jump 1 hole
    Given A game with a player, 1 pipes, 1 goombas and 1 holes
    When There is 1 pipes, 1 goombas and 1 holes
    Then The player should have passed 1 pipes at x 320
    And The player should have killed 1 enemies
    And The player should have passed 1 holes at x 1024