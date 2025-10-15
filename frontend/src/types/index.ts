import * as React from 'react';

// Базовые типы
export interface BaseEntity {
  id: number;
  created_at: string;
  updated_at: string;
}

// Траки
export interface Truck extends BaseEntity {
  tractor_no: string;
}

export interface TruckCreate {
  tractor_no: string;
}

// Фиксированные стоимости
export interface FixedCostsCommon extends BaseEntity {
  ifta: number;
  insurance: number;
  eld: number;
  tablet: number;
  tolls: number;
}

export interface FixedCostsTruck extends BaseEntity {
  truck: number;
  truck_tractor_no?: string;
  truck_payment: number;
  trailer_payment: number;
  physical_damage_insurance_truck: number;
  physical_damage_insurance_trailer: number;
}

export interface FixedCostsTruckCreate {
  truck: number;
  truck_payment: number;
  trailer_payment: number;
  physical_damage_insurance_truck: number;
  physical_damage_insurance_trailer: number;
}

// Переменные затраты
export interface TruckVariableCosts extends BaseEntity {
  period_month: string;
  truck: number;
  truck_tractor_no?: string;
  driver_name?: string;
  total_rev: number;
  total_miles: number;
  salary: number;
  fuel: number;
  tolls: number;
  cost_snapshot?: number;
}

export interface TruckVariableCostsCreate {
  period_month: string;
  truck: number;
  driver_name?: string;
  total_rev: number;
  total_miles: number;
  salary: number;
  fuel: number;
  tolls: number;
  cost_snapshot?: number;
}

// Текущие переменные затраты (без привязки к периоду)
export interface TruckCurrentVariableCosts extends BaseEntity {
  truck: number;
  truck_tractor_no?: string;
  driver_name?: string;
  total_rev: number;
  total_miles: number;
  salary: number;
  fuel: number;
  tolls: number;
}

export interface TruckCurrentVariableCostsCreate {
  truck: number;
  driver_name?: string;
  total_rev: number;
  total_miles: number;
  salary: number;
  fuel: number;
  tolls: number;
}

// Снимки
export interface CostSnapshot extends BaseEntity {
  snapshot_at: string;
  period_date: string;
  label?: string;
}

export interface CostSnapshotCreate {
  period_date: string;
  label?: string;
}

export interface SnapshotComparison {
  snapshots: CostSnapshot[];
  common_costs: Array<{
    snapshot_id: number;
    ifta: number;
    insurance: number;
    eld: number;
    tablet: number;
    tolls: number;
  }>;
  truck_costs: Array<{
    snapshot_id: number;
    truck_id: number;
    truck_tractor_no: string;
    truck_payment: number;
    trailer_payment: number;
    physical_damage_insurance_truck: number;
    physical_damage_insurance_trailer: number;
  }>;
}

// Аналитика
export interface ProfitabilityCalculation extends BaseEntity {
  truck: number;
  truck_tractor_no?: string;
  period_month: string;
  total_revenue: number;
  total_miles: number;
  salary: number;
  fuel: number;
  variable_tolls: number;
  common_ifta: number;
  common_insurance: number;
  common_eld: number;
  common_tablet: number;
  common_tolls: number;
  truck_payment: number;
  trailer_payment: number;
  truck_insurance: number;
  trailer_insurance: number;
  total_variable_costs: number;
  total_fixed_costs: number;
  total_costs: number;
  profit: number;
  profit_margin: number;
  profit_per_mile: number;
}

export interface ProfitabilitySummary {
  total_trucks: number;
  total_revenue: number;
  total_costs: number;
  total_profit: number;
  average_profit_margin: number;
  period_month: string;
}

export interface TruckProfitability {
  truck_id: number;
  truck_tractor_no: string;
  total_revenue: number;
  total_costs: number;
  profit: number;
  profit_margin: number;
  profit_per_mile: number;
}

// API Response типы
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}

// UI типы
export interface TableColumn<T> {
  key: keyof T;
  title: string;
  sortable?: boolean;
  render?: (value: any, item: T) => React.ReactNode;
}

export interface SelectOption {
  value: string | number;
  label: string;
}

// Формы
export interface FormField {
  name: string;
  label: string;
  type: 'text' | 'number' | 'date' | 'select' | 'textarea';
  required?: boolean;
  placeholder?: string;
  options?: SelectOption[];
}
