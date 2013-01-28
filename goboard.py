#!/usr/bin/python2

import argparse
import collections
import svgwrite
import sys

DefaultSizing = {
    'width':424.2,
    'length':454.5,
    'width_spacing':22,
    'length_spacing':23.7,
    'linewidth':1,
    'star_diameter':4,
    'unit':'mm'
    }

Sizes = collections.defaultdict(lambda: dict(DefaultSizing))
Sizes["Standard 19x19"].update({
  'lines':19,
  'star_points':((3,3), (3,9), (3, 15), (9, 3), (9, 9), (9, 15), (15, 3), (15, 9), (15, 15))
  })
Sizes["Standard 13x13"].update({
  'lines':13,
  'star_points':((3, 3), (3, 9), (6,6), (9, 3), (9, 9)),
  })
Sizes["Standard 9x9"].update({
  'lines':9,
  'star_points':((2, 2), (2,6), (5, 5), (6,2), (6,6)),
  })

class GoBoard(object):
  def __init__(self,
      width, length, width_spacing, length_spacing, linewidth,
      star_diameter, star_points, lines, unit):
    """Saves the parameters we're going to use to draw the board"""
    self.width = width
    self.length = length
    self.width_spacing = width_spacing
    self.length_spacing = length_spacing
    self.linewidth = linewidth
    self.star_diameter = star_diameter
    self.star_points = star_points
    self.lines = lines
    self.unit = unit

    self.drawing = None

  def draw(self, draw_border = True):
    """draws the go board using current dimentions"""
    drawing = svgwrite.Drawing(size=(
      "%f%s" % (self.width, self.unit),
      "%f%s" % (self.length, self.unit)),
      viewBox = ('0 0 %d %d' % (self.width, self.length)))

    self.drawing = drawing

    # create an initial rectangle around the drawing
    stroke = "black" if draw_border else "white"
    border = drawing.rect(size=(self.width, self.length), stroke = stroke, fill = 'white')
    drawing.add(border)

    # how much room from the edge to the first horizontal line?
    total_y_space = (self.lines - 1) * (self.linewidth + self.length_spacing)
    y_margin = (self.length - total_y_space) / 2

    total_x_space = (self.lines - 1) * (self.linewidth +  self.width_spacing)
    x_margin = (self.width - total_x_space) / 2

    start = (x_margin, y_margin)
    self.draw_lines(start, self.lines, 'across', self.linewidth, total_x_space, self.length_spacing)
    self.draw_lines(start, self.lines, 'down', self.linewidth, total_y_space, self.width_spacing)

    self.draw_starpoints(start)

  def draw_starpoint(self, pos):
    star = self.drawing.circle(pos, r=self.star_diameter)
    star['fill'] = 'black'
    self.drawing.add(star)

  def draw_starpoints(self, grid_start):
    """Draws the star points"""
    wspace = self.linewidth + self.width_spacing
    lspace = self.linewidth + self.length_spacing

    for point in self.star_points:
      center = (grid_start[0] + point[0] * wspace, grid_start[1] + point[1] * lspace)
      self.draw_starpoint(center)

  def draw_lines(self, start, count, direction, width, length, spacing):
    """Draws a bunch of lines

    start is a tuple of two values
    direction should be 'down' or 'across'
    """
    start = list(start)
    if len(start) != 2:
      raise ValueError("start must be a tuple of 2 values")

    for i in xrange(count):
      end = list(start)
      if direction == 'down':
        end[1] += length
      else:
        end[0] += length

      line = self.drawing.line(start=start, end=end)
      line['stroke'] = 'black'
      line['stroke-width'] = width
      self.drawing.add(line)

      if direction == 'down':
        start[0] += spacing + width
      else:
        start[1] += spacing + width

  def write(self, filename):
    """writes the svg rendering into a file"""
    if not self.drawing:
      self.draw()

    self.drawing.saveas(filename)

  def tostring(self):
    if self.drawing:
      return self.drawing.tostring()
    else:
      return ""

def main():
  parser = argparse.ArgumentParser(
      description="Generate an SVG file defining a go board",
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument("--size", default="Standard 19x19", choices=Sizes.keys(),
      help="Size of go board to generate")
  parser.add_argument("-o", "--output", default="goboard.svg",
      help="Output filename")

  opts = parser.parse_args()
  b = GoBoard(**Sizes[opts.size])
  b.write(opts.output)

if __name__ == "__main__":
  sys.exit(main())

