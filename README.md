# Cascade OMR
Cascade OMR is an Optical Music Recognition System using Cascade Classifier to detect the musical notation. 

# Description
In this project, we explore techniques and algorithms to implement optical music recognition. This paper aims to encourage people who just begin and enjoy learning object detection by using a simple and comprehensible framework called Haar-like Feature to detect the music notation and generate musical alphabets to assist those who have a difficult time in memorizing it. The paper will include the process of how to generate the cascade classifier model and how to imply them to detect the target object.
The limitation of this project digital sheet which have a good resolution (above 720p) to obtain a high accuracy rate, and handwritten sheets are excluded.
In this project, the whole system is build from scatch include the classifier models. The Cascade OMR architecture are divide into 4 parts.

## 1. Pre-image processing
In pre-image processing, we using Otsu's threshold to convert RGB image into a binary image. Since most of the sheet music’s are black and white, so Otsu’s threshold is the most suitable image processing for the framework, which is to remove noises and convert image into binarization.

## 2. Staff-line detection
In staff-line detection process, we divide it into 2 small processs. First, we extract the staff-line out or in other words, separate the staff-lines from the music notations by using Morphological operation.Morphological operation is a theory and technique for preprocessing images based on shapes. The Morphological operation usually works with the binary image. To apply morphological operation, first we need a structuring element or kernel. The structuring element or kernel can be known as a shape, which we use as a template to extract from the input image. Therefore, in this step, the shape that we want to extract out is a line, also known as the staff-line. According to Morphological Operations, first, we need to define a shape or structuring element. The structuring element here can be created by defining a one-pixel line with a length of a quarter of input image width.
After creating the structuring element, we applied it to Morphological operation and obtained an output image of all staff-line are separated from all music notation. Next step, we need to get coordinate of the staff-line and prepare them for the pitch alphabet determination process.

