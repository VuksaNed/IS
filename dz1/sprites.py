import pygame
import os
import config


class BaseSprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, row, col, file_name, transparent_color=None):
        pygame.sprite.Sprite.__init__(self)
        if file_name in BaseSprite.images:
            self.image = BaseSprite.images[file_name]
        else:
            self.image = pygame.image.load(os.path.join(config.IMG_FOLDER, file_name)).convert()
            self.image = pygame.transform.scale(self.image, (config.TILE_SIZE, config.TILE_SIZE))
            BaseSprite.images[file_name] = self.image
        # making the image transparent (if needed)
        if transparent_color:
            self.image.set_colorkey(transparent_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * config.TILE_SIZE, row * config.TILE_SIZE)
        self.row = row
        self.col = col


class Agent(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Agent, self).__init__(row, col, file_name, config.DARK_GREEN)

    def move_towards(self, row, col):
        row = row - self.row
        col = col - self.col
        self.rect.x += col
        self.rect.y += row

    def place_to(self, row, col):
        self.row = row
        self.col = col
        self.rect.x = col * config.TILE_SIZE
        self.rect.y = row * config.TILE_SIZE

    # game_map - list of lists of elements of type Tile
    # goal - (row, col)
    # return value - list of elements of type Tile
    def get_agent_path(self, game_map, goal):
        pass


