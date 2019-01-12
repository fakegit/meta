DESTDIR ?= /usr/local/bin

install:
	@sudo cp -r ../meta/core $(DESTDIR)/core
	@sudo cp ../meta/meta.py $(DESTDIR)/meta
	@sudo chmod +x $(DESTDIR)/core
	@sudo chmod +x $(DESTDIR)/meta
	@echo "meta was successfully installted."

uninstall:
	@sudo rm -f $(DESTDIR)/meta
	@echo "meta was uninstallted"
