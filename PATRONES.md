# Patrones de Diseño aplicados

Este documento justifica los patrones de diseño usados en el proyecto: **qué
problema concreto resolvía cada uno** y **por qué se eligió**.

---

## 1. MVP (Model–View–Presenter) — patrón arquitectónico principal

**Problema que resuelve.** En la versión inicial la lógica de negocio, los
cálculos y el acceso a archivos estaban mezclados dentro de las pantallas de
Tkinter ("arquitectura espagueti"). Eso hacía imposible probar la lógica sin
abrir la ventana y duplicaba reglas por toda la app.

**Cómo se aplica.**
- **Vista** (`screens/`): solo construye widgets, captura eventos y *pinta* lo
  que se le ordena. No hace cálculos ni decide nada. Expone métodos limpios
  (`poblar_campos`, `mostrar_error`, `pintar_activo`, `actualizar_totales`...).
- **Presentador** (`presenters/`): es **Python puro, sin `import tkinter`**.
  Coordina los eventos, aplica reglas que dependen de la interacción y traduce
  resultados a llamadas de la vista. No conoce widgets concretos.
- **Modelo** (`Models/` + `domain/`): reglas de negocio y persistencia.

> Verificación: ningún archivo de `presenters/` importa `tkinter` ni
> `messagebox`. Los diálogos los decide la vista (`mostrar_error`, etc.).

---

## 2. Repository — acceso a datos

**Problema que resuelve.** El sistema guarda los usuarios como carpetas con un
`perfil.txt`. Si cada modelo abriera ficheros a mano, el formato de
almacenamiento quedaría disperso e imposible de cambiar.

**Cómo se aplica.** `UsuarioRepository` (en `Models/login_m.py`) y
`RegistroRepository` (en `Models/registro_m.py`) son los **únicos** que conocen
rutas y ficheros. Traducen texto plano ⇄ objetos de dominio `Usuario`. Si
mañana migramos a una base de datos SQL, solo cambia el repositorio.

---

## 3. Strategy + Inversión de Dependencias — `ProveedorAPI`

**Problema que resuelve.** Los precios venían de llamadas a `yfinance`
repartidas por cuatro modelos distintos. Eso acoplaba la lógica financiera a una
librería externa concreta e impedía hacer pruebas sin conexión a internet.

**Cómo se aplica.** `ProveedorAPI` (en `domain/proveedor_api.py`) es una
**interfaz abstracta** (`abc.ABC`). `Portafolio` y los modelos dependen de esa
abstracción, no de Yahoo Finance. El proveedor se **inyecta por constructor**:

```python
portafolio = Portafolio(proveedor=YahooFinanceProveedor())
```

Así se puede sustituir por un proveedor simulado en tests sin tocar el dominio.

---

## 4. Adapter — `YahooFinanceProveedor`

**Problema que resuelve.** `yfinance` devuelve `DataFrame` de pandas con un
formato complejo (MultiIndex, sufijos `-EUR` para cripto, columnas `Close`...).
El dominio no debería conocer pandas.

**Cómo se aplica.** `YahooFinanceProveedor` (en `domain/yahoo_finance.py`)
*adapta* esa interfaz externa al contrato limpio `ProveedorAPI`
(`obtener_precio_actual`, `obtener_serie_de_tiempo`), traduciendo símbolos y
DataFrames a `float` y a objetos `CotizacionHistorica`.

---

## 5. Value Object / Encapsulamiento

`CotizacionHistorica` y `Transaccion` son objetos inmutables con atributos
privados (`__atributo`) expuestos solo por propiedades de lectura. Esto evita
estados inconsistentes y deja claro qué datos son de solo lectura.

---

## Resumen

| Patrón | Dónde | Problema que resuelve |
|--------|-------|-----------------------|
| MVP | `screens/` + `presenters/` + `Models/` | Separar UI, coordinación y negocio |
| Repository | `*Repository` en `Models/` | Aislar el acceso a ficheros |
| Strategy + DI | `ProveedorAPI` | Desacoplar la fuente de precios |
| Adapter | `YahooFinanceProveedor` | Traducir `yfinance`/pandas al dominio |
| Value Object | `CotizacionHistorica`, `Transaccion` | Inmutabilidad y encapsulamiento |
