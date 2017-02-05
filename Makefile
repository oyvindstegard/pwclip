# Simple makefile for pwclip
# Basic setup with compilation and linking flags for GTK+3.0
# Make automatic variables:
# https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html
#

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

# $^: the names of all prerequisites, with spaces between them.
$(OBJDIR)/pwclip: $(OBJS)
	gcc -o $@ $^ $(CFLAGS) $(LIBS)

$(OBJDIR):
	mkdir $(OBJDIR)

# Resources
data.h: $(DATADIR)/data.gresource.xml $(shell glib-compile-resources --sourcedir=$(DATADIR)/ --generate-dependencies $(DATADIR)/data.gresource.xml)
	glib-compile-resources --sourcedir=$(DATADIR) --generate-header --target=data.h $(DATADIR)/data.gresource.xml
DEPS += data.h

data.c: $(DATADIR)/data.gresource.xml $(shell glib-compile-resources --sourcedir=data/ --generate-dependencies $(DATADIR)/data.gresource.xml)
	glib-compile-resources --sourcedir=$(DATADIR) --generate-source --target=data.c $(DATADIR)/data.gresource.xml


# General rule for compilation units:
# $<: the name of the first prerequisite of an implicit rule
# Dependencies after "|" are only "order-dependencies", which in this case
# ensures the target directory exists.
$(OBJDIR)/%.o: %.c $(DEPS) | $(OBJDIR)
	$(CC) -c -o $@ $< $(CFLAGS)

# Tags file
.PHONY: tags
tags: TAGS
TAGS: *.[ch]
	etags *.[ch]

# Declare `clean' to be phony (not an object):
.PHONY: clean
clean:
	rm -f $(OBJDIR)/*
