from django.db import transaction, IntegrityError
from rest_framework.response import Response

from cart.tasks import del_product_in_cart
from orderapp.tasks import send_email_success
from purse.models import PurseModel


@transaction.atomic
def pay_product(request, order, cart):
    try:
        user_wallet = PurseModel.objects.filter(user_id=request.user).first()
        user_wallet.money -= cart.total_cost
        user_wallet.save()
    except IntegrityError:
        return Response(data={'Error': 'недостаточно средств'})
    for item in cart.in_cart.all():
        try:
            item.product.stock -= item.quantity
            item.product.save()
        except IntegrityError:
            del_product_in_cart.apply_async((item.pk,), countdown=2)
            return Response(data={'Error': f'Количества {item.product} не достаточно'})

    send_email_success.delay(order.validated_data['email'])
    cart.in_cart.all().delete()
    order.save(paid=True)
    return Response(order.data, status=201, headers={'Paid': 'Successful'})
