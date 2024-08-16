$(document).ready(function() {
    $('#conversion-form').submit(function(e) {
        e.preventDefault();

        const fromCurrency = $('#from').val();
        const toCurrency = $('#to').val();
        const amount = $('#amount').val();

        $.ajax({
            url: '/convert',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ from: fromCurrency, to: toCurrency, amount: parseFloat(amount) }),
            success: function(response) {
                $('#result').text(`Конвертированная валюта: ${response.converted_amount}`);
            }
        });
    });
});
