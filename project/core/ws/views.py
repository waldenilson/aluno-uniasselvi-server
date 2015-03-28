# Create your views here.
# coding: utf-8
from django.template.context import RequestContext
from django.shortcuts import render, render_to_response
from django.core import serializers
from project.core.util.functions import ws
from project.core.models import AuthUser, AuthUserSeminario, Seminario, Etapa, Tarefa
import sys
import hashlib
import datetime
import smtplib

def usuarios(request):
	retorno = ws(request)
	if retorno == 'ok':
		objs = AuthUser.objects.all()
		if objs:
			retorno = serializers.serialize('json', objs)
		else:
			retorno = '03'
	return render_to_response('core/base/webservice.html' ,{"retorno":retorno}, context_instance = RequestContext(request))

def login_email(request):
	retorno = ws(request)
	if retorno == 'ok':
		if request.GET.get('email', False):
			email = request.GET['email']
			if request.GET.get('password', False):
				senha = hashlib.md5( request.GET['password'] ).hexdigest()
				objs = AuthUser.objects.filter( email = email, password = senha, is_active = True )
				if objs:
					retorno = serializers.serialize('json', objs)
				else:
					retorno = '03'
			else:
				retorno = '01'
		else:
			retorno = '01'
	return render_to_response('core/base/webservice.html' ,{"retorno":retorno}, context_instance = RequestContext(request))

def add_user(request):
	# username, password, first_name, last_name, email
	retorno = ws(request)
	if retorno == 'ok':
		if request.GET.get('email', False):
			if request.GET.get('password', False):
				email = request.GET['email']
				senha = request.GET['password']
				try:
					obj = AuthUser(
						username = '',
						password = hashlib.md5( senha ).hexdigest(),
						first_name = '',
						email = email,
						is_active = True,
						is_staff = False,
	                    last_login = datetime.datetime.now(),
	                    date_joined = datetime.datetime.now()
						)
					obj.save()
				except:
					retorno = '04'
			else:
				retorno = '01'
		else:
			retorno = '01'
	return render_to_response('core/base/webservice.html' ,{"retorno":retorno}, context_instance = RequestContext(request))

def edit_user(request):
	# username, password, first_name, last_name, email
	retorno = ws(request)
	if retorno == 'ok':
		if request.GET.get('nome', False):
			if request.GET.get('id', False):
				nome = request.GET['nome']
				id_user = request.GET['id']
				try:
					user = AuthUser.objects.get( pk = id_user )
					obj = AuthUser(
						id = user.id,
						username = nome,
						password = user.password,
						first_name = user.first_name,
						email = user.email,
						is_active = user.is_active,
						is_staff = user.is_staff,
	                    last_login = user.last_login,
	                    date_joined = user.date_joined
						)
					obj.save()
				except:
					retorno = '04'
			else:
				retorno = '01'
		else:
			retorno = '01'
	return render_to_response('core/base/webservice.html' ,{"retorno":retorno}, context_instance = RequestContext(request))

def seminarios(request):
	retorno = ws(request)
	if retorno == 'ok':
		if request.GET.get('user', False):
			user = request.GET['user']
			lus = AuthUserSeminario.objects.filter( user__id = user, ativo = True )
			objs = []
			for us in lus:
				objs.append(us.seminario)
			if objs:
				retorno = serializers.serialize('json', objs)
			else:
				retorno = '03'
		else:
			retorno = '01'
	return render_to_response('core/base/webservice.html' ,{"retorno":retorno}, context_instance = RequestContext(request))

def tarefas(request):
	retorno = ws(request)
	if retorno == 'ok':
		if request.GET.get('user', False):
			if request.GET.get('seminario', False):
				user = request.GET['user']
				seminario = request.GET['seminario']
				try:
					lus = AuthUserSeminario.objects.filter( user__id = user, seminario__id = seminario, ativo = True )
					obj_seminario = lus[0].seminario
					le = Etapa.objects.filter( seminario__id = obj_seminario.id, ativo = True )				
					objs = []
					for e in le:
						lt = Tarefa.objects.filter( etapa__id = e.id, ativo = True )
						for t in lt:
							objs.append(t)
					if objs:
						retorno = serializers.serialize('json', objs)
					else:
						retorno = '03'
				except:
					retorno = '04'
			else:
				retorno = '01'
		else:
			retorno = '01'
	return render_to_response('core/base/webservice.html' ,{"retorno":retorno}, context_instance = RequestContext(request))

