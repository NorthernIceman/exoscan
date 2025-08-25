from typing import Dict, Any
import json
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum
from pathlib import Path

class Container(BaseModel):
    class Config:
        validate_by_name = True
        validate_assignment = True

class Severity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    informational = "informational"

class ControlMeta(BaseModel):
    check_name: str
    check_description: str
    risk: str
    service: str
    recommendation: str
    Severity: Severity
        
class ControlMetadata(BaseModel):
    severity: Severity
    control_name: str
    control_description: str
    risk: str
    recommendation: str

    @classmethod
    def from_file(cls, path: str) -> "ControlMetadata":
        with open(path) as f:
            raw = json.load(f)
        return cls.model_validate(raw)
        
class Finding(BaseModel):
    ControlMetadata: ControlMetadata
    resource_description: str #refactor so it is ResourceDescription with an alias

    @classmethod
    def from_metadata(cls, metadata_file: str, resource_description: str):
        metadata_path = Path(metadata_file)
        with open(metadata_path, "r") as f:
            meta_data = json.load(f)

        control_metadata = ControlMetadata.model_validate(meta_data)
        return cls(ControlMetadata=control_metadata, resource_description=resource_description)
    
    def format_finding(self) -> str:
        meta = self.ControlMetadata
        lines = [
            "-" * 80,
            f"{meta.severity.upper()} - {meta.control_name} - {self.resource_description}",
            "",
            f"  - Description: {meta.control_description}",
            f"  - Risk: {meta.risk}",
            f"  - Recommendation: {meta.recommendation}",
            ""
        ]
        return "\n".join(lines)

    def print_finding(self) -> None:
        print(f"{self.format_finding()}")

class SecurityGroupRule(BaseModel):
    id: Optional[str] = None
    description: Optional[str] = None
    start_port: Optional[int] = Field(default=None, alias="start-port")
    end_port: Optional[int] = Field(default=None, alias="end-port")
    security_group: Optional['SecurityGroup'] = Field(default=None, alias="security-group") #forward reference necessary
    protocol: Optional[str] = None
    network: Optional[str] = None
    flow_direction: Optional[str] = Field(default=None, alias="flow-direction")

    class Config: 
        validate_by_name = True
        validate_assignment = True

#no region because sg are global
class SecurityGroup(BaseModel):
    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    rules: Optional[List['SecurityGroupRule']] = None

    class Config:
        validate_by_name = True
        validate_assignment = True

class SecurityGroupContainer(Container):
    security_groups: List[SecurityGroup] = Field(default=None, alias="security-groups")

class InstanceType(BaseModel):
    id: Optional[str] = None
    size: Optional[str] = None
    family: Optional[str] = None
    cpus: Optional[int] = None
    gpus: Optional[int] = None
    authorized: Optional[bool] = None
    memory: Optional[int] = None
    zones: Optional[List[str]] = None

class InstanceTypeContainer(Container):
    instance_types: List[InstanceType] = Field(default=None, alias="instance-types")

class PrivateNetwork(BaseModel):
    id: str
    mac_address: Optional[str] = None

class PrivateNetwork(BaseModel):
    id: Optional[str] = None

class ElasticIP(BaseModel):
    ip: Optional[str] = None
    id: Optional[str] = None
    description: Optional[str] = None
    cidr: Optional[str] = None
    addressfamily: Optional[str] = None
    healthcheck: Optional['HealthCheck'] = None
    labels: Optional[Dict[str, str]] = None

class HealthCheck(BaseModel): 
    strikes_ok: Optional[int] = Field(default=None, alias="strikes-ok")
    tls_skip_verify: Optional[bool] = Field(default=None, alias="tls-skip-verify")
    tls_sni: Optional[str] = Field(default=None, alias="tls-sni")
    strikes_fail: Optional[int] = Field(default=None, alias="strikes-fail")
    mode: Optional[str] = None
    port: Optional[int] = None
    uri: Optional[str] = None
    interval: Optional[int] = None
    timeout: Optional[int] = None

class ElasticIPContainer(Container):
    elastic_ips: List[ElasticIP] = Field(Default=None, alias="elastic-ips")

