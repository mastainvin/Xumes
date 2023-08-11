Feature: Testing eating a coin

  @basic
  Scenario: To eat a coin
    Given A game with a ball
    And A coin
    And A tile
    When There is one coin
    Then The ball should have 1 point
