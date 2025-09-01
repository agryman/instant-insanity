from PIL import Image
img = Image.open('notebooks/images/scenes/introduction/winning-moves-instant-insanity-cubes_transparent.png')
print('Mode:', img.mode)
print('Has alpha:', img.mode == 'RGBA')
alpha = img.getchannel('A')
print('Min alpha:', alpha.getextrema()[0])
print('Max alpha:', alpha.getextrema()[1])
