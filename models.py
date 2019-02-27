# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime

import ipaddress
from ipaddress import ip_address

import re

from simple_history.models import HistoricalRecords

from solo.models import SingletonModel

import django_filters

from django.contrib.auth.models import User, Group


def findips(start, end):
    start = ip_address(start)
    end = ip_address(end)
    result = []
    while start <= end:
        result.append(str(start))
        start += 1
    return result

"""
Model AceConfig where is registered system configuration

"""

class AceConfig(SingletonModel):
    org = models.TextField(u'Nome da organização/empresa.', max_length=2000, default='Empresa Exemplo', blank=True, null=True)
    email_to = models.EmailField(u'Endereço de destinatário.', max_length=75,
                                   default='no-reply@empresa.com',
                                   help_text="Notificações de alteração de ramais/senhas:  - Ex: <em>fulano@empresa.com</em>.")
    email_from = models.EmailField(u'Endereço de remetente.', max_length=75,
                                   default='no-reply@empresa.com',
                                   help_text="Email de senhas e notificações de alteração de ramais/senhas - Ex: <em>fulano@empresa.com</em>.")
    email_co = models.EmailField(u'Email - Cópia: Endereço de destino.', max_length=75, default='no-reply@empresa.com',
                                 help_text="Campo do email para envio de cópia de mensagem. Ex: <em>fulano@empresa.com</em>.")
    password_email_text = models.TextField(u'Mensagem adicional (Texto puro).', max_length=6000,
                                           default='Texto padrão do email - modo texto',
                                           help_text="Insira aqui o texto adicional que deseja que seja enviado no email de senhas - texto puro")
    password_email_html_text = models.TextField(u'Mensagem adicional (HTML)', max_length=10000,
                                                default='Texto padrão do email - HTML',
                                                help_text="Insira aqui o texto adicional que deseja que seja enviado no email de senhas - em HTML")
    phonelist_results = models.IntegerField(u'Quantidade de telefones a serem exibidos na listagem', default=10)
    passwordlist_results = models.IntegerField(u'Quantidade de senhas a serem exibidas na listagem', default=10)
    hostlist_results = models.IntegerField(u'Quantidade de hosts a serem exibidos na listagem', default=10)
    iplist_results = models.IntegerField(u'Quantidade de ips a serem exibidos na listagem', default=10)
    networklist_results = models.IntegerField(u'Quantidade de redes a serem exibidas na listagem', default=10)
    owneridlist_results = models.IntegerField(u'Quantidade de patrimonios a serem exibidas na listagem', default=10)
    placelist_results = models.IntegerField(u'Quantidade de locais a serem exibidos na listagem', default=10)
    patchpanel_results = models.IntegerField(u'Quantidade de patchpanels a serem exibidos na listagem', default=10)
    netpointlist_results = models.IntegerField(u'Quantidade de pontos de rede a serem exibidos na listagem', default=10)
    racklist_results = models.IntegerField(u'Quantidade de racks a serem exibidos na listagem', default=10)
    sectorlist_results = models.IntegerField(u'Quantidade de setores a serem exibidos na listagem', default=10)
    servicelist_results = models.IntegerField(u'Quantidade de setores a serem exibidos na listagem', default=10)
    stacklist_results = models.IntegerField(u'Quantidade de pilhas de switch a serem exibidos na listagem', default=10)
    switchlist_results = models.IntegerField(u'Quantidade de switches a serem exibidos na listagem', default=10)
    userlist_results = models.IntegerField(u'Quantidade de usuários a serem exibidos na listagem', default=10)
    printerlist_results = models.IntegerField(u'Quantidade de impressoras a serem exibidos na listagem', default=10)
    default_host_group = models.ForeignKey(Group, verbose_name='Grupo padrão para equipamentos', null=True, blank=True,  related_name="default_hostgroup")
    default_printer_group = models.ForeignKey(Group, verbose_name='Grupo padrão para impressoras', null=True, blank=True)

    def __unicode__(self):
        return u"Ace - Configurações"

    class Meta:
        verbose_name = u"Ace - Configurações"


class Log(models.Model):

    record_name = models.CharField(max_length=200,editable=False,)
    event = models.CharField(max_length=30,editable=False,)
    event_date = models.DateTimeField(u'Data de modificação',editable=False,blank=True,null=True)
    record_type = models.CharField(max_length=50,editable=False,blank=True,null=True)
    actor = models.CharField(max_length=200,editable=False,)
    object_id = models.CharField(max_length=30,editable=False,null=True)

    def __unicode__(self):
        return self.record_name


class Person(User):

    class Meta:
        proxy = True
        ordering = ('first_name', )

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)





class Manufactorer(models.Model):
    class Meta:
        verbose_name = u'Fabricante'
        verbose_name_plural = u'Fabricantes'
        ordering = ['name']

    name = models.CharField(max_length=200, verbose_name='Nome')

    def __unicode__(self):
        return self.name


