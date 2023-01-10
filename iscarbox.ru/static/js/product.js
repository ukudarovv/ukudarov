function product_material_image (a) {
    document.example_material_img.src = a;
}

function product_thread_image (b) {
    document.example_thread_img.src = b;
}

function product_border_image (c) {
    document.example_border_img.src = c;
}

function product_accessory_image (d) {
    document.example_accessory_img.src = d;
}

$('.example').on('click', function() {
    var id = $(this).attr('data-n');
    $('.select').find("[value=" + id + "]").prop("selected", true);
});

$('.example_1').on('click', function() {
    var id = $(this).attr('data-n');
    $('.select_1').find("[value=" + id + "]").prop("selected", true);
});

$('.example_2').on('click', function() {
    var id = $(this).attr('data-n');
    $('.select_2').find("[value=" + id + "]").prop("selected", true);
});

$('.example_3').on('click', function() {
    var id = $(this).attr('data-n');
    $('.select_3').find("[value=" + id + "]").prop("selected", true);
});
