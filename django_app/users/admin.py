from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile, UserLevel


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
    )
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "level", "photo")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    )


@admin.register(UserLevel)
class UserLevelAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)