from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, UserEditForm, AddressEditForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from .models import UserBase, Address
from store.models import Watch
from order.models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth import login as log_in
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from services.generator import Generator
from django.db.models import Sum
from django.http import Http404


Users = get_user_model()


def login(request):
    return render(request, 'account/login.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        register_form = UserRegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.email = register_form.cleaned_data['email']
            user.set_password(register_form.cleaned_data['password'])
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Account Activation Link'
            message = render_to_string(
                 'account/account-activation-email.html',
                 {
                   'user': user,
                   'domain': current_site.domain,
                   'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                   'token': account_activation_token.make_token(user),
                 }) # return a template to a string
            user.email_user(subject=subject, message=message)

            success = 'Your account has been created. \n To activate your account, verify your account using the activation link sent to your e-mail address.'

            return render(request, 'account/register.html', {'data': success})

    else:
        register_form = UserRegisterForm()

    return render(request, 'account/register.html', {'form': register_form})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        log_in(request, user)

        return redirect('/')
    else:
        return render(request, 'account/activation-invalid.html')


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    login_url = 'account:login'

    def get_success_url(self):
        get_user = Users.objects.get(username=self.request.user.username)
        get_user.token_key = Generator.create_key(15, Users)
        get_user.save()

        return f'{reverse_lazy("account:password-success", kwargs={"token": get_user.token_key})}'

@login_required
def password_success(request, token):
    get_user = Users.objects.get(username=request.user.username)
    if token == get_user.token_key:
        get_user.token_key = None
        get_user.save()
        return render(request, "account/password-change-success.html")
    else:
        return redirect('account:dashboard')


@login_required
def dashboard(request):
    # orders tab
    orders = Order.objects.filter(user__username=request.user.username, billing_status=True)

    order_item = {order: order.orderitem_set.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0 for order in orders}

    # wishlist tab
    wishlist_watches = {}

    wishlist = Watch.objects.exclude(status='Deactivate', stock__lte=0).filter(wishlist__in=[request.user])

    for wish in wishlist:
        wishlist_watches[wish] = wish.total_price().get(id=wish.id)

    get_address = Address.objects.get(user=request.user) if Address.objects.filter(user=request.user) else None

    edit_form = UserEditForm(instance=request.user)
    address_form = AddressEditForm(instance=get_address)

    if request.method == "POST":
        # user tab
        if 'usereditform' in request.POST:
            edit_form = UserEditForm(instance=request.user, data=request.POST, files=request.FILES, request=request)

            if edit_form.is_valid():
                edit_form.save()

                return redirect('account:dashboard')

        # address tab
        elif 'addresseditform' in request.POST:
            address_form = AddressEditForm(instance=get_address, data=request.POST, request=request)

            if address_form.is_valid():
                address_obj = address_form.save(commit=False)
                address_obj.user = request.user
                address_obj.save()

                return redirect('account:dashboard')

    context = {
        'orders': order_item,
        'edit_form': edit_form,
        'address_form': address_form,
        'wishlist': wishlist_watches,
    }

    return render(request, 'account/dashboard.html', context)


@login_required
def view_invoice(request, id):
    try:
        order = get_object_or_404(Order, user__username=request.user.username, id=id)
    except Http404:
        return redirect('basket:cart')

    for orderitem in OrderItem.objects.filter(order=order):
        print('total priceee  ', orderitem.watch.get_total_price())

    context = {
        "order": order,
        "order_item": OrderItem.objects.filter(order=order)
    }

    return render(request, 'account/view_invoice.html', context)