from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        input_class = (
            "block w-full rounded-lg border border-slate-300 bg-white px-3 py-2.5 "
            "text-sm text-slate-900 shadow-sm outline-none transition "
            "placeholder:text-slate-400 focus:border-indigo-500 "
            "focus:ring-2 focus:ring-indigo-100"
        )

        for field in self.fields.values():
            field.widget.attrs["class"] = input_class


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
        )
