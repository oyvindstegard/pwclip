# Simple makefile for pwclip
# Basic setup with compilation and linking flags for GTK+3.0
# Make automatic variables:
# https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html
#

# Version number (used only for deb target)
PWCLIP_VERSION ::= 1.1

SHELL ::= /bin/sh

CC ::= gcc
CFLAGS = -I. $(shell pkg-config --cflags gtk+-3.0) \
         -Wall -Wunused \
         -DG_DISABLE_DEPRECATED \
         -DGDK_DISABLE_DEPRECATED \
         -DGDK_PIXBUF_DISABLE_DEPRECATED \
         -DGTK_DISABLE_SINGLE_INCLUDES \
         -DGDK_DISABLE_DEPRECATED -DGTK_DISABLE_DEPRECATED

LIBS ::= $(shell pkg-config --libs gtk+-3.0)
# For header file dependencies:
DEPS ::= pwclip.h

# Compilation unit objects
OBJDIR ::= target
DATADIR ::= data

OBJS := $(addprefix $(OBJDIR)/,pwclip.o data.o)

# First rule builds main binary
# $^: the names of all prerequisites, with spaces between them.
$(OBJDIR)/pwclip: $(OBJS)
	gcc -o $@ $^ $(CFLAGS) $(LIBS)

$(OBJDIR):
	mkdir $(OBJDIR)

# GResources
data.c: $(DATADIR)/data.gresource.xml $(shell glib-compile-resources --sourcedir=data/ --generate-dependencies $(DATADIR)/data.gresource.xml)
	glib-compile-resources --sourcedir=$(DATADIR) --generate-source --target=data.c $(DATADIR)/data.gresource.xml

# General rule for compilation units:
# $<: the name of the first prerequisite of an implicit rule
# Dependencies after "|" are only "order-dependencies", which in this case
# ensures the target directory exists.
$(OBJDIR)/%.o: %.c $(DEPS) | $(OBJDIR)
	$(CC) -c -o $@ $< $(CFLAGS)

# Make a deb package (not suitable for public distribution)
DEB_FILENAME ::= pwclip-$(PWCLIP_VERSION)_1.deb
DEB_DIR ::= $(OBJDIR)/$(DEB_FILENAME:.deb=)
.PHONY: deb
deb: $(OBJDIR)/$(DEB_FILENAME)
$(OBJDIR)/$(DEB_FILENAME): $(OBJDIR)/pwclip deb/DEBIAN/control
	mkdir -p $(DEB_DIR)/DEBIAN
	mkdir -p $(DEB_DIR)/usr/local/bin
	cp $(OBJDIR)/pwclip $(DEB_DIR)/usr/local/bin
	strip $(DEB_DIR)/usr/local/bin/pwclip
	sed 's/%{VERSION}/$(PWCLIP_VERSION)/' deb/DEBIAN/control > $(DEB_DIR)/DEBIAN/control
	fakeroot dpkg -b $(DEB_DIR)

# Tags file
.PHONY: tags
tags: TAGS
TAGS: *.[ch]
	etags *.[ch]

.PHONY: clean
clean:
	rm -rf $(DEB_DIR)
	rm -f $(OBJDIR)/*
