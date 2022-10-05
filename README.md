## **Automotive Industry 2021: Analysis and Predictions**
As it did in many other industries, the COVID pandemic caused enormous disruption in the automotive industry: reducing sales, straining supply chains, and casting great uncertainty over the future. Our group adopts a data-driven strategy to cut through this uncertainty. We analyze historical trends in monthly sales data, building machine-learning models to accurately forecast future sales, as well as examine the 2021 market to idenfity the car-features most strongly correlated with sales. We also investigate possible associations between automotive sales and external factors, such as the price of gasoline or inter-state differences in commute characteristics.

This repository contains both explanatory documents and code. The former are contained within the "Project Documents" folder, the latter within "code". Some documents of particular interest in the Project Documents folder are 

    - ExecutiveSummary.pdf, where we provide some of the exploratory questions structuring our analysis

    - RepeatableETLReport.pdf, where we describe where we found our data and how we processed it before our analysis

    - (*pending*) ProjectTechnicalReport.pdf, in which we discuss the results and key takeaways of our analysis.

The code folder contains all of the Jupyter notebooks and Python files we created in the course of this project. We sub-divide them into three categories: API calls and webscraping, Databricks, and Machine-Learning. The first category contains all of the code which pulled in data from external sources. Contained in the "Databricks" subfolder are all of the python files loading our data into our SQL database, as well as the code for our Kafka producer and consumer. Finally, the ML folder contains two Jupyter notebooks, one implementing a Vector Autoregression model and the other an LSTM neural network.

This document will be updated to reflect future changes in the structure and contents of this repo.