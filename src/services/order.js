function createOrder({ id, items }) {
  if (!id || !Array.isArray(items) || items.length === 0) {
    return { ok: false, reason: 'invalid-order' };
  }
  const totalItems = items.reduce((sum, item) => sum + (item.qty || 0), 0);
  return { ok: true, orderId: id, totalItems };
}

module.exports = { createOrder };
