# Designed with https://visualtkinter.com - paste this file into File > Import there to edit it visually
import tkinter as tk
from tkinter import ttk


class Application:
    def __init__(self, root):
        self.root = root
        root.title("Clima")
        root.geometry("520x380")

        self.main_frame = tk.Frame(root, bg="#18181b")
        self.main_frame.place(x=0, y=0, width=520, height=380)

        self.search_entry = tk.Entry(
            self.main_frame,
            bg="#27272a",
            fg="#f4f4f5",
            insertbackground="#f4f4f5",
            font=("Segoe UI", 11),
        )
        self.search_entry.place(x=24, y=20, width=376, height=36)
        self.search_entry.bind("<FocusIn>", self._limpiar_placeholder)
        self.search_entry.bind("<KeyRelease>", self._al_escribir)

        self.search_btn = tk.Button(self.main_frame, text="Buscar", command=self.on_search_btn, fg="#ffffff", bg="#3b82f6", font=("Segoe UI", 10, "bold"))
        self.search_btn.place(x=408, y=20, width=88, height=36)

        self.card_frame = tk.Frame(self.main_frame, bg="#27272a")
        self.card_frame.place(x=24, y=76, width=472, height=280)

        self.city_label = tk.Label(self.card_frame, text="Montevideo, Uruguay", fg="#f4f4f5", bg="#27272a", font=("Segoe UI", 13, "bold"))
        self.city_label.place(x=20, y=24, width=430, height=28)

        self.tz_label = tk.Label(self.card_frame, text="Timezone: America/Montevideo", fg="#a1a1aa", bg="#27272a", font=("Segoe UI", 9))
        self.tz_label.place(x=20, y=54, width=430, height=20)

        self.temp_label = tk.Label(self.card_frame, text="22.5 °C", fg="#ffffff", bg="#27272a", font=("Segoe UI", 42, "bold"))
        self.temp_label.place(x=20, y=165, width=220, height=75)

        self.condition_label = tk.Label(self.card_frame, text="Parcialmente nublado", fg="#60a5fa", bg="#27272a", font=("Segoe UI", 12, "bold"))
        self.condition_label.place(x=240, y=185, width=210, height=26)

        self.humidity_label = tk.Label(self.card_frame, text="Humedad: 68%", fg="#d4d4d8", bg="#27272a", font=("Segoe UI", 10))
        self.humidity_label.place(x=240, y=215, width=210, height=22)

        self.setup_extras()

    def on_search_btn(self):
        self.buscar_y_mostrar()

    def setup_extras(self):
        self.root.resizable(False, False)
        self.root.configure(bg="#18181b")

        self.resultados_actuales = []
        self._after_id = None

        self.suggestions_list = tk.Listbox(
            self.main_frame,
            bg="#27272a",
            fg="#f4f4f5",
            selectbackground="#3b82f6",
            selectforeground="#ffffff",
            highlightbackground="#3f3f46",
            highlightthickness=1,
            relief="flat",
            font=("Segoe UI", 10),
            activestyle="none",
        )

        self.search_entry.insert(0, "Buscar ciudad...")
        self.search_entry.bind("<FocusIn>", self._limpiar_placeholder)
        self.search_entry.bind("<KeyRelease>", self._al_escribir)
        self.suggestions_list.bind("<<ListboxSelect>>", self._al_seleccionar)
        self.root.bind("<Button-1>", self._clic_afuera)

    def _limpiar_placeholder(self, event):
        if self.search_entry.get() == "Buscar ciudad...":
            self.search_entry.delete(0, tk.END)

    def _al_escribir(self, event):
        if event.keysym in ("Up", "Down", "Return", "Escape"):
            return

        if self._after_id:
            self.root.after_cancel(self._after_id)
        self._after_id = self.root.after(350, self.buscar_y_mostrar)

    def buscar_y_mostrar(self):
        texto = self.search_entry.get().strip()
        if len(texto) < 2 or texto == "Buscar ciudad...":
            self.suggestions_list.place_forget()
            return

        # DATOS DE DEMOSTRACIÓN
        self.resultados_actuales = [
            {"etiqueta": f"{texto}, Departamento de Montevideo, Uruguay"},
            {"etiqueta": f"{texto}, Departamento de Canelones, Uruguay"},
            {"etiqueta": f"{texto}, Buenos Aires, Argentina"},
        ]

        if not self.resultados_actuales:
            self.suggestions_list.place_forget()
            return

        self.suggestions_list.delete(0, tk.END)
        for item in self.resultados_actuales:
            self.suggestions_list.insert(tk.END, f"  {item['etiqueta']}")

        alto = min(len(self.resultados_actuales), 6) * 26 + 4
        self.suggestions_list.place_configure(x=24, y=58, width=376, height=alto)
        self.suggestions_list.lift()

    def _al_seleccionar(self, event):
        seleccion = self.suggestions_list.curselection()
        if not seleccion:
            return

        indice = seleccion[0]
        elegido = self.resultados_actuales[indice]

        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, elegido["etiqueta"])
        self.suggestions_list.place_forget()

        self.city_label.config(text=elegido["etiqueta"])

    def _clic_afuera(self, event):
        if event.widget not in (self.search_entry, self.suggestions_list):
            self.suggestions_list.place_forget()


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
