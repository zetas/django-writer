stripeResponseHandler = (status, response) ->
  form = $('#checkout_payment');

  #console.log 'Inside Callback'

  if (response.error)
    # Show the errors on the form
    form.find('.payment-errors').text(response.error.message)
    $('#checkout_submit').prop('disabled', false)
    $('#checkout_submit').removeClass('disabled')
    #console.log 'Error!' + response.error.message
  else
    #console.log 'Success!'
    #// token contains id, last4, and card type
    token = response.id
    #// Insert the token into the form so it gets submitted to the server
    form.find('#stripe_token').val(token)
    form.find('#cc_type').val(response.card.type)
    form.find('#last_4').val(response.card.last4)
    #// and submit
    form.get(0).submit()

processForm = (e) ->
  e.preventDefault()

  form = $("#checkout_payment")

  # Disable the submit button to prevent repeated clicks
  $('#checkout_submit').prop('disabled', true)
  $('#checkout_submit').addClass('disabled')
  $('#checkout_submit').html('Processing... <div id="loading"><span id="loading_cog" class="glyphicon glyphicon-cog"></span></div>')

  window.Stripe.card.createToken(form, stripeResponseHandler)

numberFormat = (nStr) ->
  nStr += ""
  x = nStr.split(".")
  x1 = x[0]
  x2 = (if x.length > 1 then "." + x[1] else "")
  rgx = /(\d+)(\d{3})/
  x1 = x1.replace(rgx, "$1" + "," + "$2")  while rgx.test(x1)
  x1 + x2


$(document).ready ->

  $('#stripe_cc_owner').val $('#id_billing_name').val()

  if window.account_type == 'personal'
    $('#license_count').html '1'
    $('#license_cost').html '$5.00'

  $('#checkout_submit').click (e) ->
    processForm(e)

  $('#checkout_payment').submit (e) ->
    processForm(e)

  $('#id_last_name').focusout ->
    #id_billing_name
    #stripe_cc_owner
    first_name = $('#id_first_name')

    if first_name.val() == ''
      return false

    billing_name_input = $('#id_billing_name')
    cc_name_input = $('#stripe_cc_owner')

    billing_name_input.val first_name.val() + ' ' + $(@).val()

    cc_name_input.val first_name.val() + ' ' + $(@).val()

  $('#id_quantity').change ->

    count = $(@).val()

    monthly_div = $('#sub_type_radio_0')

    if monthly_div.attr('checked')
      multiplier = 5
    else
      multiplier = 50

    $('#license_count').html count
    $('#license_cost').html '$' + numberFormat(count * multiplier) + '.00 '

  $('.sub_type').change ->
    $('#price_type_header').html $(@).val()

    if window.account_type == 'enterprise'
      $('#license_count').html '0'
      $('#license_cost').html '$0.00'
    else
      $('#license_count').html '1'
      if $(@).val() == 'yearly'
        $('#license_cost').html '$50.00'
      else
        $('#license_cost').html '$5.00'


    current_quantity = $('#id_quantity').val()

    if current_quantity != ''
      $('#id_quantity').val ''





