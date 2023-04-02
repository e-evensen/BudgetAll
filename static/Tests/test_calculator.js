const calculate = require('../calculator.js');

test('calculates the number of days required to save up given cost and income', () => {
  expect(calculate(5000, 100)).toBe(50);
});

test('returns "badCost" if cost is not a positive number greater than one', () => {
  expect(calculate(-10, 200)).toBe('badCost');
  expect(calculate(0, 200)).toBe('badCost');
  expect(calculate('', 200)).toBe('badCost');
});

test('returns "badIncome" if income is not a positive number greater than one', () => {
  expect(calculate(5000, -100)).toBe('badIncome');
  expect(calculate(5000, 0)).toBe('badIncome');
  expect(calculate(5000, '')).toBe('badIncome');
});