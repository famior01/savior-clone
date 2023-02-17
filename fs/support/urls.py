from django.urls import path
from support import views
app_name = 'support'  

urlpatterns = [
    path('ReportIWatch/', views.ReportIWatchFunc, name='ReportIWatchFunc'),
    path('ReportZakatPost/', views.ReportZakatPostFunc, name='ReportZakatPostFunc'),
    path('Sugg2Savior/', views.Sugg2SaviorFunc, name='Sugg2SaviorFunc'),
    path('ReportSaviorProblem/', views.ReportSaviorProblemFunc, name='ReportSaviorProblemFunc'),
    path('ReportUser/', views.ReportUserFunc, name='ReportUserFunc'),
    path('SaviorMembers/', views.SaviorMembersFunc, name='SaviorMembersFunc'),
]
