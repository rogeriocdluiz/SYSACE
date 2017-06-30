
from fabric.api import *


def mem():
    output=run("free -m|awk '/^Mem:/{print $2}'")
    

def cpu():
    output=run("getconf _NPROCESSORS_ONLN")
    


