Feature: The promotions service back-end
    As an e-commerce platform Owner
    I need a RESTful service for Promotions
    So that I can keep manage all the promotions

Background:
    Given the following promotions
        | id  | name         | start_date | duration | promotion_type   | rule   | product_id | status
        | 1   | Promotion-1  | 2024-04-17 |      5    | AMOUNT_DISCOUNT | 5$ off |   990      |  True
        
Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Promotions REST API Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Promotion
    When I visit the "Home Page"
    And I set the "Name" to "Promotion-1"
    And I select "AMOUNT_DISCOUNT" in the "Promotion Type" dropdown
    And I set the "Product ID" to "990"
    And I set the "Start Date" to "2024-04-17"
    And I set the "Promotion Duration" to "5"
    And I set the "Promotion Rule" to "5$ off"
    And I select "true" in the "Status" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Product ID" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Promotion-1" in the "Name" field
    And I should see "AMOUNT_DISCOUNT" in the "Promotion Type" dropdown
    And I should see "990" in the "Product ID" field
    And I should see "2024-04-17" in the "Start Date" field
    And I should see "5" in the "Promotion Duration" field
    And I should see "5$ off" in the "Promotion Rule" field
    And I should see "true" in the "Status" dropdown
