from __future__ import unicode_literals

from django.db import models

class AuthGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    class Meta:
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    class Meta:
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        db_table = 'auth_user_user_permissions'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', null=True, blank=True)
    object_id = models.TextField()
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    class Meta:
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = 'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    class Meta:
        db_table = 'django_site'

class Seminario(models.Model):
    id = models.AutoField(primary_key=True)
    curso = models.CharField(max_length=80)
    turma = models.CharField(max_length=50)
    tema_base = models.CharField(max_length=50)
    modulo = models.CharField(max_length=50)
    class Meta:
        db_table = 'seminario'

class AuthUserSeminario(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser,null=False)
    seminario = models.ForeignKey(Seminario,null=False)
    ativo = models.BooleanField(null=False)
    adm = models.BooleanField(null=False)
    class Meta:
        db_table = 'auth_user_seminario'

class Etapa(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=80)
    descricao = models.TextField(null=False, blank=True)
    ativo = models.BooleanField(null=False)
    seminario = models.ForeignKey(Seminario, null=False)
    class Meta:
        db_table = 'etapa'

class Tarefa(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.TextField(null=False)
    descricao = models.TextField(null=False, blank=True)
    ativo = models.BooleanField(null=False)
    etapa = models.ForeignKey(Etapa, null=False)
    check = models.BooleanField(null=False)
    class Meta:
        db_table = 'tarefa'
