Feature: The promotions service back-end
    As an e-commerce platform Owner
    I need a RESTful service for Promotions
    So that I can keep manage all the promotions

Background:
    Given the following promotions
        | name           | start_date | duration  | promotion_type   | rule   | product_id | status |
        | April Sale     | 2024-04-17 |      5    | AMOUNT_DISCOUNT  | 5$ off |   990      |  true  |
        | Happy New Year | 2023-12-25 |      15   | BXGY             | B1G1   |   1234     |  false |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Promotions REST API Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Promotion
    When I visit the "Home Page"
    And I set the "Name" to "Merry Christmas"
    And I select "Percentage Discount" in the "Type" dropdown
    And I set the "Product ID" to "350"
    And I set the "Start Date" to "12-20-2023"
    And I set the "Duration" to "15"
    And I set the "Rule" to "30% off"
    And I select "false" in the "Status" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "ID" field
    And I press the "Clear" button
    Then the "ID" field should be empty
    And the "Name" field should be empty
    And the "Type" field should be empty
    And the "Product ID" field should be empty
    And the "Start Date" field should be empty
     And the "Duration" field should be empty
    And the "Rule" field should be empty
    And the "Status" field should be empty
    When I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Merry Christmas" in the "Name" field
    And I should see "Percentage Discount" in the "Type" dropdown
    And I should see "350" in the "Product ID" field
    And I should see "2023-12-20" in the "Start Date" field
    And I should see "15" in the "Duration" field
    And I should see "30% off" in the "Rule" field
    And I should see "false" in the "Status" dropdown