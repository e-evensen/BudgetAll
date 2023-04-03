function calculate(balance, income, weeks) {
  if (balance < 0 || isNaN(balance) || balance === "") {
    return "badBal";
  } else if (income < 0 || isNaN(income) || income === "") {
    return "badInc";
  } else if (weeks <= 0 || isNaN(weeks) || weeks === "") {
    return "badWks";
  } else {
    return balance + ((income / 2) * weeks);
  }
}

module.exports = calculate;

function displayResult() {
  const balance = parseFloat(document.getElementById("balance").value);
  const income = parseFloat(document.getElementById("income").value);
  const weeks = parseFloat(document.getElementById("weeks").value);
  const resultElement = document.getElementById("result");

  const result = calculate(balance, income, weeks);

  if (result === "badBal") {
    resultElement.innerHTML =
      "Please enter a valid, non-negative number for your balance.";
  } else if (result === "badInc") {
    resultElement.innerHTML =
      "Please enter a valid, non-negative number for your income.";
  } else if (result === "badWks") {
    resultElement.innerHTML =
      "Please enter a valid, positive number for the number of weeks.";
  } else {
    let frmtResult = result.toLocaleString("en-US", {
      style: "currency",
      currency: "USD"
    });
    resultElement.innerHTML =
      "Total balance after " + weeks + " weeks: " + frmtResult;
  }
}