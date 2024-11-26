# === Code Cell 1 ===
from pytamaro import show_graphic
from castle_components import drawbridge
from drawbridge_states import opened, closed  # The possible states


open_drawbridge = drawbridge(opened)

show_graphic(open_drawbridge)

# === Code Cell 2 ===
from pytamaro import show_graphic
from castle_components import drawbridge
from drawbridge_states import opened, closed  # The possible states


# Close the drawbridge!
closed_drawbridge = drawbridge(...)

show_graphic(closed_drawbridge)
