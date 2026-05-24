from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # 메인 페이지
    path("", views.home, name="home"),

    # 사용자 인증 관련 URL
    path("signup/", views.signup_view, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="lotto/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),

    # 사용자 기능 URL
    path("buy/", views.buy_ticket, name="buy_ticket"),
    path("my-tickets/", views.my_tickets, name="my_tickets"),
    path("my-results/", views.my_results, name="my_results"),

    # 관리자 기능 URL
    path("manager/", views.admin_dashboard, name="admin_dashboard"),
    path("manager/draw/", views.draw_lotto, name="draw_lotto"),
    path("manager/winners/", views.winners, name="winners"),
]
