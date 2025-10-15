import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.trucks.models import Truck
from apps.costs.models import (
    FixedCostsCommon,
    FixedCostsTruck,
    TruckVariableCosts,
    TruckCurrentVariableCosts,
)
from apps.snapshots.models import (
    CostSnapshot,
    CostSnapshotCommon,
    CostSnapshotTruck,
)


class Command(BaseCommand):
    help = "Генерирует тестовые данные: траки, фикс/переменные затраты и снимки по периодам"

    def add_arguments(self, parser):
        parser.add_argument("--trucks", type=int, default=10, help="Количество траков для генерации")
        parser.add_argument(
            "--months",
            type=int,
            default=6,
            help="Количество месячных периодов для создания снимков (скринов)",
        )
        parser.add_argument(
            "--seed",
            type=int,
            default=None,
            help="Фиксировать random seed для воспроизводимости",
        )
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Очистить связанные таблицы перед генерацией (осторожно)",
        )

    def handle(self, *args, **options):
        num_trucks = options["trucks"]
        num_months = options["months"]
        rng_seed = options["seed"]
        do_flush = options["flush"]

        if rng_seed is not None:
            random.seed(rng_seed)

        with transaction.atomic():
            if do_flush:
                self._flush_all()

            trucks = self._ensure_trucks(num_trucks)
            common = self._ensure_common_fixed_costs()
            self._ensure_fixed_costs_for_trucks(trucks)

            # Создаем текущие переменные данные для каждого трака
            self._generate_current_variable_costs(trucks)

            # Создаем месячные снимки и переменные затраты внутри каждого
            self._generate_snapshots_with_costs(trucks, common, num_months)

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно сгенерированы"))

    # --- helpers ---
    def _flush_all(self):
        TruckVariableCosts.objects.all().delete()
        TruckCurrentVariableCosts.objects.all().delete()
        CostSnapshotTruck.objects.all().delete()
        CostSnapshotCommon.objects.all().delete()
        CostSnapshot.objects.all().delete()
        FixedCostsTruck.objects.all().delete()
        FixedCostsCommon.objects.all().delete()

    def _ensure_trucks(self, target_count: int):
        trucks = list(Truck.objects.all())
        to_create = max(0, target_count - len(trucks))
        if to_create:
            base = len(trucks) + 1
            for i in range(to_create):
                tractor_no = f"TRK-{base + i:03d}"
                trucks.append(Truck.objects.create(tractor_no=tractor_no))
        return trucks

    def _ensure_common_fixed_costs(self) -> FixedCostsCommon:
        common = FixedCostsCommon.objects.first()
        if common is None:
            common = FixedCostsCommon.objects.create(
                ifta=self._money(150, 400),
                insurance=self._money(800, 2000),
                eld=self._money(20, 60),
                tablet=self._money(25, 60),
                tolls=self._money(50, 250),
            )
        return common

    def _ensure_fixed_costs_for_trucks(self, trucks):
        existing_by_truck_id = {
            fc.truck_id: fc for fc in FixedCostsTruck.objects.filter(truck_id__in=[t.id for t in trucks])
        }
        for truck in trucks:
            if truck.id in existing_by_truck_id:
                continue
            FixedCostsTruck.objects.create(
                truck=truck,
                truck_payment=self._money(1200, 2800),
                trailer_payment=self._money(300, 900),
                physical_damage_insurance_truck=self._money(150, 450),
                physical_damage_insurance_trailer=self._money(60, 180),
            )

    def _generate_current_variable_costs(self, trucks):
        for truck in trucks:
            # Случайная зарплата/топливо/пробег/т.д. для текущего статуса
            defaults = {
                "driver_name": self._driver_name(),
                "total_rev": self._money(8000, 22000),
                "total_miles": random.randint(2000, 9000),
                "salary": self._money(1500, 6000),
                "fuel": self._money(1200, 8000),
                "tolls": self._money(50, 600),
            }
            TruckCurrentVariableCosts.objects.update_or_create(truck=truck, defaults=defaults)

    def _generate_snapshots_with_costs(self, trucks, common: FixedCostsCommon, months: int):
        today = date.today().replace(day=1)
        periods = [self._shift_months(today, -i) for i in range(months)]
        periods.reverse()  # от старых к новым

        for idx, period_date in enumerate(periods, start=1):
            snapshot = CostSnapshot.objects.create(period_date=period_date, label=f"M{idx:02d}")

            # Общие фиксированные в снимке с небольшим дрейфом значений
            CostSnapshotCommon.objects.create(
                snapshot=snapshot,
                ifta=self._drift(common.ifta, 0.15),
                insurance=self._drift(common.insurance, 0.2),
                eld=self._drift(common.eld, 0.2),
                tablet=self._drift(common.tablet, 0.2),
                tolls=self._drift(common.tolls, 0.25),
            )

            # Фиксированные по тракам с дрейфом
            fc_by_truck = {fc.truck_id: fc for fc in FixedCostsTruck.objects.filter(truck__in=trucks)}
            for truck in trucks:
                base = fc_by_truck.get(truck.id)
                if not base:
                    continue
                CostSnapshotTruck.objects.create(
                    snapshot=snapshot,
                    truck=truck,
                    truck_payment=self._drift(base.truck_payment, 0.1),
                    trailer_payment=self._drift(base.trailer_payment, 0.1),
                    physical_damage_insurance_truck=self._drift(base.physical_damage_insurance_truck, 0.12),
                    physical_damage_insurance_trailer=self._drift(base.physical_damage_insurance_trailer, 0.12),
                )

                # Переменные затраты на период (snapshot)
                TruckVariableCosts.objects.create(
                    snapshot=snapshot,
                    truck=truck,
                    driver_name=self._driver_name(),
                    total_rev=self._money(10000, 35000),
                    total_miles=random.randint(3000, 12000),
                    salary=self._money(2000, 9000),
                    fuel=self._money(1500, 12000),
                    tolls=self._money(50, 900),
                )

    # --- utils ---
    def _shift_months(self, first_day: date, delta_months: int) -> date:
        y = first_day.year + (first_day.month + delta_months - 1) // 12
        m = (first_day.month + delta_months - 1) % 12 + 1
        return date(y, m, 1)

    def _money(self, low: int, high: int):
        return round(random.uniform(low, high), 2)

    def _drift(self, value, pct: float):
        # value — Decimal, приводим к float для дрейфа, затем обратно к округленному float
        base = float(value)
        change = base * random.uniform(-pct, pct)
        return round(base + change, 2)

    def _driver_name(self):
        first = [
            "Ivan",
            "Petr",
            "Oleg",
            "Sergey",
            "Dmitry",
            "Alex",
            "Max",
            "Vladimir",
            "Nikolay",
            "Andrey",
        ]
        last = [
            "Ivanov",
            "Petrov",
            "Sidorov",
            "Smirnov",
            "Kuznetsov",
            "Popov",
            "Volkov",
            "Sokolov",
            "Mikhailov",
            "Fedorov",
        ]
        return f"{random.choice(first)} {random.choice(last)}"


