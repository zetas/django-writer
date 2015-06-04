(function() {
  $(document).ready(function() {
    $('.feedback_link').click(function(e) {
      var div, id;
      e.preventDefault();
      div = $(this);
      id = div.attr('id');
      if (id === 'feedback_given') {
        $('#feedback_received').removeClass('selected');
        div.addClass('selected');
        $('#feedback_received_table').addClass('hidden');
        return $('#feedback_given_table').removeClass('hidden');
      } else if (id === 'feedback_received') {
        $('#feedback_received').addClass('selected');
        div.removeClass('selected');
        $('#feedback_given_table').addClass('hidden');
        return $('#feedback_received_table').removeClass('hidden');
      }
    });
    return $('.class_link').click(function(e) {
      var div, id;
      e.preventDefault();
      div = $(this);
      id = div.attr('id');
      $('.class_list').find('.selected').removeClass('selected');
      div.addClass('selected');
      $('.submission_table').addClass('hidden');
      if (id === 'all') {
        return $('#submission_all_table').removeClass('hidden');
      } else {
        return $('#submission_' + id + '_table').removeClass('hidden');
      }
    });
  });

}).call(this);
