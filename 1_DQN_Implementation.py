#!/usr/bin/env python
import keras, tensorflow as tf, numpy as np, gym, sys, copy, argparse

from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam

episodes = 100


# class QNetwork():

# 	# This class essentially defines the network architecture. 
# 	# The network should take in state of the world as an input, 
# 	# and output Q values of the actions available to the agent as the output. 

# 	def __init__(self, environment_name):
# 	# Define your network architecture here. It is also a good idea to define any training operations 
# 	# and optimizers here, initialize your variables, or alternately compile your model here.
# 	pass


# 	def save_model_weights(self, suffix):
# 	# Helper function to save your model / weights.
# 	pass

# 	def load_model(self, model_file):
# 	# Helper function to load an existing model.
# 	pass

# 	def load_model_weights(self,weight_file):
# 	# Helper funciton to load model weights. 
# 	pass

class Replay_Memory():

	def __init__(self, memory_size=50000, burn_in=10000):

		# The memory essentially stores transitions recorder from the agent
		# taking actions in the environment.

		# Burn in episodes define the number of episodes that are written into the memory from the 
		# randomly initialized agent. Memory size is the maximum size after which old elements in the memory are replaced. 
		# A simple (if not the most efficient) was to implement the memory is as a list of transitions. 
		pass

	def sample_batch(self, batch_size=32):
		# This function returns a batch of randomly sampled transitions - i.e. state, action, reward, next state, terminal flag tuples. 
		# You will feed this to your model to train.
		pass

	def append(self, transition):
		# Appends transition to the memory. 	
		pass

class DQN_Agent():

	# In this class, we will implement functions to do the following. 
	# (1) Create an instance of the Q Network class.
	# (2) Create a function that constructs a policy from the Q values predicted by the Q Network. 
	#		(a) Epsilon Greedy Policy.
	# 		(b) Greedy Policy. 
	# (3) Create a function to train the Q Network, by interacting with the environment.
	# (4) Create a function to test the Q Network's performance on the environment.
	# (5) Create a function for Experience Replay.
	
	def __init__(self, environment_name, render=False):

		# Create an instance of the network itself, as well as the memory. 
		# Here is also a good place to set environmental parameters,
		# as well as training parameters - number of episodes / iterations, etc. 
		
		# env = QNetwork(environment_name)
		self.env = gym.make(environment_name)
		self.state_size = self.env.observation_space.shape[0]
		self.action_size = self.env.action_space.n

		if environment_name == 'MountainCar-v0':
			self.gamma = 1
			self.iterations = 4000
		elif environment_name == 'CartPole-v0':
			self.gamma = 0.99
			self.iterations = 1000000
		self.alpha = 0.0001
		self.epsilon = 0.5

		# self.model = self._build_model()
		self.model = Sequential()
		self.model.add(Dense(self.action_size, input_dim=self.state_size,use_bias=True, activation='linear'))
		self.model.compile(loss='mse', optimizer=Adam(lr=self.alpha))


	def epsilon_greedy_policy(self, q_values):
		# Creating epsilon greedy probabilities to sample from.             
		rand = np.random.uniform(0,1)

		if(rand<=self.epsilon):
			return np.random.randint(0,self.action_size)
		else:
			return np.argmax(q_values) 

	def greedy_policy(self, q_values):
		# Creating greedy policy for test time. 
		return np.argmax(q_values) 

	def train(self):
		# In this function, we will train our network. 
		# If training without experience replay_memory, then you will interact with the environment 
		# in this function, while also updating your network parameters. 

		env = self.env

		for t_iter in range(self.iterations):
			state = env.reset()
			# state = np.reshape(state,[1,self.state_size])	
			# print(self.model.predict(state))
			print('iteration no ',t_iter)

			while True:
				action = self.epsilon_greedy_policy(self.model.predict(state))
				env.render()
				next_state, reward, done, info = env.step(action)
				next_state = np.reshape(state,[1,self.state_size])	
				if done:
					q_value_prime = reward
					q_value_target = self.model.predict(state)
					q_value_target[0][action] = q_value_prime
					self.model.fit(state,q_value_target,epochs=1, verbose=0)
					print('episode end')
					print(self.model.layer.get_weights())
					break
				else:
					q_value_prime = reward + self.gamma * np.max(self.model.predict(next_state)[0])

				q_value_target = self.model.predict(state)
				q_value_target[0][action] = q_value_prime
				self.model.fit(state,q_value_target,epochs=1, verbose=0)
				state = next_state


		# If you are using a replay memory, you should interact with environment here, and store these 
		# transitions to memory, while also updating your model.

	def test(self, model_file=None):
		# Evaluate the performance of your agent over 100 episodes, by calculating cummulative rewards for the 100 episodes.
		# Here you need to interact with the environment, irrespective of whether you are using a memory. 
		pass

  #   def burn_in_memory():
		# # # Initialize your replay memory with a burn_in number of episodes / transitions. 

		# pass

def parse_arguments():
	parser = argparse.ArgumentParser(description='Deep Q Network Argument Parser')
	parser.add_argument('--env',dest='env',type=str)
	parser.add_argument('--render',dest='render',type=int,default=0)
	parser.add_argument('--train',dest='train',type=int,default=1)
	parser.add_argument('--model',dest='model_file',type=str)
	return parser.parse_args()

def main(args):

	args = parse_arguments()
	environment_name = args.env
	dqn_agen = DQN_Agent(environment_name)

	dqn_agen.train()

	# Setting the session to allow growth, so it doesn't allocate all GPU memory. 
	gpu_ops = tf.GPUOptions(allow_growth=True)
	config = tf.ConfigProto(gpu_options=gpu_ops)
	sess = tf.Session(config=config)

	# Setting this as the default tensorflow session. 
	keras.backend.tensorflow_backend.set_session(sess)

	# You want to create an instance of the DQN_Agent class here, and then train / test it. 

if __name__ == '__main__':
	main(sys.argv)

