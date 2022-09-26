# Databricks notebook source
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