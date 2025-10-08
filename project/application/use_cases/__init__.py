"""
Use Cases - application-specific business logic.

Use cases orchestrate domain entities and services to fulfill
specific application requirements. They represent the business
processes and workflows of the application.
"""

from .truck_management import TruckManagementUseCase
from .costs_management import CostsManagementUseCase
from .reporting import ReportingUseCase

__all__ = [
    "TruckManagementUseCase",
    "CostsManagementUseCase", 
    "ReportingUseCase",
]
