from core.celery import app


@app.task
def del_product_in_cart(pk):
    from cart.models import BasketProductModel
    if queryset := BasketProductModel.objects.filter(pk=pk):
        queryset.first().delete()
    return '204_NO_CONTENT'
