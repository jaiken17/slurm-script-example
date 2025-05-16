import numpy as np

def get_initial_conditions():
    initial_conditions_file = 'initial_conditions.txt'
    values = {}

    with open(initial_conditions_file, 'r') as file:
        for line in file:
            line = line.strip()
            
            # Skip empty lines or comments
            if not line or line.startswith("#"):
                continue

            if '=' in line:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    name = parts[0].strip()
                    value_str = parts[1].strip()
                    try:
                        value = float(value_str)
                        values[name] = value
                        if len(values) == 3:
                            break
                    except ValueError:
                        # Skip lines where value isn't a float
                        continue

    return values



def main(initial_conditions):

    # Constants
    g = 9.81  # gravity (m/s^2)

    # Initial conditions
    x0 = 0.0         # initial x position (m)
    y0 = 0.0         # initial y position (m)
    v0 = initial_conditions["v0"]        # initial speed (m/s)
    angle_deg = initial_conditions["angle_deg"] # launch angle (degrees)

    # Convert angle to radians
    angle_rad = np.radians(angle_deg)
    vx0 = v0 * np.cos(angle_rad)
    vy0 = v0 * np.sin(angle_rad)

    # Time setup
    dt = initial_conditions["dt"]        # time step (s)
    t_max = 10.0     # max simulation time (s)

    # Initialize state
    t = 0.0
    x, y = x0, y0
    vx, vy = vx0, vy0

    # Open output file
    filename = 'output.data'
    file = open(filename, 'w')

    # Header
    print(f"{'Time (s)':>8} {'X (m)':>10} {'Y (m)':>10} {'Vx (m/s)':>10} {'Vy (m/s)':>10}",file=file)

    # Integration loop
    while y >= 0 and t <= t_max:
        print(f"{t:8.2f} {x:10.3f} {y:10.3f} {vx:10.3f} {vy:10.3f}", file=file)
        
        # Update position
        x += vx * dt
        y += vy * dt
        
        # Update velocity
        vy -= g * dt  # Only vy changes, vx remains constant
        
        # Update time
        t += dt


if __name__ == '__main__':

    initial_conditions = get_initial_conditions()
    main(initial_conditions)