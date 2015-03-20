'use strict';
(function ($) {
  $(document).ready(function () {
    $('input[type="password"]').showPassword('focus', {
        // toggle: { className: 'my-toggle' }
    });
    var bLazy = new Blazy({
        selector: '.b-lazy'
    });
  }
  );
}(jQuery));
