import convokit

# path of the folder storing the lexicons files "my_certain.txt", "my_geo.txt"
# "my_hedges.txt", "my_meta.txt"
path = 'D:/lexicons'

# Create instance of Constructive class
A = convokit.Constructive(path)

# Turn Features Test
A.turn_test()

# Message Features Test
A.msg_test()
