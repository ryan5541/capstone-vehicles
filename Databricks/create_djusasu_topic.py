# Databricks notebook source
# MAGIC %md 
# MAGIC 
# MAGIC # Simple Kafka Topics Example

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


def acked(err, msg):
    """ 
        Error callback is used for generic issues for producer errors. 
        
        Parameters:
            err (err): Error flag.
            msg (str): Error message that was part of the callback.
    """
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

# COMMAND ----------

# MAGIC %md 
# MAGIC 
# MAGIC ### Helpful Links
# MAGIC 
# MAGIC * [Confluent's github repo](https://github.com/confluentinc/confluent-kafka-python) - Confluent's github repo of code examples for python Kafka examples, includes almost everything needed for core development with Kafka
# MAGIC * [Docstring Documentation](https://www.datacamp.com/community/tutorials/docstrings-python) - Comments on Page made in Docstring

# COMMAND ----------

# MAGIC %md 
# MAGIC 
# MAGIC ## Connection Strings for our environment and imports

# COMMAND ----------

#DO NOT DELETE THIS
from confluent_kafka import Consumer
from time import sleep
import uuid
from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
import json
from confluent_kafka.admin import AdminClient, NewTopic


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



# COMMAND ----------

# MAGIC %md
# MAGIC ## Kakfa Admin Setup

# COMMAND ----------

admin_client = AdminClient({
    'bootstrap.servers': confluentBootstrapServers,
    'sasl.mechanism': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': confluentApiKey,
    'sasl.password': confluentSecret,
    'group.id': str(uuid.uuid1()),  # this will create a new consumer group on each invocation.
    'auto.offset.reset': 'earliest',
    'error_cb': error_cb,
})


# COMMAND ----------

# MAGIC %md 
# MAGIC 
# MAGIC 
# MAGIC ## Simple Kakfa Topics Creator

# COMMAND ----------

topic_list = []

topic_list.append(NewTopic(confluentTopicName, 1, 3))
futures = admin_client.create_topics(topic_list)


try:
    record_metadata = []
    for k, future in futures.items():
        # f = i.get(timeout=10)
        print(f"type(k): {type(k)}")
        print(f"type(v): {type(future)}")
        print(future.result())

except KafkaError:
    # Decide what to do if produce request failed...
    print(traceback.format_exc())
    result = 'Fail'
finally:
    print("finally")




# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC The create_topics method does not actually run the creation of the topic.   It sets up the a topic object and then the topic.result ( or in this case future.result) actually runs it.  This example lets you bulk load topics to kafka

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC ## Delete a topic

# COMMAND ----------

#topic_list.append(NewTopic("example_topic", 1, 3))
#admin_client.create_topics(topic_list)
#futures = admin_client.create_topics(topic_list)

# parameter: topics = list of string topics, timeout
try:
    topics =['test']
    fs = admin_client.delete_topics(topics, request_timeout=30)
    
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print("Topic {} deleted".format(topic))
        except Exception as e:
            print("Failed to delete topic {}: {}".format(topic, e))
    
except Exception as e:
    print(e)

