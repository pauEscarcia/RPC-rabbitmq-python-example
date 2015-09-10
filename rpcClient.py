#!/usr/bin/env python
import pika
import uuid

#Un cliente envia una mesaje de peticion y el servidor responde con un mensaje 
class FibonacciRpcClient(object):
    def __init__(self):
        #inciar conexion de manera local 
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='10.13.4.33',credentials = pika.PlainCredentials('job', 'job'))) #192.168.1.87  10.13.4.33

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

fibonacci_rpc = FibonacciRpcClient()

#doll = int(raw_input('Introduzca la cantidad en Dolares: '))
#print " [x] Convirtiendo  Dolares"
response = fibonacci_rpc.call(2)
print " [.] Archivos a descargar %r" % (response,)

