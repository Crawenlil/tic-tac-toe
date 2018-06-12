TEXTBUILDER=pdflatex
BUILD_DIR=_build

all: build_dir styles img
	cd ${BUILD_DIR}; $(TEXTBUILDER) -shell-escape ../*.tex

styles: build_dir
	cp *.sty ${BUILD_DIR}

img: build_dir
	cp -r img/ ${BUILD_DIR}

clean:
	rm -rvf _build

build_dir:
	mkdir -p ${BUILD_DIR}
