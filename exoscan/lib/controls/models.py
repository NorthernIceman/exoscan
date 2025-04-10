from abc import abstractmethod
from typing import Set, Dict, Any
import sys, os
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, ValidationError, field_validator
from enum import Enum

from exoscan.lib.controls.utils import import_all_controls


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
        
        

class Control(ControlMeta):

    def __init__(self, **data):
        metadata_file = (
            os.path.abspath(sys.modules[self.__module__].__file__)[:-3]
            + ".metadata.json"
        )
        print(metadata_file)
        data = ControlMeta.parse_file(metadata_file).model_dump()
        super().__init__(**data)

    def metadata(self) -> dict:
        return self.model_dump_json()
    
    @abstractmethod
    def execute(self) -> list:
        """Execute controls logic"""
    





@dataclass
class SecurityGroup:
    id: str
    name: str
    description: str
    external_sources: List[str]

@dataclass
class InstanceType:
    id: str
    size: str
    family: str
    cpus: int
    gpus: int
    authorized: bool
    memory: int
    zones: List[str]

@dataclass
class PrivateNetwork:
    id: str
    mac_address: str

@dataclass
class Template:
    dataclass
class Template:
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

@dataclass
class SSHKey:
    name: str
    fingerprint: str

@dataclass
class Manager:
    id: str
    type: str

@dataclass
class Instance:
    public_ip_assignment: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    security_groups: Optional[List[SecurityGroup]] = None
    name: Optional[str] = None
    instance_type: Optional[InstanceType] = None
    private_networks: Optional[List[PrivateNetwork]] = None
    template: Optional[{Template}] = None
    state: Optional[str] = None
    ssh_key: Optional[SSHKey] = None
    mac_address: Optional[str] = None
    manager: Optional[Manager] = None
    ipv6_address: Optional[str] = None
    id: Optional[str] = None
    ssh_keys: Optional[List[SSHKey]] = None
    created_at: Optional[datetime] = None
    public_ip: Optional[str] = None

@dataclass
class InstanceContainer:
    instances: List[Instance]

