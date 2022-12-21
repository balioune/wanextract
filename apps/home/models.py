# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Site(models.Model):
    zonegeo = models.CharField(max_length=20, default='')
    site_name = models.CharField(max_length=20)
    truview_site_id = models.IntegerField()
    in_bw = models.FloatField(default=0.0)
    out_bw = models.FloatField(default=0.0)
    avg_congestion_in = models.FloatField(default=0.0)
    avg_congestion_out = models.FloatField(default=0.0)
    PROVIDER_TYPE = (
        ('-----', '-----'),
        ('TATA', 'TATA'),
        ('SITA', 'SITA'),
        ('SONEMA', 'SONEMA'),
        ('GTT', 'GTT'),
    )

    provider = models.CharField(max_length=20, choices=PROVIDER_TYPE, help_text='Provider', default='-----')
    class Meta:
        unique_together = ('zonegeo', 'site_name')

"""
class Router(models.Model):
    site = models.ForeignKey(Site, verbose_name="Site", on_delete=models.CASCADE, related_name="+")
    name = models.CharField(max_length=20)
    truview_router_id = models.IntegerField()
    in_bw = models.FloatField(default=0.0)
    out_bw = models.FloatField(default=0.0)
    avg_congestion_in = models.FloatField(default=0.0)
    avg_congestion_out = models.FloatField(default=0.0)
    class Meta:
        unique_together = ('name',)
"""

class Interface(models.Model):
    site = models.ForeignKey(Site, verbose_name="Site", on_delete=models.CASCADE, related_name="+")
    deviceIp = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    deviceName = models.CharField(max_length=20)
    truview_if_id = models.IntegerField()
    tvfIfId = models.IntegerField(default=0.0)
    ifIndex = models.IntegerField(default=0.0)
    name = models.CharField(max_length=20)
    in_bw = models.FloatField(default=0.0)
    out_bw = models.FloatField(default=0.0)
    avg_congestion_in = models.FloatField(default=0.0)
    avg_congestion_out = models.FloatField(default=0.0)
    class Meta:
        unique_together = ('truview_if_id', 'name')

    def __str__(self):
        return str(self.deviceName) + ' : ' + str(self.name)
    def save(self, **kwargs):
        pass

class Application(models.Model):
    truview_app_id = models.IntegerField()
    app_id = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    class Meta:
        unique_together = ('truview_app_id', 'name')

class ApplicationPerInterface(models.Model):
    timestamp = models.DateTimeField()
    date = models.DateField()
    time = models.TimeField()
    interface = models.ForeignKey(Interface, verbose_name="Interface", on_delete=models.CASCADE, related_name="+")
    TxOctets = models.FloatField(default=0.0)
    RxOctets = models.FloatField(default=0.0)
    TotalOctets = models.FloatField(default=0.0)
    app_name = models.CharField(max_length=20)
    router_name = models.CharField(max_length=20)
    if_name = models.CharField(max_length=20)
    class Meta:
        # unique_together = ('timestamp', 'interface')
        pass

    def get_interface_name(self):
        return self.interface.name
class InInterfaceBurst(models.Model):
    timestamp = models.DateTimeField()
    site_name = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    interface = models.ForeignKey(Interface, verbose_name="Interface", on_delete=models.CASCADE, related_name="+")
    InBurst1 = models.FloatField(default=0.0)
    InBurst2 = models.FloatField(default=0.0)
    InBurst3 = models.FloatField(default=0.0)
    InBurst4 = models.FloatField(default=0.0)
    Burst3 = models.IntegerField(default=0)
    Burst4 = models.IntegerField(default=0)
    applications = models.TextField()

    def get_id(self):
        return self.id

    def get_interface_name(self):
        return self.interface.name

    def get_router_name(self):
        return self.interface.deviceName
    class Meta:
        # unique_together = ('timestamp', 'interface')
        pass

class OutInterfaceBurst(models.Model):
    timestamp = models.DateTimeField()
    site_name = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    interface = models.ForeignKey(Interface, verbose_name="Interface", on_delete=models.CASCADE, related_name="+")
    OutBurst1 = models.FloatField(default=0.0)
    OutBurst2 = models.FloatField(default=0.0)
    OutBurst3 = models.FloatField(default=0.0)
    OutBurst4 = models.FloatField(default=0.0)
    Burst3 = models.IntegerField(default=0)
    Burst4 = models.IntegerField(default=0)
    applications = models.TextField()

    def get_id(self):
        return self.id
    def get_interface_name(self):
        return self.interface.name

    def get_router_name(self):
        return self.interface.deviceName
    class Meta:
        #unique_together = ('timestamp', 'interface')
        pass

class AppInterfaceOut(models.Model):
    timestamp = models.DateTimeField()
    date = models.DateField()
    time = models.TimeField()
    interface = models.ForeignKey(Interface, verbose_name="Interface", on_delete=models.CASCADE, related_name="+")
    #app = models.ForeignKey(Application, verbose_name="Application", on_delete=models.CASCADE, related_name="+", null=True, blank = True)
    if_name = models.CharField(max_length=50, default='')
    router_name = models.CharField(max_length=50)
    app = models.CharField(max_length=20)
    tx_throuput = models.FloatField(default=0.0)
    class Meta:
        #unique_together = ('timestamp', 'interface', 'app')
        pass

class AppInterfaceIn(models.Model):
    timestamp = models.DateTimeField()
    date = models.DateField()
    time = models.TimeField()
    interface = models.ForeignKey(Interface, verbose_name="Interface", on_delete=models.CASCADE, related_name="+")
    #app = models.ForeignKey(Application, verbose_name="Application", on_delete=models.CASCADE, related_name="+", null=True, blank = True)
    if_name = models.CharField(max_length=50)
    router_name = models.CharField(max_length=50)
    app = models.CharField(max_length=20, default='')
    rx_throuput = models.FloatField(default=0.0)
    class Meta:
        # unique_together = ('timestamp', 'interface', 'app')
        pass
