Feature: Testing the turn

  @eat_passed
  Scenario: To eat a fruit
    Given A game with a snake
    And A fruit
    When There is one fruit
    Then The snake should be longer

  @eat_facing
  Scenario: To eat a fruit 2
    Given A game with a snake
    And A fruit
    When The head of the snake has not passed the fruit
    Then The snake should turn twice and facing the opposite direction compared to its original direction

  @basic
  Scenario: To turn before bump into the wall
    Given A game with a snake
    And A fruit
    When There is one fruit
    Then The snake should be longer

  @itself
  Scenario: To turn before bump into itself
    Given A game with a snake
    And A fruit
    When The head part of the snake is going to intersect its tail part
#  within no more than 4 spaces
#    And Is not heading to a fruit placed before intersection
    Then The snake should turn to the direction of avoiding the nearer one: its body part and the wall
#  sssssssssssssssssssssssssssssssss tail
#                                  s
#               head-----> s       s body
#                          sssssssss
#
#
#  @stretch_critical
#  Scenario: To stretch whenever fruit is going to be enclosed by the snake ( 5 points on the body has the same short(3) distant to the fruit, and in different direction ( both x and y) of the snake)
#    Given A game with a snake
#    And A fruit
#    When The fruit is going to be enclosed by the snake
#    Then The snake should turn to the direction of avoiding its body part
#    And Should not change direction before reach the end of the wall
#    And Change direction immediately for two times
#    And If it is necessary, repeat last step when reaching the length of (width or height-3) or bump into itself
#
#  @stretch_critical
#  Scenario: To stretch whenever the snake is too long and have just eaten a fruit
#    Given A game with a snake
#    And A fruit
#    When The snake is too long
#    And The snake have just eaten a fruit
#    Then The snake should turn to the direction of avoiding its body part
#    And Should not change direction before reach the end of the wall
#    And Change direction immediately for two times
#    And If it is necessary, repeat last step when reaching the length of (width or height-3) or bump into itself
#

