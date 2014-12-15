#game_topfile.py

import pyglet
from pyglet.window import key
from game import viewport,world,avatar,hud,enemy,pacer,token,spawn_tokens,monkey,key_and_door,coconuts,tile,collidable, background,instructions

ouch_sound=pyglet.media.load('./sounds/ouch.wav',streaming=False)
applause_sound=pyglet.media.load('./sounds/app-34.wav',streaming=False)
bell_sound=pyglet.media.load('./sounds/bell.wav',streaming=False)
song_sound=pyglet.media.load('./sounds/game.wav',streaming=True)

def init():

    global inst
    
    inst=instructions.Instructions_display()
    inst.batch=inst_batch
    viewport.window.push_handlers(inst.key_handler)
    pyglet.clock.schedule_interval(inst.update,1/120.0)

def check_instructions(dt):
    if inst.complete:
        pyglet.clock.unschedule(inst.update)
        pyglet.clock.unschedule(check_instructions)
        start_game()

def update(dt):
    global player_lives, death_delay, losing_screen,score,song,ruby

    death_delay-=dt

    player_dead=False
    victory=False
    
    for i in xrange(len(game_objects)):
  
        obj=game_objects[i]
        
        #make sure objects are not dead
        if not obj.dead:
            if player.collides_with(obj) or obj.collides_with(player):
                player.handle_collision_with(obj)
                obj.handle_collision_with(player)

                if isinstance(obj,coconuts.Coconut):
                    ouch_sound.play()
                    if death_delay<=0:
                        player_lives-=1
                        hud.Lives_label.text='Lives:%i'%player_lives
                        death_delay=0.5
                        player.x=0
                        player.y=75

                if isinstance(obj,pacer.Pacer):
                    ouch_sound.play()
                    if death_delay<=0:
                        player_lives-=3
                        if player_lives<0:
                            player_lives=0
                        hud.Lives_label.text='Lives:%i'%player_lives
                        death_delay=0.5
                        player.x=0
                        player.y=75
                        
                if isinstance(obj,enemy.Enemy):
                   
                    if death_delay<=0:
                        ouch_sound.play()
                        player_lives-=1
                        hud.Lives_label.text='Lives:%i'%player_lives
                        death_delay=0.5
                        player.x=0
                        player.y=75

                if isinstance(obj,key_and_door.Key):
                    bell_sound.play()
                        
                if isinstance(obj,key_and_door.Door):
                    bell_sound.play()
                    if player.met_goal:
                        applause_sound.play()
                        minute_timer=0
                        hud.Time_label.text="Time:"+str(int(minute_timer))
                        hud.Win_label.y=viewport.v_ctr+40
                        pyglet.clock.unschedule(update)
                        
    player.update(dt)
    
    for obj in game_objects:
        obj.update(dt)
        
    if death_delay<=0:
        if player.y<=50:
            player_lives-=1
            hud.Lives_label.text='Lives:%i'%player_lives
            death_delay=0.5

    if player_lives==0:
        losing_screen.y=0
       # if minute_timer>60:
        pyglet.clock.unschedule(update_main_clock)

    #get rid of dead objects

    for to_remove in [obj for obj in game_objects if obj.dead]:
        to_remove.delete()
        game_objects.remove(to_remove)
        
        #rubies, if avatar gets 3 rubies, gets one life
        if isinstance(to_remove,token.Token):
            bell_sound.play()
            score+=10
            hud.Score_label.text='Score:'+str(score)
            ruby+=1
            hud.Rubies_label.text='Rubies:'+str(ruby)
            if ruby==3:
                player_lives+=1
                hud.Lives_label.text='Lives:%i'%player_lives
                ruby=0
                hud.Rubies_label.text='Rubies:'+str(ruby)

