# wall
wall_side_cm = 200
pix_per_cm = 1

# doors
door_height_cm = wall_side_cm * 0.8
door_width_cm = wall_side_cm / 2

# window
window_height_cm = wall_side_cm * 0.6

# merlon
merlon_count = 3  # number of merlons in a battlement piece
merlon_width_cm = wall_side_cm / (merlon_count * 2)
merlon_height_cm = merlon_width_cm * 1.3

# battlement
battlement_height_cm = wall_side_cm / 2
support_count = 6  # number of supports in a battlement piece
support_width_cm = wall_side_cm / (support_count * 3)
support_height_cm = (battlement_height_cm - merlon_height_cm) * 0.6

# roof
roof_width = wall_side_cm * pix_per_cm
roof_height = roof_width / 3