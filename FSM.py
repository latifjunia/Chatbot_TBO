from enum import Enum, auto
from engine import Engine as NLPEngine

class State(Enum):
    IDLE = auto()
    ORDERING = auto()
    CONFIRMATION = auto()
    PAYMENT = auto()

class CoffeeFSM:
    def __init__(self):
        self.state = State.IDLE
        self.nlp = NLPEngine()
        self.cart = []
        self.response = ""

    def get_response(self):
        return self.response
        
    def calculate_total(self):
        return sum(item['price'] * item['qty'] for item in self.cart)

    def get_menu_text(self):
    """Fungsi bantuan untuk merangkai teks daftar menu"""
    teks_menu = "**Daftar Menu Logic Coffee:**\n\n"
    for key, data in self.nlp.menu_data.items():
        if "harga" in data:
            teks_menu += f"- ☕ **{key.capitalize()}** (Rp {data['harga']:,})\n"
        elif "variasi" in data:
            variasi_str = ", ".join(data["variasi"])
            teks_menu += f"- ☕ **{key.capitalize()}** (Rp {data['harga']:,}): *{variasi_str}*\n"
    
    teks_menu += "\nSilakan ketik pesanan Anda (contoh: *'Pesan 2 teh, 1 espresso'*)."
    return teks_menu
    def reduce_cart(self, item_to_reduce, qty_to_remove):
        """Logika untuk mengurangi qty item atau menghapusnya jika qty <= 0"""
        found = False
        message = ""
        
        # Cari Item di cart
        for item in self.cart:
            if item['item'].lower() == item_to_reduce.lower():
                item['qty'] -= qty_to_remove
                found = True
                
                if item['qty'] <= 0:
                    self.cart.remove(item)
                    message = f"❌ **{item_to_reduce.capitalize()}** telah dihapus dari keranjang."
                else:
                    message = f"✅ **{item_to_reduce.capitalize()}** dikurangi {qty_to_remove}. Sisa: {item['qty']}."
                break
                
        if not found:
            message = f"Gagal: **{item_to_reduce.capitalize()}** tidak ditemukan di keranjang Anda."
            
        return message
    def step(self, user_input=""):
        user_input = user_input.lower().strip()
        intent = self.nlp.detect_intent(user_input)

        # --- GLOBAL COMMANDS ---
        if intent == "RESET":
            self.__init__()
            self.response = "Sistem di-reset. Mari mulai dari awal. Mau pesan apa?"
            return

        if intent == "ASK_MENU":
            self.response = self.get_menu_text()
            return

        # --- STATE MACHINE ---
        if self.state == State.IDLE:
            self.response = f"Halo! Selamat datang di Logic Coffee.\n\n{self.get_menu_text()}"
            self.state = State.ORDERING

        elif self.state == State.ORDERING:
            if intent == "CHECKOUT":
                if len(self.cart) == 0:
                    self.response = "Keranjang Anda kosong. Silakan pesan sesuatu terlebih dahulu."
                else:
                    self.state = State.CONFIRMATION
                    pesanan = "\n".join([f"- {item['qty']}x {item['item']}" for item in self.cart])
                    total = self.calculate_total()
                    self.response = f"Baik, ini pesanan Anda:\n{pesanan}\n\nTotal sementara: Rp {total:,}.\nApakah pesanan sudah benar? (Ya/Tidak/Batal)"
            
            elif intent == "REDUCE_ITEM":
                # Tambahkan logika untuk mengekstrak item dan jumlah yang ingin dikurangi
                # (Sederhananya memanggil self.reduce_cart)
                self.response = "Fitur kurangi pesanan dijalankan. Silakan cek keranjang Anda."
                
            else:
                orders = self.nlp.parse_orders(user_input)
                if orders:
                    for order in orders:
                        # Cek apakah item sudah ada di keranjang
                        existing_item = next((i for i in self.cart if i['item'] == order['item']), None)
                        if existing_item:
                            existing_item['qty'] += order['qty']
                        else:
                            self.cart.append(order)
                            
                    self.response = f"Sip, ditambahkan! Keranjang Anda sekarang berisi {sum(item['qty'] for item in self.cart)} item. \nAda lagi yang ingin dipesan? (Atau ketik 'selesai' untuk bayar)."
                else:
                    self.response = "Maaf, saya tidak menangkap pesanan Anda. Bisa sebutkan item dari menu kami?"

        elif self.state == State.CONFIRMATION:
            if intent == "YES":
                self.state = State.PAYMENT
                total = self.calculate_total()
                self.response = f"Pesanan dikonfirmasi! Total yang harus dibayar adalah **Rp {total:,}**.\nSilakan lakukan pembayaran (Ketik 'bayar' jika sudah)."
            elif intent == "NO" or intent == "REDUCE_ITEM":
                self.state = State.ORDERING
                self.response = "Pemesanan dilanjutkan. Silakan tambah pesanan atau ketik 'batal semua' untuk reset."
            else:
                self.response = "Mohon konfirmasi dengan 'Ya' untuk lanjut bayar atau 'Tidak' untuk ubah pesanan."

        elif self.state == State.PAYMENT:
            # Simulasi pembayaran selesai
            self.response = "Pembayaran berhasil diterima! Pesanan Anda sedang diproses. Terima kasih telah memesan di Logic Coffee."
            self.__init__() # Reset untuk pesanan berikutnya
