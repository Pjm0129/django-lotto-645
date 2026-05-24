import random

# 6개의 1~45랜덤 숫자를 중복 없이 생성하는 함수
def generate_lotto_numbers():
    return sorted(random.sample(range(1, 46), 6))

# 당첨 번호 6개 + 보너스 번호를 생성하는 함수
def generate_draw_numbers():
    numbers = random.sample(range(1, 46), 7)
    main_numbers = sorted(numbers[:6])
    bonus_number = numbers[6]
    return main_numbers, bonus_number

# 구매 번호와 당첨 번호를 비교하여 등수와 당첨금을 계산하는 함수
def calculate_rank(ticket_numbers, draw_numbers, bonus_number):
    match_count = len(set(ticket_numbers) & set(draw_numbers))
    bonus_match = bonus_number in ticket_numbers

    if match_count == 6:
        return match_count, bonus_match, "1등", 2000000000
    elif match_count == 5 and bonus_match:
        return match_count, bonus_match, "2등", 50000000
    elif match_count == 5:
        return match_count, bonus_match, "3등", 1000000
    elif match_count == 4:
        return match_count, bonus_match, "4등", 50000
    elif match_count == 3:
        return match_count, bonus_match, "5등", 5000
    else:
        return match_count, bonus_match, "낙첨", 0
