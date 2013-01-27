import random

def decode(gene):
    if len(gene) != 4:
        return ""
    if gene[0] == 0 and gene[1] == 0 and gene[2] == 0 and gene[3] == 0:
        return 0
    if gene[0] == 0 and gene[1] == 0 and gene[2] == 0 and gene[3] == 1:
        return 1
    if gene[0] == 0 and gene[1] == 0 and gene[2] == 1 and gene[3] == 0:
        return 2
    if gene[0] == 0 and gene[1] == 0 and gene[2] == 1 and gene[3] == 1:
        return 3
    if gene[0] == 0 and gene[1] == 1 and gene[2] == 0 and gene[3] == 0:
        return 4
    if gene[0] == 0 and gene[1] == 1 and gene[2] == 0 and gene[3] == 1:
        return 5
    if gene[0] == 0 and gene[1] == 1 and gene[2] == 1 and gene[3] == 0:
        return 6
    if gene[0] == 0 and gene[1] == 1 and gene[2] == 1 and gene[3] == 1:
        return 7
    if gene[0] == 1 and gene[1] == 0 and gene[2] == 0 and gene[3] == 0:
        return 8
    if gene[0] == 1 and gene[1] == 0 and gene[2] == 0 and gene[3] == 1:
        return 9
    if gene[0] == 1 and gene[1] == 0 and gene[2] == 1 and gene[3] == 0:
        return "+"
    if gene[0] == 1 and gene[1] == 0 and gene[2] == 1 and gene[3] == 1:
        return "-"
    if gene[0] == 1 and gene[1] == 1 and gene[2] == 0 and gene[3] == 0:
        return "*"
    if gene[0] == 1 and gene[1] == 1 and gene[2] == 0 and gene[3] == 1:
        return "/"
    if gene[0] == 1 and gene[1] == 1 and gene[2] == 1 and gene[3] == 0:
        return ""
    if gene[0] == 1 and gene[1] == 1 and gene[2] == 1 and gene[3] == 1:
        return ""
    return ""

def decode_chromosome(chromosome):
    i = 0
    max = len(chromosome)/4

    decoding = []

    while i<max:
        gene = [int(chromosome[i*4]), int(chromosome[i*4+1]), int(chromosome[i*4+2]), int(chromosome[i*4+3])]
        decoding.append(decode(gene))
        i = i + 1

    return decoding

print decode_chromosome("00010001")

def result(chromosome):
    result = -1000000000000
    find_number = True
    decoding = decode_chromosome(chromosome)
    mod = ""
    for elt in decoding:
        if find_number and elt >= 0 and elt <= 9:
            if result == -1000000000000:
                result = elt
            else:
                if mod == "+":
                    result = result + elt
                if mod == "-":
                    result = result - elt
                if mod == "*":
                    result = result * elt
                if mod == "/":
                    if elt == 0:
                        return -1000000000000
                    result = result / elt
            find_number = False
        elif not find_number and type(elt) is str and len(elt) == 1:
            mod = elt
            find_number = True
    return result

def fitness(chromosome, target):
    res = float(result(chromosome))
    diff = float(abs(target-res))
    if diff == 0:
        return float("inf")
    return 1/diff

def update_population(population, target):
    sum = 0
    for chromosome in population:
        if fitness(chromosome, target) == float("inf"):
            return [chromosome, chromosome]
        sum = sum + fitness(chromosome, target)
    pop_count = len(population)
    new_population = []
    for i in range(pop_count/2):
        ri = random.random()*sum
        rj = random.random()*sum
        iC = ""
        jC = ""
        sum2 = 0
        for chromosome in population:
            sum2 = sum2 + fitness(chromosome, target)
            if len(iC) == 0 and ri < sum2:
                iC = chromosome
            if len(jC) == 0 and rj < sum2:
                jC = chromosome
        babies = make_babies(iC,jC)
        new_population.append(babies[0])
        new_population.append(babies[1])
    return new_population

def make_babies(chromosome1, chromosome2):
    swap_chance = 0.7
    mutation_rate = 0.005
    nC1 = chromosome1
    nC2 = chromosome2
    if random.random() < swap_chance:
        cut_point = random.randint(0,len(chromosome1)-1)
        nC1 = chromosome1[0:cut_point]+chromosome2[cut_point:len(chromosome2)]
        nC2 = chromosome2[0:cut_point]+chromosome1[cut_point:len(chromosome2)]
    if random.random() < mutation_rate:
        mutation_point = random.randint(0,len(chromosome1)-1)
        prev = nC1[mutation_point]
        if prev == "0":
            nC1 = nC1[0:mutation_point]+"1"+nC1[mutation_point+1:len(nC1)]
        else:
            nC1 = nC1[0:mutation_point]+"0"+nC1[mutation_point+1:len(nC1)]
    if random.random() < mutation_rate:
        mutation_point = random.randint(0,len(chromosome1)-1)
        prev = nC2[mutation_point]
        if prev == "0":
            nC2 = nC2[0:mutation_point]+"1"+nC2[mutation_point+1:len(nC2)]
        else:
            nC2 = nC2[0:mutation_point]+"0"+nC2[mutation_point+1:len(nC2)]
    return [nC1, nC2]


def random_chromosome():
    chromosome = ""
    for i in range(40):
        nextBool = random.random()
        if nextBool >= 0.5:
            nextBool = "1"
        else:
            nextBool = "0"
        chromosome = chromosome + nextBool
    return chromosome

def gen_base_set(population):
    base_set = []
    for i in range(population):
        base_set.append(random_chromosome())
    return base_set
    
def max_fitness(population, target):
    max = 0
    chromo = ""
    for chromosome in population:
        fit = fitness(chromosome,target)
        if max < fit:
            max = fit
            chromo = chromosome
    return [max, chromo]

def min_fitness(population, target):
    min = float("inf")
    chromo = ""
    for chromosome in population:
        fit = fitness(chromosome,target)
        if min > fit:
            min = fit
            chromo = chromosome
    return [min, chromo]

chromosome = random_chromosome()

population = gen_base_set(100)
best_fit = max_fitness(population,42)
print(best_fit)
print(decode_chromosome(best_fit[1]))
print(result(best_fit[1]))

for i in range(100):
    population = update_population(population,101)
    best_fit = max_fitness(population,101)
    print(best_fit)
    print(decode_chromosome(best_fit[1]))
    print(result(best_fit[1]))
    
    #worst_fit = min_fitness(population,101)
    #print(worst_fit)
    #print(decode_chromosome(worst_fit[1]))
    #print(result(worst_fit[1]))


raw_input()

