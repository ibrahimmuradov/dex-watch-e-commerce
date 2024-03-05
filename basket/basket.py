from .models import Basket
from django.db.models import Sum
from django.contrib.auth import get_user_model
from store.models import Watch
from store.models import Coupon

Users = get_user_model()

class Basket_Proc:
    def __init__(self, request):
        self.session = request.session
        self.user = request.user

    def list_basket(self):
        basket = {}

        # Checking if cart data exists in model or session
        if self.user.is_authenticated:
            basket_items = Basket.objects.filter(user__username=self.user.username)
            # to use watch and cart data separately, add them to the dictionary
            basket = {basket.watch: basket for basket in basket_items}
        elif 'cart_datas' in self.session:
            session = self.session['cart_datas']
            basket = {Watch.objects.get(id=id_, stock__gte=1): session[id_] for id_ in session.keys()}

        return basket

    def add_to_basket(self, watch, qty):
        data = {'image': watch.watchimage_set.first().image.url,
                'name': watch.name,
                'quantity': qty
                }

        total_price = watch.total_price().get(id=watch.id).total_price

        if self.user.is_authenticated:
            get_user = Users.objects.get(username=self.user.username)

            basket_obj = Basket.objects.create(user=get_user,
                                  watch=watch,
                                  quantity=qty,
                                  total_price=float(total_price)*float(qty))

            data['total_price'] = basket_obj.total_price
        else:
            if 'cart_datas' not in self.session:
                self.session['cart_datas'] = {}

            watch_id = str(watch.id)

            if watch_id in self.session['cart_datas']:
                # Watch is already in the basket session, update quantity and total price
                existing_watch_data = self.session['cart_datas'][watch_id]
                existing_watch_data['quantity'] = int(qty)
                existing_watch_data['total_price'] = float(watch.total_price().get(id=watch.id).total_price) * int(qty)
            else:
                # Watch is not in the basket session, add it
                total_price = float(watch.total_price().get(id=watch.id).total_price) * int(qty)

                cart_data = self.session['cart_datas']

                datas = {watch_id: {
                    'name': watch.name,
                    'quantity': int(qty),
                    'total_price': total_price
                }}

                cart_data.update(datas)

                self.session['cart_datas'] = cart_data

            data['total_price'] = total_price

        return data

    def update_basket(self, watch, qty):
        # Updating the quantity of watch in the cart on the quantity of request
        if self.user.is_authenticated:
            if Basket.objects.filter(user__username=self.user.username, watch=watch).exists():
                get_basket = Basket.objects.get(user__username=self.user.username, watch=watch)
                get_basket.quantity = qty
                get_basket.total_price = float(qty) * float(watch.total_price().get(id=watch.id).total_price)
                get_basket.save()
        else:
            if 'cart_datas' in self.session:
                self.session['cart_datas'][str(watch.id)]['quantity'] = qty
                self.session['cart_datas'][str(watch.id)]['total_price'] = float(qty) * float(watch.total_price().get(id=watch.id).total_price)
                self.session.save()

    def __len__(self):
        # get count of watch in cart
        if self.user.is_authenticated:
            return Basket.objects.filter(user__username=self.user.username).count()
        return len(self.session['cart_datas']) if 'cart_datas' in self.session else 0

    def subtotal(self):
        subtotal = 0

        if self.user.is_authenticated:
            subtotal = Basket.objects.filter(user__username=self.user.username).aggregate(Sum('total_price'))['total_price__sum']
        elif 'cart_datas' in self.session:
            subtotal = sum(watch['total_price'] for watch in self.session['cart_datas'].values())

        return subtotal if subtotal else 0

    def total_amount(self):
        total_amount = self.subtotal() + 50 if self.subtotal() else 0

        # Calculating the total price depending on whether the user has a coupon or not
        if Coupon.objects.filter(user__username=self.user.username).exists():
            get_coupon = Coupon.objects.get(user__username=self.user.username)
            basket = Basket_Proc(self)
            coupon_disc = round((get_coupon.discount_rate * basket.subtotal()) / 100, 2)

            total_amount -= coupon_disc

        return round(total_amount, 2)

    def coupon_disc(self):
        coupon_dis = None

        if Coupon.objects.filter(user__username=self.user.username, access="Inaccessible"):
            coupon_dis = Coupon.objects.get(user__username=self.user.username, access="Inaccessible")

        return coupon_dis

    def delete_from_basket(self, id):
        # Deleting the watch matching the ID from the cart
        if self.user.is_authenticated:
            if Basket.objects.filter(watch__id=id, user__username=self.user.username).exists():
                Basket.objects.get(watch__id=id, user__username=self.user.username).delete()
        elif 'cart_datas' in self.session:
            del self.session['cart_datas'][id]
            self.session.save()

    def clear_basket(self):
        # clearing watches in cart
        if self.user.is_authenticated:
            Basket.objects.all().delete()
        elif 'cart_datas' in self.session:
            del self.session['cart_datas']
