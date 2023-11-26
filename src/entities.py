import enum
from abc import ABCMeta, abstractmethod
from src.exceptions import ImpossibleAppointBlocksException


class Direction(enum.Enum):

    north = 'n'
    east = 'e'
    south = 's'
    west = 'w'


class City:

    def __init__(self, count_blocks_east, count_blocks_north, pizzerias):
        self._count_blocks_east = count_blocks_east
        self._count_blocks_north = count_blocks_north

        self._pizzerias = {}
        self._free_pizzeria_ids = []
        self._map = []

        self._preparing(pizzerias)

    def _preparing(self, pizzerias):
        self._init_pizzerias(pizzerias)
        self._init_map()

    def _init_pizzerias(self, pizzerias):
        for pizzeria in pizzerias:
            self._pizzerias[pizzeria.get_id()] = pizzeria

            if pizzeria.is_free():
                self._free_pizzeria_ids.append(pizzeria.get_id())

    def _init_map(self):
        self._map = [[0] * self._count_blocks_north for _ in range(self._count_blocks_east)]

        for pizzeria_id in self._pizzerias:
            block = self.get_block_pizzeria(pizzeria_id)

            coordinate_x = block.get_coordinate_x()
            coordinate_y = block.get_coordinate_y()

            self._map[coordinate_x - 1][coordinate_y - 1] = pizzeria_id

    def get_pizzerias(self):
        return tuple(self._pizzerias.values())

    def get_pizzeria_ids(self):
        return tuple(self._pizzerias.keys())

    def is_free_pizzeria(self, pizzeria_id):
        return self._pizzerias[pizzeria_id].is_free()

    def is_valid_block(self, block):
        return self._is_internal_block(block) and self._is_free_block(block)

    def _is_internal_block(self, block):
        coordinate_x = block.get_coordinate_x()
        coordinate_y = block.get_coordinate_y()

        is_internal_coordinate_x = self._count_blocks_east >= coordinate_x >= 1
        is_internal_coordinate_y = self._count_blocks_north >= coordinate_y >= 1

        return is_internal_coordinate_x and is_internal_coordinate_y

    def _is_free_block(self, block):
        coordinate_x = block.get_coordinate_x()
        coordinate_y = block.get_coordinate_y()

        return self._map[coordinate_x - 1][coordinate_y - 1] == 0

    def set_blocks(self, pizzeria_id, direction, count):
        self._pizzerias[pizzeria_id].add_serviced_blocks(direction, count)

        if not self._pizzerias[pizzeria_id].is_free():
            self._free_pizzeria_ids.remove(pizzeria_id)

        self._update_map(pizzeria_id, direction, count)

    def _update_map(self, pizzeria_id, direction, count):
        for offset in range(1, count + 1):
            offset_block = self.get_block_pizzeria_with_offset(pizzeria_id, direction, offset)

            offset_coordinate_x = offset_block.get_coordinate_x()
            offset_coordinate_y = offset_block.get_coordinate_y()

            self._map[offset_coordinate_x - 1][offset_coordinate_y - 1] = pizzeria_id

    def get_block_pizzeria_with_offset(self, pizzeria_id, direction, offset):
        block = self.get_block_pizzeria(pizzeria_id)

        coordinate_x = block.get_coordinate_x()
        coordinate_y = block.get_coordinate_y()

        block_with_offset = {
            Direction.north.value: Block(coordinate_x, coordinate_y + offset),
            Direction.east.value: Block(coordinate_x + offset, coordinate_y),
            Direction.south.value: Block(coordinate_x, coordinate_y - offset),
            Direction.west.value: Block(coordinate_x - offset, coordinate_y),
        }

        return block_with_offset[direction]

    def get_block_pizzeria(self, pizzeria_id):
        return self._pizzerias[pizzeria_id].get_block()

    def get_count_serviced_blocks_pizzeria(self, pizzeria_id, direction):
        return self._pizzerias[pizzeria_id].get_count_serviced_blocks(direction)

    def get_count_not_serviced_blocks_pizzeria(self, pizzeria_id):
        return self._pizzerias[pizzeria_id].get_count_not_serviced_blocks()

    def is_exists_free_pizzeria(self):
        return len(self._free_pizzeria_ids) != 0

    def get_free_pizzeria_ids(self):
        return self._free_pizzeria_ids


class Pizzeria:

    def __init__(self, id, block, capacity):
        self._id = id
        self._block = block
        self._capacity = capacity

        self._count_serviced_blocks_all = 0

        self._count_serviced_blocks = {
            Direction.north.value: 0,
            Direction.east.value: 0,
            Direction.south.value: 0,
            Direction.west.value: 0,
        }

    def get_id(self):
        return self._id

    def get_block(self):
        return self._block

    def get_count_serviced_blocks_to_north(self):
        return self._count_serviced_blocks[Direction.north.value]

    def get_count_serviced_blocks_to_east(self):
        return self._count_serviced_blocks[Direction.east.value]

    def get_count_serviced_blocks_to_south(self):
        return self._count_serviced_blocks[Direction.south.value]

    def get_count_serviced_blocks_to_west(self):
        return self._count_serviced_blocks[Direction.west.value]

    def is_free(self):
        return self.get_count_not_serviced_blocks() != 0

    def get_count_not_serviced_blocks(self):
        return self._capacity - self._count_serviced_blocks_all

    def get_count_serviced_blocks(self, direction):
        return self._count_serviced_blocks[direction]

    def add_serviced_blocks(self, direction, count):
        self._count_serviced_blocks[direction] += count

        self._count_serviced_blocks_all += count


