from django.db import models
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator
from django.conf import settings


class ProfileUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    # The additional attributes we wish to include.
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=
    _("Phone number in the format: '+999999999'. Up to 15 digits allowed."))
    telephone = models.CharField(_('telephone'), validators=[phone_regex], blank=True, help_text=_('The telephone to contact you.'), max_length=16)

    def __unicode__(self):
        return "{1} on {0}".format(self.user.email, self.user.name)

class Province(models.Model):
    '''In this model, we will store burundi provinces'''
    name = models.CharField(_('name'),unique=True, max_length=20)
    code = models.IntegerField(unique=True, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse('province_detail', kwargs={'pk': self.id})
        return self.id

    class Meta:
        ordering = ('name',)

class Commune(models.Model):
    '''In this model, we will store burundi communes'''
    province = models.ForeignKey(Province)
    name = models.CharField(_('name'),unique=True, max_length=20)
    code = models.IntegerField(unique=True, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse('province_detail', kwargs={'pk': self.id})
        return self.id

    class Meta:
        ordering = ('name',)

class Colline(models.Model):
    '''In this model, we will store burundi colline'''
    commune = models.ForeignKey(Commune)
    name = models.CharField(_('name'), max_length=30)
    code = models.IntegerField(unique=True, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse('province_detail', kwargs={'pk': self.id})
        return self.id

    class Meta:
        ordering = ('name',)

class District(models.Model):
    '''In this model, we will store districts'''
    province = models.ForeignKey(Province, verbose_name='province')
    name = models.CharField(_('nom'), unique=True, max_length=40)
    code = models.IntegerField(unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class CDS(models.Model):
    STATUS_CHOICES = (
        ('Pub', 'Public'),
        ('Con', 'Conf'),
        ('Priv', 'Prive'),
        ('Ass', 'Ass'),
        ('HPub', 'HPublic'),
        ('HCon', 'HConf'),
        ('HPrv', 'HPrive'),
    )
    district = models.ForeignKey(District)
    name = models.CharField( max_length=40)
    code = models.CharField(unique=True, max_length=6)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, blank=True, null=True, help_text=_('Either Public, Conf, Ass, Prive  or Hospital status.'))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
