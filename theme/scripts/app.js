requirejs(['require',
        '/scripts/flickity.pkgd.js',
        '/scripts/fontfaceobserver.js',
        '/scripts/respimage.js',
        '/scripts/ls.parent-fit.js',
        '/scripts/lazysizes-umd.js'
    ],
    function(require, Flickity) {
        'use strict';

        var font = new FontFaceObserver('Open Sans');
        font.load().then(function () {
            document.documentElement.className += " app-fonts--loaded";
        });

        // Static navigation drawer
        let navBarIsActive = false;

        function navigationToggleHandler(element, options) {
            let $navBar = document.querySelector(options.navBar);
            // Handle navigation states
            if (navBarIsActive) {
                element.classList.remove(options.navBarToggleActiveClass);
                $navBar.classList.remove(options.navBarVisible);
                $navBar.classList.add(options.navBarHidden);
            } else {
                element.classList.add(options.navBarToggleActiveClass);
                $navBar.classList.add(options.navBarVisible);
                $navBar.classList.remove(options.navBarHidden);
            }
            navBarIsActive = !navBarIsActive;
        }

        var navBarToggle = Array.prototype.slice.call(document.querySelectorAll('.js-nav-toggle'));
        // Nav bar toggle
        navBarToggle.forEach(function(el) {
            el.addEventListener("click", function(event) {
                event.preventDefault();
                event.stopPropagation();
                navigationToggleHandler(el,
                    {
                        navBar: ".c-nav-bar",
                        navBarHidden: "c-nav-bar--hidden",
                        navBarVisible: "c-nav-bar--visible",
                        navBarToggleActiveClass: "js-nav-toggle--active",
                        navBarToggleCloseClass: "js-nav-toggle--close"
                    }
                );
            })
        });

        var $bannerBar = document.querySelector('.app-js-carousel'),
            $galleryContainer = document.querySelector('.js-gallery');
        if ($bannerBar !== null) {
            var bannerflkty = new Flickity('.app-js-carousel', {
                pauseAutoPlayOnHover: false,
                autoPlay: 7000,
                contain: true,
                wrapAround: true,
                imagesLoaded: true,
                cellSelector: '.app-banner-item',
                cellAlign: 'left',
                selectedAttraction: 0.025,
                friction: 0.28
            });
            $bannerBar.classList.add('app-banner--loaded');
        }
        // Content image galleries
        if ($galleryContainer !== null) {
            var flkty = new Flickity('.js-gallery', {
                autoPlay: true,
                contain: true,
                wrapAround: true,
                imagesLoaded: true,
                cellSelector: '.app-gallery-cell',
                cellAlign: 'left'
            });
            $galleryContainer.classList.add('app-banner--loaded');
        }

        // Initialize scripts

        // Load Slider Resize
        window.addEventListener('load', function() {
            var sliders = Array.prototype.slice.call(document.querySelectorAll('.js-slider-resize'));
            if (sliders) {
                sliders.forEach(function(slider) {
                    var flkty = Flickity.data(slider);
                    flkty.resize()
                });
            }
        });



    });
