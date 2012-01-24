from commands import add, admin, get_player

@name('satchelset')
@alias('s')
def satchel_set(connection, var=None):
    #if has grenades, set charge_armed to true
add(badmin)

def apply_script(protocol, connection, config):
    class SatchelConnection(connection):
        charge_armed = None
        
        def on_block_build(self, x, y, z):
            if self.protocol.charged is None:
                self.protocol.charged = {}
            self.protocol.charged[(x, y, z)] = (self.name, self.team.id)
            connection.on_block_build(self, x, y, z)
        
        def on_block_removed(self, x, y, z):
            if self.protocol.block_info is None:
                self.protocol.block_info = {}
            if self.blocks_removed is None:
                self.blocks_removed = []
            pos = (x, y, z)
            info = (reactor.seconds(),
                self.protocol.block_info.pop(pos, None))
            self.blocks_removed.append(info)
            connection.on_block_removed(self, x, y, z)
    
    class SatchelProtocol(protocol):
        charged = None
        
        def on_map_change(self, map):
            self.block_info = None
            return protocol.on_map_change(self, map)
    
    return SatchelProtocol, SatchelConnection