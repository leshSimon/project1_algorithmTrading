## project1_algorithmTrading

![playing momont](https://user-images.githubusercontent.com/54647455/207383532-03c553e0-6870-4c8a-9470-9004b78a9f2d.png)



--------------
### 1. Purpose
Making automatic stock trading algorithm, in short, AI trader

--------------
### 2. Used stacks
+ Language
  + Python

+ Database
  + MySQL
  + Saving past chronological stock prices
  + Schema of a list of companies and prices
  + Open, high, low, close price per one day

+ Deep learning
  + Pytorch
  + LSTM
  + numPy, cuda
  + Constructing
    + Policy network
    + Value network

+ Reinforcement learning
  + A3C
  + Defining loss function

+ API
  + Securities company's stock api
  + In order to get past information
  + And manipulate real trading

+ GUI module
  + PyQt5
  + Visualizing process

-------------------
### 3. Mechanism
+ Process
  + Open GUI
  + Initialize
    + Connecting to database
    + Setting hyperparameters of networks
  + Get informations from database
  + Refine the informations into inputs
  + Put the inputs into policy network(pi)
  + Decide what action to take by pi
  + Act
  + Calculate value of current state
  + Calculate reward of value
  + Calculate Loss by using the reward
  ```
  v_s = self.network.v(inputData_old)
  v_s_prime = self.network.v(inputData)

  TD_target = reward + self.future_value_retention_rate * v_s_prime
  delta = TD_target - v_s

  v_Loss = F.mse_loss(v_s, TD_target.detach())
  pi_Loss = -torch.log(pi) * delta.detach()
  Loss = pi_Loss + v_Loss  
  ```
  + Backpropagation and update one step
  + Repeat


-----------------------
### 4. Issues
+ Collision between Nvidia cuda module and asyncronization.
+ Learning process is so slow that it can't be finished by home level desktop computer.
+ How to set the hyperparameters to optimize is still unknown.
