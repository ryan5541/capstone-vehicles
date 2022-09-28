# Databricks notebook source
# MAGIC %md 
# MAGIC 
# MAGIC # Simple Kafka Consumer All Messages Example

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

#from confluent_kafka import Consumer
from time import sleep
import uuid
from confluent_kafka import Producer, Consumer, KafkaError, KafkaException, TopicPartition
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
    'group.id': 'group1place',  # this will create a new consumer group on each invocation.
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True,
    'error_cb': error_cb,
})

c.subscribe([confluentTopicName])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Simple Kakfa Consumer a Simple JSON message consume

# COMMAND ----------

# CONSUME 1 Message

aString = {}

kafkaListDictionaries = []

for i in range(1000):
#while True:
    try:
        msg = c.poll(timeout=1.0)
        #print(msg.offset())
        if msg is None:
            break
            #pass
        elif msg.error():
            print("Consumer error: {}".format(msg.error()))
            break
        else:
            aString=json.loads('{}'.format(msg.value().decode('utf-8')))
            aString['timestamp'] = msg.timestamp()[1]
            kafkaListDictionaries.append(aString)
            c.commit()
            
    except Exception as e:
        print(e)

for message in kafkaListDictionaries:
    print(message)
#print(msg.offset())

# COMMAND ----------

kafkaListDictionaries

# COMMAND ----------

df = spark.createDataFrame(kafkaListDictionaries)
df.display()

# COMMAND ----------

###### Mount Point 1 through Oauth security.
storageAccount = "gen10datafund2207"
storageContainer = "jazztrio"
clientSecret = "Cty8Q~AvEO_qC-MjvPvosYauiNsffOHKnMpj7cmd"
clientid = "2ca50102-5717-4373-b796-39d06568588d"
mount_point = "/mnt/jazztrio/datain" # the mount point will be unique to you
#20200906-20201006/Detroit911-20200906-20201006.csv 


configs = {"fs.azure.account.auth.type": "OAuth",
       "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
       "fs.azure.account.oauth2.client.id": clientid,
       "fs.azure.account.oauth2.client.secret": clientSecret,
       "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/d46b54b2-a652-420b-aa5a-2ef7f8fc706e/oauth2/token",
       "fs.azure.createRemoteFileSystemDuringInitialization": "true"}

try: 
    dbutils.fs.unmount(mount_point)
except:
    pass

dbutils.fs.mount(
source = "abfss://"+storageContainer+"@"+storageAccount+".dfs.core.windows.net/",
mount_point = mount_point,
extra_configs = configs)

# COMMAND ----------

#This is purely for backup purposes, since we write directly to the database...

data_location = "/mnt/jazztrio/datain/Cleaned/"

#df.repartition(1).write.csv(path=f"{data_location}djusau.csv", mode="append")

df.repartition(1)\
.write.format("com.databricks.spark.csv").mode("append") \
.option("header", "true")\
.save(data_location)

# # By spark still dumps this out as one file. 
# files = dbutils.fs.ls(data_location)
# csv_file = [x.path for x in files if x.path.endswith(".csv")][0]
# print(csv_file)
# dbutils.fs.mv(csv_file, data_location.rstrip('/') + ".csv")
# dbutils.fs.rm(data_location, recurse = True)


# COMMAND ----------

database = "JazzTrio"
table = "dbo.DJUSAU"
user = "jazztrio"
password  = "YaLikeJazz!?123"
server = "gen10-data-fundamentals-22-07-sql-server.database.windows.net"

# COMMAND ----------

df.write.format('jdbc').option("url", f"jdbc:sqlserver://{server}:1433;databaseName={database};") \
    .mode("append") \
    .option("dbtable", table) \
    .option("user", user) \
    .option("password", password) \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .save()