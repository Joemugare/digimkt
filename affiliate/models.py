# affiliate/models.py
from django.db import models

class AffiliateProgram(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = 'affiliate'

    def __str__(self):
        return self.name

class AffiliateLink(models.Model):
    url = models.URLField()
    program = models.ForeignKey(AffiliateProgram, on_delete=models.CASCADE)  # Reference local AffiliateProgram
    title = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = 'affiliate'

    def __str__(self):
        return self.url

    def click_count(self):
        return self.linkclick_set.count()

    def conversion_rate(self):
        clicks = self.linkclick_set.count()
        return 0  # Replace with actual conversion logic if needed

class LinkClick(models.Model):
    link = models.ForeignKey(AffiliateLink, on_delete=models.CASCADE)
    click_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        app_label = 'affiliate'

    def __str__(self):
        return f"Click at {self.click_date}"