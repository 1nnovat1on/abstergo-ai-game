import winsound


def tone(freq=144, dur=200):
    try:
        winsound.Beep(int(freq), dur)
    except Exception:
        print("\a", end="")
