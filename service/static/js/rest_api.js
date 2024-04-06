$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#promotion_id").val(res.id);
        $("#promotion_name").val(res.name);
        $("#promotion_type").val(res.promotion_type);
        $("#product_id").val(res.product_id);
        $("#promotion_start_date").val(res.start_date);
        $("#promotion_duration").val(res.duration);
        $("#promotion_rule").val(res.rule);


    }

    /// Clears all form fields
    function clear_form_data() {
        $("#promotion_id").val("");
        $("#promotion_name").val("");
        $("#promotion_type").val("");
        $("#product_id").val("");
        $("#promotion_start_date").val("");
        $("#promotion_duration").val("");
        $("#promotion_rule").val("");

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
        let product_id=parseInt($("#promotion_id").val());
        let start_date = $("#promotion_start_date").val();
        let duration=parseInt($("#promotion_duration").val());
        let rule=$("#promotion_rule").val();
        let data = {
            "id":id,
            "name": name,
            "promotion_type":type,
            "product_id":product_id,
            "start_date":start_date,
            "duration":duration,
            "rule":rule
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

        // let promotion_id = $("#promotion_id").val();
        // let name = $("#promotion_name").val();
        // let category = $("#promotion_category").val();
        // let available = $("#promotion_available").val() == "true";
        // let gender = $("#promotion_gender").val();
        // let birthday = $("#promotion_birthday").val();

        // let data = {
        //     "name": name,
        //     "category": category,
        //     "available": available,
        //     "gender": gender,
        //     "birthday": birthday
        // };
        let id=parseInt($("#promotion_id").val());
        let name = $("#promotion_name").val();
        let type = $("#promotion_type").val();
        let product_id=parseInt($("#promotion_id").val());
        let start_date = $("#promotion_start_date").val();
        let duration=parseInt($("#promotion_duration").val());
        let rule=$("#promotion_rule").val();
        let data = {
            "id":id,
            "name": name,
            "promotion_type":type,
            "product_id":product_id,
            "start_date":start_date,
            "duration":duration,
            "rule":rule
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

        let product_id=$("#product_id").val()
        let start_date=$("#start_date").val()
        let promotion_type=$("#promotion_type").val()
        let queryString = ""

        if (product_id) {
            queryString += 'product_id=' + product_id
        }
        if (start_date) {
            queryString += 'start_date=' + start_date
        }
        if (promotion_type) {
            queryString += 'promotion_type=' + promotion_type

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
            table += '<th class="col-md-3">Name</th>'
            table += '<th class="col-md-2">Promotion Type</th>'
            table += '<th class="col-md-1">Product ID</th>'
            table += '<th class="col-md-2">Start Date</th>'
            table += '<th class="col-md-1">Duration</th>'
            table += '<th class="col-md-3">Rule</th>'

            table += '</tr></thead><tbody>'
            let firstPromotion = "";
            for(let i = 0; i < res.length; i++) {
                let promotion = res[i];
                table +=  `<tr id="row_${i}"><td>${promotion.id}</td><td>${promotion.name}</td><td>${promotion.promotion_type}</td><td>${promotion.product_id}</td><td>${promotion.start_date}</td><td>${promotion.duration}</td><td>${promotion.rule}</td></tr>`;
                if (i == 0) {
                    firstPromotion = promotion;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // // copy the first result to the form
            // if (firstPromotion != "") {
            //     update_form_data(firstPromotion)
            // }

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
