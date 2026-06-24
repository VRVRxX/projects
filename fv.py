import sys
import os

def set_volume_100():
    if sys.platform.startswith("win"):
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(1.0, None)

    elif sys.platform.startswith("linux"):
        os.system("pactl set-sink-volume @DEFAULT_SINK@ 150%")

set_volume_100()

import os
import sys
import tkinter as tk

import vlc

VIDEO_PATH = "rickroll.mp4"


class VideoPlayer:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.player = None

        self.root.title("Video Player")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")

        # Frame that VLC will render its video output into
        self.video_frame = tk.Frame(self.root, bg="black")
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        if not os.path.exists(VIDEO_PATH):
            tk.Label(
                self.root,
                text=f"Could not find '{VIDEO_PATH}' in this folder. Press Esc to quit.",
                font=("Arial", 20),
                fg="white",
                bg="black",
            ).place(relx=0.5, rely=0.5, anchor="c")
        else:
            self._setup_vlc()

        # Normal exit path - Esc just closes the app like any well-behaved
        # fullscreen application. Nothing else is touched.
        self.root.bind("<Escape>", lambda e: self.close())
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def _setup_vlc(self):
        # On Linux, "--no-xlib" avoids a common threading issue between
        # libVLC and Tkinter when both try to talk to X11. We also pass
        # "--avcodec-hw=none" to force software decoding - otherwise VLC
        # tries to use the VDPAU hardware decoder, which needs Xlib, and
        # that conflicts with --no-xlib (this is what was causing the
        # "Failed to create video converter" / "Xlib is required for
        # VDPAU" errors).
        if sys.platform.startswith("linux"):
            self.instance = vlc.Instance("--no-xlib", "--avcodec-hw=none")
        else:
            self.instance = vlc.Instance()

        self.player = self.instance.media_player_new()
        media = self.instance.media_new(VIDEO_PATH)
        self.player.set_media(media)

        # Embed VLC's video output into our Tkinter frame.
        # This is the part that differs by platform.
        self.root.update_idletasks()
        handle = self.video_frame.winfo_id()

        if sys.platform.startswith("win"):
            self.player.set_hwnd(handle)
        elif sys.platform.startswith("linux"):
            self.player.set_xwindow(handle)
        elif sys.platform == "darwin":
            self.player.set_nsobject(handle)
        else:
            raise RuntimeError(f"Unsupported platform: {sys.platform}")

        self.player.play()

        # Loop the video instead of stopping on a black screen when it ends
        self.events = self.player.event_manager()
        self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self._on_end_reached)

    def _on_end_reached(self, event):
        # This callback runs on a VLC-internal thread, so just re-trigger
        # playback rather than doing anything heavier here.
        self.player.stop()
        self.player.play()

    def close(self):
        try:
            if self.player is not None:
                self.player.stop()
        except Exception:
            pass
        self.root.destroy()


def main():
    root = tk.Tk()
    VideoPlayer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
