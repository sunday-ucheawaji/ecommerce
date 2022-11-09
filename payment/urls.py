from django.urls import path
from payment.views import CreatePaymentView 
 



urlpatterns =[
    path('create-checkout-session', CreatePaymentView.as_view(), name="payment"),
]