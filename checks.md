State: March 2025
# compute
#### instances (D)
 - template EoL
 - default user of template still enabled?
 - authorized or publicly available?
 - 80 % of instances in same zone
 - Creation Date older than a year?
 - Instance Public facing?
 - - specific ports exposed to internet (sec-group + instance public)
    - cassandra (TCP 7000, 7001, 7199, 9042, 9160)
    - elasticsearch/kibana
    - cifs
    - ftp
    - kafka
    - kerberos
    - ldap
    - memcached
    - mongodb/mysql/oracle/postgresql/redis/sqlserver
    - ssh/rdp/telnet
    - smtp
    - ingress from any to all
    - ingress from any to any
    - high risk tcp ports (25(SMTP), 110(POP3), 135(RCP), 143(IMAP), 445(CIFS), 3000(Go, Node.js, and Ruby web developemnt frameworks), 4333(ahsp), 5000(Python web development frameworks), 5500(fcp-addr-srvr1), 8080(proxy), 8088(legacy HTTP port))
    - allow wide open public ipv4
    - allow wide open public ipv6
    - userdata contains passwords

#### instance pools

#### sks 

#### block storage (D)
 - block storage volumes
   - creation date old
   - correspondig snapshot exists(backup?)
 - block storage snapshots
   - creation date old

#### templates (D)
template public (visibility)
password login disabled and no sshkey? no login - still pays


#### security groups (D)
 - specific ports exposed to internet (sec-group only)
    - cassandra (TCP 7000, 7001, 7199, 9042, 9160)
    - elasticsearch/kibana
    - cifs
    - ftp
    - kafka
    - kerberos
    - ldap
    - memcached
    - mongodb/mysql/oracle/postgresql/redis/sqlserver
    - ssh/rdp/telnet
    - smtp
    - ingress from any to all
    - ingress from any to any
    - high risk tcp ports (25(SMTP), 110(POP3), 135(RCP), 143(IMAP), 445(CIFS), 3000(Go, Node.js, and Ruby web developemnt frameworks), 4333(ahsp), 5000(Python web development frameworks), 5500(fcp-addr-srvr1), 8080(proxy), 8088(legacy HTTP port))
    - allow wide open public ipv4
    - allow wide open public ipv6
 - default security group restricts all traffic
 - security group not used
 - security group has many ingress/egress rules (50)


#### elastic ip (D)
Elastic IP Shodan?
Elastic IP unassigned

#### load balancers 

#### private networks

#### ssh-keys (D)
Info - are all ssh-keys used?

#### Anti-Affinity Groups



# ideas
key-age -> IAM 

# impossible
XX - ssh-key-age: data not available 
XX - snapshots encrypted : data not available



    