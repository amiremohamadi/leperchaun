'''to receive domains from rabbitmq. it is blocking, so always use it as the starter job'''

from interface import Job
import pika


class RabbitmqJob(Job):

    def __repr__(self):
        return 'rabbitmq'

    def _run(self):
        conn = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        chan = conn.channel()
        chan.exchange_declare(exchange='domains', exchange_type='fanout')

        result = chan.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        chan.queue_bind(exchange='logs', queue=queue_name)

        chan.basic_consume(queue=queue_name,
                           on_message_callback=self.call_back,
                           auto_ack=True)
        chan.start_consuming()

    def call_back(self, channel, method, prop, body):
        print(body)
        self.pipe(body.decode())
