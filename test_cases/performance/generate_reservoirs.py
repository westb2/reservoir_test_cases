import random

# domain configurations

def generate_random_location(nx, ny, dx, dy):
    x = float(random.randint(0, nx-1)) * dx + dx/2.
    y = float(random.randint(0, ny-1)) * dy + dy/2.
    return (x,y)


def generate_reservoirs():
    dx = 10.
    dy = 10.
    nx = 500
    ny = 500
    slope_x = -.01
    reservoir_configurations = [0,1,10,100,1000,10000]
    header = "key,Intake_X,Intake_Y,Release_X,Release_Y,Has_Secondary_Intake_Cell,\
        Secondary_Intake_X,Secondary_Intake_Y,Max_Storage,Storage,\
            Min_Release_Storage,Release_Rate\n"
    for number_of_reservoirs in reservoir_configurations:
        random.seed(0)
        reservoir_locations = set()
        for reservoir in range(0,number_of_reservoirs):
            (x,y) = generate_random_location(nx, ny, dx, dy)
            reservoirs_overlap = (x,y) in reservoir_locations \
                or (x+dx,y) in reservoir_locations \
                or (x-dx,y) in reservoir_locations
            while reservoirs_overlap:
                (x,y) = generate_random_location(nx, ny, dx, dy)
                reservoirs_overlap = (x,y) in reservoir_locations \
                    or (x+dx,y) in reservoir_locations \
                    or (x-dx,y) in reservoir_locations
            reservoir_locations.add((x,y))
        with open(f"reservoir_files/{number_of_reservoirs}_reservoirs_releasing.csv", "w") as file:
            file.write(header)
            for reservoir_number, (x,y) in enumerate(reservoir_locations):
                line = f"reservoir_{reservoir_number},{x},{y},{x+dx},{y},-1,-1,-1,10000,5000,0,10\n"
                file.write(line)
        with open(f"reservoir_files/{number_of_reservoirs}_reservoirs_not_releasing.csv", "w") as file:
            file.write(header)
            for reservoir_number, (x,y) in enumerate(reservoir_locations):
                line = f"reservoir_{reservoir_number},{x},{y},{x+dx},{y},-1,-1,-1,10000,5000,0,0\n"
                file.write(line)


