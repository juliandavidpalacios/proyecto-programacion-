"""Presentador de la pantalla de Expertos.

Python puro: NO importa tkinter. Pide los datos al modelo, los formatea y ordena
a la vista cómo pintarlos mediante métodos limpios.
"""


class ExpertosPresenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.view.set_presenter(self)

    def cargar_datos_usuario(self):
        """Carga las compras institucionales y manda a la vista renderizarlas."""
        self.view.mostrar_cargando()
        self.view.refrescar()
        try:
            compras = self.model.obtener_compras_trimestre()
        except Exception as e:
            self.view.mostrar_error("Error", f"No se pudieron obtener los datos de expertos: {e}")
            return

        self.view.limpiar_tabla()
        for compra in compras:
            signo = "+" if compra.variacion_pct >= 0 else ""
            # Pasamos a la vista textos YA formateados; ella solo los pinta.
            self.view.agregar_fila(
                inversor=compra.inversor,
                simbolo=compra.simbolo,
                empresa=compra.empresa,
                acciones=f"{compra.acciones:,.0f}",
                valor=f"{compra.valor:,.0f} €",
                variacion=f"{signo}{compra.variacion_pct:.1f} %",
                positiva=compra.variacion_pct >= 0,
            )

        # Top 6 compras por valor para el gráfico de barras.
        top = compras[:6]
        etiquetas = [f"{c.inversor[:14]}\n{c.simbolo}" for c in top]
        valores = [c.valor for c in top]
        self.view.dibujar_grafico_barras(etiquetas, valores)
        self.view.mostrar_total(f"{len(compras)} compras institucionales detectadas")
