import copy
import random as rand
from typing import Callable, List

from word import Constraint, Word


class RecursiveBacktracker:
    def __init__(
        self,
        heuristic: str = "mrv",
        forward_checking: bool = True,
        used_values: List[Word] = None,
    ):
        self.heuristic = heuristic
        self.forward_checking = forward_checking
        self.select_unassigned_variable = RecursiveBacktracker._get_selection_function(
            heuristic
        )
        self.used_values = (
            used_values if used_values is not None else []
        )  # ChatGPT line to fix a bug
        self.dead_ends_avoided = 0
        self.recursive_calls = 0
        self.values_tried = 0

    def __str__(self):
        output = f"Stats:\n"
        output += (
            f"--------------------------------------------------------------------\n"
        )
        output += f"Detected and avoided {self.dead_ends_avoided} dead ends.\n"
        output += f"Executed {self.recursive_calls} recursive calls.\n"
        output += f"Tried a total of {self.values_tried} values."
        return output

    def recursive_backtracking(self, assignment: List[Word]):
        self.recursive_calls += 1

        if RecursiveBacktracker._is_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in (
            v for v in var.domain if v not in self.used_values
        ):  # ChatGPT line
            self.values_tried += 1

            dead_end = False

            if RecursiveBacktracker._satisfies_constraints(value, var):
                dead_end, new_domains, old_domains = self._generate_new_domains(
                    var, value
                )

                if not dead_end:
                    self._apply_assignment(var, value, new_domains)

                    result = self.recursive_backtracking(assignment)

                    if result != None:
                        return result
                    else:
                        self._undo_assignment(var, value, old_domains)

        return None

    def _generate_new_domains(self, var: Word, value: str):
        old_domains = []
        new_domains = []
        dead_end = False

        for constraint in var.constraints:
            other_word = constraint.other_word
            if constraint.other_word.letters == None:
                updated_domain = RecursiveBacktracker._update_other_domain(
                    value, constraint
                )
                old_domains.append((other_word, other_word.domain))
                new_domains.append((other_word, updated_domain))
                if self.forward_checking and len(updated_domain) == 0:
                    dead_end = True
                    self.dead_ends_avoided += 1
                    break
        return dead_end, new_domains, old_domains

    def _apply_assignment(self, var: Word, value: str, new_domains):
        var.letters = value
        self.used_values.append(value)

        for word, new_domain in new_domains:
            word.domain = new_domain

    def _undo_assignment(self, var: Word, value: str, old_domains):
        var.letters = None
        self.used_values.remove(value)

        for word, old_domain in old_domains:
            word.domain = old_domain

    @staticmethod
    def _get_selection_function(heuristic: str) -> Callable[[List["Word"]], "Word"]:
        if heuristic in (
            "mrv",
            "MRV",
            "minimum_remaining_values",
            "minimum_remaining",
            "min_rem",
        ):
            return RecursiveBacktracker._minimum_remaining_values
        elif heuristic in ("degree", "deg", "d"):
            return RecursiveBacktracker._degree_heuristic
        elif heuristic in (
            "mrv+degree",
            "mrv_degree",
            "mrv_deg",
            "mrv-degree",
            "mrv-deg",
        ):
            return RecursiveBacktracker._minimum_remaining_and_degree
        else:
            return RecursiveBacktracker._first_unassigned

    @staticmethod
    def _is_complete(assignment: List[Word]):
        for word in assignment:
            if word.letters == None:
                return False
        return True

    @staticmethod
    def _satisfies_constraints(value: str, variable: Word):
        for constraint in variable.constraints:
            other_value = constraint.other_word.letters
            if (
                other_value != None
                and value[constraint.index_self] != other_value[constraint.index_other]
            ):
                return False
        return True

    @staticmethod
    def _first_unassigned(assignment: List[Word]):
        for word in assignment:
            if word.letters == None:
                return word
        return None

    @staticmethod
    def _minimum_remaining_values(assignment: List[Word]):
        minimum_remaining = -1
        selection = None

        for word in (w for w in assignment if w.letters == None):
            remaining = len(word.domain)
            if minimum_remaining == -1 or remaining < minimum_remaining:
                minimum_remaining = remaining
                selection = word

        return selection

    @staticmethod
    def _degree_heuristic(assignment: List[Word]):
        most_constraints = -1
        selection = None

        for word in (w for w in assignment if w.letters == None):
            constraint_count = len(word.constraints)
            if constraint_count > most_constraints:
                most_constraints = constraint_count
                selection = word

        return selection

    @staticmethod
    def _minimum_remaining_and_degree(assignment: List[Word]):
        minimum_remaining = -1
        selection = []

        for word in (w for w in assignment if w.letters == None):
            remaining = len(word.domain)
            if minimum_remaining == -1 or remaining < minimum_remaining:
                minimum_remaining = remaining

        for word in (w for w in assignment if w.letters == None):
            remaining = len(word.domain)
            if remaining == minimum_remaining:
                selection.append(word)

        most_constraints = -1
        final_choice = None

        for choice in selection:
            constraint_count = len(choice.constraints)
            if constraint_count > most_constraints:
                most_constraints = constraint_count
                final_choice = choice

        return final_choice

    @staticmethod
    def _update_other_domain(value: str, constraint: Constraint):
        other_word = constraint.other_word
        old_domain = other_word.domain
        critical_index = constraint.index_other
        critical_char = value[constraint.index_self]

        new_domain = [
            value for value in old_domain if value[critical_index] == critical_char
        ]

        return new_domain
