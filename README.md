# Password to clipboard utility

This small GTK program allows to input password and have it stored on
the clipboard temporarily. When closing the program, the clipboard
will be cleared automatically.


## Security

Storing passwords on clipboard is not particularly secure, but
sometimes very practical. However, this program makes no guarantees
about the password not leaking to other places, since the clipboard is
readable by all user processes.


## Building

Required development packages on Ubuntu/Debian:

- libgtk-3-dev
