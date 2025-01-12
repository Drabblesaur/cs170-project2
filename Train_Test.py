import random
import numpy as np
import math

filename = 'small-test-dataset.txt'

best_acc = 0


class Classifier:

    def __init__(self, data):

        # init feature list
        self.best_features = []

        # numpy data array
        self.data = data

        self.best_feature_data = []




    def leave_one_out_cross_val(self, input_data, current_set_of_features, feature_to_add):

        # data is simply the data being inputted
        # current_set is an array of nums, showing the col added so far
        # feature is the feature being tested, also a num

        # start from 1, since col 0 is just the class label
        data = np.copy(input_data)
        current_set = current_set_of_features.copy()
        

        # add the deature-to-add to current set, but first lets copy
        test_set = current_set
        test_set.append(feature_to_add)
        test_set.append(0)  # Always keep the class label

        col_num = 0
        for col in data:
            data_point = 0
            for point in col:
                if data_point not in test_set:
                    point = '0'
                    data[col_num][data_point] = '0'
                data_point += 1
            col_num += 1



        num_correctly_classified = 0

        i = 1

        for point in data:
            # Object to classify 
            label = float(point[0])

            # object 
            object = point[1:]

            nn_distance = float('inf')
            nn_location = float('inf')

            k = 1

            for neighbor in data:
                if(k != i):

                    # get distance 
                    distance = 0
                    for x in range(1, len(point)):
                        distance += math.pow((float(point[x]) - float(neighbor[x])), 2)
                        distance = math.sqrt(distance)

                    if distance < nn_distance:
                        nn_distance = distance
                        nn_location = k - 1
                        nn_label = float(data[nn_location][0])
                        #print("Nearest Neighbor Label: " + str(nn_label))
                k += 1

            print('Object ' + str(i) + ' is class ' + str(label))
            print('Its nearest neighbor is object ' + str(nn_location + 1) + ' which is of class ' + str(nn_label))  

            if(label == nn_label):
                num_correctly_classified += 1


            i += 1

        accuracy = num_correctly_classified / len(data)

        return accuracy

    def train(self):

        ## Init empty set for current set
        current_set_of_features = []
        best_overall = 0

        for i in range(1, len(self.data[0]) + 1):
            print("On the " + str(i) + "th level of the search tree...")
            feature_to_add = 0
            best_accuracy = 0

            for k in range(1, len(self.data[0]) + 1):
                if k in current_set_of_features:
                    continue
                print("--Considering adding the " + str(k) + "th feature...")
                accuracy = self.leave_one_out_cross_val(self.data, current_set_of_features, k)

                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    feature_to_add = k

            if best_accuracy > best_overall:
                best_overall = best_accuracy
                self.best_features = current_set_of_features.copy()

            current_set_of_features.append(feature_to_add)        
            print("On level " + str(i) + " the feature " + str(feature_to_add) + " was added to the current set\n")



        print('Best Overall was ' + str(best_overall))
        print('Feature Trace is ' + str(self.best_features))

    # Now that we have our best features, lets cxreate the data with only our best features being present

        # Each full row 
        for feature in self.data:

            # init at 0
            i = 0

            # declare an empty instance
            instance = []

            # append the classifier by default
            instance.append(float(feature[0]))

            # check if each data category is inside our best feature trace, if no do not add
            for data_point in feature:
                i += 1
                if i in self.best_features:
                    instance.append(float(data_point))

            # append new data
            self.best_feature_data.append(instance)

        # debugging :P
        print(self.best_feature_data)
        


    


    





def main():
    # data = []
    # data.append(1)
    # data.append(2)
    # data.append(3)
    # data.append(4)

    # feature_search_demo(data)

    data = np.loadtxt(filename, dtype=str, usecols=range(11))

    classifier = Classifier(data)
    classifier.train()




if __name__ == "__main__":
    main()
