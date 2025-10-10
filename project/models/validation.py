"""
Validation business rules and logic.
Moved from domain.services.validation_service.
"""
from typing import List
from dataclasses import dataclass
from .entities import Truck, Money


@dataclass
class ValidationResult:
    """Result of a validation operation."""
    is_valid: bool
    errors: List[str]
    
    @classmethod
    def success(cls) -> 'ValidationResult':
        return cls(is_valid=True, errors=[])
    
    @classmethod
    def failure(cls, errors: List[str]) -> 'ValidationResult':
        return cls(is_valid=False, errors=errors)
    
    def add_error(self, error: str) -> None:
        self.errors.append(error)
        self.is_valid = False


class ValidationService:
    """
    Business rule validation service.
    
    Centralizes validation logic that spans multiple entities
    or requires external dependencies.
    """
    
    def validate_truck_creation(self, tractor_no: str) -> ValidationResult:
        """
        Validate truck creation business rules.
        
        Rules:
        1. Tractor number format validation
        2. Length constraints
        3. Character constraints
        """
        errors = []
        
        if not tractor_no or not tractor_no.strip():
            errors.append("Номер трака не может быть пустым")
        else:
            tractor_no = tractor_no.strip()
            
            if len(tractor_no) < 2:
                errors.append("Номер трака должен содержать минимум 2 символа")
            
            if len(tractor_no) > 20:
                errors.append("Номер трака не может превышать 20 символов")
            
            # Business rule: Only alphanumeric and basic punctuation allowed
            allowed_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_")
            if not all(c in allowed_chars for c in tractor_no):
                errors.append("Номер трака может содержать только буквы, цифры, дефисы и подчеркивания")
        
        if errors:
            return ValidationResult.failure(errors)
        return ValidationResult.success()
    
    def validate_money_amount(self, amount: str, field_name: str) -> ValidationResult:
        """
        Validate monetary amount input.
        
        Rules:
        1. Must be a valid decimal number
        2. Cannot be negative for cost fields
        3. Reasonable limits (not too large)
        """
        errors = []
        
        if not amount or not amount.strip():
            errors.append(f"{field_name} не может быть пустым")
            return ValidationResult.failure(errors)
        
        try:
            money_value = Money(amount.strip())
            
            # Business rule: Most costs cannot be negative
            if money_value.is_negative:
                errors.append(f"{field_name} не может быть отрицательным")
            
            # Business rule: Reasonable upper limit (prevent data entry errors)
            if money_value.amount > 1000000:  # $1M limit
                errors.append(f"{field_name} превышает разумный лимит ($1,000,000)")
                
        except (ValueError, TypeError):
            errors.append(f"{field_name} должен быть корректным числом")
        
        if errors:
            return ValidationResult.failure(errors)
        return ValidationResult.success()
    
    def validate_truck_update(self, 
                            current_truck: Truck,
                            new_tractor_no: str) -> ValidationResult:
        """
        Validate truck update operation.
        
        Combines truck creation validation with update-specific rules.
        """
        # First validate the new tractor number format
        format_validation = self.validate_truck_creation(new_tractor_no)
        if not format_validation.is_valid:
            return format_validation
        
        # Additional update-specific validations can go here
        # For example: checking if the truck is in use, etc.
        
        return ValidationResult.success()
    
    def validate_fixed_costs_update(self, cost_updates: dict) -> ValidationResult:
        """
        Validate fixed costs update operation.
        
        Args:
            cost_updates: Dictionary of field_name -> value pairs
        """
        result = ValidationResult.success()
        
        for field_name, value in cost_updates.items():
            if isinstance(value, (str, int, float)):
                field_validation = self.validate_money_amount(str(value), field_name)
                if not field_validation.is_valid:
                    result.errors.extend(field_validation.errors)
                    result.is_valid = False
        
        return result
