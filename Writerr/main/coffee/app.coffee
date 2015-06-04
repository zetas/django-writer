loadingMgr = (action) ->
  loadingNode = $('#loading')
  if action == 'open'
    loadingNode.attr 'title', 'Please Wait'
    loadingNode.dialog duration:'null', easing:'null', modal: true, width:380
  else if action == 'close'
    loadingNode.dialog 'close'


$(document).ready ->
  $(".user_type:eq(0)").attr "checked",true

  $(".radio-buttons label").click ->
		  $(".user_type").attr "checked",false
		  $(".radio-buttons label").removeClass "selected"
		  $(@).addClass "selected"
		  idn = $(@).data "order"

		  $(".user_type:eq("+idn+")").attr "checked",true

  $("#forgot_password_link").click (e) ->
    e.preventDefault()
    dialogDiv = $('#forgot_password_modal')
    dialogDiv.dialog 'close'

    dialogDiv.attr 'title', 'Reset Password'

    dialogDiv.removeClass('hidden')
    dialogDiv.dialog duration:'null', easing:'null', modal: true, width: 'auto'

  $("#forgot_password_form").submit (e) ->
    e.preventDefault()

    errorDiv = $('#error_account_recover_password')

    $.ajax '/account/reset/',
      type: 'POST'
      data: $(@).serialize()
      success: (result) ->
        found = result['found']
        if found == 'True'
          errorDiv.html('')
          successNode = $('<span class="success_text">A new password was sent to your email address. Please check your inbox for more details.</span>')
          errorDiv.append(successNode)
        else if found == 'False'
          errorDiv.html("The email address you entered could not be found.")
        else
          errorDiv.html("Invalid email address.")
      error: (response) ->
        errorDiv.html(response.statusText)
      beforeSend: ->
        loadingMgr 'open'
      complete: ->
        loadingMgr 'close'