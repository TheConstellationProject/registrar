all: install build
	./registrar

install:
	go get -u github.com/labstack/echo/...
	go get -u github.com/dgraph-io/badger/badger
	go get gopkg.in/yaml.v2

build:
	go build -o registrar -v

run: build
	./registrar

clean: # Warning! This will delete the database!
	go clean
	rm -rf db/
