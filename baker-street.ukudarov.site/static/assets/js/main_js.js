(function ($) {
    "use strict";

     /*====== Sidebar menu Active ======*/
    function mobileMenuActive() {
        var navbarTrigger = $('.mobile-menu-button-active'),
            endTrigger = $('.sidebar-close'),
            container = $('.mobile-menu-active'),
            wrapper4 = $('.main-wrapper-3');

        wrapper4.prepend('<div class="body-overlay-3"></div>');

        navbarTrigger.on('click', function(e) {
            e.preventDefault();
            container.addClass('sidebar-visible');
            wrapper4.addClass('overlay-active-3');
        });

        endTrigger.on('click', function() {
            container.removeClass('sidebar-visible');
            wrapper4.removeClass('overlay-active-3');
        });

        $('.body-overlay-3').on('click', function() {
            container.removeClass('sidebar-visible');
            wrapper4.removeClass('overlay-active-3');
        });
    };
    mobileMenuActive();
})(jQuery);