class Template(BaseModel):
    maintainer: Optional[str] = None
    description: Optional[str] = None
    ssh_key_enabled: Optional[bool] = Field(default=None, alias="ssh-key-enabled")
    family: Optional[str] = None
    name: Optional[str] = None
    default_user: Optional[str] = Field(default=None, alias="default-user")
    size: Optional[int] = None
    password_enabled: Optional[bool] = Field(default=None, alias="password-enabled")
    build: Optional[str] = None
    checksum: Optional[str] = None
    boot_mode: Optional[str] = Field(default=None, alias="boot-mode")
    zones: Optional[List[str]] = None
    url: Optional[str] = None
    version: Optional[str] = None
    created_at: Optional[str] = Field(default=None, alias="created-at")
    visibility: Optional[str] = None
    id: Optional[str] = None

class TemplateContainer(Container):
    templates: List[Template] = None

class SSHKey(BaseModel):
    name: str
    fingerprint: Optional[str] = None

class Manager(BaseModel):
    id: str
    type: Optional[str] = None

#need alias cause api returns e.g. "security-groups" instead of "security_groups"
class Instance(BaseModel):
    public_ip_assignment: Optional[str] = Field(default=None, alias="public-ip-assignment")
    labels: Optional[Dict[str, str]] = None
    security_groups: Optional[List[SecurityGroup]] = Field(default=None, alias="security-groups")
    name: Optional[str] = None
    instance_type: Optional[InstanceType] = Field(default=None, alias="instance-type")
    private_networks: Optional[List[PrivateNetwork]] = Field(default=None, alias="private-networks")
    template: Optional[Template] = None
    state: Optional[str] = None
    ssh_key: Optional[SSHKey] = Field(default=None, alias="ssh-key")
    mac_address: Optional[str] = Field(default=None, alias="mac-address")
    manager: Optional[Any] = None  # Define this if needed
    ipv6_address: Optional[str] = Field(default=None, alias="ipv6-address")
    id: Optional[str] = None
    ssh_keys: Optional[List[SSHKey]] =  Field(default=None, alias="ssh-keys")
    created_at: Optional[datetime] = Field(default=None, alias="created-at")
    public_ip: Optional[str] = Field(default=None, alias="public-ip")
    disk_size: Optional[int] = Field(default=None, alias="disk-size")
    anti_affinity_groups: Optional[List['AntiAffinityGroup']] = Field(default=None, alias="anti-affinity-groups")
    elastic_ips: Optional[List[ElasticIP]] = Field(default=None, alias="elastic-ips")
    user_data: Optional[str] = Field(default=None, alias="user-data")
    snapshots: Optional[List[Any]] = None
    block_storage_volumes: Optional[List[Any]] = Field(default=None, alias="block-storage-volumes")
    region: Optional[str] = None
    class Config:
        validate_by_name = True
        validate_assignment = True

class AntiAffinityGroup(BaseModel):
    id: str
    name: Optional[str] = None
    description: Optional[str] = None

class InstanceContainer(Container):
    instances: List[Instance]

class SSHKeyContainer(Container):
    ssh_keys: List[SSHKey] = Field(default=None, alias="ssh-keys")

class DeployTarget(BaseModel): 
    id: str = None
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None

class InstancePool(BaseModel):
    anti_affinity_groups: Optional[List['AntiAffinityGroup']] = Field(default=None, alias="anti-affinity-groups")
    description: Optional[str] = None
    public_ip_assignment: Optional[str] = Field(default=None, alias="public-ip-assignment")
    labels: Optional[Dict[str, str]] = None
    security_groups: Optional[List[SecurityGroup]] = Field(default=None, alias="security-groups")
    elastic_ips: Optional[List[ElasticIP]] = Field(default=None, alias="elastic-ips")
    name: Optional[str] = None
    instance_type: Optional[InstanceType] = Field(default=None, alias="instance-type")
    min_available: Optional[int] = Field(default = None, alias="min-available")
    private_networks: Optional[List[PrivateNetwork]] = Field(default=None, alias="private-networks")
    template: Optional[Template] = None
    state: Optional[str] = None
    size: Optional[int] = None
    ssh_key: Optional[SSHKey] = Field(default=None, alias="ssh-key")
    instance_prefix: Optional[str] = Field(default=None, alias="instance-prefix")
    user_data: Optional[str] = Field(default=None, alias="user-data")
    manager: Optional[str] = None
    instances: Optional[List['Instance']] = None
    deploy_target: Optional[DeployTarget] = None
    ipv6_enabled: Optional[bool] = Field(default=False, alias="ipv6-enabled")
    id: Optional[str] = None
    disk_size: Optional[int] = Field(default=None, alias="disk-size")
    ssh_keys: Optional[List[SSHKey]] =  Field(default=None, alias="ssh-keys")


