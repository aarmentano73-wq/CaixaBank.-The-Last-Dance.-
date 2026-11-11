# CaixaBank.-Un mundo detrás de la estrella.-
Análisis de CaixaBank entre 2007 y 2025 con datos del banco, INE, Banco de España y BCE y propias fuentes de CaixaBank

# CaixaBank en Power BI: estructura, ingresos y ciclo económico

> **Estado del proyecto: en desarrollo.** Esta es una primera versión. Quedan por explorar muchas más líneas de análisis (ver [Próximos pasos](#próximos-pasos)).

## Objetivo

Analizar la evolución y la estructura de **CaixaBank** entre 2007 y 2025, combinando datos propios del banco con indicadores económicos de España y Europa. El proyecto busca responder a tres preguntas:

1. ¿Cómo es el banco hoy (plantilla, red, clientes, costes)?
2. ¿De dónde vienen sus ingresos y cómo ha cambiado su reparto?
3. ¿Hasta qué punto depende su negocio del ciclo económico?

## Contenido del informe

### 1. Contexto 2025
Radiografía del banco: plantilla total y reparto entre hombres y mujeres, oficinas, cajeros, número de clientes y coste de personal anual. Todo en tarjetas, con las cifras monetarias en millones de euros (M€).

### 2. Ingresos operativos
Los **12.419 M€** ingresados en 2025 se descomponen en:

- Margen de intereses
- Comisiones netas
- Resultado de operaciones financieras (ROF)
- Otros ingresos de explotación

Incluye un **gráfico de cascada** con la composición del total en 2025 y un **gráfico de columnas apiladas al 100 %** que compara el peso de cada fuente entre 2021 y 2025.

### 3. Tendencia en ciclos económicos
**Gráfico de dispersión** que relaciona el crecimiento del PIB de España con el crecimiento interanual de los ingresos del banco. Cada punto es un año; el color indica la fase del ciclo (crisis 2008-2013, recuperación, Covid y post-covid) y el tamaño refleja el volumen de ingresos. El año 2021 se anota aparte porque su salto responde a la integración de Bankia.

## Conclusiones preliminares

- El margen de intereses aporta cerca del **86 %** de los ingresos y ha ganado peso desde 2021, por lo que el banco es más sensible a la evolución de los tipos de interés.
- Las comisiones son la segunda fuente (**11,2 %**); el ROF y otros ingresos tienen un peso marginal.
- La relación entre PIB e ingresos del banco parece **débil**: los ingresos crecen incluso en años de PIB negativo (crisis y Covid).
- El salto de **2021 (+58 %)** se debe a la integración de Bankia, no al ciclo económico.

> Son correlaciones observadas con pocos datos anuales; no demuestran causalidad.

## Datos y modelo

**Fuentes** (según las tablas del modelo):

- Informes y datos de resultados de CaixaBank (ingresos, gastos, provisiones, balances).
- Información no financiera del banco (EINF): clientes, cuotas de mercado, personal y obra social.
- INE: paro.
- Banco de España: ratios del sector.
- BCE / Eurostat: comparativa España frente a la eurozona (PIB, inflación, paro, prima de riesgo).

**Modelo:** esquema en estrella con una tabla `Calendario` como eje común. Las tablas de hechos se relacionan con ella en sentido uno a varios, lo que permite filtrar todo con un único año y cruzar datos del banco con datos macroeconómicos.

## Técnicas utilizadas

- Limpieza y transformación de datos con Power Query.
- Medidas DAX: variación interanual, composición porcentual, saldos con `LASTDATE`, `REMOVEFILTERS` y formato dinámico.
- Columnas calculadas (por ejemplo, la fase del ciclo económico).
- Visualizaciones: tarjetas, cascada, columnas apiladas, dispersión con leyenda y tamaño.
- Diseño coherente con la identidad del banco: fondo oscuro, paleta azul y amarillo y unidades siempre en M€.

## Próximos pasos

- Conseguir el desglose del crédito por tipo y construir la página de crédito con su evolución temporal.
- Analizar la relación entre **paro, provisiones y morosidad** (coste del riesgo).
- Comparar a CaixaBank con el **sector** usando los ratios del Banco de España.
- Estudiar el efecto de los **tipos de interés** sobre el margen de intereses.
- Añadir KPIs de eficiencia (ratio de eficiencia, ingresos por empleado, coste de personal sobre ingresos).
- Incorporar selector de año y variación interanual en las tarjetas.
- Analizar el efecto de la integración de Bankia con más detalle.



