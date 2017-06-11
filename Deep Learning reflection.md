Tensorflow learning guide : http://www.yuchao.us/2017/01/tensorflow-my-learning-experience.html

Tensor board: http://www.yuchao.us/2017/02/tensorboard.html 

It's time to reflection on what projects I have accomplished.

| Postdate   | dateset       | records    | in/out   | Note                                     |
| ---------- | ------------- | ---------- | -------- | ---------------------------------------- |
| 2016-10-25 | MNIST         | 60 k/ 10 k | 28^2 /10 | NNDL1,sigmoid                            |
| 2016-10-27 | MNIST         | 60 k/ 10 k | 28^2 /10 | MNDL3,softmax, cross entropy             |
| 2016-10-31 | MNIST         | 60 k/ 10 k | 28^2 /10 | MNDL4, CNN, theano                       |
| 2017-2-2   | notMNIST      | 520 k      | 28^2 /10 | Tensorflow practice                      |
| 2017-2-2   | SVHN          | 99 k       | 1024/10  | Tensorflow                               |
| 2017-2-13  | bikeshareDC   | 17.4 k     | 16/reg   | from scratch, 56-30-1 net                |
| 2017-2-27  | movieReview   | 25 k       | 10 k/ 2  | from scratch, 10k-10-1 net               |
| same       | same          | same       | same     | tflearn, 10k-200-25-2 softmax            |
| same       |               |            |          | miniflow                                 |
| same       | CIFAR-10      | 60 k       | 32^2/10  | tensorflow, cnn(32)-1024-10              |
| 2017-3-30  | movieReview   | 25 k       | 10 k/2   | tf.contrib.rnn                           |
| same       | TV script     | 11.5 k     |          | tf.contrib.rnn                           |
| 2017-6-6   | flowers       | 3.67 k     | 224^2/5  | vgg transfer(5 cnn)-256-5 tf.contrib.layers.fully_connected |
|            |               |            |          |                                          |
| 2017-4-1   | TrafficSign   | 50 k       | 36^2/43  | tf 5 layer LeNet, no dropout             |
| 2017-4-7   | ImageNet      |            | 227^2/1k | AlexNet: 5 cnn + 3 fc                    |
| 2017-4-7   | behaviorClone |            | 50 k/reg | Nvidia: 5 cnn + 4 fc, 5 M para           |
| 2017-4-15  | car image     | 18 k       | 64^2/reg | LeNet: 2cnn + 3 fc                       |
|            |               |            |          |                                          |

capstone video: https://youtu.be/w15GpupQusM

several tips:

Some suggestions from reviewer:

1. use [TensorFlow](https://www.tensorflow.org/api_docs/python/tf/image/rgb_to_grayscale) to convert RGB images to grayscale
2. implement early termination, instead of a fixed number of **epochs**
3. use image augmentation technique to rebalance the number of examples for each class.Check out [this article](https://medium.com/@vivek.yadav/dealing-with-unbalanced-data-generating-additional-data-by-jittering-the-original-image-7497fe2119c3#.wvp4g6hle)
4. use `plt.bar(x,y)` to visualize softmax probability distribution.

## Appendix: the battle for deep learning frameworks

![](https://leonardoaraujosantos.gitbooks.io/artificial-inteligence/content/more_images/DeepLibrariesOverview.jpg)