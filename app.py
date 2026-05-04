import streamlit as st
import pandas as pd
import math

st.title("📦 Smart AI Warehouse")

# -------------------------
# 📊 DATASET (simulation)
# -------------------------
data = pd.DataFrame({
    "Product": ["A", "B", "C", "D", "E"],
    "X": [1, 5, 2, 8, 6],
    "Y": [1, 2, 6, 3, 7],
    "Stock": [10, 8, 15, 5, 12]
})

st.subheader("📊 Stock actuel")
st.dataframe(data)

# -------------------------
# 📦 COMMANDES
# -------------------------
st.subheader("🛒 Nouvelle commande")

products = st.multiselect(
    "Choisir les produits",
    data["Product"].tolist()
)

# -------------------------
# 📏 FONCTION DISTANCE
# -------------------------
def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# -------------------------
# 🚀 OPTIMISATION SIMPLE (Nearest Neighbor)
# -------------------------
def optimize_path(order, df):
    if not order:
        return []

    remaining = order.copy()
    path = []

    # Point de départ (entrée entrepôt)
    current = (0, 0)

    while remaining:
        nearest = None
        min_dist = float('inf')

        for product in remaining:
            row = df[df["Product"] == product].iloc[0]
            pos = (row["X"], row["Y"])
            dist = distance(current, pos)

            if dist < min_dist:
                min_dist = dist
                nearest = product

        path.append(nearest)
        row = df[df["Product"] == nearest].iloc[0]
        current = (row["X"], row["Y"])
        remaining.remove(nearest)

    return path

# -------------------------
# 📦 TRAITEMENT COMMANDE
# -------------------------
if st.button("Optimiser le picking"):
    if not products:
        st.warning("Choisissez au moins un produit")
    else:
        path = optimize_path(products, data)

        st.success("✅ Chemin optimal calculé")
        st.write("👉 Ordre de picking :", path)

        # Mise à jour du stock
        for p in path:
            data.loc[data["Product"] == p, "Stock"] -= 1

        st.subheader("📉 Stock après picking")
        st.dataframe(data)

# -------------------------
# 📊 KPI SIMPLE
# -------------------------
st.subheader("📈 KPI")

total_stock = data["Stock"].sum()
st.metric("Stock total", total_stock)
