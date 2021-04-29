from diagrams import Cluster, Diagram
from diagrams.gcp.analytics import BigQuery, Dataflow, PubSub
from diagrams.gcp.compute import AppEngine, Functions
from diagrams.gcp.database import BigTable
from diagrams.gcp.storage import GCS
from diagrams.programming.framework import React

with Diagram("Data project3:Bitcoin"):
    pubsub = PubSub("Pub Sub")
    with Cluster("Source data"):
        yfsd = Functions("yahoo finance")
        yfsd >> pubsub

    with Cluster("Artificial Intelligence - Bitcoin"):
        flow = Functions("ETL process")
        with Cluster("Data base"):
            db = BigQuery("Big Query")
            flow >> db
        
        predict = Functions("Calculate Prediction")
        with Cluster("Update model"):
            CTF = Functions("Control Training")
            train = Functions("Training")
            
    
    with Cluster("Web"):
        webpage = React("React.App")
        

    pubsub >> flow
    #db >> train
    db >> predict
    db >> CTF#
    
    
    train >> predict
    CTF >> train#
    predict >> db
    db >> webpage
    webpage >> db
