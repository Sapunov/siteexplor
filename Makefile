.PHONY: build install dist srpm rpm pypi clean

PYTHON			?=python
INSTALL_FLAGS	?=
NAME          	:= sitexplor

build:
	$(PYTHON) setup.py build

install:
	$(PYTHON) setup.py install --skip-build $(INSTALL_FLAGS)
	mkdir -p /opt/$(NAME)/data/sites /opt/$(NAME)/data/logs
	chown nsapunov:nsapunov -R /opt/$(NAME)
	cp $(NAME)app /usr/bin

dist: clean
	tar -czvf $(NAME).tgz *
	mkdir dist && mv $(NAME).tgz dist

clean:
	rm -rf build dist $(NAME).tgz $(NAME).egg-info