class InstancePoolContainer(Container): 
    instance_pools: List['InstancePool'] = Field(default=None, alias="instance-pools")

class Taint(BaseModel):
    value: str = None
    effect: str = None

class KubeletImageGC(BaseModel):
    high_threshold: Optional[int] = Field(default=None, alias="high-threshold")
    low_threshold: Optional[int] = Field(default=None, alias="low-threshold")
    min_age: Optional[str] = Field(default=None, alias="min-age")

class DeployTarget(BaseModel):
    id: str = None
    name: Optional[str] = None
    type: Optional[str] = None 
    description: Optional[str] = None

class SKSNodepool(BaseModel):
    anti_affinity_groups: Optional[List['AntiAffinityGroup']] = Field(default=None, alias="anti-affinity-groups")
    description: Optional[str] = None
    public_ip_assignment: Optional[str] = Field(default=None, alias="public-ip-assignment")
    labels: Optional[Dict[str, str]] = None
    taints: Optional[Taint] = None
    security_groups: Optional[List[SecurityGroup]] = Field(default=None, alias="security-groups")
    name: Optional[str] = None
    instance_type: Optional[InstanceType] = Field(default=None, alias="instance-type")
    private_networks: Optional[List[PrivateNetwork]] = Field(default=None, alias="private-networks")
    template: Optional[Template] = None
    state: Optional[str] = None
    size: Optional[int] = None
    kubelet_image_gc: Optional['KubeletImageGC'] = Field(default=None, alias="kubelet-image-gc")
    instance_pool: Optional['InstancePool'] = Field(default=None, alias="instance-pool")
    instance_prefix: Optional[str] = Field(default=None, alias="instance-prefix")
    deploy_target: Optional['DeployTarget'] = Field(default=None, alias="deploy-target")
    addons: Optional[List[str]] = None
    id: Optional[str] = None
    disk_size: Optional[int] = Field(default=None, alias="disk-size")
    version: Optional[str] = None
    created_at: Optional[str] = Field(default=None, alias="created-at")


class SKSCluster(BaseModel):
    description: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    cni: Optional[str] = None
    auto_upgrade: Optional[bool] = Field(default=None, alias="auto-upgrade")
    name: Optional[str] = None
    enable_operators_ca: Optional[bool] = Field(default=None, alias="enable-operators-ca")
    state: Optional[str] = None
    enable_kube_proxy: Optional[bool] = Field(default=None, alias="enable-kube-proxy")
    level: Optional[str] = None
    feature_gates: Optional[List[str]] = Field(default=None, alias="feature-gates")
    addons: Optional[List[str]] = None
    id: Optional[str] = None
    version: Optional[str] = None
    created_at: Optional[str] = Field(default=None, alias="created-at")
    endpoint: Optional[str] = None
    node_cidr_mask_size_ipv6: Optional[int] = Field(default=None, alias="node-cidr-mask-size-ipv6")
    default_security_group_id: Optional[str] = Field(default=None, alias="default-security-group-id")
    nodepools: Optional[List[SKSNodepool]] = None
    node_cidr_mask_size_ipv4: Optional[int] = Field(default=None, alias="node-cidr-mask-size-ipv4")
    service_cluster_ip_range: Optional[str] = Field(default=None, alias="service-cluster-ip-range")
    cluster_cidr: Optional[str] = Field(default=None, alias="cluster-cidr")

class SKSClusterContainer(Container):
    sks_cluster: List[SKSCluster] = Field(default=None, alias="sks-clusters")

class LoadBalancer(BaseModel):
    id: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    state: Optional[str] = None
    created_at: Optional[str] = Field(default=None, alias="created-at")
    ip: Optional[str] = None
    services: Optional[List['Service']] = None
    labels: Optional[Dict[str, str]] = None

class HealthCheckStatus(BaseModel):
    public_ip: Optional[str] = Field(default=None, alias="public-ip")
    status: Optional[str] = None

class Service(BaseModel):
    description: Optional[str] = None
    protocol: Optional[str] = None
    name: Optional[str] = None
    state: Optional[str] = None
    target_port: Optional[int] = Field(default=None, alias="target-port")
    port: Optional[int] = None
    instance_pool: Optional['InstancePool'] = Field(default=None, alias="instance-pool")
    strategy: Optional[str] = None
    healthcheck: Optional['HealthCheck'] = None
    id: Optional[str] = None
    healthcheck_status: Optional[List['HealthCheckStatus']] = Field(default=None, alias="healthcheck-status")

