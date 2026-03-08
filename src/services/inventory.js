function reserveStock(sku, qty, available) {
  if (!sku || qty <= 0) return { ok: false, reason: 'invalid-request' };
  if (available < qty) return { ok: false, reason: 'insufficient-stock' };
  return { ok: true, remaining: available - qty };
}

module.exports = { reserveStock };
