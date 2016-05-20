var $bannerBar = document.querySelectorAll('.app-js-carousel'),
    $galleryContainer = document.querySelectorAll('.js-gallery');
// Show banner bar
if ($bannerBar.length) {
    var bannerflkty = new Flickity('.app-js-carousel', {
        autoPlay: 7000,
        contain: true,
        wrapAround: true,
        imagesLoaded: true,
        cellSelector: '.app-banner-item',
        cellAlign: 'left',
        selectedAttraction: 0.025,
        friction: 0.28
    });
}
// Content image galleries
if ($galleryContainer.length) {
    var flkty = new Flickity('.js-gallery', {
        autoPlay: true,
        contain: true,
        wrapAround: true,
        imagesLoaded: true,
        cellSelector: '.app-gallery-cell',
        cellAlign: 'left'
    });
}
require( [ 'jquery-bridget/jquery.bridget' ],
    function(jQueryBridget) {
        jQueryBridget( 'fcky', Flickity);
        // make Flickity a jQuery plugin
        $('.app-js-carousel').fcky({});
        // now you can use $().flickity()
        // $('.app-js-carousel').flickity({
        //   autoPlay: 7000,
        //   contain: true,
        //   wrapAround: true,
        //   imagesLoaded: true,
        //   cellSelector: '.app-banner-item',
        //   cellAlign: 'left',
        //   selectedAttraction: 0.025,
        //   friction: 0.28
        // });
        // $('.js-gallery').flickity({
        //   autoPlay: 7000,
        //   contain: true,
        //   wrapAround: true,
        //   imagesLoaded: true,
        //   cellSelector: '.app-banner-item',
        //   cellAlign: 'left',
        //   selectedAttraction: 0.025,
        //   friction: 0.28
        // });

    });
