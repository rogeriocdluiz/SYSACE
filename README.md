=====
ACE
=====

ACE is a Django app to administrate networks hosts, ip address, services, racks, patchpanels, phones e phone passwords. The system objective is turn the IT Infraestructure adminsitration easyer.



Detailed documentation is in the "docs" directory.

Quick start
-----------
1. Install ace with command pip install django-sysace. Need development packages like gcc (build-essential in Debian and Ubuntu) and python-dev.


2. Add "ace" and other apps to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'ace',
        'simple_history',
        'django_modalview',
        'dal',
        'dal_select2',
        'mail_templated',
        'solo',
        'widget_tweaks',
        'pagination',
        'import_export'            
        'widget_tweaks',
        
        

2. Include the polls URLconf in your project urls.py like this::

   u rl(r'^ace/', include('ace.urls')),

3. Run `python manage.py migrate` to create the ace models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   (you'll need the Admin app enabled).
    
5. Visit http://127.0.0.1:8000/ace/ to start to include IT infraestructure components.



6. Install the pagination middleware. Your settings file might look something like:

    MIDDLEWARE_CLASSES = (
        # ...
        'pagination.middleware.PaginationMiddleware',
    )

7. If it’s not already added in your setup, add the request context processor. Note that context processors are set by default implicitly, so to set them explicitly, you need to copy and paste this code into your under the value TEMPLATE_CONTEXT_PROCESSORS:

    ("django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request")






PT-BR

ACE - Administração de cabeamento estruturado.

Sistema desenvolvido em Django para controle de pontos de rede (voz, dados, voip), ramais, senhas para ligações telefonicas, switches, patchpanels, equipamentos, redes, serviços e endereços IP.