def etapas(request):
	retorno = ws(request)
	if retorno == 'ok':
		if request.GET.get('user', False):
			if request.GET.get('seminario', False):
				user = request.GET['user']
				seminario = request.GET['seminario']
				try:
					lus = AuthUserSeminario.objects.filter( user__id = user, seminario__id = seminario, ativo = True )
					obj_seminario = lus[0].seminario
					le = Etapa.objects.filter( seminario__id = obj_seminario.id, ativo = True )				
					objs = []
					for e in le:
						objs.append(e)
					if objs:
						retorno = serializers.serialize('json', objs)
					else:
						retorno = '03'
				except:
					retorno = '04'
			else:
				retorno = '01'
		else:
			retorno = '01'
	return render_to_response('core/base/webservice.html' ,{"retorno":retorno}, context_instance = RequestContext(request))


def add_seminario(request):
	retorno = ws(request)
	if retorno == 'ok':
		if request.GET.get('curso', False):
			if request.GET.get('turma', False):
				if request.GET.get('tema_base', False):
					if request.GET.get('modulo', False):
						if request.GET.get('user', False):
							curso = request.GET['curso']
							turma = request.GET['turma']
							tema_base = request.GET['tema_base']
							modulo = request.GET['modulo']
							user = request.GET['user']

							lus = AuthUserSeminario.objects.filter( user__id = user, seminario__modulo = modulo, seminario__turma = turma )
							u = AuthUser.objects.filter( id = user )
							if not lus and u:
								try:
									s = Seminario(
										curso = curso,
										turma = turma,
										modulo = modulo,
										tema_base = tema_base
										)
									s.save()
								except:
									retorno = '04'
								try:
									us = AuthUserSeminario(
										user = AuthUser.objects.get( pk = user ),
										seminario = s,
										ativo = True,
										adm = True
										)
									us.save()
									add_aux_seminario(s)
								except:
									s.delete()
									retorno = '04'
							else:
								retorno = '05'
						else:
							retorno = '01'
					else:
						retorno = '01'
				else:
					retorno = '01'
			else:
				retorno = '01'
		else:
			retorno = '01'
	return render_to_response('core/base/webservice.html' ,{"retorno":retorno}, context_instance = RequestContext(request))

def edit_seminario(request):
	pass

def delete_seminario(request):
	pass

def enviar_email(host, port, from_, to, body):
	try:
		smtpObj = smtplib.SMTP(host, port)
		smtpObj.sendmail( from_, to, body)         
		return True
	except:
		return False

def add_aux_seminario(s):
	# add etapas
	e1 = Etapa( nome='Orientação', descricao='', ativo = True, seminario = s ) 
	e1.save()
	t11 = Tarefa( nome='', descricao='', ativo=True, etapa=e1, check=False)
	t11.save()
	t12 = Tarefa( nome='', descricao='', ativo=True, etapa=e1, check=False)
	t12.save()
	t13 = Tarefa( nome='', descricao='', ativo=True, etapa=e1, check=False)
	t13.save()
	t14 = Tarefa( nome='', descricao='', ativo=True, etapa=e1, check=False)
	t14.save()

	e2 = Etapa( nome='Estudos Preliminares', descricao='', ativo = True, seminario = s ) 
	e2.save()
	t21 = Tarefa( nome='', descricao='', ativo=True, etapa=e2, check=False)
	t21.save()

	e3 = Etapa( nome='Planejamento', descricao='', ativo = True, seminario = s ) 
	e3.save()
	t31 = Tarefa( nome='', descricao='', ativo=True, etapa=e3, check=False)
	t31.save()
	t32 = Tarefa( nome='', descricao='', ativo=True, etapa=e3, check=False)
	t32.save()
	t33 = Tarefa( nome='', descricao='', ativo=True, etapa=e3, check=False)
	t33.save()

	e4 = Etapa( nome='Execução', descricao='', ativo = True, seminario = s ) 
	e4.save()
	t41 = Tarefa( nome='', descricao='', ativo=True, etapa=e4, check=False)
	t41.save()
	t42 = Tarefa( nome='', descricao='', ativo=True, etapa=e4, check=False)
	t42.save()

	e5 = Etapa( nome='Análise', descricao='', ativo = True, seminario = s ) 
	e5.save()
	t51 = Tarefa( nome='', descricao='', ativo=True, etapa=e5, check=False)
	t51.save()
	t52 = Tarefa( nome='', descricao='', ativo=True, etapa=e5, check=False)
	t52.save()

	e6 = Etapa( nome='Socialização', descricao='', ativo = True, seminario = s ) 
	e6.save()
	t61 = Tarefa( nome='', descricao='', ativo=True, etapa=e6, check=False)
	t61.save()
	t62 = Tarefa( nome='', descricao='', ativo=True, etapa=e6, check=False)
	t62.save()
	t63 = Tarefa( nome='', descricao='', ativo=True, etapa=e6, check=False)
	t63.save()
	t64 = Tarefa( nome='', descricao='', ativo=True, etapa=e6, check=False)
	t64.save()
