"""
Бизнес-логика для модуля reports.
"""
from typing import List, Dict, Any, Optional
from datetime import date, datetime
from sqlalchemy.orm import Session

# from project.services.costs_service import CostsService  # Модуль не существует
# from project.services.report_service import ReportService  # Модуль не существует
from project.models.database import Truck as TruckORM, MonthlyRow as MonthlyRowORM


class ReportsAPIService:
    """API сервис для отчетов."""
    
    def __init__(self):
        # self._costs_service = CostsService()  # Модуль не существует
        # self._report_service = ReportService()  # Модуль не существует
        pass
    
    def get_truck_report(self, db: Session, truck_id: int, period: Optional[str] = None) -> Dict[str, Any]:
        """Получить детальный отчет по траку."""
        # Получаем информацию о траке
        truck = db.query(TruckORM).filter_by(id=truck_id).first()
        if not truck:
            raise ValueError(f"Трак с ID {truck_id} не найден")
        
        # Получаем месячные данные
        query = db.query(MonthlyRowORM).filter_by(truck_id=truck_id)
        if period:
            # Фильтр по периоду (если указан)
            period_date = datetime.fromisoformat(period).date()
            query = query.filter_by(period_month=period_date)
        
        monthly_rows = query.all()
        
        if not monthly_rows:
            return {
                "truck_id": truck_id,
                "tractor_no": truck.tractor_no,
                "period": period or "all",
                "revenue": 0.0,
                "total_variable_costs": 0.0,
                "total_fixed_costs": 0.0,
                "total_all_costs": 0.0,
                "profit": 0.0,
                "margin_percent": 0.0,
                "cost_breakdown": {},
                "monthly_data_count": 0
            }
        
        # Агрегируем данные
        total_revenue = sum(float(row.total_rev) for row in monthly_rows)
        variable_costs = {
            'salary': sum(float(row.salary) for row in monthly_rows),
            'fuel': sum(float(row.fuel) for row in monthly_rows),
            'tolls': sum(float(row.tolls) for row in monthly_rows),
            'repair': 0.0  # repair не хранится в MonthlyRow, используем 0
        }
        
        # Рассчитываем затраты через существующий сервис
        costs_summary = self._costs_service.calculate_truck_profitability(
            truck_id, total_revenue, variable_costs
        )
        
        cost_breakdown = self._costs_service.get_cost_breakdown_for_truck(truck_id, variable_costs)
        
        return {
            "truck_id": truck_id,
            "tractor_no": truck.tractor_no,
            "period": period or "all",
            "revenue": total_revenue,
            "total_variable_costs": costs_summary.total_variable,
            "total_fixed_costs": costs_summary.total_fixed,
            "total_all_costs": costs_summary.total_all,
            "profit": costs_summary.profit,
            "margin_percent": costs_summary.margin_percent,
            "cost_breakdown": cost_breakdown,
            "monthly_data_count": len(monthly_rows)
        }
    
    def get_fleet_report(self, db: Session) -> Dict[str, Any]:
        """Получить флотовый отчет."""
        # Получаем все траки
        trucks = db.query(TruckORM).all()
        
        if not trucks:
            return {
                "total_trucks": 0,
                "total_revenue": 0.0,
                "total_variable_costs": 0.0,
                "total_fixed_costs": 0.0,
                "total_profit": 0.0,
                "average_profit_per_truck": 0.0,
                "average_margin_percent": 0.0,
                "truck_reports": []
            }
        
        truck_reports = []
        total_revenue = 0.0
        total_variable_costs = 0.0
        total_fixed_costs = 0.0
        total_profit = 0.0
        total_margin = 0.0
        
        for truck in trucks:
            # Получаем месячные данные для трака
            monthly_rows = db.query(MonthlyRowORM).filter_by(truck_id=truck.id).all()
            
            if monthly_rows:
                truck_revenue = sum(float(row.total_rev) for row in monthly_rows)
                variable_costs = {
                    'salary': sum(float(row.salary) for row in monthly_rows),
                    'fuel': sum(float(row.fuel) for row in monthly_rows),
                    'tolls': sum(float(row.tolls) for row in monthly_rows),
                    'repair': 0.0
                }
                
                costs_summary = self._costs_service.calculate_truck_profitability(
                    truck.id, truck_revenue, variable_costs
                )
                
                truck_report = {
                    "truck_id": truck.id,
                    "tractor_no": truck.tractor_no,
                    "period": "all",
                    "revenue": truck_revenue,
                    "total_variable_costs": costs_summary.total_variable,
                    "total_fixed_costs": costs_summary.total_fixed,
                    "total_all_costs": costs_summary.total_all,
                    "profit": costs_summary.profit,
                    "margin_percent": costs_summary.margin_percent,
                    "cost_breakdown": self._costs_service.get_cost_breakdown_for_truck(truck.id, variable_costs),
                    "monthly_data_count": len(monthly_rows)
                }
                
                truck_reports.append(truck_report)
                
                total_revenue += truck_revenue
                total_variable_costs += costs_summary.total_variable
                total_fixed_costs += costs_summary.total_fixed
                total_profit += costs_summary.profit
                total_margin += costs_summary.margin_percent
        
        average_profit_per_truck = total_profit / len(trucks) if trucks else 0.0
        average_margin_percent = total_margin / len(trucks) if trucks else 0.0
        
        return {
            "total_trucks": len(trucks),
            "total_revenue": total_revenue,
            "total_variable_costs": total_variable_costs,
            "total_fixed_costs": total_fixed_costs,
            "total_profit": total_profit,
            "average_profit_per_truck": average_profit_per_truck,
            "average_margin_percent": average_margin_percent,
            "truck_reports": truck_reports
        }
    
    def get_period_report(self, db: Session, period: str) -> Dict[str, Any]:
        """Получить отчет за период."""
        try:
            period_date = datetime.fromisoformat(period).date()
        except ValueError:
            raise ValueError(f"Неверный формат периода: {period}. Используйте YYYY-MM-DD")
        
        # Получаем данные за период
        monthly_rows = db.query(MonthlyRowORM).filter_by(period_month=period_date).all()
        
        if not monthly_rows:
            return {
                "period": period,
                "year": period_date.year,
                "month": period_date.month,
                "total_trucks": 0,
                "total_revenue": 0.0,
                "total_variable_costs": 0.0,
                "total_fixed_costs": 0.0,
                "total_profit": 0.0,
                "truck_reports": []
            }
        
        # Группируем по тракам
        truck_data = {}
        for row in monthly_rows:
            if row.truck_id not in truck_data:
                truck_data[row.truck_id] = {
                    'truck_id': row.truck_id,
                    'revenue': 0.0,
                    'variable_costs': {'salary': 0.0, 'fuel': 0.0, 'tolls': 0.0, 'repair': 0.0}
                }
            
            truck_data[row.truck_id]['revenue'] += float(row.total_rev)
            truck_data[row.truck_id]['variable_costs']['salary'] += float(row.salary)
            truck_data[row.truck_id]['variable_costs']['fuel'] += float(row.fuel)
            truck_data[row.truck_id]['variable_costs']['tolls'] += float(row.tolls)
        
        truck_reports = []
        total_revenue = 0.0
        total_variable_costs = 0.0
        total_fixed_costs = 0.0
        total_profit = 0.0
        
        for truck_id, data in truck_data.items():
            # Получаем информацию о траке
            truck = db.query(TruckORM).filter_by(id=truck_id).first()
            if not truck:
                continue
            
            # Рассчитываем затраты
            costs_summary = self._costs_service.calculate_truck_profitability(
                truck_id, data['revenue'], data['variable_costs']
            )
            
            truck_report = {
                "truck_id": truck_id,
                "tractor_no": truck.tractor_no,
                "period": period,
                "revenue": data['revenue'],
                "total_variable_costs": costs_summary.total_variable,
                "total_fixed_costs": costs_summary.total_fixed,
                "total_all_costs": costs_summary.total_all,
                "profit": costs_summary.profit,
                "margin_percent": costs_summary.margin_percent,
                "cost_breakdown": self._costs_service.get_cost_breakdown_for_truck(truck_id, data['variable_costs']),
                "monthly_data_count": 1
            }
            
            truck_reports.append(truck_report)
            
            total_revenue += data['revenue']
            total_variable_costs += costs_summary.total_variable
            total_fixed_costs += costs_summary.total_fixed
            total_profit += costs_summary.profit
        
        return {
            "period": period,
            "year": period_date.year,
            "month": period_date.month,
            "total_trucks": len(truck_reports),
            "total_revenue": total_revenue,
            "total_variable_costs": total_variable_costs,
            "total_fixed_costs": total_fixed_costs,
            "total_profit": total_profit,
            "truck_reports": truck_reports
        }
    
    def get_profitability_analysis(self, db: Session) -> List[Dict[str, Any]]:
        """Получить анализ прибыльности всех траков."""
        trucks = db.query(TruckORM).all()
        analysis = []
        
        for truck in trucks:
            monthly_rows = db.query(MonthlyRowORM).filter_by(truck_id=truck.id).all()
            
            if monthly_rows:
                total_revenue = sum(float(row.total_rev) for row in monthly_rows)
                variable_costs = {
                    'salary': sum(float(row.salary) for row in monthly_rows),
                    'fuel': sum(float(row.fuel) for row in monthly_rows),
                    'tolls': sum(float(row.tolls) for row in monthly_rows),
                    'repair': 0.0
                }
                
                costs_summary = self._costs_service.calculate_truck_profitability(
                    truck.id, total_revenue, variable_costs
                )
                
                # Определяем оценку прибыльности
                margin = costs_summary.margin_percent
                if margin >= 20:
                    grade = "A"
                elif margin >= 15:
                    grade = "B"
                elif margin >= 10:
                    grade = "C"
                elif margin >= 5:
                    grade = "D"
                else:
                    grade = "F"
                
                analysis.append({
                    "truck_id": truck.id,
                    "tractor_no": truck.tractor_no,
                    "total_revenue": total_revenue,
                    "total_costs": costs_summary.total_all,
                    "profit": costs_summary.profit,
                    "margin_percent": costs_summary.margin_percent,
                    "is_profitable": costs_summary.profit > 0,
                    "profitability_grade": grade
                })
        
        return analysis


# Глобальный экземпляр сервиса
reports_api_service = ReportsAPIService()