![Before_And_After_extraction](https://user-images.githubusercontent.com/49471123/116553544-70b8ad00-a924-11eb-96d7-de3665788e37.png)

Before (Upper) and After (Lower) the extraction.

## 3. Music Notation Detection
In this project, we will focus on 7 musical notation which is the target object to detect.

![Screenshot (184)](https://user-images.githubusercontent.com/49471123/116567670-0a3a8b80-a932-11eb-9014-8da0908adf69.png)

In training cascade classifiers, we need several hundred positive sample and negative images of the same size.
For the size of positive images in each classifier training, we recommended setting it equally. For example, the size of quarter note head positive image is 32 x 32 pixel, so make sure that the size of the quarter note head’s positive images are the same size. But not all sizes of positive images of these seven classifiers must set to be equal. For instance, the size of the quarter note head’s positive images is 32 x 32 pixels, while treble clef’s positive images are 40 x 100 pixels. The reason that the size of positive images in each classifier are recommended to set equal because once we train for the classifier, all positive images of the current training classifier are set to be the same, so if the size of the positive images of the current classifier are different it will resize them, this cause change to the aspect ratio of the images. The size of negative images is recommended to be bigger than the positive image. 
The training stage will define how precise your cascade classifier model is. Therefore, the more stage we set, the better it is. However, the cascade classifier will not found anything and loss time if we overtrained it. Therefore, the training stage is recommended to set between 15 - 20 stages to create a strong cascade classifier model.
Once all seven classifier models are complete training, we can use these classifier model to detect the music notation; if music notation is found, it returns the position of detected notations as a rectangle (x, y, w, h), as shown below.

![Screenshot (186)](https://user-images.githubusercontent.com/49471123/116553319-32bb8900-a924-11eb-93b7-7383a05b4a07.png)


# 4. Pitch Alphabet Determination
In the pitch alphabet determination process, we use the coordinates of the staff-line and music notation to determine the pitch alphabet. In music theory, the pitch alphabet is determined by the position of the note compared to the staff-line and what clef they are.

![Screenshot (187)](https://user-images.githubusercontent.com/49471123/116553421-4cf56700-a924-11eb-9f63-6adeb1db1c09.png)



In pitch alphabet process we divide the process into 3 steps.
1.	Group up the staff-lines into two groups which are treble and bass groups
2.	Determine the scale signature of that clef group.
3.	Start comparing music notation with staff-line group and determine the scoring base on music theory.
During the process of grouping up the staff-line, we divide the staff-line and arrange them into two groups and store them into 2D- array as follow:
treble=[[no.flat,no.sharp,treble.start,treble.end],[stafflines]]
The example of 2D array is shown below as example.

![Screenshot (188)](https://user-images.githubusercontent.com/49471123/116553433-5088ee00-a924-11eb-80d2-fb68308c7c87.png)


The number of flat and sharp in the array are used to define the scale signature of the clef. Treble start and treble end are used to define the area of the treble clef. From Figure 7, we can see that the treble clef is defined from x-coordinate 5 till x-coordinate 205 while from x-coordinate  206 are known as the bass clef. By doing this, we can easily define the pitch alphabet easier for treble clef and bass clef.
Once we obtain the 2D-array, the next step is to define the pitch alphabet. As we knew that the pitch alphabet is determined by the staff-line, therefore we started comparing the coordinate of the note head with the staff-line. However, the bounding boxes generated by the cascade classifier are overflow the note head position, which becomes a problem for us to determine the score. So, we need to define a safe zone or a value where the bounding box can be located within that safe zone or value which shown as an example below: 

![Screenshot (189)](https://user-images.githubusercontent.com/49471123/116553452-541c7500-a924-11eb-9e8c-dc1a445f6290.png)


After we define an area that the note head could be located on which staff-line, then we can define the pitch alphabet of it according to music theory. For the bounding box of notehead, which locate in the middle of the space between staff-line, we can found it by using the current staff-line value + half-space. For half-space value, we can calculate it by finding the space between each staff-line and divide it by 2. However, there are note heads locates beyond the staff-line, but it still defines in that staff-line group, which is shown as below:

![Screenshot (190)](https://user-images.githubusercontent.com/49471123/116553464-57affc00-a924-11eb-8a55-3cf24ba826f5.png)


In this case, we can define the next staff-line, which we knew as the 6th staff-line, by adding a space value (shown in Figure 8), to the 5th staff line. By using the value of the 6th staff-line and compare to the note head, which can be defined as follow:
staffline[5]+space-safeArea < noteHead < staffline[5]+space+safeArea
If the equation is true then we can define the pitch alphabet of the current note head as B, which is shown below:

![Screenshot (192)](https://user-images.githubusercontent.com/49471123/116553472-5aaaec80-a924-11eb-86ce-a6e3962bcb95.png)


## Evaluation

In this project, we accomplish the evaluation of the system by input plenty of sheet music. The procedure is the system will compress the images into multiple resolutions from lowest to highest. Once it is done compressing, images will send to the detection system to obtain the result.
With the method described above, we start obtaining how the resolution could affect the accuracy of the music note. We resize the sheet music to respective sizes and do the testing with each different resolution. We try to investigate the accuracy and the detected rate varies with different resolutions by testing 193 notes. Table I shows the comparison of the detected rate and accuracy rate with the number of notes as well as its percentage in total. The number of detected notes increases dramatically with the 1080p resolution.
However, we also encounter some problems with sheet music that has a resolution below 1080p. The problem is the pitch alphabet of note are not detected very well according to the blurriness of the sheet. Hence, it causes a low accuracy rate of detection ability. Therefore, in the later testing, we will use the sheet music with above 1080p resolution. The number and percentage of accuracy are shown:

![Screenshot (193)](https://user-images.githubusercontent.com/49471123/116553484-5da5dd00-a924-11eb-95d9-7f1cf79cf1f4.png)


Once we get the optimal resolution (≥1080p), we keep on testing the note detection and recognition.  In total, we tested approximately 2,325 music notes, which the result is shown in below From the table, we can see that 2,283 notes are detected out of 2,325 notes, which reach up to 98.19% of the total notes. For the accuracy rate, according to Table below, the system is able to determine the pitch alphabet around 2,272 correctly out of 2,283, which brings up to 99.56% high. 

![Screenshot (194)](https://user-images.githubusercontent.com/49471123/116553498-61d1fa80-a924-11eb-8ea8-a0c27cebdf78.png)

# Installation
In this project, we are using Flask Application, and the installation is use pip to install all the library.
To install, run:
```bash
pip3 install -r requirements.txt
```

# Usage

Run the application by:

```bash
flask run --host=0.0.0.0
```

The application provide 2 choices:
- See the existing example sheet that the application provide
- Upload sheet music as pdf or any image file formats
![home](https://user-images.githubusercontent.com/49471123/116553204-13246080-a924-11eb-9023-8830d729f386.jpg)
![sheetCollections](https://user-images.githubusercontent.com/49471123/116553213-17507e00-a924-11eb-915e-3de62374154c.jpg)
![test1](https://user-images.githubusercontent.com/49471123/116553218-191a4180-a924-11eb-9ff0-9bcc48bf8714.jpg)
![test2](https://user-images.githubusercontent.com/49471123/116553235-1c153200-a924-11eb-8d63-916bebb639af.jpg)
![test3](https://user-images.githubusercontent.com/49471123/116553248-1f102280-a924-11eb-914b-7e5c8ed6f5bb.jpg)

