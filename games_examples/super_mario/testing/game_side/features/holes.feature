Feature: Testing jumping over hole

  @basic
  Scenario: Jump over 1 hole
    Given A game with a player
    When There is 1 holes
    Then The player should have passed 1 holes at 384

