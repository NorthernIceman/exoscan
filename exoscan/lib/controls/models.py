from abc import abstractmethod
from typing import Dict, Any
import json
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum
from pathlib import Path


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

class SecurityGroupContainer(BaseModel):
    security_groups: List[SecurityGroup] = Field(default=None, alias="security-groups")

    class Config:
        validate_by_name = True
        validate_assignment = True

class InstanceType(BaseModel):
    id: Optional[str] = None
    size: Optional[str] = None
    family: Optional[str] = None
    cpus: Optional[int] = None
    gpus: Optional[int] = None
    authorized: Optional[bool] = None
    memory: Optional[int] = None
    zones: Optional[List[str]] = None

class PrivateNetwork(BaseModel):
    id: str
    mac_address: Optional[str] = None

class PrivateNetwork(BaseModel):
    id: Optional[str] = None

class ElasticIP(BaseModel):
    ip: Optional[str] = None
    id: str

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
    anti_affinity_groups: Optional[List[Dict[str, Any]]] = Field(default=None, alias="anti-affinity-groups")
    elastic_ips: Optional[List[ElasticIP]] = Field(default=None, alias="elastic-ips")
    user_data: Optional[str] = Field(default=None, alias="user-data")
    snapshots: Optional[List[Any]] = None
    block_storage_volumes: Optional[List[Any]] = Field(default=None, alias="block-storage-volumes")
    region: Optional[str] = None


    class Config:
        validate_by_name = True
        validate_assignment = True


class InstanceContainer(BaseModel):
    instances: List[Instance]

class SSHKeyContainer(BaseModel):
    ssh_keys: List[SSHKey] = Field(default=None, alias="ssh-keys")



