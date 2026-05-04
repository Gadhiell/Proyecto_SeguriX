# SeguriX

## Logo de SeguriX
<img width="450" height="450" alt="image" src="https://github.com/user-attachments/assets/4917e1f9-e6be-4ad6-a144-f115df95885f" />

## Descripción
**SeguriX** es una plataforma centralizada diseñada para la administración de seguridad en edificios corporativos y residenciales.  
Su propósito es registrar y gestionar los flujos de entrada y salida de distintos tipos de usuarios (empleados, residentes, visitas, proveedores), ofreciendo una visión clara y confiable del acceso en tiempo real.

## Motivación
El principal desafío que aborda SeguriX es la **heterogeneidad de los datos**: los registros provienen de múltiples métodos de identificación (QR, biometría, tarjetas RFID), cada uno con estructuras incompatibles.  
El objetivo es **unificar esta información** en una vista de auditoría coherente y escalable, asegurando que el sistema pueda incorporar nuevas tecnologías sin comprometer su estabilidad.

## Estado del proyecto
Actualmente, SeguriX se encuentra en ouna fase **muy inicial de diseño**.  
Existe muy poco código implementado; ya que el trabajo se centro en definir la arquitectura, los módulos principales y las estrategias técnicas que permitirán construir una solución robusta y extensible.

## Objetivo general
Construir una plataforma que:
- Centralice la administración de accesos.
- Procese datos heterogéneos de distintos dispositivos.
- Permita escalar y adaptarse a nuevas tecnologías.
- Ofrezca herramientas de auditoría y control en tiempo real.

## ¿Por qué se usa Flask?
Se utiliza **Flask** porque permite crear un servidor web de forma simple.

En este proyecto Flask se encarga de:
- Recibir datos desde el frontend  
- Procesar accesos (`/acceso`)  
- Entregar logs (`/logs`)  
- Mostrar las páginas HTML  

---

## Módulos principales
- app.py : crea y ejecuta la aplicación
- routes : maneja las rutas (API)
- services : contiene la lógica
- data : almacena los datos


## Paleta de colores utilizada
<img width="889" height="268" alt="image" src="https://github.com/user-attachments/assets/a4cf1b00-bc65-493e-9e13-49d9c1d88889" />



## Kit tecnológico utilizado
<img width="551" height="339" alt="image" src="https://github.com/user-attachments/assets/5ea8f750-c54a-4a89-834f-3c61db45de1c" />



## **Diagrama UML**
<img width="1213" height="812" alt="imagen_2026-04-27_150646923" src="https://github.com/user-attachments/assets/fa0b88f9-fc81-40f2-b40d-5ff785529d89" />


## ▶️ Ejecución

```bash
cd C:\Users\suprr\Documents\Proyecto_SeguriX
python app.py

//Luego abrir en el navegador:

http://localhost:5000/




