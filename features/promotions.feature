Feature: The promotions service back-end
    As an e-commerce platform Owner
    I need a RESTful service for Promotions
    So that I can keep manage all the promotions

Background:
    Given the following promotions
        | name           | start_date | duration  | promotion_type   | rule   | product_id | status |
        | April Sale     | 2024-04-17 |      5    | AMOUNT_DISCOUNT  | 5$ off |   990      |  True  |
        | Happy New Year | 2023-12-25 |      15   | BXGY             | B1G1   |   1234     |  False |

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
    And I select "False" in the "Status" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Promotion ID" field
    And I press the "Clear" button
    Then the "Promotion ID" field should be empty
    And the "Promotion Name" field should be empty
    And the "Promotion Type" field should be empty
    And the "Product ID" field should be empty
    And the "Start Date" field should be empty
     And the "Promotion Duration" field should be empty
    And the "Promotion Rule" field should be empty
    And the "Status" field should be empty
    When I paste the "Promotion ID" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Merry Christmas" in the "Promotion Name" field
    And I should see "Percentage Discount" in the "Promotion Type" field
    And I should see "350" in the "Product ID" dropdown
    And I should see "12-20-2023" in the "Start Date" dropdown
    And I should see "15" in the "Promotion Duration" field
    And I should see "30% off" in the "Promotion Rule" field
    And I should see "False" in the "Status" field