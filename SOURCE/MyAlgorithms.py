from enum import Enum
from copy import deepcopy

class Definition(Enum):
    VALID_CLAUSE = ['True']
    EMPTY_CLAUSE = []
    EMPTY_CLAUSE_SYMBOL = '{}'
    NOT_OPERATOR_SYMBOL = '-'
    OR_OPERATOR_DELIMETER = ' OR '

class MyAlgorithms:
    # Constructor.
    def __init__(self):
        self.alpha = []
        self.KB = []
        self.new_clauses_list = []
        self.solution = False

    ################################################## MAIN FUNCTIONS ##################################################

    # Read an input data from an input file into the Knowledge Base and Alpha.
    def read_input_data(self, input_filename: str):
        f = open(input_filename, 'r')
        self.alpha = [self.standard_clause(f.readline()[:-1].split(Definition.OR_OPERATOR_DELIMETER.value))
                      for _ in range(int(f.readline()))]
        self.KB    = [self.standard_clause(f.readline()[:-1].split(Definition.OR_OPERATOR_DELIMETER.value))
                      for _ in range(int(f.readline()))]
        self.alpha = self.standard_cnf_sentence(self.alpha)
        self.KB    = self.standard_cnf_sentence(self.KB)
        f.close()

    # PL Resolution algorithm.
    def pl_resolution(self):
        cnf_clause_list = deepcopy(self.KB)
        neg_alpha = self.negative_cnf_sentence(self.alpha)
        for clause in neg_alpha:
            if clause not in cnf_clause_list:
                cnf_clause_list.append(clause)

        while True:
            self.new_clauses_list.append([])

            for i in range(len(cnf_clause_list)):
                for j in range(i + 1, len(cnf_clause_list)):
                    resolvent = self.resolve(cnf_clause_list[i], cnf_clause_list[j])
                    if self.is_valid_clause(resolvent):
                        continue
                    if resolvent not in cnf_clause_list and resolvent not in self.new_clauses_list[-1]:
                        self.new_clauses_list[-1].append(resolvent)
                    if self.is_empty_clause(resolvent):
                        self.solution = True
                        return self.solution

            if len(self.new_clauses_list[-1]) == 0:
                self.solution = False
                return self.solution
            cnf_clause_list += self.new_clauses_list[-1]

    # Write an output data into an output file.
    def write_output_data(self, output_filename: str):
        f = open(output_filename, 'w')
        for new_clauses in self.new_clauses_list:
            f.write(str(len(new_clauses)) + '\n')
            for clause in new_clauses:
                f.writelines(self.formated_clause(clause) + '\n')
        f.writelines('YES\n') if self.solution else f.writelines('NO\n')
        f.close()

    ################################################# HELPER FUNCTIONS #################################################

    # Return a standardized clause:
    # 1. Literals within a clause are sorted following the alphabetical order.
    # 2. Any clause in which two complementary literals appear is discarded.
    # 3. Get rid of all of duplicates.
    def standard_clause(self, clause: list):
        std_clause = deepcopy(clause)
        std_clause = sorted(list(set(std_clause)), key=lambda x: x[-1])
        for i in range(len(std_clause) - 1):
            if self.is_complentary_literals(std_clause[i], std_clause[i + 1]):
                std_clause = Definition.VALID_CLAUSE.value
                break
        return std_clause

    # Return a standardized CNF sentence:
    # 1. Get rid of all of valid clauses.
    @staticmethod
    def standard_cnf_sentence(cnf_sentence: list):
        std_cnf_sentence = deepcopy(cnf_sentence)
        temp_sentence = []
        for clause in std_cnf_sentence:
            if clause == Definition.VALID_CLAUSE.value:
                temp_sentence.append(clause)
        for clause in temp_sentence:
            std_cnf_sentence.remove(clause)
        return std_cnf_sentence

    # Check if 2 literals are complementary.
    @staticmethod
    def is_complentary_literals(literal_1: str, literal_2: str):
        return len(literal_1) != len(literal_2) and literal_1[-1] == literal_2[-1]

    # Return a negative CNF sentence.
    def negative_cnf_sentence(self, cnf_sentence: list):
        neg_sentence = [[self.negative_literal(literal) for literal in clause] for clause in cnf_sentence]
        neg_cnf_sentence = self.generate_combinations(neg_sentence)
        return neg_cnf_sentence

    # Return a negative literal.
    @staticmethod
    def negative_literal(literal: str):
        if literal[0] == Definition.NOT_OPERATOR_SYMBOL.value:
            return literal[1]
        return Definition.NOT_OPERATOR_SYMBOL.value + literal

    # Genrate a combination list from many set:
    # set: (a, b)
    # set: (c, d)
    # --> combinations: (a, c), (a, d), (b, c), (b, d)
    def generate_combinations(self, set_list: list):
        combination_list, combination, depth = [], [], 0
        self.generate_combinations_recursively(set_list, combination_list, combination, 0)
        return combination_list

    # Helper function of generate_combinations.
    def generate_combinations_recursively(self, set_list: list, combination_list: list, combination: list, depth: int):
        if depth == len(set_list):
            combination_list.append(deepcopy(combination))
            return

        for element in set_list[depth]:
            combination.append(deepcopy(element))
            self.generate_combinations_recursively(set_list, combination_list, combination, depth + 1)
            combination.pop()

    # Resolve 2 clauses then return a resolvent (clause).
    def resolve(self, clause_1: list, clause_2: list):
        resolvent = Definition.VALID_CLAUSE.value
        temp_clause_1 = deepcopy(clause_1)
        temp_clause_2 = deepcopy(clause_2)

        for literal_1 in temp_clause_1:
            for literal_2 in temp_clause_2:
                if self.is_complentary_literals(literal_1, literal_2):
                    temp_clause_1.remove(literal_1)
                    temp_clause_2.remove(literal_2)
                    resolvent = self.standard_clause(temp_clause_1 + temp_clause_2)
                    break
        return resolvent

    # Return a formated-string clause.
    def formated_clause(self, clause):
        formated_clause = ''
        if self.is_empty_clause(clause):
            formated_clause = Definition.EMPTY_CLAUSE_SYMBOL.value
        elif self.is_valid_clause(clause):
            formated_clause = Definition.VALID_CLAUSE.value[0]
        else:
            for i in range(len(clause) - 1):
                formated_clause += str(clause[i]) + Definition.OR_OPERATOR_DELIMETER.value
            formated_clause += str(clause[-1])

        return formated_clause

    # Check if a clause is empty.
    @staticmethod
    def is_empty_clause(clause: list):
        return len(clause) == 0

    # Check if a clause is valid.
    @staticmethod
    def is_valid_clause(clause):
        return clause == Definition.VALID_CLAUSE.value
