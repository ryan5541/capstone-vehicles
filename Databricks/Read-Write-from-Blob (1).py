# Databricks notebook source
import os.path

# COMMAND ----------

# MAGIC %md
# MAGIC ## Understanding DBUTILS and Mnt points

# COMMAND ----------

# MAGIC %md 
# MAGIC 
# MAGIC ### Mount Point 1 through Oauth security

# COMMAND ----------

###### Mount Point 1 through Oauth security.
storageAccount = "gen10dbcdatalake"
storageContainer = "gen10-ramen"
clientSecret = "Cty8Q~AvEO_qC-MjvPvosYauiNsffOHKnMpj7cmd"
clientid = "2ca50102-5717-4373-b796-39d06568588d"
mount_point = "/mnt/ragamilo/ramenin" # the mount point will be unique to you
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

# MAGIC %md
# MAGIC 
# MAGIC ### Dbtools has a simulated OS Unix methods
# MAGIC 
# MAGIC * [Databricks Dbutils Documentation](https://docs.databricks.com/dev-tools/databricks-utils.html)

# COMMAND ----------

display(dbutils.fs.ls("/mnt/classtest/carsin"))

# COMMAND ----------

# MAGIC %fs
# MAGIC 
# MAGIC ls /mnt/tomseeber/detroit/20200906-20201006/

# COMMAND ----------

# MAGIC %md 
# MAGIC 
# MAGIC ### Read in file to Spark Data frame via Mount

# COMMAND ----------

df = spark.read.csv('/mnt/classtest/carsin/911_Calls_for_Service_(Last_30_Days).csv')
display(df)

# COMMAND ----------

# MAGIC %md 
# MAGIC 
# MAGIC ### Write in file to Spark Data frame via Mount

# COMMAND ----------

df4.write.mode('overwrite').csv('/mnt/classtest/carsout/output_folder')

# COMMAND ----------

# MAGIC %fs
# MAGIC 
# MAGIC ls /mnt/classtest/carsout/output_folder

# COMMAND ----------

# MAGIC %md 
# MAGIC 
# MAGIC ### Spark Write as one file

# COMMAND ----------

data_location = "/mnt/classtest/carsout/output_folder"

df.repartition(1)\
.write.format("com.databricks.spark.csv").mode("overwrite") \
.option("header", "true")\
.save(data_location)

# By spark still dumps this out as one file. 
files = dbutils.fs.ls(data_location)
csv_file = [x.path for x in files if x.path.endswith(".csv")][0]
print(csv_file)
dbutils.fs.mv(csv_file, data_location.rstrip('/') + ".csv")
dbutils.fs.rm(data_location, recurse = True)


# COMMAND ----------

# MAGIC %fs
# MAGIC 
# MAGIC ls /mnt/classtest/carsout