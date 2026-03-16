let student_list = [];
let staff_list = [];

function initializeFunction() {
    routeCheckFunc()
    getMorningStatus()
    admin_user_check()
    get_student_staff()
}

function admin_user_check() {
    const role = $('body').attr('role');
    role == "admin" ? $('.admin_user').removeClass('d-none') : $('.admin_user').addClass('d-none');
}

function getMorningStatus() {
    const hour = new Date().getHours();
    let greeting;
    if (hour < 12) {
        $('.current_Greeting').addClass('d-none')
        $('.morning').removeClass('d-none')
        $('#greeting_data').text('Good Morning');
        $('.username_dashboard_description').text('Welcome 👋 Are you feeling awesome this morning? Great 💪');

    } else if (hour < 18) {
        $('.current_Greeting').addClass('d-none')
        $('.evening').removeClass('d-none')
        $('#greeting_data').text('Good Evening');
        $('.username_dashboard_description').text('Welcome 👋 Are you having a wonderful evening? Keep shining ✨');

    } else {
        $('.current_Greeting').addClass('d-none')
        $('.night').removeClass('d-none')
        $('#greeting_data').text('Good Night');
        $('.username_dashboard_description').text('Welcome 👋 Had a productive day? Time to relax and recharge 😌💤');

    }

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
        headers: { "Content-Type": "application/json" },
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
        headers: { "Content-Type": "application/json" },
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

    const department = document.getElementById("department").value;
    const semester = document.getElementById("semester").value;
    const staff_id = document.getElementById("staff_id").value;
    const subject_id = document.getElementById("subject_id").value;

    fetch("/filter-data", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
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
        return false;
    }
    return true;
}

function current_dashboard(data, cl) {
    $('.dashboard').addClass('d-none');
    $('.dashboard_menu').removeClass('dashboard_menu_active');
    $(`.${data}`).removeClass('d-none');
    $(`.${cl}`).addClass('dashboard_menu_active');
    if (data == 'staff_planner' && staff_list.length) {
        staff_list.forEach((ele) => {
            $('.staff_details_parent').append(`<div class="staff_card m-3">
                                <div class="profileIcon_parent">
                                    <div class="profileIconBlock">
                                        <div class="profileIcon">
                                            <img src="../static/${ele.image}" class="h-100 staff_card_image w-100">
                                        </div>
                                    </div>
                                    <div class="staff_card_name text-center ">${ele.name}</div>
                                    <div class="staff_card_designation text-center ">${ele.designation}</div>
                                </div>
                                <div class="details pb-3 pt-4 px-3">
                                    <h4>details</h4>
                                    <div class="divider"></div>
                                    <div>
                                        <div class="my-1">${ele.email}</div>
                                        <div class="my-1">${ele.department}</div>
                                    </div>
                                </div>
                            </div>`)
        })
    } else if (data == 'student_planner' && student_list.length) {
        student_list.forEach((ele) => {
            $('.student_details_parent').append(`<div class="staff_card m-3">
                                <div class="profileIcon_parent">
                                    <div class="profileIconBlock">
                                        <div class="profileIcon">
                                            <img src="../static/${ele.image}" class="h-100 staff_card_image w-100">
                                        </div>
                                    </div>
                                    <div class="staff_card_name text-center ">${ele.name}</div>
                                    <div class="staff_card_designation text-center ">${ele.designation}</div>
                                </div>
                                <div class="details pb-3 pt-4 px-3">
                                    <h4>details</h4>
                                    <div class="divider"></div>
                                    <div>
                                        <div class="my-1">${ele.email}</div>
                                        <div class="my-1">${ele.department}</div>
                                    </div>
                                </div>
                            </div>`)
        })
    }
}

function checkArrow(data, e, i) {
    if ($(`.${e}`).is('[aria-expanded="false"]')) {
        $(`#${data}`).addClass('rotate_right');
        $(`.${i}`).removeClass('expandCommon')
    } else {
        $(`#${data}`).removeClass('rotate_right');
        $(`.${i}`).addClass('expandCommon')
    }
}

function dashboard_total_func(data, item) {
    const temp_value = $(`.${data}`).val();
    const temp_item = item;
    fetch("/storeTotal", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            total: temp_value,
            value: temp_item
        })
    }).then(res => res.json()).then(data => {
        console.log(data)
    })
}

