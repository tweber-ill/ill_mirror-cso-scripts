#!/bin/bash
#
# downloads the experimental data
# @author Tobias Weber <tweber@ill.fr>
# @date 11-mar-2025
# @license see LICENSE
#


data_id=15006082


if [ -L data ] || [ -d data ]; then
	echo -e "A data directory already exists. Skipping.";
else
	echo -e "Downloading experimental data..."
	mkdir -v data && cd data

	wget -O data.zip https://zenodo.org/record/${data_id}/files/data.zip?download=1

	unzip data.zip
	rm -v data.zip
fi
