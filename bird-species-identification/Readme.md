
**Goal**

The goal of the project is to develop a model in kaggle to classify bird species and score as high an accuracy score as possible.

In order to improve the score, following tricks were used :

*1) Label Smoothing*
- Label Smoothing encourages a finite output from the fully-connected layer and can generalize better, with fewer extreme values.

*2) LR Scheduler*
- Created a scheduler which will warmup and cooldown over 5 epochs

*3) Mixup training*

- In mixup, each time we randomly sample two examples (xi; yi) and (xj ; yj). Then we form a new example by a weighted linear interpolation of these two examples:

^x =  xi + (1-lambda)xj;

^y =  yi + (1-lambda)yj;

where lambda in [0;1] is a random number drawn from the Beta(alpha;alpha) distribution. In mixup training, we only use the new example (^x; ^y)
