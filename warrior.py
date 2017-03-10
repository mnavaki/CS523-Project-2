import numpy as np
import copy

# Defining some values
core_size = 8000

num_lines = 10

opcodes = ["dat","mov","add","sub",
           "mul","div","mod","jmp",
           "jmz","jmn","djn","spl",
           "slt","cmp","seq","sne",
           "nop"]
address_modes = ["#","$","@","<","*","{","}"]
mod_list = [ ".a ",".b ",".ab",".ba",".f ",".x ",".i "]

class Warrior:

	# If another Warrior is given, make a copy
	# Otherwise, randomly create new Warrior with num_lines number of lines when constructed
	def __init__(self, otherWarrior = None):
		self.fitness = 0
		if (otherWarrior is None):
			self.warriorCode = []
			for x in range(0, num_lines):
				# Choose opcode
				opcode = np.random.randint(len(opcodes))
				# Choose mod
				mod = np.random.randint(len(mod_list))
				# Choose address mode 1
				addmode1 = np.random.randint(len(address_modes))
				# Choose address 1
				add1 = np.random.randint(-20,20) #???
				# Choose address mode 2
				addmode2 = np.random.randint(len(address_modes))
				# Choose address 2
				add2 = np.random.randint(-20,20) #???
				# Insert new line into warriorCode
				self.warriorCode.append([opcode,mod,addmode1,add1,addmode2,add2])
		else:
			self.warriorCode = copy.deepcopy(otherWarrior.warriorCode)

	# Performs one-point crossover with another Warrior
	def crossover_one_point(self, otherWarrior):
		# Choose a crossover point
		point = np.random.randint(num_lines - 1) + 1
		for x in range(0, num_lines):
			if (x < point):
				temp = copy.copy(self.warriorCode[x])
				self.warriorCode[x] = copy.copy(otherWarrior.warriorCode[x])
				otherWarrior.warriorCode[x] = temp

	# Performs uniform crossover with another Warrior
	def crossover_uniform(self, otherWarrior):
		for x in range(0, num_lines):
			if (np.random.randint(1, 100) <= 50):
				temp = copy.copy(self.warriorCode[x])
				self.warriorCode[x] = copy.copy(otherWarrior.warriorCode[x])
				otherWarrior.warriorCode[x] = temp

	# Mutate at some rate % of mutation
	def mutate(self, rate):
		for x in range(0, num_lines):
			# For each element in the line, mutate with probability rate %
			if (np.random.randint(1, 100) <= rate):
				# Choose new opcode
				self.warriorCode[x][0] = np.random.randint(len(opcodes))
			if (np.random.randint(1, 100) <= rate):
				# Choose new mod
				self.warriorCode[x][1] = np.random.randint(len(mod_list))
			if (np.random.randint(1, 100) <= rate):
				# Choose new address mode 1
				self.warriorCode[x][2] = np.random.randint(len(address_modes))
			if (np.random.randint(1, 100) <= rate):
				# Choose new address 1
				self.warriorCode[x][3] = np.random.randint(-20,20) #???
			if (np.random.randint(1, 100) <= rate):
				# Choose new address mode 2
				self.warriorCode[x][4] = np.random.randint(len(address_modes))
			if (np.random.randint(1, 100) <= rate):
				# Choose new address 2
				self.warriorCode[x][5] = np.random.randint(-20,20) #???

	# Writes out the redcode file with specified filename and names the Warrior
	def writeFile(self, warrior_name, filename):
		header = "; redcode\n"
		header += "; name " + warrior_name + "\n"
		header += "; author T16\n"
		header += "; assert CORESIZE == " + str(core_size) + "\n"
		red_file = open(filename, "w+")  # open the warrior file
		red_file.write(header)
		for x in range(0, num_lines):
			line = opcodes[self.warriorCode[x][0]]
			line += mod_list[self.warriorCode[x][1]] + " "
			line += address_modes[self.warriorCode[x][2]]
			line += str(self.warriorCode[x][3]) + ","
			line += address_modes[self.warriorCode[x][4]]
			line += str(self.warriorCode[x][5])
			line += "\n"
			red_file.write(line)
		red_file.write("end ; execution ends here")


