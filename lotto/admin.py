from django.contrib import admin
from .models import Ticket, Draw, WinningResult


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "round_no", "numbers", "pick_type", "price", "created_at")
    list_filter = ("round_no", "pick_type", "created_at")
    search_fields = ("user__username",)


@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    list_display = ("id", "round_no", "numbers", "bonus_number", "created_at")
    list_filter = ("round_no", "created_at")


@admin.register(WinningResult)
class WinningResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "ticket",
        "draw",
        "match_count",
        "bonus_match",
        "rank",
        "prize_amount",
        "created_at",
    )
    list_filter = ("rank", "draw", "created_at")