function add_subject() {
    event.preventDefault();
    const department_input = $('#department_input').val();
    const semester_input = $('#semester_input').val();
    const subject_input = $('#subject_input').val();
    const type_input = $('#type_input').val();
    const hours_input = $('#hours_input').val();
    fetch("/staff", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            department_input: department_input,
            semester_input: semester_input,
            subject_input: subject_input,
            type_input: type_input,
            hours_input: hours_input,
        })
    }).then(res => res.json()).then(data => {
        data.success ? iziToast.success({
            maxWidth: 500,
            position: 'center',
            title: 'Success',
            message: data.message,
            position: 'bottomRight',
            transitionIn: 'bounceInLeft',
        }) : iziToast.error({
            maxWidth: 500,
            position: 'center',
            title: 'Failed',
            message: data.message,
            position: 'bottomRight',
            transitionIn: 'bounceInLeft',
        });
    })
}

function save_mapping() {
    event.preventDefault();
    const semester_map = $('.semester_map').val()
    const department_map = $('.department_map').val()
    const staff_map = $('.staff_map').val()
    const subject_map = $('.subject_map').val()

    fetch("/mapping", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            semester_map: semester_map,
            department_map: department_map,
            staff_map: staff_map,
            subject_map: subject_map,
        })
    }).then(res => res.json()).then(data => {
        data.success ? iziToast.success({
            maxWidth: 500,
            position: 'center',
            title: 'Success',
            message: data.message,
            position: 'bottomRight',
            transitionIn: 'bounceInLeft',
        }) : iziToast.error({
            maxWidth: 500,
            position: 'center',
            title: 'Failed',
            message: data.message,
            position: 'bottomRight',
            transitionIn: 'bounceInLeft',
        });
        console.log(data.data)
    })
}

function get_student_staff() {
    fetch("/get_student_staff")
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                student_list = data.students
                staff_list = data.staff
            }
        })
        .catch(error => console.error("Error:", error));
}

function show_mapping() {
    fetch("/mapping", {   // <-- your backend endpoint to return mappings
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            const thead = document.querySelector(".timetable-card view_tt_thead");
            const tbody = document.querySelector(".timetable-card view_tt_tbody");
            tbody.innerHTML = ""; // clear old rows

            data.mappings.forEach(map => {
                const row = `
                    <tr>
                        <td>${map.name}</td>
                        <td>${map.subject_name}</td>
                        <td>${map.department}</td>
                        <td>${map.semester}</td>
                    </tr>
                `;
                tbody.insertAdjacentHTML("beforeend", row);
            });
        } else {
            iziToast.error({
                maxWidth: 500,
                position: 'bottomRight',
                title: 'Error',
                message: data.message || "Failed to load mappings",
                transitionIn: 'bounceInLeft',
            });
        }
    })
    .catch(err => {
        console.error("Error fetching mappings:", err);
        iziToast.error({
            maxWidth: 500,
            position: 'bottomRight',
            title: 'Error',
            message: "Something went wrong while loading mappings",
            transitionIn: 'bounceInLeft',
        });
    });
}

function view_timetable_old() {
    
    event.preventDefault();
    const semester_map = $('.view_tt_semester_map').val()
    const department_map = $('.view_tt_department_map').val()

    console.log('print here!')
    console.log('semester_map', semester_map)
    console.log('department_map', department_map)
    fetch("/student", {   // <-- your backend endpoint to return mappings
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            semester_map: Number(semester_map),
            department_map: department_map
        })
    })
    .then(res => res.json())
    .then(data => {
        debugger
        if (data.success) {
            const tbody = document.querySelector(".view_tt_tbody");
        if (!tbody) return console.error("Could not find .view_tt_tbody");

        // 1. Clear existing rows
        tbody.innerHTML = "";

        if (data.grid) {
                // 2. Loop through the days in the grid
                Object.keys(data.grid).sort().forEach(day => {
                    const tr = document.createElement("tr");
                    
                    // Add the Day Column (e.g., DAY-1)
                    let html = `<th class="day-column">${day}</th>`;
                    
                    // Add the 5 Periods
                    for (let i = 1; i <= 5; i++) {
                        const subject = data.grid[day][i] || "Library";
                        html += `<td>${subject}</td>`;
                    }
                    
                    tr.innerHTML = html;
                    tbody.appendChild(tr);
                });
            } else {
                tbody.innerHTML = "<tr><td colspan='6'>No timetable found.</td></tr>";
            }
        } else {
            iziToast.error({
                maxWidth: 500,
                position: 'bottomRight',
                title: 'Error',
                message: data.message || "Failed to load mappings",
                transitionIn: 'bounceInLeft',
            });
        }
    })
    .catch(err => {
        console.error("Error fetching mappings:", err);
        iziToast.error({
            maxWidth: 500,
            position: 'bottomRight',
            title: 'Error',
            message: "Something went wrong while loading mappings",
            transitionIn: 'bounceInLeft',
        });
    });
}

