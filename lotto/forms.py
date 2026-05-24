from django import forms


class TicketPurchaseForm(forms.Form):
    PICK_TYPE_CHOICES = [
        ("AUTO", "자동"),
        ("MANUAL", "수동"),
    ]

    pick_type = forms.ChoiceField(
        choices=PICK_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial="AUTO",
        label="구매 방식"
    )

    num1 = forms.IntegerField(min_value=1, max_value=45, required=False, label="번호 1")
    num2 = forms.IntegerField(min_value=1, max_value=45, required=False, label="번호 2")
    num3 = forms.IntegerField(min_value=1, max_value=45, required=False, label="번호 3")
    num4 = forms.IntegerField(min_value=1, max_value=45, required=False, label="번호 4")
    num5 = forms.IntegerField(min_value=1, max_value=45, required=False, label="번호 5")
    num6 = forms.IntegerField(min_value=1, max_value=45, required=False, label="번호 6")

    def clean(self):
        cleaned_data = super().clean()
        pick_type = cleaned_data.get("pick_type")

        if pick_type == "MANUAL":
            numbers = [
                cleaned_data.get("num1"),
                cleaned_data.get("num2"),
                cleaned_data.get("num3"),
                cleaned_data.get("num4"),
                cleaned_data.get("num5"),
                cleaned_data.get("num6"),
            ]

            if None in numbers:
                raise forms.ValidationError("수동 구매 시 번호 6개를 모두 입력해야 합니다.")

            if len(set(numbers)) != 6:
                raise forms.ValidationError("중복되지 않는 번호 6개를 입력해야 합니다.")

            cleaned_data["numbers"] = sorted(numbers)

        return cleaned_data