Feature: Testing killing ennemies

  @basic
  Scenario: Kill 1 Goomba
    Given A game with a player against 1 ennemies
    When There is 1 Goomba and 0 Koopa
    Then The player should have killed 1 ennemies
    #And The player should have killed at least 1 ennemies

  @basic
  Scenario: Kill 1 Koopa
    Given A game with a player against 1 ennemies
    When There is 0 Goomba and 1 Koopa
    Then The player should have killed 1 ennemies
    #And The player should have killed at least 1 ennemies

#  @complicate
#  Scenario: Kill 2 Goomba
#    Given A game with a player against 2 ennemies
#    When There is 2 Goomba and 0 Koopa
#    Then The player should have killed 2 ennemies
#    And The player should have killed at least 1 ennemies
#
#  @complicate
#  Scenario: Kill 2 Koopa
#    Given A game with a player against 2 ennemies
#    When There is 0 Goomba and 2 Koopa
#    Then The player should have killed 2 ennemies
#    And The player should have killed at least 1 ennemies
#
#  @complicate
#  Scenario: Kill 2 Goomba and 2 Koopa
#    Given A game with a player against 4 ennemies
#    When There is 2 Goomba and 2 Koopa
#    Then The player should have killed 4 ennemies
#    And The player should have killed at least 2 ennemies