class Block:

    def __init__(self, coordinate_x, coordinate_y):
        self._coordinate_x = coordinate_x
        self._coordinate_y = coordinate_y

    def get_coordinate_x(self):
        return self._coordinate_x

    def get_coordinate_y(self):
        return self._coordinate_y

    def is_equal(self, block):
        coordinate_x = block.get_coordinate_x()
        coordinate_y = block.get_coordinate_y()

        return self._coordinate_x == coordinate_x and self._coordinate_y == coordinate_y


class ManagerDelivery:

    def __init__(self, city):
        self._city = city

        self._algorithm = FreeBlockAlgorithm(self)

    def set_algorithm(self, algorithm):
        self._algorithm = algorithm

    def distribute(self):
        self._algorithm.run()

        if self._algorithm is not None and self.is_exists_free_pizzeria():
            self.distribute()

    def is_exists_free_pizzeria(self):
        return self._city.is_exists_free_pizzeria()

    def get_free_pizzeria_ids(self):
        return tuple(self._city.get_free_pizzeria_ids())

    def is_free_pizzeria(self, pizzeria_id):
        return self._city.is_free_pizzeria(pizzeria_id)

    def set_blocks(self, pizzeria_id, direction, count):
        self._city.set_blocks(pizzeria_id, direction, count)

    def get_block_pizzeria(self, pizzeria_id):
        return self._city.get_block_pizzeria(pizzeria_id)

    def is_valid_block(self, block):
        return self._city.is_valid_block(block)

    def get_count_not_serviced_blocks_pizzeria(self, pizzeria_id):
        return self._city.get_count_not_serviced_blocks_pizzeria(pizzeria_id)

    def get_count_serviced_blocks_pizzeria(self, pizzeria_id, direction):
        return self._city.get_count_serviced_blocks_pizzeria(pizzeria_id, direction)

    def get_pizzeria_ids(self):
        return self._city.get_pizzeria_ids()

    def get_block_pizzeria_with_offset(self, pizzeria_id, direction, offset):
        return self._city.get_block_pizzeria_with_offset(pizzeria_id, direction, offset)


class Algorithm:

    __metaclass__ = ABCMeta

    def __init__(self, manager_delivery):
        self._manager_delivery = manager_delivery

        self._directions = (
            Direction.north.value,
            Direction.east.value,
            Direction.south.value,
            Direction.west.value,
        )

    def run(self):
        self._appoint_blocks()

        next_algorithm = self._get_next_algorithm()

        self._manager_delivery.set_algorithm(next_algorithm)

    @abstractmethod
    def _appoint_blocks(self):
        pass

    @abstractmethod
    def _get_next_algorithm(self):
        pass

    def _get_next_conflict_block(self, pizzeria_id, other_pizzeria_id, direction, offset):
        if pizzeria_id == other_pizzeria_id:
            return None

        block = self._get_next_potential_block(pizzeria_id, direction, offset)

        if not self._manager_delivery.is_valid_block(block):
            return block

        if not self._is_potential_block(other_pizzeria_id, block):
            return None

        return block

    def _get_next_potential_block(self, pizzeria_id, direction, offset):
        count_serviced_blocks = self._manager_delivery.get_count_serviced_blocks_pizzeria(pizzeria_id, direction)

        offset += count_serviced_blocks

        block = self._manager_delivery.get_block_pizzeria_with_offset(pizzeria_id, direction, offset)

        return block

    def _is_potential_block(self, pizzeria_id, block):
        is_potential_block_by_x = self._is_potential_block_by_x(pizzeria_id, block)

        is_potential_block_by_y = self._is_potential_block_by_y(pizzeria_id, block)

        return is_potential_block_by_x or is_potential_block_by_y

    def _is_potential_block_by_x(self, pizzeria_id, block):
        block_pizzeria = self._manager_delivery.get_block_pizzeria(pizzeria_id)

        pizzeria_coordinate_x = block_pizzeria.get_coordinate_x()
        pizzeria_coordinate_y = block_pizzeria.get_coordinate_y()

        west = Direction.west.value
        east = Direction.east.value

        count_serviced_blocks_west = self._manager_delivery.get_count_serviced_blocks_pizzeria(pizzeria_id, west)
        count_serviced_blocks_east = self._manager_delivery.get_count_serviced_blocks_pizzeria(pizzeria_id, east)

        count_not_serviced_blocks = self._manager_delivery.get_count_not_serviced_blocks_pizzeria(pizzeria_id)

        min_x = pizzeria_coordinate_x - count_serviced_blocks_west - count_not_serviced_blocks
        max_x = pizzeria_coordinate_x + count_serviced_blocks_east + count_not_serviced_blocks

        return block.get_coordinate_y() == pizzeria_coordinate_y and min_x <= block.get_coordinate_x() <= max_x

    def _is_potential_block_by_y(self, pizzeria_id, block):
        block_pizzeria = self._manager_delivery.get_block_pizzeria(pizzeria_id)

        pizzeria_coordinate_x = block_pizzeria.get_coordinate_x()
        pizzeria_coordinate_y = block_pizzeria.get_coordinate_y()

        south = Direction.south.value
        north = Direction.north.value

        count_serviced_blocks_south = self._manager_delivery.get_count_serviced_blocks_pizzeria(pizzeria_id, south)
        count_serviced_blocks_north = self._manager_delivery.get_count_serviced_blocks_pizzeria(pizzeria_id, north)

        count_not_serviced_blocks = self._manager_delivery.get_count_not_serviced_blocks_pizzeria(pizzeria_id)

        min_y = pizzeria_coordinate_y - count_serviced_blocks_south - count_not_serviced_blocks
        max_y = pizzeria_coordinate_y + count_serviced_blocks_north + count_not_serviced_blocks

        return block.get_coordinate_x() == pizzeria_coordinate_x and min_y <= block.get_coordinate_y() <= max_y


