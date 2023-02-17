from django.contrib import admin
from .models import ReportIWatch, ReportSaviorProblem, ReportZakatPost, Sugg2Savior, ReportUser, SaviorMembers
# Register your models here.

@admin.register(ReportIWatch)
class IWatchRep(admin.ModelAdmin):
  list_display = ('id','iwatch_reporter','reported_iw','problem', 'created' )


@admin.register(ReportSaviorProblem)
class SaviorProblem(admin.ModelAdmin):
  list_display = ('id','savior_reporter','problem', 'created' )

@admin.register(ReportZakatPost)
class ZakatRep(admin.ModelAdmin):
  list_display = ('id','zakat_reporter','reported_zp','problem', 'created' )

@admin.register(Sugg2Savior)
class SaviorSuggestions(admin.ModelAdmin):
  list_display = ('id','savior_adviser','suggestion', 'created' )

@admin.register(ReportUser)
class UserRep(admin.ModelAdmin):
  list_display = ('id','reporter_profile','reported_profile','problem', 'created' )


@admin.register(SaviorMembers)
class SaviorMembers(admin.ModelAdmin):
  list_display = ('id','member_profile', 'deposit_receipt', 'created' )