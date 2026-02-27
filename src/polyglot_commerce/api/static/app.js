const state = {
  customers: [],
  items: [],
  orders: [],
  metrics: null,
  integration: null,
  cart: new Map(),
  quote: null,
};

const els = {
  health: document.getElementById("health"),
  customerSelect: document.getElementById("customer-select"),
  quoteBtn: document.getElementById("quote-btn"),
  orderBtn: document.getElementById("order-btn"),
  resetBtn: document.getElementById("reset-btn"),
  message: document.getElementById("message"),
  integrationList: document.getElementById("integration-list"),
  catalogGrid: document.getElementById("catalog-grid"),
  cartEmpty: document.getElementById("cart-empty"),
  cartList: document.getElementById("cart-list"),
  quoteBox: document.getElementById("quote-box"),
  quoteLines: document.getElementById("quote-lines"),
  quoteTotals: document.getElementById("quote-totals"),
  metricCards: document.getElementById("metric-cards"),
  recentOrders: document.getElementById("recent-orders"),
  inventoryAlerts: document.getElementById("inventory-alerts"),
};

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.detail || payload.error || `Request failed (${response.status})`);
  }

  return payload;
}

function money(value) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "EUR" }).format(Number(value || 0));
}

function setMessage(text, isError = false) {
  els.message.textContent = text;
  els.message.classList.toggle("error", isError);
}

function buildPayload() {
  return {
    customer_id: Number(els.customerSelect.value),
    lines: Array.from(state.cart.entries()).map(([itemId, quantity]) => ({ item_id: itemId, quantity })),
  };
}

function renderCustomers() {
  if (!state.customers.length) {
    els.customerSelect.innerHTML = "<option value=''>No customers</option>";
    return;
  }

  els.customerSelect.innerHTML = state.customers
    .map((customer) => `<option value="${customer.id}">${customer.name} · ${customer.district} · ${customer.loyaltyYears}y</option>`)
    .join("");
}

function renderIntegration() {
  const data = state.integration;
  if (!data) {
    els.integrationList.innerHTML = "<li>No integration data.</li>";
    return;
  }

  const entries = [
    ["Java Legacy", data.javaLegacy],
    ["OCaml Legacy", data.ocamlLegacy],
    ["Prolog Rules", data.prologRules],
  ];

  els.integrationList.innerHTML = entries
    .map(([label, status]) => `<li>${label}: <strong>${status ? "available" : "missing"}</strong></li>`)
    .join("");
}

function renderCatalog() {
  if (!state.items.length) {
    els.catalogGrid.innerHTML = "<div class='empty'>No catalog items.</div>";
    return;
  }

  els.catalogGrid.innerHTML = state.items
    .map((item) => {
      const lowClass = item.lowStock ? "stock-pill low" : "stock-pill";
      const disabled = item.stock <= 0 ? "disabled" : "";
      return `
        <article class="product-card">
          <h4>${item.name}</h4>
          <div class="meta">#${item.id} · ${item.category}</div>
          <div class="row">
            <strong>${money(item.price)}</strong>
            <span class="${lowClass}">Stock ${item.stock}</span>
          </div>
          <div class="meta">Category discount ${(item.categoryDiscount * 100).toFixed(0)}%</div>
          <button data-add="${item.id}" ${disabled}>Add to cart</button>
        </article>
      `;
    })
    .join("");
}

function renderCart() {
  const entries = Array.from(state.cart.entries());
  if (!entries.length) {
    els.cartEmpty.classList.remove("hidden");
    els.cartList.innerHTML = "";
    return;
  }

  els.cartEmpty.classList.add("hidden");

  els.cartList.innerHTML = entries
    .map(([itemId, quantity]) => {
      const product = state.items.find((item) => item.id === itemId);
      if (!product) return "";

      return `
        <div class="cart-item">
          <div>
            <strong>${product.name}</strong>
            <div class="meta">${money(product.price)} each</div>
          </div>
          <div class="cart-controls">
            <button class="qty" data-dec="${itemId}">-</button>
            <strong>${quantity}</strong>
            <button class="qty" data-inc="${itemId}">+</button>
            <button class="remove" data-remove="${itemId}">Remove</button>
          </div>
        </div>
      `;
    })
    .join("");
}

function renderQuote() {
  const quote = state.quote;
  if (!quote) {
    els.quoteBox.classList.add("hidden");
    return;
  }

  els.quoteBox.classList.remove("hidden");

  els.quoteLines.innerHTML = quote.lines
    .map((line) => `<div class="qrow"><span>${line.itemName} x${line.quantity}</span><span>${money(line.lineSubtotal)}</span></div>`)
    .join("");

  els.quoteTotals.innerHTML = `
    <div class="qrow"><span>Subtotal</span><span>${money(quote.subtotal)}</span></div>
    <div class="qrow"><span>Category Discount</span><span>- ${money(quote.categoryDiscount)}</span></div>
    <div class="qrow"><span>Loyalty Discount</span><span>- ${money(quote.loyaltyDiscount)}</span></div>
    <div class="qrow"><span>Shipping</span><span>${money(quote.shippingCost)}</span></div>
    <div class="qrow"><strong>Total</strong><strong>${money(quote.total)}</strong></div>
  `;
}

