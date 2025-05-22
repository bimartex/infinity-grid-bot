def generate_grid(current_price, grid_size, percent_range):
    grid = []
    step = current_price * percent_range / 100
    for i in range(-grid_size, grid_size + 1):
        grid.append(round(current_price + i * step, 2))
    return sorted(set(grid))
