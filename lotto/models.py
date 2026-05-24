from django.db import models
from django.contrib.auth.models import User

# 사용자가 구매한 복권 정보를 저장하는 모델
class Ticket(models.Model):
    PICK_TYPE_CHOICES = [
        ("MANUAL", "수동"),
        ("AUTO", "자동"),
    ]

    # 구매자 정보
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round_no = models.PositiveIntegerField(verbose_name="회차")
    numbers = models.JSONField(verbose_name="선택 번호")
    pick_type = models.CharField(
        max_length=10,
        choices=PICK_TYPE_CHOICES,
        verbose_name="구매 방식"
    )
    price = models.PositiveIntegerField(default=1000, verbose_name="가격")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="구매일")

    def __str__(self):
        return f"{self.user.username} - {self.round_no}회차 - {self.numbers}"

# 관리자가 실행한 추첨 결과를 저장하는 모델
class Draw(models.Model):
    round_no = models.PositiveIntegerField(unique=True, verbose_name="회차")
    numbers = models.JSONField(verbose_name="당첨 번호")
    bonus_number = models.PositiveIntegerField(verbose_name="보너스 번호")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="추첨일")

    def __str__(self):
        return f"{self.round_no}회차 당첨번호 {self.numbers} + {self.bonus_number}"

# 구매한 복권과 추첨 결과를 비교한 당첨 결과 모델
class WinningResult(models.Model):
    # 당첨 판정 대상 복권
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    # 해당 회차의 추첨 결과
    draw = models.ForeignKey(Draw, on_delete=models.CASCADE)
    match_count = models.PositiveIntegerField(verbose_name="일치 개수")
    bonus_match = models.BooleanField(default=False, verbose_name="보너스 일치")
    rank = models.CharField(max_length=20, verbose_name="등수")
    prize_amount = models.PositiveIntegerField(default=0, verbose_name="당첨금")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="확인일")

    def __str__(self):
        return f"{self.ticket.user.username} - {self.rank}"