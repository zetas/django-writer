$(document).ready ->
  $(document.body).on "click", ".dropdown-menu li", (event) ->
    target = $(event.currentTarget)
    target.closest(".btn-group").find("[data-bind=\"label\"]").text(target.text()).end().children(".dropdown-toggle").dropdown "toggle"
    $('#aType').val target.text().toLowerCase()

  $('#input-password1').hidePassword true
  $('#input-password2').hidePassword true

  $('#signup_submit').click (e) ->
    e.preventDefault()
    $(@).prop('disabled', true)
    $(@).addClass('disabled')
    $(@).html('Processing... <div id="loading"><span id="loading_cog" class="glyphicon glyphicon-cog"></span></div>')

    $('#signup_form').submit()

