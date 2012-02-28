from commands import add, admin, get_player, alias
from pyspades.server import input_data
from twisted.internet import reactor
from pyspades import contained as loaders

FUEL_CAP = 60.0

def jump_cycle(player, interval=0.05):
    if not player.world_object or not player.armed or not player.flying or player.fuel <=0:
        return
    world_object = player.world_object
    ##if world_object.acceleration.z == 0.0 and player.fuel > 0:
    world_object.jump = True
    input_data.player_id = player.player_id
    input_data.up = world_object.up
    input_data.down = world_object.down
    input_data.left = world_object.left
    input_data.right = world_object.right
    input_data.fire = world_object.fire
    input_data.jump = True
    input_data.crouch = world_object.crouch
    input_data.aim = world_object.aim
    player.protocol.send_contained(input_data)
    player.fuel -= 1
    #end indent
    if world_object.position.z > 0.0:
        reactor.callLater(interval, jump_cycle, player)
    else:
        player.flying = False

def charge_cycle(player, interval=0.10):
    if not player.world_object or player.flying or player.fuel >= FUEL_CAP:
        return
    player.fuel += 0.5
    if player.fuel == FUEL_CAP:
        print "fuel now full"
        player.send_chat('Your fuel is now fully charged.')
    reactor.callLater(interval, charge_cycle, player)


@alias('j')
def jetpack(player):
    if player.armed == True:
        player.armed = False
    else:
        player.armed = True
    on_off = ['OFF', 'ON'][int(player.armed)]
    return "Jetpack is now turned %s" % on_off
    #pos = player.world_object.position
    #z = player.protocol.map.get_z(pos.x, pos.y)
add(jetpack)


def apply_script(protocol, connection, config):
    class JetConnection(connection):
        armed = False
        flying = False
        fuel = FUEL_CAP
    
        def on_spawn(self, pos):
            self.fuel = FUEL_CAP
            return connection.on_spawn(self, pos)

        def on_animation_update(self, fire, jump, crouch, aim):
            if crouch == True:
                if self.armed == True and self.flying == False:
                    self.flying = True
                    jump_cycle(self)
            else:
                if self.flying == True:
                    self.flying = False
                    charge_cycle(self)
            
            if self.fuel < 0:
                self.send_chat('You are out of fuel! Wait for it to recharge.')
            return connection.on_animation_update(self, fire, jump, crouch, aim)

    return protocol, JetConnection