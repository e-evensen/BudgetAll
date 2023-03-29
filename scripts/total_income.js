function calculateTotalIncome() {
  var balance = document.getElementById("balance").value;
  var income = document.getElementById("income").value;
  var weeks = document.getElementById("weeks").value;
  var totalIncome;
  
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
  totalIncome = balance + (income * weeks * 2);
  alert("Total Income for " + weeks + " weeks: $" + totalIncome.toFixed(2));
}
