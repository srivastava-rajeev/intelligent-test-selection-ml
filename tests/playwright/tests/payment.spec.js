const { test, expect } = require('@playwright/test');
const { authorizePayment } = require('../../../src/services/payment');

test('payment: authorize success', async () => {
  const result = authorizePayment(120.5, 'card');
  expect(result.ok).toBeTruthy();
  expect(result.authCode).toContain('AUTH-');
});

test('payment: invalid amount rejected', async () => {
  const result = authorizePayment(0, 'card');
  expect(result.ok).toBeFalsy();
  expect(result.reason).toBe('invalid-amount');
});
