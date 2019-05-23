{% extends "mail_templated/base.tpl" %}


{% block subject %}
Novo ramal/senha modificado
{% endblock %}

{% block body %}

    ==================================================
    {% if pwd == "ok" %}
    
    O usuario  {{ u.get_full_name }}  ({{ u }}),

    foi {{ m }} {{ c }} senha telefônica

    na data de {{ d }}
   

    {% else %}
    
    O usuario  {{ u.get_full_name }}  ({{ u }}),

    foi {{ m }} {{ c }} telefone  {{ p }}

     na data de {{ d }}
    
    {% endif %}
    ==================================================

    {% if category %} Categoria: {{ category}}  {% endif %}
    {% if phonetype %} Tipo {{ phonetype }}  {% endif %}
    {% if place %} Local {{ place }} - {{ place.sector | default_if_none:""}}  {% endif %}

{% endblock %}



{% block html %}

<hr>
{% if pwd == "ok" %}

    <p> O usu&aacute;rio <b> {{ u.get_full_name }} </b> ({{ u }}),</b> </p>

    <p> foi <b><font color="red">{{ m }}</font></b> {{ c }} <b> senha telef&ocirc;nica</b> na data de <b> {{ d }} </b> </p>

{% else %}

    <p> O usu&aacute;rio <b> {{ u.get_full_name }} </b> ({{ u }}),</b> </p>

    <p> foi <b><font color="red">{{ m }}</font></b> {{ c }} telefone  <b>{{ p }}</b> na data de <b> {{ d }} </b> </p>

{% endif %}

    {% if category %} <p> Categoria: {{category}} </p> {% endif %}
    {% if phonetype %} <p> Tipo: {{ phonetype }}</p> {% endif %}
    {% if place %} <p> Local: {{ place }} - {{ place.sector | default_if_none:""}} </p> {% endif %}

<hr>

<p>Esta mensagem foi enviada automaticamente, por favor n&atilde;o  responda<p>

<p> ACE - Administração de Cabeamento Estruturado e Infraestrutura de Redes </p>

{% endblock %}

