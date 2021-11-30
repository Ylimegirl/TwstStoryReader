# Twst Story Reader
Inspired by [050644zf's ArknightsStoryTextReader](https://github.com/050644zf/ArknightsStoryTextReader), but shares little to no code with it, as I primarily made this myself after teaching myself the basics of Python in 5 or so hours.

To use, place the .JSON files you want parsed inside an "inputs" directory, and then run in the command line:

```python xlsxreader.py```

**The xlsx build will only work if you have [openpyxl](https://openpyxl.readthedocs.io/en/stable/#) installed**. If you do not have this installed, run `pip install openpyxl` first.

## Known issues
- May miss certain types of flavor text
- xlsx outputs may miss content the txt outputs include