class HeatmapConfig:

    x_range = 1000
    y_range = 1000
    # These options are only beeing applied when redrawing
    heat_center_x = 400
    heat_center_y = 400
    heat_area_radius = 200
    graph_display_size_x = 800
    graph_display_size_y = 800
    force_rerendering = False
    # Cache for images with specific resolution
    image_file_base_name = "cache/heatmap_image_data"
