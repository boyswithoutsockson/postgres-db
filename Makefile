# This makefile contains recipes for constructing the database.

.ONESHELL:

.PHONY: help
help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make <command> \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

# Default for `make` without any args
all: help

####################################
# Scripts for downloading raw data #
####################################

data/dump.zip:
	mkdir -p data
	FILE_ID=1cQb23nkz-DAlo33cU96BnPjdnXU9MoFA
	curl -L "https://drive.usercontent.google.com/download?id=$${FILE_ID}&confirm=true" --progress-bar \
		-o $@

DATA_DUMP = data/.unzipped
$(DATA_DUMP): data/dump.zip
	@touch $@
	unzip -oq data/dump.zip -d data


frontend/src/assets/photos-2023-2026.zip:
	mkdir -p frontend/src/assets
	FILE_ID=1K0ykFwVEdU-EmwSPC_p6Yx-S4Ko5Bylh
	curl -L "https://drive.usercontent.google.com/download?id=$${FILE_ID}&confirm=true" --progress-bar \
		-o $@

MP_PHOTOS = frontend/src/assets/.unzipped
$(MP_PHOTOS): frontend/src/assets/photos-2023-2026.zip
	@touch $@
	unzip -oq frontend/src/assets/photos-2023-2026.zip -d frontend/src/assets

.PHONY: data
data: $(DATA_DUMP) $(MP_PHOTOS) ## download and extract all raw data assets

.PHONY: clean-data
clean-data: ## deletes all raw data assets
	rm data/*
	rm frontend/src/assets/*

##################################
# Scripts for data preprocessing #
##################################

mps: pipes/mp_pipe.py data/MemberOfParliament.tsv $(DATA_DUMP) $(MP_PHOTOS)