class Sector(models.Model):
    class Meta:
        verbose_name = u'Setor/Departamento'
        verbose_name_plural = u'Setores/Departamentos'
        ordering = ['name']

    name = models.CharField(max_length=200, verbose_name='Nome', unique=True)
    comments = models.TextField(u'Observações', max_length=2000, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Floor(models.Model):
    class Meta:
        verbose_name = u'Andar'
        verbose_name_plural = u'Andares'
        ordering = ['name']

    name = models.CharField(max_length=20, unique=True, help_text=u"Ex: <em>1º</em> ou <em>1º andar</em>.")

    def __unicode__(self):
        return self.name


class NetpointManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        query_set = super(NetpointManager, self).get_queryset()

        return query_set.extra(
            select={
                '_netpoint_total': 'SELECT COUNT(*) FROM ace_netpoint where ace_netpoint.place_id = ace_place.id',
            },
        )


class Place(models.Model):
    class Meta:
        verbose_name = u'Local'
        verbose_name_plural = u'Locais'
        ordering = ['name']

    SALA = 'sala'
    GABINETE = 'gabinete'
    SALA_TECNICA = 'sala-tecnica'
    SALA_COFRE = 'sala-cofre'
    SALA_SEGURA = 'sala-segura'
    AUDITORIO = 'auditorio'
    OUTROS = 'outros'
    TIPO_LOCAL_CHOICES = (
        ('', '---------'),
        (SALA, 'Sala'),
        (GABINETE, 'Gabinete'),
        (SALA_TECNICA, 'Sala Técnica'),
        (SALA_COFRE, 'Sala Cofre'),
        (SALA_SEGURA, 'Sala Segura'),
        (AUDITORIO, 'Auditório'),
        (OUTROS, 'Outros'),
    )

    name = models.CharField('Ident/Num', max_length=200, help_text=u"Identificação do local<em>100</em> ou <em>A</em>.")
    placetype = models.CharField(max_length=20, choices=TIPO_LOCAL_CHOICES, verbose_name='Tipo')
    floor = models.ForeignKey(Floor, verbose_name='Andar')
    sector = models.ForeignKey(Sector, verbose_name='Setor/Departamento', blank=True, null=True)
    comments = models.TextField(u'Observações', max_length=2000, blank=True, null=True)

    # validacao
    def clean(self):

        try:
            f = self.floor
            l = Place.objects.all().filter(name=self.name, floor=f).exclude(pk=self.id)
            if l:
                raise ValidationError(u"Já existe este local neste andar.")

        except:
            raise ValidationError(u"Verifique o preenchimento dos campos abaixo")

    def __unicode__(self):
        return u'%s %s (%s)' % (self.placetype, self.name, self.floor)


class RackManager(models.Manager):
    def get_queryset(self):
        query_set = super(RackManager, self).get_queryset()

        return query_set.extra(
            select={
                '_patchpanel_total': 'SELECT COUNT(*) FROM ace_patchpanel where ace_patchpanel.rack_id = ace_rack.id',
            },
        )


class Rack(models.Model):
    class Meta:
        verbose_name = 'Rack'
        verbose_name_plural = 'Racks'
        ordering = ['name']

    name = models.CharField(verbose_name=u'Rack/Armário ', max_length=50)
    place = models.ForeignKey(Place, verbose_name=u'Localização', blank=True, null=True)

    objects = RackManager()

    def patchpanel_total(self):
        return self._patchpanel_total or 0

    def __unicode__(self):
        # return self.nome, self.localizacao
        return u'%s - %s' % (self.name, self.place)
        # return self.nome


class Vlan(models.Model):
    class Meta:
        verbose_name = 'VLAN'
        verbose_name_plural = 'VLANs'
        ordering = ['vlanid']

    vlanid = models.CharField(verbose_name=u'Id da VLAN', max_length=10, help_text="Ex: 1 , 5, 100", unique=True,
                              default="1")
    name = models.CharField(verbose_name=u'Nome da VLAN', max_length=50, help_text="Ex: Vlan dos servidores")
    comments = models.TextField(u'Observações', max_length=2000, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def __unicode__(self):
        return u'%s (%s)' % (self.vlanid, self.name)


class Network(models.Model):
    class Meta:
        verbose_name = 'Rede'
        verbose_name_plural = 'Redes'
        ordering = ['name']

    name = models.CharField(verbose_name=u'Nome da rede', max_length=200, help_text="Ex: Rede 1º andar")
    address = models.GenericIPAddressField(unique=True, help_text="Ex: 10.0.0.0", verbose_name=u"Endereço da rede")
    mask = models.IntegerField(u'Máscara', help_text="Ex: 24. Para mascara /24", default=24)
    gateway = models.GenericIPAddressField(help_text="Ex: 10.0.0.1", verbose_name=u"Gateway da rede", blank=True,
                                           null=True)
    dhcp = models.BooleanField('Usa DHCP?', default=False)
    dhcp_start = models.GenericIPAddressField(u'Primeiro endereço do range DHCP', help_text="Ex: 10.0.0.1", blank=True,
                                              null=True)
    dhcp_end = models.GenericIPAddressField(u'Último endereço do range DHCP', help_text="Ex: 10.0.0.254", blank=True,
                                            null=True)
    # vlan = models.CharField(verbose_name=u'VLAN', max_length=200,blank=True, null=True)
    vln = models.ForeignKey(Vlan, verbose_name='VLAN', blank=True, null=True)
    comments = models.TextField(u'Observações', max_length=2000, blank=True, null=True)

    def clean(self):
        redeid = self.id
        dhcp = self.dhcp

        r = self.address
        m = str(self.mask)
        if r != None and m != None:
            rm = r + "/" + m
            ip1 = self.dhcp_start
            ip2 = self.dhcp_end

            ''' checa se ip é valido '''
            try:
                ipaddress.ip_network(rm)

            except:
                raise ValidationError("Rede e máscara inválidos")

            ipsrede = list(ipaddress.ip_network(rm).hosts())
            #qtdipsrede = len(list(ipaddress.ip_network(rm).hosts()))
            qtdipsrede = len(ipsrede)
            fixos = Ip.objects.filter(network=redeid)
            #qtdfixos = Ip.objects.filter(network=redeid).count()
            qtdfixos = fixos.count()


            try:
                gw = self.gateway

                if gw != None:
                    verificagw = ipaddress.ip_address(gw) in ipaddress.ip_network(rm)
                    if verificagw == False:
                        raise ValidationError("Gateway informado não pertence à rede selecionada. Por favor, corrija.")
            except:
                raise ValidationError("Por favor preencha o gateway.")

            if m == None:
                raise ValidationError("Campo Máscara deve ser preenchido")

            masc = int(m)
            if masc > 31:
                raise ValidationError("Valor de máscara incorreto")

            if dhcp == False:

                if ip1:
                    raise ValidationError("Esta rede não utiliza DHCP. Primeiro IP do range não deve ser cadastrado")

                if ip2:
                    raise ValidationError("Esta rede não utiliza DHCP. Segundo IP do range não deve ser cadastrado")

            if dhcp == True:

                if not ip1:
                    raise ValidationError("Esta rede utiliza DHCP, primeiro ip do range não pode ser vazio")

                if not ip2:
                    raise ValidationError("Esta rede utiliza DHCP, segundo ip do range não pode ser vazio")

                if ip1:

                    verificaip1 = ipaddress.ip_address(ip1) in ipaddress.ip_network(rm)

                    if verificaip1 == False:
                        raise ValidationError(
                            "Primeiro endereço do range DHCP não pertence à rede selecionada. Por favor, corrija.")

                if ip2:

                    verificaip2 = ipaddress.ip_address(ip2) in ipaddress.ip_network(rm)

                    if verificaip2 == False:
                        raise ValidationError(
                            "Segundo endereço do range DHCP não pertence à rede selecionada. Por favor, corrija.")

                if ip1  and ip2 :

                    start = re.split(r'(\.|/)', ip1)
                    end = re.split(r'(\.|/)', ip2)
                    ipstart = int(start[-1])
                    ipend = int(end[-1])
                    verificatamanho = ipstart < ipend
                    rede = ipaddress.ip_network(rm)
                    broadcast = rede.broadcast_address
                    e = self.address

                    if verificatamanho == False:
                        raise ValidationError("Primeiro IP do range DHCP deve ser menor que o Segundo")

                    if (ipaddress.ip_address(ip1) == broadcast) or (ipaddress.ip_address(ip2) == broadcast):
                        raise ValidationError("Endereço de broadcast não pode fazer parte do range de DHCP")

                    if (ipaddress.ip_address(ip1) == ipaddress.ip_address(e)) or (
                            ipaddress.ip_address(ip2) == ipaddress.ip_address(e)):
                        raise ValidationError("Endereço da rede não pode fazer parte do range de DHCP")

                start = re.split(r'(\.|/)', ip1)
                end = re.split(r'(\.|/)', ip2)
                ipstart = int(start[-1])
                ipend = int(end[-1])

                qtddhcp = len(range(ipstart, ipend + 1))

                if (qtddhcp + qtdfixos) > qtdipsrede:
                    raise ValidationError(
                        "Não é possível alocar mais IPs para DHCP nesta rede - Todos os IPs já estão em uso")

                dhcprange = findips(self.dhcp_start, self.dhcp_end)

                listaips = []
                for i in fixos:
                    listaips.append(str(i))

                # verifica se há ips fixos no dhcp
                checkfixosdhcp = set(listaips).intersection(set(dhcprange))

                if checkfixosdhcp:
                    raise ValidationError("Existe um Ip fixo configurado dentro do range de DHCP, por favor corrija.")






    def __unicode__(self):
        # return self.name
        #return u'%s (%s) - VLAN: %s' % (self.name, self.address, self.vln)
        return u'%s (%s)' % (self.name, self.address)


class Ownerid(models.Model):
    class Meta:
        verbose_name = u'Patrimônio'
        verbose_name_plural = u'Patrimônios'
        ordering = ['num']

    num = models.CharField(u'Número', max_length=100, unique=True)

    def __unicode__(self):
        return self.num


class Devicemodel(models.Model):
    class Meta:
        verbose_name = u'Modelo de equipamento'
        verbose_name_plural = u'Modelos de equipamento'
        ordering = ['name']

    name = models.CharField(max_length=200, verbose_name='Nome', unique=True)
    comments = models.TextField(u'Observações', max_length=2000, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Device(models.Model):
    class Meta:
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'
        ordering = ['name']

    name = models.CharField(u'Nome/Identificação', max_length=200, unique=True)
    active = models.BooleanField(u'Ativo/Em uso', default=True)
    ownerid = models.OneToOneField(Ownerid, verbose_name=u'Patrimônio', unique=True, null=True, blank=True,
                                   help_text=u"Patrimônio")
    devicemodel = models.ForeignKey(Devicemodel, verbose_name='Modelo do equipamento', on_delete=models.PROTECT,
                                    blank=True, null=True)
    url = models.URLField('URL', blank=True, null=True, help_text=u"Endereço de interface de administração web")
    admuser = models.CharField(u'Usuário administrador', max_length=100, blank=True, null=True)
    admpass = models.CharField(u'Senha do usuário administrador', max_length=50, blank=True, null=True)
    modification_date = models.DateTimeField(u'Data de modificação', editable=False, blank=True, null=True)
    groups = models.ManyToManyField(Group, verbose_name="Grupos", blank=True,
                                    help_text=u"Grupo de usuários relacionado. Aqueles que terão permissão de edição")
    comments = models.TextField(u'Observações', max_length=2000, blank=True, null=True)

    def save(self):
        # type: () -> object
        self.modification_date = datetime.datetime.today()
        super(Device, self).save()

    def __unicode__(self):
        return unicode(self.name)


class Ip(models.Model):
    class Meta:
        verbose_name = 'IP fixo'
        verbose_name_plural = 'IPs fixos'
        ordering = ['address']

    address = models.GenericIPAddressField(verbose_name=u"Endereço", unique=True, help_text="Ex: 10.0.0.1")
    network = models.ForeignKey(Network, verbose_name=u"Rede", on_delete=models.PROTECT, blank=True, null=True)
    # device = models.ForeignKey(Device,verbose_name='Dispositivo - Host,Switch ou Pilha',on_delete=models.PROTECT)
    device = models.ForeignKey(Device, verbose_name='Dispositivo - Host,Switch ou Pilha')
    modification_date = models.DateTimeField(u'Data de modificação', editable=False, blank=True, null=True)
    comments = models.TextField(u'Observações', max_length=2000, blank=True, null=True)

    # validacao
    def clean(self):

        try:
            e = self.address
            checkip = ipaddress.IPv4Address(e)

        except:
            raise ValidationError("Endereço informado não é um endereço IP válido")

        e = self.address
        r = self.network.address
        m = str(self.network.mask)
        rm = r + "/" + m
        verificarede = ipaddress.ip_address(e) in ipaddress.ip_network(rm)
        dhcp = self.network.dhcp

        if e and r:
            if e == r:
                raise ValidationError("Endereço de rede não pode ser cadastrado como IP fixo.")
        else:
            raise ValidationError("erro")

        if verificarede == False:
            raise ValidationError("Endereço IP não pertence à rede selecionada. Por favor, corrija.")

            # chacagem broadcast
        rede = ipaddress.ip_network(rm)
        broadcast = rede.broadcast_address

        if (ipaddress.ip_address(e) == broadcast):
            raise ValidationError("Endereço informado é o endereço de broadcast da rede. Por favor, corrija.")

        if dhcp == True:
            redeid = self.network.id
            qtdipsrede = len(list(ipaddress.ip_network(rm).hosts()))
            qtdfixos = Ip.objects.filter(network=redeid).count()

            ip1 = self.network.dhcp_start
            ip2 = self.network.dhcp_end
            rede = ipaddress.ip_network(rm)
            broadcast = rede.broadcast_address

            start = re.split(r'(\.|/)', ip1)
            end = re.split(r'(\.|/)', ip2)
            ipstart = int(start[-1])
            ipend = int(end[-1])
            dhcprange = range(ipstart, ipend + 1)
            a = re.split(r'(\.|/)', e)
            ip = int(a[-1])
            verificaip = ip in dhcprange

            qtddhcp = len(range(ipstart, ipend + 1))

            if (qtddhcp + qtdfixos) >= qtdipsrede:
                raise ValidationError("Não é possível cadastrar mais IPs nesta rede - Todos os IPs já estão em uso")

            if verificaip == True:
                raise ValidationError(
                    "Este endereço IP faz parte do range do DHCP da rede. Por favor cadastre um outro IP fixo.")

    def save(self):
        # type: () -> object
        self.modification_date = datetime.datetime.today()
        super(Ip, self).save()

    def __unicode__(self):
        return self.address


class Os(models.Model):
    class Meta:
        verbose_name = 'Sistema operacional'
        verbose_name_plural = 'Sistemas operacionais'
        ordering = ['name']

    name = models.CharField(u'Nome', max_length=30)
    version = models.CharField(u'Versão', max_length=20, blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s' % (self.name, self.version)


#class Hosttype(models.Model):
#    class Meta:
#        verbose_name = 'Equipamento - Tipo'
#        verbose_name_plural = 'Equipamento - Tipos'
#        ordering = ['name']

#    name = models.CharField('Nome', max_length=50)

#    def __unicode__(self):
#        return unicode(self.name)


class Host(Device):
    class Meta:
        verbose_name = 'Equipamento '
        verbose_name_plural = 'Equipamento'
        ordering = ['name']

    LINUX = 'linux'
    WINDOWS = 'windows'
    BSD = 'bsd'
    OTHER = 'other'
    OS_PLAT_CHOICES = (
        ('', '---------'),
        (LINUX, 'Linux'),
        (WINDOWS, 'Windows'),
        (BSD, 'BSD/MacOS X'),
        (OTHER, 'Outros'),
    )

    AP = 'ap'
    CAM = 'cam'
    CFTV = 'cftv'
    DESKTOP = 'desktop'
    FW = 'fw'
    MEDIA = 'media'
    PHONE = 'voip'
    PRINTER = 'printer'
    ROUTER = "router"
    SERVER = 'server'
    STORAGE = 'storage'
    VIRT = 'virt'
    WIFI = 'wifi'
    OTHER = 'other'
    HWTYPE_CHOICES = (
        ('', '---------'),
        (AP, 'Access Point'),
        (CAM, 'Camera IP'),
        (CFTV, 'Equipamento de CFTV'),
        (DESKTOP, 'Destkop'),
        (FW, 'Firewall/UTM'),
        (MEDIA, 'Servidor de Media/Audio/Video'),
        (PHONE, 'Telefone ou Equipamento VOIP'),
        (PRINTER, 'Impressora/Scanner'),
        (ROUTER, 'Roteador'),
        (SERVER, 'Servidor de rede'),
        (STORAGE, 'Storage/Equipamento de armazenamento/Backup'),
        (VIRT, 'Servidor Virtualização'),
        (WIFI, 'Controladora WIFI'),
        (OTHER, 'Outros'),
    )

    supplierhw = models.BooleanField(u'Equipamento de terceiros', default=False)
    vm = models.BooleanField(u'Máquina Virtual', default=False)
    serial_number = models.CharField(u'Num de série', max_length=30, blank=True, null=True, unique=True)
    os = models.ForeignKey(Os, verbose_name=u'Sistema Operacional', blank=True, null=True)
    hwtype = models.CharField(u'Tipo de equipamento', blank=True, max_length=20, choices=HWTYPE_CHOICES,
                              default='other')
    osplatform = models.CharField(u'Plataforma de sistema operacional', max_length=20, choices=OS_PLAT_CHOICES,
                                  default='other')
    manufactorer = models.ForeignKey(Manufactorer, blank=True, null=True, verbose_name=u'Fabricante')
    mem = models.CharField(u'Memória instalada. Ex: 2GB', max_length=20, blank=True, null=True)
    cpu = models.IntegerField(u'Quantidade de CPUS', blank=True, null=True)
    place = models.ForeignKey(Place, verbose_name=u'Localização', null=True, blank=True,
                              help_text=u"Onde o equipamento está instalado (Não se aplica à máquinas virtuais)")
    # tags = TaggableManager()
    # diskspace
    # lastupdate = = models.DateTimeField('Ultima atualização', blank=True, null=True)
    # warranty = models.DateTimeField('Garantia', blank=True, null=True)
    # os_key = models.CharField(u'Chave/Registro do S.O.,max_length=100, blank=True, null=True)
    changed_by = models.ForeignKey(User, related_name="host_changed_by", null=True, blank=True)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value    


    def clean(self):

        v = self.vm
        s = self.serial_number
        p = self.ownerid
        sh = self.supplierhw

        if v == False:

            if p == None and sh == False:
                raise ValidationError("Campo Patrimônio é obrigatório para máquinas físicas")

        if v == True:

            if p != None:
                raise ValidationError(
                    "Campo Patrimônio só deve ser usado em máquinas físicas e de propriedade da instituição")

    def save(self, *args, **kwargs):
        # type: (object, object) -> object

        if not self.serial_number:
            self.serial_number = None

        super(Host, self).save(*args, **kwargs)

        #Log.objects.create(record_name=self.name, event_date=self.modification_date, record_type="host", actor="user")

    def __unicode__(self):
        return unicode(self.name)


class Hostupdate(models.Model):
    class Meta:
        verbose_name = u'Atualizacão'
        verbose_name_plural = u'Atualizações'
        ordering = ['aplication_date']

    name = models.CharField(u'Nome/Identificação', max_length=100, help_text=u"Identificação da atualização aplicada")
    aplication_date = models.DateField(u'Data de aplicação', blank=True, null=True)
    register_date = models.DateTimeField(u'Data de registro', blank=True, null=True, editable=False, auto_now_add=True)
    host = models.ForeignKey(Host, verbose_name='Dispositivo', on_delete=models.PROTECT)
    comments = models.CharField(u'Observações', max_length=300, blank=True)

    def __unicode__(self):
        return unicode(self.name)


class Printer(Device):
    class Meta:
        verbose_name = 'Impressora'
        verbose_name_plural = 'Impressoras'
        ordering = ['name']

    PRINT = '1'
    MULTI = '2'
    SCAN = '3'
    OTHER = '4'
    TYPE_CHOICES = (
        ('', '---------'),
        (PRINT, 'Impressora'),
        (MULTI, 'Multifuncional'),
        (SCAN, 'Scanner'),
        (OTHER, 'Outros'),
    )

    serial_number = models.CharField(u'Num de série', max_length=30, blank=True, null=True, unique=True)
    supplierhw = models.BooleanField(u'Equipamento de terceiros', default=False)
    manufactorer = models.ForeignKey(Manufactorer, blank=True, null=True, verbose_name=u'Fabricante')
    # model = models.CharField(u'Modelo', max_length=30, blank=True, null=True)
    place = models.ForeignKey(Place, verbose_name=u'Localização', null=True, blank=True)
    printer_type = models.CharField(u'Tipo de equipamento', max_length=20, choices=TYPE_CHOICES, default='1',
                                    help_text=u"Obrigatório")
    changed_by = models.ForeignKey(User, related_name="printer_changed_by", null=True, blank=True)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value   

    def clean(self):

        if not self.ownerid and not self.supplierhw:
            raise ValidationError("Campo Patrimônio é obrigatório")             

    # def save(self, *args, **kwargs):

    #    if not self.serial_number:
    #        self.serial_number = None

    #    super(self, Printer).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.name)


class Servicecategory(models.Model):
    class Meta:
        verbose_name = u'Serviços - categoria'
        verbose_name_plural = u'Serviços - categorias'
        ordering = ['name']

    name = models.CharField('Nome', max_length=100)

    def __unicode__(self):
        return unicode(self.name)


class Service(models.Model):
    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['name']

    name = models.CharField('Nome', max_length=100)
    network = models.ForeignKey(Network, verbose_name="Rede", blank=True, null=True)
    ip = models.ForeignKey(Ip, verbose_name=u"Endereço IP", blank=True, null=True)
    category = models.ManyToManyField(Servicecategory, verbose_name="Categoria", blank=True)
    modification_date = models.DateTimeField(u'Data de modificação', editable=False, blank=True, null=True)
    obs = models.CharField(u'Observações', max_length=100, blank=True)

    def save(self):
        # type: () -> object
        self.modification_date = datetime.datetime.today()
        super(Service, self).save()

    def __unicode__(self):
        return unicode(self.name)


class Stack(Device):
    class Meta:
        verbose_name = 'Switches - Pilha'
        verbose_name_plural = 'Switches - Pilhas'
        ordering = ['name']

    def __unicode__(self):
        return unicode(self.name)


class SwitchManager(models.Manager):
    def get_queryset(self):
        query_set = super(SwitchManager, self).get_queryset()

        return query_set.extra(
            select={
                '_ports_total': 'SELECT COUNT(*) FROM ace_switchport where ace_switchport.switch_id = ace_switch.device_ptr_id',
            },
        )


class Switch(Device):
    class Meta:
        verbose_name = 'Switch'
        verbose_name_plural = 'Switches'
        ordering = ['name']

    #model = models.CharField('Modelo', max_length=200, help_text=u"Obrigatório")
    serial = models.CharField('Num. Serie', max_length=30, blank=True, null=True)
    place = models.ForeignKey(Place, verbose_name=u'Localização', blank=True, null=True)
    rack = models.ForeignKey(Rack, blank=True, null=True)
    ports = models.IntegerField('Num. Portas', help_text=u"Obrigatório")
    manageable = models.BooleanField(verbose_name=u'Gerenciável (Individualmente)', default=False)
    manufactorer = models.ForeignKey(Manufactorer, blank=True, null=True, verbose_name=u'Fabricante')
    stacked = models.BooleanField('Empilhado', default=False)
    stack_field = models.ForeignKey(Stack, verbose_name='Pilha', blank=True, null=True)
    # warranty = models.DateTimeField('Garantia', blank=True, null=True)
    snmp = models.BooleanField(u'Habilitado para SNMP?', default=False, editable=False)
    snmpcom = models.CharField(u'SNMP Community - RO', max_length=25, blank=True, null=True, editable=False)
    objects = SwitchManager()
    changed_by = models.ForeignKey(User, related_name="switch_changed_by", null=True, blank=True)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


    def ports_total(self):
        return self._ports_total or 0

    # validacao
    def clean(self):
        g = self.manageable
        # o = self.ownerid
        u = self.url
        user = self.admuser
        pwd = self.admpass

        # if o == None:
        #    raise ValidationError("Campo Patrimônio é obrigatório")

        if self.active:
            if not self.rack:
                raise ValidationError("Um switch ativado deve estar instalado em um rack")

        if self.stacked:
            if not self.stack_field:
                raise ValidationError("Necessário selecionar a pilha a que o switch pertence")

            if self.url:
                raise ValidationError("Switch empilhado não deve conter endereço de interface de gerência")

            if not self.active:
                raise ValidationError("Um switch empilhado deve estar ativado")

        if not self.stacked:

            if self.stack_field:
                raise ValidationError("Campo pilha deve ser preenchico apenas se o switch estiver empilhado")

        if g == True:
            if u == u'':
                raise ValidationError("Switch gerenciável - Informe o endereço da interface de gerência do switch")

            if user == u'':
                raise ValidationError("Switch gerenciável - Informe nome do usuário")

            if pwd == u'':
                raise ValidationError("Switch gerenciável - Informe senha")

    def __unicode__(self):
        # return self.name
        if self.rack:
            return u'%s (%s)' % (self.name, self.rack.name)
        else:
            return u'%s' % (self.name)


class Patchpanel(models.Model):
    class Meta:
        verbose_name = 'Patch Panel'
        verbose_name_plural = 'Patch Panels'
        ordering = ['num']

    num = models.CharField('Num/Id', max_length=50)
    rack = models.ForeignKey(Rack)
    ports = models.IntegerField(verbose_name=u'nº de portas')

    def clean(self):

        try:

            pp = Patchpanel.objects.all().filter(num=self.num, rack=self.rack).exclude(pk=self.id)
            if pp:
                raise ValidationError(u"Este patchpanel já foi cadastrado neste rack")

        except:
            raise ValidationError(u"Verifique o preenchimento dos campos abaixo")

    def __unicode__(self):
        return u'%s (%s)' % (self.num, self.rack)
        # return self.num


class Patchpanelport(models.Model):
    class Meta:
        verbose_name = 'Patch panel - porta'
        verbose_name_plural = 'Patch panel - portas'
        ordering = ['num']

    num = models.CharField('Num/Id da Porta', max_length=60)
    patchpanel = models.ForeignKey(Patchpanel)
    comments = models.TextField(u'Observações', max_length=2000, blank=True)

    """

            verificar portas_cadastradas - pegando todas as portas....
            Portasw.objects.get(id=1).switch.portas .
            Portasw.objects.all().filter(switch="1").count()

    """

    def clean(self):

        pp = Patchpanelport.objects.all().filter(num=self.num, patchpanel=self.patchpanel).exclude(pk=self.id)

        if pp:
            raise ValidationError("Esta porta já foi cadastrada neste patchpanel")

        portas_cadastradas = Patchpanelport.objects.all().filter(patchpanel=self.patchpanel).count()
        portas_disponiveis = self.patchpanel.ports
        if portas_disponiveis <= portas_cadastradas:
            raise ValidationError("O switch selecionado ja possui todas as portas ocupadas")

    def __unicode__(self):
        return '%s (%s)' % (self.num, self.patchpanel)


class Phonecategory(models.Model):
    class Meta:
        verbose_name = 'Telefone/ramal - Categoria/Classe'
        verbose_name_plural = 'Telefone/ramal - Categorias'
        ordering = ['name']

    name = models.CharField(u'Descrição', max_length=100, unique=True)

    def __unicode__(self):
        return unicode(self.name)


class Phonetype(models.Model):
    class Meta:
        verbose_name = 'Telefone - Tipo/tecnologia de telefone'
        verbose_name_plural = 'Telefone - Tipo/tecnologia de telefone'
        ordering = ['name']

    name = models.CharField(max_length=100, unique=True, help_text="Digital, analógico, IP")
    comments = models.TextField(u'Observações', max_length=2000, blank=True)

    def __unicode__(self):
        return unicode(self.name)


class Phone(models.Model):
    class Meta:
        verbose_name = 'Telefone/Senha'
        verbose_name_plural = 'Telefones/Senhas'
        ordering = ['num']
        permissions = (
            ("view_password", "Can see password"),
            ("change_password", "Can change password"),
        )

    num = models.CharField('Número', max_length=14, unique=True, help_text='Número do ramal ou código da senha')
    user = models.ForeignKey(Person, blank=True, null=True, verbose_name=u'Usuário')
    place = models.ForeignKey(Place, verbose_name=u'Local', blank=True, null=True)
    active = models.BooleanField(default=False, verbose_name='Ativo', help_text='Indica se número está em uso ou não')
    password = models.BooleanField(default=False, verbose_name='É senha',
                                   help_text='Indica se número se refere a uma senha')
    #newpassword = models.BooleanField(default=True, verbose_name='Senha nova',
    #                                  help_text='Indica se a senha é nova ou não')
    phonecategory = models.ForeignKey(Phonecategory, verbose_name=u'Categoria', blank=True,
                                      null=True, help_text='Indica o tipo de chamada telefônica permitida')
    telephonetype = models.ForeignKey(Phonetype, verbose_name=u'Tipo/tecnologia', blank=True, null=True,
                                      help_text="Digital, analógico, IP")
    phonehw = models.CharField('Aparelho telefônico', max_length=50, help_text='Identificação do aparelho telefônico', blank=True, null=True)
    comments = models.TextField(u'Observações', max_length=2000, blank=True)
    date_creation = models.DateField(u'Data de cadastro', editable=False)
    date_modification = models.DateTimeField(u'Data de modificação', editable=False)
    dist = models.IntegerField(blank=True, null=True, help_text="Posição no quadro de distribuição")
    bloco = models.IntegerField(blank=True, null=True, help_text="Identificação no bloco")
    par = models.IntegerField(blank=True, null=True, help_text="posição no bloco")
    dg = models.IntegerField(blank=True, null=True, help_text="identificação ou posição no DG")
    changed_by = models.ForeignKey(User, related_name="phone_changed_by", null=True, blank=True)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def clean(self):

        p = self.password
        pl = self.place
        a = self.active
        u = self.user
        #n = self.newpassword

        if p == True:
            if pl != None:
                raise ValidationError("Senhas não são associadas a locais")
            #if a == True:
            #    if u == None:
            #        raise ValidationError("Campo Usuário é obrigatório para senhas ativas")
            if u and not self.phonecategory:
                    raise ValidationError("Informe a categoria ou tipo de ligação que esta senha poderá realizar")

                #if n == True:
                #    raise ValidationError("Senhas novas ou disponíveis devem estar desativadas")
            #if a == False:
                # if n == False:
                #    if u == None:
                #        raise ValidationError("Nome do antigo usuário é obrigatório para senhas desativadas")
                #if n == True:
                #    if u != None:
                #        raise ValidationError("Senhas novas não podem estar associadas a usuários")

        if a == True:

            #    if u == None:
            #        raise ValidationError("Campo Usuário é obrigatório")

            if p == False:

                if pl == None:
                    raise ValidationError("Campo local é obrigatório")

    def save(self):
        # type: () -> object
        if not self.id:
            self.date_creation = datetime.date.today()
        self.date_modification = datetime.datetime.today()
        super(Phone, self).save()

    def __unicode__(self):
        return unicode(self.num)


class Phoneownership(models.Model):
    class Meta:
        verbose_name = 'Posse de telefone'
        verbose_name_plural = 'Posses de telefone'

    active = models.BooleanField(editable=False, default=True, verbose_name="Ativo(a)")
    phone = models.ForeignKey(Phone, blank=True, null=True, verbose_name='Telefone')
    user = models.ForeignKey(Person, blank=True, null=True, verbose_name=u'Usuário')
    date_activation = models.DateTimeField(u'Data de ativação', blank=True, null=True, editable=False,
                                           auto_now_add=True)
    date_deactivation = models.DateTimeField(u'Data de desativação', blank=True, null=True, editable=False)


    def save(self):
        # type: () -> object
        if not self.id:
            # self.date_activation = datetime.date.today()
            self.active = True
        super(Phoneownership, self).save()

    def __unicode__(self):
        return unicode(self.user.get_full_name())


class Switchport(models.Model):
    class Meta:
        verbose_name = 'Switch - Porta'
        verbose_name_plural = 'Switch - Portas'
        ordering = ['num']

    UTP = 'UTP'
    FIBRA = 'Fibra'
    TIPO_PORTA_CHOICES = (
        (UTP, 'UTP'),
        (FIBRA, 'Fibra'),
    )
    num = models.IntegerField('Num da Porta', )
    # vlan = models.IntegerField(blank=True,null=True)
    vlans = models.ManyToManyField(Vlan, verbose_name='VLANs', blank=True)
    # vln = models.ForeignKey(Vlan,verbose_name='VLAN',blank=True,null=True,related_name="vln")
    switch = models.ForeignKey(Switch)
    tipo = models.CharField(max_length=20, choices=TIPO_PORTA_CHOICES)
    #host = models.ForeignKey(Host, blank=True, null=True)
    host = models.ForeignKey(Device, blank=True, null=True, related_name='swport_host')
    obs = models.CharField(u'Observações', max_length=100, blank=True)

    """

            verificar portas_cadastradas - pegando todas as portas....
            Portasw.objects.get(id=1).switch.portas .
            Portasw.objects.all().filter(switch="1").count()

    """

    def clean(self):
        portas_cadastradas = Switchport.objects.filter(switch=self.switch).count()
        portas_disponiveis = self.switch.ports
        if portas_disponiveis <= portas_cadastradas:
            raise ValidationError("O switch selecionado ja possui todas as portas ocupadas")

        porta = Switchport.objects.all().filter(num=self.num, switch=self.switch, tipo=self.tipo).exclude(pk=self.id)
        if porta:
            raise ValidationError("Já existe uma porta com este número neste switch")

        # if self.host != None:
        #    p = Switchport.objects.filter(host=self.host).exclude(pk = self.id)
        #    if p:
        #        raise ValidationError("Já existe uma porta associada a este host")

    def __unicode__(self):
        # return u'%s (%s)' % (self.num, self.switch.name)
        return u'%s' % (self.num)


class Netpoint(models.Model):
    class Meta:
        verbose_name = 'Ponto de rede'
        verbose_name_plural = 'Pontos de rede'
        ordering = ['num']

    DESATIVADO = 'desativado'
    DADOS = 'dados'
    VOZ = 'voz'
    VOIP = 'voip'
    TIPO_PONTO_CHOICES = (
        ('', '---------'),
        (DESATIVADO, 'Desativado'),
        (DADOS, 'Dados'),
        (VOZ, 'Voz'),
        (VOIP, 'VoIP'),
    )

    num = models.CharField('Num/Id', max_length=10)
    pointtype = models.CharField(max_length=20, default='desativado', choices=TIPO_PONTO_CHOICES, verbose_name='Tipo')
    rack = models.ForeignKey(Rack, blank=True, null=True)
    patchpanel = models.ForeignKey(Patchpanel, blank=True, null=True)
    patchpanelport = models.ForeignKey(Patchpanelport, blank=True, null=True, verbose_name=u'Porta do patchpanel')
    switch = models.ForeignKey(Switch, blank=True, null=True)
    swport = models.ForeignKey(Switchport, blank=True, null=True, verbose_name='Porta do switch')
    place = models.ForeignKey(Place, verbose_name='Localização', blank=True, null=True,
                              help_text='localização do ponto de rede')
    phone = models.ForeignKey(Phone, blank=True, null=True, verbose_name='Telefone/Ramal',
                              help_text='Telefone associado ao ponto de rede')
    # dist = models.IntegerField(blank=True, null=True)
    # bloco = models.IntegerField(blank=True, null=True)
    # par = models.IntegerField(blank=True, null=True)
    # dg = models.IntegerField(blank=True, null=True)
    comments = models.TextField(u'Observações', max_length=2000, blank=True)
    creation_date = models.DateField(u'Data de cadastro', editable=False)
    modification_date = models.DateTimeField(u'Data de modificação', editable=False)

    # validacao
    def clean(self):
        t = self.pointtype
        r = self.phone
        # d = self.dist
        # b = self.bloco
        # p = self.par
        # dg = self.dg
        l = self.place
        s = self.switch
        ps = self.swport
        pp = self.patchpanel
        ppp = self.patchpanelport
        rck = self.rack

        points = Netpoint.objects.filter(phone=self.phone).exclude(pk=self.id)

        if t == 'voz' or t == 'voip':
            if points and self.phone != None:
                raise ValidationError("Já existe um ponto de rede relacionado a este ramal")

        if rck == None:
            raise ValidationError("Ponto deve estar ligado a um rack")

        """ Validação de Patchpanel - Descomente os trechos abaixo para forçar o cadastro obrigatório de patchpanel e portas """
        # if pp == None:
        #    raise ValidationError("Ponto deve estar ligado a um patchpanel")

        # if ppp == None:
        #    raise ValidationError("Ponto deve estar ligado a uma porta de patchpanel")

        if t == 'desativado':

            if l == None:
                raise ValidationError("Preencha o local do ponto")

            if r != None:
                raise ValidationError("Pontos desativados não possuem ramal associado")

            if s != None:
                raise ValidationError("Pontos desativados não devem ter um switch associado.")

            if ps != None:
                raise ValidationError("Pontos desativados não devem ter uma porta de switch associada.")

        if t == 'dados':

            if r != None:
                raise ValidationError("Ponto do tipo dados não possui ramal")

            # if d != None:
            #    raise ValidationError("Ponto do tipo dados não possui campo dist")

            # if b != None:
            #    raise ValidationError("Ponto do tipo dados não possui campo bloco")

            # if p != None:
            #    raise ValidationError("Ponto do tipo dados não possui campo par")

            # if dg != None:
            #    raise ValidationError("Ponto do tipo dados não possui campo dg")

        """ Validação de Switch - Descomente os trechos abaixo para forçar o cadastro obrigatório de switch e porta de switch """

        # if s == None:
        #        raise ValidationError("Pontos de dados devem ter um switch associado.")

        # if ps == None:
        #        raise ValidationError("Pontos de dados devem ter uma porta de switch associada.")

        if s != None:
            if ps == None:
                raise ValidationError("Porta de switch deve ser preenchida")

            if ps.switch != s:
                raise ValidationError("Esta porta de switch não pertence ao switch selecionado")

            ponto = Netpoint.objects.filter(switch=s, swport=ps).exclude(pk=self.id)
            if ponto:
                raise ValidationError("A porta de switch selecionada já está ligada a outro ponto de rede")

        # Checar e testar melhor verificaçoes abaixo

        # if s != None:
        #    switchrack = self.switch.rack
        #    switchporta = self.swport.switch
        #    patchrack = self.patchpanelport.patchpanel.rack
        #    if switchrack != None:
        #        if patchrack != switchrack:
        #            raise ValidationError("Patchpanel da porta selecionada não está localizado no mesmo rack do switch.")
        #    if s != switchporta:
        #        raise ValidationError("Porta de switch cadastrada não está localizada no switch selecionado anteriormente.")

        if t == 'voz':

            if r == None:
                raise ValidationError("Pontos de voz ativos devem ter um ramal associado.")

            if s != None:
                raise ValidationError("Pontos de voz não são ligados a switches.")

            localramal = self.phone.place
            if l != localramal:
                raise ValidationError("Ramal selecionado não está localizado no mesmo local do ponto de rede.")

        if t == 'voip':

            # if d != None:
            #    raise ValidationError("Ponto do tipo VoIP não possui campo dist")

            # if b != None:
            #    raise ValidationError("Ponto do tipo VoIP não possui campo bloco")

            # if p != None:
            #    raise ValidationError("Ponto do tipo VoIP não possui campo par")

            # if dg != None:
            #    raise ValidationError("Ponto do tipo VoIP não possui campo dg")

            if r == None:
                raise ValidationError("Pontos do tipo VoIP devem ter um ramal associado.")

            if s == None:
                raise ValidationError("Pontos do tipo VoIP devem ter um switch associado.")

            if s != None:
                switchrack = self.switch.rack
                switchporta = self.swport.switch
                patchrack = self.patchpanelport.patchpanel.rack
                if switchrack != None:
                    if patchrack != switchrack:
                        raise ValidationError(
                            "Porta do patchpanel selecionada não está localizada no mesmo rack do switch.")
                if s != switchporta:
                    raise ValidationError(
                        "Porta de switch cadastrada não está localizada no switch selecionado anteriormente.")

        # pp -> patchpanel
        if pp != None:
            ponto = Netpoint.objects.all().filter(num=self.num, patchpanel=pp).exclude(pk=self.id)
            if ponto:
                raise ValidationError("Já exite um ponto de rede com este número cadastrado neste patchpanel.")

        if l != None:
            ponto = Netpoint.objects.all().filter(num=self.num, place=self.place).exclude(pk=self.id)
            if ponto:
                raise ValidationError("Já existe um ponto de rede com este número neste local.")

    def save(self):
        # type: () -> object
        if not self.id:
            self.creation_date = datetime.date.today()
        self.modification_date = datetime.datetime.today()
        super(Netpoint, self).save()

    def __unicode__(self):
        return self.num



