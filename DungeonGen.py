from random import randint
# 10 x 10 array of dungeon

def genFloor(width, height, minRooms, maxRooms):
    mapArray = []
    for y in range(0, height):
        mapArray.append([])
        for x in range(0, width):
            mapArray[y].append('o')
    start = [randint(0, width-1), randint(0, height-1)]
    mapArray[start[0]][start[1]] = 'x'
    rooms = 0
    for y in range(0, height):
        for x in range(0, width):
            if y - 1 > -1 and mapArray[y - 1][x] == 'x':
                if randint(0, 1) == 0 and rooms < maxRooms:
                    mapArray[y][x] = 'x'
                    rooms += 1
                elif rooms < minRooms:
                    mapArray[y][x] = 'x'
                    rooms += 1
            if y + 1 < height and mapArray[y + 1][x] == 'x':
                if randint(0, 1) == 0 and rooms < maxRooms:
                    mapArray[y][x] = 'x'
                    rooms += 1
                elif rooms < minRooms:
                    mapArray[y][x] = 'x'
                    rooms += 1
            if x - 1 > -1 and mapArray[y][x-1] == 'x':
                if randint(0, 2) == 0 and rooms < maxRooms:
                    mapArray[y][x] = 'x'
                    rooms += 1
                elif rooms < minRooms:
                    mapArray[y][x] = 'x'
                    rooms += 1
            if x + 1 < width and mapArray[y][x+1] == 'x':
                if randint(0, 2) == 0 and rooms < maxRooms:
                    mapArray[y][x] = 'x'
                    rooms += 1
                elif rooms < minRooms:
                    mapArray[y][x] = 'x'
                    rooms += 1
    return [start, mapArray]

mapArray = genFloor(20, 20, 20, 100)
for i in mapArray[1]:
    print(i)
