function initializeFunction() {
    routeCheckFunc()
}

function routeCheckFunc() {
    let getPathNames = window.location.pathname.split('/')
    getPathNames.forEach((data) => {
        if (data) {
            $('.routeUi').append($(`<li class="breadCrumbItem">
            <span class="d-block ellipsis breadCrumbsLastName">${data}</span></li>`)
            );
        }
    })
}

function filterStaffByDepartment() {
        const department = document.getElementById("department").value;
        const staffSelect = document.getElementById("staff_id");

        if (!department) return;

        fetch("/staff/filter-staff-by-dept", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ department: department })
        })
        .then(response => response.json())
        .then(data => {

            // Clear old options
            staffSelect.innerHTML = '<option value="">-- Select Staff --</option>';

            data.forEach(staff => {
                let option = document.createElement("option");
                option.value = staff.id;
                option.textContent = staff.name;
                staffSelect.appendChild(option);
            });

            // Clear subjects also
            document.getElementById("subject_id").innerHTML =
                '<option value="">-- Select Subject --</option>';
        });
    }


    function filterSubjectByStaff() {
        const department = document.getElementById("department").value;
        const staff_id = document.getElementById("staff_id").value;
        const subjectSelect = document.getElementById("subject_id");

        if (!staff_id || !department) return;

        fetch("/staff/filter-subject-by-staff", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ staff_id: staff_id, department: department })
        })
        .then(response => response.json())
        .then(data => {

            subjectSelect.innerHTML = '<option value="">-- Select Subject --</option>';

                data.forEach(subject => {
                    let option = document.createElement("option");
                    option.value = subject.id;
                    option.textContent =
                        subject.subject_name +
                        "(Sem " + subject.semester + ")";

                subjectSelect.appendChild(option);
                });
            });
        }

    // advance level filtering


    function applyFilters() {

        const semester = document.getElementById("semester").value;
        const department = document.getElementById("department").value;
        const staff_id = document.getElementById("staff_id").value;
        const subject_id = document.getElementById("subject_id").value;

        fetch("/filter-data", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                semester: semester,
                department: department,
                staff_id: staff_id,
                subject_id: subject_id
            })
        })
        .then(response => response.json())
        .then(data => {

            // Update staff dropdown
            const staffSelect = document.getElementById("staff_id");
            staffSelect.innerHTML = '<option value="">-- Select Staff --</option>';

            data.staff.forEach(staff => {
                let option = document.createElement("option");
                option.value = staff.id;
                option.textContent = staff.name;
                staffSelect.appendChild(option);
            });

            // Update subject dropdown
            const subjectSelect = document.getElementById("subject_id");
            subjectSelect.innerHTML = '<option value="">-- Select Subject --</option>';

            data.subjects.forEach(subject => {
                let option = document.createElement("option");
                option.value = subject.id;
                option.textContent =
                    subject.subject_name + " (Sem " + subject.semester + ")";
                subjectSelect.appendChild(option);
            });

        });
    }


    function validateForm() {
    let semester = document.getElementById("semester").value.trim();
    let department = document.getElementById("department").value.trim();

    if (semester === "" && department === "") {
        alert("Please fill at least Semester or Department");
        return false; // stop form submit
    }
    return true; // allow submit
}