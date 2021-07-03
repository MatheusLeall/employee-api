from datetime import date
from typing import Any, List

from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema

from .models import Department, Employee

api = NinjaAPI()


class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None  # The None indicate that this attribute is optional
    birthdate: date = None


class EmployeeOut(Schema):
    id: Any
    first_name: str
    last_name: str
    department_id: int = None  # The None indicate that this attribute is optional
    birthdate: date = None


class DepartmentIn(Schema):
    title: str


class DepartmentOut(Schema):
    id: int
    title: str


@api.post("employees/")
def create_employee(request, payload: EmployeeIn):
    """Create a new employee

    Args:
        payload (EmployeeIn): A payload with employee data
        {
            first_name: str
            last_name: str
            department_id: int = None
            birthdate: date = None
        }

    Returns:
        id (str): Expected return is a uuid of the created user
    """
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}


@api.get("employees/", response=List[EmployeeOut])
def list_employees(request):
    queryset = Employee.objects.all()
    return queryset


@api.get("employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: str):
    """Route to take an individual employee

    Args:
        employee_id (str): uuid that represents a unique employee indentifier

    Returns:
        Employee: The expected return is an Employee instance
    """
    employee = get_object_or_404(Employee, id=employee_id)
    return employee


@api.put("employees/{employee_id}", response=EmployeeOut)
def update_employee(request, employee_id: str, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return employee


@api.delete("employees/{employee_id}")
def delete_employee(request, employee_id: str):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"Success": f"The employee with ID={employee_id} was deleted with success"}


@api.post("departments/", response=DepartmentOut)
def create_department(request, payload: DepartmentIn):
    department = Department.objects.create(**payload.dict())
    return department


@api.get("departments/", response=List[DepartmentOut])
def list_departments(request):
    queryset = Department.objects.all()
    return queryset


@api.get("departments/{department_id}", response=DepartmentOut)
def get_department(request, department_id: int):
    department = get_object_or_404(Department, id=department_id)
    return department
