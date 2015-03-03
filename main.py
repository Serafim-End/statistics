__author__ = 'nikita'

from math import sqrt


class MatStat:
    def __init__(self, number_of_lines, start_line, end_line):
        self.dictionary = {}
        self.number_of_lines = number_of_lines + 1
        self.start_line = start_line
        self.end_line = end_line
        self.filename = "matstat.txt"

    def read_file(self, filename):
        f = open(filename, "r+")
        for line in f:
            new_line = line.replace('\t', '*').replace(' ', '*').replace('\n', '*')
            array = new_line.split('*')

            info_array = []
            for i in xrange(1, len(array)):
                if array[i] != '':
                    info_array.append(array[i])

            self.dictionary[array[0]] = info_array
        f.close()


class FirstTask(MatStat):
    def __init__(self, start_line, end_line, kvantil=1.96):
        MatStat.__init__(self, end_line - start_line, start_line, end_line)
        self.kvantil = kvantil
        self.left_result = 0
        self.right_result = 0

    def print_first_task(self):
        self.first_task()
        print self.left_result, ", ", self.right_result

    def first_task(self):
        # 5 - finds job more then one year = count[4]
        count = [0, 0, 0, 0, 0]

        for i in xrange(self.start_line, self.end_line + 1):
            for j in xrange(5):
                if self.dictionary[str(i)][1] == str(j + 1):
                    count[j] += 1

        p = float(count[4]) / self.number_of_lines
        self.left_result = p - self.kvantil * sqrt((1. / self.number_of_lines) * p * (1 - p))
        self.right_result = p + self.kvantil * sqrt((1. / self.number_of_lines) * p * (1 - p))

        return self.left_result, self.right_result


class SecondTask(MatStat):
    def __init__(self, start_line, end_line, t=1.671):
        MatStat.__init__(self, end_line - start_line, start_line, end_line)
        self.t = t

        self.left_result_t = 0
        self.right_result_t = 0

    def print_second_task(self):
        self.second_task_a()
        print self.left_result_t, ", ", self.right_result_t

    def second_task_a(self):
        men_benefits, women_benefits = [], []
        for i in xrange(self.start_line, self.end_line + 1):
            if len(self.dictionary[str(i)]) == 3:
                if self.dictionary[str(i)][0] == '1':
                    men_benefits.append(self.dictionary[str(i)][2])
                elif self.dictionary[str(i)][0] == '2':
                    women_benefits.append(self.dictionary[str(i)][2])

        print "number of men with benefits: ", len(men_benefits)
        print "number of women with benefits: ", len(women_benefits)

        middle_x = float(sum([int(i) for i in men_benefits])) / len(men_benefits)
        middle_y = float(sum([int(i) for i in women_benefits])) / len(women_benefits)

        print "men middle: ", middle_x
        print "women middle: ", middle_y

        x_dispersion = sqrt((1. / (len(men_benefits) - 1)) *
                            sum([(int(i) - middle_x) ** 2 for i in men_benefits]))

        y_dispersion = sqrt((1. / (len(women_benefits) - 1)) *
                            sum([(int(i) - middle_y) ** 2 for i in women_benefits]))

        print "dispersion x: ", x_dispersion
        print "dispersion y: ", y_dispersion

        s = sqrt(float((len(men_benefits) - 1) *
                       (x_dispersion ** 2) + (len(women_benefits) - 1) *
                       (y_dispersion ** 2)) / (len(men_benefits) + len(women_benefits) - 2))

        print "normal dispersion: ", s

        self.left_result_t = (middle_x - middle_y) - self.t * s *\
                                                sqrt(float(len(men_benefits) + len(women_benefits)) /
                                                     (len(men_benefits) * len(women_benefits)))
        self.right_result_t = (middle_x - middle_y) + self.t * s *\
                                                 sqrt(float(len(men_benefits) + len(women_benefits)) /
                                                      (len(men_benefits) * len(women_benefits)))
        return self.left_result_t, self.right_result_t


class ThirdTask(MatStat):
    def __init__(self, start_line, end_line):
        MatStat.__init__(self, end_line - start_line, start_line, end_line)
        self.number_of_lines = end_line - start_line + 1
        self.left_result = 0
        self.right_result = 0
        self.xi_2 = 0

    @staticmethod
    def print_table(men, women, sum_men, sum_women):
        print 4 * " " + "men ", " women", "  lambda"
        for i in xrange(1, 6):
            print i, " ", men[i], 3 * " ", women[i], 2 * " ", men[i] + women[i]
        print "s  ", sum_men, 2 * " ", sum_women, 2 * " ", sum_women + sum_men

    def print_third_task(self):
        print self.third_task()

    def third_task(self):

        def frequency(lambda_element, sum_gender):
            return float(lambda_element) * float(sum_gender) / self.number_of_lines

        men = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        women = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

        for i in xrange(self.start_line, self.end_line + 1):
            if self.dictionary[str(i)][0] == '1':
                for k in xrange(1, 6):
                    if self.dictionary[str(i)][1] == str(k):
                        men[k] += 1
            else:
                for k in xrange(1, 6):
                    if self.dictionary[str(i)][1] == str(k):
                        women[k] += 1

        sum_men = sum([men[i] for i in xrange(1, 6)])
        sum_women = sum(women[i] for i in xrange(1, 6))

        ThirdTask.print_table(men, women, sum_men, sum_women)

        freq_men = {i: frequency((men[i] + women[i]), sum_men) for i in xrange(1, 6)}
        freq_women = {i: frequency((men[i] + women[i]), sum_women) for i in xrange(1, 6)}
        sum_freq_men = sum([freq_men[i] for i in xrange(1, 6)])
        sum_freq_women = sum([freq_women[i] for i in xrange(1, 6)])

        ThirdTask.print_table(freq_men, freq_women, sum_freq_men, sum_freq_women)

        table_xi_men = [(float(men[i] - freq_men[i]) ** 2) / freq_men[i] for i in xrange(1, 6)]
        table_xi_women = [(float(women[i] - freq_women[i]) ** 2) / freq_women[i] for i in xrange(1, 6)]

        for i in xrange(5):
            print table_xi_men[i], " ", table_xi_women[i]
        self.xi_2 = sum(table_xi_men) + sum(table_xi_women)
        return self.xi_2


def main():
    start_line = 2601
    end_line = 3000

    task3 = ThirdTask(start_line, end_line)
    task3.read_file(task3.filename)
    task3.print_third_task()


if __name__ == '__main__':
    main()