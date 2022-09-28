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

df = spark.read.options(header = True).json('/mnt/jazztrio/datain/Cleaned/cars.json')
#df = df.withColumnRenamed('_c0', 'CarsSold2021ID')
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Database variables 

# COMMAND ----------

database = "JazzTrio"
table = "dbo.Raw_Cars"
user = "jazztrio"
password  = "YaLikeJazz!?123"
server = "gen10-data-fundamentals-22-07-sql-server.database.windows.net"

# COMMAND ----------

# MAGIC %md 
# MAGIC ## Write Data from Dataframe

# COMMAND ----------

# #set up to add rows
# columns = ["ramenTesT_id"]
# data = [("1"), ("2", "4"), ("4", "6")]
# jbdcDF_2= spark.createDataFrame([1,11,13,14, 15], "int").toDF("TestTable")
# display(jbdcDF_2)

df.write.format('jdbc').option("url", f"jdbc:sqlserver://{server}:1433;databaseName={database};") \
    .mode("overwrite") \
    .option("dbtable", table) \
    .option("user", user) \
    .option("password", password) \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .save()


# COMMAND ----------

