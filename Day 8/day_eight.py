from day_eight_input import PUZZLE_INPUT, EXAMPLE_PUZZLE_INPUT


class Grove:
    def __init__(self, trees: list) -> None:
        self.trees = trees

    @property
    def transposed_trees(self) -> list:
        """Returns tree list transposed so rows and columns and columns are rows"""
        return list(zip(*self.trees))

    def __get_tree_lines(self, row_id, column_id) -> list:
        """Returns list of tree lines and index of tree"""
        return [
            (self.trees[row_id], column_id),
            (self.trees[row_id][::-1], len(self.trees[row_id]) - 1 - column_id),
            (self.transposed_trees[column_id], row_id),
            (
                self.transposed_trees[column_id][::-1],
                len(self.transposed_trees[column_id]) - 1 - row_id,
            ),
        ]

    def count_visible_trees(self) -> int:
        """Return number of visible trees"""
        total = 0
        for row_id, row in enumerate(self.trees):
            for column_id, _ in enumerate(row):
                total += self.is_visible(row_id, column_id)
        return total

    def is_visible(self, row_id: int, column_id: int) -> bool:
        """Returns True if tree is visible from at least one direction"""
        tree_lines = self.__get_tree_lines(row_id, column_id)
        return any(self.is_visible_in_line(*tree_line) for tree_line in tree_lines)

    def is_visible_in_line(self, tree_line: list, tree_index: int) -> bool:
        """Returns True if tree is visible from left to right in tree_line"""
        highest_tree = -1
        for position, tree_height in enumerate(tree_line):
            if position == tree_index:
                return tree_height > highest_tree
            highest_tree = max(highest_tree, tree_height)
        return False


def main():
    trees = [list(map(int, list(row))) for row in PUZZLE_INPUT.splitlines()]
    my_grove = Grove(trees)
    print(my_grove.count_visible_trees())


if __name__ == "__main__":
    main()
