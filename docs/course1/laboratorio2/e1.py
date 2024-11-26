from pytamaro import show_graphic
from castle_components import drawbridge
from drawbridge_states import opened, closed  # The possible states


# Close the drawbridge!
closed_drawbridge = drawbridge(closed)

show_graphic(closed_drawbridge)
