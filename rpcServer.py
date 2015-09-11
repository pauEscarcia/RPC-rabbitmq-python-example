#!/usr/bin/env python
# coding=utf-8
from cPickle import dumps, loads
import pika
import os
import base64
import sqlite3
import time

#Realiza la conexion de manera remota al host, esto puede ser modificado asi como a las credenciales
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost',credentials = pika.PlainCredentials('usuario', 'password')))


#creamos loa canales de conexión para RabbitMQ
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')
channel.queue_declare(queue='rpc_queue_login')
channel.queue_declare(queue='rpc_queue_download')

#Metodo para establecer conexión y regresar una llave para accesos
def login(usuario,password):
    #establece conexión
    conn = sqlite3.connect('users.sqlite')
    c = conn.cursor()
    #revisamos si existe un usuario con los parametros dados
    c.execute("SELECT * FROM users WHERE user=? and password = ?",(usuario, password))  
    row = c.fetchone()
    conn.commit()
    llave = None
    #si existe el usuario generamos una llave con el id del usuario y la hora actual
    if row is not None:        
        llave = base64.b64encode(str(row[0])+time.strftime("%H:%M:%S"))
        #actualizamos la llave en el registro del usuario
        c.execute("UPDATE users set key=? where id = ?",(llave, row[0]))
        conn.commit()   
    conn.close()
    return llave

#Metodo que lista todos los archivos con la extension .py en la ruta especifica del directorio 
def archivos (n):
    #Variable para la ruta al directorio
    #path = 'C:\' #Cambiar si se esta usando windows
    path ='/'    #Cambiar la ruta 

    #Lista vacia para incluir los ficheros
    lstFiles = []
    #Lista con todos los ficheros del directorio:
    lstDir = os.walk(path)   #os.walk()Lista directorios y ficheros
    #Crea una lista de los ficheros py que existen en el directorio y los incluye a la lista.
    for root, dirs, files in lstDir:
        for fichero in files:
            (nombreFichero, extension) = os.path.splitext(fichero)
            if(extension == ".py"):
                lstFiles.append(nombreFichero+extension)
                print (nombreFichero+extension)
    print(lstFiles)
    return lstFiles

#Metodo que regresa el archivo a descargar, primero lo serializa y regresa una lista con el contenido al cliente
def SerFile(nom):
    #path = 'C:\'    #Cambiar si se esta usando windows
    path = '/'#Cambiar la ruta 
    arch = open(path+nom,'r')
    lineas = arch.readlines()
    arch.close()
    ser = dumps(lineas)
    return ser

#Por cada metodo debemos crear un request para dirigir la petición del cliente

#metodo de respuesta hacia el cliete de listado de archivos
def on_request(ch, method, props, body):
    n = int(body)
    print " [.] Envio(%s)"  % (n,)
    
    response = archivos(n)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

#metodo de respuesta hacia el cliete de login
def on_request_login(ch, method, props, body):
    n = body    
    credencial = n.split(',')    
    response = login(credencial[0], credencial[1])
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

#metodo de respuesta hacia el cielnte para descargar archivos
def on_request_download(ch, method, props, body):
    n = body     
    response = SerFile(n)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

#Creamos el mapeo de canales y metodos de respuesta para RabbitMQ
channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')
channel.basic_consume(on_request_login, queue='rpc_queue_login')
channel.basic_consume(on_request_download, queue='rpc_queue_download')

#Imprimimos el consumo de metodos en nuestro server
print " [x] Esperando por peticiones RPC"
channel.start_consuming()
