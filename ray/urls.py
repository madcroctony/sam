from django.urls import path
from . import views

app_name = 'ray'
b=views.Games()

urlpatterns = [
    #path('', index, name='index'),
    path('cot/', b.cot, name='cot'),
    path('ans/', b.ans, name='ans'),
    path('signup/', b.signup, name='signup'),
    path('login/', b.login, name='login'),
    path('all_logout', b.all_logout, name='all_logout'),
]
