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

"""
Promotion Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Promotions from the inventory of promotions in the PromotionShop
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Promotion, db, PromotionType
from service.common import status  # HTTP Status Codes


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/health")
def health_check():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
# @app.route("/")
# def index():
#     """Root URL response"""
#     data = {
#         "version": "1.0.0",
#         "description": "A RESTful API for managing promotions shown to users! "
#         "Supports create, read, update, delete, and list operations!",
#         "endpoints": [
#             {
#                 "method": "POST",
#                 "url": "/promotions",
#                 "details": "Create a new promotion",
#             },
#             {
#                 "method": "GET",
#                 "url": "/promotions/<int:promotion_id>",
#                 "details": "Read the promotion with id <promotion_id>",
#             },
#             {
#                 "method": "DELETE",
#                 "url": "/promotions/<int:promotion_id>",
#                 "details": "Delete the promotion with id <promotion_id>",
#             },
#             {
#                 "method": "GET",
#                 "url": "/promotions",
#                 "details": "List all the promotions",
#             },
#             {
#                 "method": "PUT",
#                 "url": "/promotions/<int:promotion_id>",
#                 "details": "Update the promotion with id <promotion_id>",
#             },
#         ],
#     }
#     json_response = jsonify(data)
#     return (json_response, status.HTTP_200_OK)


@app.route("/")
def index():
    """Base URL for our service"""
    return app.send_static_file("index.html")


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# CREATE A NEW PROMOTION
######################################################################
@app.route("/promotions", methods=["POST"])
def create_promotions():
    """
    Creates a Promotion

    This endpoint will create a Promotion based the data in the body that is posted
    """
    app.logger.info("Request to create a promotion")
    check_content_type("application/json")

    promotion = Promotion()
    # Get the data from the request and deserialize it
    promotion.deserialize(request.get_json())

    # Save the new Promotion to the database
    promotion.create()
    message = promotion.serialize()

    # Return the location of the new Promotion
    location_url = url_for("get_promotions", promotion_id=promotion.id, _external=True)

    app.logger.info("Promotion with ID: %d created.", promotion.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# READ A PROMOTION
######################################################################
@app.route("/promotions/<int:promotion_id>", methods=["GET"])
def get_promotions(promotion_id):
    """
    Retrieve a single Promotion

    This endpoint will return a Promotion based on it's id
    """
    app.logger.info("Request for promotion with id: %s", promotion_id)

    # Attempt to find the Promotion and abort if not found
    promotion = Promotion.find(promotion_id)
    if not promotion:
        error(
            status.HTTP_404_NOT_FOUND,
            f"Promotion with id '{promotion_id}' was not found.",
        )

    app.logger.info("Returning promotion: %s", promotion.name)
    return jsonify(promotion.serialize()), status.HTTP_200_OK


######################################################################
# DELETE A PROMOTION
######################################################################
# @app.route("/promotions/<int:promotion_id>", methods=["DELETE"])
# def delete_promotions(promotion_id):
#     """
#     Delete a single Promotion

#     This endpoint will return the deleted promotion if success


#     Otherwise return 404 Not Found
#     """
#     app.logger.info("Request to delete promotion with id: %s", promotion_id)
#     Promotion.delete_by_id(promotion_id)
#     return "", status.HTTP_204_NO_CONTENT


@app.route("/promotions/<int:promotion_id>", methods=["DELETE"])
def delete_promotions(promotion_id):
    """
    Delete a Promotion

    This endpoint will delete a Promotion based the id specified in the path
    """
    app.logger.info("Request to Delete a promotion with id [%s]", promotion_id)
    # Delete the Promotion if it exists
    promotion = Promotion.find(promotion_id)
    if promotion:
        app.logger.info("Promotion with ID: %d found.", promotion.id)
        promotion.delete()

    app.logger.info("Promotion with ID: %d delete complete.", promotion_id)
    return {}, status.HTTP_204_NO_CONTENT


