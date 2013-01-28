# goboard #

Creates an svg file for a go board, suitable for a laser printer.
You will need svgwrite to use this program:

```bash
  pip install svgwrite
```

To use, simply run from the command line:

```bash
  python goboard.py
```

There are a few command line options which allow you pick where to write the file, and what kind of board to generate.
A `-h` flag will show all the options.
Here's an example:

```bash
  python goboard.py --size="Standard 13x13" --output="13x13board.svg"
```
