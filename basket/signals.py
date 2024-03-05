from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import get_user_model
from .basket import Basket_Proc
from .models import Basket
from store.models import Watch

Users = get_user_model()

@receiver(user_logged_in)
def user_loged_in_handler(sender, request, user, **kwargs):
    get_user = Users.objects.get(username=request.user)

    # Saving the watch in the session to the database when the user logs in to his account
    if 'cart_datas' in request.session:
        for watch_id, watch in request.session['cart_datas'].items():
            if not Basket.objects.filter(user=get_user, watch__id=watch_id).exists():
                get_watch = Watch.objects.get(id=watch_id)
                Basket_Proc.add_to_basket(request, get_watch, watch['quantity'])
        del request.session['cart_datas']