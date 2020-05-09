#kennex

import pygame, time
import gf
#import pygame.font
import puzzles
import multiline_text as mt
import random
from settings import Settings
import inventory
import check_steam
#import tv_channels

i_enlarged_remote = 'images/remote_enlarged.png'
i_big_shirt = 'images/shirt_no_hang.png'
i_enlarged_papers_top1 = 'images/papers_1top.png'
i_enlarged_papers_top2 = 'images/papers_2top.png'
i_enlarged_papers_top3 = 'images/papers_3top.png'

enlarged_remote = pygame.image.load(i_enlarged_remote)
enlarged_shirt = pygame.image.load(i_big_shirt)
enlarged_papers_top1 = pygame.image.load(i_enlarged_papers_top1)
enlarged_papers_top2 = pygame.image.load(i_enlarged_papers_top2)
enlarged_papers_top3 = pygame.image.load(i_enlarged_papers_top3)

# Scaled Images
red_key_scaled = pygame.transform.smoothscale(inventory.red_key_taped, ((inventory.red_key_taped.get_width() // 3), (inventory.red_key_taped.get_height() // 3)))
ripped_tape_scaled = pygame.transform.smoothscale(inventory.ripped_tape, ((inventory.red_key_taped.get_width() // 3) // 2, (inventory.red_key_taped.get_height() // 3)))

# Load Sounds
key_sound = pygame.mixer.Sound('sounds/key_jingle.wav')
flip_page_sound = pygame.mixer.Sound('sounds/flip_page.wav')
safe_init_sound = pygame.mixer.Sound('sounds/safe_init.wav')
message_sound = pygame.mixer.Sound('sounds/message.wav')

pygame.font.init()


class Stable_Items():
    """Class to store all of the information regarding the camera and chair manuals"""
    def __init__(self, gs, screen):
        self.gs = gs
        self.screen = screen



        self.number_index_dict = {'4': 1,
                                  '5': 2,
                                  '6': 3,
                                  '7': 4,
                                  '8': 5,
                                  '9': 6,
                                  '10': 7,
                                  '11': 8,
                                  '12': 9,
                                  '13': 0,
                                  '15': 'F',
                                  '22': 'U',
                                  '23': 'R',
                                  '24': 'D',
                                  '25': 'L'}

        # Shirt Settings
        self.shirt_rect = enlarged_shirt.get_rect(center = screen.get_rect().center)

        if gs.screen_width == 1200:
            self.clickbox_shirt_pocket = [(537, 280), (570, 288), (566, 322), (536, 314)]
        elif gs.screen_width == 1440:
            self.clickbox_shirt_pocket = [(658, 362), (689, 367), (685, 402), (655, 394)]

        # Drawer Settings
        self.sdx = screen.get_rect().centerx
        self.sdy = screen.get_rect().centery
        self.scaled_drawer = gf.aspect_scale(inventory.sur_inv_desk_drawer, 400)
        self.drawer_rect = self.scaled_drawer.get_rect(center = screen.get_rect().center)

        # Book / Manual Settings
        self.red_key_clickbox = [(637, 546), (655, 531), (666, 448), (680, 411), (661, 377),
                                (635, 371), (595, 395), (598, 437), (611, 479), (616, 527), (637, 548)]

        self.manual_view_cover = pygame.Rect(410, 130, 450, 525)
        # Define the cover shapes.  These will be clickable to turn the pages
        self.bc_x = 160  # Back Cover X
        self.bc_tc_y = 58  # Back Cover, Top Corner Y
        self.bc_bc_y = 727  # Back Cover, Top Corner Y
        self.back_cover = [self.manual_view_cover.topleft, (self.bc_x, self.bc_tc_y), (self.bc_x, self.bc_bc_y), self.manual_view_cover.bottomleft]

        self.manual_pages = self.manual_view_cover.inflate(-10, -10)
        self.manual_pages = self.manual_pages.move(-5, 0)
        # Page Area for Page Content
        self.page_area = self.manual_pages.inflate(-50, -50)


        # Remote Settings
        self.remote_rect = enlarged_remote.get_rect()
        self.remote_rect.x += 750
        self.remote_rect.y += 195

        # Remote Click Box List
        self.remote_square_buttons_clickbox = [
                                        [(784, 370), (812, 370), (812, 392), (784, 392)], # Volume Up // 0
                                        [(784, 415), (812, 415), (812, 437), (784, 437)], # Volume Down // 1
                                        [(872, 370), (900, 370), (900, 392), (872, 392)], # Channel Up // 2
                                        [(872, 416), (900, 416), (900, 437), (872, 437)], # Channel Down // 3

                                        [(784, 473), (813, 473), (812, 490), (784, 490)], # 1 Button // 4
                                        [(827, 473), (856, 473), (856, 490), (827, 490)], # 2 Button // 5
                                        [(870, 473), (900, 473), (900, 490), (870, 490)], # 3 Button // 6

                                        [(784, 510), (813, 510), (812, 530), (784, 530)], # 4 Button // 7
                                        [(827, 510), (856, 510), (856, 530), (827, 530)], # 5 Button // 8
                                        [(870, 510), (900, 510), (900, 530), (870, 530)], # 6 Button // 9

                                        [(784, 549), (813, 549), (812, 569), (784, 569)], # 7 Button // 10
                                        [(827, 549), (856, 549), (856, 569), (827, 569)], # 8 Button // 11
                                        [(870, 549), (900, 549), (900, 569), (870, 569)], # 9 Button // 12

                                        [(827, 589), (856, 589), (856, 607), (827, 607)], # 0 Button // 13
                                        [(784, 589), (813, 589), (812, 607), (784, 607)], # L Button // 14
                                        [(870, 589), (900, 589), (900, 607), (870, 607)], # F Button // 15

                                        [(782, 641), (805, 641), (805, 655), (782, 655)], # Rewind // 16
                                        [(815, 641), (837, 641), (837, 655), (815, 655)], # Play // 17
                                        [(847, 641), (868, 641), (868, 655), (847, 655)], # Pause // 18
                                        [(878, 641), (902, 641), (902, 655), (878, 655)], # Fast Forward // 19

                                        [(782, 220), (812, 220), (812, 240), (782, 240)], # Mute // 20

                                        [(823, 290), (840, 283), (858, 291), (865, 307), (860, 326), (842, 333), (823, 325), (816, 307)], # Central Play // 21
                                        [(823, 290), (840, 283), (859, 291), (877, 271), (860, 260), (840, 255), (821, 260), (804, 270)], # Top Arrow // 22
                                        [(859, 291), (879, 272), (889, 286), (893, 307), (890, 323), (879, 344), (860, 325), (867, 306)], # Right Arrow // 23
                                        [(822, 327), (840, 334), (857, 328), (876, 343), (859, 356), (841, 361), (821, 355), (804, 346)], # Bottom Arrow // 24
                                        [(803, 272), (823, 290), (815, 307), (822, 327), (804, 344), (789, 323), (789, 309), (793, 285)], # Left Arrow // 25

                                        [(899, 218), (910, 221), (914, 231), (908, 241), (900, 245), (888, 239), (887, 229), (890, 221)] # Power Button // 26
                                        ]

        # Papers Click Boxes
        if gs.screen_width == 1200:
            self.papers_page1_list = [(427, 49), (841, 121), (740, 681), (327, 607)]
            self.papers_page2_list = [(322, 68), (743, 68), (743, 642), (322, 642)]
            self.papers_page3_list = [(217, 110), (629, 37), (729, 596), (315, 673)]

        else:
            self.papers_page1_list = [(536, 125), (938, 198), (838, 748), (436, 675)]
            self.papers_page2_list = [(431, 148), (839, 148), (842, 706), (432, 708)]
            self.papers_page3_list = [(327, 189), (729, 117), (827, 664), (426, 736)]


    def book_page_content(self, gs, screen, page, page_area):
        if gs.current_book == 'red_book':
            # Page 1
            if page == 1:
                gs.text = None
                channels = ['', # todo update channels accordingly
                        'Press Button on Remote',
                        'To go to a Channel',
                        '',
                        '1... Brought To You By...',
                        '2... Music and Sounds By...',
                        '3... Default',
                        '4... Camera 1',
                        '5... Camera 2',
                        '6... Camera 3',
                        '7... ???',
                        '8... Nothing',
                        '9...',
                        '',
                        'There are others!',
                        'Just hit Central Play!']
                line_spacing = 200
                text_height = gs.verdana18.get_height()

                heading_image = gs.cambria30.render('CHANNELS', True, gs.black)
                screen.blit(heading_image, ((self.page_area.centerx-(heading_image.get_width()/2)), (line_spacing-25)))

                for channel in channels:
                    text_image = gs.verdana18.render(channel, True, gs.black)
                    screen.blit(text_image, (465, line_spacing+35))
                    line_spacing += text_height

            # Page 2
            if page == 2:
                instructions = ['',
                                '-The TV can be turned on or off',
                                '   when you point the remote at it.',
                                '-Batteries are required for the',
                                '   remote to work. (Sold separately)',
                                '-Use the channel buttons to',
                                '   change the channel.',
                                '-You can also enter in channels,',
                                '   but must press the central',
                                '   play button afterward.',
                                '-Some channels may start with 0.**',
                                '-Enjoy your TV!'
                                ]
                line_spacing = 200
                text_height = gs.verdana18.get_height()

                heading_image = gs.cambria30.render('TELEVISION', True, gs.black)
                screen.blit(heading_image, ((self.page_area.centerx-(heading_image.get_width()/2)), (line_spacing-25)))

                for instruction in instructions:
                    text_image = gs.verdana18.render(instruction, True, gs.black)
                    screen.blit(text_image, (460, line_spacing+35))
                    line_spacing += text_height

            # Page 3
            if page == 3:
                instructions = ['',
                                '-Cameras can be viewed by going',
                                '   to the proper camera channel.',
                                '-Cameras must be powered by a',
                                '   power cord. (Sold Separately)',
                                '-Cameras are live action only.',
                                '-They are not recording.',
                                '-Enjoy your cameras!'
                                ]
                line_spacing = 200
                text_height = gs.verdana18.get_height()

                heading_image = gs.cambria30.render('CAMERAS', True, gs.black)
                screen.blit(heading_image, ((self.page_area.centerx-(heading_image.get_width()/2)), (line_spacing-25)))

                for instruction in instructions:
                    text_image = gs.verdana18.render(instruction, True, gs.black)
                    screen.blit(text_image, (460, line_spacing+35))
                    line_spacing += text_height
            # Page 4
            if page == 4:
                #surface = pygame.Surface((100,100))

                text_image = gs.cambria18.render('closets hold secrets', True, gs.gray)
                screen.blit(text_image, (655, 170))

                if not gs.red_key_found:
                    screen.blit(red_key_scaled, (540, 380))
                    # pygame.draw.polygon(screen, gs.yellow, self.red_key_clickbox, 1) # todo comment this out
                else:
                    screen.blit(ripped_tape_scaled, (540, 380))

        elif gs.current_book == 'blue_book':
            if page == 1:
                gs.text = 'An interesting diary...'
                # Page 1 - Pages to a diary
                if gs.diary_choice == 1:
                    diary = "I'm not sure how long I've been in this room. I'm not sure how long I've been in this room. I'm not sure how long I've been in this room. I'm not sure how long I've been in this room. I'm not sure how long I've been in this room. I'm not sure how long I've been in this room. I'm not sure how long I've been in this room. I'm not sure how long I've been in this room."
                    diary = mt.multiline_text(diary, 210, gs.cambria22)
                    text_height = gs.cambria22.get_height()

                    line_spacing = 200

                    for line in diary:
                        text_image = gs.cambria22.render(line, True, gs.black)
                        screen.blit(text_image, (465, line_spacing))
                        line_spacing += text_height

                elif gs.diary_choice == 2:
                    diary = "Once you've seen darkness, you probably don't see light.  But a good way to look into the future, is to see it with open eyes.  If you ever feel like you're alone, remember I'm by your side.  If you ever feel like you're alone, don't close your eyes at night..."
                    diary = mt.multiline_text(diary, 210, gs.cambria22)
                    text_height = gs.cambria22.get_height()

                    line_spacing = 200

                    for line in diary:
                        text_image = gs.cambria22.render(line, True, gs.black)
                        screen.blit(text_image, (465, line_spacing))
                        line_spacing += text_height

                elif gs.diary_choice == 3:
                    diary = "Day 17: I think I know why I'm in here.  I noticed the TV was flickering and I couldn't explain the sounds.  I think I have lost my lunch.  I also realize that there is no food or bathroom here... So I must leave at once..."
                    diary = mt.multiline_text(diary, 210, gs.cambria22)
                    text_height = gs.cambria22.get_height()

                    line_spacing = 200

                    for line in diary:
                        text_image = gs.cambria22.render(line, True, gs.black)
                        screen.blit(text_image, (465, line_spacing))
                        line_spacing += text_height

            # Page 2 - Two Math Problems (Problems A and B)
            elif page == 2:
                gs.text = 'Some ... Math problems???'
                problem_a_text = "safe_alpha=STREETSIGN / SUBJECT * 25 / 10"
                problem_a_text2 = "IF A=0...then:"
                problem_a_text3 = "Then round down safe_alpha"
                pra_text_image = gs.times14.render(problem_a_text, True, gs.black)
                pra_text_image2 = gs.arial16.render(problem_a_text2, True, gs.black)
                pra_text_image3 = gs.arial14.render(problem_a_text3, True, gs.black)
                screen.blit(pra_text_image, (440, 240))
                screen.blit(pra_text_image2, (505, 210))
                screen.blit(pra_text_image3, (495, 285))


                problem_b_text = "kn+(2k(3+n))+(k+n)"
                prb_text_image = gs.verdana22.render(problem_b_text, True, gs.black)
                prbn1_text_image = gs.verdana16.render("k= " + str(gs.prb_n1), True, gs.black)
                prbn2_text_image = gs.verdana16.render("n= " + str(gs.prb_n2), True, gs.black)
                box_text_image = gs.cambria20.render("Box I", True, gs.black)
                screen.blit(prbn1_text_image, (455, 505))
                screen.blit(prbn2_text_image, (680, 515))
                screen.blit(prb_text_image, (520, 570))


                box = pygame.Rect(430, 483, 400, 144)
                pygame.draw.rect(screen, gs.black, box, 3)

                box_text_image_rect = box_text_image.get_rect()
                box_text_image_rect.center = box.center
                screen.blit(box_text_image, (box_text_image_rect.x, 455))

            # Page 3 - Puzzle B (see excel file)
            elif page == 3:
                gs.text = '...Is there a pattern to be found?'
                pub_grid_piece = pygame.Rect(500, 250, 100, 100)
                pub_grid_piece.centerx = page_area.centerx
                pub_grid_piece.centery = page_area.centery

                pub_grid_numbers = [gs.pub_n1, gs.pub_n3, gs.pub_n2,
                                    gs.pub_n4, gs.pub_n5, gs.pub_n6,
                                    gs.pub_n7, "?", gs.pub_n9]

                width = 100
                height = 100
                grid = [(((pub_grid_piece.x - width)/100), ((pub_grid_piece.y - height)/100)), # Grid 1
                        (((pub_grid_piece.x + width)/100), ((pub_grid_piece.y - height)/100)), # Grid 3
                        ((pub_grid_piece.x/100), ((pub_grid_piece.y - height)/100)), # Grid 2 >> 2 is after 3 because of how the grid calcs
                        (((pub_grid_piece.x - width)/100), (pub_grid_piece.y/100)), # Grid 4
                        ((pub_grid_piece.x/100), (pub_grid_piece.y/100)), # Grid 5 *** Same as grid piece
                        (((pub_grid_piece.x + width)/100), (pub_grid_piece.y/100)), # Grid 6
                        (((pub_grid_piece.x - width)/100), ((pub_grid_piece.y + height)/100)), # Grid 7
                        ((pub_grid_piece.x/100), ((pub_grid_piece.y + height)/100)), # Grid 8
                        (((pub_grid_piece.x + width)/100), ((pub_grid_piece.y + height)/100)), # Grid 9
                        ]

                index = 0

                for column, row in grid:

                    x = column * width
                    y = row * height
                    current_grid = pygame.Rect(x, y, width, height)
                    if index == 6:
                        pygame.draw.rect(screen, gs.blue_book_color, current_grid)
                        pygame.draw.rect(screen, gs.black, current_grid, 3)
                    else:
                        pygame.draw.rect(screen, gs.black, current_grid, 3)

                    text_image = gs.verdana22.render(str(pub_grid_numbers[index]), True, gs.black)
                    text_rect = text_image.get_rect(center = current_grid.center)

                    screen.blit(text_image, text_rect)
                    index += 1

                box_text_image = gs.cambria20.render("Box II", True, gs.black)
                box_text_image_rect = box_text_image.get_rect()
                box_text_image_rect.center = pub_grid_piece.center
                screen.blit(box_text_image, (box_text_image_rect.x, 195))

                text = 'ONLY THE LAST 3 DIGITS of ?'
                text_image = gs.cambria18.render(text, True, gs.black)
                text_image_rect = text_image.get_rect()
                text_image_rect.center = pub_grid_piece.center
                screen.blit(text_image, (text_image_rect.x, 573))

            # Page 4 - Colors in random order for Puzzle A based on how they were generated
            elif page == 4:
                gs.text = 'Colors?'
                pua_grid_piece = pygame.Rect(500, 250, 150, 30)

                width = 150
                height = 30
                x = 500
                y = 250

                grid = [pua_grid_piece, pua_grid_piece, pua_grid_piece, pua_grid_piece, pua_grid_piece, pua_grid_piece]
                index = 1

                for bar in grid:
                    for v in gs.color_codes.values():
                        if v[0] == index:
                            color = v[2]
                            current_rect = pygame.Rect(x, y, width, height)
                            pygame.draw.rect(screen, color, current_rect)
                            x += 15
                            y += 40
                            index += 1

        elif gs.current_book == 'yellow_book':
            # Page 1
            if page == 1:
                gs.text = None
                channels = ['', # todo update channels accordingly
                            '',
                            '',
                            '',
                            'There are numbers...',
                            'In the achievements...',
                            'For more achievements...',
                            'START WITH 1',
                            'Do you like puzzles?',
                            '',
                            '']
                line_spacing = 200
                text_height = gs.verdana18.get_height()

                heading_image = gs.cambria30.render('THIS BOOK', True, gs.black)
                screen.blit(heading_image, ((self.page_area.centerx-(heading_image.get_width()/2)), (line_spacing-25)))

                for channel in channels:
                    text_image = gs.verdana18.render(channel, True, gs.black)
                    screen.blit(text_image, (465, line_spacing+35))
                    line_spacing += text_height

            # Page 2
            if page == 2:
                instructions = ['',
                                '',
                                'dO yOU lIKE pUZZLES?',
                                'ENTER RAPPICAN',
                                '',
                                '',
                                '',
                                '',
                                '3o!3o!6o!fo!',
                                '3o!3o!6o!fo!',
                                '',
                                ''
                                ]
                line_spacing = 200
                text_height = gs.verdana18.get_height()

                heading_image = gs.cambria30.render('HOLDS MANY', True, gs.black)
                screen.blit(heading_image, ((self.page_area.centerx-(heading_image.get_width()/2)), (line_spacing-25)))

                for instruction in instructions:
                    text_image = gs.verdana18.render(instruction, True, gs.black)
                    screen.blit(text_image, (460, line_spacing+35))
                    line_spacing += text_height

            # Page 3
            if page == 3:
                instructions = ['',
                                '',
                                'do YOU like PUZZLES?',
                                'egg',
                                '',
                                'numbers',
                                'the beginning of Fun',
                                'is',
                                'helpFul',
                                ''
                                ]
                line_spacing = 200
                text_height = gs.verdana18.get_height()

                heading_image = gs.cambria30.render('SECRETS', True, gs.black)
                screen.blit(heading_image, ((self.page_area.centerx-(heading_image.get_width()/2)), (line_spacing-25)))

                for instruction in instructions:
                    text_image = gs.verdana18.render(instruction, True, gs.black)
                    screen.blit(text_image, (460, line_spacing+35))
                    line_spacing += text_height
            # Page 4
            if page == 4:
                #surface = pygame.Surface((100,100))

                text_image = gs.cambria18.render('this page intentially leFt blank', True, gs.gray)
                text_image_rect = text_image.get_rect(center = self.page_area.center)
                screen.blit(text_image, text_image_rect)


    def open_shirt(self, gs, screen):
        # Open Shirt
        screen.blit(enlarged_shirt, self.shirt_rect)


        #pygame.draw.polygon(screen, gs.yellow, self.clickbox_shirt_pocket, 1)

    def shirt_clicks(self, gs, event, steamworks):
        # Closes shirt if anywhere is clicked but the shirt
        if gs.shirt_opened:
            gs.text = 'A nice shirt.'
        if gs.shirt_opened == True and not self.shirt_rect.collidepoint(event.pos):
            gs.shirt_opened = False
            gs.stable_item_opened = False
            gs.text = None

        if gf.check_inside_clickbox(self, self.clickbox_shirt_pocket, ((event.pos), (0, 0))) and not gs.purple_key_found:
            gs.text = 'I found a purple key!'
            pygame.mixer.Sound.play(key_sound)
            gs.purple_key_found = True
            gs.moveable_items_index_list.append(2)
            gf.found_all_items(gs, steamworks)

    def pull_up_desk_drawer(self, gs, screen):
        # Pull up drawer



        screen.blit(self.scaled_drawer, (self.sdx - self.scaled_drawer.get_width() // 2, self.sdy - self.scaled_drawer.get_height() // 2 ))
        gs.text = "This is the drawer I pulled out of the desk. I think it's useless now, but I'll carry it..."

    def pull_up_desk_drawer_clicks(self, gs, event):
        # Closes drawer if anywhere is clicked but the drawer

        if gs.desk_drawer_up == True and not self.drawer_rect.collidepoint(event.pos):
            gs.desk_drawer_up = False
            gs.stable_item_opened = False
            gs.text = None

    def draw_manual(self, gs, screen):  # Defines and draws the manuals when they are clicked todo figure out what needs to go in the manuals
        """Function to draw the manuals to the screen based on the inputs given, i.e. which color/which one is clicked"""


        cf = 5  # CF stands for change factor
        cover_color = None

        # Define the colors of the covers, as they can change
        if gs.current_book == 'red_book':
            cover_color = gs.red_book_color
        elif gs.current_book == 'blue_book':
            cover_color = gs.blue_book_color
        elif gs.current_book == 'yellow_book':
            cover_color = gs.yellow_book_color

        # Draw the covers
        pygame.draw.rect(screen, cover_color, self.manual_view_cover)
        pygame.draw.polygon(screen, cover_color, (self.manual_view_cover.topleft, (160, 58), (160, 727), self.manual_view_cover.bottomleft))

        # Draw the pages that you view on the right side
        pygame.draw.rect(screen, gs.off_white, self.manual_pages)
        pygame.draw.rect(screen, gs.black, self.manual_pages, 2)

        # Draw page area
        #pygame.draw.rect(screen, gs.green, self.page_area)

        # Draw the exterior borders for the covers
        pygame.draw.polygon(screen, gs.black, self.back_cover, 3)
        pygame.draw.rect(screen, gs.black, self.manual_view_cover, 3)

        # Draw the pages that you can view on the left side
        if gs.current_page == 1:
            self.book_page_content(gs, screen, gs.current_page, self.page_area)

        if gs.current_page == 2:
            # Page 2
            pygame.draw.polygon(screen, gs.off_white, (self.manual_pages.topleft, (self.bc_x + cf * 5 * gs.current_page, self.bc_tc_y), (self.bc_x + cf * 5 * gs.current_page, self.bc_bc_y), self.manual_pages.bottomleft))
            pygame.draw.polygon(screen, gs.black, (self.manual_pages.topleft, (self.bc_x + cf * 5 * gs.current_page, self.bc_tc_y), (self.bc_x + cf * 5 * gs.current_page, self.bc_bc_y), self.manual_pages.bottomleft), 2)
            self.book_page_content(gs, screen, gs.current_page, self.page_area) # Function to call the contents of the page
        elif gs.current_page == 3:
            # Page 2
            pygame.draw.polygon(screen, gs.off_white, (self.manual_pages.topleft, (self.bc_x + cf * 5 * (gs.current_page-1), self.bc_tc_y), (self.bc_x + cf * 5 * (gs.current_page-1), self.bc_bc_y), self.manual_pages.bottomleft))
            pygame.draw.polygon(screen, gs.black, (self.manual_pages.topleft, (self.bc_x + cf * 5 * (gs.current_page-1), self.bc_tc_y), (self.bc_x + cf * 5 * (gs.current_page-1), self.bc_bc_y), self.manual_pages.bottomleft), 2)
            # Page 3
            pygame.draw.polygon(screen, gs.off_white, (self.manual_pages.topleft, (self.bc_x + cf * 5 * gs.current_page, self.bc_tc_y), (self.bc_x + cf * 5 * gs.current_page, self.bc_bc_y), self.manual_pages.bottomleft))
            pygame.draw.polygon(screen, gs.black, (self.manual_pages.topleft, (self.bc_x + cf * 5 * gs.current_page, self.bc_tc_y), (self.bc_x + cf * 5 * gs.current_page, self.bc_bc_y), self.manual_pages.bottomleft), 2)
            self.book_page_content(gs, screen, gs.current_page, self.page_area) # Function to call the contents of the page
        elif gs.current_page == 4:
            # Page 2
            pygame.draw.polygon(screen, gs.off_white, (self.manual_pages.topleft, (self.bc_x + cf * 5 * (gs.current_page-2), self.bc_tc_y), (self.bc_x + cf * 5 * (gs.current_page-2), self.bc_bc_y), self.manual_pages.bottomleft))
            pygame.draw.polygon(screen, gs.black, (self.manual_pages.topleft, (self.bc_x + cf * 5 * (gs.current_page-2), self.bc_tc_y), (self.bc_x + cf * 5 * (gs.current_page-2), self.bc_bc_y), self.manual_pages.bottomleft), 2)
            # Page 3
            pygame.draw.polygon(screen, gs.off_white, (self.manual_pages.topleft, (self.bc_x + cf * 5 * (gs.current_page-1), self.bc_tc_y), (self.bc_x + cf * 5 * (gs.current_page-1), self.bc_bc_y), self.manual_pages.bottomleft))
            pygame.draw.polygon(screen, gs.black, (self.manual_pages.topleft, (self.bc_x + cf * 5 * (gs.current_page-1), self.bc_tc_y), (self.bc_x + cf * 5 * (gs.current_page-1), self.bc_bc_y), self.manual_pages.bottomleft), 2)
            # Page 4
            pygame.draw.polygon(screen, gs.off_white, (self.manual_pages.topleft, (self.bc_x + cf * 5 * gs.current_page, self.bc_tc_y), (self.bc_x + cf * 5 * gs.current_page, self.bc_bc_y), self.manual_pages.bottomleft))
            pygame.draw.polygon(screen, gs.black, (self.manual_pages.topleft, (self.bc_x + cf * 5 * gs.current_page, self.bc_tc_y), (self.bc_x + cf * 5 * gs.current_page, self.bc_bc_y), self.manual_pages.bottomleft), 2)
            self.book_page_content(gs, screen, gs.current_page, self.page_area) # Function to call the contents of the page
        elif gs.current_page == 5:
            # Page 2
            pygame.draw.polygon(screen, gs.off_white, (self.manual_pages.topleft, (self.bc_x + cf * 5 * (gs.current_page-3), self.bc_tc_y), (self.bc_x + cf * 5 * (gs.current_page-3), self.bc_bc_y), self.manual_pages.bottomleft))
            pygame.draw.polygon(screen, gs.black, (self.manual_pages.topleft, (self.bc_x + cf * 5 * (gs.current_page-3), self.bc_tc_y), (self.bc_x + cf * 5 * (gs.current_page-3), self.bc_bc_y), self.manual_pages.bottomleft), 2)
            # Page 3
            pygame.draw.polygon(screen, gs.off_white, (self.manual_pages.topleft, (self.bc_x + cf * 5 * (gs.current_page-2), self.bc_tc_y), (self.bc_x + cf * 5 * (gs.current_page-2), self.bc_bc_y), self.manual_pages.bottomleft))
            pygame.draw.polygon(screen, gs.black, (self.manual_pages.topleft, (self.bc_x + cf * 5 * (gs.current_page-2), self.bc_tc_y), (self.bc_x + cf * 5 * (gs.current_page-2), self.bc_bc_y), self.manual_pages.bottomleft), 2)
            # Page 4
            pygame.draw.polygon(screen, gs.off_white, (self.manual_pages.topleft, (self.bc_x + cf * 5 * (gs.current_page-1), self.bc_tc_y), (self.bc_x + cf * 5 * (gs.current_page-1), self.bc_bc_y), self.manual_pages.bottomleft))
            pygame.draw.polygon(screen, gs.black, (self.manual_pages.topleft, (self.bc_x + cf * 5 * (gs.current_page-1), self.bc_tc_y), (self.bc_x + cf * 5 * (gs.current_page-1), self.bc_bc_y), self.manual_pages.bottomleft), 2)
            self.book_page_content(gs, screen, gs.current_page, self.page_area) # Function to call the contents of the page

            gs.red_book_opened = False
            gs.blue_book_opened = False
            gs.yellow_book_opened = False
            gs.stable_item_opened = False
            gs.text = None
            color_cover = None
            gs.current_page = 1

    def change_manual_pages(self, gs, event, steamworks):
        """Function to change the pages in the manuals"""
        if self.manual_pages.collidepoint(event.pos):
            if gs.current_book == 'red_book' and gs.current_page == 4 and not gs.red_key_found and gf.check_inside_clickbox(self, self.red_key_clickbox, ((event.pos), (0, 0))):
                gs.text = 'Hey! A red key! What does it go to?'
                pygame.mixer.Sound.play(key_sound)
                gs.red_key_found = True
                gs.moveable_items_index_list.append(1)
                gf.found_all_items(gs, steamworks)
            else:
                gs.current_page += 1
                pygame.mixer.Sound.play(flip_page_sound)
        else:
            gs.red_book_opened = False
            gs.blue_book_opened = False
            gs.yellow_book_opened = False
            gs.stable_item_opened = False
            gs.text = None
            color_cover = None
            gs.current_page = 1

    def draw_remote(self, gs, screen):
        """Function to draw the remote when clicked"""

        if gs.current_room_view == 1 and gs.room_view_drill_down == 0:
            # Draw Enlarged Remote Inventory Item When Clicked on the TV view
            screen.blit(enlarged_remote, (750,195))
            pygame.draw.rect(screen, gs.yellow, self.remote_rect, -1)

            """
            # Commented out to show or not show clickboxes for remote
            index = 0
            for box in self.remote_square_buttons_clickbox:
                pygame.draw.polygon(screen, gs.clickboxcolor, self.remote_square_buttons_clickbox[index], 1)
                index += 1
            """

            if gs.close_remote:
                gs.remote_opened = False
                gs.stable_item_opened = False
                gs.close_remote = False
                gs.button_input_list.clear()
        else:
            gs.text = 'I need to point the remote at the TV...'
            gs.remote_opened = False
            gs.stable_item_opened = False

    def remote_buttons_clicked(self, gs, event, steamworks):
        """Function to change the TV screen when remote can be opened as well as close the remote"""
        if gs.batteries_input:
            for box in self.remote_square_buttons_clickbox:
                if gf.check_inside_clickbox(self, box, ((event.pos), (0, 0))):
                    box_index = self.remote_square_buttons_clickbox.index(box)
                    # print(box_index) # todo comment this out later

                    # Logic for when buttons are pressed on remote and how they interact with the TV
                    if not gs.tv_on:
                        print("tv off")
                        if box_index == 26:
                            if gs.current_channel == 'INVALID':
                                gs.current_channel = '3'
                            elif gs.current_channel == '7':
                                pygame.mixer.Sound.play(safe_init_sound)
                            gs.tv_on = True

                            gs.text = 'I turned on the TV.'
                    elif gs.tv_on:
                        if box_index == 0:  # Volume Up todo figure out how sounds work in pygame
                            pass
                        elif box_index == 1:  # Volume Down todo figure out how sounds work in pygame
                            pass
                        elif box_index == 2:  # Channel Up
                            if gs.current_channel.isnumeric() and len(gs.current_channel) <= 12:
                                gs.current_channel = str(int(gs.current_channel)+1)
                                gs.current_tv_screen_color = gs.tv_screen
                            else:
                                gs.current_channel = 'INVALID'
                                gs.current_tv_screen_color = gs.tv_screen
                        elif box_index == 3:  # Channel Down
                            if gs.current_channel.isnumeric():
                                gs.current_channel = str(int(gs.current_channel)-1)
                                gs.current_tv_screen_color = gs.tv_screen
                            else:
                                gs.current_channel = 'INVALID'
                                gs.current_tv_screen_color = gs.tv_screen
                        elif box_index >= 4 and box_index <= 13:  # Numbers 1,2,3,4,5,6,7,8,9,0
                            gs.button_input_list.append(box_index)
                            self.enter_button(gs)
                        elif box_index == 14:  # L Button
                            gs.button_input_list.clear()
                        elif box_index == 15:  # F Button
                            gs.button_input_list.append(box_index)
                            self.enter_button(gs)
                        elif box_index == 16:  # Rewind
                            pass # todo print something in text stating that nothing happened
                        elif box_index == 17:  # Play
                            if gs.current_channel == str(11):
                                pygame.mixer.stop()
                                pygame.mixer.Sound.play(message_sound, loops=0)
                        elif box_index == 18:  # Pause
                            pygame.mixer.pause()
                        elif box_index == 19:  # Fast Forward
                            pass # todo print something in text stating that nothing happened
                        elif box_index == 20:  # Mute todo figure out how sounds work in pygame
                            if not gs.muted:
                                gs.volume = message_sound.get_volume()
                                message_sound.set_volume(0)
                                gs.muted = True
                            else:
                                message_sound.set_volume(gs.volume)
                                gs.muted = False
                        elif box_index == 21:  # Central Play
                            self.remote_entry(gs)
                            self.check_channel_achievements(gs, steamworks)

                        elif box_index == 22:  # Top Arrow
                            gs.button_input_list.append(box_index)
                            self.enter_button(gs)
                        elif box_index == 23:  # Right Arrow
                            gs.button_input_list.append(box_index)
                            self.enter_button(gs)
                        elif box_index == 24:  # Bottom Arrow
                            gs.button_input_list.append(box_index)
                            self.enter_button(gs)
                        elif box_index == 25:  # Left Arrow
                            gs.button_input_list.append(box_index)
                            self.enter_button(gs)
                        elif box_index == 26:  # Power Button
                            gs.tv_on = False
                            gs.current_tv_screen_color = gs.tv_screen
                            gs.safe_initialized = False
                            pygame.mixer.stop()
                            gs.text = 'I turned off the TV.'

        else:
            gs.text = "The remote isn't working right now..."

        # Closes remote if anywhere is clicked but the remote
        if gs.remote_opened == True and not self.remote_rect.collidepoint(event.pos):
            gs.close_remote = True
            gs.message_channel_play = False
            pygame.mixer.stop()

    def enter_button(self, gs):
        temp_channel = []
        if len(gs.button_input_list) <= 12:
            for button in gs.button_input_list:
                temp_channel.append(self.number_index_dict.get(str(button)))
                gs.entered_buttons = ''.join(map(str, temp_channel))
        else:
            gs.current_channel = 'INVALID'
            gs.button_input_list.clear()

    def check_channel_achievements(self, gs, steamworks):
        if gs.current_channel == '1234567890F':
            check_steam.check_set_achievement(steamworks, b'ACH_BUTTONS') # Buttons Achievement
        if gs.current_channel == '181161693114':
            check_steam.check_set_achievement(steamworks, b'ACH_RAPP') # Rappican Achievement
        if gs.current_channel == '1510F':
            check_steam.check_set_achievement(steamworks, b'ACH_IVXF') # IVXF Achievement Channel

    def remote_entry(self, gs):
        temp_channel = []
        if len(gs.button_input_list) <= 12:
            gs.current_tv_screen_color = gs.tv_screen
            for button in gs.button_input_list:
                temp_channel.append(self.number_index_dict.get(str(button)))
                gs.current_channel = ''.join(map(str, temp_channel))

            gs.button_input_list.clear()
        else:
            gs.current_channel = 'INVALID'
            gs.current_tv_screen_color = gs.tv_screen
            gs.button_input_list.clear()

    def draw_papers(self, gs, screen):
        """Function to draw the papers to the screen"""

        # Clickboxes
        if gs.screen_width == 1200:
            #self.papers_page1_clickbox = pygame.draw.polygon(screen, gs.clickboxcolor, self.papers_page1_list, 1)
            #self.papers_page2_clickbox = pygame.draw.polygon(screen, gs.clickboxcolor, self.papers_page2_list, 1)
            #self.papers_page3_clickbox = pygame.draw.polygon(screen, gs.clickboxcolor, self.papers_page3_list, 1)
            x_spacing = 530
            line_spacing = 150
            line_spacing_3 = 95
            x_spacing_3 = 325
        else:
            #self.papers_page1_clickbox = pygame.draw.polygon(screen, gs.red, self.papers_page1_list, 1)
            #self.papers_page2_clickbox = pygame.draw.polygon(screen, gs.red, self.papers_page2_list, 1)
            #self.papers_page3_clickbox = pygame.draw.polygon(screen, gs.red, self.papers_page3_list, 1)
            x_spacing = 722
            line_spacing = 220
            line_spacing_3 = 172
            x_spacing_3 = 425

        if gs.current_paper_in_view == 1:
            gs.text = 'What does this stuff mean?'
            # Code to Scale and Draw All Pages
            sdx = gs.gw_width // 2
            sdy = gs.gw_height // 2
            scaled_papers = gf.aspect_scale(enlarged_papers_top1, 625)
            screen.blit(scaled_papers, (sdx - scaled_papers.get_width() // 2, sdy - scaled_papers.get_height() // 2 ))

            texts = ['',
                    'open thrice',
                    '',
                    'and more',
                    '',
                    '',
                    '',
                    'check out:', str(gs.random_channel)
                    ]

            #line_spacing = 150

            text_height = gs.verdana22.get_height()
            angle = 6

            for text in texts:
                if text == '':
                    line_spacing += text_height
                    x_spacing -= 10
                    angle += 8
                else:
                    text_image = gs.verdana22.render(text, True, gs.black)
                    text_image = pygame.transform.rotozoom(text_image, angle, 1)
                    screen.blit(text_image, (x_spacing, line_spacing))
                    line_spacing += text_height
                    x_spacing -= 10
                    angle += 8

        if gs.current_paper_in_view == 2:
            gs.text = 'Is this a puzzle?'
            # Code to Scale and Draw All Pages
            sdx = gs.gw_width // 2
            sdy = gs.gw_height // 2
            scaled_papers = gf.aspect_scale(enlarged_papers_top2, 625)
            screen.blit(scaled_papers, (sdx - scaled_papers.get_width() // 2, sdy - scaled_papers.get_height() // 2 ))

            puzzles.get_board(gs, screen, 10, gs.pua_double_digits)

        if gs.current_paper_in_view == 3:
            gs.text = 'What?'
            # Code to Scale and Draw All Pages
            sdx = gs.gw_width // 2
            sdy = gs.gw_height // 2
            scaled_papers = gf.aspect_scale(enlarged_papers_top3, 625)
            screen.blit(scaled_papers, (sdx - scaled_papers.get_width() // 2, sdy - scaled_papers.get_height() // 2 ))

            texts = ['',
                    'SAFE TO SAY: ',
                    '    LEAVE IT ON SEVEN!',
                    '',
                    '',
                    'solve, then',
                    'boxIboxII >',
                    '',
                    '',
                    'colors number downward',
                    '',
                    'grids number upward',
                    'without diamonds'
                    ]


            text_height = gs.verdana22.get_height()
            angle = 13

            for text in texts:
                if text == '':
                    line_spacing_3 += text_height
                    x_spacing_3 += 12
                else:
                    text_image = gs.times20.render(text, True, gs.black)
                    #text_image = pygame.transform.rotate(text_image, angle)
                    text_image = pygame.transform.rotozoom(text_image, angle, 1)
                    screen.blit(text_image, (x_spacing_3, line_spacing_3))
                    line_spacing_3 += text_height
                    x_spacing_3 += 12
                    #angle += 2.5

    def change_papers(self, gs, event):
        """Function to flip through the papers on the screen"""

        if gf.check_inside_clickbox(self, self.papers_page1_list, ((event.pos), (0, 0))) and not gf.check_inside_clickbox(self, self.papers_page2_list, ((event.pos), (0, 0))) and not gf.check_inside_clickbox(self, self.papers_page3_list, ((event.pos), (0, 0))):
            pygame.mixer.Sound.play(flip_page_sound)
            gs.current_paper_in_view = 1
        if gs.current_paper_in_view == 1:
            if gf.check_inside_clickbox(self, self.papers_page2_list, ((event.pos), (0, 0))) and not gf.check_inside_clickbox(self, self.papers_page1_list, ((event.pos), (0, 0))):
                pygame.mixer.Sound.play(flip_page_sound)
                gs.current_paper_in_view = 2
        if gs.current_paper_in_view == 3:
            if gf.check_inside_clickbox(self, self.papers_page2_list, ((event.pos), (0, 0))) and not gf.check_inside_clickbox(self, self.papers_page3_list, ((event.pos), (0, 0))):
                pygame.mixer.Sound.play(flip_page_sound)
                gs.current_paper_in_view = 2
        if gf.check_inside_clickbox(self, self.papers_page3_list, ((event.pos), (0, 0))) and not gf.check_inside_clickbox(self, self.papers_page1_list, ((event.pos), (0, 0))) and not gf.check_inside_clickbox(self, self.papers_page2_list, ((event.pos), (0, 0))):
            pygame.mixer.Sound.play(flip_page_sound)
            gs.current_paper_in_view = 3
        if gs.papers_opened == True and not gf.check_inside_clickbox(self, self.papers_page1_list, ((event.pos), (0, 0))) and not gf.check_inside_clickbox(self, self.papers_page2_list, ((event.pos), (0, 0))) and not gf.check_inside_clickbox(self, self.papers_page3_list, ((event.pos), (0, 0))):
            pygame.mixer.Sound.play(flip_page_sound)
            gs.papers_opened = False
            gs.stable_item_opened = False
            gs.text = None
            gs.current_paper_in_view = 1






