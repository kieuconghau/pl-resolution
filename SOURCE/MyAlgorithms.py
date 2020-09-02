from enum import Enum
from copy import deepcopy

class Definition(Enum):
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
        self.alpha = [f.readline()[:-1].split(Definition.OR_OPERATOR_DELIMETER.value) for _ in range(int(f.readline()))]
        self.KB    = [f.readline()[:-1].split(Definition.OR_OPERATOR_DELIMETER.value) for _ in range(int(f.readline()))]
        self.alpha = self.standard_cnf_sentence(self.alpha)
        self.KB    = self.standard_cnf_sentence(self.KB)
        f.close()


    # PL Resolution algorithm.
    def pl_resolution(self):
        cnf_clause_list = deepcopy(self.KB)
        neg_alpha = self.negation_of_cnf_sentence(self.alpha)
        for clause in neg_alpha:
            if clause not in cnf_clause_list:
                cnf_clause_list.append(clause)

        while True:
            self.new_clauses_list.append([])

            for i in range(len(cnf_clause_list)):
                for j in range(i + 1, len(cnf_clause_list)):
                    resolvents = self.resolve(cnf_clause_list[i], cnf_clause_list[j])
                    if [] in resolvents:
                        self.solution = True
                        self.new_clauses_list[-1].append([])
                        return self.solution

                    for resolvent in resolvents:
                        if self.is_valid_clause(resolvent):
                            break
                        if resolvent not in cnf_clause_list and resolvent not in self.new_clauses_list[-1]:
                            self.new_clauses_list[-1].append(resolvent)

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

    # Return a standardized CNF sentence:
    # 1. Standardize all of clauses.
    # 2. Get rid of all of valid clauses.
    def standard_cnf_sentence(self, cnf_sentence: list):
        std_cnf_sentence = deepcopy(cnf_sentence)
        temp_sentence = []
        for clause in std_cnf_sentence:
            clause = self.standard_clause(clause)
            if self.is_valid_clause(clause):
                temp_sentence.append(clause)
        for clause in temp_sentence:
            std_cnf_sentence.remove(clause)
        return std_cnf_sentence


    # Return a standardized clause:
    # 1. Get rid of all of duplicates.
    # 2. Literals within a clause are sorted following the alphabetical order.
    @staticmethod
    def standard_clause(clause: list):
        return sorted(list(set(deepcopy(clause))), key=lambda x: x[-1])


    # Check if 2 literals are complementary.
    @staticmethod
    def is_complentary_literals(literal_1: str, literal_2: str):
        return len(literal_1) != len(literal_2) and literal_1[-1] == literal_2[-1]


    # Return a negation of a CNF sentence.
    def negation_of_cnf_sentence(self, cnf_sentence: list):
        neg_sentence = [[self.negation_of_literal(literal) for literal in clause] for clause in cnf_sentence]
        neg_cnf_sentence = self.generate_combinations(neg_sentence)
        return neg_cnf_sentence


    # Return a negation of a literal.
    @staticmethod
    def negation_of_literal(literal: str):
        if literal[0] == Definition.NOT_OPERATOR_SYMBOL.value:
            return literal[1]
        return Definition.NOT_OPERATOR_SYMBOL.value + literal


    # Genrate a combination list from many sets:
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


    # Resolve 2 clauses then return a list of resolvents (list of clauses).
    def resolve(self, clause_1: list, clause_2: list):
        resolvents = []
        for i in range(len(clause_1)):
            for j in range(len(clause_2)):
                if self.is_complentary_literals(clause_1[i], clause_2[j]):
                    resolvent = clause_1[:i] + clause_1[i + 1:] + clause_2[:j] + clause_2[j + 1:]
                    resolvents.append(self.standard_clause(resolvent))
        return resolvents


    # Return a formated-string clause.
    def formated_clause(self, clause):
        if self.is_empty_clause(clause):
            return Definition.EMPTY_CLAUSE_SYMBOL.value

        formated_clause = ''
        for i in range(len(clause) - 1):
            formated_clause += str(clause[i]) + Definition.OR_OPERATOR_DELIMETER.value
        formated_clause += str(clause[-1])

        return formated_clause


    # Check if a clause is empty.
    @staticmethod
    def is_empty_clause(clause: list):
        return len(clause) == 0


    # Check if a clause is valid (always True).
    def is_valid_clause(self, clause):
        for i in range(len(clause) - 1):
            if self.is_complentary_literals(clause[i], clause[i + 1]):
                return True
        return False


"""
    # A pseudo code to improve the PL Resolution.
    def pl_resolution(KB, alpha):
        clauses = KB + negation(alpha)
        new_clauses_list = []       # New clauses at each loop
        
        while True:
            new_clauses_list.append([])
            n = 
            for i in range(len(clauses)):
                for j in range(n + i + 1, len(clauses))):
                    resolvents = resolve(clauses[i], clauses[j])
                    if [] in resolvents:
                        return True
                    for resolvent in resolvents:
                        if resolvent not in clauses:
                            new_clauses_list.append(resolvent)
                            
            if len(new_clauses_list[-1]) == 0:
                return False
            clauses += new_clauses_list[-1]
"""
