######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################
# spell: ignore Rofrano jsonify restx dbname
"""
Promotion Store Service with Swagger

Paths:
------
GET / - Displays a UI for Selenium testing
GET /promotions - Returns a list all of the Promotions
GET /promotions/{id} - Returns the Promotion with a given id number
POST /promotions - creates a new Promotion record in the database
PUT /promotions/{id} - updates a Promotion record in the database
DELETE /promotions/{id} - deletes a Promotion record in the database
"""


from flask import jsonify
from flask import current_app as app  # Import Flask application
from flask_restx import Resource, fields, reqparse, inputs
from service.models import Promotion, PromotionType
from service.common import status  # HTTP Status Codes
from . import api  # pylint: disable=cyclic-import


######################################################################
# Configure the Root route before OpenAPI
######################################################################
@app.route("/")
def index():
    """Index page"""
    return app.send_static_file("index.html")


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/health")
def health_check():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


# Define the model so that the docs reflect what can be sent
create_model = api.model(
    "Promotion",
    {
        "name": fields.String(required=True, description="The name of the Promotion"),
        "start_date": fields.Date(
            required=True, description="The start date of the Promotion"
        ),
        "duration": fields.Integer(
            required=True, description="The duration of the Promotion"
        ),
        # pylint: disable=protected-access
        "promotion_type": fields.String(
            enum=PromotionType._member_names_, description="The type of the Promotion"
        ),
        "rule": fields.String(
            required=True,
            description="The rule of Promotion",
        ),
        "product_id": fields.Integer(
            required=True, description="The product ID of the Promotion"
        ),
        "status": fields.Boolean(
            required=True, description="Is the Promotion activated?"
        ),
    },
)

promotion_model = api.inherit(
    "PromotionModel",
    create_model,
    {
        "id": fields.String(
            readOnly=True, description="The unique id assigned internally by service"
        ),
    },
)

# query string arguments
promotion_args = reqparse.RequestParser()
promotion_args.add_argument(
    "name", type=str, location="args", required=False, help="List Promotions by name"
)
promotion_args.add_argument(
    "start_date",
    type=str,
    location="args",
    required=False,
    help="List Promotions by start date",
)
promotion_args.add_argument(
    "promotion_type",
    type=str,
    location="args",
    required=False,
    help="List Promotions by type",
)
promotion_args.add_argument(
    "product_id",
    type=int,
    location="args",
    required=False,
    help="List Promotions by product ID",
)
promotion_args.add_argument(
    "status",
    type=inputs.boolean,
    location="args",
    required=False,
    help="List Promotions by status",
)


