#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import sys

import mpv


def mpv_log(loglevel, component, message):
    print(f"[{loglevel}] {component}: {message.strip()}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} Directory Scene1 [Scene2] [...]")
        sys.exit(1)
    _, directory, *scenes = sys.argv
    os.chdir(directory)

    player = mpv.MPV(
        log_handler=mpv_log, input_default_bindings=True, input_vo_keyboard=True
    )
    player.fullscreen = True
    player.loop_playlist = False
    player.keep_open = "always"
    player.osc = False
    player.osd_bar = False

    play_data = []
    for scene in scenes:
        with open(f"{scene}.json") as f:
            play_data.extend(json.load(f))

    for slide in play_data:
        player.playlist_append(slide["video"])

    player.playlist_play_index(0)
    player.pause = True

    @player.property_observer("pause")
    def pause_observer(_name, value):
        if value:
            idx = player.playlist_pos
            if play_data[idx]["type"] == "default.loop":
                # Loop
                player.seek(0, "absolute")
                player.playlist_play_index(idx)
                player.pause = False
            else:
                # Just pause, queue next playlist entry
                if idx < len(play_data) - 1:
                    player.playlist_next()
                else:
                    player.show_text("End of presentation", 5000)

    player.wait_for_shutdown()
