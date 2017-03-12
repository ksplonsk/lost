#!/bin/bash

if test -d $2
then
	rm $2/*
else
	mkdir $2
fi

python export_data.py $1 $2
