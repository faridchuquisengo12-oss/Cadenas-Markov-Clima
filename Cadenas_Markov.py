import random
import tkinter as tk
from tkinter import ttk


estadosPosibles = ["NU", "P", "PS", "SO"]

MATRIZ_MODELO = [
    [0.00, 0.67, 0.33, 0.00],
    [0.00, 0.40, 0.60, 0.00],
    [0.00, 0.00, 0.10, 0.90],
    [0.40, 0.20, 0.00, 0.40],
]

COLORES_ESTADOS = {
    "NU": "#64748b",
    "P": "#38bdf8",
    "PS": "#fbbf24",
    "SO": "#fb7185",
}

FONDO = "#f1f5f9"
TEXTO = "#0f172a"
TEXTO_SECUNDARIO = "#64748b"
AZUL = "#2563eb"


def generarCuadro(n, estado_inicial=None):
    estado = estado_inicial or random.choice(estadosPosibles)
    cuadro = [estado]
    for _ in range(n - 1):
        indice = estadosPosibles.index(estado)
        estado = random.choices(
            estadosPosibles, weights=MATRIZ_MODELO[indice], k=1
        )[0]
        cuadro.append(estado)
    return cuadro


def actualizarMatriz(matriz, estado_anterior, estado_actual):
    if estado_anterior is not None:
        i = estadosPosibles.index(estado_anterior)
        j = estadosPosibles.index(estado_actual)
        matriz[i][j] += 1
    return matriz


def calcularMatrizEstocastica(transiciones):
    matrizEstocastica = []
    for fila in transiciones:
        total = sum(fila)
        nuevaFila = []
        for x in fila:
            nuevaFila.append(round(x / total, 2) if total else 0.0)
        matrizEstocastica.append(nuevaFila)
    return matrizEstocastica


