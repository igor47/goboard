# goboard #

`goboard.py` generates an svg file for a [go board](http://en.wikipedia.org/wiki/Go_(game)#Boards).
The resulting file is suitable to print your own board.
I used it on wood with a [laser cutter](http://en.wikipedia.org/wiki/Laser_cutting) to create a beautiful handmade board.
This is also a great example of how to use the [svgwrite](http://pypi.python.org/pypi/svgwrite/) library in python to create simple graphics.

## Usage ##

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
