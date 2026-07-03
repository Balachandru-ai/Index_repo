from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, Employee
from schemas import EmployeeCreate

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://13.48.149.24",
        "http://localhost",
        "http://127.0.0.1",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Home API
@app.get("/")
def home():
    return {"message": "Employee Management API"}


# Create Employee
@app.post("/employees")
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = Employee(
        name=employee.name,
        department=employee.department,
        salary=employee.salary,
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


# Get All Employees
@app.get("/employees")
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()


# Get Employee by ID
@app.get("/employees/{emp_id}")
def get_employee(emp_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == emp_id).first()

    if not employee:
        return {"message": "Employee not found"}

    return employee


# Update Employee
@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, employee: EmployeeCreate, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()

    if not emp:
        return {"message": "Employee not found"}

    emp.name = employee.name
    emp.department = employee.department
    emp.salary = employee.salary

    db.commit()
    db.refresh(emp)

    return emp


# Delete Employee
@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()

    if not emp:
        return {"message": "Employee not found"}

    db.delete(emp)
    db.commit()

    return {"message": "Employee deleted successfully"}
