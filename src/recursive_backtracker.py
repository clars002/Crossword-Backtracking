"""
The RecursiveBacktracker class that arbitrates the entire search.
"""

import copy
import random as rand
from typing import Callable, List

from word import Constraint, Word


class RecursiveBacktracker:
    """
    Class that arbitrates the solution search for the CSP.

    Contains several optional heuristics (MRV, Degree, MRV+Degree)
    and toggleable forward checking.

    Attributes:
        heuristic (str):
            The heuristic used when selecting the next unassigned
            variable.
        forward_checking (bool): Whether to use forward checking.

    Methods:
        recursive_backtracking(self, assignment: List[Word])
        -> List[Word]:
            Performs the recursive backtracking search on the set
            of variables provided in the assignment argument.
    """

    def __init__(
        self,
        heuristic: str = "mrv",
        forward_checking: bool = True,
    ):
        self.heuristic = heuristic
        self.forward_checking = forward_checking
        # Private attributes:
        self._select_unassigned_variable = RecursiveBacktracker._get_selection_function(
            heuristic
        )
        self._used_values = []
        self._dead_ends_avoided = 0
        self._recursive_calls = 0
        self._values_tried = 0

    def __str__(self):
        """
        Outputs stats from the backtracking search.

        Returns:
            str: String containing several stats from the search.
        """
        output = f"Stats:\n"
        output += f"-----------------------------------------------------\n"
        output += f"Detected and avoided {self._dead_ends_avoided} dead ends.\n"
        output += f"Executed {self._recursive_calls} recursive calls.\n"
        output += f"Tried a total of {self._values_tried} values."
        return output

    def recursive_backtracking(self, assignment: List[Word]) -> List[Word]:
        """
        Performs the recursive backtracking search on the CSP.

        All the requisite CSP info is provided in the assignment param,
        assuming that the words therein have populated number,
        orientation, start position, and length.

        Args:
            assignment (List[Word]):
                The list of variables with pending assignment (i.e.
                Word objects with unassigned letters). Expected to have
                all members assigned except letters.

        Returns:
            List[Word]:
                The list of variables with their final assignments
                (i.e. the Word objects with letters assigned so that
                all constraints are satisfied).
        """

        self._recursive_calls += 1

        if RecursiveBacktracker._is_complete(assignment):
            return assignment

        var = self._select_unassigned_variable(assignment)

        for value in (
            v for v in var.domain if v not in self._used_values
        ):  # ChatGPT line; iterate over only values not already used
            self._values_tried += 1

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
        """
        Generate new domains for all variables affected by the
        assignment of value to var, while keeping a record of the prior
        domains to enable backtracking if necessary.

        If self.forward_checking is True, resulting dead ends will
        be detected and reported.
        """
        old_domains = []
        new_domains = []
        dead_end = False

        for constraint in var.constraints:
            other_word = constraint.other_word
            if constraint.other_word.letters == None:
                updated_domain = RecursiveBacktracker.generate_new_domain(
                    value, constraint
                )
                # Keep the words and their domains together to
                # facilitate future re-assignment
                old_domains.append((other_word, other_word.domain))
                new_domains.append((other_word, updated_domain))
                if self.forward_checking and len(updated_domain) == 0:
                    dead_end = True
                    self._dead_ends_avoided += 1
                    break

        # Return old domains along with new domains for backtracking:
        return dead_end, new_domains, old_domains

    @staticmethod
    def generate_new_domain(value: str, constraint: Constraint):
        """
        Generates a new domain for the other_word specified in
        constraint after the assignment of value to the
        co-constrained word.
        """

        other_word = constraint.other_word
        old_domain = other_word.domain
        critical_index = constraint.index_other
        critical_char = value[constraint.index_self]

        new_domain = [
            value for value in old_domain if value[critical_index] == critical_char
        ]

        return new_domain

    def _apply_assignment(self, var: Word, value: str, new_domains):
        var.letters = value
        self._used_values.append(value)

        for word, new_domain in new_domains:
            word.domain = new_domain

    def _undo_assignment(self, var: Word, value: str, old_domains):
        var.letters = None
        self._used_values.remove(value)

        for word, old_domain in old_domains:
            word.domain = old_domain

    @staticmethod
    def _get_selection_function(heuristic: str) -> Callable[[List["Word"]], "Word"]:
        """
        Return the appropriate function for unassigned variable
        selection, based on provided heuristic str.
        """
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
        """
        Finds all words in assignment with minimum remaining values;
        if there are multiple, uses degree as a tie-breaker.
        """
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
        final_choice = selection[0]

        if len(selection) > 1:
            for choice in selection:
                constraint_count = len(choice.constraints)
                if constraint_count > most_constraints:
                    most_constraints = constraint_count
                    final_choice = choice

        return final_choice
