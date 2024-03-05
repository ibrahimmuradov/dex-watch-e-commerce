from django import template
from store.models import Coupon


register = template.Library()

@register.simple_tag(takes_context=True)
def coupon_discount(context):
    request = context['request']

    coupon_disc = 0

    if Coupon.objects.filter(user__username=request.user.username, access="Inaccessible").exists():
        coupon_disc = Coupon.objects.get(user__username=request.user.username, access="Inaccessible").coupon_discount(request)

    return coupon_disc