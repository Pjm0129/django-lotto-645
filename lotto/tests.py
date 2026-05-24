from django.test import TestCase
from django.contrib.auth.models import User

from .models import Ticket, Draw, WinningResult
from .services import (
    generate_lotto_numbers,
    generate_draw_numbers,
    calculate_rank,
)

# AI로 생성한 테스트 코드

class LottoServiceTest(TestCase):
    def test_generate_lotto_numbers(self):
        numbers = generate_lotto_numbers()

        self.assertEqual(len(numbers), 6)
        self.assertEqual(len(set(numbers)), 6)
        self.assertTrue(all(1 <= number <= 45 for number in numbers))

    def test_generate_draw_numbers(self):
        main_numbers, bonus_number = generate_draw_numbers()

        self.assertEqual(len(main_numbers), 6)
        self.assertEqual(len(set(main_numbers)), 6)
        self.assertTrue(all(1 <= number <= 45 for number in main_numbers))
        self.assertTrue(1 <= bonus_number <= 45)
        self.assertNotIn(bonus_number, main_numbers)

    def test_first_rank(self):
        match_count, bonus_match, rank, prize_amount = calculate_rank(
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            7,
        )

        self.assertEqual(match_count, 6)
        self.assertFalse(bonus_match)
        self.assertEqual(rank, "1등")
        self.assertEqual(prize_amount, 100000000)

    def test_second_rank(self):
        match_count, bonus_match, rank, prize_amount = calculate_rank(
            [1, 2, 3, 4, 5, 7],
            [1, 2, 3, 4, 5, 6],
            7,
        )

        self.assertEqual(match_count, 5)
        self.assertTrue(bonus_match)
        self.assertEqual(rank, "2등")


class LottoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass1234"
        )

    def test_ticket_creation(self):
        ticket = Ticket.objects.create(
            user=self.user,
            round_no=1,
            numbers=[1, 2, 3, 4, 5, 6],
            pick_type="MANUAL",
            price=1000,
        )

        self.assertEqual(ticket.user.username, "testuser")
        self.assertEqual(ticket.round_no, 1)
        self.assertEqual(ticket.pick_type, "MANUAL")

    def test_winning_result_creation(self):
        ticket = Ticket.objects.create(
            user=self.user,
            round_no=1,
            numbers=[1, 2, 3, 4, 5, 6],
            pick_type="AUTO",
            price=1000,
        )

        draw = Draw.objects.create(
            round_no=1,
            numbers=[1, 2, 3, 4, 5, 6],
            bonus_number=7,
        )

        result = WinningResult.objects.create(
            ticket=ticket,
            draw=draw,
            match_count=6,
            bonus_match=False,
            rank="1등",
            prize_amount=100000000,
        )

        self.assertEqual(result.rank, "1등")
        self.assertEqual(result.prize_amount, 100000000)
