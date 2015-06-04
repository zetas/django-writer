loadingMgr = (action) ->
  loadingNode = $('#loading')
  if action == 'open'
    loadingNode.attr 'title', 'Please Wait'
    loadingNode.dialog duration:'null', easing:'null', modal: true, width:380
  else if action == 'close'
    loadingNode.dialog 'close'

$(document).ready ->
  $.ajaxSetup cache: false
  $("#loadMenu").sidr name:'leftMenu', source:'#sideMenu', displace: false, attachTo: 'body', renaming: false

  $("#leftMenu").on 'click', '#menu_logo', ->
    $.sidr('close', 'leftMenu')

  $('#leftMenu').on 'click', '#classes-button', (e) ->
    e.preventDefault()

    $.sidr('close', 'leftMenu')

    $.ajax '/classes/list/',
      timeout: 3000
      success: (response) ->
        dialogNode = $(response)
        #dialogNode.dialog 'close'
        dialogNode.attr 'title', 'Class List'
        dialogNode.dialog duration:'null', easing:'null', modal: true, width: 720
      error: (response) ->
        showAlert 'error', response.statusText
      beforeSend: ->
        loadingMgr 'open'
      complete: ->
        loadingMgr 'close'

  $('#leftMenu').on 'click', '#edit-paper-button', (e) ->
    e.preventDefault()

    $.sidr('close', 'leftMenu')

    $.ajax '/papers/list/',
      timeout: 3000
      success: (response) ->
        dialogNode = $(response)
        #dialogNode.dialog 'close'
        dialogNode.attr 'title', 'Paper List'
        dialogNode.dialog duration:'null', easing:'null', modal: true, width: 720
      error: (response) ->
        showAlert 'error', response.statusText
      beforeSend: ->
        loadingMgr 'open'
      complete: ->
        loadingMgr 'close'

  $('#leftMenu').on 'click', '#submission-list-button', (e) ->
    e.preventDefault()

    $.sidr('close', 'leftMenu')

    $.ajax '/papers/submit/list/',
      timeout: 3000
      success: (response) ->
        dialogNode = $(response)
        #dialogNode.dialog 'close'
        dialogNode.attr 'title', 'Submission List'
        dialogNode.dialog duration:'null', easing:'null', modal: true, width: 720
      error: (response) ->
        showAlert 'error', response.statusText
      beforeSend: ->
        loadingMgr 'open'
      complete: ->
        loadingMgr 'close'