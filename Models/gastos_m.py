import os


class GastosModel:
    def __init__(self):
        pass

    def _convertir_a_ruta_ahorros(self, ruta_base_usuario):
        """
        Método interno para asegurar que siempre leamos 'ahorros.txt'
        sin importar si 'ruta_base_usuario' apunta a perfil.txt o a la carpeta.
        """
        if not ruta_base_usuario:
            return None

        # Si la ruta apunta a un archivo (como perfil.txt), nos quedamos con su carpeta
        if os.path.isfile(ruta_base_usuario):
            carpeta_usuario = os.path.dirname(ruta_base_usuario)
        else:
            carpeta_usuario = ruta_base_usuario

        # Unimos la carpeta con el archivo objetivo exacto: ahorros.txt
        return os.path.join(carpeta_usuario, "ahorros.txt")

    def obtener_saldo_cuenta(self, ruta_usuario):
        """
        Busca el archivo ahorros.txt del usuario, lo lee línea por línea
        y calcula el saldo neto de la 'Cuenta' procesando Ingresos y Retiros.
        """
        # Convertimos la ruta recibida al archivo ahorros.txt real
        ruta_ahorros = self._convertir_a_ruta_ahorros(ruta_usuario)

        if not ruta_ahorros or not os.path.exists(ruta_ahorros):
            print(f"[AVISO GASTOS] No se encontró el archivo físico en: {ruta_ahorros}")
            return 0.0

        saldo_acumulado = 0.0

        try:
            with open(ruta_ahorros, "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()

                    # Ignoramos líneas vacías o registros de la interfaz gráfica
                    if not linea or linea.startswith("GASTO_DETALLE|"):
                        continue

                    # Separamos los campos por comas (Tipo,Categoría,Monto)
                    partes = linea.split(",")
                    if len(partes) < 3:
                        continue

                    # Limpiamos espacios invisibles o molestos
                    tipo_movimiento = partes[0].strip()  # 'Ingreso' o 'Retiro'
                    categoria = partes[1].strip()  # 'Cuenta'
                    monto_str = partes[2].strip()  # El número en texto

                    # Filtro estricto: Solo sumamos/restamos si pertenece a "Cuenta"
                    if categoria == "Cuenta":
                        try:
                            monto = float(monto_str)
                            if tipo_movimiento == "Ingreso":
                                saldo_acumulado += monto
                            elif tipo_movimiento == "Retiro":
                                saldo_acumulado -= monto
                        except ValueError:
                            continue  # Si no se puede convertir a número, salta la línea

            return saldo_acumulado

        except Exception as e:
            print(f"[ERROR GASTOS] Al calcular saldo en ahorros.txt: {e}")
            return 0.0

    def registrar_gasto_en_archivo(self, ruta_usuario, tipo_gasto, categoria, subcategoria, monto):
        """
        Valida los fondos en ahorros.txt y escribe el 'Retiro' correspondiente a la Cuenta.
        """
        ruta_ahorros = self._convertir_a_ruta_ahorros(ruta_usuario)

        if not ruta_ahorros or not os.path.exists(ruta_ahorros):
            return False, "Error: No se detectó el archivo de ahorros del cliente."

        # 1. Validamos el saldo leyendo el archivo correcto
        saldo_actual = self.obtener_saldo_cuenta(ruta_usuario)

        if saldo_actual < monto:
            return False, f"Fondos insuficientes en Cuenta. Saldo actual: {saldo_actual:.2f} €"

        try:
            # 2. Preparamos las líneas con la sintaxis exacta de tu base de datos
            nueva_linea_ahorros = f"Retiro,Cuenta,{monto:.2f}\n"
            registro_informe = f"GASTO_DETALLE|{tipo_gasto}|{categoria}|{subcategoria}|{monto:.2f}\n"

            # 3. Anexamos al final de ahorros.txt
            with open(ruta_ahorros, "a", encoding="utf-8") as f:
                f.write(nueva_linea_ahorros)
                f.write(registro_informe)

            return True, "Gasto registrado y restado de tu Cuenta con éxito."

        except Exception as e:
            return False, f"Error al escribir en ahorros.txt: {str(e)}"

    def obtener_informe_gastos(self, ruta_usuario):
        """Lee las etiquetas GASTO_DETALLE desde ahorros.txt para armar las tablas gráficas"""
        ruta_ahorros = self._convertir_a_ruta_ahorros(ruta_usuario)

        totales = {
            "Fijos": 0.0, "Variables": 0.0, "Hogar": 0.0, "Coche": 0.0, "Total": 0.0
        }
        historial = []

        if not ruta_ahorros or not os.path.exists(ruta_ahorros):
            return totales, historial

        try:
            with open(ruta_ahorros, "r", encoding="utf-8") as f:
                for linea in f:
                    if linea.startswith("GASTO_DETALLE|"):
                        _, tipo, cat, sub, monto_str = linea.strip().split("|")
                        monto = float(monto_str)

                        historial.append((tipo, cat, sub, f"{monto:.2f} €"))
                        totales["Total"] += monto

                        if tipo == "Fijo":
                            totales["Fijos"] += monto
                        elif tipo == "Variable":
                            totales["Variables"] += monto

                        if cat == "Gastos del Hogar 🏠":
                            totales["Hogar"] += monto
                        elif cat == "Gastos del Coche 🚗":
                            totales["Coche"] += monto
        except Exception as e:
            print(f"Error al generar informe desde ahorros.txt: {e}")

        return totales, historial

    def obtener_ahorro_total(self, ruta_usuario):
        """Calcula la suma de todas las huchas (ahorros) excluyendo la 'Cuenta'"""
        ruta_ahorros = self._convertir_a_ruta_ahorros(ruta_usuario)
        ahorro_acumulado = 0.0

        if not ruta_ahorros or not os.path.exists(ruta_ahorros):
            return 0.0

        try:
            with open(ruta_ahorros, "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea or linea.startswith("GASTO_DETALLE|"):
                        continue

                    partes = linea.split(",")
                    if len(partes) < 3: continue

                    tipo = partes[0].strip()
                    categoria = partes[1].strip()
                    monto = float(partes[2].strip())

                    # Si NO es cuenta, es ahorro o inversión en huchas
                    if categoria != "Cuenta":
                        if tipo == "Ingreso":
                            ahorro_acumulado += monto
                        elif tipo == "Retiro":
                            ahorro_acumulado -= monto
            return ahorro_acumulado
        except Exception:
            return 0.0