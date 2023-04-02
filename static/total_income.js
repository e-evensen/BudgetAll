function calculateTotalIncome() {
  let balance = parseInt(document.getElementById("balance").value);
  let income = parseInt(document.getElementById("income").value);
  let weeks = parseInt(document.getElementById("weeks").value);
  let totalIncome;

  // Validate input fields
  if (balance < 0 || isNaN(balance)) {
    document.getElementById("balanceError").style.display = "block";
    return;
  } else {
    document.getElementById("balanceError").style.display = "none";
  }

  if (income < 0 || isNaN(income)) {
    document.getElementById("incomeError").style.display = "block";
    return;
  } else {
    document.getElementById("incomeError").style.display = "none";
  }

  if (weeks < 1 || isNaN(weeks)) {
    document.getElementById("weeksError").style.display = "block";
    return;
  } else {
    document.getElementById("weeksError").style.display = "none";
  }

  // Calculate total income
  const resultElement = document.getElementById("result");
  totalIncome = balance + (income * weeks * 2);
  resultElement.innerHTML = "Total Income for " + weeks + " weeks: $" + totalIncome.toFixed(2);
  //alert("Total Income for " + weeks + " weeks: $" + totalIncome.toFixed(2));
}