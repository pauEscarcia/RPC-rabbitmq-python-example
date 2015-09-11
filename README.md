# RPC-rabbitmq-python-example

Requerimientos
1.- python 2.7
2.- RabbitMQ 3.5.4
3.- SQLite

Instrucciones 
1.-Arrancar el servicio de RabbitMQ (https://www.rabbitmq.com/man/rabbitmq-server.1.man.html), si se quiere ingresar desde un host remoto se tendrá que configurar el acceso (https://www.rabbitmq.com/man/rabbitmqctl.1.man.html#Access%20control).

2.-Arrancar el servidor RPC, ejecute el archivo rpcServer (# python rpcServer.py).

3.-Ejecute el cliente (# python rpcClient.py), enseguida ingrese el usuario (admin) y contraseña (admin), la aplicación les mostrará un menú en el cual usted podrá interactuar con el servidor de RPC.
