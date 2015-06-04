$(document).ready ->
  $('.feedback_link').click (e) ->
    e.preventDefault()

    div = $(@)

    id = div.attr('id')

    if id == 'feedback_given'
      $('#feedback_received').removeClass('selected')
      div.addClass('selected')

      $('#feedback_received_table').addClass('hidden')
      $('#feedback_given_table').removeClass('hidden')
    else if id == 'feedback_received'
      $('#feedback_received').addClass('selected')
      div.removeClass('selected')

      $('#feedback_given_table').addClass('hidden')
      $('#feedback_received_table').removeClass('hidden')

  $('.class_link').click (e) ->
    e.preventDefault()

    div = $(@)
    id = div.attr('id')


    $('.class_list').find('.selected').removeClass('selected')
    div.addClass('selected')

    $('.submission_table').addClass('hidden')

    if id == 'all'
      $('#submission_all_table').removeClass('hidden')
    else
      $('#submission_'+id+'_table').removeClass('hidden')



