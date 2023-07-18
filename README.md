# xG-soccer

• Expected goals metric is one of the widely used metrics in football analytics field. It allows us to evaluate team and player performance.

• In a low-scoring game such as football, final match score does not provide a clear picture of the performance. This is why more and more sports analytics turn to the advanced models like xG, which is a statistical measure of the quality of chances created and conceded.

# What is xG?
• Put simply, Expected Goals (xG) is a metric designed to measure the probability of a shot resulting in a goal.

• An xG model uses historical information from thousands of shots with similar characteristics to estimate the likelihood of a goal on a scale between 0 and 1.

• For example, a shot with an xG value of 0.2 is one that we would generally expect to be converted twice in every 10 attempts.

# How is xG calculated?
• Each xG model has its own characteristics, but these are the main factors that have traditionally been fed into the large majority of Expected Goals models: distance to goal, angle to goal, body part with which the shot was taken, and type of assist or previous action (throughball, cross, set-piece, dribble, etc…). Based on historical information of shots with similar characteristics, the xG model then attributes a value between 0 and 1 to each shot that expresses the probability of it producing a goal.

# Why is xG important?
• xG models are important because they are the most accurate predictor of future team and player performance available. At a team level, Expected Goals models are more predictive of future performance than both current goal difference and simple shot-count metrics such as Total Shots Ratio (TSR). xG models allow us to look beyond current results to get a better idea of the underlying quality of both teams and players.

# xG Model
• I have used Statsbomb's open-data for traning and testing my models

• Attributes:

  • under_pressure

  • position
  
  • play_pattern
  
  • body_part
  
  • technique
  
  • type
  
  • distance
  
  • angle

# scikit-learn

• Logistic regression
  
  • fit(X,Y)
  
  • predict(X)
  
  • predict_proba(X)
  
  • score(X,Y)

• Random forest
  
  • fit(X,Y)
  
  • predict(X)
  
  • score(X,Y)
