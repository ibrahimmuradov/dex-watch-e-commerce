from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Choice, Watch, WatchReview
from order.models import Order, OrderItem, Country
from basket.models import Basket
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .forms import ReviewForm
from services.filter import WatchFilter
from services.choices import GENDER
from services.filter import WatchFilter
from django.contrib import messages


Users = get_user_model()


def index(request):
    # get the 3 objects with the most views
    header_watches = Watch.objects.filter(status='Active', discount__gt=0).order_by('-view_count')[:3]
    trend_watch = Watch.total_price().order_by('-view_count').first()

    context = {
        'header_watches': header_watches,
        'trend_watch': trend_watch,
        'first_watch': Watch.total_price().first(),
    }
    return render(request, 'store/index.html', context)


def shop(request):
    context = {}

    watches = Watch.total_price().order_by("-created_at")

    watch_filter = None

    if request.method == "GET":
        # Sending a request to the filter function of the WatchFilter class for filtering
        watch_filter = WatchFilter().filter(request)

        watches = watch_filter['watches']

    basket_status = []

    # Collecting the id values of the watches in the user's cart into a list
    for watch in watches:
        if request.user.is_authenticated:
            if Basket.objects.filter(user__username=request.user.username, watch=watch).exists():
                basket_status.append(watch.id)
        else:
            if 'cart_datas' in request.session and str(watch.id) in request.session['cart_datas']:
                basket_status.append(watch.id)

    total_watch = watches.count()

    context["watches"] = watches
    context["watches_filter"] = watch_filter['filters']
    context["basket_status"] = basket_status
    context["categories"] = Category.objects.all()
    context["styles"] = Choice.objects.filter(type="Style")
    context["movements"] = Choice.objects.filter(type="Movement")
    context["functionalities"] = Choice.objects.filter(type="Functionality")
    context["materials"] = Choice.objects.filter(type="Material")
    context["colors"] = Choice.objects.filter(type="Color")
    context["genders"] = GENDER
    context["total_watch"] = total_watch


    return render(request, 'store/shop.html', context)


def details(request, id):
    get_watch = get_object_or_404(Watch.total_price(), id=id)

    get_watch.view_count += 1
    get_watch.save()

    # Checking that the watch is in the basket
    cart_status = 'cart_datas' in request.session and str(get_watch.id) in request.session['cart_datas'] if True else False

    if request.user.is_authenticated:
        cart_status = Basket.objects.filter(user__username=request.user.username, watch=get_watch).exists()


    get_reviews = WatchReview.objects.filter(watch=get_watch)

    reviews = {}

    # add reviews and review ratings to a dictionary to list
    for review in get_reviews:
        reviews[review] = range(review.rating)

    review_form = ReviewForm()

    # create review
    if request.POST:
        review_form = ReviewForm(data=request.POST, request=request, id=id)

        if review_form.is_valid():
            review = review_form.cleaned_data['review']
            rating = review_form.cleaned_data['rating']

            get_user = Users.objects.get(username=request.user.username)

            WatchReview.objects.create(
                user=get_user,
                watch=get_watch,
                review=review,
                rating=rating
            )

            return redirect(request.build_absolute_uri())

    context = {
        "watch": get_watch,
        "reviews": reviews,
        "average_range_rating": range(int(round(get_watch.rating(), 1))) if get_watch.rating() else None,
        "review_form": review_form,
        "cart_status": cart_status,
        "related_watches": Watch.objects.exclude(id=get_watch.id).filter(category_id=get_watch.category.id),
    }

    return render(request, 'store/product-details.html', context)


def wishlist(request):
    data = {}

    get_watch = get_object_or_404(Watch, id=int(request.POST.get("watchID")))

    if get_watch.status == "Active":
        if request.user.is_authenticated:
            get_user = get_object_or_404(Users, username=request.user)

            # check if the watch is in the user's wish list
            if get_user in get_watch.wishlist.all():
                get_watch.wishlist.remove(get_user)
                data["response"] = False
            else:
                get_watch.wishlist.add(get_user)
                data["response"] = True

        else:
            data["error"] = "Please log in to your user account"
    else:
        data["error"] = "Error"

    return JsonResponse(data)


def delete_review(request):
    data = {}

    get_review = get_object_or_404(WatchReview, id=(int(request.POST.get('reviewID'))))

    if request.user.is_authenticated:
        # check if user has review at current watch
        if OrderItem.objects.filter(user=request.user, watch__id=get_review.watch.id).exists():
            get_review.delete()
            data["response"] = True
        else:
            data["response"] = False
    else:
        data["error"] = "Please log in to your user account"

    return JsonResponse(data)

