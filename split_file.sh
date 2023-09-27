#!/bin/bash

file_path="files2bedownload.list"

# Read the file line by line
while IFS= read -r line; do
			# You can replace the echo command with whatever operation you want to perform with each ID
	    echo "Processing ID: $line"
	    sb download --file $line
	    ori_FILE=`ls *exome.vep_105.vcf.gz`
	    zgrep "^#" $ori_FILE > head.vcf
	    zgrep -v "^#" $ori_FILE | split -d -l 1000000 - small_file_
	    rm -f $ori_FILE
        for CHUNKFILE in `ls small_file_*`
        do
            numeric_suffixes=`echo $CHUNKFILE |  sed 's/small_file0//g'`
            cat head.vcf $CHUNKFILE | bgzip > "_"${numeric_suffixes}${ori_FILE}
            tabix "_"${numeric_suffixes}${ori_FILE}
            sb upload --file "_"${numeric_suffixes}${ori_FILE} --project yiran/variant-workbench-testing
            sb upload --file "_"${numeric_suffixes}${ori_FILE}".tbi" --project yiran/variant-workbench-testing
        done
	    rm -f small_file_*
	    rm -f *vcf*
    done < "$file_path"