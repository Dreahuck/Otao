from django.contrib import admin

from .models import ParametrageTache , Personne , Tache, AttestationInfos

admin.site.register(ParametrageTache)
admin.site.register(Personne)
admin.site.register(Tache)
admin.site.register(AttestationInfos)