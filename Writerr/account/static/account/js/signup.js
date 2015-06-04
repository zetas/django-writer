(function() {
  $(document).ready(function() {
    $(document.body).on("click", ".dropdown-menu li", function(event) {
      var target;
      target = $(event.currentTarget);
      target.closest(".btn-group").find("[data-bind=\"label\"]").text(target.text()).end().children(".dropdown-toggle").dropdown("toggle");
      return $('#aType').val(target.text().toLowerCase());
    });
    $('#input-password1').hidePassword(true);
    $('#input-password2').hidePassword(true);
    return $('#signup_submit').click(function(e) {
      e.preventDefault();
      $(this).prop('disabled', true);
      $(this).addClass('disabled');
      $(this).html('Processing... <div id="loading"><span id="loading_cog" class="glyphicon glyphicon-cog"></span></div>');
      return $('#signup_form').submit();
    });
  });

}).call(this);
