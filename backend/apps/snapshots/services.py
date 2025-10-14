from django.db import transaction
from django.utils import timezone
from datetime import date, datetime
from .models import CostSnapshot, CostSnapshotCommon, CostSnapshotTruck
from apps.costs.models import FixedCostsCommon, FixedCostsTruck
from apps.trucks.models import Truck


class SnapshotService:
    """Сервис для работы со снимками стоимостей"""
    
    @staticmethod
    @transaction.atomic
    def create_snapshot(period_date: datetime, label: str = None) -> CostSnapshot:
        """
        Создать снимок текущего состояния фиксированных стоимостей
        
        Args:
            period_date: Дата периода для снимка
            label: Опциональная метка для снимка
            
        Returns:
            CostSnapshot: Созданный снимок
        """
        # Создаем основной снимок
        snapshot = CostSnapshot.objects.create(
            period_date=period_date,
            label=label
        )
        
        # Копируем общие фиксированные стоимости
        common_costs = FixedCostsCommon.objects.first()
        if common_costs:
            CostSnapshotCommon.objects.create(
                snapshot=snapshot,
                ifta=common_costs.ifta,
                insurance=common_costs.insurance,
                eld=common_costs.eld,
                tablet=common_costs.tablet,
                tolls=common_costs.tolls
            )
        
        # Копируем фиксированные стоимости по тракам
        truck_costs = FixedCostsTruck.objects.all()
        for truck_cost in truck_costs:
            CostSnapshotTruck.objects.create(
                snapshot=snapshot,
                truck=truck_cost.truck,
                truck_payment=truck_cost.truck_payment,
                trailer_payment=truck_cost.trailer_payment,
                physical_damage_insurance_truck=truck_cost.physical_damage_insurance_truck,
                physical_damage_insurance_trailer=truck_cost.physical_damage_insurance_trailer
            )
        
        return snapshot
    
    @staticmethod
    def get_snapshot_comparison(snapshot_ids: list) -> dict:
        """
        Сравнить несколько снимков
        
        Args:
            snapshot_ids: Список ID снимков для сравнения
            
        Returns:
            dict: Данные для сравнения снимков
        """
        snapshots = CostSnapshot.objects.filter(id__in=snapshot_ids).order_by('snapshot_at')
        
        comparison_data = {
            'snapshots': [],
            'common_costs': [],
            'truck_costs': []
        }
        
        for snapshot in snapshots:
            snapshot_data = {
                'id': snapshot.id,
                'snapshot_at': snapshot.snapshot_at,
                'period_date': snapshot.period_date,
                'label': snapshot.label
            }
            comparison_data['snapshots'].append(snapshot_data)
            
            # Общие стоимости
            try:
                common = CostSnapshotCommon.objects.get(snapshot=snapshot)
                comparison_data['common_costs'].append({
                    'snapshot_id': snapshot.id,
                    'ifta': common.ifta,
                    'insurance': common.insurance,
                    'eld': common.eld,
                    'tablet': common.tablet,
                    'tolls': common.tolls
                })
            except CostSnapshotCommon.DoesNotExist:
                comparison_data['common_costs'].append({
                    'snapshot_id': snapshot.id,
                    'ifta': 0,
                    'insurance': 0,
                    'eld': 0,
                    'tablet': 0,
                    'tolls': 0
                })
            
            # Стоимости по тракам
            truck_costs = CostSnapshotTruck.objects.filter(snapshot=snapshot)
            for truck_cost in truck_costs:
                comparison_data['truck_costs'].append({
                    'snapshot_id': snapshot.id,
                    'truck_id': truck_cost.truck.id,
                    'truck_tractor_no': truck_cost.truck.tractor_no,
                    'truck_payment': truck_cost.truck_payment,
                    'trailer_payment': truck_cost.trailer_payment,
                    'physical_damage_insurance_truck': truck_cost.physical_damage_insurance_truck,
                    'physical_damage_insurance_trailer': truck_cost.physical_damage_insurance_trailer
                })
        
        return comparison_data
    
    @staticmethod
    def restore_from_snapshot(snapshot_id: int) -> bool:
        """
        Восстановить текущие фиксированные стоимости из снимка
        
        Args:
            snapshot_id: ID снимка для восстановления
            
        Returns:
            bool: True если восстановление прошло успешно
        """
        try:
            snapshot = CostSnapshot.objects.get(id=snapshot_id)
            
            with transaction.atomic():
                # Восстанавливаем общие стоимости
                try:
                    snapshot_common = CostSnapshotCommon.objects.get(snapshot=snapshot)
                    common_costs, created = FixedCostsCommon.objects.get_or_create(
                        defaults={
                            'ifta': snapshot_common.ifta,
                            'insurance': snapshot_common.insurance,
                            'eld': snapshot_common.eld,
                            'tablet': snapshot_common.tablet,
                            'tolls': snapshot_common.tolls
                        }
                    )
                    if not created:
                        common_costs.ifta = snapshot_common.ifta
                        common_costs.insurance = snapshot_common.insurance
                        common_costs.eld = snapshot_common.eld
                        common_costs.tablet = snapshot_common.tablet
                        common_costs.tolls = snapshot_common.tolls
                        common_costs.save()
                except CostSnapshotCommon.DoesNotExist:
                    pass
                
                # Восстанавливаем стоимости по тракам
                snapshot_trucks = CostSnapshotTruck.objects.filter(snapshot=snapshot)
                for snapshot_truck in snapshot_trucks:
                    truck_costs, created = FixedCostsTruck.objects.get_or_create(
                        truck=snapshot_truck.truck,
                        defaults={
                            'truck_payment': snapshot_truck.truck_payment,
                            'trailer_payment': snapshot_truck.trailer_payment,
                            'physical_damage_insurance_truck': snapshot_truck.physical_damage_insurance_truck,
                            'physical_damage_insurance_trailer': snapshot_truck.physical_damage_insurance_trailer
                        }
                    )
                    if not created:
                        truck_costs.truck_payment = snapshot_truck.truck_payment
                        truck_costs.trailer_payment = snapshot_truck.trailer_payment
                        truck_costs.physical_damage_insurance_truck = snapshot_truck.physical_damage_insurance_truck
                        truck_costs.physical_damage_insurance_trailer = snapshot_truck.physical_damage_insurance_trailer
                        truck_costs.save()
            
            return True
            
        except CostSnapshot.DoesNotExist:
            return False

    @staticmethod
    def get_latest_snapshot_for_period(period_date: datetime) -> CostSnapshot | None:
        """Вернуть последний снимок с period_date <= указанной дате периода.

        При равенстве нескольких по period_date приоритет по времени создания (snapshot_at).
        """
        return (
            CostSnapshot.objects
            .filter(period_date__lte=period_date)
            .order_by('-period_date', '-snapshot_at')
            .first()
        )

    @staticmethod
    def get_common_costs_from_snapshot(snapshot: CostSnapshot) -> dict:
        """Извлечь общие фиксированные стоимости из снимка в виде словаря."""
        try:
            common = CostSnapshotCommon.objects.get(snapshot=snapshot)
            return {
                'ifta': common.ifta,
                'insurance': common.insurance,
                'eld': common.eld,
                'tablet': common.tablet,
                'tolls': common.tolls,
            }
        except CostSnapshotCommon.DoesNotExist:
            return {'ifta': 0, 'insurance': 0, 'eld': 0, 'tablet': 0, 'tolls': 0}

    @staticmethod
    def get_truck_costs_from_snapshot(snapshot: CostSnapshot, truck: Truck) -> dict:
        """Извлечь фиксированные стоимости по траку из снимка в виде словаря."""
        try:
            tc = CostSnapshotTruck.objects.get(snapshot=snapshot, truck=truck)
            return {
                'truck_payment': tc.truck_payment,
                'trailer_payment': tc.trailer_payment,
                'physical_damage_insurance_truck': tc.physical_damage_insurance_truck,
                'physical_damage_insurance_trailer': tc.physical_damage_insurance_trailer,
            }
        except CostSnapshotTruck.DoesNotExist:
            return {
                'truck_payment': 0,
                'trailer_payment': 0,
                'physical_damage_insurance_truck': 0,
                'physical_damage_insurance_trailer': 0,
            }

    @staticmethod
    def get_snapshot_details(snapshot: CostSnapshot) -> dict:
        """Получить детали снимка: общие фикс-стоимости и по тракам."""
        from .models import CostSnapshotTruck
        
        # Получаем общие затраты
        common_costs = SnapshotService.get_common_costs_from_snapshot(snapshot)
        
        # Получаем затраты по тракам
        truck_costs = CostSnapshotTruck.objects.filter(snapshot=snapshot)
        trucks_data = []
        for tc in truck_costs:
            trucks_data.append({
                'truck_id': tc.truck.id,
                'truck_tractor_no': tc.truck.tractor_no,
                'truck_payment': tc.truck_payment,
                'trailer_payment': tc.trailer_payment,
                'physical_damage_insurance_truck': tc.physical_damage_insurance_truck,
                'physical_damage_insurance_trailer': tc.physical_damage_insurance_trailer,
            })
        
        return {
            'common': common_costs,
            'trucks': trucks_data
        }

