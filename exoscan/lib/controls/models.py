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

    # @field_validator("Severity", mode='before')
    # def severity_lower(severity):
    #     return severity.lower()
    
    @staticmethod
    def get_all_controls(category: str = None) -> dict[str, "ControlMeta"]: # return dictionary of ControlMeta with control_name as key
        all_controls = {}
        controls = import_all_controls()

        for control_info in controls:
            control_name = control_info[0]
            control_path = control_info[1]
            metadata_file = f"{control_path}/{control_name}.metadata.json"

######################continue here###################


    @staticmethod
    def list(
        bulk_controls_meta: dict = None
    ) -> Set["ControlMeta"]:
        if not bulk_controls_meta: 
            bulk_controls_meta = ControlMeta.get_all_controls()
        
        

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
    maintainer: str
    description: str
    ssh_key_enabled: bool
    family: str
    name: str
    default_user: str
    size: int
    password_enabled: bool
    build: str
    checksum: str
    boot_mode: str
    id: str
    zones: List[str]
    url: str
    version: str
    created_at: datetime
    visibility: str

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
    public_ip_assignment: str
    labels: Dict[str, str]
    security_groups: List[SecurityGroup]
    name: str
    instance_type: InstanceType
    private_networks: List[PrivateNetwork]
    template: Template
    state: str
    ssh_key: SSHKey
    mac_address: str
    manager: Manager
    ipv6_address: str
    id: str
    ssh_keys: List[SSHKey]
    created_at: datetime
    public_ip: str

@dataclass
class InstanceContainer:
    instances: List[Instance]