def set_level(num_lives):
    global player,player_lives,game_objects,event_stack_size
    global level,max_tokens,tokens_spawned,tokens_collected,max_power_ups,power_ups_spawned

    max_tokens=2+level*3
    tokens_remaining_label.text='Tokens Remaining:'+str(max_notes)
    tokens_spawned=0
    tokens_collected=0

    max_power_ups=level
    power_ups_spawned=0

    #clear the event stack of any remaining handlers from other levels

    while event_stack_size>0:
        viewport.window.pop_handlers()
        event_stack_size-=1

    for life in player_lives:
        life.delete()

    #initialize the avatar sprite

    player=avatar.Avatar(x=viewport.window.width//2,y=viewport.window.height//2,batch=main_batch)

    #create player life icons

    #player_lives=load_player_lives(num_lives,main_batch)

    #create hazards for level

    enemies=load_enemies(player.x, player.y, main_batch)

    #store all objects that update each frame in a list

    game_objects=[player]+enemies

    #add any specified event handlers to the event handler stack

    for obj in game_objects:
        for handler in obj.event_handlers:
            game_window.push_handlers(handler)
            event_stack_size+=1

def update_main_clock(dt):

    global minute_timer

    minute_timer+=dt
    hud.Time_label.text="Time:"+str(int(minute_timer))

minute_timer=0.0

def start_game():

    global game_objects,pacer,coconut,gorilla,hanging_monkey,losing_screen,background
    global hanging_monkey2,rubies,door,key,player,player_lives

    game_objects=[]

    world.generate_world()

    player=avatar.Avatar(batch=main_batch)
    player.affected_by_gravity=True
    player.update_bounding_box()

    player_lives=3
    losing_screen=hud.Losing_screen()

    gorilla=enemy.Enemy(batch=main_batch)
    gorilla.affected_by_gravity=True
    game_objects.append(gorilla)
    gorilla.update_bounding_box()

    hanging_monkey=monkey.Monkey(batch=main_batch)
    game_objects.append(hanging_monkey)
    hanging_monkey.update_bounding_box()

    hanging_monkey2=monkey.Monkey(batch=main_batch)
    game_objects.append(hanging_monkey2)
    hanging_monkey2.x=700
    hanging_monkey2.y=560
    hanging_monkey2.update_bounding_box()

    chucknorris=pacer.Pacer(batch=main_batch)
    game_objects.append(chucknorris)
    chucknorris.update_bounding_box()

    coconut=coconuts.Coconut(batch=main_batch)
    coconut.x=700
    coconut.y=540
    game_objects.append(coconut)
    coconut.update_bounding_box()

    coconut2=coconuts.Coconut(batch=main_batch)
    coconut2.x=375
    coconut2.y=540
    game_objects.append(coconut2)
    coconut2.update_bounding_box()

    rubies=spawn_tokens.spawn_tokens(7)
    for ruby in rubies:
        ruby.batch=main_batch
    game_objects.extend(rubies)

    door=key_and_door.Door(batch=main_batch)
    door.affected_by_gravity=False
    game_objects.append(door)
    door.update_bounding_box()

    key=key_and_door.Key(batch=main_batch)
    key.affected_by_gravity=False
    game_objects.append(key)
    key.update_bounding_box()

    background=background.Background()

    song_sound.play()

    viewport.window.push_handlers(player.key_handler)
    pyglet.clock.schedule_interval(update,1.0/120.0)
    pyglet.clock.schedule_interval(update_main_clock,1.0)

@viewport.window.event
def on_draw():
    viewport.window.clear()
    
    if not inst.complete:
        inst_batch.draw()
    else:
        background.draw()
        world.tile_batch.draw()
    
    main_batch.draw()
    
    hud.hud_batch.draw()

@viewport.window.event
def on_close():
    viewport.window.close()
    quit()

if __name__=='__main__':

    pyglet.gl.glClearColor(0.0,0.24,0.0,1.0)
    main_batch=pyglet.graphics.Batch()
    inst_batch=pyglet.graphics.Batch()
    game_objects=[]
    death_delay=0
    score=0
    ruby=0

    init()

    pyglet.clock.schedule_interval(check_instructions,1/120.0)

    pyglet.app.run()


