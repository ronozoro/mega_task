from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render
from django.db import connection
from .models import Site
from .models import SiteLog


def site_home(request):
    site_ids = Site.objects.all()
    return render(request, 'sites.html', {'available_sites': site_ids, 'title': 'Available Sites','site':True})


def site_detail(request, site_id):
    try:
        site_id = Site.objects.get(pk=site_id)
        site_log_ids = site_id.sitelog_set.all()
    except Site.DoesNotExist:
        raise Http404("Site does not exist")
    return render(request, 'sites_detail.html', {'site_id': site_id, 'site_log_ids': site_log_ids,'site':True})


def sites_summary_sum(request):
    site_ids = Site.objects.all()
    list_of_sites = []
    for site in site_ids:
        vals = dict()
        site_details = SiteLog.objects.filter(site_id=site)
        a_sum = SiteLog.objects.filter(site_id=site).aggregate(Sum('a_value'))['a_value__sum']
        b_sum = SiteLog.objects.filter(site_id=site).aggregate(Sum('b_value'))['b_value__sum']
        vals.update({'name': site.name, 'a_value': a_sum, 'b_value': b_sum})
        list_of_sites.append(vals)
    return render(request, 'sites_summary.html', {'list_of_sites':list_of_sites,'page_type':'sum','site':False})

def sites_summary_avg(request):
    site_ids = Site.objects.all()
    list_of_sites = []
    site_ids = Site.objects.all()
    cursor = connection.cursor()
    list_of_sites = []
    for site in site_ids:
        cursor.execute("SELECT s.name as name,avg(l.a_value) as a_value,avg(l.b_value) as b_value FROM sites_site s,sites_sitelog l where l.site_id_id==s.id and  s.id=%s"%site.id)
        row = cursor.fetchall()
        col_names = cursor.description
        data=[{col_names[item][0]:col for item, col in enumerate(record)} for record in row]
        list_of_sites.extend(data)
    cursor.close()
    return render(request, 'sites_summary.html', {'list_of_sites': list_of_sites,'page_type':'avg','site':False})
