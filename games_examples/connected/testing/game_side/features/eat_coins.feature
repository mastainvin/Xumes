Feature: Testing eating a coin

  @basic
  Scenario: Pattern 1
    Given A game with a ball
    And A generator
    When Pattern 1 is used
#    bottom bottom bottom
    Then The ball should have 3 point
    And The ball should have 2 point
    And The ball should have 1 point

    @basic
  Scenario: Pattern 2
    Given A game with a ball
    And A generator
    When Pattern 2 is used
#      bottom bottom top
    Then The ball should have 3 point
    And The ball should have 2 point
    And The ball should have 1 point

    @basic
  Scenario: Pattern 3
    Given A game with a ball
    And A generator
    When Pattern 3 is used
#      top bottom bottom
    Then The ball should have 3 point
    And The ball should have 2 point
    And The ball should have 1 point

    @basic
  Scenario: Pattern 4
    Given A game with a ball
    And A generator
    When Pattern 4 is used
#      top middle bottom
    Then The ball should have 3 point
    And The ball should have 2 point
    And The ball should have 1 point


    @basic
  Scenario: Pattern 5
    Given A game with a ball
    And A generator
    When Pattern 5 is used
#    top bottom middle
    Then The ball should have 3 point
    And The ball should have 2 point
    And The ball should have 1 point

    @basic
  Scenario: Pattern 6
    Given A game with a ball
    And A generator
    When Pattern 6 is used
#      middle middle middle
    Then The ball should have 3 point
    And The ball should have 2 point
    And The ball should have 1 point

    @basic
  Scenario: Pattern 7
    Given A game with a ball
    And A generator
    When Pattern 7 is used
#      middle middle middle
    Then The ball should have 3 point
    And The ball should have 2 point
    And The ball should have 1 point





#      @basic
#  Scenario: To eat a coin
#    Given A game with a ball
#    And A coin
##    And A tile
#    When There is one coin
##    When The player is alive
#    Then The ball should have 1 point