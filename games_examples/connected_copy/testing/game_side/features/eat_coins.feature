Feature: Testing eating a coin

  @basic
  Scenario: To eat a coin
    Given A game with a ball, a coin and a tile
    When The player is alive
#    When The player is alive
    Then The ball should have 1 point

#      @basic
#  Scenario: To eat a coin
#    Given A game with a ball
#    And A coin
##    And A tile
#    When There is one coin
##    When The player is alive
#    Then The ball should have 1 point