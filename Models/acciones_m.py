import os  
import yfinance as yf  
from datetime import datetime  

class AccionesModel:  
    def __init__(self):  
        pass  

    def calcular_portafolio(self, perfil_path, filtro_activo, periodo_actual):  
        folder = os.path.dirname(perfil_path)  
        archivo_historial = os.path.join(folder, "historial_inversiones.txt")  
        transacciones = []  
        
        if os.path.exists(archivo_historial):  
            with open(archivo_historial, "r", encoding="utf-8") as f:  
                for linea in f:  
                    try:  
                        if "COMPRA" in linea:  
                            partes = linea.split("|")  
                            fecha_str = partes[0].split("]")[0].replace("[", "").strip()  
                            fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")  
                            ticker = partes[1].split(":")[1].strip()  
                            dinero_usado = float(partes[2].split(":")[1].strip().replace("€", "").strip())  
                            acciones = float(partes[3].split(":")[1].strip().replace("+", ""))  
                            transacciones.append({"fecha": fecha, "ticker": ticker, "acciones": acciones, "dinero_usado": dinero_usado})  
                    except Exception as e:  
                        print(f"Error leyendo línea del historial: {e}")  
                        continue  

        if not transacciones:  
            return "VACIO"  

        criptos_conocidas = ["BTC", "ETH", "DOGE", "ADA", "SOL", "XRP"]  
        if filtro_activo == "Acciones":  
            transacciones = [t for t in transacciones if t["ticker"] not in criptos_conocidas]  
        elif filtro_activo == "Cripto":  
            transacciones = [t for t in transacciones if t["ticker"] in criptos_conocidas]  

        if not transacciones:  
            return None  

        tickers_unicos = list(set([t["ticker"] for t in transacciones]))  
        tickers_yf = [f"{t}-EUR" if t in criptos_conocidas else t for t in tickers_unicos]  

        mapeo_tiempo = {
            "1D": {"periodo": "1d", "intervalo": "2m"},
            "1S": {"periodo": "5d", "intervalo": "5m"},
            "1M": {"periodo": "1mo", "intervalo": "30m"},
            "1A": {"periodo": "1y", "intervalo": "1d"},
            "MAX": {"periodo": "max", "intervalo": "1d"}
        }
        config = mapeo_tiempo.get(periodo_actual, {"periodo": "1mo", "intervalo": "1d"})  

        try:  
            datos = yf.download(tickers_yf, period=config["periodo"], interval=config["intervalo"], progress=False)  
            if datos.empty: return None  

            precios = datos['Close'].ffill().bfill()  

            if hasattr(precios, 'to_frame'):  
                precios = precios.to_frame(name=tickers_yf[0])  

            precios.index = precios.index.tz_localize(None)  

            ahora = datetime.now()  
            if ahora not in precios.index and periodo_actual in ["1D", "1S", "1M"]:  
                precios.loc[ahora] = precios.iloc[-1].copy()  
                precios = precios.sort_index()  

            fechas = precios.index  
            valores = []  
            es_grafico_diario = periodo_actual in ["1A", "MAX"]  

            for fecha_merc in fechas:  
                valor_momento = 0.0  
                for i, ticker in enumerate(tickers_unicos):  
                    ticker_yf = tickers_yf[i]  
                    if es_grafico_diario:  
                        acciones_acumuladas = sum([tr["acciones"] for tr in transacciones if tr["ticker"] == ticker and tr["fecha"].date() <= fecha_merc.date()])  
                    else:  
                        acciones_acumuladas = sum([tr["acciones"] for tr in transacciones if tr["ticker"] == ticker and tr["fecha"] <= fecha_merc])  

                    if acciones_acumuladas > 0:  
                        precio_activo = float(precios[ticker_yf].loc[fecha_merc])  
                        valor_momento += acciones_acumuladas * precio_activo  

                valores.append(valor_momento)  

        except Exception as e:  
            print(f"Error descargando portafolio real: {e}")  
            return None  

        valor_final = valores[-1] if valores else 0  
        coste_base = sum(tr["dinero_usado"] for tr in transacciones if tr.get("dinero_usado") is not None)  

        if coste_base == 0:  
            for tr in transacciones:  
                ticker_yf_tr = f"{tr['ticker']}-EUR" if tr['ticker'] in criptos_conocidas else tr['ticker']  
                try:  
                    idx_compra = precios.index.searchsorted(tr["fecha"])  
                    idx_compra = min(idx_compra, len(precios) - 1)  
                    precio_en_compra = float(precios[ticker_yf_tr].iloc[idx_compra])  
                    coste_base += tr["acciones"] * precio_en_compra  
                except Exception:  
                    pass  

        if coste_base == 0:  
            primeros_no_cero = [v for v in valores if v > 0]  
            coste_base = primeros_no_cero[0] if primeros_no_cero else valor_final  

        valor_inicial = coste_base  

        # DEVOLUCIÓN PURA (Principio SRP: Responsabilidad Única)
        return valores, fechas, valor_final, valor_inicial