from django.urls import path

from . import views

urlpatterns = [

    # ********** paths that render page **********

    path('', views.index),
    path('quotes', views.quote_dashboard),
    path('user/<int:user_id>', views.user_quote),
    path('myaccount/<int:user_id>', views.edit_account),


    # ***** paths that redirect to render page *****


    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('add_author', views.add_author),
    path('like/<int:user_id>', views.like_quote),
    path('update/<int:user_id>', views.update),
    path('remove_quote/<int:user_id>', views.delete),

]
