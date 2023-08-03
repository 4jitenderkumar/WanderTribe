from django.contrib import admin
from django.contrib.auth import get_user_model

from main.models import Customer , Guide, Hike, EnrolledHikers, NewsLetter, Contact
from django import forms

admin.site.site_header = 'GUIDE DASHBOARD'


class hikes_admin(admin.ModelAdmin):

    list_display = ["trail", "user_id"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user_id':
            # Limit the queryset for the user_id field to only the currently logged-in staff user
            kwargs['queryset'] = Guide.objects.filter(username=request.user.username)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    # def changelist_view(self, request, extra_context=None):
    #     queryset = self.get_queryset(request)
    #
    #     if not queryset.exists():
    #         empty_message = "No courses found for the current user."
    #         context = {'empty_message': empty_message}
    #         return super().changelist_view(request, extra_context=context)
    #
    #     return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset

        print(request.user)
        author_detail = Guide.objects.filter(username=request.user)[0]
        print(author_detail)
        queryset = queryset.filter(user_id=author_detail)

        if not queryset.exists():
            return queryset.none()

        return queryset

class GuideAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset

        print(request.user)
        return queryset.filter(username__startswith=request.user)



# Register your models here.
admin.site.register(Customer)
admin.site.register(Guide, GuideAdmin)
admin.site.register(Hike, hikes_admin)
admin.site.register(EnrolledHikers)
admin.site.register(NewsLetter)
admin.site.register(Contact)