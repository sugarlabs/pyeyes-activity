#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# PyEyes
# A simple face tracker using OpenCV and pygame.
# Nirav Patel http://eclecti.cc
# Copyright (C) 2008, 2009, 2010, 2011
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information:
# Nirav Patel <nrp@andrew.cmu.edu>
# Alan Aguiar <alanjas@gmail.com>


import pygame, sys, os

import opencv
from opencv.cv import *
from opencv.highgui import *


def main():
    storage = cvCreateMemStorage(0)
    cascade = cvLoadHaarClassifierCascade("opencv/data/haarcascade_frontalface_alt.xml", cvSize(1,1))
    capture = cvCreateCameraCapture(0)
    small = cvCreateImage(cvSize(320,240), 8, 1)
    gray = cvCreateImage(cvSize(640,480), 8, 1)
    size = (1200,900)
    screen = pygame.display.set_mode(size)
    
    surface = pygame.display.get_surface()    
    
    lefteye = pygame.Rect(0,0,550,800)
    righteye = pygame.Rect(650,0,550,800)

    leftx = 275
    lefty = 450
    width = 100
    running = True
    while running:
        screen.fill((255,255,255))
        
        pygame.draw.ellipse(surface, (0,0,0), lefteye, 50)
        pygame.draw.ellipse(surface, (0,0,0), righteye, 50)	
        frame = cvQueryFrame(capture)
        cvCvtColor(frame, gray, CV_BGR2GRAY)
        cvResize(gray, small, CV_INTER_NN)
        cvEqualizeHist(small,small)
        cvClearMemStorage(storage)
        faces = cvHaarDetectObjects(small, cascade, storage, 1.3, 2, CV_HAAR_DO_CANNY_PRUNING, cvSize(75, 75))
	
	# convert face location to approximate screen location
        if faces:
            for r in faces:
		leftx = int(430 - r.x)
		lefty = 200+int(1.8*(r.y + r.height/2))
                width = r.width

        pygame.draw.circle(surface, (0,0,0), (leftx,lefty), 75, 0)
	pygame.draw.circle(surface, (0,0,0), (leftx+750-width,lefty), 75, 0)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

if __name__ == "__main__":
    main()
