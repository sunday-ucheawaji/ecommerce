from django.shortcuts import redirect
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# This is your test secret API key.
stripe.api_key = 'sk_test_51M1BvtESeOfTGQ8nrACOvoHmcEFeS4vIvxhCISfskv9uU7ScEv1ALpHKvOxNdXRskW5b86apJlMk0dgzuWF0KOK900TkYzC6Tc'


YOUR_DOMAIN = 'http://localhost:3000'

class CreatePaymentView(APIView):
    authentication_classes = []
    permission_classes = []
    # serializer_class = VerifySerializer

    def post(self, request):
        # serializer = self.serializer_class(data=request.data)
        # if serializer.is_valid():
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data":{
                        "currency": "usd",
                        "unit_amount": 20 * 100,
                        "product_data": {
                            "name": "abc",
                            "description": "test description",

                        }

                        },
                        "quantity": 2,
                    },
                ],
                payment_method_types=["card",],
                mode='payment',
                success_url=YOUR_DOMAIN + '?success=true',
                cancel_url=YOUR_DOMAIN + '?canceled=true',
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return redirect(checkout_session.url)

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





