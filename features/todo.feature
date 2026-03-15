Feature: Todo list management
  As a user
  I want to manage my tasks from the command line
  So that I can track what needs to be done

  Background:
    Given I have an empty todo list

  Scenario: Add a new task
    When I add a task "Buy groceries"
    Then the task "Buy groceries" should be in my list
    And the task "Buy groceries" should be pending

  Scenario: Add multiple tasks
    When I add a task "Task one"
    And I add a task "Task two"
    Then my todo list should have 2 tasks

  Scenario: List tasks shows numbered output
    When I add a task "Go jogging"
    And I list my todos
    Then the output should contain "1."
    And the output should contain "Go jogging"

  Scenario: List an empty todo list
    When I list my todos
    Then the output should contain "No todos yet"

  Scenario: Complete a task
    Given I have a task "Write report"
    When I complete task number 1
    Then the task "Write report" should be done

  Scenario: Complete a task shows confirmation
    Given I have a task "Call dentist"
    When I complete task number 1
    Then the output should contain "Completed: Call dentist"

  Scenario: Complete with an invalid index
    Given I have a task "Some task"
    When I complete task number 99
    Then the output should contain "Invalid index"

  Scenario: Delete a task
    Given I have a task "Old reminder"
    When I delete task number 1
    Then my todo list should have 0 tasks

  Scenario: Delete a task shows confirmation
    Given I have a task "Buy coffee"
    When I delete task number 1
    Then the output should contain "Deleted: Buy coffee"

  Scenario: Delete with an invalid index
    Given I have a task "Some task"
    When I delete task number 99
    Then the output should contain "Invalid index"

  Scenario: Deleted task does not affect others
    Given I have a task "Keep this"
    And I have a task "Remove this"
    When I delete task number 2
    Then the task "Keep this" should be in my list
    And my todo list should have 1 tasks