// this method works fine
function view_timetable(event) {
     // FIX: Only prevent default if an event exists (from a button click)
    if (event && typeof event.preventDefault === 'function') {
        event.preventDefault();
    }

    const sem = document.getElementById("view_tt_semester").value;
    const dept = document.getElementById("view_tt_department").value;

    if (!sem || !dept) {
        // Only alert if we aren't calling this from the generate function
        if (event) alert("Please select both Semester and Department");
        return;
    }
    
    fetch("/student", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            semester_map: Number(sem),
            department_map: dept
        })
    })
    .then(response => response.json())
    .then(data => {
        const tbody = document.querySelector(".view_tt_tbody");
        const section = document.querySelector(".timetable_planner");
        // Change this line in your dashboard.js

        // Always add this safety check
        if (!tbody) {
            console.error("DEBUG: Could not find .view_tt_tbody in the DOM!");
            return;
        }
        tbody.innerHTML = ""; // Now this won't crash
        // Show the section
        section.classList.remove("d-none");
        
        if (data.grid && Object.keys(data.grid).length > 0) {
            // Sort days to ensure DAY-1 comes before DAY-2
            const sortedDays = Object.keys(data.grid).sort();

            sortedDays.forEach(day => {
                const tr = document.createElement("tr");
                
                // Add the Day header cell
                let rowHtml = `<th class="day-column">${day}</th>`;
                
                // Add periods 1 to 5
                for (let i = 1; i <= 5; i++) {
                    const subject = data.grid[day][i.toString()] || "Library";
                    rowHtml += `<td>${subject}</td>`;
                }
                
                tr.innerHTML = rowHtml;
                tbody.appendChild(tr);
            });
        } else {
            tbody.innerHTML = "<tr><td colspan='6' class='text-center'>No Timetable Found</td></tr>";
        }
    })
    .catch(err => console.error("Error fetching timetable:", err));
}

function generate_timetable(event) {
    if (event) event.preventDefault();

    const sem_select = document.getElementById("view_tt_semester").value;
    const dept_select = document.getElementById("view_tt_department").value;

    if (!sem_select || !dept_select) {
        alert("Please select both Semester and Department");
        return;
    }

    if (!confirm("This will overwrite the existing timetable for this selection. Continue?")) return;

    const btn = event.target;
    // btn.innerText = "Generating...";
    btn.disabled = true;
    sem_select.disabled = true;  // Prevent changes during generation
    dept_select.disabled = true;

    fetch(`/generate/${sem}/${dept}`)
    .then(response => {
        if (!response.ok) throw new Error("Server error during generation");
        return response.json();
    })
    .then(response => response.json()) // This won't fail now!
    .then(data => {
        if (data.success) {
            alert(data.message);
            // view_timetable(); // Automatically refresh the table
            btn.innerText = "Generate Timetable";
        } else {
            alert("Error: " + data.message);
        }
    })
    .catch(err => {
        console.error("Fetch Error:", err);
        alert("The server sent an invalid response. Check Python return statement.");
    })
    .finally(() => {
            // 3. Reset Components (Runs for both Success AND Error)
            btn.innerText = "Generate Timetable";
            btn.disabled = false;
            sem_select.disabled = false;
            dept_select.disabled = false;
            
            // Optional: If you want to clear the dropdowns on error:
            if (!data.success) { sem_select.value = ""; dept_select.value = ""; }
        });

    // Call the specific generate route
    // fetch(`/generate/${sem}/${dept}`)
    //     .then(response => {
    //         if (response.ok) {
    //             alert("Timetable generated successfully!");
    //             // Re-use your view logic to refresh the table automatically
    //             view_timetable(); 
    //         } else {
    //             alert("Failed to generate timetable. Check if subjects are mapped.");
    //         }
    //     })
    //     .catch(err => console.error("Error:", err))
    //     .finally(() => {
    //         genBtn.innerText = "Generate Timetable";
    //         genBtn.disabled = false;
    //     });
}

