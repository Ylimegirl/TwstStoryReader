# Twst Story Reader
[XLSX Build](https://github.com/Ylimegirl/TwstStoryReader/tree/xlsx)

Inspired by [050644zf's ArknightsStoryTextReader](https://github.com/050644zf/ArknightsStoryTextReader), but shares little to no code with it, as I primarily made this myself after teaching myself the basics of Python in 5 or so hours.

To use, place the .JSON files you want parsed inside an "inputs" directory, and then run in the command line:

```python reader.py```

## Compatiblity with English server
This script, while primarily designed and used for the Japanese server files, will also work with the story files for the English server, with the following caveats:
- The parser will still replace the text `[HERO_NAME]` included in story files with the default Japanese name, ユウ, rather than the default English name, Yu
- The parser will still attempt to search for basic Japanese terms to find and replace even if they're not at all present, potentially leading to redundant effort--which, considering how relatively lightweight this script is, probably isn't too big of an issue
- Like with the Japanese server files, this parser could stop working at any time with any files if the devs make changes to the file format on their end

## Known issues
- May miss certain types of flavor text
- Output could use some retooling in formatting