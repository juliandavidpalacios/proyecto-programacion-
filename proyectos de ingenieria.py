from graphviz import Digraph

# Crear el objeto del diagrama
dot = Digraph(comment='Caja Blanca BioCampus', format='png')

# Configuración general: de izquierda a derecha y fuentes claras
dot.attr(rankdir='LR', size='12,8', fontname='Arial')
dot.attr('node', fontname='Arial', fontsize='10')

# --- DEFINICIÓN DE ENTRADAS (FUERA DEL SISTEMA) ---
dot.node('In_Res', 'Residuos Orgánicos\n(Cafeterías)', shape='parallelogram', style='filled', fillcolor='#f9f9f9')
dot.node('In_Die', 'Energía: Diésel', shape='parallelogram', style='filled', fillcolor='#fff4e6')
dot.node('In_Ele', 'Energía: Eléctrica', shape='parallelogram', style='filled', fillcolor='#fff4e6')

# --- SISTEMA BIOCAMPUS (CAJA BLANCA) ---
with dot.subgraph(name='cluster_biocampus') as c:
    c.attr(label='LÍMITE DEL SISTEMA BIOCAMPUS', style='dashed', color='grey', fontcolor='blue')
    c.attr('node', shape='box', style='filled', fillcolor='#e1f5fe')

    c.node('Log', 'Logística y\nRecogida')
    c.node('Pre', 'Pre-tratamiento\n(Mezcla y Pesaje)')
    c.node('Comp', 'Compostaje Activo\n(Reactores/Pilas)')

    # Nodo de control para los sensores
    c.node('Ctrl', 'Sistema de Control\n(Sensores Hº y Tª)', shape='component', fillcolor='#fff9c4')

    c.node('Mad', 'Maduración y\nCribado')
    c.node('Emp', 'Proceso de\nEmpaquetado')

# --- DEFINICIÓN DE SALIDAS (FUERA DEL SISTEMA) ---
dot.node('Out_Com', 'PRODUCTO FINAL:\nCompost en Sacos', shape='doubleoctagon', style='filled', fillcolor='#c8e6c9')
dot.node('Out_Gas', 'Emisiones\n(CO2 y Vapor)', shape='plaintext', fontcolor='grey')
dot.node('Out_Rec', 'Rechazos\n(No compostables)', shape='plaintext', fontcolor='red')

# --- CONEXIÓN DE FLUJOS (LAS FLECHAS) ---

# Flujos de entrada
dot.edge('In_Res', 'Log')
dot.edge('In_Die', 'Log', label='Consumo camiones')
dot.edge('In_Ele', 'Pre')
dot.edge('In_Ele', 'Comp')
dot.edge('In_Ele', 'Emp')

# Flujos internos del proceso
dot.edge('Log', 'Pre', label='Materia prima')
dot.edge('Pre', 'Comp', label='Mezcla óptima')

# Bucle de retroalimentación de los sensores (Humedad y Temperatura)
dot.edge('Comp', 'Ctrl', label='Datos Hº/Tª', color='orange', style='dotted')
dot.edge('Ctrl', 'Comp', label='Actuación (Riego/Aire)', color='orange')

dot.edge('Comp', 'Mad', label='Materia estabilizada')
dot.edge('Mad', 'Emp', label='Compost fino')

# Flujos de salida
dot.edge('Emp', 'Out_Com')
dot.edge('Comp', 'Out_Gas')
dot.edge('Mad', 'Out_Rec')

# Guardar y mostrar
dot.render('caja_blanca_biocampus', view=True)
print("Diagrama generado como 'caja_blanca_biocampus.png'")