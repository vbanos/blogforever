# $Id$

include ../../config.mk

SUBDIRS =

LIBFILES = tabfill.sql

all:
	$(foreach SUBDIR, $(SUBDIRS), cd $(SUBDIR) && make all && cd .. ;)
	@echo "Done.  Please run make test now."

test:
	$(foreach SUBDIR, $(SUBDIRS), cd $(SUBDIR) && make test && cd .. ;)
	python $(LIBDIR)/python/invenio/template.py --check-custom-templates -v3
	@echo "Done.  Please run make install now."

install:
	$(INSTALL) $(LIBFILES) $(PREFIX)/lib/sql/invenio
	$(foreach SUBDIR, $(SUBDIRS), cd $(SUBDIR) && make install && cd .. ;)
	@echo "Done.  You may want to restart Apache now."