class LoadBalancerContainer(Container):
    load_balancers: List['LoadBalancer'] = Field(default=None, alias="load-balancers")

class BlockStorageVolume(BaseModel):
    labels: Optional[Dict[str, str]] = None
    id: Optional[str] = None
    name: Optional[str] = None
    instance: Optional[Instance] = None
    state: Optional[str] = None
    size: Optional[int] = None
    blocksize: Optional[int] = None
    block_storage_snapshots: Optional[List['BlockStorageSnapshot']] = Field(default=None, alias="block-storage-snapshots")
    created_at: Optional[str] = Field(default=None, alias="created-at")

class BlockStorageSnapshot(BaseModel):
    labels: Optional[Dict[str, str]] = None
    id: Optional[str] = None
    name: Optional[str] = None
    size: Optional[int] = None
    volume_size: Optional[int] = Field(default=None, alias="volume-size")
    created_at: Optional[str] = Field(default=None, alias="created-at")
    state: Optional[str] = None
    block_storage_volume: Optional[List['BlockStorageVolume']] = Field(default=None, alias="block-storage-volume")

class BlockStorageVolumeContainer(Container):
    block_storage_volumes: List['BlockStorageVolume'] = Field(default=None, alias="block-storage-volumes")

class BlockStorageSnapshotContainer(Container):
    block_storage_snapshots: List['BlockStorageSnapshot'] = Field(default=None, alias="block-storage-snapshots")

class Leases(BaseModel):
    ip: Optional[str] = None
    instance_id: Optional[str] = Field(default=None, alias="instance-id")

class Options(BaseModel):
    routers: Optional[List[str]] = None
    dns_servers: Optional[List[str]] = Field(default=None, alias="dns-servers")
    ntp_servers: Optional[List[str]] = Field(default=None, alias="ntp-servers")
    domain_search:  Optional[List[str]] = Field(default=None, alias="domain-search")

class PrivateNetwork(BaseModel):
    description: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    name: Optional[str] = None
    start_ip: Optional[str] = Field(default=None, alias="start-ip")
    end_ip: Optional[str] = Field(default=None, alias="end-ip")
    leases: Optional[List['Leases']] = None
    id: Optional[str] = None
    vni: Optional[int] = None
    netmask: Optional[str] = None
    options: Optional['Options'] = None

class PrivateNetworkContainer(Container):
    private_networks: List['PrivateNetwork'] = Field(default=None, alias="private-networks")

class Grantee(BaseModel):
    display_name: Optional[str] = Field(default=None, alias="DisplayName")
    id: Optional[str] = Field(default=None, alias="ID")
    grantee_type: Optional[str] = Field(default=None, alias="Type")
    uri: Optional[str] = Field(default=None, alias="URI")

class ACL(BaseModel):
    grantee: Optional['Grantee'] = Field(default=None, alias="Grantee")
    permission: Optional[str] = Field(default=None, alias="Permission")

#https://docs.aws.amazon.com/AmazonS3/latest/API/API_CORSRule.html:
class CorsRules(BaseModel): 
    allowed_headers: Optional[List[str]] = Field(default=None, alias="AllowedHeaders")
    allowed_methods: Optional[List[str]] = Field(default=None, alias="AllowedMethods")
    allowed_origins: Optional[List[str]] = Field(default=None, alias="AllowedOrigins")
    exposed_headers: Optional[List[str]] = Field(default=None, alias="ExposeHeaders")
    id: Optional[str] = Field(default=None, alias="ID")
    max_age_seconds: Optional[int] = Field(default=None, alias="MaxAgeSeconds")

class SOSBucket(BaseModel):
    name: Optional[str] = None
    created_at: Optional[str] = Field(default=None, alias="created-at")
    zone_name: Optional[str] = Field(default=None, alias="zone-name")
    size: Optional[int] = None
    acl: Optional[List['ACL']] = Field(default=None, alias="ACL")
    cors: Optional[List['CorsRules']] = Field(default=None, alias="CORSRules")
    versioning: Optional[str] = Field(default=None, alias="Status")
    #cdn is impossible to view via api???
    
