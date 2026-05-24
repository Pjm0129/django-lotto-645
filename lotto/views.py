from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .forms import TicketPurchaseForm
from .models import Draw, Ticket
from .services import generate_lotto_numbers

# 메인 페이지를 보여주는 view
def home(request):
    return render(request, "lotto/home.html")

# 회원가입 view
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "회원가입이 완료되었습니다.")
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "lotto/signup.html", {"form": form})

# 현재 구매해야 할 다음 회차 번호를 계산하는 함수
def get_next_round():
    latest_draw = Draw.objects.order_by("-round_no").first()

    if latest_draw is None:
        return 1

    return latest_draw.round_no + 1

# 로그인한 사용자가 복권을 구매하는 view
@login_required
def buy_ticket(request):
    if request.method == "POST":
        form = TicketPurchaseForm(request.POST)

        if form.is_valid():
            pick_type = form.cleaned_data["pick_type"]
            round_no = get_next_round()

            if pick_type == "AUTO":
                numbers = generate_lotto_numbers()
            else:
                numbers = form.cleaned_data["numbers"]

            Ticket.objects.create(
                user=request.user,
                round_no=round_no,
                numbers=numbers,
                pick_type=pick_type,
                price=1000,
            )

            messages.success(
                request,
                f"{round_no}회차 복권 구매가 완료되었습니다. 선택 번호: {numbers}"
            )

            return redirect("my_tickets")
    else:
        form = TicketPurchaseForm()

    return render(request, "lotto/buy.html", {"form": form})

# 로그인한 사용자의 복권 구매 내역을 보여주는 view
@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "lotto/my_tickets.html", {
        "tickets": tickets
    })

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum

from .models import WinningResult
from .services import generate_draw_numbers, calculate_rank

# 관리자에게 판매 내역을 보여주는 view
@staff_member_required
def admin_dashboard(request):
    total_tickets = Ticket.objects.count()
    total_sales = Ticket.objects.aggregate(total=Sum("price"))["total"] or 0

    sales_by_round = (
        Ticket.objects
        .values("round_no")
        .annotate(ticket_count=Count("id"), sales=Sum("price"))
        .order_by("-round_no")
    )

    return render(request, "lotto/admin_dashboard.html", {
        "total_tickets": total_tickets,
        "total_sales": total_sales,
        "sales_by_round": sales_by_round,
    })

# 해당 회차의 로또 추첨을 실행하는 view
@staff_member_required
def draw_lotto(request):
    latest_draw = Draw.objects.order_by("-round_no").first()
    next_round = 1 if latest_draw is None else latest_draw.round_no + 1

    if request.method == "POST":
        tickets = Ticket.objects.filter(round_no=next_round)

        if not tickets.exists():
            messages.error(request, f"{next_round}회차 구매 내역이 없어 추첨할 수 없습니다.")
            return redirect("draw_lotto")

        main_numbers, bonus_number = generate_draw_numbers()

        draw = Draw.objects.create(
            round_no=next_round,
            numbers=main_numbers,
            bonus_number=bonus_number,
        )

        for ticket in tickets:
            match_count, bonus_match, rank, prize_amount = calculate_rank(
                ticket.numbers,
                draw.numbers,
                draw.bonus_number,
            )

            WinningResult.objects.create(
                ticket=ticket,
                draw=draw,
                match_count=match_count,
                bonus_match=bonus_match,
                rank=rank,
                prize_amount=prize_amount,
            )

        messages.success(
            request,
            f"{next_round}회차 추첨 완료! 당첨번호: {main_numbers}, 보너스: {bonus_number}"
        )

        return redirect("winners")

    return render(request, "lotto/draw.html", {
        "next_round": next_round,
    })

# 관리자가 전체 당첨 결과를 확인하는 view
@staff_member_required
def winners(request):
    results = WinningResult.objects.select_related(
        "ticket",
        "ticket__user",
        "draw"
    ).order_by("-draw__round_no", "rank")

    return render(request, "lotto/winners.html", {
        "results": results,
    })

# 사용자가 당첨 결과를 확인하는 view
@login_required
def my_results(request):
    results = WinningResult.objects.select_related(
        "ticket",
        "draw"
    ).filter(ticket__user=request.user).order_by("-draw__round_no")

    return render(request, "lotto/my_results.html", {
        "results": results,
    })


from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum


@staff_member_required
def admin_dashboard(request):
    total_tickets = Ticket.objects.count()
    total_sales = Ticket.objects.aggregate(total=Sum("price"))["total"] or 0

    sales_by_round = (
        Ticket.objects
        .values("round_no")
        .annotate(ticket_count=Count("id"), sales=Sum("price"))
        .order_by("-round_no")
    )

    return render(request, "lotto/admin_dashboard.html", {
        "total_tickets": total_tickets,
        "total_sales": total_sales,
        "sales_by_round": sales_by_round,
    })
