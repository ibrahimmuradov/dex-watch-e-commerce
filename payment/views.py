from django.shortcuts import render, redirect, get_object_or_404
from order.models import Order, OrderItem, Coupon
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Payment
from .forms import PaymentForm
from basket.basket import Basket_Proc
from django.urls import reverse_lazy

@login_required
def payment(request, key):
    try:
        order = get_object_or_404(Order, user__username=request.user.username, verification_key=key)
    except Http404:
        return redirect('basket:cart')

    if key == order.verification_key:
        payment_form = PaymentForm()

        # save payment information
        if request.method == "POST":
            payment_form = PaymentForm(data=request.POST)

            if payment_form.is_valid():
                Payment.objects.create(
                    name=payment_form.cleaned_data['name'],
                    number=payment_form.cleaned_data['number'],
                    code=payment_form.cleaned_data['code'],
                    date=request.POST.get('date'),
                    order=order,
                )

                order.billing_status = True

                # The stock of watches decreases according to the quantities purchased
                for order_item in order.orderitem_set.all():
                    order_item.watch.stock -= order_item.quantity
                    order_item.watch.save()

                order.save()

                basket = Basket_Proc(request)

                # Purchased watches are deleted from the cart
                basket.clear_basket()

                # The coupon used for payment is deactivated
                if basket.coupon_disc():
                    get_coupon = Coupon.objects.get(user__username=request.user.username)
                    get_coupon.user = None
                    get_coupon.status = 'Deactivate'
                    get_coupon.save()

                return redirect(reverse_lazy("payment:invoice", kwargs={"key": order.verification_key}))


        context = {
            "order": order,
            "payment_form": payment_form,
        }

        return render(request, 'payment/payment.html', context)
    else:
        return redirect('watch:shop')

@login_required
def invoice(request, key):
    try:
        order = get_object_or_404(Order, user__username=request.user.username, verification_key=key)
    except Http404:
        return redirect('basket:cart')

    # The verification code is deleted once the payment transaction is completed
    if key == order.verification_key:
        order.verification_key = None
        order.save()

        context = {
            "order": order,
            "order_item": OrderItem.objects.filter(order=order)
        }

        return render(request, 'payment/invoice.html', context)
    else:
        return redirect('basket:cart')