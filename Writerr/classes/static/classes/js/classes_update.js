(function() {
  var studentConfirm;

  studentConfirm = function(studentDiv, type, verb) {
    var classroom, name, student;
    classroom = studentDiv.data('class');
    student = studentDiv.data('student');
    name = studentDiv.data('name');
    return noty({
      text: "Are you sure you want to <strong>" + verb + "</strong> " + name + "?",
      type: 'warning',
      modal: true,
      layout: 'center',
      buttons: [
        {
          addClass: "btn btn-primary",
          text: "Ok",
          onClick: function($noty) {
            $noty.close();
            $('#alerts').noty({
              text: "Not yet implemented.",
              type: "error",
              timeout: 1500
            });
          }
        }, {
          addClass: "btn btn-danger",
          text: "Cancel",
          onClick: function($noty) {
            $noty.close();
            $('#alerts').noty({
              text: "Ok, cancelled.",
              timeout: 1500
            });
          }
        }
      ]
    });
  };

  $(document).ready(function() {
    $('.class_tooltip').tooltip({
      container: 'body'
    });
    $('#add_student_link').click(function(e) {
      var dialogDiv;
      e.preventDefault();
      $("#id_students").val('');
      dialogDiv = $('#dialog_holder_add');
      dialogDiv.dialog('close');
      dialogDiv.attr('title', 'Update Class & Assign New Students');
      dialogDiv.removeClass('hidden');
      return dialogDiv.dialog({
        duration: 'null',
        easing: 'null',
        modal: true,
        width: 480
      });
    });
    $('#classes_add_student').click(function(e) {
      e.preventDefault();
      $(this).prop('disabled', true);
      $(this).addClass('disabled');
      $(this).html('Processing... <div id="loading"><span id="loading_cog" class="glyphicon glyphicon-cog"></span></div>');
      return $('#add_student_form').submit();
    });
    $('.pending_remove_link').click(function(e) {
      e.preventDefault();
      return studentConfirm($(this), 'pending', 'remove');
    });
    $('.remove_link').click(function(e) {
      e.preventDefault();
      return studentConfirm($(this), 'active', 'remove');
    });
    $('.promote_link').click(function(e) {
      e.preventDefault();
      return studentConfirm($(this), 'active', 'promote');
    });
    return $('.demote_link').click(function(e) {
      e.preventDefault();
      return studentConfirm($(this), 'active', 'demote');
    });
  });

}).call(this);
