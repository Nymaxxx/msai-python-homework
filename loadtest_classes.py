from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass(init=True)
class RequestDescriptor:

    method: str
    url: str
    headers: Dict[str, str]
    body: Optional[str]

    @classmethod
    def from_cfg(cls, cfg: dict) -> "RequestDescriptor":
        if "body" in cfg:
            return RequestDescriptor(cfg["method"], cfg["url"], cfg["headers"], cfg["body"])
        else:
            return RequestDescriptor(cfg["method"], cfg["url"], cfg["headers"], None)


@dataclass(init=True)
class StageDescriptor:

    requests: List[RequestDescriptor]
    timeout: int
    duration: int
    rps_from: int
    rps_to: int
    repeats: int

    @classmethod
    def from_cfg(cls, requests: List[RequestDescriptor], cfg: dict) -> "StageDescriptor":
        return StageDescriptor(
            requests, 
            cfg["timeout"], 
            cfg["duration"],
            cfg["rps_from"],
            cfg["rps_to"],
            cfg["repeats"]
        )

