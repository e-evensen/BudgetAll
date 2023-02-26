function calculate(cost, income) {

    if (cost == "" || isNaN(cost) || cost < 1) {
        //alert("Please enter a valid, positive number greater than one for your cost");
        return "badCost";
    }
    else if (income == "" || isNaN(income) || income < 1) {
        //alert("Please enter a valid, positive number greater than one for your income");
        return "badIncome";
    }
    else {
        return Math.ceil(cost / income);
    }
}

function displayResult() {
    const cost = document.forms["calcForm"]["cost"].value;
    const income = document.forms["calcForm"]["income"].value;
    const resultElement = document.getElementById("result");
    
    const result = calculate(cost, income);

    if (result === "badCost") {
        resultElement.innerHTML = "Please enter a valid, positive number greater than one for your cost";
    }
    else if (result === "badIncome") {
        resultElement.innerHTML = "Please enter a valid, positive number greater than one for your income";
    }
    else {
        let frmtCost = Number(cost).toLocaleString("en-US", {style:"currency", currency:"USD"})
        resultElement.innerHTML = "It would take you roughly " + result + " days to save up " + frmtCost + ".";
    }
}