{% extends "mail_templated/base.tpl" %}


{% block subject %}
Senha para ligações telefonicas  
{% endblock %}

{% block body %}

==================================================
Usu&aacute;rio {{ u.get_full_name }}, 

Tipo de senha {{ t }}:

Senha: {{ c }}
==================================================

{% load solo_tags %}
{% get_solo 'ace.AceConfig' as site_config %}

{{ site_config.password_email_text|safe }}


{% endblock %}



{% block html %}
<hr>
<p>Prezado(a) <b>{{ u.get_full_name }}</b>,<p>

<p>Informamos sua senha para realiza&ccedil;&atilde;o de <b>liga&ccedil;&otilde;es {{t}}</b>:</p>

<b>Senha</b>: <spam style="color:blue;">{{c}}</spam>
<hr>

{% load solo_tags %}
{% get_solo 'ace.AceConfig' as site_config %}

<br>

{{ site_config.password_email_html_text|safe }}

<p>Esta mensagem foi enviada automaticamente, por favor n&atilde;o  responda<p>

<p> ACE - Administração de Cabeamento Estruturado e Infraestrutura de Redes </p>

{% endblock %}