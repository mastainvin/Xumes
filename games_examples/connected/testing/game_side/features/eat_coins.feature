Feature: Testing eating a coin

  @basic
  Scenario: To eat a coin
    Given A game with a ball
    And A generator
    When The first coin is at 50 % and the tile is at 50 % and the second coin is at 50 %
    Then The ball should have 2 point
    And The ball should have at least 1 point




#      @basic
#  Scenario: To eat a coin
#    Given A game with a ball
#    And A coin
##    And A tile
#    When There is one coin
##    When The player is alive
#    Then The ball should have 1 point