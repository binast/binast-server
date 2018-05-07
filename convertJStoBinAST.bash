#!/usr/bin/env bash
SRC_PATH=$1 # e.g. '../binast-server/fb_bench/'
ENCODER_PATH="./target/debug/binjs_encode"

# Note, this default is zero laziness!!
ENCODING_OPTIONS=

if [ $# -lt 1 ];
then
   echo "Usage: convertJStoBinAST.bash <path to source directory>"
   exit 0
fi

for nextpath in `find $SRC_PATH -type f -name "*.js"`
do
	#echo $i;
	$ENCODER_PATH $ENCODING_OPTIONS -i $nextpath -o $(dirname $nextpath) 
done
