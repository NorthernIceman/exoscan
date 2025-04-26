State: March 2025
# compute ca.90
#### instances (D) 27
 - instance type large -> does it need to be this large?
 - gpus to instances attributed - necessary?
 - template EoL
 - default user of template still enabled?
 - authorized or publicly available?
 - 80 % of instances in same zone
 - ***created long ago***
 - ***no snapshot for instance***
 - Instance Public facing?
 - userdata contains passwords
 - default sec-group used
 - specific ports exposed to internet (sec-group + instance public)
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
   

#### instance pools (D) 21
 - instance pool uses no anit-affinity group
 - user data contains passwords
 - created long ago
 - state error?
 - extensively many nodes in nodepool?
 - specific ports exposed to internet (sec-group + instance public)
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

#### sks (D) 9+
 - auto-upgrade enabled?
 - cluster state error?
 - creation date is old
 - control plane version outdated?
 - Nodepools:
   - extra-large types ?
   - default-security groups?
   - Anti-Affinity-groups?
   - specific ports exposed to the internet? (look at ports from instances)
   - extensively many nodes in nodepool?

#### block storage (D) 3
 - block storage volumes
   - creation date old
   - correspondig snapshot exists(backup?)
 - block storage snapshots
   - creation date old

#### templates (D) 1
template public (visibility)



#### security groups (D) 20
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


#### elastic ip (D) 2
Elastic IP Shodan?
Elastic IP unassigned

#### load balancers (D) 4+
 - service is internet facing
 - health check interval too big
 - health check retries too high
 - health check timeout too high

#### private networks (D) 2
 - any dangers with too big private networks?
 - maybe subnet almost full - threshold of 80% of ip leases of network

#### ssh-keys (D) 1
Info - are all ssh-keys used?

#### Anti-Affinity Groups (D) 0
no checks itself, but influences other services

# Storage ca.15

#### Buckets (D) 14+
 - how old is bucket?
 - CORS rules: https://<bucket-name>.sos-ch-dk-2.exo.io/?cors
 - ACLs? Analysis with boto3 
   - Cross Account access?
   - Public Write?
   - public Access?
   - Public List ACL?
   - Public Write ACL?
 - Versioning enabled?
 - Object Lock?
 - cross region replication?


# DBaaS (ca. 47)
 - more than 80% of db in same region?
 - certificate expiration?
 - deprecated engine version?

#### PostgreSQL (8)
   - Termination Protection?
   - Backups in last 30/20 days? 
   - SSL Mode required?
   - defaultuser (avnadmin)?
   - password of a user not strong enough?
   - ipfilter 0.0.0.0/0? /8? /16 (/24)?
   - password encryption md5?
   - default port?


#### OpenSearch (8)
 - termination protection?
 - default user (avnadmin?)
 - recent backups?
 - ip filter -> too large subnet?
 - user password weak?
 - default port?
 - OpenSearch - ACL
 - service settings?

#### Kafka (7)
 - default port?
 - termination protection?
 - ip filter? 
 - username/password default/weak
 - Kafka ACL
 - Schema Registry ACL
 - DB Settings?


#### Valkey (6)
  - termination protection?
  - recent backups?
  - ip filter too large?
  - default users
  - weak passwords
  - db settings: ssl?...

#### Grafana (6)
 - termination protection?
 - default port? 
 - ip-filter?
 - default users?
 - weak passwd?
 - insecure service settings?

#### MySQL (8)
 - termination protection?
 - ssl required?
 - backups recent?
 - ip filter detailed? 
 - databasename default?
 - user default
 - password weak
 - insecure db settings?

# DNS (ToDo)


# IAM (ca. 10, ToDo?)
 - mandate 2FA
 - avoid use of default user
 - administrator access without mfa
 - policy allows priviledge escalation
 - ensure inline policies that allow full \"*:*\" administrative privileges are not associated to IAM identities
 - no full access to iam
 - organization policy is allow all/standard
 - too many owner accounts
 - allow action before later deny action => short circuits and allows action nonetheless
 - don't mix resources in a single rule

# Organization (1)
 - Quotas almost depleted

# sum: 
162 checks to be written in 6 categories


# ideas
key-age -> IAM 
state -> error: retreve all with state error (inventory?)
password login disabled and no sshkey? no login - still pays
check certificate stuff in sks?

# impossible
XX - ssh-key-age: data not available 
XX - snapshots encrypted : data not available
XX - ACL Analysis: no ACLs



    