class DashboardMarkov:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard | Cadenas de Markov")
        self.root.geometry("1100x760")
        self.root.minsize(860, 620)
        self.root.configure(bg=FONDO)

        self.cuadro = []
        self.transiciones = [[0] * len(estadosPosibles) for _ in estadosPosibles]

        self._configurar_estilos()
        self._crear_interfaz()

    def _configurar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(14, 9),
            background=AZUL,
            foreground="white",
            borderwidth=0,
        )
        estilo.map("TButton", background=[("active", "#1d4ed8")])
        estilo.configure(
            "TSpinbox",
            font=("Segoe UI", 11),
            padding=8,
            fieldbackground="white",
        )

    def _crear_interfaz(self):
        encabezado = tk.Frame(self.root, bg="#0f172a", padx=28, pady=20)
        encabezado.pack(fill="x")

        tk.Label(
            encabezado,
            text="CADENAS DE MARKOV",
            bg="#0f172a",
            fg="white",
            font=("Segoe UI", 19, "bold"),
        ).pack(anchor="w")
        tk.Label(
            encabezado,
            text="Dashboard de simulación de estados climáticos",
            bg="#0f172a",
            fg="#cbd5e1",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))

        contenido = tk.Frame(self.root, bg=FONDO, padx=24, pady=20)
        contenido.pack(fill="both", expand=True)

        configuracion = tk.Frame(contenido, bg="white", padx=18, pady=14)
        configuracion.pack(fill="x", pady=(0, 16))
        tk.Label(
            configuracion,
            text="Estados iniciales (20–40)",
            bg="white",
            fg=TEXTO,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left")
        self.cantidad_var = tk.IntVar(value=20)
        ttk.Spinbox(
            configuracion,
            from_=20,
            to=40,
            width=5,
            textvariable=self.cantidad_var,
            style="TSpinbox",
        ).pack(side="left", padx=(12, 14))
        tk.Label(
            configuracion,
            text="Estado inicial",
            bg="white",
            fg=TEXTO,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left")
        self.estado_inicial_var = tk.StringVar(value="Aleatorio")
        ttk.Combobox(
            configuracion,
            textvariable=self.estado_inicial_var,
            values=["Aleatorio", *estadosPosibles],
            state="readonly",
            width=11,
        ).pack(side="left", padx=(10, 14))
        ttk.Button(
            configuracion,
            text="Iniciar / reiniciar simulación",
            command=self.iniciar_simulacion,
        ).pack(side="left")
        ttk.Button(
            configuracion,
            text="＋ Agregar estado",
            command=self.agregar_estado,
        ).pack(side="right")

        self.error_var = tk.StringVar()
        tk.Label(
            contenido,
            textvariable=self.error_var,
            bg=FONDO,
            fg="#dc2626",
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(0, 6))

        tarjetas = tk.Frame(contenido, bg=FONDO)
        tarjetas.pack(fill="x", pady=(0, 16))
        self.total_var = tk.StringVar(value="—")
        self.dia_var = tk.StringVar(value="—")
        self.estado_var = tk.StringVar(value="—")
        self._crear_tarjeta(tarjetas, "TOTAL DE ESTADOS", self.total_var, "#2563eb")
        self._crear_tarjeta(tarjetas, "DÍA ACTUAL", self.dia_var, "#7c3aed")
        self._crear_tarjeta(tarjetas, "ESTADO ACTUAL", self.estado_var, "#db2777")

        paneles = tk.Frame(contenido, bg=FONDO)
        paneles.pack(fill="both", expand=True)
        paneles.columnconfigure(0, weight=3, uniform="panel")
        paneles.columnconfigure(1, weight=2, uniform="panel")
        paneles.rowconfigure(0, weight=1)

        historial = tk.Frame(paneles, bg="white", padx=18, pady=16)
        historial.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        tk.Label(
            historial,
            text="Historial de estados",
            bg="white",
            fg=TEXTO,
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w")
        tk.Label(
            historial,
            text="Los días más recientes aparecen primero",
            bg="white",
            fg=TEXTO_SECUNDARIO,
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(3, 12))

        area_historial = tk.Frame(historial, bg="white")
        area_historial.pack(fill="both", expand=True)
        self.historial_canvas = tk.Canvas(
            area_historial, bg="white", highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            area_historial, orient="vertical", command=self.historial_canvas.yview
        )
        self.historial_canvas.configure(yscrollcommand=scrollbar.set)
        self.historial_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.historial_frame = tk.Frame(self.historial_canvas, bg="white")
        self.historial_window = self.historial_canvas.create_window(
            (0, 0), window=self.historial_frame, anchor="nw"
        )
        self.historial_frame.bind(
            "<Configure>",
            lambda _event: self.historial_canvas.configure(
                scrollregion=self.historial_canvas.bbox("all")
            ),
        )
        self.historial_canvas.bind(
            "<Configure>",
            lambda event: self.historial_canvas.itemconfigure(
                self.historial_window, width=event.width
            ),
        )

        matriz_panel = tk.Frame(paneles, bg="white", padx=18, pady=16)
        matriz_panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        tk.Label(
            matriz_panel,
            text="Matriz estocástica",
            bg="white",
            fg=TEXTO,
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w")
        tk.Label(
            matriz_panel,
            text="Probabilidad de transición entre estados",
            bg="white",
            fg=TEXTO_SECUNDARIO,
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(3, 14))

        pestanas = ttk.Notebook(matriz_panel)
        pestanas.pack(fill="both", expand=True)
        self.tablas = {
            "frecuencias": self._crear_tabla_matriz(pestanas, "Frecuencias"),
            "observada": self._crear_tabla_matriz(
                pestanas, "Prob. observadas"
            ),
            "modelo": self._crear_tabla_matriz(pestanas, "Modelo"),
        }
        for estado, color in COLORES_ESTADOS.items():
            tk.Label(
                matriz_panel,
                text=f"●  {estado}",
                bg="white",
                fg=color,
                font=("Segoe UI", 9, "bold"),
            ).pack(anchor="w", pady=(12 if estado == "NU" else 3, 0))

        tk.Label(
            matriz_panel,
            text="El siguiente estado se sortea según la fila del modelo correspondiente al estado actual.",
            bg="white",
            fg=TEXTO_SECUNDARIO,
            font=("Segoe UI", 8),
            wraplength=320,
            justify="left",
        ).pack(anchor="w", pady=(12, 0))

        self.iniciar_simulacion()

    def _crear_tabla_matriz(self, parent, titulo):
        marco = tk.Frame(parent, bg="white")
        parent.add(marco, text=titulo)
        tabla = ttk.Treeview(
            marco,
            columns=("origen", *estadosPosibles),
            show="headings",
            height=5,
        )
        tabla.heading("origen", text="De / A")
        tabla.column("origen", width=55, minwidth=50, anchor="center")
        for estado in estadosPosibles:
            tabla.heading(estado, text=estado)
            tabla.column(estado, width=48, minwidth=40, anchor="center")
        tabla.pack(fill="both", expand=True, padx=4, pady=4)
        return tabla

    def _crear_tarjeta(self, parent, titulo, variable, color):
        tarjeta = tk.Frame(parent, bg="white", padx=18, pady=14)
        tarjeta.pack(side="left", fill="x", expand=True, padx=6)
        tk.Frame(tarjeta, bg=color, width=4).pack(side="left", fill="y", padx=(0, 12))
        textos = tk.Frame(tarjeta, bg="white")
        textos.pack(side="left", fill="x", expand=True)
        tk.Label(
            textos,
            text=titulo,
            bg="white",
            fg=TEXTO_SECUNDARIO,
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w")
        tk.Label(
            textos,
            textvariable=variable,
            bg="white",
            fg=TEXTO,
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w", pady=(3, 0))

    def iniciar_simulacion(self):
        try:
            cantidad = self.cantidad_var.get()
        except (tk.TclError, ValueError):
            self.error_var.set("Ingrese un número entero entre 20 y 40.")
            return

        if not 20 <= cantidad <= 40:
            self.error_var.set("La cantidad debe estar entre 20 y 40.")
            return

        self.error_var.set("")
        estado_inicial = self.estado_inicial_var.get()
        if estado_inicial == "Aleatorio":
            estado_inicial = None
        self.cuadro = generarCuadro(cantidad, estado_inicial)
        self.transiciones = [[0] * len(estadosPosibles) for _ in estadosPosibles]
        for anterior, actual in zip(self.cuadro, self.cuadro[1:]):
            actualizarMatriz(self.transiciones, anterior, actual)
        self.actualizar_dashboard()

    def agregar_estado(self):
        if not self.cuadro:
            self.error_var.set("Inicie primero una simulación.")
            return

        anterior = self.cuadro[-1]
        fila_modelo = MATRIZ_MODELO[estadosPosibles.index(anterior)]
        nuevo_estado = random.choices(
            estadosPosibles, weights=fila_modelo, k=1
        )[0]
        self.cuadro.append(nuevo_estado)
        actualizarMatriz(self.transiciones, anterior, nuevo_estado)
        self.error_var.set("")
        self.actualizar_dashboard()

    def actualizar_dashboard(self):
        self.total_var.set(str(len(self.cuadro)))
        self.dia_var.set(str(len(self.cuadro)))
        self.estado_var.set(self.cuadro[-1] if self.cuadro else "—")

        for widget in self.historial_frame.winfo_children():
            widget.destroy()

        for indice, estado in enumerate(reversed(self.cuadro)):
            dia = len(self.cuadro) - indice
            nombre_dia = "HOY" if indice == 0 else f"DÍA {dia}"
            tarjeta = tk.Frame(
                self.historial_frame,
                bg="#f8fafc",
                padx=10,
                pady=9,
                highlightbackground="#e2e8f0",
                highlightthickness=1,
            )
            tarjeta.grid(
                row=indice // 3,
                column=indice % 3,
                sticky="ew",
                padx=4,
                pady=4,
            )
            tk.Label(
                tarjeta,
                text=nombre_dia,
                bg="#f8fafc",
                fg=TEXTO_SECUNDARIO,
                font=("Segoe UI", 8, "bold"),
            ).pack(anchor="w")
            tk.Label(
                tarjeta,
                text=estado,
                bg="#f8fafc",
                fg=COLORES_ESTADOS[estado],
                font=("Segoe UI", 15, "bold"),
            ).pack(anchor="w", pady=(2, 0))

        for columna in range(3):
            self.historial_frame.columnconfigure(columna, weight=1)
        self.historial_canvas.yview_moveto(0)

        probabilidades = calcularMatrizEstocastica(self.transiciones)
        self._actualizar_tabla("frecuencias", self.transiciones, decimales=0)
        self._actualizar_tabla("observada", probabilidades)
        self._actualizar_tabla("modelo", MATRIZ_MODELO)

    def _actualizar_tabla(self, nombre, matriz, decimales=2):
        tabla = self.tablas[nombre]
        for item in tabla.get_children():
            tabla.delete(item)
        for estado, fila in zip(estadosPosibles, matriz):
            if decimales == 0:
                valores = tuple(str(int(valor)) for valor in fila)
            else:
                valores = tuple(f"{valor:.{decimales}f}" for valor in fila)
            tabla.insert("", "end", values=(estado, *valores))


def main():
    Dash = tk.Tk()
    DashboardMarkov(Dash)
    Dash.mainloop()


if __name__ == "__main__":
    main()
