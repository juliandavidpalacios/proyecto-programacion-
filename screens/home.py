import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime
import yfinance as yf


class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller
        self._construir_ui()

    # ─────────────────────────────────────────────
    #  UI ESTÁTICA (se construye una sola vez)
    # ─────────────────────────────────────────────
    def _construir_ui(self):
        # ── HEADER: saludo + botón cerrar sesión ──
        frame_header = tk.Frame(self, bg="#121212")
        frame_header.pack(fill="x", padx=25, pady=(18, 6))

        self.lbl_saludo = tk.Label(
            frame_header, text="Bienvenido", font=("Arial", 20, "bold"),
            bg="#121212", fg="white"
        )
        self.lbl_saludo.pack(side="left")

        self.lbl_fecha = tk.Label(
            frame_header, text="", font=("Arial", 10),
            bg="#121212", fg="#666666"
        )
        self.lbl_fecha.pack(side="left", padx=(14, 0), pady=(6, 0))

        btn_signout = tk.Button(
            frame_header, text="⏻  Cerrar sesión",
            font=("Arial", 10, "bold"), bg="#1e1e1e", fg="#ff4c4c",
            bd=0, padx=12, pady=6, cursor="hand2",
            activebackground="#2a2a2a", activeforeground="#ff4c4c",
            command=self._cerrar_sesion
        )
        btn_signout.pack(side="right")

        # ── FILA DE TARJETAS DE RESUMEN ──
        frame_cards = tk.Frame(self, bg="#121212")
        frame_cards.pack(fill="x", padx=25, pady=(6, 0))

        self.card_ahorro   = self._crear_card(frame_cards, "💰 Total Ahorrado",   "—",     "#2ecc71")
        self.card_mes      = self._crear_card(frame_cards, "📅 Aportado este mes", "—",    "#00ffcc")
        self.card_invertido = self._crear_card(frame_cards, "📈 Invertido",        "—",    "#ffcc00")
        self.card_valor    = self._crear_card(frame_cards, "💹 Valor actual",      "—",    "#a78bfa")

        # ── FILA INFERIOR: portafolio + historial reciente ──
        frame_inferior = tk.Frame(self, bg="#121212")
        frame_inferior.pack(fill="both", expand=True, padx=25, pady=12)

        # Panel izquierdo: portafolio de activos
        frame_portafolio = tk.LabelFrame(
            frame_inferior, text=" Mis Activos ",
            font=("Arial", 10, "bold"), fg="#a78bfa",
            bg="#121212", bd=1, padx=10, pady=8
        )
        frame_portafolio.pack(side="left", fill="both", expand=True, padx=(0, 8))

        # Cabecera de columnas
        frame_cab = tk.Frame(frame_portafolio, bg="#1a1a1a")
        frame_cab.pack(fill="x", pady=(0, 4))
        for txt, w, anc in [("Activo", 80, "w"), ("Cantidad", 90, "e"), ("Precio", 90, "e"), ("Valor", 90, "e"), ("±%", 70, "e")]:
            tk.Label(frame_cab, text=txt, font=("Arial", 8, "bold"),
                     fg="#666666", bg="#1a1a1a", width=w//8, anchor=anc).pack(side="left", padx=4)

        self.frame_filas = tk.Frame(frame_portafolio, bg="#121212")
        self.frame_filas.pack(fill="both", expand=True)

        self.lbl_sin_activos = tk.Label(
            self.frame_filas, text="Sin inversiones todavía.\nPulsa + Nueva Inversión para empezar.",
            font=("Arial", 10), fg="#444444", bg="#121212", justify="center"
        )
        self.lbl_sin_activos.pack(expand=True, pady=20)

        # Panel derecho: últimos movimientos de ahorro
        frame_historial = tk.LabelFrame(
            frame_inferior, text=" Últimos movimientos ",
            font=("Arial", 10, "bold"), fg="#2ecc71",
            bg="#121212", bd=1, padx=10, pady=8
        )
        frame_historial.pack(side="right", fill="both", expand=True, padx=(8, 0))

        self.frame_movimientos = tk.Frame(frame_historial, bg="#121212")
        self.frame_movimientos.pack(fill="both", expand=True)

        self.lbl_sin_mov = tk.Label(
            self.frame_movimientos, text="Sin movimientos de ahorro.",
            font=("Arial", 10), fg="#444444", bg="#121212"
        )
        self.lbl_sin_mov.pack(expand=True, pady=20)

        # Botón de acceso rápido a Nueva Inversión
        btn_invertir = tk.Button(
            self, text="➕  Nueva Inversión",
            font=("Arial", 10, "bold"), bg="#2ecc71", fg="black",
            bd=0, padx=16, pady=7, cursor="hand2",
            command=lambda: self.controller.mostrar_frame("Invertir")
        )
        btn_invertir.pack(anchor="e", padx=25, pady=(0, 14))

    # ─────────────────────────────────────────────
    #  HELPERS DE UI
    # ─────────────────────────────────────────────
    def _crear_card(self, parent, titulo, valor, color):
        card = tk.Frame(parent, bg="#1e1e1e", bd=0,
                        highlightbackground=color, highlightthickness=1)
        card.pack(side="left", fill="both", expand=True, padx=(0, 8), ipady=8)
        tk.Label(card, text=titulo, font=("Arial", 9),
                 fg="#888888", bg="#1e1e1e").pack(pady=(8, 2))
        lbl = tk.Label(card, text=valor, font=("Arial", 16, "bold"),
                       fg=color, bg="#1e1e1e")
        lbl.pack()
        return lbl

    def _fila_activo(self, parent, ticker, cantidad, precio, valor, pct, row):
        bg = "#121212" if row % 2 == 0 else "#161616"
        frame = tk.Frame(parent, bg=bg)
        frame.pack(fill="x", pady=1)
        color_pct = "#2ecc71" if pct >= 0 else "#ff4c4c"
        signo = "+" if pct >= 0 else ""
        datos = [
            (ticker,                  80, "w", "white"),
            (f"{cantidad:.5f}",       90, "e", "#b3b3b3"),
            (f"{precio:,.2f} €",      90, "e", "#b3b3b3"),
            (f"{valor:,.2f} €",       90, "e", "white"),
            (f"{signo}{pct:.2f}%",    70, "e", color_pct),
        ]
        for txt, w, anc, fg in datos:
            tk.Label(frame, text=txt, font=("Arial", 9),
                     fg=fg, bg=bg, width=w//8, anchor=anc).pack(side="left", padx=4)

    def _fila_movimiento(self, parent, tipo, categoria, cantidad, row):
        bg = "#121212" if row % 2 == 0 else "#161616"
        frame = tk.Frame(parent, bg=bg)
        frame.pack(fill="x", pady=1)
        icono  = "▲" if tipo == "Ingreso" else "▼"
        color  = "#2ecc71" if tipo == "Ingreso" else "#ff4c4c"
        signo  = "+" if tipo == "Ingreso" else "-"
        tk.Label(frame, text=icono, font=("Arial", 10, "bold"),
                 fg=color, bg=bg, width=2).pack(side="left", padx=(2, 4))
        tk.Label(frame, text=categoria, font=("Arial", 9),
                 fg="#b3b3b3", bg=bg, anchor="w", width=22).pack(side="left")
        tk.Label(frame, text=f"{signo}{cantidad:.2f} €", font=("Arial", 9, "bold"),
                 fg=color, bg=bg, anchor="e").pack(side="right", padx=6)

    # ─────────────────────────────────────────────
    #  CARGA DE DATOS (se llama al entrar a Home)
    # ─────────────────────────────────────────────
    def cargar_datos_usuario(self):
        perfil_path = self.controller.usuario_logueado
        if not perfil_path:
            return

        # Fecha y saludo
        self.lbl_fecha.config(text=datetime.now().strftime("%A, %d de %B de %Y").capitalize())
        nombre = self._leer_nombre(perfil_path)
        self.lbl_saludo.config(text=f"Hola, {nombre} 👋")

        folder = os.path.dirname(perfil_path)

        # ── AHORROS ──────────────────────────────
        total_ahorrado, aportado_mes, ultimos_movs = self._leer_ahorros(folder)
        self.card_ahorro.config(text=f"{total_ahorrado:,.2f} €")
        self.card_mes.config(text=f"{aportado_mes:,.2f} €")
        self._poblar_movimientos(ultimos_movs)

        # ── INVERSIONES ──────────────────────────
        total_invertido = self._leer_total_invertido(folder)
        self.card_invertido.config(text=f"{total_invertido:,.2f} €")

        # ── PORTAFOLIO CON PRECIOS EN TIEMPO REAL ─
        portafolio = self._leer_portafolio(perfil_path)
        if portafolio:
            valor_actual = self._poblar_activos(portafolio, folder)
            self.card_valor.config(text=f"{valor_actual:,.2f} €")
        else:
            self.card_valor.config(text="0.00 €")
            self._limpiar_frame(self.frame_filas)
            self.lbl_sin_activos = tk.Label(
                self.frame_filas,
                text="Sin inversiones todavía.\nPulsa + Nueva Inversión para empezar.",
                font=("Arial", 10), fg="#444444", bg="#121212", justify="center"
            )
            self.lbl_sin_activos.pack(expand=True, pady=20)

    # ─────────────────────────────────────────────
    #  LECTORES DE DATOS
    # ─────────────────────────────────────────────
    def _leer_nombre(self, perfil_path):
        try:
            with open(perfil_path, "r", encoding="utf-8") as f:
                for linea in f:
                    if linea.startswith("Nombre Completo:"):
                        return linea.split(":", 1)[1].strip()
        except Exception:
            pass
        return "Usuario"

    def _leer_ahorros(self, folder):
        """Devuelve (total_ahorrado, aportado_mes, últimos 5 movimientos)"""
        archivo = os.path.join(folder, "ahorros.txt")
        total = 0.0
        mes   = 0.0
        movs  = []
        mes_actual = datetime.now().month
        anio_actual = datetime.now().year
        if not os.path.exists(archivo):
            return total, mes, movs
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                lineas = f.readlines()
            for linea in lineas:
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split(",")
                if len(partes) == 3:
                    tipo, cat, cant_str = partes
                    cantidad = float(cant_str)
                    if tipo == "Ingreso":
                        total += cantidad
                        mes   += cantidad   # simplificado: todas las entradas cuentan
                    else:
                        total -= cantidad
                    movs.append((tipo, cat, cantidad))
        except Exception as e:
            print(f"[Home] Error leyendo ahorros: {e}")
        return total, mes, list(reversed(movs))[:5]

    def _leer_total_invertido(self, folder):
        """Suma todos los 'Dinero usado' del historial de inversiones"""
        archivo = os.path.join(folder, "historial_inversiones.txt")
        total = 0.0
        if not os.path.exists(archivo):
            return total
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    if "COMPRA" in linea and "Dinero usado:" in linea:
                        partes = linea.split("|")
                        for p in partes:
                            if "Dinero usado:" in p:
                                # "Dinero usado: 100.00 €" — usamos split("Dinero usado:") para
                                # evitar romper por los dos puntos de la marca de tiempo [fecha]
                                valor_str = p.split("Dinero usado:")[1].strip().replace("€", "").strip()
                                total += float(valor_str)
        except Exception as e:
            print(f"[Home] Error leyendo historial: {e}")
        return total

    def _leer_portafolio(self, perfil_path):
        """Lee el archivo perfil_portafolio.txt (TICKER: cantidad)"""
        folder      = os.path.dirname(perfil_path)
        nombre_base = os.path.splitext(os.path.basename(perfil_path))[0]
        archivo     = os.path.join(folder, f"{nombre_base}_portafolio.txt")
        portafolio  = {}
        if not os.path.exists(archivo):
            return portafolio
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if ":" in linea:
                        ticker, cant = linea.split(":", 1)
                        portafolio[ticker.strip().upper()] = float(cant.strip())
        except Exception as e:
            print(f"[Home] Error leyendo portafolio: {e}")
        return portafolio

    # ─────────────────────────────────────────────
    #  POBLADORES DE UI
    # ─────────────────────────────────────────────
    def _poblar_movimientos(self, movs):
        self._limpiar_frame(self.frame_movimientos)
        if not movs:
            tk.Label(self.frame_movimientos, text="Sin movimientos de ahorro.",
                     font=("Arial", 10), fg="#444444", bg="#121212").pack(expand=True, pady=20)
            return
        for i, (tipo, cat, cantidad) in enumerate(movs):
            self._fila_movimiento(self.frame_movimientos, tipo, cat, cantidad, i)

    def _leer_coste_por_ticker(self, folder):
        """Lee historial_inversiones.txt y devuelve el dinero real gastado por ticker.
        Misma fuente que usa acciones.py → los porcentajes siempre cuadran."""
        archivo = os.path.join(folder, "historial_inversiones.txt")
        coste = {}          # {ticker: euros_gastados_totales}
        if not os.path.exists(archivo):
            return coste
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    if "COMPRA" not in linea:
                        continue
                    partes = linea.split("|")
                    if len(partes) < 3:
                        continue
                    try:
                        ticker      = partes[1].split(":")[1].strip()
                        dinero_str  = partes[2].split("Dinero usado:")[1].strip().replace("€", "").strip()
                        dinero      = float(dinero_str)
                        coste[ticker] = coste.get(ticker, 0.0) + dinero
                    except Exception:
                        continue
        except Exception as e:
            print(f"[Home] Error leyendo coste por ticker: {e}")
        return coste

    def _poblar_activos(self, portafolio, folder):
        """Descarga precios intradía y pinta las filas.
        El ±% se calcula respecto al coste real de compra (igual que acciones.py)."""
        self._limpiar_frame(self.frame_filas)

        criptos    = {"BTC", "ETH", "DOGE", "ADA", "SOL", "XRP", "BNB", "LTC"}
        tickers_yf = [f"{t}-EUR" if t in criptos else t for t in portafolio.keys()]

        # Coste real por ticker leído del historial (mismo fichero que usa acciones.py)
        coste_ticker = self._leer_coste_por_ticker(folder)

        valor_total = 0.0
        precios     = {}
        cambios     = {}

        try:
            import pandas as pd
            # Precio intradía reciente (igual que acciones.py en periodo 1D)
            datos = yf.download(tickers_yf, period="1d", interval="2m",
                                progress=False, auto_adjust=True)
            if not datos.empty:
                # Normalizar siempre a DataFrame con columnas = tickers_yf
                if isinstance(datos.columns, pd.MultiIndex):
                    cierre = datos["Close"]
                else:
                    cierre = datos["Close"].to_frame(name=tickers_yf[0])

                for ticker_orig, ticker_yf_str in zip(portafolio.keys(), tickers_yf):
                    try:
                        col = cierre[ticker_yf_str].dropna()
                        if col.empty:
                            raise ValueError("sin datos")
                        precio_actual           = float(col.iloc[-1])
                        precios[ticker_orig]    = precio_actual
                    except Exception as ex:
                        print(f"[Home] Sin precio para {ticker_yf_str}: {ex}")
                        precios[ticker_orig] = 0.0
        except Exception as e:
            print(f"[Home] Error descargando precios: {e}")

        for i, (ticker, cantidad) in enumerate(portafolio.items()):
            precio = precios.get(ticker, 0.0)
            valor  = cantidad * precio

            # ±% respecto al coste real de compra (mismo criterio que acciones.py)
            coste  = coste_ticker.get(ticker, 0.0)
            if coste > 0:
                pct = (valor - coste) / coste * 100
            else:
                pct = 0.0

            cambios[ticker] = pct
            valor_total    += valor
            self._fila_activo(self.frame_filas, ticker, cantidad, precio, valor, pct, i)

        return valor_total

    def _limpiar_frame(self, frame):
        for w in frame.winfo_children():
            w.destroy()

    # ─────────────────────────────────────────────
    #  CERRAR SESIÓN
    # ─────────────────────────────────────────────
    def _cerrar_sesion(self):
        if not messagebox.askyesno("Cerrar sesión",
                                   "¿Estás seguro de que quieres cerrar sesión?"):
            return

        # Detener timers activos en AccionesFrame antes de destruir los frames
        if "Acciones" in self.controller.frames:
            acciones_frame = self.controller.frames["Acciones"]
            if hasattr(acciones_frame, "detener_refresco"):
                acciones_frame.detener_refresco()

        # Destruir frames de la sesión actual
        for frame in self.controller.frames.values():
            frame.destroy()
        self.controller.frames = {}

        # Ocultar el menú lateral
        if hasattr(self.controller, "menu_lateral"):
            self.controller.menu_lateral.destroy()
        if hasattr(self.controller, "contenedor_principal"):
            self.controller.contenedor_principal.destroy()

        # Limpiar usuario y volver al login
        self.controller.usuario_logueado = None
        self.controller.contenedor_auth = tk.Frame(self.controller, bg="#121212")
        self.controller.contenedor_auth.pack(fill="both", expand=True)
        self.controller.mostrar_login()