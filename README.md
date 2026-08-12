# Docking Reference Audit

**Estado:** auditoría estructural y subpilotos estrictos en curso; resultados
descriptivos reproducibles, sin conclusiones de rendimiento, afinidad o
actividad biológica.

Proyecto independiente para construir un conjunto curado de complejos proteína–ligando de acceso público y auditar su preparación para campañas de redocking reproducibles. No utiliza entradas, estructuras ni resultados del proyecto doctoral.

## Pregunta de investigación

¿Qué condiciones documentables de procedencia, estructura, composición y preparación permiten decidir si un complejo público es apto para un experimento de redocking de referencia?

## Producto previsto

- un conjunto de casos y un manifiesto versionado;
- scripts que descargan, verifican y registran cada entrada;
- informes por caso, incluidos motivos explícitos de exclusión;
- figuras y tablas generadas desde los manifiestos;
- depósito reproducible (repositorio + Zenodo) antes de cualquier manuscrito.

El objetivo no es afirmar que una herramienta es superior ni extrapolar eficacia farmacológica. Los resultados son descriptivos y reproducibles, limitados a los casos que cumplan el protocolo. Las preparaciones rechazadas bajo una política congelada también se conservan como resultados.

## Estructura

```text
protocol/       criterios, decisiones y registro de cambios
data/           manifiestos CSV/JSON; nunca resultados sin procedencia
scripts/        recuperación, auditoría y generación de informes
reports/        salidas derivadas y trazables
```

## Fuente primaria

Las estructuras y sus metadatos se recuperarán exclusivamente desde RCSB PDB/wwPDB mediante identificadores y URLs registradas. Cada caso conservará checksum, fecha de recuperación, formato, método experimental y referencia al informe de validación.

## Regla de integridad

No se incorporará a un resultado un número, pose, clasificación o figura que no pueda regenerarse desde los archivos y scripts versionados. Las exclusiones son resultados válidos y se conservarán.

Consulte [el protocolo inicial](protocol/PROTOCOL-v0.1.md) antes de añadir casos.
La expansión controlada se describe en [EXPANSION-PLAN-v0.1.md](protocol/EXPANSION-PLAN-v0.1.md); los resultados actuales del subpiloto están en [SUBPILOT-RESULTS-v0.1.md](reports/SUBPILOT-RESULTS-v0.1.md).
