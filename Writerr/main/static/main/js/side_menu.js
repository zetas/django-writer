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
    $.ajaxSetup({
      cache: false
    });
    $("#loadMenu").sidr({
      name: 'leftMenu',
      source: '#sideMenu',
      displace: false,
      attachTo: 'body',
      renaming: false
    });
    $("#leftMenu").on('click', '#menu_logo', function() {
      return $.sidr('close', 'leftMenu');
    });
    $('#leftMenu').on('click', '#classes-button', function(e) {
      e.preventDefault();
      $.sidr('close', 'leftMenu');
      return $.ajax('/classes/list/', {
        timeout: 3000,
        success: function(response) {
          var dialogNode;
          dialogNode = $(response);
          dialogNode.attr('title', 'Class List');
          return dialogNode.dialog({
            duration: 'null',
            easing: 'null',
            modal: true,
            width: 720
          });
        },
        error: function(response) {
          return showAlert('error', response.statusText);
        },
        beforeSend: function() {
          return loadingMgr('open');
        },
        complete: function() {
          return loadingMgr('close');
        }
      });
    });
    $('#leftMenu').on('click', '#edit-paper-button', function(e) {
      e.preventDefault();
      $.sidr('close', 'leftMenu');
      return $.ajax('/papers/list/', {
        timeout: 3000,
        success: function(response) {
          var dialogNode;
          dialogNode = $(response);
          dialogNode.attr('title', 'Paper List');
          return dialogNode.dialog({
            duration: 'null',
            easing: 'null',
            modal: true,
            width: 720
          });
        },
        error: function(response) {
          return showAlert('error', response.statusText);
        },
        beforeSend: function() {
          return loadingMgr('open');
        },
        complete: function() {
          return loadingMgr('close');
        }
      });
    });
    return $('#leftMenu').on('click', '#submission-list-button', function(e) {
      e.preventDefault();
      $.sidr('close', 'leftMenu');
      return $.ajax('/papers/submit/list/', {
        timeout: 3000,
        success: function(response) {
          var dialogNode;
          dialogNode = $(response);
          dialogNode.attr('title', 'Submission List');
          return dialogNode.dialog({
            duration: 'null',
            easing: 'null',
            modal: true,
            width: 720
          });
        },
        error: function(response) {
          return showAlert('error', response.statusText);
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
