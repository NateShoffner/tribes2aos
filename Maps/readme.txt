----------------------------------------
--Ace of Spades bitmap converters v1.1--
----------------------------------------

==Legal stuff==

Blah blah not my fault, blah blah don't copy and claim as own. -bildramer


==Instructions==

To convert a 512x512 bitmap into a flat map, type "convert.exe <filename> <height>" in a console or use a batch file.
For example:

convert.exe moon.bmp 5

A map with a height of 0 will only have water, so using 0 is not recommended.


To convert a 512x512 bitmap and a 512x512 heightmap into a map, type "converth.exe <filename> <heightmapfilename>" in a console or use a batch file (edit example.bat for an example).

Note that only 24-bit .bmps will work.


==Changelog==

20.05.2011 - version 1.1
-Bitmap loading now uses SDL to avoid nasty glitches
-Fixed bug where black in heightmap skips the entire column

14.05.2011 - version 1.0
-Released