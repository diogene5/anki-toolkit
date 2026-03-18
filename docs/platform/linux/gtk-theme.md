# Anki not picking up GTK theme on Gnome/Linux

If Anki fails to recognize the GTK theme on GNOME/Linux systems, you can manually configure the GTK theme settings.

## Solution

Execute these terminal commands:

```
theme=$(gsettings get org.gnome.desktop.interface gtk-theme)
echo "gtk-theme-name=$theme" >> ~/.gtkrc-2.0
echo "export GTK2_RC_FILES=$HOME/.gtkrc-2.0" >> ~/.profile
```

After running these commands, log out and log back in.

## How It Works

The first command retrieves the current GTK theme setting from GNOME's configuration. The subsequent commands append the theme information to configuration files that Anki can access, ensuring proper theme detection upon restart.
