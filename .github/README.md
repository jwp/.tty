## Terminal Emulator Configuration and Control

Collection of scripts to generate configurations for various emulators.
Currently, only xterm; some initial hints for rust(Alacritty).

Much of this is purely experimental; the configuration performed by these scripts are
specialized for custom applications and are likely undesirable for most environments.

This is not likely to be useful to others outside of a starting point or inspiration
for making your own configuration generator.

### Input

- Keyboard mapping generator(CSI-u bindings).
- Keyboard mapping index for application support(ambiguous modifier resolution).
- Map switching with symbolic links?

### Output

Currently, nothing implemented here.

- High-level color definitions.
- Definition based theme generator.

### Proxy

Session daemon configuration. tmux, screen, and mirrors.

- Signal relay shell launcher.
- tmux configuration.

### Usage

This project serves as functionality and notes. Generated xterm translations include
CSI-u bindings that may not be recognized by applications without further configuration.
Some legacy bindings (shift-tab, control-space, and others) are discarded in favor CSI-u
variants for better or worse.

```shell
# Currently, only generates xterm translations.
~/.tty/configure keyboard && ~/.tty/configure xterm
```
