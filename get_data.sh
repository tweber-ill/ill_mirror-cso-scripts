#!/bin/bash
#
# downloads the experimental data
# @author Tobias Weber <tweber@ill.fr>
# @date 11-mar-2025
# @license see LICENSE
#


# TODO: use correct data id, this is just a placeholder for the moment
data_id=5724117


if [ -L data ] || [ -d data ]; then
	echo -e "A data directory already exists. Skipping.";
else
	echo -e "Downloading experimental data..."
	mkdir -v data && cd data

	wget -O data.zip https://zenodo.org/record/${data_id}/files/data.zip?download=1

	unzip data.zip
	rm -v data.zip
fi
