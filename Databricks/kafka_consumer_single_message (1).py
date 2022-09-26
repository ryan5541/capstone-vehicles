# Databricks notebook source
# MAGIC %md 
# MAGIC 
# MAGIC # Simple Kafka Consumer Example

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC ## Error Callback Functions

# COMMAND ----------

def error_cb(err):
    """ The error callback is used for generic client errors. These
        errors are generally to be considered informational as the client will
        automatically try to recover from all errors, and no extra action
        is typically required by the application.
        For this example however, we terminate the application if the client
        is unable to connect to any broker (_ALL_BROKERS_DOWN) and on
        authentication errors (_AUTHENTICATION). """

    print("Client error: {}".format(err))
    if err.code() == KafkaError._ALL_BROKERS_DOWN or \
       err.code() == KafkaError._AUTHENTICATION:
        # Any exception raised from this callback will be re-raised from the
        # triggering flush() or poll() call.
        raise KafkaException(err)


# COMMAND ----------

# MAGIC %md 
# MAGIC 
# MAGIC ### Helpful Links
# MAGIC 
# MAGIC * [Confluent's github repo](https://github.com/confluentinc/confluent-kafka-python) - Confluent's github repo of code examples for python Kafka examples, includes almost everything needed for core development with Kafka
# MAGIC * [Docstring Documentation](https://www.datacamp.com/community/tutorials/docstrings-python) - Comments on Page made in Docstring

# COMMAND ----------

# MAGIC %md
# MAGIC ## Kakfa Consumer Setup

# COMMAND ----------

from time import sleep
import uuid
from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
import json


#KAFKA variables, Move to the OS variables or configuration
# This will work in local Jupiter Notebook, but in a databrick, hiding config.py is tougher. 
confluentClusterName = "stage3talent"
confluentBootstrapServers = "pkc-ldvmy.centralus.azure.confluent.cloud:9092"
confluentTopicName = "DJUSAU"
schemaRegistryUrl = "https://psrc-gq7pv.westus2.azure.confluent.cloud"
confluentApiKey = "YHMHG7E54LJA55XZ"
confluentSecret = "/XYn+w3gHGMqpe9l0TWvA9FznMYNln2STI+dytyPqtZ9QktH0TbGXUqepEsJ/nR0"
confluentRegistryApiKey = "YHMHG7E54LJA55XZ"
confluentRegistrySecret = "/XYn+w3gHGMqpe9l0TWvA9FznMYNln2STI+dytyPqtZ9QktH0TbGXUqepEsJ/nR0"


#Kakfa Class Setup.
c = Consumer({
    'bootstrap.servers': confluentBootstrapServers,
    'sasl.mechanism': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': confluentApiKey,
    'sasl.password': confluentSecret,
    'group.id': str(uuid.uuid1()),  # this will create a new consumer group on each invocation.
    'auto.offset.reset': 'earliest',
    'error_cb': error_cb,
})

c.subscribe(['DJUSAU'])


# COMMAND ----------

# MAGIC %md
# MAGIC ## Simple Kakfa Consumer a Simple JSON message consume

# COMMAND ----------

# CONSUME 1 Message

aString = ""

msg = c.poll(timeout=1.0)
if msg is None:
    print("nothing")
elif msg.error():
    print("Consumer error: {}".format(msg.error()))
else:
    aString=json.loads('{}'.format(msg.value().decode('utf-8')))
    aString['timestamp'] = msg.timestamp()[1]


print(aString)

# COMMAND ----------

