$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) 
    {
        $("#promotion_id").val(res.id);
        $("#promotion_name").val(res.name);
        $("#promotion_type").val(res.promotion_type);
        $("#promotion_product_id").val(res.product_id);
        $("#promotion_start_date").val(res.start_date);
        $("#promotion_duration").val(res.duration);
        $("#promotion_rule").val(res.rule);
        if (res.status === true) {
            $("#promotion_status").val("true");
        } else if (res.status === false) {
            $("#promotion_status").val("false");
        } 
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#promotion_id").val("");
        $("#promotion_name").val("");
        $("#promotion_type").val("");
        $("#promotion_product_id").val("");
        $("#promotion_start_date").val("");
        $("#promotion_duration").val("");
        $("#promotion_rule").val("");
        $("#promotion_status").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Promotion
    // ****************************************

    $("#create-btn").click(function () {
        event.preventDefault();

        let id=parseInt($("#promotion_id").val());
        let name = $("#promotion_name").val();
        let type = $("#promotion_type").val();
        let product_id=parseInt($("#promotion_product_id").val());
        let start_date = $("#promotion_start_date").val();
        let duration=parseInt($("#promotion_duration").val());
        let rule=$("#promotion_rule").val();
        let status_string=$("#promotion_status").val();
        let status = status_string === "true";
        let data = {
            "id":id,
            "name": name,
            "promotion_type":type,
            "product_id":product_id,
            "start_date":start_date,
            "duration":duration,
            "rule":rule,
            "status":status,
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/promotions",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Promotion
    // ****************************************

    $("#update-btn").click(function () {
        let id=parseInt($("#promotion_id").val());
        let name = $("#promotion_name").val();
        let type = $("#promotion_type").val();
        let product_id=parseInt($("#promotion_product_id").val());
        let start_date = $("#promotion_start_date").val();
        let duration=parseInt($("#promotion_duration").val());
        let rule=$("#promotion_rule").val();
        let status_string=$("#promotion_status").val();
        let status = status_string === "true";
        let data = {
            "id":id,
            "name": name,
            "promotion_type":type,
            "product_id":product_id,
            "start_date":start_date,
            "duration":duration,
            "rule":rule,
            "status":status
        };
        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/promotions/${id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Promotion
    // ****************************************

    $("#retrieve-btn").click(function () {

        let promotion_id = $("#promotion_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/promotions/${promotion_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Promotion
    // ****************************************

    $("#delete-btn").click(function () {

        let promotion_id = $("#promotion_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/promotions/${promotion_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Promotion has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });
    
    // ****************************************
    // Activate a Promotion
    // ****************************************

    $("#activate-btn").click(function () {

        let promotion_id = $("#promotion_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/promotions/${promotion_id}/activate`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Promotion has been Activated!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Deactivate a Promotion
    // ****************************************

    $("#deactivate-btn").click(function () {

        let promotion_id = $("#promotion_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/promotions/${promotion_id}/deactivate`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Promotion has been Deactivated!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });


    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#promotion_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Promotion
    // ****************************************

    $("#search-btn").click(function () {
        let name = $("#promotion_name").val();
        let ptype = $("#promotion_type").val();
        let product_id = $("#promotion_product_id").val();
        let start_date = $("#promotion_start_date").val();
        let status = $("#promotion_status").val() == "true";
        

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (ptype) {
            if (queryString.length > 0) {
                queryString += '&promotion_type=' + ptype
            } else {
                queryString += 'promotion_type=' + ptype
            }
        }
        if (product_id) {
            if (queryString.length > 0) {
                queryString += '&product_id=' + product_id
            } else {
                queryString += 'product_id=' + product_id
            }
        }
        if (start_date) {
            if (queryString.length > 0) {
                queryString += '&start_date=' + start_date
            } else {
                queryString += 'start_date=' + start_date
            }
        }
        if (status) {
            if (queryString.length > 0) {
                queryString += '&status=' + status
            } else {
                queryString += 'status=' + status
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/promotions?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-1">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Promotion Type</th>'
            table += '<th class="col-md-1">Product ID</th>'
            table += '<th class="col-md-2">Start Date</th>'
            table += '<th class="col-md-1">Duration</th>'
            table += '<th class="col-md-3">Rule</th>'
            table += '<th class="col-md-1">Status</th>'


            table += '</tr></thead><tbody>'
            let firstPromotion = "";
            for(let i = 0; i < res.length; i++) {
                let promotion = res[i];
                table +=  `<tr id="row_${i}"><td>${promotion.id}</td><td>${promotion.name}</td><td>${promotion.promotion_type}</td><td>${promotion.product_id}</td><td>${promotion.start_date}</td><td>${promotion.duration}</td><td>${promotion.rule}</td><td>${promotion.status}</td></tr>`;
                if (i == 0) {
                    firstPromotion = promotion;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstPromotion != "") {
                update_form_data(firstPromotion)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    $("#clear-table-btn").ready(function() {
        $('#clear-table-btn').click(function() {
          $('#search_results table tbody').empty();
        });
      });

})
