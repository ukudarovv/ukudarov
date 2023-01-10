$(document).ready(function(){
    $(".owl-carousel").owlCarousel({
        items: 1,
        autoplay: true,
        loop: true,
        dots: false,
        autoplayTimeout: 7000
    });

    // function basketUpdating(product_id, quantity, product_material, product_thread, product_border, product_accessory){
    //     var data = {};
    //     data.product_id = product_id;
    //     data.quantity = quantity;
    //     data.product_material = product_material;
    //     data.product_thread = product_thread;
    //     data.product_border = product_border;
    //     data.product_accessory = product_accessory;
    //     var csrf_token = $('#form_add_cart [name="csrfmiddlewaretoken"]').val();
    //     data ["csrfmiddlewaretoken"] = csrf_token;
    //     var url = form.attr("action");
    //     console.log(data)
    //     $.ajax({
    //         url: url,
    //         type: 'POST',
    //         data: data,
    //         cache: true,
    //         success: function (data){
    //         },
    //         error: function(e){
    //         },
    //     });
    // }
    //
    // var form = $('#form_add_cart');
    // form.on('submit', function(e) {
    //     e.preventDefault();
    //
    //     var product_id = $('#submit_btn').data("product_id");
    //     var product_price = $('#submit_btn').data("product_price");
    //     var quantity = $('#quantity').val();
    //
    //     var e = document.getElementById("select");
    //     var product_material = e.options[e.selectedIndex].value;
    //     var e = document.getElementById("select_1");
    //     var product_thread = e.options[e.selectedIndex].value;
    //     var e = document.getElementById("select_2");
    //     var product_border = e.options[e.selectedIndex].value;
    //     var e = document.getElementById("select_3");
    //     var product_accessory = e.options[e.selectedIndex].value;
    //
    //     basketUpdating(product_id, quantity, product_material, product_thread, product_border, product_accessory)
    // });
});
