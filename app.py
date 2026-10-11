import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Blinkit Store Dashboard",
    page_icon="🛒",
    layout="wide"
)

# ---------------- COLOURFUL DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fffbea, #effaf3, #f1edff);
}
.block-container {
    padding-top: 1.5rem;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fff0a6, #fffdf3, #e5f7e9);
}
.brand {
    background: linear-gradient(100deg, #ffe135, #ffbd35);
    padding: 22px;
    border-radius: 18px;
    color: #174d27;
    font-size: 34px;
    font-weight: 900;
}
.hero {
    background: linear-gradient(110deg, #fff06b, #ffc928);
    padding: 22px;
    border-radius: 18px;
    color: #174d27;
}
div[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #e4eee5;
    box-shadow: 0 4px 14px #0000000d;
}
div.stButton > button {
    background: linear-gradient(90deg, #ffe135, #ffc928);
    color: #174d27;
    border: none;
    border-radius: 10px;
    font-weight: bold;
}
div.stButton > button:hover {
    background: #168b45;
    color: white;
}
.product-card {
    background: white;
    border-radius: 15px;
    padding: 15px;
    border: 1px solid #e5eee7;
}
h1, h2, h3 {
    color: #174d27;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown(
        "<h1 style='text-align:center;color:#174d27'>blink"
        "<span style='color:#16a34a'>it</span></h1>",
        unsafe_allow_html=True
    )
    st.caption("India's Last Minute App")
    page = st.radio(
        "NAVIGATION",
        ["Dashboard", "Store", "Inventory", "Analytics"]
    )
    st.divider()
    st.markdown("### 🚚 Fast & Fresh")
    st.write("🥦 Fresh groceries")
    st.write("🛵 Quick delivery")
    st.write("🌱 Better food, better future")

# ---------------- PRODUCT DATA ----------------
if "products" not in st.session_state:
    st.session_state.products = pd.DataFrame([
        {"Product": "Fresh Apples", "Category": "Fruits",
         "Price": 120, "Stock": 25, "Emoji": "🍎"},
        {"Product": "Bananas", "Category": "Fruits",
         "Price": 45, "Stock": 40, "Emoji": "🍌"},
        {"Product": "Tomatoes", "Category": "Vegetables",
         "Price": 35, "Stock": 30, "Emoji": "🍅"},
        {"Product": "Potatoes", "Category": "Vegetables",
         "Price": 30, "Stock": 40, "Emoji": "🥔"},
        {"Product": "Amul Milk", "Category": "Dairy",
         "Price": 30, "Stock": 50, "Emoji": "🥛"},
        {"Product": "Cheese", "Category": "Dairy",
         "Price": 95, "Stock": 14, "Emoji": "🧀"},
        {"Product": "Bread", "Category": "Bakery",
         "Price": 40, "Stock": 5, "Emoji": "🍞"},
        {"Product": "Potato Chips", "Category": "Snacks",
         "Price": 20, "Stock": 35, "Emoji": "🍟"},
        {"Product": "Chocolate", "Category": "Snacks",
         "Price": 50, "Stock": 20, "Emoji": "🍫"},
        {"Product": "Orange Juice", "Category": "Beverages",
         "Price": 90, "Stock": 15, "Emoji": "🧃"},
        {"Product": "Dish Soap", "Category": "Household",
         "Price": 75, "Stock": 18, "Emoji": "🧴"},
        {"Product": "Eggs", "Category": "Dairy",
         "Price": 70, "Stock": 12, "Emoji": "🥚"}
    ])

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "orders" not in st.session_state:
    st.session_state.orders = []

products = st.session_state.products

# ---------------- HEADER ----------------
st.markdown(
    "<div class='brand'>🛒 blinkit Store Dashboard</div>",
    unsafe_allow_html=True
)
st.write("Manage products, shopping, stock and store analytics.")

# ---------------- SEARCH ----------------
c1, c2 = st.columns([3, 1])

with c1:
    search = st.text_input(
        "🔎 Search products",
        placeholder="Search apples, milk, bread..."
    )

with c2:
    categories = ["All"] + sorted(
        products["Category"].unique().tolist()
    )
    category = st.selectbox("🗂️ Category", categories)

filtered = products.copy()

if search:
    filtered = filtered[
        filtered["Product"].str.contains(
            search, case=False, na=False
        )
    ]

if category != "All":
    filtered = filtered[
        filtered["Category"] == category
    ]

# ---------------- METRICS ----------------
total_products = len(products)
total_stock = int(products["Stock"].sum())
low_stock = int((products["Stock"] < 10).sum())
cart_count = sum(st.session_state.cart.values())
revenue = sum(order["total"] for order in st.session_state.orders)

m1, m2, m3, m4 = st.columns(4)
m1.metric("📦 Total Products", total_products)
m2.metric("💰 Demo Revenue", f"₹{revenue:,}")
m3.metric("🏬 Stock Units", total_stock)
m4.metric("⚠️ Low Stock", low_stock)

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.markdown("""
    <div class="hero">
        <h2>🥑 Fresh groceries, happy homes!</h2>
        <p>Shop daily essentials and manage your store in one place.</p>
        <h4>✨ Fresh picks • Great value • Easy shopping</h4>
    </div>
    """, unsafe_allow_html=True)

# ---------------- STORE ----------------
if page in ["Dashboard", "Store"]:

    st.subheader("🛍️ Shop by Category")

    category_emojis = {
        "Fruits": "🍎",
        "Vegetables": "🥦",
        "Dairy": "🥛",
        "Bakery": "🍞",
        "Snacks": "🍿",
        "Beverages": "🧃",
        "Household": "🧴"
    }

    cat_cols = st.columns(6)

    for i, cat in enumerate(
        products["Category"].unique()
    ):
        with cat_cols[i % 6]:
            st.markdown(
                f"<div class='product-card' "
                f"style='text-align:center'>"
                f"<h2>{category_emojis.get(cat, '🛍️')}</h2>"
                f"<b>{cat}</b></div>",
                unsafe_allow_html=True
            )

    st.subheader("✨ Featured Products")

    if filtered.empty:
        st.warning("No products found.")

    else:
        cols = st.columns(4)

        for i, (_, product) in enumerate(
            filtered.iterrows()
        ):
            with cols[i % 4]:

                with st.container(border=True):
                    st.markdown(
                        f"<div style='text-align:center;"
                        f"background:#f0fff3;border-radius:12px;"
                        f"padding:10px;font-size:45px'>"
                        f"{product['Emoji']}</div>",
                        unsafe_allow_html=True
                    )

                    st.markdown(f"### {product['Product']}")
                    st.caption(product["Category"])
                    st.markdown(
                        f"**₹{product['Price']}**"
                    )
                    st.write(f"📦 Stock: {product['Stock']}")

                    stock = int(product["Stock"])

                    if stock > 0:
                        qty = st.number_input(
                            "Quantity",
                            min_value=1,
                            max_value=stock,
                            value=1,
                            key=f"qty_{product['Product']}"
                        )

                        if st.button(
                            "🛒 Add to Cart",
                            key=f"add_{product['Product']}",
                            use_container_width=True
                        ):
                            name = product["Product"]
                            old_qty = st.session_state.cart.get(
                                name, 0
                            )

                            if old_qty + qty <= stock:
                                st.session_state.cart[name] = (
                                    old_qty + qty
                                )
                                st.toast(f"{name} added!")
                                st.rerun()
                            else:
                                st.error("Stock limit exceeded.")
                    else:
                        st.error("Out of stock")

    # ---------------- CART ----------------
    st.divider()
    st.subheader("🛒 Shopping Cart")

    if not st.session_state.cart:
        st.info("Your cart is empty.")

    else:
        rows = []

        for name, qty in st.session_state.cart.items():
            match = products[products["Product"] == name]

            if not match.empty:
                p = match.iloc[0]
                rows.append({
                    "Product": name,
                    "Quantity": qty,
                    "Price": int(p["Price"]),
                    "Amount": int(p["Price"]) * qty
                })

        cart_df = pd.DataFrame(rows)

        st.dataframe(
            cart_df,
            use_container_width=True,
            hide_index=True
        )

        subtotal = int(cart_df["Amount"].sum())
        delivery = 0 if subtotal >= 499 else 25
        total = subtotal + delivery

        b1, b2, b3 = st.columns(3)
        b1.metric("Subtotal", f"₹{subtotal}")
        b2.metric("Delivery Fee", f"₹{delivery}")
        b3.metric("Total Bill", f"₹{total}")

        left, right = st.columns(2)

        with left:
            if st.button("✅ Place Demo Order"):
                st.session_state.orders.append({
                    "Order ID": len(st.session_state.orders) + 1,
                    "Items": len(rows),
                    "total": total
                })

                for name, qty in st.session_state.cart.items():
                    idx = st.session_state.products.index[
                        st.session_state.products["Product"] == name
                    ][0]

                    st.session_state.products.loc[
                        idx, "Stock"
                    ] -= qty

                st.session_state.cart = {}
                st.success("Demo order placed successfully!")
                st.rerun()

        with right:
            if st.button("🗑️ Clear Cart"):
                st.session_state.cart = {}
                st.rerun()

# ---------------- INVENTORY ----------------
if page == "Inventory":
    st.subheader("📦 Inventory Management")

    st.dataframe(
        products[["Product", "Category", "Price", "Stock"]],
        use_container_width=True,
        hide_index=True
    )

    st.subheader("✏️ Update Stock")

    selected = st.selectbox(
        "Select product",
        products["Product"].tolist()
    )

    current_stock = int(
        products.loc[
            products["Product"] == selected, "Stock"
        ].iloc[0]
    )

    new_stock = st.number_input(
        "New stock quantity",
        min_value=0,
        value=current_stock,
        step=1
    )

    if st.button("💾 Update Inventory"):
        idx = st.session_state.products.index[
            st.session_state.products["Product"] == selected
        ][0]

        st.session_state.products.loc[
            idx, "Stock"
        ] = int(new_stock)

        st.success("Stock updated for this session.")
        st.rerun()

    st.subheader("🚨 Low Stock Alerts")

    low = products[products["Stock"] < 10]

    if low.empty:
        st.success("All products have sufficient stock.")
    else:
        st.dataframe(
            low[["Product", "Category", "Stock"]],
            use_container_width=True,
            hide_index=True
        )

# ---------------- ANALYTICS ----------------
if page == "Analytics":
    st.subheader("📊 Store Analytics")

    st.caption(
        "Charts use demo product data. Revenue comes only "
        "from demo orders placed during this session."
    )

    chart1, chart2 = st.columns(2)

    with chart1:
        st.markdown("### 💸 Product Prices")
        st.bar_chart(
            products.set_index("Product")["Price"]
        )

    with chart2:
        st.markdown("### 📦 Stock by Category")
        st.bar_chart(
            products.groupby("Category")["Stock"].sum()
        )

    st.subheader("🧾 Demo Orders")

    if st.session_state.orders:
        orders = pd.DataFrame(st.session_state.orders)
        st.dataframe(
            orders,
            use_container_width=True,
            hide_index=True
        )
        st.line_chart(orders.set_index("Order ID")["total"])
    else:
        st.info("Place a demo order to see revenue analytics.")

    st.subheader("📋 Product Inventory")
    st.dataframe(
        products[["Product", "Category", "Price", "Stock"]],
        use_container_width=True,
        hide_index=True
    )

# ---------------- FOOTER ----------------
st.divider()
st.markdown(
    "<p style='text-align:center;color:#66776a'>"
    "🌱 Blinkit Store Dashboard | Python + Streamlit + Pandas"
    "</p>",
    unsafe_allow_html=True
)
