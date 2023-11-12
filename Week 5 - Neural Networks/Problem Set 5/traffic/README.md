YouTube Link: https://youtu.be/m4bJerM1QgQ
Github Username: erenesinler23

Modifications and Corresponding Results: 
** Max-Pooling Layer is 2x2 and Kernel is 3x3 | These Are Constants
** Dropout always set to 0.5. 

1st Try:
** Usage: One convolutional layer with 32 filter and one max-pooling layer,
one hidden layer with 256 units. 
** Result: 333/333 - 1s - loss: 0.8769 - accuracy: 0.7163 - 1s/epoch - 3ms/step
** NOTES: Very low accuracy, fast in each step. 

2nd Try:
** Usage: One convolutional layer with 32 filter and one max-pooling layer,
one hidden layer with 512 units. 
** Result: 333/333 - 4s - loss: 0.2933 - accuracy: 0.9079 - 4s/epoch - 11ms/step
** NOTES: Moderate accuracy, very slow in each step. 

3rd Try:
** Usage: Two convolutional layers with 32 (each) filters and two max-pooling layers,
one hidden layer with 512 units. 
** Result: 333/333 - 1s - loss: 0.1638 - accuracy: 0.9172 - 1s/epoch - 5ms/step
** NOTES: Good accuracy and fast in each step.

4th Try: 
** Usage: Two convolutional layers with 32 (each) filters and two max-pooling layers,
two hidden layers with 512 and 256 units. 
** Result: 333/333 - 1s - loss: 0.2738 - accuracy: 0.9387 - 1s/epoch - 4ms/step
** NOTES: Very good in accuracy, fast in each step. 

** The 4th try was the best result because it was the trial with the highest amount 
of hidden layers and units. Also it was the trial with the highest amount of 
convolutional and max-pooling layers with highest filters. 