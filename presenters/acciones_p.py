# Fíjate que hemos ELIMINADO por completo el "import tkinter". 
# Este archivo ahora es Python puro, lógica de negocio al 100%.

class AccionesPresenter: 
    def __init__(self, view, model): 
        self.view = view 
        self.model = model 
        
        self.modo_porcentaje = True 
        self.periodo_actual = "1M" 
        self.filtro_activo = "Todo" 
        
        # Inyección de dependencias (le decimos a la vista quién es su cerebro)
        self.view.set_presenter(self) 

    def cargar_datos_usuario(self): 
        # 1. Le pedimos a la vista que detenga cualquier temporizador que tuviese antes
        self.view.cancelar_refresco()
        
        # 2. Le pedimos a la vista el string con la ruta del usuario logueado
        usuario_logueado = self.view.obtener_usuario_logueado()
        if not usuario_logueado:
            return

        # 3. Consumimos el Modelo purificado (que ahora solo devuelve datos)
        resultado = self.model.calcular_portafolio(usuario_logueado, self.filtro_activo, self.periodo_actual) 

        if resultado == "VACIO": 
            self.view.mostrar_estado_vacio() 
            self.view.programar_refresco(10000, self.cargar_datos_usuario)
            return 

        if resultado is None: 
            # Si falla la descarga, simplemente lo reintentaremos en 10 segundos
            self.view.programar_refresco(10000, self.cargar_datos_usuario)
            return 

        # 4. Desempaquetamos los vectores crudos del modelo
        valores, fechas, valor_final, valor_inicial = resultado 
        self.valor_final = valor_final 
        self.valor_inicial = valor_inicial 

        # 5. LÓGICA DE NEGOCIO: Calculamos aquí el color (antes esto ensuciaba el modelo)
        color_linea = "#2ecc71" if valor_final >= valor_inicial else "#ff4c4c" 

        # 6. ENVIAMOS ÓRDENES LIMPIAS A LA VISTA
        self.view.actualizar_balance_total(f"{valor_final:,.2f} €")
        self.view.dibujar_grafica(fechas, valores, self.periodo_actual, color_linea) 
        self.actualizar_datos_variacion() 

        # 7. Le decimos a la vista que ella misma reprograme el ciclo de llamadas
        self.view.programar_refresco(10000, self.cargar_datos_usuario)

    def actualizar_datos_variacion(self): 
        if not hasattr(self, 'valor_inicial'): return 
        
        diferencia = self.valor_final - self.valor_inicial 
        porcentaje = (diferencia / self.valor_inicial) * 100 if self.valor_inicial != 0 else 0 
        
        color = "#2ecc71" if diferencia >= 0 else "#ff4c4c" 
        signo = "+" if diferencia >= 0 else "" 
        
        if self.modo_porcentaje: 
            texto = f"{signo}{porcentaje:.2f}%" 
        else: 
            texto = f"{signo}{diferencia:,.2f} €" 
            
        # ¡Magia MVP! No tocamos Tkinter, solo enviamos los parámetros a un método puente.
        self.view.actualizar_etiqueta_variacion(texto, color) 

    def cambiar_filtro(self, filtro): 
        self.filtro_activo = filtro 
        self.view.iluminar_boton_filtro(filtro) 
        self.cargar_datos_usuario() 

    def cambiar_periodo(self, periodo): 
        self.periodo_actual = periodo 
        self.view.iluminar_boton_periodo(periodo) 
        self.cargar_datos_usuario() 

    def alternar_modo_variacion(self): 
        self.modo_porcentaje = not self.modo_porcentaje 
        self.actualizar_datos_variacion() 

    def detener_refresco(self): 
        # Delegamos la parada del reloj interno a la vista
        self.view.cancelar_refresco()