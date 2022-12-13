## project1_algorithmTrading
--------------
### 1. Purpose
Making automatic stock trading algorithm
In short, AI trader

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
  1. Open GUI
  2. Initialize
    + Connecting to database
    + Setting hyperparameters of networks
  3. Get informations from database
  4. Refine the informations into inputs
  5. Put the inputs into policy network(pi)
  6. Decide what action to take by pi
  7. Act
  8. Calculate value of current state
  9. Calculate reward of value
  10. Calculate Loss by using the reward
  ```
  v_s = self.network.v(inputData_old)
        v_s_prime = self.network.v(inputData)

        TD_target = reward + self.future_value_retention_rate * v_s_prime
        delta = TD_target - v_s

        v_Loss = F.mse_loss(v_s, TD_target.detach())
        pi_Loss = -torch.log(pi) * delta.detach()
        Loss = pi_Loss + v_Loss
  
  ```


-----------------------
### 4. Issues
+ Collision between Nvidia cuda module and asyncronization
+ Learning process is so slow that it can't be finished by home level desktop computer
