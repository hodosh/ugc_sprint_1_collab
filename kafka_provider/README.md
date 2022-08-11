# Kafka

Простые клиенты продюсера и консьюмера Kafka, сделанные на основе [kafka-python](https://kafka-python.readthedocs.io/)

# KafkaProducer

Предназначен для отправки сообщений (в виде словаря) в kafka.

Параметры конструктора:

* _bootstrap_servers_: str,
    * обязательный параметр для подключения к серверам Kafka
* _topic_name_: str,
    * Название топика, с которым будет работать продюсер. Обязательный параметр.
    * При необходимости может быть изменен через свойство topic_name
* При необходимости можно расширить конфиг (принимаются через kwargs). Подробнее о параметрах [тут](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html).

Реализует методы:

* _**send_message**_ - отправляет сообщение в топик Kafka. Имеет параметры:
    * message - сообщение в формате словаря.
    * partition - номер партиции, в которую надо писать сообщение. Необязательный параметр.
* _**close**_ - метод закрывает соединение с kafka.

Пример использования:

1) базовый способ:

```
producer =  KafkaProducer(bootstrap_servers='localhost:9092', topic_name='test_topic')
producer.send_message(msg)
producer.close()
```

2) с менеджером контекста (закрывает соединение после завершения работы, вызывая метод _**close**_), наиболее
   предпочтительный:

```
with KafkaProducer(bootstrap_servers='localhost:9092', topic_name='test_topic') as producer:
    producer.send_message(msg)
```

# KafkaConsumer

Предназначен для чтения сообщений (в виде словаря) из kafka.

Параметры конструктора:

* _bootstrap_servers_: str,
    * обязательный параметр для подключения к серверам Kafka
* _topic_name_: str,
    * Название топика, с которым будет работать консьюмер. Обязательный параметр. При необходимости может быть изменен
      через свойство topic_name
* _group_id_: str = None,
    * имя группы, с которой будет работать консьюмер. Необязательный параметр.
* _auto_offset_reset_: str = 'latest',
    * Политика сброса смещения. Как правило, потребление начинается с самого раннего либо с самого позднего смещения. По
      умолчанию latest.
* _enable_auto_commit_: bool = False,
    * Параметр коммита сообщения после прочтения. По умолчанию False
* При необходимости можно расширить конфиг (принимаются через kwargs). Подробнее о параметрах [тут](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html).

Реализует методы:

* _**subscribe**_ - обязательный метод для чтения сообщений. Осуществляет подписку на топик. Имеет параметры:
    * offset - номер оффсета, с которого надо начать читать сообщения. Необязательный параметр.
    * partition - номер партиции, с которой надо начать читать. Обязательный параметр при использовании с offset.
* _**list_messages**_ - чтение сообщений из топика kafka. Возвращает генератор сообщений, считывания их с момента начала
  работы метода и до того момента, когда поток сообщений прекратится. Имеет параметры:
    * timeout_ms: int = 500 - таймаут ожидания новых сообщений в Kafka при выполнении запроса poll.
    * raw: bool = False - признак того, чтобы возвращать ConsumerRecord (raw) или только значения (value) сообщений. По
      умолчанию возвращаются только value.
* _**commit**_ - коммит сообщений. В качестве входного параметра сообщение в исходном виде (ConsumerRecord).
* _**close**_ - метод закрывает соединение с kafka.

Пример использования:

1) базовый способ:

```
consumer = KafkaConsumer(bootstrap_servers='localhost:9092', topic_name='test_topic')
consumer.subscribe()
msg_generator = list_messages(raw=True, timeout_ms=1000)
consumer.close()
```

2) с менеджером контекста (закрывает соединение после завершения работы, вызывая метод _**close**_), наиболее
   предпочтительный:

```
with KafkaConsumer(bootstrap_servers='localhost:9092', topic_name='test_topic') as consumer:
    consumer.subscribe()
    msg_generator = consumer.list_messages(raw=True, timeout_ms=1000)
```

3) с заданным оффсетом и партицией:

```
with KafkaConsumer(bootstrap_servers='localhost:9092', topic_name='test_topic') as consumer:
    consumer.subscribe(offset=115, partition=0)
    msg_generator = consumer.list_messages()
```
