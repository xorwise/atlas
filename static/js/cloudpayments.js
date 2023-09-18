const serverError = document.getElementById('serverError')
function pay(amount, transaction_id) {
    var widget = new cp.CloudPayments();
        widget.pay('auth', // или 'charge'
           { //options
               publicId: publicID, //id из личного кабинета
               description: 'Пополнение баланса на atlas-book.com', //назначение
               amount: parseFloat(amount), //сумма
               currency: 'RUB', //валюта
               email: email, //email плательщика (необязательно)
               skin: "modern", //дизайн виджета (необязательно)
               autoClose: 3, //время в секундах до авто-закрытия виджета (необязательный)
               data: {
                   myProp: 'myProp value'
               },
               configuration: {
                   common: {
                       successRedirectUrl: "https://{ваш сайт}/success", // адреса для перенаправления 
                       failRedirectUrl: "https://{ваш сайт}/fail"        // при оплате по Tinkoff Pay
                   }
               },
           },
           {
               onSuccess: function (options) { // success
                   //действие при успешной оплате
                //    console.log(options)
               },
               onFail: function (reason, options) { // fail
                    console.log(reason)
                   //действие при неуспешной оплате
               },
               onComplete: function (paymentResult, options) { //Вызывается как только виджет получает от api.cloudpayments ответ с результатом транзакции.
                    return fetch('/api/payment', {
                        method: 'PATCH',
                        body: JSON.stringify({
                            id: transaction_id,
                            success: paymentResult.success
                        }),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }).then((res) => {
                        console.log(res)
                        if(res.ok) {
                            return res.json()
                        } else {
                            return res.text()
                        }
                    }).then((data) => {
                        serverError.innerText = data
                    })
               }
           }
       )
   };

const button = document.getElementById('paymentBtn')
const input = document.getElementById('amountInput')

button.addEventListener('click', () => {
    return fetch('/api/payment', {
        method: 'POST',
        body: JSON.stringify({
            amount: parseFloat(input.value)
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then((res) => {
        if(res.ok) {
            return res.json()
        } else {
            const response = res.text()
            serverError.innerText = response
            return Promise.reject()
        }
    }).then((data) => pay(input.value, data.id))
    
})