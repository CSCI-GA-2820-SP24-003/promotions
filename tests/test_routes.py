"""
TestPromotion API Service Test Suite
"""

import os
import logging
from unittest import TestCase
from datetime import date
from urllib.parse import quote_plus
from wsgi import app
from service.common import status
from service.models import db, Promotion, PromotionType
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

    def _create_promotions(self, count):
        """Factory method to create promotions in bulk"""
        promotions = []
        for _ in range(count):
            test_promotion = PromotionFactory()
            response = self.client.post(BASE_URL, json=test_promotion.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test promotion",
            )
            new_promotion = response.get_json()
            test_promotion.id = new_promotion["id"]
            promotions.append(test_promotion)
        return promotions

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], 200)
        self.assertEqual(data["message"], "Healthy")

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
        self.assertEqual(
            new_promotion["promotion_type"], test_promotion.promotion_type.name
        )
        self.assertEqual(new_promotion["rule"], test_promotion.rule)
        self.assertEqual(new_promotion["product_id"], test_promotion.product_id)
        self.assertEqual(new_promotion["status"], test_promotion.status)

        # Check that the location header was correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_promotion = response.get_json()
        self.assertEqual(new_promotion["name"], test_promotion.name)
        self.assertEqual(
            date.fromisoformat(new_promotion["start_date"]), test_promotion.start_date
        )
        self.assertEqual(new_promotion["duration"], test_promotion.duration)
        self.assertEqual(
            new_promotion["promotion_type"], test_promotion.promotion_type.name
        )
        self.assertEqual(new_promotion["rule"], test_promotion.rule)
        self.assertEqual(new_promotion["product_id"], test_promotion.product_id)
        self.assertEqual(new_promotion["status"], test_promotion.status)

    def test_get_promotion(self):
        """It should Get a single Promotion"""
        # get the id of a promotion
        test_promotion = self._create_promotions(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_promotion.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_promotion.name)

    def test_delete_promotion(self):
        """This should delete a single Promotion"""
        # get the id of a promotion
        test_db = self._create_promotions(5)
        test_promotion_id = test_db[0].id
        response = self.client.delete(f"{BASE_URL}/{test_promotion_id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_promotion(self):  # maybe we dont need an input for the call
        """It should list all Promotions"""
        self._create_promotions(2)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        promotions = response.get_json()
        self.assertEqual(len(promotions), 2)

    def test_list_promotions_by_product_id(self):
        """This should list all promotions with given product id"""
        test_db = self._create_promotions(5)
        test_product = test_db[0].product_id
        count = 0
        for item in test_db:
            if item.product_id == test_product:
                count = count + 1
        response = self.client.get(f"{BASE_URL}?product_id={test_product}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        promotions = response.get_json()
        self.assertEqual(len(promotions), count)

    def test_list_promotions_by_promotion_type(self):
        """This should list all promotions with given type"""
        test_db = self._create_promotions(5)
        test_type = test_db[0].promotion_type.name
        count = 0
        for item in test_db:
            if item.promotion_type.name == test_type:
                count = count + 1
        response = self.client.get(f"{BASE_URL}?promotion_type={test_type}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        promotions = response.get_json()
        self.assertEqual(len(promotions), count)

    def test_list_promotions_by_start_date(self):
        """This should list all promotions with given start date"""
        test_db = self._create_promotions(5)
        test_date = test_db[0].start_date
        count = 0
        for item in test_db:
            if item.start_date == test_date:
                count = count + 1
        response = self.client.get(f"{BASE_URL}?start_date={test_date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        promotions = response.get_json()
        self.assertEqual(len(promotions), count)

    def test_get_promotion_not_found(self):
        """It should not Get a Promotion thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    def test_update_promotion(self):
        """It should Update an existing Promotion"""
        # create a promotion to update
        test_promotion = PromotionFactory()
        response = self.client.post(BASE_URL, json=test_promotion.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the promotion
        new_promotion = response.get_json()
        logging.debug(new_promotion)
        new_promotion["rule"] = "unknown"
        response = self.client.put(
            f"{BASE_URL}/{new_promotion['id']}", json=new_promotion
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_promotion = response.get_json()
        self.assertEqual(updated_promotion["rule"], "unknown")

    # ----------------------------------------------------------
    # TEST QUERY
    # ----------------------------------------------------------
    def test_query_by_name(self):
        """It should Query Promotions by name"""
        promotions = self._create_promotions(5)
        test_name = promotions[0].name
        name_count = len(
            [promotion for promotion in promotions if promotion.name == test_name]
        )
        response = self.client.get(
            BASE_URL, query_string=f"name={quote_plus(test_name)}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), name_count)
        # check the data just to be sure
        for promotion in data:
            self.assertEqual(promotion["name"], test_name)

    def test_query_by_product_id(self):
        """It should Query Promotions by product_id"""
        promotions = self._create_promotions(5)
        test_product_id = promotions[0].product_id
        product_id_count = len(
            [
                promotion
                for promotion in promotions
                if promotion.product_id == test_product_id
            ]
        )
        response = self.client.get(
            BASE_URL, query_string=f"product_id={test_product_id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), product_id_count)
        # check the data just to be sure
        for promotion in data:
            self.assertEqual(promotion["product_id"], test_product_id)

    def test_query_by_start_date(self):
        """It should Query Promotions by start_date"""
        promotions = self._create_promotions(5)
        test_start_date = promotions[0].start_date
        start_date_count = len(
            [
                promotion
                for promotion in promotions
                if promotion.start_date == test_start_date
            ]
        )
        response = self.client.get(
            BASE_URL, query_string=f"start_date={test_start_date}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), start_date_count)
        # check the data just to be sure
        for promotion in data:
            self.assertEqual(promotion["start_date"], test_start_date.isoformat())

    def test_query_by_promotion_type(self):
        """It should Query Promotions by promotion_type"""
        promotions = self._create_promotions(10)
        bxgy_promotions = [
            promotion
            for promotion in promotions
            if promotion.promotion_type == PromotionType.BXGY
        ]
        bxgy_count = len(bxgy_promotions)
        logging.debug("Female Promotions [%d] %s", bxgy_count, bxgy_promotions)

        # test for activated
        response = self.client.get(BASE_URL, query_string="promotion_type=BXGY")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), bxgy_count)
        # check the data just to be sure
        for promotion in data:
            self.assertEqual(promotion["promotion_type"], PromotionType.BXGY.name)

    def test_query_by_promotion_status(self):
        """It should Query Promotions by promotion status"""
        promotions = self._create_promotions(10)
        activated_promotions = [
            promotion for promotion in promotions if promotion.status is True
        ]
        deactivated_promotions = [
            promotion for promotion in promotions if promotion.status is False
        ]
        activated_count = len(activated_promotions)
        deactivated_count = len(deactivated_promotions)
        logging.debug(
            "Activated Promotions [%d] %s", activated_count, activated_promotions
        )
        logging.debug(
            "Deacticated Promotions [%d] %s", deactivated_count, deactivated_promotions
        )

        # test for activated
        response = self.client.get(BASE_URL, query_string="status=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), activated_count)
        # check the data just to be sure
        for promotion in data:
            self.assertEqual(promotion["status"], True)

        # test for deactivated
        response = self.client.get(BASE_URL, query_string="status=false")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), deactivated_count)
        # check the data just to be sure
        for promotion in data:
            self.assertEqual(promotion["status"], False)

    # ----------------------------------------------------------
    # TEST ACTIONS
    # ----------------------------------------------------------
    def test_activate_promotion(self):
        """It should Activate an existing Promotion"""
        test_promotion = PromotionFactory()
        response = self.client.post(BASE_URL, json=test_promotion.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Activate the promotion
        new_promotion = response.get_json()
        logging.debug(new_promotion)
        new_promotion["status"] = False
        promotion_id = new_promotion["id"]
        response = self.client.put(f"{BASE_URL}/{promotion_id}/activate")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        activated_promotion = response.get_json()
        self.assertEqual(activated_promotion["status"], True)

    def test_deactivate_promotion(self):
        """It should Deactivate an existing Promotion"""
        test_promotion = PromotionFactory()
        response = self.client.post(BASE_URL, json=test_promotion.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Deactivate the promotion
        new_promotion = response.get_json()
        logging.debug(new_promotion)
        new_promotion["status"] = True
        promotion_id = new_promotion["id"]
        response = self.client.put(f"{BASE_URL}/{promotion_id}/deactivate")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        deactivated_promotion = response.get_json()
        self.assertEqual(deactivated_promotion["status"], False)

    def test_activate_promotion_not_found(self):
        """It should not Activate a Promotion thats not found"""
        response = self.client.put(f"{BASE_URL}/0/activate")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    def test_deactivate_promotion_not_found(self):
        """It should not Deactivate a Promotion thats not found"""
        response = self.client.put(f"{BASE_URL}/0/deactivate")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    def test_update_promotion_not_found(self):
        """It should not update a Promotion thats not found"""
        test_promotion = PromotionFactory()
        response = self.client.post(
            BASE_URL, json=test_promotion.serialize(), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the non-existing Wishlist
        non_existing_promotion = response.get_json()
        non_existing_promotion["name"] = "Trial Promotion"
        new_promotion_id = non_existing_promotion["id"] + 1
        resp = self.client.put(
            f"{BASE_URL}/{new_promotion_id}", json=non_existing_promotion
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


######################################################################
#  T E S T   S A D   P A T H S
######################################################################
class TestSadPaths(TestCase):
    """Test REST Exception Handling"""

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()

    def test_method_not_allowed(self):
        """It should not allow update without a promotion id"""
        response = self.client.put(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_promotion_no_data(self):
        """It should not Create a Promotion with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_promotion_no_content_type(self):
        """It should not Create a Promotion with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_promotion_wrong_content_type(self):
        """It should not Create a Promotion with the wrong content type"""
        response = self.client.post(BASE_URL, data="hello", content_type="text/html")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_promotion_bad_promotion_type(self):
        """It should not Create a Promotion with bad promotion_type data"""
        promotion = PromotionFactory()
        logging.debug(promotion)
        # change promotion_type to a bad string
        test_promotion = promotion.serialize()
        test_promotion["promotion_type"] = "male"  # wrong case
        response = self.client.post(BASE_URL, json=test_promotion)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
