Styling
========

Customize plot appearance using style presets, color palettes, and
export formats.

Style Presets
-------------

Three built-in presets are available:

**paper** - Publication-ready plots
* High DPI (300)
* Compact size (8x6 inches)
* Clean, professional appearance

**presentation** - Projector-friendly
* Large figure (16x9)
* Bold fonts
* High contrast

**dark** - Dark background theme
* Dark background with light text
* Suitable for dark mode interfaces

.. code-block:: python

   drawer.set_style('paper')
   drawer.set_style('presentation')
   drawer.set_style('dark')

Color Palettes
--------------

Four built-in color palettes:

* **default** - matplotlib tab10
* **colorblind** - Wong's palette (colorblind-friendly)
* **vivid** - High saturation colors
* **muted** - Desaturated, professional colors

.. code-block:: python

   drawer.set_palette('colorblind')
   drawer.set_palette('vivid')

Combining Styles and Palettes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Chain style and palette configuration:

.. code-block:: python

   (mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components)
       .set_style('presentation')
       .set_palette('colorblind')
       .draw(['x', 'map'], save=True))

Export Formats
--------------

Control output format via the style object:

.. code-block:: python

   # PNG (default)
   drawer.style.format = 'png'

   # SVG (vector graphics)
   drawer.style.format = 'svg'

   # PDF (vector format)
   drawer.style.format = 'pdf'
