"""
HTTP клиент для взаимодействия с FastAPI REST API.
"""
import requests
from typing import List, Dict, Any, Optional
import streamlit as st


class APIClient:
    """Базовый HTTP клиент для API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Обработка ответа от API."""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise ValueError(f"Ресурс не найден: {response.text}")
            elif response.status_code == 400:
                error_detail = response.json().get('detail', str(e))
                raise ValueError(f"Ошибка валидации: {error_detail}")
            else:
                raise ValueError(f"Ошибка API ({response.status_code}): {response.text}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Ошибка соединения с API: {str(e)}")
    
    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET запрос."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params)
        return self._handle_response(response)
    
    def _post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """POST запрос."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=data)
        return self._handle_response(response)
    
    def _put(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """PUT запрос."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(url, json=data)
        return self._handle_response(response)
    
    def _delete(self, endpoint: str) -> bool:
        """DELETE запрос."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url)
        try:
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise ValueError(f"Ресурс не найден: {response.text}")
            else:
                raise ValueError(f"Ошибка API ({response.status_code}): {response.text}")


class TruckAPIClient(APIClient):
    """Клиент для работы с траками."""
    
    @st.cache_data(ttl=60)  # Кэш на 60 секунд
    def get_trucks(self) -> List[Dict[str, Any]]:
        """Получить все траки."""
        response = self._get("/api/v1/trucks/")
        return response.get("trucks", [])
    
    @st.cache_data(ttl=60)
    def get_truck(self, truck_id: int) -> Dict[str, Any]:
        """Получить трак по ID."""
        return self._get(f"/api/v1/trucks/{truck_id}")
    
    def create_truck(self, tractor_no: str) -> Dict[str, Any]:
        """Создать трак."""
        data = {"tractor_no": tractor_no}
        result = self._post("/api/v1/trucks/", data)
        st.cache_data.clear()  # Очищаем кэш
        return result
    
    def update_truck(self, truck_id: int, tractor_no: str) -> Dict[str, Any]:
        """Обновить трак."""
        data = {"tractor_no": tractor_no}
        result = self._put(f"/api/v1/trucks/{truck_id}", data)
        st.cache_data.clear()  # Очищаем кэш
        return result
    
    def delete_truck(self, truck_id: int) -> bool:
        """Удалить трак."""
        result = self._delete(f"/api/v1/trucks/{truck_id}")
        st.cache_data.clear()  # Очищаем кэш
        return result
    
    def can_delete_truck(self, truck_id: int) -> bool:
        """Проверить, можно ли удалить трак."""
        response = self._get(f"/api/v1/trucks/{truck_id}/can-delete")
        return response.get("can_delete", False)


class CostsAPIClient(APIClient):
    """Клиент для работы с затратами."""
    
    @st.cache_data(ttl=60)
    def get_truck_costs(self, truck_id: int) -> Dict[str, float]:
        """Получить затраты трака."""
        return self._get(f"/api/v1/costs/trucks/{truck_id}")
    
    def update_truck_costs(self, truck_id: int, cost_updates: Dict[str, float]) -> Dict[str, float]:
        """Обновить затраты трака."""
        result = self._put(f"/api/v1/costs/trucks/{truck_id}", cost_updates)
        st.cache_data.clear()  # Очищаем кэш
        return result
    
    @st.cache_data(ttl=60)
    def get_common_costs(self) -> Dict[str, float]:
        """Получить общие затраты."""
        return self._get("/api/v1/costs/common")
    
    def update_common_costs(self, cost_updates: Dict[str, float]) -> Dict[str, float]:
        """Обновить общие затраты."""
        result = self._put("/api/v1/costs/common", cost_updates)
        st.cache_data.clear()  # Очищаем кэш
        return result
    
    def calculate_costs(self, truck_id: int, revenue: float, variable_costs: Dict[str, float]) -> Dict[str, Any]:
        """Рассчитать затраты и прибыль."""
        data = {
            "truck_id": truck_id,
            "revenue": revenue,
            "variable_costs": variable_costs
        }
        return self._post("/api/v1/costs/calculate", data)
    
    def get_common_costs_impact(self) -> float:
        """Получить влияние общих затрат на каждый трак."""
        response = self._get("/api/v1/costs/common/impact-per-truck")
        return response.get("common_costs_impact_per_truck", 0.0)


class MonthlyAPIClient(APIClient):
    """Клиент для работы с месячными данными."""
    
    @st.cache_data(ttl=60)
    def get_monthly_data_for_truck(self, truck_id: int) -> List[Dict[str, Any]]:
        """Получить месячные данные для трака."""
        response = self._get(f"/api/v1/monthly/trucks/{truck_id}")
        return response.get("monthly_data", [])
    
    @st.cache_data(ttl=60)
    def get_monthly_data(self, monthly_id: int) -> Dict[str, Any]:
        """Получить месячные данные по ID."""
        return self._get(f"/api/v1/monthly/{monthly_id}")
    
    def create_monthly_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Создать месячные данные."""
        result = self._post("/api/v1/monthly/", data)
        st.cache_data.clear()  # Очищаем кэш
        return result
    
    def update_monthly_data(self, monthly_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Обновить месячные данные."""
        result = self._put(f"/api/v1/monthly/{monthly_id}", updates)
        st.cache_data.clear()  # Очищаем кэш
        return result
    
    def delete_monthly_data(self, monthly_id: int) -> bool:
        """Удалить месячные данные."""
        result = self._delete(f"/api/v1/monthly/{monthly_id}")
        st.cache_data.clear()  # Очищаем кэш
        return result
    
    @st.cache_data(ttl=60)
    def get_available_periods(self) -> List[Dict[str, Any]]:
        """Получить доступные периоды."""
        response = self._get("/api/v1/monthly/periods/available")
        return response.get("periods", [])
    
    def upload_monthly_data(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Загрузить месячные данные из файла."""
        url = f"{self.base_url}/api/v1/monthly/upload"
        files = {"file": (filename, file_content)}
        
        # Для загрузки файлов используем multipart/form-data
        response = self.session.post(url, files=files)
        result = self._handle_response(response)
        st.cache_data.clear()  # Очищаем кэш
        return result


class ReportsAPIClient(APIClient):
    """Клиент для работы с отчетами."""
    
    @st.cache_data(ttl=300)  # Кэш на 5 минут
    def get_truck_report(self, truck_id: int, period: Optional[str] = None) -> Dict[str, Any]:
        """Получить отчет по траку."""
        params = {"period": period} if period else None
        return self._get(f"/api/v1/reports/truck/{truck_id}", params)
    
    @st.cache_data(ttl=300)
    def get_fleet_report(self) -> Dict[str, Any]:
        """Получить флотовый отчет."""
        return self._get("/api/v1/reports/fleet")
    
    @st.cache_data(ttl=300)
    def get_period_report(self, period: str) -> Dict[str, Any]:
        """Получить отчет за период."""
        return self._get(f"/api/v1/reports/period/{period}")
    
    @st.cache_data(ttl=300)
    def get_profitability_analysis(self) -> List[Dict[str, Any]]:
        """Получить анализ прибыльности."""
        return self._get("/api/v1/reports/profitability")
    
    @st.cache_data(ttl=300)
    def get_report_summary(self) -> Dict[str, Any]:
        """Получить сводку по отчетам."""
        return self._get("/api/v1/reports/summary")


class TruckManagementAPI:
    """Главный класс для работы с API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.trucks = TruckAPIClient(base_url)
        self.costs = CostsAPIClient(base_url)
        self.monthly = MonthlyAPIClient(base_url)
        self.reports = ReportsAPIClient(base_url)
        self.base_url = base_url
    
    def health_check(self) -> bool:
        """Проверить состояние API."""
        try:
            response = self._get("/health")
            return response.get("status") == "healthy"
        except:
            return False
    
    def _get(self, endpoint: str) -> Dict[str, Any]:
        """Внутренний GET запрос."""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()


# Глобальный экземпляр API клиента
api = TruckManagementAPI()
