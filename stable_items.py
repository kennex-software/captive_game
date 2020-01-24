#kennex

import pygame, time
import gf
import pygame.font
import puzzles
import multiline_text as mt
import random
from settings import Settings
import inventory

i_enlarged_remote = 'images/remote_enlarged.png'
i_enlarged_papers_top1 = 'images/papers_1top.png'
i_enlarged_papers_top2 = 'images/papers_2top.png'
i_enlarged_papers_top3 = 'images/papers_3top.png'

enlarged_remote = pygame.image.load(i_enlarged_remote)
enlarged_papers_top1 = pygame.image.load(i_enlarged_papers_top1)
enlarged_papers_top2 = pygame.image.load(i_enlarged_papers_top2)
enlarged_papers_top3 = pygame.image.load(i_enlarged_papers_top3)

class Stable_Items():
    """Class to store all of the information regarding the camera and chair manuals"""
    def __init__(self, gs, screen):
        self.gs = gs
        self.screen = screen

    def book_page_content(self, gs, screen, page, page_area):
        if gs.current_manual == 'red_book':
            # Page 1
            if page == 1:
                channels = ['',
                        'Press Button on Remote',
                        'To go to a Channel',
                        '',
                        '1... Nothing?',
                        '2... Wait for it',
                        '3... Default',
                        '4... Camera 1',
                        '5... Camera 2',
                        '6... Camera 3',
                        '7... Nothing?',
                        '8... Nothing?',
                        '9...',
                        '0 + channel + F + >']
                line_spacing = 200
                text_height = gs.verdana18.get_height()

                heading_image = gs.garamond30.render('CHANNELS', True, gs.black)
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
                                '   play button afterward.'
                                '-Some channels may start with 0.',
                                '-Enjoy your TV!'
                                ]
                line_spacing = 200
                text_height = gs.verdana18.get_height()

                heading_image = gs.garamond30.render('TELEVISION', True, gs.black)
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
                                '-They are not recording.,',
                                '-Enjoy your cameras!'
                                ]
                line_spacing = 200
                text_height = gs.verdana18.get_height()

                heading_image = gs.garamond30.render('CAMERAS', True, gs.black)
                screen.blit(heading_image, ((self.page_area.centerx-(heading_image.get_width()/2)), (line_spacing-25)))

                for instruction in instructions:
                    text_image = gs.verdana18.render(instruction, True, gs.black)
                    screen.blit(text_image, (460, line_spacing+35))
                    line_spacing += text_height
            # Page 4
            if page == 4:
                surface = pygame.Surface((100,100))

                width = inventory.red_key_taped.get_width() // 3
                height = inventory.red_key_taped.get_height() // 3

                screen.blit(pygame.transform.smoothscale(inventory.red_key_taped, (width, height)), (540, 380))
                screen.blit(pygame.transform.smoothscale(inventory.ripped_tape, (width // 2, height)), (540, 380))

                red_key_clickbox = [(637, 546), (655, 531), (666, 448), (680, 411), (661, 377),
                                (635, 371), (595, 395), (598, 437), (611, 479), (616, 527), (637, 548)]

                clickbox_red_key = pygame.draw.polygon(screen, gs.yellow, red_key_clickbox, 1)

                #if gf.check_inside_clickbox(clickbox_red_key, ((event.pos), (0, 0))):
                #    print("clicked")

                # todo figure out how to turn this into a clickbox and select the key

        elif gs.current_manual == 'blue_book':
            if page == 1:
                # Page 1 - Pages to a diary
                if gs.diary_choice == 1:
                    diary = "words1"
                    diary = mt.multiline_text(diary, 210, gs.garamond22)
                    text_height = gs.garamond22.get_height()

                    line_spacing = 200

                    for line in diary:
                        text_image = gs.garamond22.render(line, True, gs.black)
                        screen.blit(text_image, (465, line_spacing))
                        line_spacing += text_height

                elif gs.diary_choice == 2:
                    diary = "words2"
                    diary = mt.multiline_text(diary, 210, gs.garamond22)
                    text_height = gs.garamond22.get_height()

                    line_spacing = 200

                    for line in diary:
                        text_image = gs.garamond22.render(line, True, gs.black)
                        screen.blit(text_image, (465, line_spacing))
                        line_spacing += text_height

                elif gs.diary_choice == 3:
                    diary = "words3"
                    diary = mt.multiline_text(diary, 210, gs.garamond22)
                    text_height = gs.garamond22.get_height()

                    line_spacing = 200

                    for line in diary:
                        text_image = gs.garamond22.render(line, True, gs.black)
                        screen.blit(text_image, (465, line_spacing))
                        line_spacing += text_height

            # Page 2 - Two Math Problems (Problems A and B)
            elif page == 2:
                problem_b_text = "kn+(2k(3+n))+(k+n)"
                prb_text_image = gs.verdana22.render(problem_b_text, True, gs.black)
                prbn1_text_image = gs.verdana16.render("k= " + str(gs.prb_n1), True, gs.black)
                prbn2_text_image = gs.verdana16.render("n= " + str(gs.prb_n2), True, gs.black)
                screen.blit(prbn1_text_image, (455, 505))
                screen.blit(prbn2_text_image, (680, 515))
                screen.blit(prb_text_image, (520, 570))

            # Page 3 - Puzzle B (see excel file)
            elif page == 3:
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
                    pygame.draw.rect(screen, gs.black, current_grid, 3)

                    text_image = gs.verdana22.render(str(pub_grid_numbers[index]), True, gs.black)
                    text_rect = text_image.get_rect(center = current_grid.center)

                    screen.blit(text_image, text_rect)
                    index += 1

            # Page 4 - Colors in random order for Puzzle A based on how they were generated
            elif page == 4:
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

                """
                # Grid 1
                (((pub_grid_piece.x + width)/100), ((pub_grid_piece.y - height)/100)), # Grid 3
                ((pub_grid_piece.x/100), ((pub_grid_piece.y - height)/100)), # Grid 2 >> 2 is after 3 because of how the grid calcs
                (((pub_grid_piece.x - width)/100), (pub_grid_piece.y/100)), # Grid 4
                ((pub_grid_piece.x/100), (pub_grid_piece.y/100)), # Grid 5 *** Same as grid piece
                (((pub_grid_piece.x + width)/100), (pub_grid_piece.y/100)), # Grid 6
                (((pub_grid_piece.x - width)/100), ((pub_grid_piece.y + height)/100)), # Grid 7
                ((pub_grid_piece.x/100), ((pub_grid_piece.y + height)/100)), # Grid 8
                (((pub_grid_piece.x + width)/100), ((pub_grid_piece.y + height)/100)), # Grid 9
                



                for bar in grid:

                    x = column * width
                    y = row * height
                    current_grid = pygame.Rect(x, y, width, height)
                    pygame.draw.rect(screen, gs.black, current_grid, 3)
                """


    def draw_manual(self, gs, screen):  # Defines and draws the manuals when they are clicked todo figure out what needs to go in the manuals
        """Function to draw the manuals to the screen based on the inputs given, i.e. which color/which one is clicked"""

        # Define the cover shapes.  These will be clickable to turn the pages
        self.manual_view_cover = pygame.Rect(410, 130, 450, 525)
        self.bc_x = 160  # Back Cover X
        self.bc_tc_y = 58  # Back Cover, Top Corner Y
        self.bc_bc_y = 727  # Back Cover, Top Corner Y
        self.back_cover = [self.manual_view_cover.topleft, (self.bc_x, self.bc_tc_y), (self.bc_x, self.bc_bc_y), self.manual_view_cover.bottomleft]
        cf = 5  # CF stands for change factor
        cover_color = None

        # Define the colors of the covers, as they can change
        if gs.current_manual == 'red_book':
            cover_color = gs.red_book_color
        elif gs.current_manual == 'blue_book':
            cover_color = gs.blue_book_color

        # Draw the covers
        pygame.draw.rect(screen, cover_color, self.manual_view_cover)
        pygame.draw.polygon(screen, cover_color, (self.manual_view_cover.topleft, (160, 58), (160, 727), self.manual_view_cover.bottomleft))

        # Draw the pages that you view on the right side
        self.manual_pages = self.manual_view_cover.inflate(-10, -10)
        self.manual_pages = self.manual_pages.move(-5, 0)
        pygame.draw.rect(screen, gs.off_white, self.manual_pages)
        pygame.draw.rect(screen, gs.black, self.manual_pages, 2)

        # Page Area for Page Content
        self.page_area = self.manual_pages.inflate(-50, -50)
        #pygame.draw.rect(screen, gs.green, self.page_area)

        # Draw the exterior borders for the covers
        pygame.draw.polygon(screen, gs.black, self.back_cover, 3)
        pygame.draw.rect(screen, gs.black, self.manual_view_cover, 3)

        #if manual_pages.collidepoint(event.pos):
        #    print("ayoooooo")

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
            gs.stable_item_opened = False
            color_cover = None
            gs.current_page = 1

    def change_manual_pages(self, gs, event):
        """Function to change the pages in the manuals"""
        if self.manual_pages.collidepoint(event.pos):
            gs.current_page += 1

    def draw_remote(self, gs, screen):
        """Function to draw the remote when clicked"""

        self.remote_rect = enlarged_remote.get_rect()
        self.remote_rect.x += 750
        self.remote_rect.y += 195

        if gs.current_room_view == 1 and gs.room_view_drill_down == 0:
            # Draw Enlarged Remote Inventory Item When Clicked on the TV view
            self.screen.blit(enlarged_remote, (750,195))
            pygame.draw.rect(screen, gs.yellow, self.remote_rect, -1)
            if gs.close_remote:
                gs.remote_opened = False
                gs.stable_item_opened = False
                gs.close_remote = False
        else:
            print("Need to be on TV view")
            gs.remote_opened = False
            gs.stable_item_opened = False

    def remote_buttons_clicked(self, gs, event):
        """Function to change the TV screen when remote can be opened as well as close the remote"""

        # Closes remote is anywhere is clicked but the remote
        if gs.remote_opened == True and not self.remote_rect.collidepoint(event.pos):
            gs.close_remote = True

    def draw_papers(self, gs, screen):  # todo figure out what needs to go on the papers (use the SVG's and don't scale them)
        """Function to draw the papers to the screen"""

        # Clickboxes
        self.papers_page1_list = [(427, 49), (841, 121), (740, 681), (327, 607)]
        self.papers_page2_list = [(322, 68), (743, 68), (743, 642), (322, 642)]
        self.papers_page3_list = [(217, 110), (629, 37), (729, 596), (315, 673)]
        #self.papers_page1_clickbox = pygame.draw.polygon(screen, gs.clickboxcolor, papers_page1_list, 1)
        #self.papers_page2_clickbox = pygame.draw.polygon(screen, gs.clickboxcolor, papers_page2_list, 1)
        #self.papers_page3_clickbox = pygame.draw.polygon(screen, gs.clickboxcolor, papers_page3_list, 1)

        if gs.current_paper_in_view == 1:
            # Code to Scale and Draw All Pages
            sdx = gs.gw_width // 2
            sdy = gs.gw_height // 2
            scaled_papers = gf.aspect_scale(enlarged_papers_top1, 625)
            screen.blit(scaled_papers, (sdx - scaled_papers.get_width() // 2, sdy - scaled_papers.get_height() // 2 ))

        if gs.current_paper_in_view == 2:
            # Code to Scale and Draw All Pages
            sdx = gs.gw_width // 2
            sdy = gs.gw_height // 2
            scaled_papers = gf.aspect_scale(enlarged_papers_top2, 625)
            screen.blit(scaled_papers, (sdx - scaled_papers.get_width() // 2, sdy - scaled_papers.get_height() // 2 ))

            board = puzzles.get_board(gs, screen, 10, gs.pua_double_digits)

        if gs.current_paper_in_view == 3:

            # Code to Scale and Draw All Pages
            sdx = gs.gw_width // 2
            sdy = gs.gw_height // 2
            scaled_papers = gf.aspect_scale(enlarged_papers_top3, 625)
            screen.blit(scaled_papers, (sdx - scaled_papers.get_width() // 2, sdy - scaled_papers.get_height() // 2 ))

    def change_papers(self, gs, event):
        """Function to flip through the papers on the screen"""

        if gf.check_inside_clickbox(self, self.papers_page1_list, ((event.pos), (0, 0))) and not gf.check_inside_clickbox(self, self.papers_page2_list, ((event.pos), (0, 0))) and not gf.check_inside_clickbox(self, self.papers_page3_list, ((event.pos), (0, 0))):
            gs.current_paper_in_view = 1
        if gs.current_paper_in_view == 1:
            if gf.check_inside_clickbox(self, self.papers_page2_list, ((event.pos), (0, 0))) and not gf.check_inside_clickbox(self, self.papers_page1_list, ((event.pos), (0, 0))):
                gs.current_paper_in_view = 2
        if gs.current_paper_in_view == 3:
            if gf.check_inside_clickbox(self, self.papers_page2_list, ((event.pos), (0, 0))) and not gf.check_inside_clickbox(self, self.papers_page3_list, ((event.pos), (0, 0))):
                gs.current_paper_in_view = 2
        if gf.check_inside_clickbox(self, self.papers_page3_list, ((event.pos), (0, 0))) and not gf.check_inside_clickbox(self, self.papers_page1_list, ((event.pos), (0, 0))) and not gf.check_inside_clickbox(self, self.papers_page2_list, ((event.pos), (0, 0))):
            gs.current_paper_in_view = 3
        if gs.papers_opened == True and not gf.check_inside_clickbox(self, self.papers_page1_list, ((event.pos), (0, 0))) and not gf.check_inside_clickbox(self, self.papers_page2_list, ((event.pos), (0, 0))) and not gf.check_inside_clickbox(self, self.papers_page3_list, ((event.pos), (0, 0))):
            gs.papers_opened = False
            gs.stable_item_opened = False
            gs.current_paper_in_view = 1






