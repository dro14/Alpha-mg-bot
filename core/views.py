from django.shortcuts import redirect


def redirect_view(_):
    return redirect("/admin/login/")
