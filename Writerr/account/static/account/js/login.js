(function() {
  $(document).ready(function() {
    $("#loginform_submit").click(function(e) {
      e.preventDefault();
      return $("#loginform").submit();
    });
    return $("#signup_button").click(function(e) {
      e.preventDefault();
      return window.location = $(this).data('target');
    });
  });

}).call(this);
