Feature: Testing the rotation

  @basic
  Scenario: To eat a coin
    Given A game with a ball
    And A coin
    When There is on coin
    Then The ball should have 1 point
