from django.db import models


# Create your models here.
ONLINE = 'Online'
OFFLINE = 'Offline'
REACHABLE = [
    (ONLINE, ONLINE),
    (OFFLINE, OFFLINE)
]

class Light(models.Model):
    light_id = models.IntegerField('Light id in Hue', null=False, primary_key=True)
    name = models.CharField('Light name in Hue', blank=False, max_length=30)
    on = models.BooleanField('Light is on/off', default=False)
    reachable = models.CharField('Online/Offline', max_length=8,
            choices=REACHABLE, default=OFFLINE)
    type = models.CharField('Light type', max_length=30, default='Dimmable light')
    value = models.IntegerField('Light value', default=1)

    def __str__(self):
        return self.name


