#!/bin/bash

# Runs the scraper for the given pages

if [[ $# -lt 4 ]]; then
	echo "Usage: $0 <list_name> <start_page> <end_page> <output_file_suffix>";
	exit 1
fi

LIST_NAME=$1
START_PAGE=$2
END_PAGE=$3
JSONLINE_FILE_PREFIX=$4

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
	--set OUTPUT_FILE_SUFFIX="$JSONLINE_FILE_PREFIX"_"$START_PAGE"_"$END_PAGE" \
	-a start_page_no=$START_PAGE \
	-a end_page_no=$END_PAGE \
	-a list_name=$LIST_NAME \
	list
