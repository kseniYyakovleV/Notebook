let create_task_button = document.getElementById("create_task_button");



create_task_button.addEventListener("click", e=>{
    e.preventDefault();
    if (!is_title_valid()) { title_error.hidden = false; }
    else if (!is_deadlines_valid()) { interval_error.hidden = false; }
    else if (!is_datetime_format_valid()) { date_format_error.hidden = false; }
    else if (!is_period_types_valid()) { type_error.hidden = false; }
    else if (!is_period_values_valid()) { period_error.hidden = false; }
    else {
        form = document.getElementById("forma");
        form.submit();
    }
     
})
