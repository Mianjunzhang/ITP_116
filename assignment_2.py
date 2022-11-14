# NAME: Mianjun Zhang
# ID: 2793313312
# DATE: 2022-10-6
# DESCRIPTION: In this assignment, the main objective is to write a program with several functions
# to recommend the most likely new friend to users of a social network.
# In each split-up functions, the operations related with list, string functions could be
# pretty useful to finalize the algorithm we need. In a detailed version, the ideal results is that
# the program will return a recommend friend ID for a user ID given that the network data are provided.
# Then, the program will read the raw network and reform it into a cleaner and useful version. After that,
# a similarity matrix will be computed based on the common friends two user have. The person who is not friend
# with the user with the highest number of common friend will be desired recommend subject for user.


from typing import IO, List


# The function used to open the data file
def open_file() -> IO:
    # Prompt the user to enters the filename
    file_name = input("Enter a filename: ")
    # Initialize the file pointer data set
    pointer = None
    # Checking if the input filename can be referenced
    while pointer is None:
        try:
            # Try to open the file with input filename
            pointer = open(file_name, "r")
        # Inform the user the input is not valid filename
        except IOError:
            # Alert the user
            print("Error in filename.")
            # Re-enter the filename
            file_name = input("Enter a filename: ")
    # Return the file data
    return pointer


# The function to read the file
def read_file(fp: IO) -> List[List[int]]:
    # Read the number of users in the provided social network
    n = fp.readline()
    # Convert the string into integer
    n = int(n)
    # Initialize the network lists of list
    network = []
    # Create the list which store the lists of each user's connections
    for i in range(n):
        # Append the network
        network.append([])
    # Read the remaining lines after the first line of the provided data file
    line = fp.readline()
    # Iterate each line
    while line is not None and len(line) >= 3:
        # Format each line and split them in a cleaner manner
        split_line = line.strip().split(" ")
        # Update the network list by appending with each user's connections
        network[int(split_line[0])].append(int(split_line[1]))
        network[int(split_line[1])].append(int(split_line[0]))
        # Read all the remaining lines in order to get full data
        line = fp.readline()
    # Return a list of lists
    return network


# The function to initialize a matrix
def init_matrix(n: int) -> List[List[int]]:
    # Initialization
    matrix = []
    # Iterate each row the nxn matrix
    for row in range(n):
        # Iterate each column in the nxn matrix
        # Update the empty matrix
        matrix.append([])
        for column in range(n):
            # Adding zero into each list of the matrix
            matrix[row].append(0)
    # Return the matrix
    return matrix


# The function which returns the number of friends in common for two users
def num_in_common_between_lists(list1: List[int], list2: List[int]) -> int:
    # Initialization
    num_in_common = 0
    # Iterate over the length of list of connections of user 1
    for i in range(len(list1)):
        # Check if they have a same friend form user1's connections
        if list1[i] in list2:
            # Update the number of friends in common
            num_in_common += 1
    return num_in_common


# The function used to calculate similarity scores of the network matrix
def calc_similarity_scores(network: List[List[int]]) -> List[List[int]]:
    # Compute the number of users in social network
    n = len(network)
    # Build n x n matrix with all zero
    similarity_matrix = init_matrix(n)
    # Iterate each row
    for i in range(n):
        # Iterate over each column
        for j in range(n):
            # Insert the number of common friends as similarity scores and update the similarity matrix
            similarity_matrix[i][j] = num_in_common_between_lists(network[i], network[j])
    # Return the matrix
    return similarity_matrix


# Function which used to figure out a suggestion for user_id
def recommend(user_id: int, network: List[List[int]], similarity_matrix: List[List[int]]) -> int:
    # Initialization for max similarity score and its index
    max_value = -1
    max_index = -1
    # Iterate over each item in the list of user's similarity scores with all other users
    for i in range(len(network)):
        # Check the suggestion won't be itself or someone who is already a friend of user
        # Check the condition for updating max similarity score
        if i != user_id and i not in network[user_id] and max_value < similarity_matrix[user_id][i]:
            # Update max similarity score and its index
            max_index = i
            max_value = similarity_matrix[user_id][i]
    # Return the index of recommend subject
    return max_index


def main():
    # Title of the program
    print("Facebook friend recommendation.")
    # Call the functions to open and read a data file
    network = read_file(open_file())
    # Obtain the similarity_matrix
    similarity_matrix = calc_similarity_scores(network)
    # Obtain the number of users in the social network provided
    number_of_users = len(network)
    # Initialization
    play_again = "yes"
    # Check if user want to find a suggestion
    while play_again.lower() == "yes":
        # Prompt the user to enter an integer as user ID
        user_id = input("Enter an integer in the range 0 to {}:".format(number_of_users - 1))
        # Check if the input is valid or not
        while not user_id.isnumeric() or int(user_id) not in range(number_of_users):
            # The user has entered an invalid user ID.
            # Prompt the user to re-enter a value until it is a valid value
            print("Error: input must be an int between 0 and {}".format(number_of_users - 1))
            user_id = input("Enter an integer in the range 0 to {}:".format(number_of_users - 1))
        # Obtain the user ID of the suggested friend
        rec_friend = recommend(int(user_id), network, similarity_matrix)
        # Print out final suggestion for user
        print("The suggested friend for", user_id, "is", rec_friend)
        # Check if the user want another suggestion for another user
        play_again = input("Do you want to continue (yes/no)?").lower()


if __name__ == "__main__":
    # Call the boss function
    main()
