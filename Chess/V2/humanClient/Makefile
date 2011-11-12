all: libclient.so

submit: libclient.so
	@echo "$(shell cd ..;sh submit.sh c)"


libclient.so:
	$(MAKE) -C ../client/c/ libclient.so
	cp ../client/c/libclient.so libclient.so


clean:
	rm -f libclient.so
	rm -f *.pyc
