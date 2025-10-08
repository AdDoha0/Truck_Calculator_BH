"""
Cost calculation domain service.
"""

from typing import List, Dict
from ..entities.truck import TruckId
from ..entities.costs import TotalCosts, VariableCosts, FixedCostsTruck, FixedCostsCommon
from ..entities.financial import Money, Period
from ..repositories.costs_repository import CostsRepository


class CostCalculator:
    """
    Domain service for cost calculations and aggregations.
    
    Implements business rules around cost calculations:
    - Variable vs Fixed cost separation
    - Per-truck vs Common cost aggregation
    - Profitability calculations
    """
    
    def __init__(self, costs_repo: CostsRepository):
        self._costs_repo = costs_repo
    
    def calculate_total_costs_for_truck(self,
                                      truck_id: TruckId,
                                      variable_costs: VariableCosts) -> TotalCosts:
        """
        Calculate total costs for a truck by combining:
        1. Variable costs (from uploaded files)
        2. Truck-specific fixed costs
        3. Common fixed costs (applied to all trucks)
        
        Business rule: Both truck and common fixed costs are added together.
        """
        # Get truck-specific fixed costs
        truck_fixed = self._costs_repo.find_truck_costs(truck_id)
        if not truck_fixed:
            truck_fixed = FixedCostsTruck.zero_for_truck(truck_id)
        
        # Get common fixed costs
        common_fixed = self._costs_repo.find_common_costs()
        if not common_fixed:
            common_fixed = FixedCostsCommon.zero()
        
        return TotalCosts(
            variable_costs=variable_costs,
            truck_fixed_costs=truck_fixed,
            common_fixed_costs=common_fixed
        )
    
    def calculate_profit_for_truck(self,
                                 truck_id: TruckId,
                                 revenue: Money,
                                 variable_costs: VariableCosts) -> tuple[Money, float]:
        """
        Calculate profit and profit margin for a truck.
        
        Returns:
            (profit_amount, profit_margin_percentage)
        """
        total_costs = self.calculate_total_costs_for_truck(truck_id, variable_costs)
        
        profit = revenue - total_costs.total_monthly_amount()
        
        # Calculate profit margin
        if revenue.is_zero:
            margin = 0.0
        else:
            margin = float(profit.amount / revenue.amount * 100)
        
        return profit, margin
    
    def get_cost_breakdown_for_truck(self,
                                   truck_id: TruckId,
                                   variable_costs: VariableCosts) -> Dict[str, Money]:
        """
        Get detailed cost breakdown for reporting.
        
        Returns dictionary with all cost categories and amounts.
        """
        total_costs = self.calculate_total_costs_for_truck(truck_id, variable_costs)
        return total_costs.breakdown()
    
    def calculate_fleet_summary(self, 
                              truck_data: List[tuple[TruckId, Money, VariableCosts]]) -> Dict[str, Money]:
        """
        Calculate fleet-wide cost and profit summary.
        
        Args:
            truck_data: List of (truck_id, revenue, variable_costs) tuples
            
        Returns:
            Dictionary with fleet totals
        """
        total_revenue = Money(0)
        total_variable = Money(0)
        total_fixed = Money(0)
        
        for truck_id, revenue, variable_costs in truck_data:
            total_costs = self.calculate_total_costs_for_truck(truck_id, variable_costs)
            
            total_revenue += revenue
            total_variable += total_costs.total_variable_amount()
            total_fixed += total_costs.total_fixed_amount()
        
        total_profit = total_revenue - total_variable - total_fixed
        
        return {
            'total_revenue': total_revenue,
            'total_variable_costs': total_variable,
            'total_fixed_costs': total_fixed,
            'total_profit': total_profit,
        }
    
    def get_common_costs_impact_per_truck(self) -> Money:
        """
        Get how much common costs add to each truck's monthly expenses.
        
        This is useful for reporting and showing cost allocation.
        """
        common_costs = self._costs_repo.find_common_costs()
        if not common_costs:
            return Money(0)
        
        return common_costs.total()
