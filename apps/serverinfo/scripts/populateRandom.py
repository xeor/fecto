import sys
import random
import string
import datetime
import ipaddr

from apps.serverinfo.models import Server, AttributeType, Vlan, IP, AttributeValue, AttributeMapping

def getRandomIP():
    randchoise = random.randint(1,5)
    if randchoise == 1:
        return ipaddr.IPv4Address(random.randint(100000000, 1000000000)) # Between '5.245.225.0' and '59.154.202.0'

    if randchoise in [2,3,3]:
        subnet = ipaddr.IPNetwork(random.choice([ n.network for n in Vlan.network_objects.all() ]))
        return random.choice(list(subnet.iterhosts()))

    return None

def run():
    count = 1000
    print 'Generating %s random servers with some random attributes and ip adresses on each' % str(count)
    print

    randWords = 'yes no some random words used in example the names values the servers below hello yes no'.split(' ')
    randChars = string.ascii_letters + string.digits

    for i in range(count):
        serverObj = Server()
        serverObj.name = ''.join([ random.choice(randChars) for _ in range(random.randint(4,12)) ]) + '-' + str(i)
        serverObj.function = ' '.join([ random.choice(randWords) for _ in range(random.randint(0,10)) ])
        serverObj.description = ' '.join([ random.choice(randWords) for _ in range(random.randint(0,20)) ])
        serverObj.status = random.randint(1,5)

        randTime = datetime.datetime.now() - datetime.timedelta(seconds=random.randint(1000,4000000))
        serverObj.reg_time = randTime
        serverObj.upd_time = randTime + datetime.timedelta(seconds=random.randint(1000,100000))
        serverObj.save() # So we will get an primary key..

        for ipCount in range(random.randint(1,5)):
            randomIP = getRandomIP()
            if not randomIP:
                continue
            randomIP = str(randomIP)

            try:
                ipObj = IP.objects.get(ip=randomIP)
            except IP.DoesNotExist:
                ipObj = IP()
                ipObj.ip = randomIP
                ipObj.save()
            serverObj.ip.add(ipObj)
        serverObj.save()

        for attrCount in range(random.randint(1, 3)):
            randomAttr = random.choice(AttributeType.objects.all())
            attrValueObj = AttributeValue()
            attrValueObj.value = random.choice(randWords)
            attrValueObj.save()
            attrMapObj = AttributeMapping()
            attrMapObj.attributeType = randomAttr
            attrMapObj.attributeValue = attrValueObj
            attrMapObj.server = serverObj
            attrMapObj.save()

        print serverObj.name