class FreeBlockAlgorithm(Algorithm):

    def __init__(self, manager_delivery):
        super().__init__(manager_delivery)

    def _get_next_algorithm(self):
        return CrossConflictAlgorithm(self._manager_delivery)

    def _appoint_blocks(self):
        while True:
            is_appointed_blocks = False

            for pizzeria_id in self._manager_delivery.get_free_pizzeria_ids():
                for direction in self._directions:
                    count_free_blocks = self._get_count_free_blocks_by_direction(pizzeria_id, direction)

                    if count_free_blocks != 0:
                        self._manager_delivery.set_blocks(pizzeria_id, direction, count_free_blocks)

                        is_appointed_blocks = True

                        if not self._manager_delivery.is_free_pizzeria(pizzeria_id):
                            break

            if not self._manager_delivery.is_exists_free_pizzeria() or not is_appointed_blocks:
                break

    def _get_count_free_blocks_by_direction(self, pizzeria_id, direction):
        count_free_blocks = 0

        max_offset = self._manager_delivery.get_count_not_serviced_blocks_pizzeria(pizzeria_id)

        for offset in range(1, max_offset + 1):
            potential_block = self._get_next_potential_block(pizzeria_id, direction, offset)

            if not self._manager_delivery.is_valid_block(potential_block):
                return count_free_blocks

            if self._is_free_block(pizzeria_id, direction, offset):
                count_free_blocks = offset

        return count_free_blocks

    def _is_free_block(self, pizzeria_id, direction, offset):
        for other_pizzeria_id in self._manager_delivery.get_pizzeria_ids():
            next_conflict_block = self._get_next_conflict_block(pizzeria_id, other_pizzeria_id, direction, offset)

            if next_conflict_block is not None:
                return False

        return True


class CrossConflictAlgorithm(Algorithm):

    def __init__(self, manager_delivery):
        super().__init__(manager_delivery)
        
        self._count_swapped_blocks = 0

    def _get_next_algorithm(self):
        return FreeBlockAlgorithm(self._manager_delivery)

    def _appoint_blocks(self):
        for pizzeria_id in self._manager_delivery.get_free_pizzeria_ids():
            for direction in self._directions:
                self._swap_blocks_with_cross_conflict_by_direction(pizzeria_id, direction)
        
        if self._count_swapped_blocks == 0:
            raise ImpossibleAppointBlocksException()

    def _swap_blocks_with_cross_conflict_by_direction(self, pizzeria_id, direction):
        for other_pizzeria_id in self._manager_delivery.get_free_pizzeria_ids():
            for other_pizzeria_direction in self._directions:
                if self._is_cross_conflict(pizzeria_id, direction, other_pizzeria_id, other_pizzeria_direction):
                    self._swap_blocks(pizzeria_id, direction, other_pizzeria_id, other_pizzeria_direction)

                    return

    def _is_cross_conflict(self, pizzeria_id, direction, other_pizzeria_id, other_pizzeria_direction):
        block = self._get_next_conflict_block(pizzeria_id, other_pizzeria_id, direction, 1)

        if block is None or not self._manager_delivery.is_valid_block(block):
            return False

        other_block = self._get_next_conflict_block(other_pizzeria_id, pizzeria_id, other_pizzeria_direction, 1)

        if other_block is None or not self._manager_delivery.is_valid_block(other_block):
            return False

        if block.is_equal(other_block):
            return False

        return True

    def _swap_blocks(self, pizzeria_id, direction, other_pizzeria_id, other_pizzeria_direction):
        self._manager_delivery.set_blocks(pizzeria_id, direction, 1)
        self._manager_delivery.set_blocks(other_pizzeria_id, other_pizzeria_direction, 1)

        self._count_swapped_blocks += 2
