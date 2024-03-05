"""
TestPromotion API Service Test Suite
"""

import os
import logging
from unittest import TestCase
from datetime import date
from wsgi import app
from service.common import status
from service.models import db, Promotion
from .factories import PromotionFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/promotions"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestPromotionService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Promotion).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_promotion(self):
        """It should Create a new Promotion"""
        test_promotion = PromotionFactory()
        logging.debug("Test Promotion: %s", test_promotion.serialize())
        response = self.client.post(BASE_URL, json=test_promotion.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_promotion = response.get_json()
        self.assertEqual(new_promotion["name"], test_promotion.name)
        self.assertEqual(
            date.fromisoformat(new_promotion["start_date"]), test_promotion.start_date
        )
        self.assertEqual(new_promotion["duration"], test_promotion.duration)
        self.assertEqual(new_promotion["rule"], test_promotion.rule)
        self.assertEqual(new_promotion["product_id"], test_promotion.product_id)

        # Todo: Uncomment this code when get_promotions is implemented
        # Check that the location header was correct
        # response = self.client.get(location)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # new_promotion = response.get_json()
        # self.assertEqual(new_promotion["name"], test_promotion.name)
        # self.assertEqual(date.fromisoformat(new_promotion["start_date"]), test_promotion.start_date)
        # self.assertEqual(new_promotion["duration"], test_promotion.duration)
        # self.assertEqual(new_promotion["rule"], test_promotion.rule)
        # self.assertEqual(new_promotion["product_id"], test_promotion.product_id)


    def test_list_promotion(self): #maybe we dont need an input for the call
        """It should list all Promotions"""
        self._create_promotions(2)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        promotions = response.get_json()
        self.assertEqual(len(promotions), 2) 


######################################################################
#  HELPER FUNCTION
######################################################################
    def _create_promotions(self, size):
        """Factory method to create promotions in bulk"""
        promotions = []
        for _ in range(size):
            promotion = PromotionFactory()
            resp = self.client.post(BASE_URL, json=promotion.serialize())
            self.assertEqual(
                resp.status_code,
                status.HTTP_201_CREATED,
                "Could not create test promotion"
            )
            new_promotion = resp.get_json()
            promotion.id = new_promotion["id"]
            promotions.append(promotion)

        return promotions