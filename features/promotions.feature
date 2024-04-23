Feature: The promotions service back-end
    As an e-commerce platform Owner
    I need a RESTful service for Promotions
    So that I can keep manage all the promotions

Background:
    Given the following promotions
        | name           | start_date | duration  | promotion_type      | rule   | product_id | status |
        | April Sale     | 2024-04-17 |      5    | AMOUNT_DISCOUNT     | 5$ off |   990      |  true  |
        | Happy New Year | 2023-12-25 |      15   | BXGY                | B1G1   |   1234     |  false |
        | Weekend Sale   | 2024-02-20 |      2    | PERCENTAGE_DISCOUNT | 10% off|   5678     |  false |
        | March Sale     | 2024-03-01 |      30   | PERCENTAGE_DISCOUNT | 5% off |   990      |  false |

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

Scenario: List all promotions
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "April Sale" in the results
    And I should see "Happy New Year" in the results
    And I should see "Weekend Sale" in the results
    And I should see "March Sale" in the results
    And I should not see "Merry Christmas" in the results

Scenario: Search for promotions of type percentage discount
    When I visit the "Home Page"
    And I select "Percentage Discount" in the "Type" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Weekend Sale" in the results
    And I should see "March Sale" in the results
    And I should not see "April Sale" in the results
    And I should not see "Happy New Year" in the results

Scenario: Search for promotions by product ID
    When I visit the "Home Page"
    And I set the "Product ID" to "990"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "March Sale" in the results
    And I should see "April Sale" in the results
    And I should not see "Weekend Sale" in the results
    And I should not see "Happy New Year" in the results

Scenario: Search for promotions by start date
    When I visit the "Home Page"
    And I set the "Start Date" to "02-20-2024"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Weekend Sale" in the results
    And I should not see "April Sale" in the results
    And I should not see "March Sale" in the results
    And I should not see "Happy New Year" in the results

Scenario: Search for promotions by status
    When I visit the "Home Page"
    And I select "true" in the "Status" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should not see "March Sale" in the results
    And I should see "April Sale" in the results
    And I should not see "Weekend Sale" in the results
    And I should not see "Happy New Year" in the results
    When I press the "Clear" button
    And I select "false" in the "Status" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "March Sale" in the results
    And I should not see "April Sale" in the results
    And I should see "Weekend Sale" in the results
    And I should see "Happy New Year" in the results

Scenario: Update a promotion
    When I visit the "Home Page"
    And I set the "Name" to "April Sale"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "April Sale" in the "Name" field
    And I should see "Amount Discount" in the "Type" dropdown
    And I should see "true" in the "Status" dropdown
    When I change "Rule" to "10$ off" 
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "10$ off" in the "Rule" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "10$ off" in the results
    And I should not see "5$ off" in the results

Scenario: Dectivate a promotion
    When I visit the "Home Page"
    And I set the "Name" to "April Sale"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Deactivate" button
    Then I should see the message "Promotion has been Deactivated!"
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "false" in the "Status" dropdown

Scenario: Activate a promotion
    When I visit the "Home Page"
    And I set the "Name" to "April Sale"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Deactivate" button
    Then I should see the message "Promotion has been Deactivated!"
    When I paste the "Id" field
    And I press the "Activate" button
    Then I should see the message "Promotion has been Activated!"
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "true" in the "Status" dropdown

Scenario: Delete a promotion
    When I visit the "Home Page"
    And I set the "Name" to "April Sale"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "April Sale" in the "Name" field
    And I should see "2024-04-17" in the "Start Date" field
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Start Date" field should be empty
    When I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Promotion has been Deleted!"
    When I press the "Clear" button 
    # And I paste the "Id" field
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Weekend Sale" in the results
    And I should see "Happy New Year" in the results
    And I should see "March Sale" in the results
    And I should not see "April Sale" in the results

Scenario: Retrieve a promotion
    When I visit the "Home Page"
    And I set the "Name" to "April Sale"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "April Sale" in the "Name" field
    And I should see "2024-04-17" in the "Start Date" field
    When I copy the "Id" field
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"    
    And I should see "April Sale" in the results
