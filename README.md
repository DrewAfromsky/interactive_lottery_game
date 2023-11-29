##### Problem Statement
* Some number of players, `0 <= N <= 10x10^6` , have picked 5 distinct numbers from 1 to 90. Each week, a lottery organization picks 5 numbers between 1 and 90, inclusively, randomly. Players are rewarded based upon how many of the weekly set of 5 numbers match with the ones they have selected. Players must have at least two matching numbers to win.
* Given an input file, a txt/ASCII file, where each line represents one player's picks and contains 5 space-separated integers, report the number of winners per category, where a category is the number of matching numbers and is represented by a 2, 3, 4, or 5.
* When the lottery organization picks the set of 5 distinct numbers, all numbers are generated prior to determining winners. The desired stdout looks like the following, where the input file is processed only once and `a b c d` is the output where `a,b,c,` and `d` represent the number of players/winners for each of the four matching categories, 2,3,4,5 respectively).

```
READY
>>> 19 77 24 27 8 (​Example lottery committee numbers; provided by the user)

Run the application with input txt file and display the following to stdout:

​1 1​2 ​81​8 ​22613 (Number of winners, for each category 2,3,4, and 5​. 1 player has 2 matching numbers, 12 players have 3 matching numbers, 818 players have 4 matching numbers, and 22613 have 5 matching numbers)
```

##### Solution Overview
* **Workflow**
	1. Read in the input file (serial read)
	2. Partition the input file into batches, representing groups of players
	3. For each batch, assign a process to it
	4. Define a hashmap/Python dictionary with keys as the 4 winning categories and values the number of players that have won in that category
	5. For each assigned batch and process, calculate number of matches between each number in the player's set and the winning lottery numbers picked by the committee
	6. Find this number in the hashmap's keys and increment the associated values by 1 if there were at least 2 matches
	7. Do this for all processes/players and return a formatted version of the values in the hashmap printed to stdout

* **Implementation**
	- `main.py` is a program/executable file with the instructions to get the number of winners per each category.
	- `main.py` is loaded into memory (process, with its own memory space).
	- Detailed "how to use" instructions are below, but the program is accessible via a Docker container:
		- `docker run -it -v $PWD:/data --rm <image_name> bash` , entering a bash Linux terminal, then running `python3 main.py --input /data/<name_of_file.txt>` to bring up the interactive game.
	* **Single-Process solution**
		* A single process running on the entire input file, not in batches
		* The process will get winners and print to stdout
	* **Multi-Process solution**
		* Create batches of players
			* Batch size is the number of rows of input file divided by number of available cpu on the machine
		* Assign a process to each batch of players
		* Each process will operate on a batch of players, getting winners for that batch and return a dictionary 
			* The returned dictionary represents the number of winners per category for that batch of players
		* The returned dictionaries by each process is put into a list, which is used as input to return the desired stdout
		* After all dictionaries are generated, perform a final merging and reformatting on all the dictionaries to print to stdout
##### Performance (Time and Space Complexity)
* _Documented in the code as comments._
* `TLDR;` Runtime is calculated from reading in the input file, getting all winners per batch, performing some processing steps, and printing the number of winners per category to stdout
	* The input file is read serially using Python's built-in `open()` function enclosed in a `with` statement, which ensures proper acquisition and release of object resources when the code using the resource is completely executed. Within the `with` statement, all lines in the file are read and returned as a list where each line is an item in the list object.
	* `update_winner_map` is the primary function for getting winners from batches of players and returning a dictionary representing the number of winners by category for the batch
	* `update_winner_map` accepts a list of players (as strings) from the batch as input. It begins by initializing a dictionary representing winners per category. It iterates over the provided batch of players, which is `O(N)` where `N` is the number of players in the batch, stores a constant per player in the loop that gets overwritten during each iteration (i.e. number of matches between player and committee lottery numbers), compares the numbers from the player (`O(N=5 numbers)`) and the committee's picks in an inner loop (i.e. `O(N=5 numbers)`, since each player will always have 5 numbers; this inner loop is `O(5x5=25)`), then finally, for each player, in the outer loop, check that matches is `>=` 2 to update the dictionary for that batch of players.
