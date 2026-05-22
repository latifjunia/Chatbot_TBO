import re

class NLPEngine:
    def __init__(self):
        # Data harga (Bisa berupa dict, database, atau API)
        self.menu_data = {
            "Kopi": {"variasi": ["Espresso", "Latte", "Mocha"], "harga": 15000},
            "Teh": {"variasi": ["Manis", "Tawar"], "harga": 5000},
            "Roti": {"variasi": ["Coklat", "Keju"], "harga": 10000},
            "Espresso": {"harga": 15000}, 
            "Latte": {"harga": 15000}, 
            "Mocha": {"harga": 15000}
        }
        
        # Regex Patterns
        self.re_menu = r"(?i)\b(kopi|teh|roti)\b"
        
        # Pola untuk menangkap jumlah dan item
        self.re_qty = r"(?i)\b(\d+)\s*(porsi|gelas|cup|buah|pcs)?\b"
        self.re_item = r"(?i)\b(kopi|teh|roti|espresso|latte|mocha)\b"
        
        # Regex untuk memecah kalimat order
        self.re_split = r"(?i)\b(dan|sama|terus|,|kemudian|tambah|serta|sekalian)\b"
        self.re_cancel = r"(?i)\b(gak|nggak|batal|cancel|hapus|kurang)\b"

    def _parse_single_segment(self, text):
        # Mengecek item dan jumlah dalam satu potongan kalimat
        item = re.search(self.re_item, text)
        
        qty_match = re.search(self.re_qty, text)
        if qty_match:
            qty = int(qty_match.group(1))
        else:
            qty = 1
            
        if item:
            # Mengembalikan dictionary data pesanan
            return {
                "item": item.group().capitalize(),
                "qty": qty,
                "price": self.menu_data[item.group().capitalize()]["harga"],
                "total": qty * self.menu_data[item.group().capitalize()]["harga"]
            }
        return None
    
    def parse_orders(self, full_text):
        """
        Memecah kalimat majemuk: "pesan teh 2, espresso 2"
        Menjadi list orders.
        """
        segments = re.split(self.re_split, full_text)
        
        found_orders = []
        for segment in segments:
            if segment.strip():
                order = self._parse_single_segment(segment)
                if order:
                    found_orders.append(order)
                    
        return found_orders
    
    def detect_intent(self, text):
        text = text.lower()
        if re.search(r"\b(reset|ulang|batal semua)\b", text):
            return "RESET"
        if re.search(r"\b(cancel_all)\b", text):
            return "CANCEL_ALL"
        if re.search(self.re_cancel, text):
            return "REDUCE_ITEM"
        if re.search(r"\b(menu|daftar|apa saja|jual apa)\b", text):
            return "ASK_MENU"
        if re.search(r"\b(selesai|bayar|checkout|cukup)\b", text):
            return "CHECKOUT"
        if re.search(r"\b(ya|yes|oke|betul|siap)\b", text):
            return "YES"
        if re.search(r"\b(tidak|enggak|batal|nanti)\b", text):
            return "NO"
        return "UNKNOWN"
    
    def print_menu(self):
        print(self.menu_data)
