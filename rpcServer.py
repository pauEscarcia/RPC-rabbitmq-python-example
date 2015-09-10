#!/usr/bin/env python
import pika
import os

#Realiza la conexion de manera local  
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='10.13.4.33',credentials = pika.PlainCredentials('job', 'job')))

channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

#Metodo para establecer conexion 
def login(usuario,password):
    conn = sqlite3.connect('users.sqlite')
    c = conn.cursor()   
    c.execute("SELECT * FROM users WHERE user=? and password = ?",(usuario, password))  
    row = c.fetchone()
    conn.commit()
    if row is not None:
        print row
        
    conn.close()

#Metodo que lista todos los archivos con la extension .py en la ruta especifica del directorio 
def archivos (n):
    #Variable para la ruta al directorio
    path = 'C:\Users\Master PC\Documents\RPC-rabbitmq-python-example'
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
    #print ('LISTADO FINALIZADO')
    #print "longitud de la lista = ", len(lstFiles)
    return lstFiles

#metodo que realiza la converision de pesos a dolares 
#def fib(n):
#    return n * 16.97  #fib(n-1) + fib(n-2)

#metodo de respuesta hacia el cliete
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

print " [x] Esperando por peticiones RPC"
channel.start_consuming()
