const { test, expect } = require('@playwright/test');
const { reserveStock } = require('../../../src/services/inventory');

test('inventory: reserve stock success', async () => {
  const result = reserveStock('SKU-1', 2, 10);
  expect(result.ok).toBeTruthy();
  expect(result.remaining).toBe(8);
});

test('inventory: reserve stock fails on low inventory', async () => {
  const result = reserveStock('SKU-1', 5, 3);
  expect(result.ok).toBeFalsy();
  expect(result.reason).toBe('insufficient-stock');
});
