/*
 * pwclip.c
 * Utility app which allows to input a password and temporarily put in
 * on clipboard. Clear clipboard on exit.
 * First experiment with GTK+ coding.
 *
 * TODO clear clipboard on interrupt/term OS signals as well.
 *
 * Author: Øyvind Stegard <oyvinst@ifi.uio.no>
 */

#include <gtk/gtk.h>
#include <gdk/gdkkeysyms.h>
#include <glib/gprintf.h>

#include "pwclip.h"

/*
 * Window system delete event handler. Events are not the same as signals and
 * callback signature is slightly different. Events are related to platform
 * windowing system.
 */
static gboolean delete_event( GtkWidget *widget,
                              GdkEvent  *event,
                              gpointer   data ) {
  /* If you return FALSE in the "delete-event" signal handler,
   * GTK will emit the "destroy" signal. Returning TRUE means
   * you don't want the window to be destroyed.
   * This is useful for popping up 'are you sure you want to quit?'
   * type dialogs.
   * Change TRUE to FALSE and the main window will be destroyed with
   * a "delete-event".
   */
  return FALSE;
}

/* Top level window destroy handler. Clears clipboard and quits app. */
static void destroy(GtkWidget *widget, gpointer data) {
  GtkClipboard *cb = gtk_clipboard_get(GDK_SELECTION_CLIPBOARD);
  gtk_clipboard_clear(cb);
  gtk_main_quit();
}

/* This is a callback function.
 * Expects newline checkbox widget as custom data. */
static void set_clipboard_handler(GtkWidget *widget, gpointer data) {
  GtkClipboard* cb = gtk_clipboard_get(GDK_SELECTION_CLIPBOARD);
  GString* text = g_string_new(gtk_entry_get_text(GTK_ENTRY(widget)));

  // If extra newline is requested, then append it.
  if (gtk_toggle_button_get_active(GTK_TOGGLE_BUTTON(data)) && text->len) {
    text = g_string_append(text, "\n");
  }

  gtk_clipboard_set_text(cb, text->str, -1);
  g_string_free(text, TRUE);
}

static gboolean is_current_password_on_clipboard(GtkClipboard *cb, GtkEntry *entry) {
  gboolean retval = FALSE;
  gchar* clipboard_text = gtk_clipboard_wait_for_text(cb);
  if (clipboard_text) g_strchomp(clipboard_text);

  if (gtk_entry_get_text_length(entry) && clipboard_text) {
    if (g_strcmp0(clipboard_text, gtk_entry_get_text(entry)) == 0) {
      retval = TRUE;
    }
  }
  
  g_free(clipboard_text);
  return retval;
}

static GdkPixbuf* get_icon_pixbuf(void) {
  static GdkPixbuf* pixbuf;
  if (!pixbuf) {
    pixbuf = gdk_pixbuf_new_from_inline(-1, pw_icon_data, FALSE, NULL);
  }
  return pixbuf;
}

/*
 * Handles owner-change events for clipboard, updates status.
 * Requires top-level GTK window as data.
 */
static void clipboard_status_handler(GtkClipboard *cb, GdkEvent *event, gpointer gtk_window) {
  GtkLabel *status = g_object_get_data(gtk_window, "label_status");
  GtkEntry *entry = g_object_get_data(gtk_window, "entry_pw");
  
  if (is_current_password_on_clipboard(cb, entry)) {
    gtk_label_set_text(status, "<b><span color='red'>PASSWORD SET ON CLIPBOARD</span></b>");
    gtk_label_set_use_markup(status, TRUE);
  } else {
    gtk_label_set_text(status, "No password set.");
  }
}

/* Moves window to top right corner */
static void move_window(GtkWidget *window) {
  GdkScreen *default_screen;
  gint width, height, screen_width;
  
  gtk_window_get_size(GTK_WINDOW(window), &width, &height);
  default_screen = gdk_screen_get_default();
  screen_width = gdk_screen_get_width(default_screen);
  gtk_window_move(GTK_WINDOW(window), screen_width - width - 10, 30);
}

