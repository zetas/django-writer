
loadingMgr = (action) ->
  loadingNode = $('#loading')
  if action == 'open'
    loadingNode.attr 'title', 'Please Wait'
    loadingNode.dialog duration:'null', easing:'null', modal: true, width:380
  else if action == 'close'
    loadingNode.dialog 'close'

$(document).ready ->

  $('#send_invites_form').submit (e) ->
    e.preventDefault()

    errorDiv = $('#error_invites')

    resultsTable = $('#invites_sent')

    resultsTbody = resultsTable.find('tbody')

    $.ajax '/account/send_invite/',
      type: 'POST'
      data: $(@).serialize()
      success: (result) ->
        resultsTbody.html('')

        if result.error == 'invalid_form'
          resultsTbody.append($("<tr class='danger'><td colspan='3'>Invalid Recipients</td></tr>"))
        else if result.error == 'no_licenses_available'
          resultsTbody.append($("<tr class='danger'><td colspan='3'>You have no licenses available.</td></tr>"))
        else

          successes = 0
          for email of result
            if result[email]['error'] == 'invalid_email'
              resultsTbody.append($("<tr class='danger'><td>"+email+"</td><td><span class='glyphicon glyphicon-remove'></span></td><td>Invalid email address, skipping</td></tr>"))
              continue

            if result[email]['already_licensed'] == true
              resultsTbody.append($("<tr class='info'><td>"+email+"</td><td><span class='glyphicon glyphicon-ok'></span></td><td>Pre-existing license, skipping</td></tr>"))
            else
              if result[email]['exists'] == false
                if result[email]['already_sent'] == true
                  resultsTbody.append($("<tr class='info'><td>"+email+"</td><td><span class='glyphicon glyphicon-remove'></span></td><td>Previously sent license, resending the same code</td></tr>"))
                else
                  resultsTbody.append($("<tr class='success'><td>"+email+"</td><td><span class='glyphicon glyphicon-remove'></span></td><td>License code sent</td></tr>"))
              else
                resultsTbody.append($("<tr class='success'><td>"+email+"</td><td><span class='glyphicon glyphicon-ok'></span></td><td>License assigned</td></tr>"))

              successes++

            resultsTable.removeClass('hidden')

            if successes > 0
              total_licenses = $('#license_count').text()
              if total_licenses > 0
                if successes >= total_licenses
                  $('#additional_license_div').addClass('hidden')
                  $('#send_invites_form').addClass('hidden')
                else
                  $('#license_count').text total_licenses - successes


      error: (response) ->
        errorDiv.html(response.statusText)
      beforeSend: ->
        loadingMgr 'open'
      complete: ->
        loadingMgr 'close'