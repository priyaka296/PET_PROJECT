from django.urls import path
from petapp import views
from pet import settings
from django.conf.urls.static import static





urlpatterns = [
    path('index/', views.index),
    path('base/', views.base),
    path('Booking/', views.Booking),
    path('viewcart/', views.viewcart),
    path('Pet_details/<pid>', views.Pet_details),
    path('catfilter/<cv>', views.catfilter),
    path('about/',views.about),
    path('contact/',views.contact),
     path('addtocart/<pid>',views.addtocart),
    path('remove/<uid>', views.remove),
    path('footer/',views.footer),
    path('header/',views.header),
    path('login/',views.ulogin),
    path('logout/',views.ulogout),
    path('register/',views.register),
    path('services/',views.services),
    path('Price/',views.Price),
    path('updateqty/<qv>/<cid>', views.updateqty), 
    path('placeorder/',views.placeorder),
    path('makepayment/',views.makepayment),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
