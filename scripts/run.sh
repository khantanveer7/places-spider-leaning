#!/usr/bin/env bash
echo "Starting Container Actions Now"
echo "Env Variables Provided: "
echo $spider $source $type

spider_date=$(date -u +%Y%m%d.%H%M%S)

if [ $? -eq 0 ]; then
  echo "Starting Crawl"
  echo "${spider_date}"
  cd ./dac-spiders

  mkdir -p "/output/${source}/${spider}/${spider_date}"
    
  output_file_name="/output/${source}/${spider}/${spider_date}/${spider}.geojson"
  log_file_name="/output/${source}/${spider}/${spider_date}/${spider}_log.json"

  # OLD APPROACH WITH ERROR
  # pipenv run scrapy crawl $spider --output-format=geojson --output=$output_file_name -s LOGSTATS_FILE=$log_file_name
  
  # NEW APPROACH THAT WORKS
  pipenv run scrapy crawl $spider -o $output_file_name:geojson --logfile=$log_file_name -s LOGSTATS_FILE=$log_file_name
  # pipenv run scrapy crawl $spider --logfile=$log_file_name
  
else
  echo "Spider Download Failed"
fi