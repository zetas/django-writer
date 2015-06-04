window.showAlert = (alertType, alertText, redirect = false, quiet = false) ->
    if redirect != false
        doRedirect = ->
            window.location = redirect
    else
        doRedirect = ->

    if not quiet
      $('#alerts').noty({timeout: 1500, dismissQueue: true, type: alertType, text: alertText, callback: {afterClose: -> doRedirect()}})
    else
      qAlertDiv = $('#quiet_alert')
      qAlertDiv.html alertText
      qAlertDiv.fadeIn('slow')
      qAlertDiv.fadeOut(2000)

window.loadingMgr = (action) ->
  loadingNode = $('#loading')
  if action == 'open'
    loadingNode.attr 'title', 'Please Wait'
    loadingNode.dialog duration:'null', easing:'null', modal: true, width:380
  else if action == 'close'
    loadingNode.dialog 'close'