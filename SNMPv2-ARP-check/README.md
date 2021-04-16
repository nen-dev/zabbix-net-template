# ARP Check


This script help to process ipNetToMediaPhysAddress.
This script obtain "#ARPINDEX" (part of OID = interface ID + ip) to constrain ipNetToMediaPhysAddress OID:
"1.3.6.1.2.1.4.22.1.2" + "." + interface ID + "." + ip =
"1.3.6.1.2.1.4.22.1.2" + {#ARPINDEX}

Also it gets:

{#ARPIFNAME} - Name of the interface (Example: Vl900 - VLAN 900)

{#ARPIP} - IP row from ARP Cache




1. Uncomment ExternalScripts in zabbix.conf or zabbix_proxy.conf

2. Copy file snmpv2-arp.py to $ExternalScripts

3. Run this*: 


```console

echo '#!/bin/bash
python3 /usr/lib/zabbix/externalscripts/snmpv2-arp.py $1 $2
' > /usr/lib/zabbix/externalscripts/snmpv2-arp-bash.sh

```

* there is an issue to run python3 file (slowdown server, I do not know why)

4. Import template ARP Check.xml to your Zabbix Server



