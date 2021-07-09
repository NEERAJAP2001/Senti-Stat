
from pywebio.input import *
from pywebio.output import *
import requests
from collections import defaultdict
import time 
from pywebio.output import put_html
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
import argparse
from pywebio import start_server

app = Flask(__name__)



def task_func():

    name=input("Enter Your name",type="text",required=True)
    put_markdown("# Welcome,to Emorec Stats %s!! " %(name))




    def check(agree):
        if agree != ['I Agree to terms and conditions']:
            return 'Please agree to the terms and conditions'


    
    put_markdown(' ## Refer To Terms [Here](https://github.com/appdotnet/template-terms-of-service/blob/master/terms_template.md)')
    agree = checkbox("User terms and Conditions", options=['I Agree to terms and conditions'],validate=check)




    file = file_upload(label='Upload your text file', accept='.txt',required=True)
    content = file['content'].decode('utf-8').splitlines()



    with put_loading(shape='grow',color='primary'):
        time.sleep(5)

        dic = defaultdict(lambda:0)
        for i in range(len(content)):
            query = {'text':str(content[i])}
            response = requests.get('https://detect-emotionapi.herokuapp.com/sentiment_analysis/', params=query)
            dic[response.json()]+=1



        Reviews= list(dic.keys())
        values = list(dic.values())


        put_markdown("## Table Here : ")
        fig = go.Figure(data=[go.Table(header=dict(values=['Reviews', 'Count']),cells=dict(values=[Reviews, values]))])
        html = fig.to_html(include_plotlyjs="require", full_html=False)
        put_html(html)




        put_markdown("## Bar Chart Here : ")
        fig = go.Figure([go.Bar(x=Reviews, y=list(dic.values()))])
        html = fig.to_html(include_plotlyjs="require", full_html=False)
        put_html(html)
 



        put_markdown('## Pie Chart Here : ')
        fig = go.Figure(data=[go.Pie(labels=Reviews, values=values)])
        html = fig.to_html(include_plotlyjs="require", full_html=False)
        put_html(html)



        put_markdown('## Donut Chart Here: ')
        fig = go.Figure(data=[go.Pie(labels=Reviews, values=values, hole=.3)])
        html = fig.to_html(include_plotlyjs="require", full_html=False)
        put_html(html)

        put_markdown('## Horizontal Bar Chart Here : ')
        fig = go.Figure(go.Bar(x=values,y=Reviews,orientation='h'))
        html = fig.to_html(include_plotlyjs="require", full_html=False)
        put_html(html)




        put_markdown('## Pulled Donut Chart Here: ')
        fig = go.Figure(data=[go.Pie(labels=Reviews, values=values, pull=[0, 0, 0.2, 0])])
        html = fig.to_html(include_plotlyjs="require", full_html=False)
        put_html(html)




app.add_url_rule('/tool', 'webio_view', webio_view(task_func),
            methods=['GET', 'POST', 'OPTIONS'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(task_func, port=args.port)