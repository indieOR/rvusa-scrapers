#!/bin/bash

baseurl="https://www.rvusa.com"

#URL Navigation Sequence
#All Class A
#https://www.rvusa.com/rv-guide/specs-by-type-class-a-t2
#Pic a model...(e.g. All Coachmen Encore)
#https://www.rvusa.com/rv-guide/specs-by-model-coachmen-encore-m7714-b113
#Pick a year of Coachmen Encore (e.g. 2022)
#https://www.rvusa.com/rv-guide/specs-by-model-2022-coachmen-encore-class-a-m7714-y2022-b113
#Pick a floorplan cor 2022 Coachmen Encore, e.g. Coachmen Encore 325SS
#https://www.rvusa.com/rv-guide/2022-coachmen-encore-class-a-floorplan-325ss-tr54414

for classurl in `curl -s https://www.rvusa.com/rv-guide/specs-by-type-popup-t6 | grep -o \/rv-guide\/specs-by-model.*t6`; do
	#At Specs_Guide->Class A
	#Now get years for this model...

	#https://www.rvusa.com/rv-guide/specs-by-model-coachmen-encore-m7714-b113
	for yearurl in `curl -s ${baseurl}/${classurl} | grep -Po "/rv-guide/specs-by-model-\d\d\d\d.*t6"`; do
		#At Specs_Guide->
		#Get list of years
		for floorplanurl in `curl -s ${baseurl}${yearurl} | grep -Po \/rv-guide\/.*floorplan.*\"\> | grep -v "h2 class" | awk -F '"' '{print $1}'`; do
			#echo "./rvparse.py --url ${baseurl}${floorplanurl}"
			#For each floor plan call the python script to capture all the specs as JSON
			./rvparse.py --url ${baseurl}${floorplanurl} --path ./popup/ &
		done
	done
done
