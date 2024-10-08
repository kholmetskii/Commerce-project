from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>/", views.view_listing, name="view_listing"),
    path('listing/<int:listing_id>/toggle_watchlist/', views.toggle_watchlist, name='toggle_watchlist'),
    path("watchlist", views.watchlist, name="watchlist"),
    path('listing/<int:listing_id>/make_bid/', views.make_bid, name='make_bid'),
    path('listing/<int:listing_id>/make_comment/', views.make_comment, name='make_comment'),
    path('listing/<int:listing_id>/toggle_listing/', views.toggle_listing, name='toggle_listing')
]