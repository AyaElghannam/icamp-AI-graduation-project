# Deep Learning Model
The goal of SIGNARA is to develop software that is capable of real-time translation of Arabic sign language into text. Due to resources and time constraints, the scope has been limited to implementing 9 Words and the whole Arabic alphabet.

We achieved the words sector using [Mediapipe](https://mediapipe.dev/) - a framework for building multimodal, cross-platform, applied ML pipelines. While the alphabets sector Uses transfer learning. 

<p align="center">
<img src="img\Mediapipe.png" alt="Meidapipe"/>
</p>

Now we will discuss technical details of the 2 sectors:

## Words
Challenges we faced while doing this part for having a dynamic data that can be represented as series of motion we had many questions during the research process

### Dataset
After doing online research we found that there is no public dataset for the Arabic Sign Language words which contain continuous motion. So we started collecting our dataset by capturing video that takes 30 and 60 Frames of the word motion. We Captured 120 videos of 2 different data collectors to have a variety

### Model
Deep learning methods such as recurrent neural networks like as LSTMs and variations that make use of one-dimensional convolutional neural networks or CNNs have been shown to provide state-of-the-art results on challenging activity recognition tasks with little or no data feature engineering, instead using feature learning on raw data.
We applied our knowledge and tried many deep learning algorithms in order to get insghts of the performance by comparing different approaches.
- CONV1D
- LSTM
- CONV1DLSTM
- LSTM With CTC Loss
- Transformers

## Characters

<p align="center">
<img src="img\Char.png" alt="Characters"/>
</p>

We found dataset consists of 54,049 images of [ArSL alphabets](https://data.mendeley.com/datasets/y7pckrw6z2/1) performed by more than 40 people for 32 standard Arabic signs and alphabets. The number of images per class differs from one class to another. The dataset gathered are of size 64 * 64 Pixels of grayscale.

Deep convolutional neural network models may take days or even weeks to train on very large datasets.

A way to short-cut this process is to re-use the model weights from pre-trained models that were developed for standard computer vision benchmark datasets, such as the ImageNet image recognition tasks. Top performing models can be downloaded and used directly, or integrated into a new model for your own computer vision problems. This way is called Transfer Learning

In our Approach we used VGG16 Model ,The model achieves 92.7% top-5 test accuracy in ImageNet, which is a dataset of over 14 million images belonging to 1000 classes.