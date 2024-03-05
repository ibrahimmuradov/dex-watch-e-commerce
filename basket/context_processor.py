from .basket import Basket_Proc
from store.models import Watch
from django.db.models import Max, Min
import math

def basket_context_processor(request):
    watches = Watch.total_price().order_by("-created_at")

    context = {
        "basket": Basket_Proc(request),
        "min_price": int(watches.aggregate(min_price=Min("total_price")).get("min_price")),
        "max_price": int(math.ceil(watches.aggregate(max_price=Max("total_price")).get("max_price"))),
    }

    return context