# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from typing import List  # noqa: F401

from libqtile import hook, layout
from libqtile.config import Click, Drag, Group, Key, Match
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from screens import get_screens

grey = "686868"
red = "FF5C57"
yellow = "F3F99D"
blue = "57C7FF"
magenta = "FF6AC1"
cyan = "9AEDFE"
white = "F1F1F0"

MOD = "mod4"
ALT = "mod1"


class Commands:
    menu = "rofi -show run"
    menu_desktop = "rofi -modi drun -show"
    browser = "firefox"
    terminal = guess_terminal()
    lock = "loginctl lock-session"
    slack = "slack"


keys = [
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 3%+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 3%-")),
    Key([], "XF86AudioMute", lazy.spawn("amixer -D pulse set Master toggle")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("acpilight -inc 10")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("acpilight -dec 10")),
    Key([MOD], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([MOD], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([MOD], "j", lazy.layout.down(), desc="Move focus down"),
    Key([MOD], "k", lazy.layout.up(), desc="Move focus up"),
    Key(
        [MOD],
        "space",
        lazy.spawn(Commands.menu_desktop),
    ),
    Key(
        [MOD, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [MOD, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([MOD, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([MOD, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([MOD], "g", lazy.layout.grow()),
    Key([MOD, "shift"], "g", lazy.layout.shrink()),
    Key([MOD], "m", lazy.layout.maximize()),
    Key([MOD], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key(
        [MOD],
        "r",
        lazy.spawn(Commands.menu),
        desc="Spawn a command using a prompt widget",
    ),
    Key([MOD], "z", lazy.window.kill(), desc="Kill focused window"),
    Key([MOD], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([MOD], "Print", lazy.spawn("flameshot gui")),
    Key([MOD], "Return", lazy.spawn(Commands.terminal), desc="Launch terminal"),
    Key([MOD, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([MOD], "Delete", lazy.spawn(Commands.lock), desc="Lock the screen"),
    Key([MOD], "Tab", lazy.layout.next()),
    Key([ALT], "Tab", lazy.screen.next_group(skip_empty=True)),
]

_group_conf = {
    "WEB": {"keys": ("ampersand", "1"), "apps": ("firefox",), "layout": "max"},
    "TERM": {"keys": ("eacute", "2"), "apps": ()},
    "CODE": {"keys": ("quotedbl", "3"), "apps": ("code",), "layout": "max"},
    "SLA": {"keys": ("apostrophe", "4"), "apps": ("slack",), "layout": "max"},
    "SPO": {"keys": ("o",), "apps": ()},
    "WTE": {"keys": ("p",), "apps": ()},
}

groups = []
for name, conf in _group_conf.items():
    groups.append(
        Group(
            name,
            matches=[Match(wm_class=[app]) for app in conf["apps"]],
            layout=conf.get("layout", "monadtall"),
        )
    )
    for key in conf["keys"]:
        keys.extend(
            [
                # MOD1 + letter of group = switch to group
                Key([MOD], key, lazy.group[name].toscreen()),
                # MOD1 + shift + letter of group = switch to & move focused window to group
                Key([MOD, "shift"], key, lazy.window.togroup(name)),
            ]
        )

layouts = [
    layout.MonadTall(border_width=2, margin=7, border_focus=blue, border_normal=grey),
    layout.Max(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = get_screens()

# Drag floating layouts.
mouse = [
    Drag(
        [MOD],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [MOD], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([MOD], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="pinentry-gtk-2"),
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="blueman-manager"),
        Match(wm_class="keepassxc"),
        Match(wm_class="pavucontrol"),
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
    auto_float_types=["notification", "toolbar", "splash", "dialog"],
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True
wmname = "LG3D"


# Weird GNOME issue
# @hook.subscribe.startup
# def dbus_register():
#     id = os.environ.get("DESKTOP_AUTOSTART_ID")
#     if not id:
#         return
#     subprocess.Popen(
#         [
#             "dbus-send",
#             "--session",
#             "--print-reply",
#             "--dest=org.gnome.SessionManager",
#             "/org/gnome/SessionManager",
#             "org.gnome.SessionManager.RegisterClient",
#             "string:qtile",
#             "string:" + id,
#         ]
# )


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/autostart.sh"])


@hook.subscribe.client_new
def dialogs(window):
    if window.window.get_wm_type() == "dialog" or window.window.get_wm_transient_for():
        window.floating = True


@hook.subscribe.client_new
def follow_window(client):
    for group in groups:
        match = next((m for m in group.matches if m.compare(client)), None)
        if match:
            targetgroup = client.qtile.groups_map[group.name]
            targetgroup.cmd_toscreen(toggle=False)
            break
