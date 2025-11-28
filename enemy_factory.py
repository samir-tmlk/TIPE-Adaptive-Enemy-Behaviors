# enemy_factory.py

import random
from enemy import EnemyLevel1, EnemyLevel2, EnemyLevel3
from settings import width, height

class EnemyFactory:
    def __init__(self, difficulty_manager, base_count=3):
        self.dm          = difficulty_manager
        self.base_count  = base_count

    def create_enemies(self):
        level = self.dm.get_level()
        enemies = []
        for i in range(self.base_count):
            if level == 1:
                e = EnemyLevel1()
            elif level == 2:
                e = EnemyLevel2()
            else:
                # calcule tes paramètres pour Level3
                health = 50  + (level-1)*10 + random.randint(-5,5)
                damage = 5   + (level-1)*2  + random.randint(-1,1)
                speed  = 2.0 + (level-1)*0.2 + random.uniform(-0.2,0.2)
                x = random.randint(50, width-100)
                y = random.randint(50, height-100)
                e = EnemyLevel3(health=health, damage=damage, speed=speed, x=x, y=y)
            enemies.append(e)
        return enemies
