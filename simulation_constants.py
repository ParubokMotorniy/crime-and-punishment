g = 5 #theft gain
l = 10 #theft loss
p = 25 #punishment

k = 5 #inspection cost
r = 10 #inspection reward
 
################################################################################ 

s_i = k / r #crime commitment probability, as follows from the derivative of rational inspection utility 
c_j = g / p #inspection probability, as follows from the derivative of rational crime utility 

randomness_weight = 0.0
rationality_weight = 1.0 - randomness_weight

agent_memory_length = 1001
