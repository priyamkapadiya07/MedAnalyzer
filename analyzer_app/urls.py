from django.contrib import admin
from django.urls import path,include
from analyzer_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_report, name='upload'),
    path('report/<int:report_id>/', views.report_detail, name='report_detail'),
    path('reports/', views.report_history, name='reports'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete/<int:id>', views.delete_view, name='delete'),
    path('QandA/', views.QuestionAnswer, name='Q&A'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('clear_chat/', views.clear_chat, name='clear_chat'),
    path('report/<int:report_id>/<str:action>/', views.handle_report, name='handle_report'),
]
