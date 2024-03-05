from django.shortcuts import render, redirect
from basket.basket import Basket_Proc
from .models import Order, OrderItem
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from services.generator import Generator
from account.models import Address


@login_required
def checkout(request):
    basket = Basket_Proc(request)

    if basket.__len__() <= 0:
        # If the basket is empty, the user is directed to the shop page
        return redirect('watch:shop')
    else:
        if Address.objects.filter(user__username=request.user.username).exists():
            # If the user's current address information is registered in the database, an order object is created using that data
            address = Address.objects.get(user__username=request.user.username)

            if request.method == "POST":
                order = Order.objects.create(
                    invoice_id=int(Generator.create_id(8, Order)),
                    user=request.user,
                    first_name=address.first_name,
                    last_name=address.last_name,
                    company_name=address.company_name,
                    email=address.email,
                    address=address.address,
                    country=address.country,
                    city=address.city,
                    phone=address.phone,
                    postal_code=address.postal_code,
                    coupon_discount=basket.coupon_disc(),
                    coupon_discount_value=basket.coupon_disc().coupon_discount(request) if basket.coupon_disc() else None,
                    subtotal=basket.subtotal(),
                    total_paid=basket.total_amount(),
                    verification_key=Generator.order_key(20, Order),
                    billing_status=False,
                )

                for _, basket in basket.list_basket().items():
                    OrderItem.objects.create(
                        order=order,
                        watch=basket.watch,
                        user=request.user,
                        price=basket.total_price,
                        quantity=basket.quantity,
                    )

                return redirect(reverse_lazy("payment:payment", kwargs={"key": order.verification_key}))

            context = {
                'address': address
            }
        else:
            # If the user's current address information is not registered in the database, that user is asked to enter
            # address information and a new address and order object is created
            order_form = OrderForm()

            if request.method == "POST":
                order_form = OrderForm(data=request.POST, request=request)

                if order_form.is_valid():
                    order = Order.objects.create(
                        invoice_id=int(Generator.create_id(8, Order)),
                        user=request.user,
                        first_name=order_form.cleaned_data['first_name'],
                        last_name=order_form.cleaned_data['last_name'],
                        company_name=order_form.cleaned_data.get('company_name', None),
                        email=order_form.cleaned_data['email'],
                        address=order_form.cleaned_data['address'],
                        country=order_form.cleaned_data['country'],
                        city=order_form.cleaned_data['city'],
                        phone=order_form.cleaned_data['phone'],
                        postal_code=order_form.cleaned_data['postal_code'],
                        coupon_discount=basket.coupon_disc(),
                        coupon_discount_value=basket.coupon_disc().coupon_discount(request) if basket.coupon_disc() else None,
                        subtotal=basket.subtotal(),
                        total_paid=basket.total_amount(),
                        verification_key=Generator.order_key(20, Order),
                        billing_status=False,
                    )

                    Address.objects.create(
                        user=request.user,
                        first_name=order_form.cleaned_data['first_name'],
                        last_name=order_form.cleaned_data['last_name'],
                        company_name=order_form.cleaned_data.get('company_name', None),
                        email=order_form.cleaned_data['email'],
                        address=order_form.cleaned_data['address'],
                        country=order_form.cleaned_data['country'],
                        city=order_form.cleaned_data['city'],
                        phone=order_form.cleaned_data['phone'],
                        postal_code=order_form.cleaned_data['postal_code'],
                    )

                    for _, basket in basket.list_basket().items():
                        OrderItem.objects.create(
                            order=order,
                            watch=basket.watch,
                            user=request.user,
                            price=basket.total_price,
                            quantity=basket.quantity,
                        )

                    return redirect(reverse_lazy("payment:payment", kwargs={"key": order.verification_key}))

            context = {
                'order_form': order_form
            }

    return render(request, 'order/checkout.html', context)
