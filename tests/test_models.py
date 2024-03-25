"""
Test cases for Promotion Model
"""

import os
import logging
from unittest import TestCase
from unittest.mock import patch
from datetime import date
from wsgi import app
from service.models import Promotion, PromotionType, DataValidationError, db
from tests.factories import PromotionFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  B A S E   T E S T   C A S E S
######################################################################
class TestCaseBase(TestCase):
    """Base Test Case for common setup"""

    # pylint: disable=duplicate-code
    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Promotion).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()


######################################################################
#  P R O M O T I O N   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestPromotionModel(TestCaseBase):
    """Test Cases for Promotion Model"""

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_promotion(self):
        """It should Create a promotion and assert that it exists"""
        promotion = Promotion(
            name="Happy_New_Year",
            start_date=date.fromisoformat("2023-12-29"),
            duration=5,
            promotion_type=PromotionType.PERCENTAGE_DISCOUNT,
            rule="30'%'discount",
            product_id=1,
        )
        self.assertEqual(str(promotion), "<Promotion Happy_New_Year id=[None]>")
        self.assertTrue(promotion is not None)
        self.assertEqual(promotion.id, None)
        self.assertEqual(promotion.start_date, date.fromisoformat("2023-12-29"))
        self.assertEqual(promotion.duration, 5)
        self.assertEqual(promotion.promotion_type, PromotionType.PERCENTAGE_DISCOUNT)
        self.assertEqual(promotion.rule, "30'%'discount")
        self.assertEqual(promotion.product_id, 1)

    def test_add_a_promotion(self):
        """It should Create a promotion and add it to the database"""
        promotions = Promotion.all()
        self.assertEqual(promotions, [])
        promotion = Promotion(
            name="Happy_New_Year",
            start_date=date.fromisoformat("2023-12-29"),
            duration=5,
            promotion_type=PromotionType.PERCENTAGE_DISCOUNT,
            rule="30'$'off",
            product_id=1,
        )
        self.assertTrue(promotion is not None)
        self.assertEqual(promotion.id, None)
        promotion.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(promotion.id)
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 1)

    def test_read_a_promotion(self):
        """It should Read a Promotion"""
        promotion = PromotionFactory()
        logging.debug(promotion)
        promotion.id = None
        promotion.create()
        self.assertIsNotNone(promotion.id)
        # Fetch it back
        found_promotion = promotion.find(promotion.id)
        self.assertEqual(found_promotion.id, promotion.id)
        self.assertEqual(found_promotion.name, promotion.name)
        self.assertEqual(found_promotion.start_date, promotion.start_date)
        self.assertEqual(found_promotion.duration, promotion.duration)
        self.assertEqual(found_promotion.rule, promotion.rule)
        self.assertEqual(found_promotion.product_id, promotion.product_id)

    def test_update_a_promotion(self):
        """It should Update a Promotion"""
        promotion = PromotionFactory()
        logging.debug(promotion)
        promotion.id = None
        promotion.create()
        logging.debug(promotion)
        self.assertIsNotNone(promotion.id)
        # Change it an save it
        promotion.product_id = 2
        original_id = promotion.id
        promotion.update()
        self.assertEqual(promotion.id, original_id)
        self.assertEqual(promotion.product_id, 2)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 1)
        self.assertEqual(promotions[0].id, original_id)
        self.assertEqual(promotions[0].product_id, 2)

    def test_update_no_id(self):
        """It should not Update a Promotion with no id"""
        promotion = PromotionFactory()
        logging.debug(promotion)
        promotion.id = None
        self.assertRaises(DataValidationError, promotion.update)

    def test_delete_a_promotion(self):
        """It should Delete a Promotion"""
        promotion = PromotionFactory()
        promotion.create()
        self.assertEqual(len(Promotion.all()), 1)
        # delete the promotion and make sure it isn't in the database
        promotion.delete()
        self.assertEqual(len(Promotion.all()), 0)

    def test_list_all_promotions(self):
        """It should List all Promotions in the database"""
        promotions = Promotion.all()
        self.assertEqual(promotions, [])
        # Create 5 Promotions
        for _ in range(5):
            promotion = PromotionFactory()
            promotion.create()
        # See if we get back 5 promotions
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 5)

    def test_serialize_a_promotion(self):
        """It should serialize a Promotion"""
        promotion = PromotionFactory()
        data = promotion.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], promotion.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], promotion.name)
        self.assertIn("start_date", data)
        self.assertEqual(date.fromisoformat(data["start_date"]), promotion.start_date)
        self.assertIn("duration", data)
        self.assertEqual(data["duration"], promotion.duration)
        self.assertIn("promotion_type", data)
        self.assertEqual(data["promotion_type"], promotion.promotion_type.name)
        self.assertIn("rule", data)
        self.assertEqual(data["rule"], promotion.rule)
        self.assertIn("product_id", data)
        self.assertEqual(data["product_id"], promotion.product_id)

    def test_deserialize_a_promotion(self):
        """It should de-serialize a Promotion"""
        data = PromotionFactory().serialize()
        promotion = Promotion()
        promotion.deserialize(data)
        self.assertNotEqual(promotion, None)
        self.assertEqual(promotion.id, None)
        self.assertEqual(promotion.name, data["name"])
        self.assertEqual(promotion.start_date, date.fromisoformat(data["start_date"]))
        self.assertEqual(promotion.promotion_type.name, data["promotion_type"])
        self.assertEqual(promotion.rule, data["rule"])
        self.assertEqual(promotion.duration, data["duration"])
        self.assertEqual(promotion.product_id, data["product_id"])

    def test_deserialize_missing_data(self):
        """It should not deserialize a Promotion with missing data"""
        data = {"id": 1, "name": "Kitty"}
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_bad_duration(self):
        """It should not deserialize a bad duration attribute"""
        test_promotion = PromotionFactory()
        data = test_promotion.serialize()
        data["duration"] = "2"
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_bad_product_id(self):
        """It should not deserialize a bad product_id attribute"""
        test_promotion = PromotionFactory()
        data = test_promotion.serialize()
        data["product_id"] = "abc"  # wrong case
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_bad_promotion_type(self):
        """It should not deserialize a bad promotion_type attribute"""
        test_promotion = PromotionFactory()
        data = test_promotion.serialize()
        data["promotion_type"] = "unknown"  # wrong case
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)


