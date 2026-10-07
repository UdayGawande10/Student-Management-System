const form = document.getElementById("studentForm");
const studentId = document.getElementById("studentId");
const nameInput = document.getElementById("name");
const rollNoInput = document.getElementById("rollNo");
const classInput = document.getElementById("className");
const marksInput = document.getElementById("marks");
const contactInput = document.getElementById("contact");
const table = document.getElementById("studentTable");
const emptyState = document.getElementById("emptyState");
const searchInput = document.getElementById("search");
const totalCount = document.getElementById("totalCount");
const avgMarks = document.getElementById("avgMarks");
const topMarks = document.getElementById("topMarks");
const formTitle = document.getElementById("formTitle");
const saveBtn = document.getElementById("saveBtn");
const cancelBtn = document.getElementById("cancelBtn");
const recordInfo = document.getElementById("recordInfo");
const toast = document.getElementById("toast");

let debounceTimer;

function showToast(message) {
    toast.textContent = message;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 2500);
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

async function loadStudents(query = "") {
    const response = await fetch(`/api/students?q=${encodeURIComponent(query)}`);
    const students = await response.json();

    table.innerHTML = "";
    emptyState.classList.toggle("hidden", students.length !== 0);
    recordInfo.textContent = `${students.length} record${students.length === 1 ? "" : "s"} shown`;

    students.forEach(student => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${escapeHtml(student.name)}</td>
            <td>${escapeHtml(student.roll_no)}</td>
            <td>${escapeHtml(student.class_name)}</td>
            <td>${Number(student.marks).toFixed(2)}</td>
            <td>${escapeHtml(student.contact)}</td>
            <td>
                <div class="actions">
                    <button class="edit-btn" onclick='startEdit(${JSON.stringify(student)})'>Edit</button>
                    <button class="delete-btn" onclick="deleteStudent(${student.id})">Delete</button>
                </div>
            </td>`;
        table.appendChild(row);
    });

    updateStats(students);
}

function updateStats(students) {
    totalCount.textContent = students.length;
    if (!students.length) {
        avgMarks.textContent = "0";
        topMarks.textContent = "0";
        return;
    }
    const marks = students.map(s => Number(s.marks));
    avgMarks.textContent = (marks.reduce((a, b) => a + b, 0) / marks.length).toFixed(1);
    topMarks.textContent = Math.max(...marks).toFixed(1);
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
        name: nameInput.value.trim(),
        roll_no: rollNoInput.value.trim(),
        class_name: classInput.value.trim(),
        marks: marksInput.value,
        contact: contactInput.value.trim()
    };

    const id = studentId.value;
    const method = id ? "PUT" : "POST";
    const url = id ? `/api/students/${id}` : "/api/students";

    const response = await fetch(url, {
        method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
        showToast(data.error || "Unable to save record.");
        return;
    }

    showToast(id ? "Student updated successfully." : "Student added successfully.");
    resetForm();
    loadStudents(searchInput.value.trim());
});

function startEdit(student) {
    studentId.value = student.id;
    nameInput.value = student.name;
    rollNoInput.value = student.roll_no;
    classInput.value = student.class_name;
    marksInput.value = student.marks;
    contactInput.value = student.contact;
    formTitle.textContent = "Update Student";
    saveBtn.textContent = "Update Student";
    cancelBtn.classList.remove("hidden");
    window.scrollTo({top: 0, behavior: "smooth"});
}

cancelBtn.addEventListener("click", resetForm);

function resetForm() {
    form.reset();
    studentId.value = "";
    formTitle.textContent = "Add Student";
    saveBtn.textContent = "Add Student";
    cancelBtn.classList.add("hidden");
}

async function deleteStudent(id) {
    if (!confirm("Delete this student record?")) return;

    const response = await fetch(`/api/students/${id}`, {method: "DELETE"});
    const data = await response.json();

    if (!response.ok) {
        showToast(data.error || "Unable to delete record.");
        return;
    }

    showToast("Student deleted successfully.");
    loadStudents(searchInput.value.trim());
}

searchInput.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => loadStudents(searchInput.value.trim()), 250);
});

loadStudents();
