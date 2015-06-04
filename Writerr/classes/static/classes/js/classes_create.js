(function() {
  $(document).ready(function() {
    return $('#classes_submit_button').click(function(e) {
      e.preventDefault();
      $(this).prop('disabled', true);
      $(this).addClass('disabled');
      $(this).html('Processing... <div id="loading"><span id="loading_cog" class="glyphicon glyphicon-cog"></span></div>');
      return $('#class_create_form').submit();
    });
  });

}).call(this);
