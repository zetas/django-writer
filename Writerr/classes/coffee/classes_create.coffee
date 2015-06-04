$(document).ready ->
  $('#classes_submit_button').click (e) ->
    e.preventDefault()

    $(@).prop('disabled', true)
    $(@).addClass('disabled')
    $(@).html('Processing... <div id="loading"><span id="loading_cog" class="glyphicon glyphicon-cog"></span></div>')

    $('#class_create_form').submit()





