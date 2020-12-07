import tkinter as tk
from tkinter import messagebox
from crypto.elgamal import decrypt, encrypt, generate_keys

class GUI(tk.Frame):
    def __init__(self, main=None):
        tk.Frame.__init__(self, main)
        self.main=main

        self.main.title("ElGamal Calculator")
        self.main.resizable(False, False)

        # Bagian Atas
        self.top_frame = tk.Frame(self.main, bd=1)
        self.key_label = tk.Label(self.top_frame, text="Masukkan ukuran kunci (minimal 16-bit)")
        self.key_entry = tk.Entry(self.top_frame)
        self.keygen_button = tk.Button(self.top_frame, text="Generate", command=self.generateButton)
        self.keygen_label = tk.Label(self.top_frame, text="Kunci yang terbentuk:")
        self.keygen_result = tk.Text(self.top_frame, width=30, height=5)

        self.top_frame.grid(row=0, column=0, sticky="NSEW", pady=2)
        self.key_label.grid(row=0, column=0, sticky=tk.N, pady=2)
        self.key_entry.grid(row=1, column=0, stick=tk.N, pady=2)
        self.keygen_button.grid(row=2, column=0, stick=tk.N, pady=2)
        self.keygen_label.grid(row=3, column=0, stick=tk.N, pady=2)
        self.keygen_result.grid(row=4, column=0, stick=tk.N, pady=2, padx=10)
        self.keygen_result.config(state=tk.DISABLED)

        # Bagian Enkripsi
        self.bot_frame = tk.Frame(self.main, bd=1)
        self.pt_label = tk.Label(self.bot_frame, text="Masukkan Plaintext")
        self.pt_entry = tk.Entry(self.bot_frame)
        self.encrypt_button = tk.Button(self.bot_frame, text="Enkripsi", command=self.encryptButton)
        self.ct_result_label = tk.Label(self.bot_frame, text="Ciphertext Hasil:")
        self.ct_result = tk.Text(self.bot_frame, width=15, height=10)

        self.bot_frame.grid(row=1, column=0, sticky="NSEW", pady=2)
        self.pt_label.grid(row=5, column=0, stick=tk.N, pady=2, padx=10)
        self.pt_entry.grid(row=6, column=0, stick=tk.N, pady=2)
        self.encrypt_button.grid(row=7, column=0, stick=tk.N, pady=2)
        self.ct_result_label.grid(row=8, column=0, stick=tk.N, pady=2)
        self.ct_result.grid(row=9, column=0, stick=tk.N, pady=2)
        self.ct_result.config(state=tk.DISABLED)

        # Bagian Dekripsi
        self.ct_label = tk.Label(self.bot_frame, text="Masukkan Ciphertext")
        self.ct_entry = tk.Entry(self.bot_frame)
        self.decrypt_button = tk.Button(self.bot_frame, text="Dekripsi", command=self.decryptButton)
        self.pt_result_label = tk.Label(self.bot_frame, text="Plaintext Hasil:")
        self.pt_result = tk.Text(self.bot_frame, width=15, height=10)

        self.ct_label.grid(row=5, column=1, stick=tk.N, pady=2, padx=5)
        self.ct_entry.grid(row=6, column=1, stick=tk.N, pady=2)
        self.decrypt_button.grid(row=7, column=1, stick=tk.N, pady=2)
        self.pt_result_label.grid(row=8, column=1, stick=tk.N, pady=2)
        self.pt_result.grid(row=9, column=1, stick=tk.N, pady=2)
        self.pt_result.config(state=tk.DISABLED)

    def generateButton(self):
        size = int(self.key_entry.get())
        if size <= 16:
            messagebox.showerror(title="Terjadi Kesalahan",
                message="Besar kunci harus lebih dari 16-bit!")
        else:
            self.priv, self.pub = generate_keys(size)
            comps = ('p', 'g', 'x')
            self.priv_keys = '\n'.join(["{} = {}".format(comp, getattr(self.priv, comp))
                        for comp in comps])
            comps = ('p', 'g', 'h')
            self.pub_keys = '\n'.join(["{} = {}".format(comp, getattr(self.pub, comp))
                        for comp in comps])
            self.keygen_result.config(state=tk.NORMAL)
            self.keygen_result.delete("1.0", "end")
            self.keygen_result.insert(tk.INSERT,
                f'Public Key:\n{self.pub_keys}\nPrivate Key:\n{self.priv_keys}\n')
            self.keygen_result.config(state = tk.DISABLED)
        
    def encryptButton(self):
        ciphertext = encrypt(self.pub, self.pt_entry.get())
        self.ct_result.config(state=tk.NORMAL)
        self.ct_result.delete("1.0", "end")
        self.ct_result.insert(tk.INSERT, ciphertext)
        self.ct_result.config(state=tk.DISABLED)
        
    def decryptButton(self):
        plaintext = decrypt(self.priv, self.ct_entry.get())
        self.pt_result.config(state=tk.NORMAL)
        self.pt_result.delete("1.0", "end")
        self.pt_result.insert(tk.INSERT, plaintext)
        self.pt_result.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    elgamalGUI=GUI(root)
    elgamalGUI.mainloop()