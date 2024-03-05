from django.shortcuts import render, redirect
from django.http import JsonResponse
from store.models import Watch
from .basket import Basket_Proc
from .forms import CouponForm
from store.models import Coupon
from services.check_model import get_or_none

def cart(request):
    coupon_form = CouponForm()

    if request.method == "POST":
        if 'watch_id' in request.POST:
            get_id = request.POST.getlist('watch_id')

            get_watch = Watch.objects.filter(id__in=get_id)

            basket = Basket_Proc(request)

            # Updating the quantity of watch in the cart
            for watch in get_watch:
                quantity = request.POST.get(f'watch_quantity-{watch.id}')
                basket.update_basket(watch, quantity)

            return redirect('basket:cart')

        elif 'code' in request.POST:
            coupon_form = CouponForm(data=request.POST, request=request)

            if coupon_form.is_valid():
                get_code = coupon_form.cleaned_data.get('code')

                # activate user coupon code
                coupon_obj = Coupon.objects.get(code=get_code)
                coupon_obj.user = request.user
                coupon_obj.access = 'Inaccessible'
                coupon_obj.save()

                return redirect(request.build_absolute_uri())

    context = {
        'coupon_form': coupon_form,
        'coupon': get_or_none(Coupon, user__username=request.user.username)
    }

    return render(request, 'basket/cart.html', context)


def remove_coupon(request):
    if request.method == "POST":
        if Coupon.objects.filter(user__username=request.user.username, id=request.POST.get('id')).exists():
            get_coupon = Coupon.objects.get(id=request.POST.get('id'))

            # deactivate coupon
            get_coupon.user = None
            get_coupon.access = 'Accessible'
            get_coupon.save()

    return JsonResponse({"data": "success"})


def basket_add(request):
    data = {}

    if request.method == "POST":
        watch_id = request.POST.get('watchID')
        watch_qty = request.POST.get('watchQty')

        if Watch.objects.filter(id=watch_id).exists():
            get_watch = Watch.objects.get(id=watch_id)

            # Creating a new watch with watch id and quantity values
            basket = Basket_Proc(request)
            add_to_basket = basket.add_to_basket(get_watch, watch_qty)

            data['success'] = add_to_basket
        else:
            data['error'] = 'Watch not found'

    return JsonResponse(data)


def basket_delete(request):
    data = {}

    if request.method == 'POST':
        watch_id = request.POST.get('watchID')

        if Watch.objects.filter(id=watch_id).exists():
            basket = Basket_Proc(request)
            # Delete watch from cart using watch id
            basket.delete_from_basket(watch_id)

            data['success'] = {'stock': Watch.objects.get(id=watch_id).stock}
        else:
            data['error'] = 'Watch not found delete'

    return JsonResponse(data)


def subtotal(request):
    basket = Basket_Proc(request)
    # calculate subtotal
    get_subtotal = basket.subtotal()

    return JsonResponse({'subtotal': get_subtotal})