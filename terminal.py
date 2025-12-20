import pyte

screen = pyte.Screen(80,200)
stream = pyte.Stream(screen)
stream.feed(b"heloworod")
screen.display