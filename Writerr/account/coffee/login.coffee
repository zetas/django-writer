$(document).ready ->

  $("#loginform_submit").click (e) ->
    e.preventDefault()

    $("#loginform").submit()

  $("#signup_button").click (e) ->
    e.preventDefault()

    window.location = $(@).data 'target'