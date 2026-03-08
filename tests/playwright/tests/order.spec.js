const { test, expect } = require('@playwright/test');
const { createOrder } = require('../../../src/services/order');

test('order: create order success', async () => {
  const result = createOrder({
    id: 'ORD-100',
    items: [{ sku: 'SKU-1', qty: 2 }, { sku: 'SKU-2', qty: 1 }]
  });

  expect(result.ok).toBeTruthy();
  expect(result.totalItems).toBe(3);
});

test('order: invalid order is rejected', async () => {
  const result = createOrder({ id: '', items: [] });
  expect(result.ok).toBeFalsy();
  expect(result.reason).toBe('invalid-order');
});
