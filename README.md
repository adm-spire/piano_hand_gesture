# piano_hand_gesture

####  this project utilizes pygame , opencv and mediapipe to simulate piano and drums without require physical sensors . Users can play these instruments using hand gestures.

>[!IMPORTANT]
> ### Usage
> - project3.py is the actual program for this project , it opens up opencv window with an template and pygame piano.
>  - drag the keyboard over the template and play any number of keys using all fingers of both hands.
>  - quit by pressing 'q'
> - drum2.py is program for playing two types of drums , if finger point is detected inside the circle , sound is played
> - piano_lists.py is the mapping of piano keys.
> - there are some audio files for the piano and drum.

>[!NOTE]
> ### This program requires a webcam

####  mediapipe is a library by google , it contains models trained on images of hand and faces . I am using this library to detect finger tips , then i am mapping the locations of finger tips using opencv with help of template of piano , finally the actual piano which i made using pygame.

![](https://github.com/adm-spire/piano_hand_gesture/blob/master/Screenshot%202024-04-26%20002908.png)
![](https://github.com/adm-spire/piano_hand_gesture/blob/master/Screenshot%202024-04-26%20010457.png)
