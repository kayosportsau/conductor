OS := $(shell uname)

preview:
ifeq ($(OS),Darwin)
	sed -i "" -e "s/version:.*/version: $(PREVIEW_VERSION)/" Chart.yaml
	sed -i "" -e "s/version:.*/version: $(PREVIEW_VERSION)/" ../*/Chart.yaml
	sed -i "" -e "s/tag:.*/tag: $(PREVIEW_VERSION)/" values.yaml
else ifeq ($(OS),Linux)
	sed -i -e "s/version:.*/version: $(PREVIEW_VERSION)/" Chart.yaml
	sed -i -e "s/version:.*/version: $(PREVIEW_VERSION)/" ../*/Chart.yaml
	sed -i -e "s|preview_repository_server:.*|repository: $(DOCKER_REGISTRY)\/netflix-conductor|" values.yaml # Please do not edit this line! Managed by customize.sh
	sed -i -e "s|preview_repository_ui:.*|repository: $(DOCKER_REGISTRY)\/netflix-conductor|" values.yaml # Please do not edit this line! Managed by customize.sh

	sed -i -e "s/preview_tag_server:.*/tag: $(PREVIEW_VERSION)/" values.yaml
	sed -i -e "s/preview_tag_ui:.*/tag: ui-$(PREVIEW_VERSION)/" values.yaml
	sed -i -e "s/name: conductor/name: $(PREVIEW_NAMESPACE)/" ns-iam.yaml
	echo "configuring KIAM" && cp -v ns-iam.yaml ../netflix-conductor/templates
else
	echo "platfrom $(OS) not supported to release from"
	exit -1
endif
	echo "  version: $(PREVIEW_VERSION)" >> requirements.yaml
	mkdir -p ~/.helm/repository
	cp -v ../../repositories.yaml ~/.helm/repository/repositories.yaml
	mkdir -p ~/.helm/repository/cache/
	cp -v ../../stable-index.yaml ~/.helm/repository/cache/stable-index.yaml
	jx step helm build

print:
	rm -rf requirements.lock
	helm template .