class ExampleAgent(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        row = self.row
        col = self.col
        while True:
            if row != goal[0]:
                row = row + 1 if row < goal[0] else row - 1
            elif col != goal[1]:
                col = col + 1 if col < goal[1] else col - 1
            else:
                break
            path.append(game_map[row][col])
        return path


class Aki(Agent):

    def get_agent_path(self, game_map, goal):

        visina = len(game_map)
        sirina = len(game_map[0])
        putanja = []
        trenutnicvorovi = [[self.row, self.col]]
        trenutnaputanja = [[[self.row, self.col]]]
        trenutnipath = [[game_map[self.row][self.col]]]

        while True:

            cvor = trenutnicvorovi.pop(0)
            putanja = trenutnaputanja.pop(0)
            path = trenutnipath.pop(0)

            row = cvor[0]
            col = cvor[1]

            if row == goal[0] and col == goal[1]:
                break

            rows = row - 1
            cols = col
            costs = 0
            if rows != -1:
                costs = game_map[rows][cols].cost()
            else:
                costs = -1
            if [rows, cols] in putanja:
                rows = -1
                cols = -1
                costs = -1

            rowi = row
            coli = col + 1
            costi = 0
            if coli != sirina:
                costi = game_map[rowi][coli].cost()
            else:
                costi = -1
            if [rowi, coli] in putanja:
                rowi = -1
                coli = -1
                costi = -1

            rowj = row + 1
            colj = col
            costj = 0
            if rowj != visina:
                costj = game_map[rowj][colj].cost()
            else:
                costj = -1
            if [rowj, colj] in putanja:
                rowj = -1
                colj = -1
                costj = -1

            rowz = row
            colz = col - 1
            costz = 0
            if colz != -1:
                costz = game_map[rowz][colz].cost()
            else:
                costz = -1
            if [rowz, colz] in putanja:
                rowz = -1
                colz = -1
                costz = -1

            maximum = max(costs, costi, costz, costj)

            pomocni = [costs, costi, costz, costj]

            while maximum != -1:
                pomocni = []

                if maximum == costz:
                    trenutnicvorovi.insert(0, [rowz, colz])

                    putanja.append([rowz, colz])
                    trenutnaputanja.insert(0, putanja.copy())
                    putanja.pop()

                    path.append(game_map[rowz][colz])
                    trenutnipath.insert(0, path.copy())
                    path.pop()
                else:
                    if (costz < maximum):
                        pomocni.append(costz)

                if maximum == costj:
                    trenutnicvorovi.insert(0, [rowj, colj])

                    putanja.append([rowj, colj])
                    trenutnaputanja.insert(0, putanja.copy())
                    putanja.pop()

                    path.append(game_map[rowj][colj])
                    trenutnipath.insert(0, path.copy())
                    path.pop()
                else:
                    if (costj < maximum):
                        pomocni.append(costj)

                if maximum == costi:
                    trenutnicvorovi.insert(0, [rowi, coli])

                    putanja.append([rowi, coli])
                    trenutnaputanja.insert(0, putanja.copy())
                    putanja.pop()

                    path.append(game_map[rowi][coli])
                    trenutnipath.insert(0, path.copy())
                    path.pop()
                else:
                    if (costi < maximum):
                        pomocni.append(costi)

                if maximum == costs:
                    trenutnicvorovi.insert(0, [rows, cols])

                    putanja.append([rows, cols])
                    trenutnaputanja.insert(0, putanja.copy())
                    putanja.pop()

                    path.append(game_map[rows][cols])
                    trenutnipath.insert(0, path.copy())
                    path.pop()
                else:
                    if (costs < maximum):
                        pomocni.append(costs)

                if len(pomocni) == 0:
                    maximum = -1
                else:
                    maximum = max(pomocni)

        return path


class Jocke(Agent):

    def srednja_cena(self, row, col, path, game_map):

        visina = len(game_map)
        sirina = len(game_map[0])

        cost = 0
        count = 0
        rows = row - 1
        cols = col
        if rows != -1:
            # if [rows, cols] not in path:
            cost += game_map[rows][cols].cost()
            count += 1

        rowi = row
        coli = col + 1
        if coli != sirina:
            # if [rowi, coli] not in path:
            cost += game_map[rowi][coli].cost()
            count += 1

        rowj = row + 1
        colj = col
        if rowj != visina:
            # if [rowj, colj] not in path:
            cost += game_map[rowj][colj].cost()
            count += 1

        rowz = row
        colz = col - 1
        if colz != -1:
            # if [rowz, colz] not in path:
            cost += game_map[rowz][colz].cost()
            count += 1
        if count == 0:
            return 1001
        else:
            return cost / count

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        visina = len(game_map)
        sirina = len(game_map[0])
        putanja = []
        trenutnicvorovi = [[self.row, self.col]]
        trenutnaputanja = [[[self.row, self.col]]]
        trenutnipath = [[game_map[self.row][self.col]]]

        while True:
            cvor = trenutnicvorovi.pop(0)
            putanja = trenutnaputanja.pop(0)
            path = trenutnipath.pop(0)

            row = cvor[0]
            col = cvor[1]

            if row == goal[0] and col == goal[1]:
                break

            rows = row - 1
            cols = col
            costs = 0
            if rows != -1:
                costs = self.srednja_cena(rows, cols, path, game_map)
            else:
                costs = 1001
            if [rows, cols] in putanja:
                rows = -1
                cols = -1
                costs = 1001

            rowi = row
            coli = col + 1
            costi = 0
            if coli != sirina:
                costi = self.srednja_cena(rowi, coli, path, game_map)
            else:
                costi = 1001
            if [rowi, coli] in putanja:
                rowi = -1
                coli = -1
                costi = 1001

            rowj = row + 1
            colj = col
            costj = 0
            if rowj != visina:
                costj = self.srednja_cena(rowj, colj, path, game_map)
            else:
                costj = 1001
            if [rowj, colj] in putanja:
                rowj = -1
                colj = -1
                costj = 1001

            rowz = row
            colz = col - 1
            costz = 0
            if colz != -1:
                costz = self.srednja_cena(rowz, colz, path, game_map)
            else:
                costz = 1001
            if [rowz, colz] in putanja:
                rowz = -1
                colz = -1
                costz = 1001

            minimum = min(costs, costi, costz, costj)

            pomocni = [costs, costi, costz, costj]

            while minimum != 1001:
                pomocni = []
                if minimum == costs:
                    trenutnicvorovi.append([rows, cols])

                    putanja.append([rows, cols])
                    trenutnaputanja.append(putanja.copy())
                    putanja.pop()

                    path.append(game_map[rows][cols])
                    trenutnipath.append(path.copy())
                    path.pop()
                else:
                    if (costs > minimum):
                        pomocni.append(costs)

                if minimum == costi:
                    trenutnicvorovi.append([rowi, coli])

                    putanja.append([rowi, coli])
                    trenutnaputanja.append(putanja.copy())
                    putanja.pop()

                    path.append(game_map[rowi][coli])
                    trenutnipath.append(path.copy())
                    path.pop()
                else:
                    if (costi > minimum):
                        pomocni.append(costi)

                if minimum == costj:
                    trenutnicvorovi.append([rowj, colj])

                    putanja.append([rowj, colj])
                    trenutnaputanja.append(putanja.copy())
                    putanja.pop()

                    path.append(game_map[rowj][colj])
                    trenutnipath.append(path.copy())
                    path.pop()
                else:
                    if (costj > minimum):
                        pomocni.append(costj)

                if minimum == costz:
                    trenutnicvorovi.append([rowz, colz])

                    putanja.append([rowz, colz])
                    trenutnaputanja.append(putanja.copy())
                    putanja.pop()

                    path.append(game_map[rowz][colz])
                    trenutnipath.append(path.copy())
                    path.pop()
                else:
                    if (costz > minimum):
                        pomocni.append(costz)

                if len(pomocni) == 0:
                    minimum = 1001
                else:
                    minimum = min(pomocni)

        return path


class Draza(Agent):

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        visina = len(game_map)
        sirina = len(game_map[0])
        putanja = []
        trenutnicvorovi = [[self.row, self.col, game_map[self.row][self.col].cost(), [[self.row, self.col]],
                            [game_map[self.row][self.col]]]]

        while True:
            cvor = trenutnicvorovi.pop(0)

            row = cvor[0]
            col = cvor[1]
            cost = cvor[2]
            putanja = cvor[3]
            path = cvor[4]

            if row == goal[0] and col == goal[1]:
                break

            rows = row - 1
            cols = col
            costs = 0
            if rows != -1:
                costs = cost + game_map[rows][cols].cost()
            else:
                costs = -1
            if [rows, cols] in putanja:
                rows = -1
                cols = -1
                costs = -1

            rowi = row
            coli = col + 1
            costi = 0
            if coli != sirina:
                costi = cost + game_map[rowi][coli].cost()
            else:
                costi = -1
            if [rowi, coli] in putanja:
                rowi = -1
                coli = -1
                costi = -1

            rowj = row + 1
            colj = col
            costj = 0
            if rowj != visina:
                costj = cost + game_map[rowj][colj].cost()
            else:
                costj = -1
            if [rowj, colj] in putanja:
                rowj = -1
                colj = -1
                costj = -1

            rowz = row
            colz = col - 1
            costz = 0
            if colz != -1:
                costz = cost + game_map[rowz][colz].cost()
            else:
                costz = -1
            if [rowz, colz] in putanja:
                rowz = -1
                colz = -1
                costz = -1

            if costs != -1:
                path.append(game_map[rows][cols])
                putanja.append([rows, cols])

                trenutnicvorovi.append([rows, cols, costs, putanja.copy(), path.copy()])

                putanja.pop()
                path.pop()

            if costi != -1:
                path.append(game_map[rowi][coli])
                putanja.append([rowi, coli])

                trenutnicvorovi.append([rowi, coli, costi, putanja.copy(), path.copy()])

                putanja.pop()
                path.pop()

            if costj != -1:
                path.append(game_map[rowj][colj])
                putanja.append([rowj, colj])

                trenutnicvorovi.append([rowj, colj, costj, putanja.copy(), path.copy()])

                putanja.pop()
                path.pop()

            if costz != -1:
                path.append(game_map[rowz][colz])
                putanja.append([rowz, colz])

                trenutnicvorovi.append([rowz, colz, costz, putanja.copy(), path.copy()])

                putanja.pop()
                path.pop()

            sorter = lambda x: (x[2], len(x[4]))
            trenutnicvorovi.sort(key=sorter)

        return path


class Bole(Agent):

    def dohvati_heuristiku(self, game_map, goal, row, col):
        cost = 0
        colr = abs(goal[1] - col)
        rowr = abs(goal[0] - row)
        cost = (colr + rowr) * game_map[row][col].cost()

        return cost

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        visina = len(game_map)
        sirina = len(game_map[0])
        putanja = []
        trenutnicvorovi = [[self.row, self.col, game_map[self.row][self.col].cost(), [[self.row, self.col]],
                            [game_map[self.row][self.col]]]]

        while True:
            cvor = trenutnicvorovi.pop(0)

            row = cvor[0]
            col = cvor[1]
            cost = cvor[2] - self.dohvati_heuristiku(game_map, goal, row, col)
            putanja = cvor[3]
            path = cvor[4]

            if row == goal[0] and col == goal[1]:
                break

            rows = row - 1
            cols = col
            costs = 0
            if rows != -1:
                costs = cost + game_map[rows][cols].cost() + self.dohvati_heuristiku(game_map, goal, rows, cols)
            else:
                costs = -1
            if [rows, cols] in putanja:
                rows = -1
                cols = -1
                costs = -1

            rowi = row
            coli = col + 1
            costi = 0
            if coli != sirina:
                costi = cost + game_map[rowi][coli].cost() + self.dohvati_heuristiku(game_map, goal, rowi, coli)
            else:
                costi = -1
            if [rowi, coli] in putanja:
                rowi = -1
                coli = -1
                costi = -1

            rowj = row + 1
            colj = col
            costj = 0
            if rowj != visina:
                costj = cost + game_map[rowj][colj].cost() + self.dohvati_heuristiku(game_map, goal, rowj, colj)
            else:
                costj = -1
            if [rowj, colj] in putanja:
                rowj = -1
                colj = -1
                costj = -1

            rowz = row
            colz = col - 1
            costz = 0
            if colz != -1:
                costz = cost + game_map[rowz][colz].cost() + self.dohvati_heuristiku(game_map, goal, rowz, colz)
            else:
                costz = -1
            if [rowz, colz] in putanja:
                rowz = -1
                colz = -1
                costz = -1

            if costs != -1:
                path.append(game_map[rows][cols])
                putanja.append([rows, cols])

                trenutnicvorovi.append([rows, cols, costs, putanja.copy(), path.copy()])

                putanja.pop()
                path.pop()

            if costi != -1:
                path.append(game_map[rowi][coli])
                putanja.append([rowi, coli])

                trenutnicvorovi.append([rowi, coli, costi, putanja.copy(), path.copy()])

                putanja.pop()
                path.pop()

            if costj != -1:
                path.append(game_map[rowj][colj])
                putanja.append([rowj, colj])

                trenutnicvorovi.append([rowj, colj, costj, putanja.copy(), path.copy()])

                putanja.pop()
                path.pop()

            if costz != -1:
                path.append(game_map[rowz][colz])
                putanja.append([rowz, colz])

                trenutnicvorovi.append([rowz, colz, costz, putanja.copy(), path.copy()])

                putanja.pop()
                path.pop()

            sorter = lambda x: (x[2], len(x[4]))
            trenutnicvorovi.sort(key=sorter)

        return path


class Tile(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Tile, self).__init__(row, col, file_name)

    def position(self):
        return self.row, self.col

    def cost(self):
        pass

    def kind(self):
        pass


class Stone(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'stone.png')

    def cost(self):
        return 1000

    def kind(self):
        return 's'


class Water(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'water.png')

    def cost(self):
        return 500

    def kind(self):
        return 'w'


class Road(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'road.png')

    def cost(self):
        return 2

    def kind(self):
        return 'r'


class Grass(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'grass.png')

    def cost(self):
        return 3

    def kind(self):
        return 'g'


class Mud(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'mud.png')

    def cost(self):
        return 5

    def kind(self):
        return 'm'


class Dune(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'dune.png')

    def cost(self):
        return 7

    def kind(self):
        return 's'


class Goal(BaseSprite):
    def __init__(self, row, col):
        super().__init__(row, col, 'x.png', config.DARK_GREEN)


class Trail(BaseSprite):
    def __init__(self, row, col, num):
        super().__init__(row, col, 'trail.png', config.DARK_GREEN)
        self.num = num

    def draw(self, screen):
        text = config.GAME_FONT.render(f'{self.num}', True, config.WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
