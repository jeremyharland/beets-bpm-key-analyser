from beets.plugins import BeetsPlugin
import librosa
import eyed3  # or mutagen for FLAC files

class BpmAnalysisPlugin(BeetsPlugin):
    def __init__(self):
        super(BpmAnalysisPlugin, self).__init__()
        self.config.add({
            'auto': True,
            'overwrite': False  # Set to True if you want to overwrite existing BPM tags
        })

    def analyze_bpm(self, item):
        audio_path = item.path
        audio, sr = librosa.load(audio_path)

        # Calculate BPM
        bpm, _ = librosa.beat.beat_track(y=audio, sr=sr)

        # Add BPM to metadata
        try:
            if self.config['overwrite'].get(bool):
                item.bpm = bpm
                item.write()
            else:
                meta = eyed3.load(audio_path)
                meta.tag.bpm = bpm
                meta.tag.save()
        except Exception as e:
            self._log.error(f"Error adding BPM to {audio_path}: {e}")

    # def commands(self):
    #   cmd = self._commands  # Use self._commands instead of self._command
    #   cmd.parser.add_option(
    #       '-b', '--bpm', action='store_true',
    #       help='Calculate and add BPM to the file(s)')

    #   def func(lib, opts, args):
    #       for item in lib.items(args):
    #           self.analyze_bpm(item)

    #   cmd.func = func


