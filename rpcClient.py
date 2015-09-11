#!/usr/bin/env python
from cPickle import dumps, loads
import pika
import uuid
import base64
import getpass

#Un cliente envia una mesaje de peticion y el servidor responde con un mensaje 
class RpcClient(object):
    def __init__(self):
        #inciar conexion de manera local 
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='10.13.4.33',credentials = pika.PlainCredentials('job', 'job')))
        #self.connection = pika.BlockingConnection(pika.ConnectionParameters(
        #        host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
        
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

user = raw_input('Enter your user:')
password = getpass.getpass()
response = rpc.call_login(user, password)
if response is not None:
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
