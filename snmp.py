#Testes de uso de snmp

#Mais em https://wiki.debian.org/SNMP

#http://easysnmp.readthedocs.io/en/latest/

from easysnmp import snmp_get, snmp_set, snmp_walk




snmp_walk('system', hostname='10.65.3.20', community='r_prdf_public', version=1)

snmp_walk(hostname='10.65.3.20', community='r_prdf_public', version=1) 
