# Mooney Faces

Mooney faces are monochrome images of faces, heavily shadowed.
They were introduced by Craig Mooney.

Mooney’s original paper is unclear on the construction of the faces used as
stimuli: he states "The closure items were drawings of the heads and faces of
miscellaneous people. They presented, in solid blacks and whites, only the
salient shadows or high-lights, as revealed in strongly lighted photographs."
(Mooney, 1957).  

This python program generates Mooney style faces, using OpenCV and a fairly
simple algorithm. It was written to investigate the effect of various
parameters upon perception, including the presence or absence of a border,
the highlight/shadow colour, and motion. The software was inspired by (and mostly written
at) Dagstuhl, in seminar 15192 "The Message in the Shadow: Noise or
Knowledge?" [https://www.dagstuhl.de/en/program/calendar/semhp/?semnr=15192].

A video of the software in action can be found on youtube here: [https://www.youtube.com/watch?v=CHvpeir3dDA]

A summary of the algorithm follows:
set threshold t to mid-grey (126,126,126)
 - Take input image 
 - Run face detector
 - If face found set threshold t to mean face value
 - Blur image
 - Threshold by t
 - Morphologically tidy up the thresholded image
 - Colour in the image and draw a boundary line if required
 


C. M. Mooney. Age in the development of closure ability in children. Canadian
Journal of Psychology, 11:219–226 1957
[http://d20uo2axdbh83k.cloudfront.net/20140401/4843d99c2f0957c1212ccbb770e363cc.pdf ]
