from core.celery import app


@app.task
def del_product_in_cart(pk):
    from cart.models import BasketProductModel
    if obj := BasketProductModel.objects.filter(pk=pk):
        obj.first().delete()
    return '204_NO_CONTENT'
