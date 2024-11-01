let inputs = document.getElementsByTagName("input");
let select = document.getElementsByTagName("select")[0];
let textarea = document.getElementsByTagName("textarea")[0];
let change_button = document.getElementById("change_button");
let delete_button = document.getElementById("delete_button");
let save_changes_button = document.getElementById("save_changes_button");
let cansel_button = document.getElementById("cansel_button");
let complete_button = document.getElementById("complete_button");
let form = document.getElementById("forma");



change_button.addEventListener("click", e=>{
    complete_button.hidden = true;
    change_button.hidden = true;
    delete_button.hidden = true;
    save_changes_button.hidden = false;
    cansel_button.hidden = false;

    for (let index = 0; index < inputs.length; index++) {
        inputs[index].disabled = false;
    }
    select.disabled = false;
    textarea.disabled = false;
})


cansel_button.addEventListener("click", e=>{
    complete_button.hidden = false;
    change_button.hidden = false;
    delete_button.hidden = false;
    save_changes_button.hidden = true;
    cansel_button.hidden = true;

    for (let index = 0; index < inputs.length; index++) {
        inputs[index].disabled = true;
    }

    location.reload()
})


save_changes_button.addEventListener("click", e=>{
    if (!is_title_valid()) { title_error.hidden = false; }
    else if (!is_deadlines_valid()) { interval_error.hidden = false; }
    else if (!is_datetime_format_valid()) { date_format_error.hidden = false; }
    else if (!is_period_types_valid()) { type_error.hidden = false; }
    else if (!is_period_values_valid()) { period_error.hidden = false; }
    else {
        if (window.confirm("Принять изменения?")) {
            form.action += "change/";
            form.submit();
        }
    }
})


delete_button.addEventListener("click", e=>{
    let url = form.action + "delete/";
    if (window.confirm("Вы уверены, что хотите удалить задачу? Действие необратимо.")) {
        window.location.replace(url);
    }
})



complete_button.addEventListener("click", e=>{
    console.log("fds")
    let url = form.action + "complete/";
    window.location.replace(url);
})


