

# 

def test(iterx):
	for x in iterx:
		yield(x)


x = [1, 2, 3, 4]
y = test(x)


print([x for x in y])