#!/bin/sh
# Shell launcher for signalrelay enabled sessions.
echo "(pane/$TMUX_PANE)"
exec "$HOME/.tty/signalrelay" "$SHELL" "$SHELL"
