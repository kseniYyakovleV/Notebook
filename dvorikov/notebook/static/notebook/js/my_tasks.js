let clear_icon = document.getElementById("clear_icon");
let find_input = document.getElementById("find_input");
let filter_button = document.getElementById("filter_button");

let ahead_tasks_checkbox = document.getElementById("ahead_tasks_checkbox");
let current_tasks_checkbox = document.getElementById("current_tasks_checkbox");
let failed_tasks_checkbox = document.getElementById("failed_tasks_checkbox");
let completed_tasks_checkbox = document.getElementById("completed_tasks_checkbox");

let tasks = document.getElementById("tasks");
let menu = document.getElementById("menu");
let tasks_list = tasks.children;
let is_filter_hidden = true;

filter_button.addEventListener("click", e=>{
    console.log("funny");
    if (is_filter_hidden) {
        menu.style.display = "flex";
        find_input.focus();
    } else {
        menu.style.display = "none";
        console.log(2)
    }
    is_filter_hidden = !is_filter_hidden;
})

function find_and_filter() {
    let hidden_tasks = [];
    let visible_tasks = [];
    let tasks_list = tasks.children;
    let find_text = find_input.value.toLowerCase();

    if (!ahead_tasks_checkbox.checked) {
        hidden_tasks.push("ahead_task");
    } else {
        visible_tasks.push("ahead_task");
    }
    if (!current_tasks_checkbox.checked) {
        hidden_tasks.push("current_task");
    } else {
        visible_tasks.push("current_task");
    }
    if (!failed_tasks_checkbox.checked) {
        hidden_tasks.push("failed_task");
    } else {
        visible_tasks.push("failed_task");
    }
    if (!completed_tasks_checkbox.checked) {
        hidden_tasks.push("completed_task");
    } else {
        visible_tasks.push("completed_task");
    }


    for (let i = 0; i < tasks_list.length; i++) {
        for (let j = 0; j < hidden_tasks.length; j++) {
            if (tasks_list[i].className === hidden_tasks[j]) {
                tasks_list[i].style.display = 'none';
                 
            }
        }
        for (let j = 0; j < visible_tasks.length; j++) {
            if ((tasks_list[i].className === visible_tasks[j]) & tasks_list[i].children[0].children[0].textContent.toLowerCase().includes(find_text)) {
                tasks_list[i].style.display = 'flex';
            }
        }

        if (!tasks_list[i].children[0].children[0].textContent.toLowerCase().includes(find_text)) {
            tasks_list[i].style.display = 'none';
        }
    }
}


ahead_tasks_checkbox.addEventListener("change", e=>{
    find_and_filter();
})

current_tasks_checkbox.addEventListener("change", e=>{
    find_and_filter();
})

failed_tasks_checkbox.addEventListener("change", e=>{
    find_and_filter();
})

completed_tasks_checkbox.addEventListener("change", e=>{
    find_and_filter();
})

find_input.addEventListener("input", e=>{
    find_and_filter();
    if (e.target.value != "") {
        clear_icon.style.display = "block";
    } else {
        clear_icon.style.display = "none";
    }
})

