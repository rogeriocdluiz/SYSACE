
Instalação
==========

Caso esteja utilizando um sistema GNU-Linux será necessário instalar previamente pacotes de desenvolvimento como gcc, make e outros (o pacote build-essential no Debian e Ubuntu) além do python-dev.

Versão 1.2.x compatível com **Django 1.11**

1. Instale o ACE com o comando a seguir::

    pip install django-sysace




2. Adicione **django.contrib.admin**, **ace** e os outros apps necessários à seção **INSTALLED_APPS** do arquivos **settings.py**.  ::

	INSTALLED_APPS = [
	    ...
	    'django.contrib.admin',    
	    ...
	    'ace',
	    'simple_history',
	    'django_modalview',
	    'dal',
	    'dal_select2',
	    'mail_templated',
	    'solo',
	    'tinymce',
	    'widget_tweaks',
	    'django_cron',
	    'localflavor',
	    'django_extensions',
	    'dbbackup',
	    'django_tables2',
	    'import_export',
	    'massadmin',
	    'pagination', 
 	    


4. Inclua no arquivo urls.py do projeto URLconf do ace no arquivo urls.py do projeto como mostrado a seguir::

	url(r'^ace/', include('ace.urls')),


5. Rode o comando abaixo para criar os modelos do ace::

	python manage.py migrate

6. Inicie o servidor e acesse pelo endereço http://127.0.0.1:8000/admin/
   (vocẽ precisará do app Admin habilitado).
    
7. Acesse http://127.0.0.1:8000/ace/ para iniciar a inclusão dos componentes da infraestrutura de TI.