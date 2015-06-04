(function() {
  window.showAlert = function(alertType, alertText, redirect, quiet) {
    var doRedirect, qAlertDiv;
    if (redirect == null) {
      redirect = false;
    }
    if (quiet == null) {
      quiet = false;
    }
    if (redirect !== false) {
      doRedirect = function() {
        return window.location = redirect;
      };
    } else {
      doRedirect = function() {};
    }
    if (!quiet) {
      return $('#alerts').noty({
        timeout: 1500,
        dismissQueue: true,
        type: alertType,
        text: alertText,
        callback: {
          afterClose: function() {
            return doRedirect();
          }
        }
      });
    } else {
      qAlertDiv = $('#quiet_alert');
      qAlertDiv.html(alertText);
      qAlertDiv.fadeIn('slow');
      return qAlertDiv.fadeOut(2000);
    }
  };

  window.loadingMgr = function(action) {
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

}).call(this);
