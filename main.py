import csv


def read_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        result = []
        for row in reader:
            result.append(';'.join(row).replace(" ", "").replace(",", ".").split(";"))
        return result


def get_distance(point1, point2):
    sum_of_squares = sum([(a - b) ** 2 for a, b in zip(point1, point2)])
    return sum_of_squares ** 0.5


def get_most_common(k, list):
    count = {}
    for i in range(k):
        string = list[i][1]
        if string in count:
            count[string] += 1
        else:
            count[string] = 1
    #print(f'get_most_common: {count}')
    most_common = None
    max_count = 0
    for string, c in count.items():
        if c > max_count:
            most_common = string
            max_count = c
    return most_common

def normalize(x, min, max):
    x_normalized = (x - min) / (max - min)
    return x_normalized


def kNN(k, training_data, test_point):
    if len(test_point) > 4:
        return "Podany wektor ma za dużo atrybutów"
    training_numbers = [point[:len(test_point)] for point in training_data]  # remove decision attribute
    training_numbers = [[float(num) for num in set] for set in training_numbers]  # convert strings to floats
    test_point = [float(num) for num in test_point]
    distances = [get_distance(training_point, test_point) for training_point in training_numbers]

    # add iris description to distance list
    counter = 0
    for row in distances:
        result = training_data[counter][len(training_data[0]) - 1]
        distances[counter] = [row, result]
        counter += 1

    #posortowana lista z dystansami

    sorted_distances = sorted(distances, key=lambda x: x[0])

    #print(sorted_distances)
    # zwróc najbardziej popularny w k pierwszych elementach

    result = get_most_common(k, sorted_distances)

    return result


if __name__ == "__main__":
    iris_test = read_csv('data/iris_test.txt')
    iris_training = read_csv('data/iris_training.txt')

    k = int(input("Podaj wartość parametru k: "))

    true_prediction = 0
    false_prediction = 0

    #kNN(k, iris_training, iris_test[22][:4])

    for i in range(len(iris_test)):
        if iris_test[i][len(iris_test[i]) - 1] == kNN(k, iris_training, iris_test[i][:(len(iris_test[i]) - 1)]):
            true_prediction += 1
        else:
            false_prediction += 1
        #print(iris_test[i][len(iris_test[i])-1 ])

    print(f"Liczba prawidłowo zaklasyfikowanych przykładów: {true_prediction}/{false_prediction+true_prediction}")
    percentage = "Dokładność {:.2%}".format(true_prediction/(true_prediction+false_prediction))
    print(percentage)


    while True:
        user_input = input("Podaj wektor atrybutów do zbadania (dane oddzielaj \",\"): ")
        if user_input == 'q':
            break
        test_point = user_input.split(",");
        test_point = [float(num) for num in test_point]
        print(kNN(k, iris_training, test_point))