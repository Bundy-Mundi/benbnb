from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class LoggedOutOnlyView(UserPassesTestMixin):

    permission_denied_message = "Page Not Found"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect(reverse("cores:home"))


class LoggedInOnlyView(LoginRequiredMixin):
    def get_permission_denied_message(self):
        return "Can't go there"

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect(reverse("users:login"))
