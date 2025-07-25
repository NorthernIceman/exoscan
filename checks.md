State: March 2025
# compute ca.90 y
#### instances (D) 27 y
 - ***instance type large -> does it need to be this large?***
 - ***gpus to instances attributed - necessary?***
 - ***template EoL*** - y
 - ***default user of template still enabled? - impossible***
 - ***authorized or publicly available?*** already done below
 - ***80 % of instances in same zone***
 - ***created long ago*** y
 - ***no snapshot for instance*** y
 - ***Instance Public facing? - done by checks below***
 - userdata contains passwords - how do i do this?
 - ***default sec-group used***  - not necessary cause fail-save defaults: no one ingress. 
 - ***ANTI-AFFINITY-Group!*** y
 - check if instance private AND no private network attached
 - specific ports exposed to internet (sec-group + instance public) y
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
   

#### instance pools (D) 21 y
 - all checks in instances also apply here (yay)
 - Instance Pool member instances might have different types. Updating the instance type applies only to new members; existing members remain untouched.
  -> ***check if all instances of instance pool have same type*** y
  -> check if all instances have same os as pool dictates
  ->***check if all instances have status running*** y
    following already done with instances: 
 - ***instance pool uses no anit-affinity group*** y
 - ***user data contains passwords*** y
 - ***created long ago***
 - ***state error?***
 - ***extensively many nodes in nodepool?***
 - ***specific ports exposed to internet (sec-group + instance public)***
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

#### sks (D) 9+ maybe
 - ***auto-upgrade enabled?***
 - cluster state error?
 - creation date is old
 - ***control plane version outdated?***
 - ***Nodepools: ***
   - extra-large types ?
   - default-security groups?
   - Anti-Affinity-groups?
   - specific ports exposed to the internet? (look at ports from instances)
   - extensively many nodes in nodepool?
    => Nodepools are instance-pools, so all checks from instances and instance-pools apply here YAY!!!

#### block storage (D) 3 y
 - block storage volumes
   - creation date old - no
   - correspondig snapshot exists(backup?) - yes
 - block storage snapshots
   - creation date old
 - unassigned block-storage - yes

#### templates (D) 1 y
***template public (visibility) => does not make sense!!***



#### security groups (D) 20 y
 - specific ports exposed to internet (sec-group only) y
    - cassandra (TCP 7000, 7001, 7199, 9042, 9160) y
    - elasticsearch/kibana y
    - cifs y
    - ftp y
    - kafka y [389, 636]
    - kerberos n [88, 464, 749, 750], y
    - ldap y
    - memcached y
    - mongodb/mysql/oracle/postgresql/redis/sqlserver y
    - ssh/rdp/telnet y
    - smtp y
    - ingress from any to all y
    - ingress from any to any y
    - high risk tcp ports (25(SMTP), 110(POP3), 135(RCP), 143(IMAP), 445(CIFS), 3000(Go, Node.js, and Ruby web developemnt frameworks), 4333(ahsp), 5000(Python web development frameworks), 5500(fcp-addr-srvr1), 8080(proxy), 8088(legacy HTTP port)) y
    - allow wide open public ipv4 y
    - allow wide open public ipv6 y
 - default security group restricts all traffic y
 - security group not used y
 - security group has many ingress/egress rules (50) TODO: ask michael


#### elastic ip (D) 2 y
***Elastic IP Shodan?*** y
?***Elastic IP unassigned?*** y

#### load balancers (D) 4+ y
 - service is internet facing
 - health check interval too big
 - health check retries too high
 - health check timeout too high
 => health check: has built-in checks so no one can go higher
 => get service, get healthcheck, get instance-sec-group and check if security group does not allow healthcheck? => no positive healthcheck, now service. so: sec-group must enable access to this. 

#### private networks (D) 2 y
 - any dangers with too big private networks? - no
 - maybe subnet almost full - threshold of 80% of ip leases of network

#### ssh-keys (D) 1 y
Info - are all ssh-keys used?

#### Anti-Affinity Groups (D) 0 y
no checks itself, but influences other services

# Storage ca.15

#### Buckets (D) 14+
 - CORS rules: https://<bucket-name>.sos-ch-dk-2.exo.io/?cors
   - CORS Wildcard at origin (CWE-942)
 - ACLs? Analysis with boto3 
   - Cross Account access?
   - Public Write?
   - public Access?
   - Public List ACL?
   - Public Write ACL?
   ***- AllUsers FULL_ACCESS*** y
 - Versioning enabled?
 - cross region replication? - not possible in exoscale
 - first 100 objects? 


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

why all ports seperatly? -> because of Metadata and more precise interpretation of results

# impossible
XX - ssh-key-age: data not available 
XX - snapshots encrypted : data not available
XX - ACL Analysis: no ACLs



    