function renderMetrics() {
  if (!state.metrics) {
    els.metricCards.innerHTML = "";
    return;
  }

  const cards = [
    ["Revenue", money(state.metrics.revenue)],
    ["Orders", state.metrics.orders],
    ["Quotes", state.metrics.quotes],
    ["Avg Order", money(state.metrics.avgOrderValue)],
    ["Inventory", state.metrics.inventoryCount],
    ["Errors", state.metrics.errors],
  ];

  els.metricCards.innerHTML = cards
    .map(([label, value]) => `<article class="metric"><span>${label}</span><strong>${value}</strong></article>`)
    .join("");
}

function renderOrders() {
  if (!state.orders.length) {
    els.recentOrders.innerHTML = "<li>No orders created yet.</li>";
    return;
  }

  els.recentOrders.innerHTML = state.orders
    .slice(0, 5)
    .map((order) => `<li><strong>${order.orderId}</strong><br>${order.customer.name} · ${money(order.quote.total)}</li>`)
    .join("");
}

function renderAlerts() {
  const low = state.items.filter((item) => item.lowStock || item.stock <= 5);
  if (!low.length) {
    els.inventoryAlerts.innerHTML = "<li>No low stock alerts.</li>";
    return;
  }

  els.inventoryAlerts.innerHTML = low
    .map((item) => `<li>${item.name}: <strong>${item.stock}</strong> left</li>`)
    .join("");
}

function refreshUI() {
  renderCustomers();
  renderIntegration();
  renderCatalog();
  renderCart();
  renderQuote();
  renderMetrics();
  renderOrders();
  renderAlerts();
}

async function loadBase() {
  const [health, customers, items, orders, metrics, integration] = await Promise.all([
    api("/health"),
    api("/api/customers"),
    api("/api/items"),
    api("/api/orders"),
    api("/api/metrics"),
    api("/api/integration"),
  ]);

  els.health.textContent = `${health.service} · ${health.status}`;
  state.customers = customers.customers || [];
  state.items = items.items || [];
  state.orders = orders.orders || [];
  state.metrics = metrics;
  state.integration = integration;
}

async function generateQuote() {
  if (!state.cart.size) {
    throw new Error("Cart is empty.");
  }

  const response = await api("/api/quote", {
    method: "POST",
    body: JSON.stringify(buildPayload()),
  });

  state.quote = response.quote;
  state.items = response.inventory || state.items;
}

async function createOrder() {
  if (!state.cart.size) {
    throw new Error("Cart is empty.");
  }

  const response = await api("/api/orders", {
    method: "POST",
    body: JSON.stringify(buildPayload()),
  });

  state.quote = response.order.quote;
  state.items = response.inventory || state.items;
  state.cart.clear();

  const orders = await api("/api/orders");
  const metrics = await api("/api/metrics");
  state.orders = orders.orders || [];
  state.metrics = metrics;
}

async function resetSession() {
  await api("/api/reset", { method: "POST" });
  state.cart.clear();
  state.quote = null;

  const [items, orders, metrics] = await Promise.all([api("/api/items"), api("/api/orders"), api("/api/metrics")]);
  state.items = items.items || [];
  state.orders = orders.orders || [];
  state.metrics = metrics;
}

function wireEvents() {
  els.catalogGrid.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-add]");
    if (!button) return;

    const itemId = Number(button.dataset.add);
    const current = state.cart.get(itemId) || 0;
    const product = state.items.find((item) => item.id === itemId);
    if (!product || current >= product.stock) {
      setMessage("Cannot exceed available stock.", true);
      return;
    }
    state.cart.set(itemId, current + 1);
    renderCart();
  });

  els.cartList.addEventListener("click", (event) => {
    const inc = event.target.closest("button[data-inc]");
    if (inc) {
      const itemId = Number(inc.dataset.inc);
      const current = state.cart.get(itemId) || 0;
      const product = state.items.find((item) => item.id === itemId);
      if (!product || current >= product.stock) {
        setMessage("Cannot exceed available stock.", true);
        return;
      }
      state.cart.set(itemId, current + 1);
      renderCart();
      return;
    }

    const dec = event.target.closest("button[data-dec]");
    if (dec) {
      const itemId = Number(dec.dataset.dec);
      const current = state.cart.get(itemId) || 0;
      if (current <= 1) {
        state.cart.delete(itemId);
      } else {
        state.cart.set(itemId, current - 1);
      }
      renderCart();
      return;
    }

    const remove = event.target.closest("button[data-remove]");
    if (remove) {
      state.cart.delete(Number(remove.dataset.remove));
      renderCart();
    }
  });

  els.quoteBtn.addEventListener("click", async () => {
    try {
      await generateQuote();
      refreshUI();
      setMessage("Quote generated.");
    } catch (error) {
      setMessage(error.message, true);
    }
  });

  els.orderBtn.addEventListener("click", async () => {
    try {
      await createOrder();
      refreshUI();
      setMessage("Order created successfully.");
    } catch (error) {
      setMessage(error.message, true);
    }
  });

  els.resetBtn.addEventListener("click", async () => {
    try {
      await resetSession();
      refreshUI();
      setMessage("Session reset completed.");
    } catch (error) {
      setMessage(error.message, true);
    }
  });
}

async function bootstrap() {
  wireEvents();
  try {
    await loadBase();
    refreshUI();
    setMessage("Dashboard loaded.");
  } catch (error) {
    setMessage(error.message, true);
  }
}

bootstrap();
