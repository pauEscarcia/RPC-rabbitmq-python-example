# RPC-rabbitmq-python-example

Requerimientos
1.- python 2.7
2.- RabbitMQ 3.5.4
3.- SQLite

Instrucciones para ejecución 
1.-El arranque del servicio RabbitMQ varia según el sistema operativo para mas información visita la pagina https://www.rabbitmq.com/man/rabbitmq-server.1.man.html.

Ejemplo en Mac OS X:
dentro de una consola ingresa a
# cd rabbitmq_server-3.5.4/sbin/

ejecuta el archivo 
# rabbitmq-server

Nota: si se quiere ingresar desde un host remoto se tendrá que configurar el acceso (https://www.rabbitmq.com/man/rabbitmqctl.1.man.html#Access%20control).

2.-Arrancar el servidor RPC, dentro de una consola ejecute el archivo rpcServer.py
# python rpcServer.py

Nota:
Por default la ruta de los archivos a mostrar es /, si se esta en un sistema operativo windows abrá que modificarla a c:\, para modificar la ruta edita las lineas 44 y 63 del archivo rpcServer.py

3.-Ejecute el cliente, dentro de una consola ejecute el archivo rpcClient.py
# python rpcClient.py)

enseguida ingrese el usuario (admin) y contraseña (admin), la aplicación les mostrará un menú en el cual usted podrá interactuar con el servidor de RPC.
Nota: los archivos que se muestran en la opción 1 deben de tener extensión .py, para mdificar la extensión de los archivos que queremos visualiar y descargar edita la línea 54 del archivo rpcServer.py
