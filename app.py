import streamlit as st
from FSM import CoffeeFSM

st.set_page_config(page_title="Logic Coffee Bot", page_icon="📖", layout="wide")

st.markdown("""<style>
    .stMetric {
    background-color: #f0f2f6;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #e0e0e0;
    }
    .stChatMessage { padding: 10px; }
</style>
""", unsafe_allow_html=True)

if 'bot' not in st.session_state:
    st.session_state.bot = CoffeeFSM()
    st.session_state.bot.step()
    st.session_state.history = [{"role": "assistant", "content": st.session_state.bot.get_response()}]

st.title(" 🐱 Logic Coffee Shop")
st.markdown("---")

tab1, tab2 = st.tabs(["Chat Pemesanan", "Daftar Menu"])

with tab1:
    col_chat, col_info = st.columns([2, 1])

    with col_info:
        st.subheader("🔒 Keranjang")
        if st.session_state.bot.cart:
            total = 0
            for i, item in enumerate(st.session_state.bot.cart):
                subtotal = item['price'] * item['qty']
                total += subtotal
                st.markdown(f"{i+1}. {item['emoji']} **{item['item'].capitalize()}**")
                st.caption(f"{item['qty']} x Rp {item['price']:,.0f} = Rp {subtotal:,.0f}")
                st.divider()
            st.metric("Total Tagihan", f"Rp {total:,.0f}")

            if st.button("Kosongkan Keranjang"):
                st.session_state.bot.cart = []
                st.rerun()
        else:
            st.info("Keranjang masih kosong.")

        st.markdown("---")
        st.caption(f"Status Bot: `{st.session_state.bot.state.name}`")
        if st.button("Reset Sistem"):
            st.session_state.clear()
            st.rerun()

    with col_chat:
        chat_container = st.container(height=500)

        with chat_container:
            for msg in st.session_state.history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        if prompt := st.chat_input("Contoh: Pesan 2 kopi dan 1 teh..."):
            st.session_state.history.append({"role": "user", "content": prompt})
            st.session_state.bot.step(prompt)
            bot_reply = st.session_state.bot.get_response()
            st.session_state.history.append({"role": "assistant", "content": bot_reply})

with tab2:
    st.header("Daftar Menu Kami")
    st.markdown("Minuman terbaik diracik dengan *logika* dan *cinta*.")

    menu_items = st.session_state.bot.nlp.menu_data
    cols = st.columns(2)

    for index, (key, data) in enumerate(menu_items.items()):
        with cols[index % 2]:
            st.container()
            st.markdown(f"### {data['emoji']} {key.capitalize()} ")
            st.markdown(f"{data['desc']}")
            st.metric(label="Harga", value=f"Rp {data['price']:,.0f}")
            st.markdown("---")
