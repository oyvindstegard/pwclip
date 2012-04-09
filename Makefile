# Simple makefile for pwclip
# Basic setup with compilation and linking flags for GTK+2.0

CC = gcc
CFLAGS = -I. $(shell pkg-config --cflags gtk+-2.0) \
         -Wall -Wunused \
         -DG_DISABLE_DEPRECATED \
         -DGDK_DISABLE_DEPRECATED \
         -DGDK_PIXBUF_DISABLE_DEPRECATED

LIBS = $(shell pkg-config --libs gtk+-2.0)
# For header file dependencies:
DEPS = pwclip.h

# Compilation unit objects
OBJ = pwclip.o

# General rule for compilation units:
# $<: the name of the first prerequisite of an implicit rule
%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

# $^: the names of all prerequisites, with spaces between them.
pwclip: $(OBJ)
	gcc -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(OBJ) pwclip
