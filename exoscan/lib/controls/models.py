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
            "-" * 71,
            f"{meta.severity.upper()} - {meta.control_name} - {self.resource_description}",
            "",
            f"  - Description: {meta.control_description}",
            f"  - Risk: {meta.risk}",
            f"  - Recommendation: {meta.recommendation}"
        ]
        return "\n".join(lines)

    def print_finding(self) -> None:
        print(self.format_finding())

    

class SecurityGroup(BaseModel):
    id: str
    name: str
    description: str
    external_sources: List[str]

class InstanceType(BaseModel):
    id: str
    size: str
    family: str
    cpus: int
    gpus: int
    authorized: bool
    memory: int
    zones: List[str]

class PrivateNetwork(BaseModel):
    id: str
    mac_address: str

class Template(BaseModel):
    maintainer: Optional[str] = None
    description: Optional[str] = None
    ssh_key_enabled: Optional[bool] = None
    family: Optional[str] = None
    name: Optional[str] = None
    default_user: Optional[str] = None
    size: Optional[int] = None
    password_enabled: Optional[bool] = None
    build: Optional[str] = None
    checksum: Optional[str] = None
    boot_mode: Optional[str] = None
    zones: Optional[List[str]] = None
    url: Optional[str] = None
    version: Optional[str] = None
    created_at: Optional[str] = None
    visibility: Optional[str] = None
    id: Optional[str] = None

class SSHKey(BaseModel):
    name: str
    fingerprint: str

class Manager(BaseModel):
    id: str
    type: str


class Instance(BaseModel):
    public_ip_assignment: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    security_groups: Optional[List["SecurityGroup"]] = None
    name: Optional[str] = None
    instance_type: Optional["InstanceType"] = None
    private_networks: Optional[List["PrivateNetwork"]] = None
    template: Optional["Template"] = None
    state: Optional[str] = None
    ssh_key: Optional["SSHKey"] = None
    mac_address: Optional[str] = None
    manager: Optional["Manager"] = None
    ipv6_address: Optional[str] = None
    id: Optional[str] = None
    ssh_keys: Optional[List["SSHKey"]] = None
    created_at: Optional[datetime] = Field(default=None, alias="created-at")
    public_ip: Optional[str] = None

    class Config:
        validate_by_name = True


class InstanceContainer(BaseModel):
    instances: List[Instance]

