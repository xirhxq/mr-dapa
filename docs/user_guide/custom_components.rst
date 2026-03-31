Custom Components
=================

To create your own visualization component, subclass
:class:`~mr_dapa.BaseComponent` and implement the ``_initialize()`` method.

Basic Example
-------------

.. code-block:: python

   from mr_dapa import BaseComponent, register_component

   class BarComponent(BaseComponent):
       """Horizontal bar chart showing final values."""

       FIGSIZE = (8, 4)
       expand = False
       required_config_keys = {'keys': list}

       def __init__(self, ax, interpreter, title="", mode='static', **kwargs):
           super().__init__(ax, interpreter, title=title, mode=mode, **kwargs)
           self.keys = self.kwargs['keys']
           self._initialize()

       def _initialize(self):
           self.ax.set_title(self.title)
           # Get final value for each robot
           robots = []
           values = []
           for robot in self.interpreter.data:
               for value in robot['values']:
                   if value['alias'] in self.keys:
                       robots.append(f"Robot #{robot['id']}")
                       values.append(value['value'][-1])

           self.ax.barh(robots, values)

       def update(self, timestamp):
           # Not implemented for static component
           return []

   # Register the component
   register_component('Bar', BarComponent)

Using Custom Components
-----------------------

After registering, use your component like any built-in:

.. code-block:: python

   components = {
       'bar': {
           'title': 'Final Values',
           'class': 'Bar',
           'keys': ['x']
       }
   }

   drawer = mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components)
   drawer.draw(['bar'])

Config Validation
-----------------

Use ``required_config_keys`` to validate configuration at drawer init:

.. code-block:: python

   class MyComponent(BaseComponent):
       required_config_keys = {
           'keys': list,      # Required, must be a list
           'threshold': float  # Optional, can be any type
       }

This ensures users get clear error messages when configuration is missing.

See the ``examples/custom_component/`` directory for a complete working example.
