function authorizePayment(amount, method) {
  if (amount <= 0) return { ok: false, reason: 'invalid-amount' };
  if (!method) return { ok: false, reason: 'missing-method' };
  return { ok: true, authCode: `AUTH-${Math.floor(amount * 100)}` };
}

module.exports = { authorizePayment };
