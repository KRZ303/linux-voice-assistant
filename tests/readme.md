# Automated testing

From the root of LVA run:-
```./script/tests```

The development scripts use the existing `.venv/bin/python3`, regardless of the shell's Python version.
On macOS, install `mpv` with Homebrew before running the tests.
The test launcher searches the standard Homebrew library directories unless `DYLD_FALLBACK_LIBRARY_PATH` is already set.
For a custom library location, set that variable inside an activated environment and invoke the interpreter directly:

```sh
source .venv/bin/activate
DYLD_FALLBACK_LIBRARY_PATH=/path/to/lib python script/tests
```

Run the JavaScript checks separately:

```sh
node --test tests/browser/*.test.mjs
```

# Manual testing

## Functions from HA side:

### Announcement:

Function in HA is: assist_satellite.announce

### TTS:

Function in HA is: tts.speak

## Play music from MA:

### Start and stop
Start playing a playlist. Check if it is playing. Stop playing. Check if it is stopped.

### Next track

Start playing a playlist. Check if it is playing. Next track. Check if it is playing.

### Pause

## Timer

Play music and then start a timer. Test if duck and unduck works. Test if unduck work when using wake word or stop word to stop the timer ringing.

