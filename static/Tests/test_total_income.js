const calculate = require('../total_income.js');

describe("calculate", () => {
  test("returns 'badBal' if balance is not a positive number", () => {
    expect(calculate(-1000, 1000, 4)).toBe("badBal");
    expect(calculate("", 1000, 4)).toBe("badBal");
    expect(calculate(NaN, 1000, 4)).toBe("badBal");
  });

  test("returns 'badInc' if income is not a positive number", () => {
    expect(calculate(5000, -1000, 4)).toBe("badInc");
    expect(calculate(5000, "", 4)).toBe("badInc");
    expect(calculate(5000, NaN, 4)).toBe("badInc");
  });

  test("returns 'badWks' if weeks is not a positive number", () => {
    expect(calculate(5000, 1000, -4)).toBe("badWks");
    expect(calculate(5000, 1000, "")).toBe("badWks");
    expect(calculate(5000, 1000, NaN)).toBe("badWks");
    expect(calculate(5000, 1000, 0)).toBe("badWks");
  });

  test("calculates the total balance after 4 weeks", () => {
    expect(calculate(5000, 1000, 4)).toBe(7000);
  });
});