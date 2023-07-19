

Features
========

We are using the [Gherkin](https://cucumber.io/docs/gherkin/reference/) language to describe the features.

You need to create a `features` directory in the test directory.
And write your features (`.feature` files) in the `features` directory.

The difference with normal using of BDD is about the sense of the keywords : 

- `Given` is used to set up the game.
- `When` is used to set up the testing situation.
- `Then` is used to assert after the agent's play.

Here is an example of a feature file:

```gherkin
Feature: Testing the jump

  Scenario: Top and bottom
    Given A game with a player
    And A pipe generator
    When The first pipe is at 50 % and the next pipe is at 100 %
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipes

  Scenario: Bottom and top
    Given A game with a player
    And A pipe generator
    When The first pipe is at 100 % and the next pipe is at 50 %
    Then The player should have passed 2 pipes
    And The player should have passed at least 1 pipes
```

> **IMPORTANT:** As you can see, the `And` keyword is used to chain the steps. That's means that it has the same function as the keyword just before him.
