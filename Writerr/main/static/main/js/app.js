(function() {
  var loadingMgr;

  loadingMgr = function(action) {
    var loadingNode;
    loadingNode = $('#loading');
    if (action === 'open') {
      loadingNode.attr('title', 'Please Wait');
      return loadingNode.dialog({
        duration: 'null',
        easing: 'null',
        modal: true,
        width: 380
      });
    } else if (action === 'close') {
      return loadingNode.dialog('close');
    }
  };

  $(document).ready(function() {
    $(".user_type:eq(0)").attr("checked", true);
    $(".radio-buttons label").click(function() {
      var idn;
      $(".user_type").attr("checked", false);
      $(".radio-buttons label").removeClass("selected");
      $(this).addClass("selected");
      idn = $(this).data("order");
      return $(".user_type:eq(" + idn + ")").attr("checked", true);
    });
    $("#forgot_password_link").click(function(e) {
      var dialogDiv;
      e.preventDefault();
      dialogDiv = $('#forgot_password_modal');
      dialogDiv.dialog('close');
      dialogDiv.attr('title', 'Reset Password');
      dialogDiv.removeClass('hidden');
      return dialogDiv.dialog({
        duration: 'null',
        easing: 'null',
        modal: true,
        width: 'auto'
      });
    });
    return $("#forgot_password_form").submit(function(e) {
      var errorDiv;
      e.preventDefault();
      errorDiv = $('#error_account_recover_password');
      return $.ajax('/account/reset/', {
        type: 'POST',
        data: $(this).serialize(),
        success: function(result) {
          var found, successNode;
          found = result['found'];
          if (found === 'True') {
            errorDiv.html('');
            successNode = $('<span class="success_text">A new password was sent to your email address. Please check your inbox for more details.</span>');
            return errorDiv.append(successNode);
          } else if (found === 'False') {
            return errorDiv.html("The email address you entered could not be found.");
          } else {
            return errorDiv.html("Invalid email address.");
          }
        },
        error: function(response) {
          return errorDiv.html(response.statusText);
        },
        beforeSend: function() {
          return loadingMgr('open');
        },
        complete: function() {
          return loadingMgr('close');
        }
      });
    });
  });

}).call(this);
