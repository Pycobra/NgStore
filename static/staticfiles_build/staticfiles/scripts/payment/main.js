var stripe=Stripe('')

var elem = document.getElementById('submit');
clientsecret = elem.getAttribute('data-secret');

var elements = stripe.elements();
var style = {
    base: {
        color: "#000",
        lineHeight: "2.4",
        fontSize: "16px"
    }
};
var card = elements.create('card', {style:style});
card.mount('#card-element');

card.on('change', function(event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
        displayError.textContent=event.error.message;
        $('#card-errors').addClass('alert alert-info');
    } else {
        displayError.textContent='';
        $('#card-errors').removeClass('alert alert-info');
    }
})

var elem = document.getElementById('payment-form');
form.addEventListener('submit', function(ev)
    ev.preventDefault();

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/orders/add_checkout/"
        data: {
            order_key: clientsecret,
            custName: document.getElementById('custName').value;
            custAdd: document.getElementById('custAdd').value;
            custAdd2: document.getElementById('custAdd2').value;
            country: document.getElementById('country').value;
            city: document.getElementById('city').value;
            email: document.getElementById('email').value;
            postCode: document.getElementById('postCode').value;
            csrfmiddlewaretoken: CSRF_TOKEN,
            action: "post",
        },
        success: function (json) {
            console.log(json.success)

            stripe.confirmCardPayment(clientsecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        address:{
                            line1:custAdd,
                            line2:custAdd2
                        },
                        name: custName
                    },
                }
            }).then(function(result) {
                if (result.error){
                    console.log('payment error');
                    console.log(result.error.message);
                } else {
                    if (result.paymentIntent.status === 'succeded') {
                        console.log('payment processed')
                        window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
                    }
                }
            });
        },
        error: function (xhr, errmsg, err) {

        },
    });
)

/* document.addEventListener('DOMContentLoaded', {} => {
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
    if ($navbarBurgers.length > 0){
        $navbarBurgers.forEach( el => {
            el.addEventListener('click', {} => {
                const target = el.dataset.target;
                const starget = document.getElementById(target);

                el.classList.toggle('is-active');
                starget.classList.toggle('is-active');
            });
        });
    }
}) */