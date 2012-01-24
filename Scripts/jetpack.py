from commands import add, admin, get_player
from pyspades.server import input_data
from twisted.internet import reactor
from pyspades import contained as loaders

FUEL_CAP = 60.0

def jump_cycle(player, interval=0.05):
    print "jump cycle start"
    if not player.world_object or not player.armed or not player.flying or player.fuel <=0:
        return
    print "made jump cycle first check"
    world_object = player.world_object
    ##if world_object.acceleration.z == 0.0 and player.fuel > 0:
    print "jumping!"
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
        print "not jumping"
        reactor.callLater(interval, jump_cycle, player)
    else:
        print "done jumping"
        player.flying = False

def charge_cycle(player, interval=0.10):
    print "charge cycle start"
    if not player.world_object or player.flying or player.fuel >= FUEL_CAP:
        return
    print "made charge cycle first check"
    player.fuel += 0.5
    reactor.callLater(interval, charge_cycle, player)



def jetpack(player):
    print "jetpack, start"
    player.armed = True
    #pos = player.world_object.position
    #z = player.protocol.map.get_z(pos.x, pos.y)
add(jetpack)


def apply_script(protocol, connection, config):
    class JetConnection(connection):
        armed = False
        flying = False
        fuel = 100
    
        def on_animation_update(self, fire, jump, crouch, aim):
            if crouch == True:
                print "anim update: jump true"
                if self.armed == True and self.flying == False:
                    print "anim update: turn on flying"
                    self.flying = True
                    jump_cycle(self)
            else:
                if self.flying == True:
                    print "anim update: stop flying"
                    self.flying = False
                    charge_cycle(self)
            
            return connection.on_animation_update(self, fire, jump, crouch, aim)

    return protocol, JetConnection