# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC # Create your database in Azure portal in your Azure Dabase server.

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC # Connect via Admin to database server
# MAGIC 
# MAGIC Password: IWantToBeADataScientist123!@#
# MAGIC 
# MAGIC User: gen10dbadmin
# MAGIC 
# MAGIC Hostname:  gen10-data-fundamentals-22-07-sql-server.database.windows.net

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC --Select Master DB:
# MAGIC USE Master;
# MAGIC 
# MAGIC --create User and Passord for Database Server
# MAGIC CREATE LOGIN <YOUR USER>
# MAGIC WITH PASSWORD = '<Strong_Password_Goes_Here>';
# MAGIC 
# MAGIC 
# MAGIC --Select your DB:
# MAGIC USE <Your-DB>;
# MAGIC --Tie Account to Particular database:
# MAGIC CREATE USER [Your-User]
# MAGIC FROM LOGIN [Your-User ]
# MAGIC WITH DEFAULT_SCHEMA=dbo;
# MAGIC 
# MAGIC -- add user to database role(s) (i.e. db_owner)
# MAGIC ALTER ROLE db_owner ADD MEMBER [YOUR-DB];

# COMMAND ----------

# MAGIC %md
# MAGIC ## Database variables 

# COMMAND ----------

database = "JazzTrio"
table = "dbo.tomRamen"
user = "rgamilo"
password  = "a1ntN0b0dy"
server = "gen10-data-fundamentals-22-07-sql-server.database.windows.net"

# COMMAND ----------

# MAGIC %md 
# MAGIC ## Read Data from Database

# COMMAND ----------

print(f"jdbc:sqlserver://{server}:1433;databaseName={database}")

# COMMAND ----------

#read table data into a spark dataframe
jdbcDF = spark.read.format("jdbc") \
    .option("url", f"jdbc:sqlserver://{server}:1433;databaseName={database};") \
    .option("dbtable", table) \
    .option("user", user) \
    .option("password", password) \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .load()
 
#show the data loaded into dataframe
jdbcDF.show()

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

df = spark.read.csv('/mnt/classtest/carsin/911_Calls_for_Service_(Last_30_Days).csv')
display(df)