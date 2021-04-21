import numpy
import random
import time


def genetic_algorithm(popul_size, cross_prob, mut_prob, possible_inputs, numb_of_values, max_iteration_number):
    probability_base = numpy.linspace(0, 1, 1000)
    population_list = []
    rating_list = []
    new_population_list = []
    iteration = 0

    population_size = popul_size
    crossing_probability = cross_prob
    mutation_probability = mut_prob
    all_possible_values = possible_inputs
    number_of_values_in_individual = numb_of_values
    number_of_bits_for_value = len(all_possible_values[0][0])
    number_of_bits_for_population_value = number_of_values_in_individual * number_of_bits_for_value

    # creating random first population
    for i in range(population_size):
        population_to_add = []
        for ii in range(number_of_values_in_individual):
            population_to_add.append(random.choice(all_possible_values))
        population_list.append(population_to_add)

    # evaluation of first population
    for i2 in range(population_size):
        q = 0
        for i1 in range(number_of_values_in_individual):
            x = int(population_list[i2][i1][1])
            q += (x ** 4 - 16 * x ** 2 + 5 * x) / 2
        q = - q
        rating_list.append((q, population_list[i2]))

    # assigning highest value as final result
    rating_list = sorted(rating_list, key=lambda element: element[0], reverse=True)
    end_result = rating_list[0]
    end_result_iteration = 0
    start_loop_time = time.perf_counter()
	
    # loop for genetic algorithm
    while iteration < max_iteration_number:
        total_value_in_rating_list = 0
        probability_values_list = []

        # reproduction
        for i3 in range(population_size):
            total_value_in_rating_list += rating_list[i3][0]
            probability_values_list.append(total_value_in_rating_list)

        for i4 in range(population_size):
            random_number = random.randint(1, total_value_in_rating_list)
            for i5 in range(population_size):
                if random_number > probability_values_list[i5]:
                    continue
                else:
                    new_population_list.append(rating_list[i5][1])
                    break

        # conversion of new population to bites array for crossing and mutation
        new_population_in_bits = []
        for con1 in range(population_size):
            population_element_in_bits = []
            for con2 in range(number_of_values_in_individual):
                for con3 in range(number_of_bits_for_value):
                    population_element_in_bits.append(new_population_list[con1][con2][0][con3])
            new_population_in_bits.append(population_element_in_bits)

        # crossing
        for c1 in range(0, population_size, 2):
            if c1 == population_size - 1:
                break
            check_if_crossing_occurs = random.choice(probability_base)
            if crossing_probability > check_if_crossing_occurs:
                where_to_cut = random.randint(1, number_of_bits_for_population_value - 1)
                first_element_1_cut = new_population_in_bits[c1][:where_to_cut]
                second_element_1_cut = new_population_in_bits[c1 + 1][:where_to_cut]
                first_element_2_cut = new_population_in_bits[c1][where_to_cut:]
                second_element_2_cut = new_population_in_bits[c1 + 1][where_to_cut:]
                first_element_new = []
                second_element_new = []
                first_element_new.extend(first_element_1_cut)
                first_element_new.extend(second_element_2_cut)
                second_element_new.extend(second_element_1_cut)
                second_element_new.extend(first_element_2_cut)
                new_population_in_bits[c1] = first_element_new
                new_population_in_bits[c1 + 1] = second_element_new

        # mutation
        for m1 in range(population_size):
            changed_item = []
            for m2 in range(number_of_bits_for_population_value):
                check_if_mutation_occurs = random.choice(probability_base)
                if mutation_probability > check_if_mutation_occurs:
                    if new_population_in_bits[m1][m2] == 1:
                        changed_item.append(0)
                    else:
                        changed_item.append(1)
                else:
                    changed_item.append(new_population_in_bits[m1][m2])

            new_population_in_bits[m1] = changed_item

        # conversion of new population from bites array for evaluation
        for cb1 in range(population_size):
            new_population_list_item = []
            for cb2 in range(0, number_of_bits_for_population_value, 3):
                value_in_bits = []
                for cb3 in range(number_of_bits_for_value):
                    value_in_bits.append(new_population_in_bits[cb1][cb2 + cb3])

                new_tuple_item_array = [item for item in all_possible_values if item[0] == value_in_bits]
                new_tuple_item = new_tuple_item_array[0]
                new_population_list_item.append(new_tuple_item)
            new_population_list[cb1] = new_population_list_item

        # evaluation of new population
        rating_list = []
        for e in range(population_size):
            q = 0
            for e1 in range(number_of_values_in_individual):
                x = int(new_population_list[e][e1][1])
                q += (x ** 4 - 16 * x ** 2 + 5 * x) / 2
            q = - q
            rating_list.append((q, new_population_list[e]))

        new_population_list = []
        rating_list = sorted(rating_list, key=lambda element: element[0], reverse=True)
        new_end_result = rating_list[0]

        # checking if newly found highest result is better
        if new_end_result[0] > end_result[0]:
            end_result = new_end_result
            end_result_iteration = iteration

        iteration += 1

    end_loop_time = time.perf_counter()
    time_loop_took = round(end_loop_time - start_loop_time, 2)
    return end_result[0], end_result_iteration, time_loop_took


# generating Gray code
gray_code = []
for b in range(8):
    gray = b ^ (b >> 1)
    bits_str = '{0:03b}'.format(gray)
    bits_array = []
    for b1 in range(3):
        bits_array.append(int(bits_str[b1]))
    gray_code.append(bits_array)

# assigning possible values with Gray code
possible_values = []
gray_index = 0
for v in list(range(-4, 4)):
    possible_values.append((gray_code[gray_index], v))
    gray_index += 1

user_population_number = int(input("Population size [int]: "))
user_cross_probability = float(input("Crossing probability [0, 1]: "))
user_mutation_probability = float(input("Mutation probability  [0, 1]: "))
user_algorithm_loop_number = float(input("Number of algorithm loops: "))
user_algorithm_number = 10

average_result = 0
average_iteration_number = 0
average_time = 0

# calling algorithm
for a in range(user_algorithm_number):
    algorithm_result = genetic_algorithm(user_population_number, user_cross_probability, user_mutation_probability,
                                         possible_values, 6, user_algorithm_loop_number)
    print(algorithm_result)
    average_result += algorithm_result[0]
    average_iteration_number += algorithm_result[1]
    average_time += algorithm_result[2]

average_result = round(average_result / user_algorithm_number, 2)
average_iteration_number = round(average_iteration_number / user_algorithm_number, 2)
average_time = round(average_time / user_algorithm_number, 2)
print("Average result:", average_result, average_iteration_number, average_time)