/* Looks for ESC key press, and quits if received. Otherwise lets event
   propagate further. */
static gboolean esc_key_press_handler(GtkWidget *widget, GdkEvent *event, gpointer data) {
  GdkEventKey event_key = event->key;
  if (event_key.keyval == GDK_KEY_Escape) {
    destroy(widget, NULL);
    return TRUE;
  }
  return FALSE;
}

/* Set up window accelerators/keybindings */
static void set_global_keybindings(GtkWidget *window) {
  GtkAccelGroup *accel_group = gtk_accel_group_new();
  
  // CTRL+Q to quit:
  gtk_accel_group_connect(accel_group, (guint)'q', GDK_CONTROL_MASK, GTK_ACCEL_LOCKED,
                          g_cclosure_new(G_CALLBACK(destroy), NULL, NULL));
  gtk_window_add_accel_group(GTK_WINDOW(window), accel_group);

  // ESC to quit:
  g_signal_connect (window, "key-press-event",
                    G_CALLBACK (esc_key_press_handler), NULL);
}

int main(int argc, char *argv[] ) {
  /* GtkWidget is the general storage type for widgets */
  GtkWidget *window;
  GtkWidget *vbox, *hbox1, *hboxtop;
  GtkWidget *label_info, *label_status, *label_pw;
  GtkWidget *entry_pw;
  GtkWidget *check_button_toggle_newline;
  GtkWidget *button_quit;
  GtkWidget *image_icon;

  /* This is called in all GTK applications. Arguments are parsed
   * from the command line and are returned to the application. */
  gtk_init (&argc, &argv);

  /* create a new window */
  window = gtk_window_new(GTK_WINDOW_TOPLEVEL);

  /* gtk_window_set_default_size(GTK_WINDOW(window), 500, 50); */
  /* gtk_window_set_position(GTK_WINDOW(window), GTK_WIN_POS_CENTER); */
  gtk_container_set_border_width (GTK_CONTAINER (window), 10);
  gtk_window_set_title(GTK_WINDOW(window), "Password to clipboard");
  gtk_window_set_keep_above(GTK_WINDOW(window), TRUE);
  gtk_window_set_resizable(GTK_WINDOW(window), FALSE);
  gtk_window_set_type_hint(GTK_WINDOW(window), GDK_WINDOW_TYPE_HINT_UTILITY);
  gtk_window_stick(GTK_WINDOW(window));
  gtk_window_set_icon(GTK_WINDOW(window), get_icon_pixbuf());
  set_global_keybindings(window);
  

  /* When the window is given the "delete-event" signal (this is given
   * by the window manager, usually by the "close" option, or on the
   * titlebar), we ask it to call the delete_event () function
   * as defined above. The data passed to the callback
   * function is NULL and is ignored in the callback function. */
  g_signal_connect (window, "delete-event",
                    G_CALLBACK (delete_event), NULL);
    
  /* Here we connect the "destroy" event to a signal handler.  
   * This event occurs when we call gtk_widget_destroy() on the window,
   * or if we return FALSE in the "delete-event" callback. */
  g_signal_connect (window, "destroy",
                    G_CALLBACK (destroy), NULL);

  // Set up signal handling for clipboard events:
  GtkClipboard* clipboard = gtk_clipboard_get(GDK_SELECTION_CLIPBOARD);
  g_signal_connect(clipboard, "owner-change",
                   G_CALLBACK(clipboard_status_handler), window);
    
  // Set up vertical box container:
  vbox = gtk_box_new(GTK_ORIENTATION_VERTICAL, 0);

  label_info = gtk_label_new("Type password to set on clipboard.");
  gtk_label_set_line_wrap(GTK_LABEL(label_info), TRUE);
  gtk_label_set_use_markup(GTK_LABEL(label_info), TRUE);
  gtk_misc_set_alignment(GTK_MISC(label_info), 0.0f, .5f);

  hboxtop = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 0);
  gtk_box_pack_start(GTK_BOX(hboxtop), label_info, TRUE, TRUE, 0);
  image_icon = gtk_image_new_from_pixbuf(get_icon_pixbuf());
  gtk_box_pack_start(GTK_BOX(hboxtop), image_icon, TRUE, TRUE, 0);
  
  hbox1 = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 0);
  label_pw = gtk_label_new_with_mnemonic("_Password:");
  gtk_misc_set_alignment(GTK_MISC(label_pw), 0.0f, .5f);
  gtk_box_pack_start(GTK_BOX(hbox1), label_pw, TRUE, TRUE, 0);

  check_button_toggle_newline = gtk_check_button_new_with_mnemonic("_Append newline to password text.");
  gtk_toggle_button_set_active(GTK_TOGGLE_BUTTON(check_button_toggle_newline), TRUE);
  entry_pw = gtk_entry_new();
  gtk_entry_set_max_length(GTK_ENTRY(entry_pw), MAX_PW_LEN);
  gtk_entry_set_visibility(GTK_ENTRY(entry_pw), FALSE);

  g_signal_connect(entry_pw, "changed", G_CALLBACK(set_clipboard_handler), check_button_toggle_newline);
  g_signal_connect(entry_pw, "activate", G_CALLBACK(set_clipboard_handler), check_button_toggle_newline);
  // When checkbox is toggled, trigger set_clipboard_handler as well:
  g_signal_connect_swapped(check_button_toggle_newline,  "toggled", G_CALLBACK(set_clipboard_handler), entry_pw);
  gtk_box_pack_start(GTK_BOX(hbox1), entry_pw, TRUE, TRUE, 0);

  // Connect mnemoic for "Password:"-label to entry widget
  gtk_label_set_mnemonic_widget(GTK_LABEL(label_pw), entry_pw);
  // Add entry_pw as custom data on window object:
  g_object_set_data(G_OBJECT(window), "entry_pw", entry_pw);
  
  // Status label
  label_status = gtk_label_new("No password set.");
  /* gtk_misc_set_alignment(GTK_MISC(label_status), 0.0f, .5f); */
  // Set custom data object on window object, with key "label_status":
  g_object_set_data(G_OBJECT(window), "label_status", label_status);

  // Creates a new button with label
  button_quit = gtk_button_new_with_label ("_Quit and clear clipboard");
  gtk_button_set_use_underline(GTK_BUTTON(button_quit), TRUE);

  /* This will cause the window to be destroyed by calling
   * gtk_widget_destroy(window) when "clicked".  Again, the destroy
   * signal could come from here, or the window manager. */
  g_signal_connect_swapped (button_quit, "clicked",
                            G_CALLBACK (gtk_widget_destroy),
                            window);

  // Pack child widgets into vertical box
  gtk_box_pack_start(GTK_BOX(vbox), hboxtop, TRUE, TRUE, 0);
  gtk_box_pack_start(GTK_BOX(vbox), hbox1, TRUE, TRUE, 0);
  gtk_box_pack_start(GTK_BOX(vbox), check_button_toggle_newline, TRUE, TRUE, 0);
  gtk_box_pack_start(GTK_BOX(vbox), label_status, TRUE, TRUE, 0);
  gtk_box_pack_start(GTK_BOX(vbox), button_quit, TRUE, TRUE, 0);
  
  // Add vertical box container into top level window:
  gtk_container_add(GTK_CONTAINER(window), vbox);
    
  /* The final step is to display this newly created widget hierarchy: */
  // call gtk_widget_show_all from root widget:
  gtk_widget_show_all(window);

  // Instead of calling show individually for all created widgets:
  /* ... */
  /* gtk_widget_show(label_status); */
  /* gtk_widget_show(button_quit); */
  /* and show the window last */
  /* gtk_widget_show (window); */

  /* move window after showing it, to get size calculations correct. */
  move_window(window);

  /* All GTK applications must have a gtk_main(). Control ends here
   * and waits for an event to occur (like a key press or
   * mouse event). */

  gtk_main ();
    
  return 0;
}
