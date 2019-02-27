{% extends "mail_templated/base.tpl" %}


{% block subject %}
Novo ramal/senha modificado
{% endblock %}

{% block body %}

    {% if pwd == "ok" %}
    ==================================================
    O usuario  {{ u.get_full_name }}  ({{ u }}),

    foi {{ m }} {{ c }} senha ******

     na data de {{ d }}
    ==================================================

    {% else %}
    ==================================================
    O usuario  {{ u.get_full_name }}  ({{ u }}),

    foi {{ m }} {{ c }} telefone  {{ p }}

     na data de {{ d }}
    ==================================================
    {% endif %}



{% endblock %}



{% block html %}

<hr>
{% if pwd == "ok" %}

    <p> O usu&aacute;rio <b> {{ u.get_full_name }} </b> ({{ u }}),</b> </p>

    <p> foi {{ m }} {{ c }} senha  <b>******</b> na data de <b> {{ d }} </b> </p>


{% else %}

    <p> O usu&aacute;rio <b> {{ u.get_full_name }} </b> ({{ u }}),</b> </p>

    <p> foi {{ m }} {{ c }} telefone  <b>{{ p }}</b> na data de <b> {{ d }} </b> </p>


{% endif %}



<hr>

<p>Esta mensagem foi enviada automaticamente, por favor n&atilde;o  responda<p>

<p> ACE - Administração de Cabeamento Estruturado e Infraestrutura de Redes </p>

{% endblock %}

