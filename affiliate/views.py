from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import AffiliateLink, LinkClick
from django.utils import timezone

def redirect_affiliate_link(request, link_id):
    link = get_object_or_404(AffiliateLink, id=link_id, is_active=True)
    LinkClick.objects.create(
        link=link,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        referrer=request.META.get('HTTP_REFERER', '')
    )
    link.click_count += 1
    link.last_clicked = timezone.now()
    link.save()
    return HttpResponseRedirect(link.affiliate_url)

def affiliate_link_list(request):
    links = AffiliateLink.objects.filter(is_active=True)
    return render(request, 'affiliate/link_list.html', {'links': links})