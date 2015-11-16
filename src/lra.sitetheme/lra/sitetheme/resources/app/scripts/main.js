'use strict';
(function ($) {
  $(document).ready(function () {
    // Setup media query for enabling dynamic layouts only on
    // larger screen sizes
    var mq = window.matchMedia("(min-width: 480px)");
    if ($(".userrole-anonymous")[0]){
      $('input[type="password"]').showPassword('focus', {
      });
      $('.app-signin-input').jvFloat();
      var $mcNote = $('#app-signin-suggestion');
      Mailcheck.defaultDomains.push('lra-aic-fdb.de')
      $('#ac-name').on('blur', function (event) {
        console.log("event ", event);
        console.log("this ", $(this));
        $(this).mailcheck({
          // domains: domains,                       // optional
          // topLevelDomains: topLevelDomains,       // optional
          suggested: function (element, suggestion) {
                // callback code
                console.log("suggestion ", suggestion.full);
                $mcNote.removeClass('hidden').addClass('fadeInDown');
                $mcNote.html("Meinten Sie <i>" + suggestion.full + "</i>?");
                $mcNote.on('click', function (evt) {
                  evt.preventDefault();
                  $('#ac-name').val(suggestion.full);
                  $mcNote.removeClass('fadeInDown').addClass('fadeOutUp').delay(2000).addClass('hidden');
                });
              },
          empty: function (element) {
                // callback code
                $mcNote.html('').addClass('hidden');
              }
        });
      });
      // Enable gallery and masonry scripts based on screen size
      if (mq.matches) {
        var bannerflkty = new Flickity('.app-banner', {
          autoPlay: 7000,
          contain: true,
          wrapAround: true,
          imagesLoaded: true,
          cellSelector: '.app-banner-item',
          cellAlign: 'left',
          selectedAttraction: 0.025,
          friction: 0.28
          // lower attraction and lower friction
          // slower transitions
          // easier to flick past cells
        });
        var flkty = new Flickity('.main-gallery', {
          autoPlay: true,
          contain: true,
          wrapAround: true,
          imagesLoaded: true,
          cellSelector: '.app-gallery-cell',
          cellAlign: 'left'
        });
      }
    };
  }
  );
}(jQuery));

