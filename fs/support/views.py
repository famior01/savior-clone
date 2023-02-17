from django.shortcuts import render
from .models import ReportIWatch, ReportZakatPost, ReportSaviorProblem, Sugg2Savior, ReportUser, SaviorMembers
from zakat_posts.models import ZakatPosts
from IWatch.models import IWatch
from profiles.models import Profile
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from notifications.signals import notify
from .forms import SaviorMembersForm
# Create your views here.

@login_required
def ReportSaviorProblemFunc(request):
  if request.method == "POST":
    problem = request.POST['problem']
    profile = Profile.objects.get(user=request.user)

    if problem:
      report_savior_problem = ReportSaviorProblem.objects.create(savior_reporter=profile, problem=problem)
      report_savior_problem.save()
      messages.success(request, f'Your problem has been sent to the savior, we will check it out and get back to you.')
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      messages.error(request, f'You have sent nothing :)')
      return redirect(request.META.get('HTTP_REFERER'))
  return redirect(request.META.get('HTTP_REFERER'))

@login_required
def Sugg2SaviorFunc(request):
  if request.method == 'POST':
    sugg = request.POST['suggestion']
    profile = Profile.objects.get(user=request.user)

    if sugg:
      sugg2savior = Sugg2Savior.objects.create(savior_adviser=profile, suggestion=sugg)
      sugg2savior.save()
      messages.success(request, f'Your suggestion has been sent to the savior, we will check it out and get back to you.')
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      messages.error(request, f'You have sent nothing :)')
      return redirect(request.META.get('HTTP_REFERER'))
  return redirect(request.META.get('HTTP_REFERER'))

@login_required
def ReportIWatchFunc(request):
  if request.method == 'POST':
    iw_id = request.POST['iw_id']
    problem = request.POST['problem'] 
    profile = Profile.objects.get(user=request.user)
    iw = IWatch.objects.get(id=iw_id)

    if iw.reported_iw.filter(iwatch_reporter=profile).exists():
      messages.error(request, f'You have already reported this video')
      return redirect(request.META.get('HTTP_REFERER'))

    if problem: 
      iw_report = ReportIWatch.objects.create(iwatch_reporter=profile, reported_iw=iw, problem=problem)
      iw_report.save()
      messages.success(request, f'You have reported {iw.creator} for {problem}, We are sorry for this inconvenience, we will check it out.')
      notify.send(request.user, recipient=iw.creator.user, verb=f'{profile.user.full_name} have reported you for {problem}, we are checking it, if found guilty, your video will be deleted.')
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      messages.error(request, f'You have reported nothing :)')
      return redirect(request.META.get('HTTP_REFERER'))
  return redirect(request.META.get('HTTP_REFERER'))

@login_required
def ReportZakatPostFunc(request):
  if request.method == 'POST':
    zp_id = request.POST['zp_id']
    problem = request.POST['problem'] 
    profile = Profile.objects.get(user=request.user)
    zp = ZakatPosts.objects.get(id=zp_id)
    print("\n***************", zp_id,"zp_id", "******", zp, "zp", "***************\n")

    if zp.reported_zp.filter(zakat_reporter=profile).exists():
      messages.error(request, f'You have already reported this Seeker')
      return redirect(request.META.get('HTTP_REFERER'))

    if problem:
      zp_report = ReportZakatPost.objects.create(zakat_reporter=profile, reported_zp=zp, problem=problem)
      zp_report.save()
      messages.success(request, f'You have reported {zp.creator} for {problem}, We are sorry for this inconvenience, we will check it out.')
      notify.send(request.user, recipient=zp.creator.user, verb=f'{profile.user.full_name} have reported you for {problem}, we are checking, if found guilty, your post will be deleted.')
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      messages.error(request, f'You have reported nothing :)')
      return redirect(request.META.get('HTTP_REFERER'))
  return redirect(request.META.get('HTTP_REFERER'))


@login_required()
def ReportUserFunc(request):
  if request.method == 'POST':
    problem = request.POST['problem']
    profile_pk = request.POST['profile_pk']
    reporter_pro = Profile.objects.get(user=request.user)
    reported_pro= Profile.objects.get(id=profile_pk)


    if reported_pro.reported_profile.filter(reporter_profile=reporter_pro).exists():
      messages.error(request, f'You have already reported this user')
      return redirect(request.META.get('HTTP_REFERER'))
    elif  problem:
      report_user = ReportUser.objects.create(reporter_profile=reporter_pro, reported_profile=reported_pro, problem=problem)
      report_user.save()
      reported_pro.following.remove(reporter_pro.user)
      reported_pro.save()
      reporter_pro.following.remove(reported_pro.user)
      reporter_pro.save()
      messages.success(request, f'You have reported {reported_pro.user.full_name} for {problem}, We are sorry for this inconvenience, we will check it out.')
      # notify.send(request.user, recipient=user.user, verb=f'{profile.user.full_name} have reported you for {problem}, we are checking, if found guilty, your account will be deleted.')
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      messages.error(request, f'You have reported nothing :)')
      return redirect(request.META.get('HTTP_REFERER'))
  return redirect(request.META.get('HTTP_REFERER'))


@login_required
def SaviorMembersFunc(request):
  if request.method == 'POST':
    deposit_receipt = request.POST['deposit_recipient']
    member = Profile.objects.get(user=request.user)
    
    if deposit_receipt:
      savior_member = SaviorMembers.objects.create(member_profile=member, deposit_receipt=deposit_receipt) # first check by admin
      savior_member.save()
      messages.success(request, f'Thank you for joining the savior, we will check your deposit receipt.')
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      messages.error(request, f'You have reported nothing :)')
      return redirect(request.META.get('HTTP_REFERER'))
  return redirect(request.META.get('HTTP_REFERER'))



# @login_required
# class SaviorMemberCreate(CreateView):
#   model = SaviorMembers
#   fields = ['deposit_receipt']
#   template_name = 'main/navbar.html'
#   success_url = reverse_lazy(request.META.get('HTTP_REFERER'))

#   def form_valid(self, form):
#     form.instance.member_profile = Profile.objects.get(user=self.request.user)
#     return super().form_valid(form)