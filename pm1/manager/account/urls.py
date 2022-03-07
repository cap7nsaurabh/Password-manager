from django.urls import path,re_path
from account import views
app_name='account'
urlpatterns=[
path('signup/',views.signup_view,name='signup'),
path('login/',views.login_view,name='login'),
path('logout/',views.logout_view,name='logout'),
path('dashboard/',views.dashboard,name='dashboard'),
path('view_cards/',views.card_view,name='view_cards'),
path('entercard/',views.cardform,name='cardform'),
path('entry/',views.add_entry,name='pass_entry'),
path('listentry/',views.list_viewp,name='list_pass'),
path('pass/<slug:slug>/',views.detailp_view,name='pass_detail_view'),
path('card/<slug:slug>/',views.card_detail_view,name='card_detail_view'),
path('meetingsfill/',views.meeting_fill,name='view_meetings'),
path('listmeeting/',views.listmeet,name='list_meet'),
path('meets/<slug:slug>/',views.meetdetail,name='meet_detail'),
path('card/<slug:slug>/delete',views.delc,name='delete_card'),
path('pass/<slug:slug>/delete',views.delp,name='delete_pass'),
path('meet/<slug:slug>/delete',views.delm,name='delete_meet'),

]