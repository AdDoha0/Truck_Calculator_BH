"""
Mappers for converting between ORM models and domain entities.
"""

from typing import Optional
from ..database.models import Truck as TruckORM, FixedCostsTruck as FixedCostsTruckORM, FixedCostsCommon as FixedCostsCommonORM
from ...domain.entities.truck import Truck, TruckId
from ...domain.entities.costs import FixedCostsTruck, FixedCostsCommon
from ...domain.entities.financial import Money


class TruckMapper:
    """
    Maps between Truck ORM model and Truck domain entity.
    """
    
    @staticmethod
    def to_domain(orm_truck: TruckORM) -> Truck:
        """Convert SQLAlchemy Truck model to domain entity."""
        return Truck(
            id=TruckId(orm_truck.id) if orm_truck.id else None,
            tractor_no=orm_truck.tractor_no
        )
    
    @staticmethod
    def to_orm(domain_truck: Truck, orm_truck: Optional[TruckORM] = None) -> TruckORM:
        """
        Convert domain Truck to SQLAlchemy model.
        
        Args:
            domain_truck: Domain entity to convert
            orm_truck: Existing ORM object to update (for updates)
            
        Returns:
            SQLAlchemy Truck model
        """
        if orm_truck is None:
            orm_truck = TruckORM()
        
        if domain_truck.id:
            orm_truck.id = int(domain_truck.id)
        orm_truck.tractor_no = domain_truck.tractor_no
        
        return orm_truck


class CostsMapper:
    """
    Maps between Costs ORM models and domain entities.
    """
    
    @staticmethod
    def truck_costs_to_domain(orm_costs: FixedCostsTruckORM) -> FixedCostsTruck:
        """Convert SQLAlchemy FixedCostsTruck to domain entity."""
        return FixedCostsTruck(
            truck_id=TruckId(orm_costs.truck_id) if orm_costs.truck_id else None,
            truck_payment=Money(orm_costs.truck_payment),
            trailer_payment=Money(orm_costs.trailer_payment),
            physical_damage_insurance_truck=Money(orm_costs.physical_damage_insurance_truck),
            physical_damage_insurance_trailer=Money(orm_costs.physical_damage_insurance_trailer)
        )
    
    @staticmethod
    def truck_costs_to_orm(domain_costs: FixedCostsTruck, 
                          orm_costs: Optional[FixedCostsTruckORM] = None) -> FixedCostsTruckORM:
        """Convert domain FixedCostsTruck to SQLAlchemy model."""
        if orm_costs is None:
            orm_costs = FixedCostsTruckORM()
        
        if domain_costs.truck_id:
            orm_costs.truck_id = int(domain_costs.truck_id)
        orm_costs.truck_payment = float(domain_costs.truck_payment.amount)
        orm_costs.trailer_payment = float(domain_costs.trailer_payment.amount)
        orm_costs.physical_damage_insurance_truck = float(domain_costs.physical_damage_insurance_truck.amount)
        orm_costs.physical_damage_insurance_trailer = float(domain_costs.physical_damage_insurance_trailer.amount)
        
        return orm_costs
    
    @staticmethod
    def common_costs_to_domain(orm_costs: FixedCostsCommonORM) -> FixedCostsCommon:
        """Convert SQLAlchemy FixedCostsCommon to domain entity."""
        return FixedCostsCommon(
            ifta=Money(orm_costs.ifta),
            insurance=Money(orm_costs.insurance),
            eld=Money(orm_costs.eld),
            tablet=Money(orm_costs.tablet),
            tolls=Money(orm_costs.tolls)
        )
    
    @staticmethod
    def common_costs_to_orm(domain_costs: FixedCostsCommon,
                           orm_costs: Optional[FixedCostsCommonORM] = None) -> FixedCostsCommonORM:
        """Convert domain FixedCostsCommon to SQLAlchemy model."""
        if orm_costs is None:
            orm_costs = FixedCostsCommonORM()
        
        orm_costs.ifta = float(domain_costs.ifta.amount)
        orm_costs.insurance = float(domain_costs.insurance.amount)
        orm_costs.eld = float(domain_costs.eld.amount)
        orm_costs.tablet = float(domain_costs.tablet.amount)
        orm_costs.tolls = float(domain_costs.tolls.amount)
        
        return orm_costs
