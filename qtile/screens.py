import subprocess
from pathlib import Path

from libqtile import bar, widget
from libqtile.config import Screen

SPACER = widget.Sep(font="Ubuntu Mono", padding=2, fontsize=14)

DEFAULT_WIDGETS = [
    widget.GroupBox(),
    widget.WindowName(),
]

MAIN = Screen(
    top=bar.Bar(
        [
            *DEFAULT_WIDGETS,
            widget.Systray(),
            SPACER,
            widget.CPU(format="Cpu: {load_percent}%"),
            SPACER,
            widget.Memory(format="{MemUsed: .0f}{mm}", fmt="M: {}"),
            SPACER,
            widget.Battery(
                format="{percent:2.0%} {hour:d}:{min:02d}",
                fmt="B: {}",
                notify_below=20,
            ),
            SPACER,
            widget.Net(
                format="N: {down:03.0f}{down_suffix:2} ↓↑ {up:03.0f}{up_suffix:2}",
                # prefix="k",
            ),
            SPACER,
            widget.KeyboardLayout(
                configured_keyboards=["fr", "us_qwerty-fr", "us"], fmt="K: {}"
            ),
            SPACER,
            widget.Clock(format="%a %d/%m/%Y %H:%M"),
            SPACER,
            widget.LaunchBar(
                progs=[
                    (
                        "/usr/share/icons/gnome/22x22/actions/system-log-out.png",
                        str(Path(__file__).parent / "byebye.sh"),
                        "Byebye",
                    ),
                ]
            ),
        ],
        24,
    ),
)

SUB = Screen(
    top=bar.Bar(
        [
            *DEFAULT_WIDGETS,
            widget.LaunchBar(progs=[("🔊", "pavucontrol", "audio settings")]),
            widget.Battery(
                format="{percent:2.0%} {hour:d}:{min:02d}",
                notify_below=20,
            ),
            widget.Clock(format="%a %d/%m/%Y %H:%M"),
        ],
        24,
    ),
)


def get_screens():
    screens_nb = int(subprocess.getoutput("xrandr --query | grep Screen | wc -l"))
    screens = [SUB] * (screens_nb - 1)
    screens.insert(screens_nb // 2, MAIN)

    return screens


print(get_screens())
