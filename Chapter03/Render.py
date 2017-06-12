#!/usr/bin/env python

import pygame
from pygame.locals import *
from sys import exit

pygame.init()

# 15 * 40 = 600, 10 * 40 = 400
block_size = 40
screen = pygame.display.set_mode((600, 400), 0, 32)
color_roadblock = [255, 255, 255]
color_blank     = [0, 0, 0]
color_path      = [0, 0, 255]
color_start     = [255, 0, 0]
color_end       = [0, 255, 0]

BobsMap = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
[8, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1],
[1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1],
[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1],
[1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 5],
[1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# pos = (x, y), top left position of the rect
def set_block(screen, color, pos):
	top_side_rect   = Rect(pos[0], pos[1], block_size, 1)
	right_side_rect = Rect(pos[0] + block_size, pos[1], 1, block_size)
	bottom_side_rect= Rect(pos[0], pos[1] + block_size, block_size, 1)
	left_side_rect  = Rect(pos[0], pos[1], 1, block_size)
	center_rect     = Rect(pos[0]+1, pos[1]+1, block_size-1, block_size-1)
	pygame.draw.rect(screen, (255, 255, 255), top_side_rect)
	pygame.draw.rect(screen, (255, 255, 255), right_side_rect)
	pygame.draw.rect(screen, (255, 255, 255), bottom_side_rect)
	pygame.draw.rect(screen, (255, 255, 255), left_side_rect)
	pygame.draw.rect(screen, color, center_rect)
def flush_map(screen, map):
	return

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

	screen.fill((255, 255, 255))

	#set_block(screen, (255,0,0), (100, 100))
	for yIdx, rowItem in enumerate(BobsMap):
		for xIdx, blockItem in enumerate(rowItem):
			if blockItem == 1:
				block_pos = (xIdx*block_size, yIdx*block_size)
				set_block(screen, (0, 0, 0), block_pos)
			elif blockItem == 5:
				block_pos = (xIdx*block_size, yIdx*block_size)
				set_block(screen, (255, 0, 0), block_pos)
			elif blockItem == 8:
				block_pos = (xIdx*block_size, yIdx*block_size)
				set_block(screen, (0, 255, 0), block_pos)
			
	pygame.display.update()