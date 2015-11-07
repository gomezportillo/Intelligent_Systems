Arges
=====

Repositorio de código fuente del proyecto Arges (CTED)

Generación de ejecutable (.exe)
-------------------------------

1. Clonar el repositorio.
2. Descargar las [dependencias](https://bitbucket.org/ctedfantasticteam/arges/downloads/redist.zip) desde el repositorio.
3. Descomprimir las dependencias en `arges/` quedando como `arges/redist/{avconv, sox, lame, blender}`.
4. Descargar e instalar [pyinstaller](https://github.com/pyinstaller/pyinstaller/wiki) (depende de [pywin32](http://sourceforge.net/projects/pywin32/)).
5. Ejecutar el script `arges/build_exe.bat`.
6. Ejecutar el script de InnoSetup `arges/build_installer.iss`.
7. El directorio `arges/Output` contiene el instalador de Arges.