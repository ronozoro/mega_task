from django.db import models


class Site(models.Model):
    name = models.CharField(verbose_name='Site Name', max_length=256, blank=False, null=False)

    def __str__(self):
        return self.name


Site()


class SiteLog(models.Model):
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)
    date = models.DateField('Date')
    a_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    b_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '%s : %s' % (self.site_id.name, self.date)


SiteLog()
