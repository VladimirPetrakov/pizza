from src.exceptions import CustomException, InvalidCountCityBlocksDirectionException, InvalidCountPizzeriasException, \
    InvalidCoordinateBlockException
from src.entities import City, Pizzeria, Block, ManagerDelivery


def main():
    cities = build_cities()

    distribute_delivery(cities)

    print_delivery_cities(cities)


def build_cities():
    cities = []
    count_cities = 0

    while True:
        if count_cities == 50:
            break

        input_line = input()

        if input_line == '0':
            break

        n, m, k = map(int, input_line.split())

        check_valid_city(n, m, k)

        pizzerias = []

        for i in range(0, k):
            input_line = input()
            x, y, c = map(int, input_line.split())

            check_valid_coordinate_block(x, n)
            check_valid_coordinate_block(y, m)

            pizzerias.append(Pizzeria(i + 1, Block(x, y), c))

        cities.append(City(n, m, pizzerias))
        count_cities += 1

    return cities


def check_valid_city(count_blocks_east, count_blocks_north, count_pizzerias):
    if count_blocks_east < 1 or count_blocks_east > 30:
        raise InvalidCountCityBlocksDirectionException(count_blocks_east, 30)

    if count_blocks_north < 1 or count_blocks_north > 30:
        raise InvalidCountCityBlocksDirectionException(count_blocks_north, 30)

    if count_pizzerias < 1 or count_pizzerias > 200:
        raise InvalidCountPizzeriasException(count_pizzerias, 200)


def check_valid_coordinate_block(coordinate, max_coordinate):
    if coordinate < 1 or coordinate > max_coordinate:
        raise InvalidCoordinateBlockException(coordinate, max_coordinate)


def distribute_delivery(cities):
    for city in cities:
        manager_delivery = ManagerDelivery(city)
        manager_delivery.distribute()


def print_delivery_cities(cities):
    count_cities = len(cities)

    for i in range(0, count_cities):
        print('Case {}:'.format(i + 1))

        pizzerias = cities[i].get_pizzerias()

        for pizzeria in pizzerias:
            print_delivery_pizzeria(pizzeria)

        print("\n", end="")


def print_delivery_pizzeria(pizzeria):
    north = pizzeria.get_count_serviced_blocks_to_north()
    east = pizzeria.get_count_serviced_blocks_to_east()
    south = pizzeria.get_count_serviced_blocks_to_south()
    west = pizzeria.get_count_serviced_blocks_to_west()

    str_pizzeria = '{} {} {} {}'.format(north, east, south, west)

    print(str_pizzeria)


if __name__ == '__main__':
    try:   
        main()
    except CustomException as e:
        print(e.message)
