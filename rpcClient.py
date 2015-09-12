#!/usr/bin/env python
# coding=utf-8
from cPickle import dumps, loads
import pika
import uuid
import base64
import getpass

#Un cliente envia una mesaje de peticion y el servidor responde con un mensaje 
class RpcClient(object):
    #creamos el metodo inicializador de nuestra clase el cual contiene la conexión a RabbirMQ
    def __init__(self):
        # inciar conexion de manera remota
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)
    #Metodo de respuesta RabbitMQ
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
    #Metodo para hacer peticiones al metodo de listado de archivos en el server
    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response #regresa la respuesta del server
    #Metodo para hacer peticiones al metodo de login en el server
    def call_login(self, user, password ):
        self.response = None
        password = base64.b64encode(password)
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue_login',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=user+","+password)
        while self.response is None:
            self.connection.process_data_events()
        return self.response 
    #Metodo para hacer peticiones al metodo de descarga en el server
    def call_download(self, filename):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue_download',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=filename)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

rpc = RpcClient()
# Menu de opciones y peticiones al server
user = raw_input('Enter your user:')
password = getpass.getpass()
response = rpc.call_login(user, password)
if response != 'None':
    menu = {}
    menu['1']="List files." 
    menu['2']="Dowload file."    
    menu['3']="Exit"
    while True:
        options=menu.keys()
        options.sort()
        for entry in options:
            print entry, menu[entry]
        selection=raw_input("Please Select:")
        if selection == '1':
            response = rpc.call(2)
            print " [.] Archivos a descargar %r" % (response)
        elif selection == '2':
            archivo = raw_input('Enter the file:')
            response = rpc.call_download(archivo)
            dec = loads(response)
            ar = open(archivo,'w')
            for li in dec:
                ar.write(li)
            ar.close()
            print "File downloaded successfully."
        elif selection == '3':
            break
        else:
            print "Unknown Option Selected!"    
else:
    print 'Error in user or password'
