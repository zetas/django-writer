studentConfirm = (studentDiv, type, verb) ->
  classroom = studentDiv.data 'class'
  student = studentDiv.data 'student'
  name = studentDiv.data 'name'

  noty
    text: "Are you sure you want to <strong>" + verb + "</strong> " + name + "?"
    type: 'warning'
    modal: true
    layout: 'center'
    buttons: [
      {
        addClass: "btn btn-primary"
        text: "Ok"
        onClick: ($noty) ->
          $noty.close()
          $('#alerts').noty
                        text: "Not yet implemented."
                        type: "error"
                        timeout: 1500
          return
      }
      {
        addClass: "btn btn-danger"
        text: "Cancel"
        onClick: ($noty) ->
          $noty.close()
          $('#alerts').noty
                        text: "Ok, cancelled."
                        timeout: 1500
          return
      }
    ]


$(document).ready ->
  $('.class_tooltip').tooltip container: 'body'

  $('#add_student_link').click (e) ->
    e.preventDefault()

    $("#id_students").val('')

    dialogDiv = $('#dialog_holder_add')
    dialogDiv.dialog 'close'

    dialogDiv.attr 'title', 'Update Class & Assign New Students'
    dialogDiv.removeClass('hidden')
    dialogDiv.dialog duration:'null', easing:'null', modal: true, width: 480

  $('#classes_add_student').click (e) ->
    e.preventDefault()

    $(@).prop('disabled', true)
    $(@).addClass('disabled')
    $(@).html('Processing... <div id="loading"><span id="loading_cog" class="glyphicon glyphicon-cog"></span></div>')

    $('#add_student_form').submit()

  $('.pending_remove_link').click (e) ->
    e.preventDefault()

    studentConfirm($(@), 'pending', 'remove')

  $('.remove_link').click (e) ->
    e.preventDefault()

    studentConfirm($(@), 'active', 'remove')

  $('.promote_link').click (e) ->
    e.preventDefault()

    studentConfirm($(@), 'active', 'promote')

  $('.demote_link').click (e) ->
    e.preventDefault()

    studentConfirm($(@), 'active', 'demote')




#$('#alerts').noty({timeout: 1500, dismissQueue: true, type: alertType, text: alertText, callback: {afterClose: -> doRedirect()}})