######################################################################
# LIST PROMOTIONS
######################################################################
@app.route("/promotions", methods=["GET"])
def list_promotions():
    """
    Retrieves list of all Promotions
    This endpoint will return a list of all Promotions
    """
    app.logger.info("Request to List all promotions")

    promotions = []

    # Parse any arguments from the query string
    name = request.args.get("name")
    product_id = request.args.get("product_id", type=int)
    promotion_type = request.args.get("promotion_type")
    start_date = request.args.get("start_date")
    promotion_status = request.args.get("status")

    if name:
        app.logger.info("Find by name: %s", name)
        promotions = Promotion.find_by_name(name)
    elif promotion_type:
        app.logger.info("Find by promotion type: %s", promotion_type)
        # create enum from string
        promotion_type_value = getattr(PromotionType, promotion_type.upper())
        promotions = Promotion.find_by_promotion_type(promotion_type_value)
    elif product_id:
        app.logger.info("Find by product id: %d", product_id)
        promotions = Promotion.find_by_product_id(product_id)
    elif start_date:
        app.logger.info("Find by promotion type: %s", start_date)
        promotions = Promotion.find_by_start_date(start_date)
    elif promotion_status:
        app.logger.info("Find by promotion status: %s", promotion_status)
        # create bool from string
        promotion_status_value = promotion_status.lower() in ["true", "yes", "1"]
        promotions = Promotion.find_by_promotion_status(promotion_status_value)
    else:
        app.logger.info("Find all")
        promotions = Promotion.all()

    results = [promotion.serialize() for promotion in promotions]
    app.logger.info("[%s] Promotions returned", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# UPDATE AN EXISTING PROMOTION
######################################################################
@app.route("/promotions/<int:promotion_id>", methods=["PUT"])
def update_promotions(promotion_id):
    """
    Update a Promotion

    This endpoint will update a Promotion based on the body that is posted
    """
    app.logger.info("Request to update promotion with id: %s", promotion_id)
    check_content_type("application/json")

    promotion = Promotion.find(promotion_id)
    if not promotion:
        error(
            status.HTTP_404_NOT_FOUND,
            f"Promotion with id '{promotion_id}' was not found.",
        )

    promotion.deserialize(request.get_json())
    promotion.update()

    # Commit changes to the database
    db.session.commit()

    app.logger.info("Promotion with ID [%s] updated.", promotion.id)
    return jsonify(promotion.serialize()), status.HTTP_200_OK


######################################################################
# ACTIVATE AN EXISTING PROMOTION
######################################################################
@app.route("/promotions/<int:promotion_id>/activate", methods=["PUT"])
def activate_promotions(promotion_id):
    """
    Activates a Promotion

    This endpoint will activate a Promotion
    """
    app.logger.info("Request to activate the promotion with id: %s", promotion_id)
    promotion = Promotion.find(promotion_id)
    if not promotion:
        error(
            status.HTTP_404_NOT_FOUND,
            f"Promotion with id '{promotion_id}' was not found.",
        )
    promotion.activate()
    # Commit changes to the database
    db.session.commit()
    app.logger.info("Promotion with ID [%s] activated.", promotion.id)
    return jsonify(promotion.serialize()), status.HTTP_200_OK


######################################################################
# DEACTIVATE AN EXISTING PROMOTION
######################################################################
@app.route("/promotions/<int:promotion_id>/deactivate", methods=["PUT"])
def deactivate_promotions(promotion_id):
    """
    Deactivates a Promotion

    This endpoint will deactivate a Promotion
    """
    app.logger.info("Request to deactivate the promotion with id: %s", promotion_id)
    # check_content_type("application/json")

    promotion = Promotion.find(promotion_id)
    if not promotion:
        error(
            status.HTTP_404_NOT_FOUND,
            f"Promotion with id '{promotion_id}' was not found.",
        )

    # promotion.deserialize(request.get_json())
    promotion.deactivate()

    # Commit changes to the database
    db.session.commit()

    app.logger.info("Promotion with ID [%s] deactivated.", promotion.id)
    return jsonify(promotion.serialize()), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


######################################################################
# Checks the ContentType of a request
######################################################################
def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        error(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    error(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


######################################################################
# Logs error messages before aborting
######################################################################
def error(status_code, reason):
    """Logs the error and then aborts"""
    app.logger.error(reason)
    abort(status_code, reason)