######################################################################
#  T E S T   E X C E P T I O N   H A N D L E R S
######################################################################
class TestExceptionHandlers(TestCaseBase):
    """Promotion Model Exception Handlers"""

    @patch("service.models.db.session.commit")
    def test_create_exception(self, exception_mock):
        """It should catch a create exception"""
        exception_mock.side_effect = Exception()
        promotion = PromotionFactory()
        self.assertRaises(DataValidationError, promotion.create)

    @patch("service.models.db.session.commit")
    def test_update_exception(self, exception_mock):
        """It should catch a update exception"""
        exception_mock.side_effect = Exception()
        promotion = PromotionFactory()
        self.assertRaises(DataValidationError, promotion.update)

    @patch("service.models.db.session.commit")
    def test_delete_exception(self, exception_mock):
        """It should catch a delete exception"""
        exception_mock.side_effect = Exception()
        promotion = PromotionFactory()
        self.assertRaises(DataValidationError, promotion.delete)


######################################################################
#  Q U E R Y   T E S T   C A S E S
######################################################################
class TestModelQueries(TestCaseBase):
    """Promotion Model Query Tests"""

    def test_find_promotion(self):
        """It should Find a Promotion by ID"""
        promotions = PromotionFactory.create_batch(5)
        for promotion in promotions:
            promotion.create()
        logging.debug(promotions)
        # make sure they got saved
        self.assertEqual(len(Promotion.all()), 5)
        # find the 2nd promotion in the list
        promotion = Promotion.find(promotions[1].id)
        self.assertIsNot(promotion, None)
        self.assertEqual(promotion.id, promotions[1].id)
        self.assertEqual(promotion.name, promotions[1].name)
        self.assertEqual(promotion.start_date, promotions[1].start_date)
        self.assertEqual(promotion.duration, promotions[1].duration)
        self.assertEqual(promotion.promotion_type, promotions[1].promotion_type)
        self.assertEqual(promotion.rule, promotions[1].rule)
        self.assertEqual(promotion.product_id, promotions[1].product_id)

    def test_find_by_name(self):
        """It should Find a Promotion by Name"""
        promotions = PromotionFactory.create_batch(10)
        for promotion in promotions:
            promotion.create()
        name = promotions[0].name
        count = len([promotion for promotion in promotions if promotion.name == name])
        found = Promotion.find_by_name(name)
        self.assertEqual(found.count(), count)
        for promotion in found:
            self.assertEqual(promotion.name, name)

    def test_find_by_promotion_type(self):
        """It should Find Promotions by Gender"""
        promotions = PromotionFactory.create_batch(10)
        for promotion in promotions:
            promotion.create()
        promotion_type = promotions[0].promotion_type
        count = len(
            [
                promotion
                for promotion in promotions
                if promotion.promotion_type == promotion_type
            ]
        )
        found = Promotion.find_by_promotion_type(promotion_type)
        self.assertEqual(found.count(), count)
        for promotion in found:
            self.assertEqual(promotion.promotion_type, promotion_type)
