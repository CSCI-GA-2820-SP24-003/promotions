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
from service.models import Promotion, db
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
    promotion.deserialize(request.get_json())
    promotion.create()
    message = promotion.serialize()
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
    product_id = request.args.get("product_id", type=int)
    start_date = request.args.get("start_date")
    promotion_type = request.args.get("promotion_type")
    if product_id or start_date or promotion_type:
        promotions = Promotion.find_by_filters(product_id, start_date, promotion_type)
    else:
        promotions = Promotion.all()
    serialized_promotions = [promotion.serialize() for promotion in promotions]
    app.logger.info("Promotions Listed")
    return jsonify(serialized_promotions), status.HTTP_200_OK


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