######################################################################
#  PATH: /promotions/{id}
######################################################################
@api.route("/promotions/<promotion_id>")
@api.param("promotion_id", "The Promotion identifier")
class PromotionResource(Resource):
    """
    PromotionResource class

    Allows the manipulation of a single Promotion
    GET /promotion{id} - Returns a Promotion with the id
    PUT /promotion{id} - Update a Promotion with the id
    DELETE /promotion{id} -  Deletes a Promotion with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A PROMOTION
    # ------------------------------------------------------------------
    @api.doc("get_promotions")
    @api.response(404, "Promotion not found")
    @api.marshal_with(promotion_model)
    def get(self, promotion_id):
        """
        Retrieve a single Promotion

        This endpoint will return a Promotion based on it's id
        """
        app.logger.info("Request to Retrieve a promotion with id [%s]", promotion_id)
        promotion = Promotion.find(promotion_id)
        if not promotion:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Promotion with id '{promotion_id}' was not found.",
            )
        return promotion.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING PROMOTION
    # ------------------------------------------------------------------
    @api.doc("update_promotions", security="apikey")
    @api.response(404, "Promotion not found")
    @api.response(400, "The posted Promotion data was not valid")
    @api.expect(promotion_model)
    @api.marshal_with(promotion_model)
    def put(self, promotion_id):
        """
        Update a Promotion

        This endpoint will update a Promotion based the body that is posted
        """
        app.logger.info("Request to Update a promotion with id [%s]", promotion_id)
        promotion = Promotion.find(promotion_id)
        if not promotion:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Promotion with id '{promotion_id}' was not found.",
            )
        app.logger.debug("Payload = %s", api.payload)
        data = api.payload
        promotion.deserialize(data)
        promotion.id = promotion_id
        promotion.update()
        return promotion.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A PROMOTION
    # ------------------------------------------------------------------
    @api.doc("delete_promotions", security="apikey")
    @api.response(204, "Promotion deleted")
    def delete(self, promotion_id):
        """
        Delete a Promotion

        This endpoint will delete a Promotion based the id specified in the path
        """
        app.logger.info("Request to Delete a promotion with id [%s]", promotion_id)
        promotion = Promotion.find(promotion_id)
        if promotion:
            promotion.delete()
            app.logger.info("Promotion with id [%s] was deleted", promotion_id)

        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /promotions
######################################################################
@api.route("/promotions", strict_slashes=False)
class PromotionCollection(Resource):
    """Handles all interactions with collections of Promotions"""

    # ------------------------------------------------------------------
    # LIST ALL PROMOTIONS
    # ------------------------------------------------------------------
    @api.doc("list_promotions")
    @api.expect(promotion_args, validate=True)
    @api.marshal_list_with(promotion_model)
    def get(self):
        """Returns all of the Promotions"""
        app.logger.info("Request to list Promotions...")
        promotions = []
        args = promotion_args.parse_args()
        if args["name"]:
            app.logger.info("Filtering by name: %s", args["name"])
            promotions = Promotion.find_by_name(args["name"])
        elif args["start_date"]:
            app.logger.info("Filtering by start date: %s", args["start_date"])
            promotions = Promotion.find_by_start_date(args["start_date"])
        elif args["promotion_type"]:
            app.logger.info("Filtering by type: %s", args["promotion_type"])
            promotion_type = PromotionType[args["promotion_type"].upper()]
            promotions = Promotion.find_by_promotion_type(promotion_type)
        elif args["product_id"]:
            app.logger.info("Filtering by product ID: %s", args["product_id"])
            promotions = Promotion.find_by_product_id(args["product_id"])
        elif args["status"] is not None:
            app.logger.info("Filtering by status: %s", args["status"])
            promotions = Promotion.find_by_promotion_status(args["status"])
        else:
            app.logger.info("Returning unfiltered list.")
            promotions = Promotion.all()

        results = [promotion.serialize() for promotion in promotions]
        app.logger.info("[%s] Promotions returned", len(results))
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW PROMOTION
    # ------------------------------------------------------------------
    @api.doc("create_promotions", security="apikey")
    @api.response(400, "The posted data was not valid")
    @api.expect(create_model)
    @api.marshal_with(promotion_model, code=201)
    def post(self):
        """
        Creates a Promotion
        This endpoint will create a Promotion based the data in the body that is posted
        """
        app.logger.info("Request to Create a Promotion")
        promotion = Promotion()
        app.logger.debug("Payload = %s", api.payload)
        promotion.deserialize(api.payload)
        promotion.create()
        app.logger.info("Promotion with new id [%s] created!", promotion.id)
        location_url = api.url_for(
            PromotionResource, promotion_id=promotion.id, _external=True
        )
        return (
            promotion.serialize(),
            status.HTTP_201_CREATED,
            {"Location": location_url},
        )


######################################################################
#  PATH: /promotions/{id}/activate
######################################################################
@api.route("/promotions/<promotion_id>/activate")
@api.param("promotion_id", "The Promotion identifier")
class ActivateResource(Resource):
    """Activate actions on a Promotion"""

    @api.doc("activate_promotions")
    @api.response(404, "Promotion not found")
    @api.response(409, "The Promotion is already activated")
    def put(self, promotion_id):
        """
        Activate a Promotion

        This endpoint will activate a Promotion and make it in effect
        """
        app.logger.info("Request to Activate a Promotion")
        promotion = Promotion.find(promotion_id)
        if not promotion:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Promotion with id [{promotion_id}] was not found.",
            )
        # if promotion.status:
        #     abort(
        #         status.HTTP_409_CONFLICT,
        #         f"Promotion with id [{promotion_id}] is already activated.",
        #     )
        promotion.status = True
        promotion.update()
        app.logger.info("Promotion with id [%s] has been activated!", promotion.id)
        return promotion.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /promotions/{id}/deactivate
######################################################################
@api.route("/promotions/<promotion_id>/deactivate")
@api.param("promotion_id", "The Promotion identifier")
class DeactivateResource(Resource):
    """Deactivate actions on a Promotion"""

    @api.doc("deactivate_promotions")
    @api.response(404, "Promotion not found")
    @api.response(409, "The Promotion is already deactivated")
    def put(self, promotion_id):
        """
        Deactivate a Promotion

        This endpoint will deactivate a Promotion
        """
        app.logger.info("Request to Deactivate a Promotion")
        promotion = Promotion.find(promotion_id)
        if not promotion:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Promotion with id [{promotion_id}] was not found.",
            )
        # if not promotion.status:
        #     abort(
        #         status.HTTP_409_CONFLICT,
        #         f"Promotion with id [{promotion_id}] is already deactivated.",
        #     )
        promotion.status = False
        promotion.update()
        app.logger.info("Promotion with id [%s] has been deactivated!", promotion.id)
        return promotion.serialize(), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)
