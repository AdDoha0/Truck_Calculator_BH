from django.db.models import Sum, Avg, Count
from decimal import Decimal
from datetime import date
from typing import Dict, List, Any
from .models import ProfitabilityCalculation
from apps.trucks.models import Truck
from apps.costs.models import TruckVariableCosts, FixedCostsCommon, FixedCostsTruck


class AnalyticsService:
    """Сервис для аналитики и расчетов прибыльности"""
    
    @staticmethod
    def calculate_profitability_for_period(period_month: date) -> List[ProfitabilityCalculation]:
        """
        Рассчитать прибыльность для всех траков за период
        
        Args:
            period_month: Месяц для расчета
            
        Returns:
            List[ProfitabilityCalculation]: Список расчетов прибыльности
        """
        calculations = []
        
        # Получаем общие фиксированные стоимости
        common_costs = FixedCostsCommon.objects.first()
        common_costs_data = {
            'ifta': common_costs.ifta if common_costs else Decimal('0'),
            'insurance': common_costs.insurance if common_costs else Decimal('0'),
            'eld': common_costs.eld if common_costs else Decimal('0'),
            'tablet': common_costs.tablet if common_costs else Decimal('0'),
            'tolls': common_costs.tolls if common_costs else Decimal('0'),
        }
        
        # Получаем переменные затраты за период
        variable_costs = TruckVariableCosts.objects.filter(period_month=period_month)
        
        for variable_cost in variable_costs:
            # Получаем фиксированные стоимости для трака
            truck_fixed = FixedCostsTruck.objects.filter(truck=variable_cost.truck).first()
            truck_fixed_data = {
                'truck_payment': truck_fixed.truck_payment if truck_fixed else Decimal('0'),
                'trailer_payment': truck_fixed.trailer_payment if truck_fixed else Decimal('0'),
                'physical_damage_insurance_truck': truck_fixed.physical_damage_insurance_truck if truck_fixed else Decimal('0'),
                'physical_damage_insurance_trailer': truck_fixed.physical_damage_insurance_trailer if truck_fixed else Decimal('0'),
            }
            
            # Подготавливаем данные переменных затрат
            variable_data = {
                'total_rev': variable_cost.total_rev,
                'total_miles': variable_cost.total_miles,
                'salary': variable_cost.salary,
                'fuel': variable_cost.fuel,
                'tolls': variable_cost.tolls,
            }
            
            # Создаем или обновляем расчет
            calculation, created = ProfitabilityCalculation.objects.get_or_create(
                truck=variable_cost.truck,
                period_month=period_month,
                defaults=ProfitabilityCalculation.calculate_profitability(
                    truck=variable_cost.truck,
                    period_month=period_month,
                    variable_costs_data=variable_data,
                    fixed_costs_common=common_costs_data,
                    fixed_costs_truck=truck_fixed_data
                ).__dict__
            )
            
            if not created:
                # Обновляем существующий расчет
                new_calculation = ProfitabilityCalculation.calculate_profitability(
                    truck=variable_cost.truck,
                    period_month=period_month,
                    variable_costs_data=variable_data,
                    fixed_costs_common=common_costs_data,
                    fixed_costs_truck=truck_fixed_data
                )
                
                calculation.total_revenue = new_calculation.total_revenue
                calculation.total_miles = new_calculation.total_miles
                calculation.salary = new_calculation.salary
                calculation.fuel = new_calculation.fuel
                calculation.variable_tolls = new_calculation.variable_tolls
                calculation.common_ifta = new_calculation.common_ifta
                calculation.common_insurance = new_calculation.common_insurance
                calculation.common_eld = new_calculation.common_eld
                calculation.common_tablet = new_calculation.common_tablet
                calculation.common_tolls = new_calculation.common_tolls
                calculation.truck_payment = new_calculation.truck_payment
                calculation.trailer_payment = new_calculation.trailer_payment
                calculation.truck_insurance = new_calculation.truck_insurance
                calculation.trailer_insurance = new_calculation.trailer_insurance
                calculation.total_variable_costs = new_calculation.total_variable_costs
                calculation.total_fixed_costs = new_calculation.total_fixed_costs
                calculation.total_costs = new_calculation.total_costs
                calculation.profit = new_calculation.profit
                calculation.profit_margin = new_calculation.profit_margin
                calculation.profit_per_mile = new_calculation.profit_per_mile
                calculation.save()
            
            calculations.append(calculation)
        
        return calculations
    
    @staticmethod
    def get_profitability_summary(period_month: date) -> Dict[str, Any]:
        """
        Получить сводку по прибыльности за период
        
        Args:
            period_month: Месяц для анализа
            
        Returns:
            Dict: Сводка по прибыльности
        """
        calculations = ProfitabilityCalculation.objects.filter(period_month=period_month)
        
        if not calculations.exists():
            # Если нет расчетов, создаем их
            AnalyticsService.calculate_profitability_for_period(period_month)
            calculations = ProfitabilityCalculation.objects.filter(period_month=period_month)
        
        summary = calculations.aggregate(
            total_trucks=Count('id'),
            total_revenue=Sum('total_revenue'),
            total_costs=Sum('total_costs'),
            total_profit=Sum('profit'),
            average_profit_margin=Avg('profit_margin')
        )
        
        return {
            'total_trucks': summary['total_trucks'] or 0,
            'total_revenue': summary['total_revenue'] or Decimal('0'),
            'total_costs': summary['total_costs'] or Decimal('0'),
            'total_profit': summary['total_profit'] or Decimal('0'),
            'average_profit_margin': summary['average_profit_margin'] or Decimal('0'),
            'period_month': period_month
        }
    
    @staticmethod
    def get_truck_profitability(period_month: date) -> List[Dict[str, Any]]:
        """
        Получить прибыльность по тракам за период
        
        Args:
            period_month: Месяц для анализа
            
        Returns:
            List[Dict]: Список прибыльности по тракам
        """
        calculations = ProfitabilityCalculation.objects.filter(period_month=period_month)
        
        if not calculations.exists():
            AnalyticsService.calculate_profitability_for_period(period_month)
            calculations = ProfitabilityCalculation.objects.filter(period_month=period_month)
        
        truck_data = []
        for calc in calculations:
            truck_data.append({
                'truck_id': calc.truck.id,
                'truck_tractor_no': calc.truck.tractor_no,
                'total_revenue': calc.total_revenue,
                'total_costs': calc.total_costs,
                'profit': calc.profit,
                'profit_margin': calc.profit_margin,
                'profit_per_mile': calc.profit_per_mile
            })
        
        return truck_data
    
    @staticmethod
    def get_profitability_trends(start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """
        Получить тренды прибыльности за период
        
        Args:
            start_date: Начальная дата
            end_date: Конечная дата
            
        Returns:
            List[Dict]: Данные трендов по месяцам
        """
        calculations = ProfitabilityCalculation.objects.filter(
            period_month__gte=start_date,
            period_month__lte=end_date
        ).order_by('period_month')
        
        trends = []
        for calc in calculations:
            month_data = {
                'period_month': calc.period_month,
                'truck_id': calc.truck.id,
                'truck_tractor_no': calc.truck.tractor_no,
                'total_revenue': calc.total_revenue,
                'total_costs': calc.total_costs,
                'profit': calc.profit,
                'profit_margin': calc.profit_margin,
                'profit_per_mile': calc.profit_per_mile
            }
            trends.append(month_data)
        
        return trends

