#!/usr/bin/env bash
FBBENCH_PATH='../binast-server/fb_bench/'
ENCODER_PATH="./target/debug/binjs_encode"

# Note, this default is zero laziness!!
ENCODING_OPTIONS=

for nextpath in `find $FBBENCH_PATH -type f -name "*.js"`
do
	#echo $i;
	$ENCODER_PATH $ENCODING_OPTIONS -i $nextpath -o $(dirname $nextpath) 
done
