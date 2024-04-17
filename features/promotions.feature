Feature: The promotions service back-end
    As an e-commerce platform Owner
    I need a RESTful service for Promotions
    So that I can keep manage all the promotions

Background:
    Given the following promotions
        | id  | name         | start_date | duration | promotion_type   | rule   | product_id | status
        | 1   | Promotion-1  | 2024-04-17 |      5    | AMOUNT_DISCOUNT | 5$ off |   990      |  True
        