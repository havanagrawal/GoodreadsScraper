#!/bin/bash

# Runs the scraper for the given pages

if [[ $# -lt 4 ]]; then
	echo "Usage: $0 <list_name> <start_page> <end_page> <json_file_prefix>";
	exit 1
fi

LIST_NAME=$1
START_PAGE=$2
END_PAGE=$3
JSON_FILE_PREFIX=$4

if [[ ${#START_PAGE} -lt 2 ]] ; then
			START_PAGE="0${START_PAGE}"
			START_PAGE="${START_PAGE: -2}"
fi

if [[ ${#END_PAGE} -lt 2 ]] ; then
			END_PAGE="0${END_PAGE}"
			END_PAGE="${END_PAGE: -2}"
fi

scrapy crawl \
	--logfile=scrapy.log \
	--output "$JSON_FILE_PREFIX"_"$START_PAGE"_"$END_PAGE".json \
	-a start_page_no=$START_PAGE \
	-a end_page_no=$END_PAGE \
	-a list_name=$LIST_NAME \
	list
