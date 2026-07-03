const API="http://13.48.149.24:8000";

loadEmployees();

async function loadEmployees(){

    const response=await fetch(API+"/employees");

    const data=await response.json();

    let rows="";

    data.forEach(emp=>{

        rows+=`
        <tr>

        <td>${emp.id}</td>

        <td>${emp.name}</td>

        <td>${emp.department}</td>

        <td>${emp.salary}</td>

        <td>
        <button class="delete"
        onclick="deleteEmployee(${emp.id})">
        Delete
        </button>
        </td>

        </tr>
        `;
    });

    document.getElementById("employeeTable").innerHTML=rows;

}

async function addEmployee(){

    const name=document.getElementById("name").value;

    const department=document.getElementById("department").value;

    const salary=parseInt(document.getElementById("salary").value);

    await fetch(API+"/employees",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            name,
            department,
            salary
        })

    });

    document.getElementById("name").value="";
    document.getElementById("department").value="";
    document.getElementById("salary").value="";

    loadEmployees();

}

async function deleteEmployee(id){

    await fetch(API+"/employees/"+id,{
        method:"DELETE"
    });

    loadEmployees();

}
