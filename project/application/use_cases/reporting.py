"""
Reporting use cases.
"""

from typing import Dict, List
from decimal import Decimal
from ...domain.entities.truck import TruckId
from ...domain.entities.costs import VariableCosts
from ...domain.entities.financial import Money
from ...domain.services.cost_calculator import CostCalculator
from ...domain.repositories.costs_repository import CostsRepository


class ReportingUseCase:
    """
    Use case for generating reports and calculations.
    
    Handles profitability analysis, cost breakdowns, and fleet summaries.
    """
    
    def __init__(self, costs_repo: CostsRepository):
        self._cost_calculator = CostCalculator(costs_repo)
    
    def calculate_truck_profitability(self,
                                    truck_id: TruckId,
                                    revenue: Decimal,
                                    salary: Decimal,
                                    fuel: Decimal,
                                    tolls: Decimal,
                                    repair: Decimal) -> Dict[str, any]:
        """
        Calculate comprehensive profitability analysis for a truck.
        
        Args:
            truck_id: ID of the truck
            revenue: Monthly revenue
            salary: Driver salary
            fuel: Fuel costs
            tolls: Toll costs
            repair: Repair costs
            
        Returns:
            Dictionary with profitability metrics and cost breakdown
        """
        # Create variable costs object
        variable_costs = VariableCosts(
            salary=Money(salary),
            fuel=Money(fuel),
            tolls=Money(tolls),
            repair=Money(repair)
        )
        
        # Calculate profit and margin
        revenue_money = Money(revenue)
        profit, margin = self._cost_calculator.calculate_profit_for_truck(
            truck_id, revenue_money, variable_costs
        )
        
        # Get detailed cost breakdown
        cost_breakdown = self._cost_calculator.get_cost_breakdown_for_truck(
            truck_id, variable_costs
        )
        
        # Calculate totals
        total_variable = sum(
            cost_breakdown[key].amount 
            for key in ['salary', 'fuel', 'tolls_variable', 'repair']
        )
        
        total_fixed = sum(
            cost_breakdown[key].amount
            for key in cost_breakdown.keys()
            if key not in ['salary', 'fuel', 'tolls_variable', 'repair']
        )
        
        return {
            'truck_id': truck_id,
            'revenue': revenue,
            'profit': profit.amount,
            'profit_margin': round(margin, 2),
            
            # Cost totals
            'total_variable_costs': total_variable,
            'total_fixed_costs': total_fixed,
            'total_costs': total_variable + total_fixed,
            
            # Detailed breakdown
            'cost_breakdown': {
                key: float(value.amount) 
                for key, value in cost_breakdown.items()
            },
            
            # Key metrics
            'is_profitable': profit.is_positive,
            'break_even_revenue': total_variable + total_fixed,
        }
    
    def get_fleet_summary(self, 
                         truck_data: List[tuple[TruckId, Decimal, Decimal, Decimal, Decimal, Decimal]]) -> Dict[str, any]:
        """
        Generate fleet-wide summary report.
        
        Args:
            truck_data: List of (truck_id, revenue, salary, fuel, tolls, repair) tuples
            
        Returns:
            Fleet summary with totals and averages
        """
        # Convert to domain objects format
        domain_data = []
        for truck_id, revenue, salary, fuel, tolls, repair in truck_data:
            variable_costs = VariableCosts(
                salary=Money(salary),
                fuel=Money(fuel),
                tolls=Money(tolls),
                repair=Money(repair)
            )
            domain_data.append((truck_id, Money(revenue), variable_costs))
        
        # Calculate fleet summary
        fleet_totals = self._cost_calculator.calculate_fleet_summary(domain_data)
        
        # Calculate averages
        truck_count = len(truck_data)
        avg_revenue = fleet_totals['total_revenue'] / truck_count if truck_count > 0 else Money(0)
        avg_profit = fleet_totals['total_profit'] / truck_count if truck_count > 0 else Money(0)
        
        # Calculate fleet profit margin
        if fleet_totals['total_revenue'].is_zero:
            fleet_margin = 0.0
        else:
            fleet_margin = float(
                fleet_totals['total_profit'].amount / 
                fleet_totals['total_revenue'].amount * 100
            )
        
        return {
            'truck_count': truck_count,
            
            # Fleet totals
            'total_revenue': float(fleet_totals['total_revenue'].amount),
            'total_variable_costs': float(fleet_totals['total_variable_costs'].amount),
            'total_fixed_costs': float(fleet_totals['total_fixed_costs'].amount),
            'total_profit': float(fleet_totals['total_profit'].amount),
            
            # Fleet averages
            'average_revenue_per_truck': float(avg_revenue.amount),
            'average_profit_per_truck': float(avg_profit.amount),
            
            # Fleet metrics
            'fleet_profit_margin': round(fleet_margin, 2),
            'is_fleet_profitable': fleet_totals['total_profit'].is_positive,
            
            # Common costs impact
            'common_costs_per_truck': float(
                self._cost_calculator.get_common_costs_impact_per_truck().amount
            ),
        }
    
    def get_cost_breakdown_report(self, truck_id: TruckId) -> Dict[str, any]:
        """
        Get detailed cost breakdown for a specific truck.
        
        Returns cost structure without revenue calculations.
        """
        # Use zero variable costs to get only fixed costs structure
        zero_variable = VariableCosts.zero()
        cost_breakdown = self._cost_calculator.get_cost_breakdown_for_truck(
            truck_id, zero_variable
        )
        
        # Separate into categories
        truck_fixed = {
            'truck_payment': float(cost_breakdown['truck_payment'].amount),
            'trailer_payment': float(cost_breakdown['trailer_payment'].amount),
            'truck_insurance': float(cost_breakdown['truck_insurance'].amount),
            'trailer_insurance': float(cost_breakdown['trailer_insurance'].amount),
        }
        
        common_fixed = {
            'ifta': float(cost_breakdown['ifta'].amount),
            'business_insurance': float(cost_breakdown['business_insurance'].amount),
            'eld': float(cost_breakdown['eld'].amount),
            'tablet': float(cost_breakdown['tablet'].amount),
            'tolls_fixed': float(cost_breakdown['tolls_fixed'].amount),
        }
        
        return {
            'truck_id': truck_id,
            'truck_specific_costs': truck_fixed,
            'common_costs': common_fixed,
            'total_truck_fixed': sum(truck_fixed.values()),
            'total_common_fixed': sum(common_fixed.values()),
            'total_monthly_fixed': sum(truck_fixed.values()) + sum(common_fixed.values()),
        }
