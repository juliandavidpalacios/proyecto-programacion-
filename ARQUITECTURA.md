# Arquitectura del proyecto

Aplicación de escritorio (Tkinter) de finanzas personales construida con el
patrón **MVP** y un **modelo de dominio orientado a objetos** que se corresponde
1:1 con `diagram.puml`.

## Capas

```
screens/      VISTA        -> solo widgets y eventos, cero lógica
presenters/   PRESENTADOR  -> coordinación, Python puro (sin tkinter)
Models/       MODELO        -> reglas de aplicación + persistencia (Repository)
domain/       DOMINIO       -> objetos de negocio puros (el diagrama)
```

### Flujo de una acción (ejemplo: comprar un activo)

1. **Vista** `InvertirView`: el botón "COMPRAR" llama a `presenter.ejecutar_compra()`.
2. **Presentador** `InvertirPresenter`: valida la entrada y llama a
   `model.registrar_compra(...)`. No abre ficheros ni muestra popups.
3. **Modelo** `InvertirModel`: comprueba fondos, actualiza el portafolio, crea
   una **`Transaccion`** de dominio (`domain.Transaccion`) y la persiste usando
   `transaccion.a_linea_historial()`. Devuelve datos puros.
4. **Vista**: muestra el recibo con `mostrar_exito(...)`.

## Mapa diagrama ⇄ código

| Clase del diagrama | Archivo | Usada por |
|--------------------|---------|-----------|
| `Usuario` | `domain/usuario.py` | `UsuarioRepository` / `LoginModel` |
| `CuentaBancaria` | `domain/cuenta_bancaria.py` | `AhorrosModel.calcular_resumen`, agregado de `Usuario` |
| `Portafolio` | `domain/portafolio.py` | `AhorrosModel` |
| `Posicion` | `domain/posicion.py` | `Portafolio` |
| `Accion` | `domain/accion.py` | `Posicion`, `Portafolio` |
| `CotizacionHistorica` | `domain/cotizacion_historica.py` | `ProveedorAPI` |
| `Transaccion` | `domain/transaccion.py` | `InvertirModel` |
| `ProveedorAPI` (interfaz) | `domain/proveedor_api.py` | `Portafolio`, modelos |
| `YahooFinanceProveedor` | `domain/yahoo_finance.py` | implementa `ProveedorAPI` |
| `CompraInstitucional` | `domain/compra_institucional.py` | `ExpertosModel` |
| `InversorInstitucional` | `domain/inversor_institucional.py` | `ExpertosModel` |
| `ProveedorExpertos` (interfaz) | `domain/proveedor_expertos.py` | `ExpertosModel` |
| `YahooExpertosProveedor` | `domain/yahoo_expertos.py` | implementa `ProveedorExpertos` |
| `TipoTransaccion`, `IntervaloTiempo` | `domain/enums.py` | dominio |

### Pantalla de Expertos

`screens/expertos.py` + `presenters/expertos_p.py` + `Models/expertos_m.py`
muestran las acciones que los grandes inversores institucionales (Berkshire,
Vanguard, BlackRock…) han **comprado** (aumentado en cartera) durante el último
trimestre. El `ExpertosModel` no sabe de dónde salen los datos: depende de la
interfaz `ProveedorExpertos`, implementada por `YahooExpertosProveedor`
(Adapter sobre `yfinance.Ticker.institutional_holders`, con datos de ejemplo de
respaldo si no hay conexión). Sustituye a la antigua pantalla de Gastos.

## Reglas de oro (para mantener MVP estricto)

- Un archivo de `presenters/` **nunca** importa `tkinter`/`messagebox`.
- Una clase de `screens/` **nunca** hace cálculos de negocio ni accede a disco.
- El acceso a ficheros vive en los `*Repository` o en los `*Model`.
- El dominio (`domain/`) **no** depende de Tkinter ni de pandas/yfinance
  (la dependencia de yfinance es perezosa, solo dentro de `YahooFinanceProveedor`).

Ver `PATRONES.md` para la justificación de cada patrón de diseño.