class SOSBucketContainer(Container):
    sos_buckets_usage: Optional[List['SOSBucket']] = Field(default=None, alias="sos-buckets-usage")

class DBaaService(BaseModel):
    updated_at: Optional[str] = Field(default=None, alias="updated-at")
    node_count: Optional[int] = Field(default=None, alias="node-count")
    node_cpu_count: Optional[int] = Field(default=None, alias="node-cpu-count")
    integrations: Optional[List[str]] = None
    zone: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    state: Optional[str] = None
    termination_protection: Optional[bool] = Field(default=None, alias="termination-protection")
    notifications: Optional[List[str]] = None
    disk_size: Optional[int] = Field(default=None, alias="disk-size")
    node_memory: Optional[int] = None
    created_at: Optional[str] = Field(default=None, alias="created-at")
    plan: Optional[str] = None

class DBaaServiceContainer(Container):
    dbaas_services: Optional[List['DBaaService']] = Field(default=None, alias="dbaas-services")

class ConnectionInformation(BaseModel):
    uri: Optional[List[str]] = None
    params: Optional[List[dict]] = None
    standby: Optional[List[str]] = None
    syncing: Optional[List[str]] = None

class Backups(BaseModel):
    backup_name: Optional[str] = Field(default=None, alias="backup-name")
    backup_time: Optional[str] = Field(default=None, alias="backup-time")
    data_size: Optional[int] = Field(default=None, alias="data-size")

class Maintenance(BaseModel):
    dow: Optional[str] = None
    time: Optional[str] = None
    updates: Optional[List[dict]] = None

class URIParams(BaseModel):
    password: Optional[str] = None
    sslmode: Optional[str] = None
    port: Optional[int] = None
    dbname: Optional[str] = None
    host: Optional[str] = None
    user: Optional[str] = None

class DBUsers(BaseModel):
    type: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    allow_replication: Optional[bool] = Field(default=None, alias="allow-replication")

class CommonDBProperties(DBaaService):
    connection_info: Optional['ConnectionInformation'] = Field(default=None, alias="connection-info")
    backup_schedule: Optional[dict] = Field(default=None, alias="backup-schedule")
    prometheus_uri: Optional[dict] = Field(default=None, alias="prometheus-uri")
    ip_filter: Optional[List[str]] = Field(default=None, alias="ip-filter")
    backups: Optional[List['Backups']] = None
    maintenance: Optional['Maintenance'] = None
    uri_params: Optional['URIParams'] = Field(default=None, alias="uri-params")
    users: Optional[List['DBUsers']] = None

class DBaaServicePostgreSQL(CommonDBProperties):
    pg_settings: Optional[dict] = Field(default=None, alias="pg-settings")
    
class DBaaServicePostgreSQLContainer(Container):
    dbaas_pg_services: Optional[List['DBaaServicePostgreSQL']] = Field(default=None, alias="dbaas-pg-services")

class DBaaServiceMySQL(CommonDBProperties):
    mysql_settings: Optional[dict] = Field(default=None, alias="mysql-settings")
    
class DBaaServiceMySQLContainer(Container):
    dbaas_mysql_services: Optional[List['DBaaServiceMySQL']] = Field(default=None, alias="dbaas-mysql-services")

class IAMRole(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[List[str]] = None
    labels: Optional[Dict[str, str]] = None
    editable: Optional[bool] = None
    policy: Optional['IAMPolicy'] = None

class IAMPolicy(BaseModel): 
    default_service_strategy: str = Field(default=None, alias="default-service-strategy")
    services: Optional[Dict[str, 'IAMServices']] = None

class IAMServices(BaseModel): 
    access_type: Optional[str] = Field(default=None, alias="type")
    rules: Optional[List['IAMRules']] = None

class IAMRules(BaseModel):
    action: Optional[str] = None
    expression: Optional[str] = None
    resources: Optional[List[str]] = None

class IAMUser(BaseModel):
    sso: Optional[bool] = None
    two_factor_authentication:  Optional[bool] = Field(default=None, alias="two-factor-authentication")
    email: str = None #requ.
    id: Optional[str] = None
    role: 'IAMRole' = None #req
    pending: Optional[bool] = None

class IAMRoleContainer(Container):
    roles: Optional[List['IAMRole']] = Field(default=None, alias="iam-roles")

class IAMUserContainer(Container):
    users: Optional[List['IAMUser']] = Field(default=None, alias="users")









