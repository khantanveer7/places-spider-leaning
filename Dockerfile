from python:3.9-slim-buster

# Environment Variables with default value set for mode, source and type of spider
ENV mode aws
ENV source dac
ENV type chain


RUN pip install pipenv
RUN pip install boto3
RUN pip install pyyaml


#Create Parent Directory For
RUN mkdir dac-spiders

#Copy Configs From All The Places GitHub CodeBase
COPY scrapy.cfg dac-spiders/
COPY locations dac-spiders/locations
COPY Pipfile dac-spiders/Pipfile

# Copy run script
COPY scripts/run.sh run.sh
RUN chmod 755 run.sh

#Install Dependencies
RUN cd ./dac-spiders && pipenv install

#Verify Scrapy Installation
RUN cd ./dac-spiders && pipenv run scrapy

#Add Entry Point
ENTRYPOINT ["./run.sh"]
