import streamlit as st
from FSM import CoffeeFSM  # Mengimpor class FSM yang dibuat pada pertemuan 10

# Inisialisasi chatbot pada session state Streamlit
if 'bot' not in st.session_state:
    st.session_state.bot = CoffeeFSM()
    st.session_state.bot.step() # Memulai state awal
    # Menyimpan riwayat percakapan dengan sapaan awal dari bot
    st.session_state.history = [{"role": "assistant", "content": st.session_state.bot.get_response()}]

    # Menambahkan header title dan markdown sebagai judul web
st.title("☕ Logic Coffee Shop")
st.markdown("---")

# Membuat 2 tab menu: Menu Pemesanan dan Daftar Menu
tab1, tab2 = st.tabs(["Pemesanan", "Daftar Menu"])

# --- TAB 1: MENU PEMESANAN ---
with tab1:
    # Membagi layout menjadi 2 kolom (Kiri untuk Keranjang, Kanan untuk Chatbot)
    col1, col2 = st.columns([1, 2])
    
    # Bagian 1: Menampilkan Keranjang Belanja
    with col1:
        st.subheader("🛒 Keranjang Belanja")
        cart_items = st.session_state.bot.cart
        
        if len(cart_items) == 0:
            st.info("Keranjang masih kosong.")
        else:
            for item in cart_items:
                st.write(f"- {item['qty']}x **{item['item']}** (Rp {item['total']:,})")
            
            st.markdown("---")
            total_harga = st.session_state.bot.calculate_total()
            st.success(f"**Total: Rp {total_harga:,}**")

    # Bagian 2: Percakapan dengan Chatbot
    with col2:
        st.subheader("💬 Chatbot Pelayan")
        
        # Menampilkan riwayat chat dari session_state
        for message in st.session_state.history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Menerima input dari user
        user_input = st.chat_input("Ketik pesanan Anda di sini...")
        
        if user_input:
            # Menampilkan pesan user
            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state.history.append({"role": "user", "content": user_input})
            
            # Memproses input menggunakan FSM
            st.session_state.bot.step(user_input)
            bot_response = st.session_state.bot.get_response()
            
            # Menampilkan balasan bot dan menyimpannya ke riwayat
            with st.chat_message("assistant"):
                st.markdown(bot_response)
            st.session_state.history.append({"role": "assistant", "content": bot_response})
            
            # Refresh halaman untuk memperbarui keranjang belanja di kolom kiri
            st.rerun()

# --- TAB 2: DAFTAR MENU ---
with tab2:
    st.subheader("📖 Daftar Menu yang Tersedia")
    # Mengambil teks menu dari fungsi get_menu_text() yang ada di FSM
    menu_text = st.session_state.bot.get_menu_text()
    st.markdown(menu_text)