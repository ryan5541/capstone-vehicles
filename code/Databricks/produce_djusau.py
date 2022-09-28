# Databricks notebook source
#%pip install bs4
#%pip install requests

# COMMAND ----------

from bs4 import BeautifulSoup
import requests
from datetime import datetime
import time

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

from confluent_kafka import Consumer
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
p = Producer({
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

## Simple Producer with JSON message. 
#dict_list = []
for i in range(6):
#while True:
    row_dict = {}
    response = requests.get('https://www.google.com/finance/quote/DJUSAU:INDEXDJX?sa=X&ved=2ahUKEwi_oaSkwab6AhV3EVkFHf-mDLIQ3ecFegQIBBAY')
    html = BeautifulSoup(response.text, 'html.parser')
    price = float(html.find('div', attrs = {'class': 'YMlKec fxKbKc'}).text.replace(',',''))
    row_dict['price'] = price
    row_dict['time'] = datetime.strftime(datetime.now(), '%x %X')
    #print(f"Price: {row_dict['price']}, Timestamp: {row_dict['time']}")
    aDict = row_dict
    
    ## Clarification on p.produce
    # produce ( topic, message in JSON)
    p.produce(confluentTopicName,json.dumps(aDict))
    p.flush()
    time.sleep(10)

# COMMAND ----------

