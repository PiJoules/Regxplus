function failedValidation(){
    $(".check").removeClass("btn-primary").addClass("btn-danger").text("Incorrect. Try again.");
}

function successfulValidation(){
    $(".check").removeClass("btn-primary btn-danger").addClass("btn-success").text("Valid!");
}