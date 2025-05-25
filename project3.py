def parse_gwc(file_path):
    """Read a GWC file and return a dict mapping height → list of (frequency, A, k) tuples."""
    with open(file_path, 'r') as file:
        raw_lines = [ln.strip() for ln in file if ln.strip()]

    # Header line: [ignored, num_heights, num_directions, ...]
    header_vals = list(map(int, raw_lines[1].split()))
    _, height_count, direction_count = header_vals

    # Sector frequencies and measurement heights
    sector_frequencies = list(map(float, raw_lines[4].split()))
    altitude_list = list(map(float, raw_lines[3].split()))

    # Prepare storage
    results_dict = {int(alt): [] for alt in altitude_list}

    # Data starts at line index 5: alternating A and k lines per direction
    base_index = 5
    for dir_idx in range(direction_count):
        a_values = list(map(float, raw_lines[base_index + 2*dir_idx].split()))
        k_values = list(map(float, raw_lines[base_index + 2*dir_idx + 1].split()))
        freq = (
            sector_frequencies[dir_idx]
            if dir_idx < len(sector_frequencies)
            else 1.0 / direction_count
        )

        for lvl_idx, altitude in enumerate(altitude_list):
            results_dict[int(altitude)].append(
                (freq, a_values[lvl_idx], k_values[lvl_idx])
            )

    return results_dict


def display_gwc_data(gwc_data):
    """Pretty‑print the GWC statistics by height and direction."""
    for altitude, measurements in gwc_data.items():
        print(f"Height: {altitude} m")
        for dir_idx, (freq, a, k) in enumerate(measurements):
            angle = dir_idx * 30
            print(f"  {angle:>3}° │ f={freq:.3f}, A={a:.3f}, k={k:.3f}")
        print()  # blank line between heights


if __name__ == "__main__":
    print("Vineyard Wind data:")
    vineyard_data = parse_gwc("Vineyard_Wind_GWC.lib")
    display_gwc_data(vineyard_data)

    print("Sofia data:")
    sofia_data = parse_gwc("sofia_gwc.lib")
    display_gwc_data(sofia_data)
