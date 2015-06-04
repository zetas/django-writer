(function() {
  var numberFormat, processForm, stripeResponseHandler;

  stripeResponseHandler = function(status, response) {
    var form, token;
    form = $('#checkout_payment');
    if (response.error) {
      form.find('.payment-errors').text(response.error.message);
      $('#checkout_submit').prop('disabled', false);
      return $('#checkout_submit').removeClass('disabled');
    } else {
      token = response.id;
      form.find('#stripe_token').val(token);
      form.find('#cc_type').val(response.card.type);
      form.find('#last_4').val(response.card.last4);
      return form.get(0).submit();
    }
  };

  processForm = function(e) {
    var form;
    e.preventDefault();
    form = $("#checkout_payment");
    $('#checkout_submit').prop('disabled', true);
    $('#checkout_submit').addClass('disabled');
    $('#checkout_submit').html('Processing... <div id="loading"><span id="loading_cog" class="glyphicon glyphicon-cog"></span></div>');
    return window.Stripe.card.createToken(form, stripeResponseHandler);
  };

  numberFormat = function(nStr) {
    var rgx, x, x1, x2;
    nStr += "";
    x = nStr.split(".");
    x1 = x[0];
    x2 = (x.length > 1 ? "." + x[1] : "");
    rgx = /(\d+)(\d{3})/;
    while (rgx.test(x1)) {
      x1 = x1.replace(rgx, "$1" + "," + "$2");
    }
    return x1 + x2;
  };

  $(document).ready(function() {
    $('#stripe_cc_owner').val($('#id_billing_name').val());
    if (window.account_type === 'personal') {
      $('#license_count').html('1');
      $('#license_cost').html('$5.00');
    }
    $('#checkout_submit').click(function(e) {
      return processForm(e);
    });
    $('#checkout_payment').submit(function(e) {
      return processForm(e);
    });
    $('#id_last_name').focusout(function() {
      var billing_name_input, cc_name_input, first_name;
      first_name = $('#id_first_name');
      if (first_name.val() === '') {
        return false;
      }
      billing_name_input = $('#id_billing_name');
      cc_name_input = $('#stripe_cc_owner');
      billing_name_input.val(first_name.val() + ' ' + $(this).val());
      return cc_name_input.val(first_name.val() + ' ' + $(this).val());
    });
    $('#id_quantity').change(function() {
      var count, monthly_div, multiplier;
      count = $(this).val();
      monthly_div = $('#sub_type_radio_0');
      if (monthly_div.attr('checked')) {
        multiplier = 5;
      } else {
        multiplier = 50;
      }
      $('#license_count').html(count);
      return $('#license_cost').html('$' + numberFormat(count * multiplier) + '.00 ');
    });
    return $('.sub_type').change(function() {
      var current_quantity;
      $('#price_type_header').html($(this).val());
      if (window.account_type === 'enterprise') {
        $('#license_count').html('0');
        $('#license_cost').html('$0.00');
      } else {
        $('#license_count').html('1');
        if ($(this).val() === 'yearly') {
          $('#license_cost').html('$50.00');
        } else {
          $('#license_cost').html('$5.00');
        }
      }
      current_quantity = $('#id_quantity').val();
      if (current_quantity !== '') {
        return $('#id_quantity').val('');
      }
    });
  });

}).call(this);