* The Python multiprocessing module introduces APIs, such as accessing a `Pool` object, allowing parallelized execution of the `update_winner_map` function across multiple input values (i.e. batches of players and committee lottery numbers), distributing the input batches across processes. The `Pool` object also offers access to the `starmap` method, which maps a function (`update_winner_map`) to a set of iterables of iterables, (i.e. `zip(batches, [committee_lottery_numbers]*len(batches))`), where the inner iterables are unpacked as arguments to the `update_winner_map` function. Python's `zip()` function accepts iterables as arguments and returns an iterator.
* Without running numerous amounts of tests and benchmarking the runtime for the fixed input file size, the observable total execution time, including printing to stdout, is ~1.8-2.4 seconds.
##### Containerization
* The solution is deployed/packaged as a Linux container (Docker container), with all the dependencies and necessary files to keep the application isolated. The Docker container will have its own isolated running process, file system, and network. The container is started/ran from the container image (static version of all the files, environment variables, and the default command/program present in the container). Any changes caused by the running container will exist only in that container, but would not persist in the underlying container image (would not be saved to disk). The container image includes in its metadata the default program/command that should be run when the container is started and the parameters to be passed to that program/command. The container image is a Docker image, based on an official Python image.
##### How to Use
* Requires an installation of **Docker** then can run the following commands:

	###### Build the Docker image
	`docker build -t <image_name> --target base .`
	
	###### Run the Docker image
	`docker run -it -v $PWD:/data --rm <image_name> bash`, where `$PWD` is the absolute file path to the current working directory with only the custom input file in its path.
	`--rm` option tells Docker to automatically remove the container when it exits.

* This command will bring up a Linux terminal and bring you to the `/code` directory. From here you can run `python3 main.py --input /data/<name_of_file.txt>`, which will bring up the interactive lottery game! 
* Here you can provide 5 space-separated numbers in the inclusive range `[1, 90]` and check if there are matches!
* To quit the game, hit `CTRL+C` and to exit the Docker shell, run `exit`
##### Considerations
* **Container Memory**
	* Running a single process per container will have a more or less stable, and limited amount of memory consumed by the container
	* If we wanted to deploy this solution to a cluster, we'd be able to set those same memory limits and requirements in a configuration for the container management system like Kubernetes. That way it will be able to replicate the container in the available machines taking into account the amount of memory needed by them, and the amount available in the machines in the cluster. The app is very simple, so this wouldn't necessarily be a problem, but something to consider for more resource-intensive applications, where we would want to adjust the number of container in each machine or add more machines to the cluster.
##### Test Cases
`docker build -t <image_name> --target test . && docker run --rm <image_name>`

* The testing conducted tests inputs and outputs for the `update_winner_map` function, `get_winners` function, and the `report_winners_per_category` function. It focuses on unit testing each function, integration testing, and system testing. 
	* `Unit tests`: tests on individual components that each have a single responsibility
	* `Integration tests`: tests on the combined functionality of individual components
	* `System tests`: tests on the design of a system for expected outputs given inputs
* Other forms of validations including validating user input and only reporting winners with at least two matches is performed in the code.

***Things NOT tested:***
* (1.) Test code that makes an external HTTP request to a third-party API and database queries -- ideally would be able to mock the request. This test isn't relevant to the problem, since there are no requests like this being made. Also, our input file is currently saved directly into the Docker container file system. 
* (2.) If working with cloud-based storage or databases like DynamoDB, we can create temporary objects like a table via a `setupclass`, run a test on it, then tear it down via a `teardown class`, using SDK specific API calls to a cloud service.
* (3.) There are other forms of testing (mutation testing, hypotheses testing, regression testing, etc)