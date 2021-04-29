from diagrams import Cluster, Diagram
from diagrams.gcp.analytics import BigQuery, Dataflow, PubSub
from diagrams.gcp.compute import AppEngine, Functions
from diagrams.gcp.database import BigTable
from diagrams.gcp.storage import GCS
from diagrams.programming.framework import React

with Diagram("Prediction Bitcoin"):
    pubsub = PubSub("Pub Sub")
    with Cluster("Source data"):
        yfsd = Functions("yahoo finance")
        yfsd >> pubsub

    with Cluster("AI"):
        with Cluster("ETL process"):
            with Cluster("Transform"):
                flow = Functions("data flow")

            with Cluster("Data base"):
                db = BigQuery("bq")
                flow >> db
        
        
        with Cluster("Prediction"):
            predict = Functions("Calculate Prediction")
        with Cluster("Update model"):
            CTF = Functions("Control Training")
            with Cluster("Training"):
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
