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


@api.post("employees/", response=EmployeeOut, tags=["Employee"], summary="Cria um novo funcionário")
def create_employee(request, payload: EmployeeIn):
    """Create a new employee

    Args:
        payload (EmployeeIn): A payload with employee data
        {
            "first_name": "Fakeson"
            "last_name": "Faked"
            "department_id": 2
            "birthdate": "1997-03-05"
        }

    Returns:
        json (EmployeeOut): A json with employee data created
        {
            "id":
            "first_name": "Fakeson"
            "last_name": "Faked"
            "department_id": 2
            "birthdate": "1997-03-05"
        }
    """
    employee = Employee.objects.create(**payload.dict())
    return employee


@api.get("employees/", response=List[EmployeeOut], tags=["Employee"], summary="Lista todos os funcionários")
def list_employees(request):
    queryset = Employee.objects.all()
    return queryset


@api.get("employees/{employee_id}", response=EmployeeOut, tags=["Employee"], summary="Obtém um funcionário específico")
def get_employee(request, employee_id: str):
    """Route to take an individual employee

    Args:
        employee_id (str): uuid that represents a unique employee indentifier

    Returns:
        Employee: The expected return is an Employee instance
    """
    employee = get_object_or_404(Employee, id=employee_id)
    return employee


@api.put("employees/{employee_id}", response=EmployeeOut, tags=["Employee"], summary="Atualiza um funcionário")
def update_employee(request, employee_id: str, payload: EmployeeIn):
    """Update an employee

    Args:
        employee_id (str): employee id to be updated
        payload (EmployeeIn): A payload with employee data
        {
            "first_name": "Fakeson"
            "last_name": "Fake"
            "department_id": 2
            "birthdate": "1970-01-01"
        }

    Returns:
        json (EmployeeOut): A json with employee data updated
        {
            "id":
            "first_name": "Fakeson"
            "last_name": "Fake"
            "department_id": 2
            "birthdate": "1970-01-01"
        }
    """
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return employee


@api.delete("employees/{employee_id}", tags=["Employee"], summary="Deleta um funcionário")
def delete_employee(request, employee_id: str):
    """Delete an employee

    Args:
        employee_id (str): Employee id to be deleted

    """
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"Success": f"The employee with ID={employee_id} was deleted with success"}


@api.post("departments/", response=DepartmentOut, tags=["Department"], summary="Cria um novo departamento")
def create_department(request, payload: DepartmentIn):
    """Create a new department

    Args:
        payload (DepartmentIn): A payload with department title
        {
            "title": "department"
        }

    Returns:
        payload (DepartmentOut): A payload with department created
        {
            "id": 1
            "title": "department"
        }
    """
    department = Department.objects.create(**payload.dict())
    return department


@api.get("departments/", response=List[DepartmentOut], tags=["Department"], summary="Lista todos os departamentos")
def list_departments(request):
    queryset = Department.objects.all()
    return queryset


@api.get(
    "departments/{department_id}",
    response=DepartmentOut,
    tags=["Department"],
    summary="Obtém um departamento específico",
)
def get_department(request, department_id: int):
    department = get_object_or_404(Department, id=department_id)
    return department


@api.put("departments/{department_id}", response=DepartmentOut, tags=["Department"], summary="Atualiza um departamento")
def update_department(request, department_id: int, payload: DepartmentIn):
    """Update an department

    Args:
        department_id (int): Department id to be updated
        payload (DepartmentIn): A payload with department title to be updated
        {
            "title": "department"
        }

    Returns:
        payload (DepartmentOut): A payload with department updated
        {
            "id": 1
            "title": "department"
        }
    """
    department = get_object_or_404(Department, id=department_id)
    for attr, value in payload.dict().items():
        setattr(department, attr, value)
    department.save()
    return department


@api.delete("departments/{department_id}", tags=["Department"], summary="Remove um departamento")
def delete_department(request, department_id: int):
    """Delete an department

    Args:
        department_id (str): Department id to be deleted

    """
    department = get_object_or_404(Department, id=department_id)
    department.delete()
    return {"success": f"Department {department.title} was deleted with success!"}
