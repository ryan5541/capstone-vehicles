--use master

create table DJUSAU(
    Price int,
    DateTime datetime,
    TimeStamp int
)

drop table if exists TimeSeries
create table TimeSeries(
    --TimeSeriesID int identity(1,1) primary key,
    date date,
    domesticAuto float,
    foreignAuto float,
    foreignLightTruck float,
    heavyTruck float,
    gasPrice float
)

drop table if exists Commuting
create table Commuting(
    CommutingID int identity(1,1) primary key,
    travelMethod varchar(255),
    numberOfPeople int,
    meanTravelTime int,
)

drop table if exists streamData
create table streamData(
    streamDataID int not NULL,
    timeRecorded datetime not NULL,
    timestamp int not null
)

drop table if exists CarsSold2021
create table CarsSold2021(
    CarsSold2021ID int identity(1,1) primary key,
    carName varchar(255),
    sales2021 int,
    sales2020 int,
    carCategoryID int,
    carSubtypeID int,
    carFeaturesID int
)

drop table carCategory
create table carCategory(
    carCategoryID int primary key identity(1,1),
    category varchar(255)
)

drop table carSubtype
create table carSubtype(
    carSubtypeID int identity(1,1) primary key,
    subtypeName varchar(255)
)

drop table if exists carFeatures
create table carFeatures(
    carFeaturesID int,
    numDoors int,
    numSeats int,
    mpg int,
    engineDrive varchar(255),
    id int,
    length float,
    height float,
    brand varchar(255),
    model varchar(255)
)

drop table if exists Raw_CarFeatures
select * from Raw_CarFeatures

--select top 5 * from DJUSAU
--order by time desc

insert into carCategory
    select distinct category
    from Raw_Cars

select * from carCategory

insert into carSubtype
    select distinct segment
    from Raw_Cars

select * from carSubtype

insert into CarsSold2021
    select sub_segment, [2020], [2021], C.carCategoryID, S.carSubtypeID, NULL
    from Raw_Cars R
        inner join carCategory C
        on R.category = C.category
        inner join carSubtype S
        on R.segment = S.subtypeName