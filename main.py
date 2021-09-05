from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QTableWidget,  QFileDialog, QDialog, QTableWidgetItem, QStyle
from PyQt6 import QtGui, QtCore
import sys
import os
from ui_def import Ui_MainWindow
import json
import logging
from constants import EQUIP_LIST_ORDER, STAT_LOOKUP_TABLE, SET_LOOKUP_TABLE, RARITY_COLOUR_LOOKUP_TABLE\
    , ELEMENT_COLOUR_LOOKUP_TABLE, SET_IMAGE_SIZE, EQUIP_LIST_ORDER, FILL_WHITE, FNT, FNT2, FNT3, FNT4\
    , FN2SMALL, FN2VSMALL, FNT5, ARTIFACT_FNT, NEW_SET_LOOKUP_TABLE, FNT6, IMPRINT_LOOKUP
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageChops
import datetime
import requests
import webbrowser
import traceback
import collections
import decimal

logging.basicConfig(filename='infographic.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s: %(message)s')

def send_messages(message, ui_log):
    '''Helper function to send a single message to multiple output logs'''
    if ui_log == 'input':
        target_ui_log = ui.jsonLogText
    if ui_log == 'output':
        target_ui_log = ui.outputLogText
    target_ui_log.appendPlainText(f'{datetime.datetime.now().strftime("%Y-%M-%d %H:%M:%S")}: {message}')
    logging.info(message)

def fileInputDialogButton(buttonName):
    '''Dialog handler for fileInput tab. Returns filename to edits on page.'''
    home_dir = os.getcwd()
    fileName = QFileDialog.getOpenFileName(window, "Open File",home_dir, '*.json')
    if fileName[0]:
        if buttonName == 'herodataButton':
            ui.heroDataEdit.setText(fileName[0])
        elif buttonName == 'artifactDataButton':
            ui.artifactDataEdit.setText(fileName[0])
        elif buttonName == 'fribbelsButton':
            ui.fribbelsDataEdit.setText(fileName[0])

def fileOutputDialogButton(buttonName):
    '''Dialog handler for Output file tab. Returns filename to edits on page.'''
    home_dir = os.path.join(os.getcwd(), 'output')
    directory = QFileDialog.getExistingDirectory(window, caption="Output File Directory", directory=home_dir)
    if directory:
        if buttonName == 'outputLocationButton':
            ui.outputLocationEdit.setText(directory)


def loadFileData(heroDataFileName, artifactDataFileName, fribbelsDataFileName):
    '''File Manager for Loading Data'''
    fileerror = 0
    if os.path.exists(heroDataFileName) == False:
        send_messages(f'Hero Data File Not Found - Please check if you entered it correctly', 'input')
        fileerror = fileerror + 1
    else:
        send_messages(f'Processing hero data file {heroDataFileName}', 'input')
    if os.path.exists(artifactDataFileName) == False:
        send_messages(f'Artifact Data File Not Found - Please check if you entered it correctly', 'input')
        fileerror = fileerror + 1
    else:
        send_messages(f'Processing hero data file {artifactDataFileName}', 'input')
    if os.path.exists(fribbelsDataFileName) == False:
        send_messages(f'Fribbels Data File Not Found - Please check if you entered it correctly', 'input')
        fileerror = fileerror + 1
    else:
        send_messages(f'Processing hero data file {fribbelsDataFileName}', 'input')
    if fileerror > 0:
        send_messages(f'ERROR: File issue occurred, please check log for details', 'input')
    else:
        with open(heroDataFileName, 'r') as hero_file:
            global hero_data
            hero_data = json.load(hero_file)
            send_messages(f'Hero Data Loaded: {len(hero_data)} rows found', 'input')
        with open(artifactDataFileName, 'r') as artifact_file:
            global artifact_data
            artifact_data = json.load(artifact_file)
            send_messages(f'Artifact Data Loaded: {len(artifact_data)} rows found', 'input')
        with open(fribbelsDataFileName, 'r') as player_file:
            global player_data
            player_data = json.load(player_file)
            send_messages(f'Fribbels Data Loaded: {len(player_data["heroes"])} heroes found. {len(player_data["items"])} items found. ', 'input')
        total_hero_count = len(player_data['heroes'])

        tableHeaders = ['Hero', 'Order', 'Skill 1', 'Skill 2', 'Skill 3', 'Reason for Issue']
        ui.heroViewList.setRowCount(0);
        ui.heroViewList.setRowCount(total_hero_count)
        ui.heroViewList.setColumnCount(6)
        ui.heroViewList.setSortingEnabled(1)
        ui.heroViewList.setHorizontalHeaderLabels(tableHeaders)
        badDataFont = QtGui.QFont('MS Shell Dlg 2', weight=99)
        badDataFont.setStrikeOut(1)
        badDataColor = QtGui.QColor('red')
        questionableColor = QtGui.QColor('orange')
        questionableFont = QtGui.QFont('MS Shell Dlg 2', weight=99)
        badDataFont.setStrikeOut(1)

        hero_iter = 0
        for hero in player_data['heroes']:
            name_object = QTableWidgetItem(str(hero['name']))
            if 'artifactName' not in hero:
                name_object.setForeground(questionableColor)
                name_object.setFont(questionableFont)
                error_object = QTableWidgetItem("No artifact equipped")
                error_object.setForeground(questionableColor)
                # Prevent editing errors
                error_object.setFlags(error_object.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                ui.heroViewList.setItem(hero_iter, 5, error_object)
            if len(hero['equipment']) < 6:
                name_object.setForeground(badDataColor)
                name_object.setFont(badDataFont)
                error_object = QTableWidgetItem("Less than 6 items")
                error_object.setForeground(badDataColor)
                # Prevent editing errors
                error_object.setFlags(error_object.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                ui.heroViewList.setItem(hero_iter, 5, error_object)

            # Prevent editing unit names
            name_object.setFlags(name_object.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
            ui.heroViewList.setItem(hero_iter, 0, name_object)
            hero_iter = hero_iter + 1
        ui.heroViewList.resizeColumnsToContents()
        send_messages(f'{total_hero_count} Heroes Loaded into table! Ready to go!', 'input')
        config_save()

# Start e7-infographic code
def find_character_image_id(name):
    """Return the id for a character on epicsevendb when provided their name """
    for character in hero_data:
        if character == name:
            return hero_data[character]['assets']
    return -1


def find_character_in_player_data(name):
    """Return the index within the player_data json for a character when provided their name """
    index = 0
    for character in player_data['heroes']:
        if character['name'] == name:
            return index
        index = index + 1
    return -1


def find_artifact_in_artifact_data(name):
    """Return the index within the artifact json for a artifact when provided their name """
    index = 0
    for artifact in artifact_data:
        if artifact == name:
            return index
        index = index + 1
    return -1

class MissingHeroError(Exception):
    """Could not find the hero requested in the data files"""
    pass


class NoHeroError(Exception):
    """Could not find the hero requested in the data files"""
    # sys.tracebacklimit = 0
    pass

def confirm_file(filename, url):
    """Check if file exists, if not download from url and save in correct location"""
    logging.info("Confirming if {} exists".format(filename))
    # nodl is used as an intentional exception upstream to replace a broken image with a question mark from assets
    if url != 'nodl':
        if not os.path.exists(filename):
            send_messages(f"Downloading {url}", 'output')
            r = requests.get(url)
            if r.status_code == 200:
                open(filename, 'wb').write(r.content)
            else:
                shutil.copy('assets/qm.png', filename)
    else:
        shutil.copy('assets/qm.png', filename)

def colour_image(img, colour):
    """Replace white-shades with RGB Colour provided"""
    recolour_image_data = []
    img_data = img.getdata()
    # Slow way of doing things for now - finds all pixels that are "white" and changes them to the identified colour
    for item in img_data:
        if item[0] in list(range(190, 256)):
            recolour_image_data.append(colour)
        else:
            recolour_image_data.append(item)
    img.putdata(recolour_image_data)
    return img

def get_character_data(name, artifact_name="Firm Shield", artifact_level=-1, skill_levels=None):
    """Build character data from within the herodata / autosave json, and return a dict with relevant data for image"""
    if skill_levels is [None, None, None] or None:
        skill_levels = ['?', '?', '?']
    send_messages(f'Looking for {name}', 'output')
    character_data = {}
    for character in hero_data:
        if character == name:
            logging.info(f'Getting data for {character}')
            base_rarity = hero_data[character]['rarity']
            devotion = hero_data[character]['devotion']
            self_devotion = hero_data[character]['self_devotion']
            assets = hero_data[character]['assets']
            db_api_id = remove_url_prefixes(hero_data[character]['assets']['thumbnail'])[:-6]
            if db_api_id[:44] == 'https://assets.epicsevendb.com/_source/face/':
                source_site = "epicsevendb"
            if db_api_id[:43] == 'https://raw.githubusercontent.com/fribbels/':
                source_site = "fribbels"

            logging.info('Getting data for ' + character + ' from player data')
            player_data_id = find_character_in_player_data(name)
            atk = player_data['heroes'][player_data_id]['atk']
            hp = player_data['heroes'][player_data_id]['hp']
            defence = player_data['heroes'][player_data_id]['def']
            cr = player_data['heroes'][player_data_id]['cr']
            cd = player_data['heroes'][player_data_id]['cd']
            eff = player_data['heroes'][player_data_id]['eff']
            res = player_data['heroes'][player_data_id]['res']
            dac = player_data['heroes'][player_data_id]['dac']
            spd = player_data['heroes'][player_data_id]['spd']
            ehp = player_data['heroes'][player_data_id]['ehp']
            dmg = player_data['heroes'][player_data_id]['dmg']
            dmgH = player_data['heroes'][player_data_id]['dmgh']
            score = player_data['heroes'][player_data_id]['score']
            hero_class = player_data['heroes'][player_data_id]['role']
            attribute = player_data['heroes'][player_data_id]['attribute']
            imprint = None
            imprint_team = ''
            imprint_team_val = ''
            imprint_team_1 = ''
            imprint_team_2 = ''
            imprint_team_3 = ''
            imprint_team_4 = ''
            imprint_solo = ''
            imprint_solo_val = ''
            imprint_value = ''
            if 'imprintNumber' in player_data['heroes'][player_data_id]:
                imprint_value = player_data['heroes'][player_data_id]['imprintNumber']
                for devotion_level in self_devotion['grades']:
                    # Handles the different cases where hero imprint data does not show up in json
                    if (imprint_value is not None) and (imprint_value != 'None') and (self_devotion['grades'][devotion_level] != 'None') and ( self_devotion['grades'][devotion_level] is not None) :
                        if int(round(self_devotion['grades'][devotion_level] * 100, 2)) == int(round(decimal.Decimal(imprint_value), 2)):
                            imprint = devotion_level
                            imprint_team = IMPRINT_LOOKUP[devotion['type']]
                            imprint_team_val = devotion['grades'][imprint]
                            imprint_team_1 = devotion['slots']["1"] # right
                            imprint_team_2 = devotion['slots']["2"] # bottom
                            imprint_team_3 = devotion['slots']["3"] # top
                            imprint_team_4 = devotion['slots']["4"] # left
                            imprint_solo = IMPRINT_LOOKUP[self_devotion['type']]
                            imprint_solo_val = self_devotion['grades'][imprint]

            # Firm shield is used as a placeholder to be replaced later to handle issues where artifact shows up weirdly in json
            if 'artifactName' in player_data['heroes'][player_data_id]:
                if player_data['heroes'][player_data_id]['artifactName'] is not None:
                    artifact_name = player_data['heroes'][player_data_id]['artifactName']
                else:
                    artifact_name = "Firm Shield"
            else:
                artifact_name = "Firm Shield"

            if 'artifactLevel' in player_data['heroes'][player_data_id]:
                if player_data['heroes'][player_data_id]['artifactLevel'] is not None:
                    artifact_level = player_data['heroes'][player_data_id]['artifactLevel']
                else:
                    artifact_level = -1
            else:
                artifact_level = -1

            artifact = artifact_data[artifact_name]
            artifact_image = artifact['assets']['icon']
            if attribute == 'wind':
                attribute = 'earth'

            if artifact['assets']['thumbnail'] != "https://raw.githubusercontent.com/fribbels/Fribbels-Epic-7-Optimizer/main/app/assets/blank.png":
                artifact_id = remove_url_prefixes(artifact['assets']['thumbnail'])[:-6]
            else:
                artifact_id = remove_url_prefixes(artifact['assets']['thumbnail'])[:-4]
            cp = player_data['heroes'][player_data_id]['cp']
            equipment = player_data['heroes'][player_data_id]['equipment']

            set_list = []
            for slot in EQUIP_LIST_ORDER:
                set_list.append(player_data['heroes'][player_data_id]['equipment'][slot]['set'])
            set_list = collections.Counter(set_list)
            sets = []
            for set_name in NEW_SET_LOOKUP_TABLE:
                if set_list[set_name] >= 2 * NEW_SET_LOOKUP_TABLE[set_name]:
                    sets.append(set_name)
                    sets.append(set_name)
                elif set_list[set_name] >= NEW_SET_LOOKUP_TABLE[set_name]:
                    sets.append(set_name)
            character_data = {
                'name': name,
                'atk': atk,
                'defence': defence,
                'hp': hp,
                'cr': cr,
                'cd': cd,
                'eff': eff,
                'res': res,
                'dac': dac,
                'spd': spd,
                'ehp': ehp,
                'dmg': dmg,
                'dmgH': dmgH,
                'score': score,
                'hero_class': hero_class,
                'attribute': attribute,
                'cp': cp,
                'equipment': equipment,
                'sets': sets,
                'base_rarity': base_rarity,
                'imprint':imprint or '',
                'imprint_team':imprint_team,
                'imprint_team_1':imprint_team_1,
                'imprint_team_2':imprint_team_2,
                'imprint_team_3':imprint_team_3,
                'imprint_team_4':imprint_team_4,
                'imprint_team_val': imprint_team_val,
                'imprint_solo':imprint_solo or '',
                'imprint_solo_val': imprint_solo_val or '',
                'devotion': devotion,
                'self_devotion': self_devotion,
                'assets': assets,
                'db_api_id': db_api_id,
                'artifact': artifact,
                'artifact_image': artifact_image,
                'artifact_id': artifact_id,
                'artifact_level': artifact_level,
                'skill_levels': skill_levels
            }
            logging.info("Found " + name)
    if character_data != {}:
        return character_data
    else:
        logging.error("Couldn't find " + name + " in herodata json. Usually this is because a new unit came out.")
        raise MissingHeroError(
            "Couldn't find " + name + " in herodata.json. Usually this is because a new unit came out. If this unit is already in Fribbels, typically you need to get a newer herodata.json.")

def remove_url_prefixes(string):
    """Format URLs to return character values by removing strings from the start of them"""
    string = string.removeprefix('https://assets.epicsevendb.com/_source/face/')
    string = string.removeprefix(
        "https://raw.githubusercontent.com/fribbels/Fribbels-Epic-7-Optimizer/main/data/cachedimages/")
    string = string.removeprefix('https://assets.epicsevendb.com/_source/item_arti/')
    return string

def make_character_image(character_data):
    """Build image for a character when provided a character_data json"""
    # This should really be broken down into smaller junks and allow for pieces to be put together for customisation
    # In the future, I guess!

    send_messages(f'Building image for {character_data["name"]}', 'output')

    # Create base image
    img = Image.new(mode='RGBA', size=(920, 175), color=(33, 37, 41, 255))
    d1 = ImageDraw.Draw(img)
    imprinton = Image.open('assets\\imprint-on.png').convert("RGBA").resize((15, 15))
    imprintoff = Image.open('assets\\imprint-off.png').convert("RGBA").resize((15, 15))

    # Hero image
    hero_image_file = remove_url_prefixes(character_data['assets']['thumbnail'])
    hero_image_file = remove_url_prefixes(hero_image_file)
    hero_image_file = 'images//' + hero_image_file
    confirm_file(hero_image_file, character_data['assets']['thumbnail'])
    im1 = Image.open(hero_image_file).convert("RGBA")
    im1 = trim(im1)
    img.paste(im1, (0, 35), im1)

    # Hero Skill Image Names
    hero_s1_image_file = 'images\\sk_' + character_data['db_api_id'] + '_1.png'
    hero_s2_image_file = 'images\\sk_' + character_data['db_api_id'] + '_2.png'
    hero_s3_image_file = 'images\\sk_' + character_data['db_api_id'] + '_3.png'
    hero_s1_url = 'https://assets.epicsevendb.com/_source/skill/sk_' + character_data['db_api_id'] + '_1.png'
    hero_s2_url = 'https://assets.epicsevendb.com/_source/skill/sk_' + character_data['db_api_id'] + '_2.png'
    hero_s3_url = 'https://assets.epicsevendb.com/_source/skill/sk_' + character_data['db_api_id'] + '_3.png'

    # Verify skill images exist, and get if not
    confirm_file(hero_s1_image_file, hero_s1_url)
    confirm_file(hero_s2_image_file, hero_s2_url)
    confirm_file(hero_s3_image_file, hero_s3_url)
    skill_image_list = [hero_s1_image_file, hero_s2_image_file, hero_s3_image_file]

    # Place skill images
    for index, skill_image in enumerate(skill_image_list):
        im1 = Image.open(skill_image).convert("RGBA")
        im1 = im1.resize((30, 30))
        img.paste(im1, (20 + 35 * index, 140), mask=im1)
        d1.text((30 + 35 * index, 126), '+' + str(character_data['skill_levels'][index]), font=FNT4, fill=FILL_WHITE)

    # Artifact image
    hero_artifact_image_url = character_data['artifact_image']
    # Hero Artifact Images
    # Catch a blank url and replace with ? symbol image
    if character_data['artifact_id'] == "https://raw.githubusercontent.com/fribbels/Fribbels-Epic-7-Optimizer/main/app/assets/blank":
        hero_artifact_image_file = 'images\\qm.png'
        hero_artifact_image_url = 'nodl'
    else:
        hero_artifact_image_file = 'images\\icon_art' + character_data['artifact_id'] + '.png'

    confirm_file(hero_artifact_image_file, hero_artifact_image_url)

    # Replace artifact if no artifact equipped
    if character_data['artifact']['name'] == 'Firm Shield':
        character_data['artifact']['name'] = 'Not Equipped'
        hero_artifact_image_file = 'assets\\qm.png'
        character_data['artifact_level'] = '?'

    # Artifact image + Text
    im1 = Image.open(hero_artifact_image_file).convert("RGBA")
    im1 = im1.resize((30, 30))
    d1.text((330, 135), "Artifact:", font=FNT3, fill=FILL_WHITE)
    d1.text((330, 160), f"{character_data['artifact']['name']} +{str(character_data['artifact_level'])}", font=FNT4, fill=FILL_WHITE)
    img.paste(im1, (390, 129), mask=im1)

    # Hero Name - different size font for longer names
    if len(character_data['name']) < 14:
        d1.text((35, 0), character_data['name'], font=FNT2, fill=FILL_WHITE)
    elif len(character_data['name']) < 20:
        d1.text((35, 10), character_data['name'], font=FN2SMALL, fill=FILL_WHITE)
    else:
        d1.text((35, 10), character_data['name'], font=FN2VSMALL, fill=FILL_WHITE)

    # Values used for easier adjustment/positioning
    # Height of a row, used as a multiplier
    data_height = 15
    # Initial height of Stat Panel Start
    start_height = 10
    # Position for start of attribute name
    stat_name_x = 210
    # Position for end of attribute value
    stat_value_x = 290
    # Currently unused, intended to be total size of panel holding stat and attribute
    panel_width = 150

    # Hero Stat Panel
    d1.text((stat_name_x, start_height), "Atk:", font=FNT, fill=FILL_WHITE)
    d1.text((stat_value_x, start_height), str(character_data['atk']), font=FNT, fill=FILL_WHITE, anchor="ra")
    d1.text((stat_name_x, start_height + 1 * data_height), "Def:", font=FNT, fill=FILL_WHITE)
    d1.text((stat_value_x, start_height + 1 * data_height), str(character_data['defence']), font=FNT, fill=FILL_WHITE,
            anchor="ra")
    d1.text((stat_name_x, start_height + 2 * data_height), "HP:", font=FNT, fill=FILL_WHITE)
    d1.text((stat_value_x, start_height + 2 * data_height), str(character_data['hp']), font=FNT, fill=FILL_WHITE,
            anchor="ra")
    d1.text((stat_name_x, start_height + 3 * data_height), "Spd:", font=FNT, fill=FILL_WHITE)
    d1.text((stat_value_x, start_height + 3 * data_height), str(character_data['spd']), font=FNT, fill=FILL_WHITE,
            anchor="ra")
    d1.text((stat_name_x, start_height + 4 * data_height), "Crit:", font=FNT, fill=FILL_WHITE)
    d1.text((stat_value_x, start_height + 4 * data_height),
            str(character_data['cr']) + '%/ ' + str(character_data['cd']) + '%', font=FNT, fill=FILL_WHITE, anchor="ra")
    d1.text((stat_name_x, start_height + 5 * data_height), "Eff:", font=FNT, fill=FILL_WHITE)
    d1.text((stat_value_x, start_height + 5 * data_height), str(character_data['eff']) + '%', font=FNT, fill=FILL_WHITE,
            anchor="ra")
    d1.text((stat_name_x, start_height + 6 * data_height), "Res:", font=FNT, fill=FILL_WHITE)
    d1.text((stat_value_x, start_height + 6 * data_height), str(character_data['res']) + '%', font=FNT, fill=FILL_WHITE,
            anchor="ra")
    d1.text((stat_name_x, start_height + 7 * data_height), "Dual:", font=FNT, fill=FILL_WHITE)
    d1.text((stat_value_x, start_height + 7 * data_height), str(character_data['dac'] + 5) + '%', font=FNT,
            fill=FILL_WHITE, anchor="ra")

    # Updated summary stat handling
    imprintValue = str(character_data['imprint'])
    if imprintValue is None or imprintValue == 'None' or imprintValue == '':
        imprintValue = '-'
    d1.text((445, start_height + 7.25 * data_height + 15), 'Imprint:', font=FNT3, fill=FILL_WHITE)
    d1.text((515, 125), imprintValue, font=FNT2, fill=FILL_WHITE)
    if imprintValue != '-':
        d1.text((515, 160), (f"({round(character_data['imprint_team_val']*100,2)}{character_data['imprint_team']} / {round(character_data['imprint_solo_val']*100,2)}{character_data['imprint_solo']})"), font=FNT4, fill=FILL_WHITE)
    d1.text((630, start_height + 7.25 * data_height + 15), "EHP:", font=FNT3, fill=FILL_WHITE)
    d1.text((670, start_height + 7.25 * data_height + 15), "{:,}".format(character_data['ehp']), font=FNT3,
            fill=FILL_WHITE)
    # d1.text((550, start_height + 7.25 * data_height + 40), "(effective hp)", font=FNT5, fill=FILL_WHITE)
    d1.text((730, start_height + 7.25 * data_height + 15), "DMG:", font=FNT3, fill=FILL_WHITE)
    d1.text((770, start_height + 7.25 * data_height + 15), "{:,}".format(character_data['dmg']), font=FNT3,
            fill=FILL_WHITE)
    d1.text((830, start_height + 7.25 * data_height + 15), "Total GS:", font=FNT3, fill=FILL_WHITE)
    d1.text((910, start_height + 7.25 * data_height + 15), str(character_data['score']), font=FNT3,
            fill=FILL_WHITE, anchor="ra")

    # Variables to handle whether or not imprints impact specific team slots
    if character_data['imprint_team_1'] == True:
        imprint_1 = imprinton
    else:
        imprint_1 = imprintoff
    if character_data['imprint_team_2'] == True:
        imprint_2 = imprinton
    else:
        imprint_2 = imprintoff

    if character_data['imprint_team_3'] == True:
        imprint_3 = imprinton
    else:
        imprint_3 = imprintoff

    if character_data['imprint_team_4'] == True:
        imprint_4 = imprinton
    else:
        imprint_4 = imprintoff

    img.paste(imprint_1, (585, 135), mask=imprint_1)
    img.paste(imprint_2, (575, 145), mask=imprint_2)
    img.paste(imprint_3, (575, 125), mask=imprint_3)
    img.paste(imprint_4, (565, 135), mask=imprint_4)

    # Place Hero Sets
    completed_sets = []
    for set in character_data['sets']:
        completed_sets.append('assets\\set' + set[:-3] + '.png')
    d1.text((170, start_height + 7.25 * data_height + 25), 'Sets:', font=FNT3, fill=FILL_WHITE)
    for index, set_image in enumerate(completed_sets):
        hero_set_image_x = 205 + index * 30
        hero_set_image_y = 140
        im1 = Image.open(set_image).convert("RGBA")
        im1 = im1.resize((30, 30))
        img.paste(im1, ((hero_set_image_x, hero_set_image_y)), mask=im1)

    # Recolour and resize of Class Image with Element
    class_image = 'assets/class' + character_data['hero_class'] + '.png'
    im1 = Image.open(class_image).convert("RGBA")
    elemental_colour = ELEMENT_COLOUR_LOOKUP_TABLE[character_data['attribute']]
    im1 = colour_image(im1, elemental_colour)
    im1 = im1.resize((30, 30))
    img.paste(im1, (0, 3), im1)

    # Item Stat Panel starts
    item_panel_start_x = 330
    item_panel_start_y = 10
    item_count = 0
    d1.line((item_panel_start_x + 100 * item_count, item_panel_start_y + 1 * data_height,
             item_panel_start_x + 100 * item_count + 700, item_panel_start_y + 1 * data_height))
    d1.line((item_panel_start_x + 100 * item_count, item_panel_start_y + 2.1 * data_height,
             item_panel_start_x + 100 * item_count + 700, item_panel_start_y + 2.1 * data_height))
    d1.line((item_panel_start_x + 100 * item_count, item_panel_start_y + 6.4 * data_height,
             item_panel_start_x + 100 * item_count + 700, item_panel_start_y + 6.4 * data_height))

    if len(character_data['equipment']) > 5:
        for slot in EQUIP_LIST_ORDER:
            set_image = ('assets\\' + character_data['equipment'][slot]['set'][-3:] + character_data['equipment'][slot][
                                                                                          'set'][:-3] + '.png').lower()
            im1 = Image.open(set_image).convert("RGBA")
            im1 = im1.resize(SET_IMAGE_SIZE)
            img.paste(im1, (item_panel_start_x + 15 + 100 * item_count + 20, item_panel_start_y - 5), im1)
            level = character_data['equipment'][slot]['level']
            enhance = character_data['equipment'][slot]['enhance']
            rarity = character_data['equipment'][slot]['rank']
            rarity_colour = RARITY_COLOUR_LOOKUP_TABLE[rarity]
            # Unused, may implement option to use words instead of images
            slot_name = slot
            main_stat_type = character_data['equipment'][slot]['main']['type']
            main_stat_type = STAT_LOOKUP_TABLE[main_stat_type]
            main_stat_value = character_data['equipment'][slot]['main']['value']

            # Equip Slot Images
            slot_image = 'assets\\gear' + slot + '.png'
            im1 = Image.open(slot_image).convert("RGBA")
            # Recolor Equipment Slot Image for Rarity
            im1 = im1.resize((20, 20))
            im1 = colour_image(im1, rarity_colour)
            img.paste(im1, (item_panel_start_x + 15 + 100 * item_count, item_panel_start_y - 5), im1)

            # Item Level / Enhancement Level
            d1.text((item_panel_start_x + 100 * item_count, item_panel_start_y), str(level), font=FNT, fill=FILL_WHITE)
            d1.text((item_panel_start_x + 60 + 100 * item_count, item_panel_start_y), '+' + str(enhance), font=FNT,
                    fill=FILL_WHITE)

            # Add % to mainstat string if necessary
            if "Percent" in str(character_data['equipment'][slot]['main']['type']):
                main_stat_value = str(main_stat_value) + '%'

            d1.text((item_panel_start_x + 100 * item_count, item_panel_start_y + 1 * data_height), str(main_stat_type),
                    font=FNT, fill=FILL_WHITE)
            d1.text((item_panel_start_x + 80 + 100 * item_count, item_panel_start_y + 1 * data_height),
                    str(main_stat_value), font=FNT, fill=FILL_WHITE, anchor="ra")

            # Iterate over substats in order
            substat_count = 0
            for substat in character_data['equipment'][slot]['substats']:
                substat_type = STAT_LOOKUP_TABLE[substat['type']]
                if 'modified' in substat:
                    substat_type = 'Ф' + STAT_LOOKUP_TABLE[substat['type']]
                # Rolls not currently used by may be used by future designs
                if 'rolls' in substat:
                    substat_rolls = substat['rolls']
                else:
                    substat_rolls = 0
                substat_value = substat['value']
                if "Percent" in str(substat['type']):
                    substat_value = str(substat_value) + '%'
                d1.text((item_panel_start_x + 100 * item_count, item_panel_start_y + (2.3 + substat_count) * data_height),
                        str(substat_type), font=FNT, fill=FILL_WHITE)
                d1.text(
                    (item_panel_start_x + 80 + 100 * item_count, item_panel_start_y + (2.3 + substat_count) * data_height),
                    str(substat_value), font=FNT, fill=FILL_WHITE, anchor="ra")
                substat_count = substat_count + 1

            d1.text((item_panel_start_x + 100 * item_count, item_panel_start_y + 6.4 * data_height),
                    'Gear Score:', font=FNT, fill=FILL_WHITE)
            d1.text((item_panel_start_x + 80 + 100 * item_count, item_panel_start_y + 6.4 * data_height),
                    str(character_data['equipment'][slot]['wss']), font=FNT, fill=FILL_WHITE, anchor="ra")
            item_count = item_count + 1
    else:
        send_messages(f'{character_data["name"]} does not have six items equipped.', 'output')
    return img

def make_multichar(character_list, filename):
    """Iteratively build and stack images using names from character_list and save into filename"""
    if ui.appDetailCheck.isChecked():
        bottom_tag_included = 0
    else:
        bottom_tag_included = 1
    if ui.previewCheck.isChecked():
        show_preview = 1
    else:
        show_preview = 0
    image_size = (920, 175 * (len(character_list)) + bottom_tag_included * 15)
    img = Image.new(mode='RGBA', size=(image_size), color=(33, 37, 41))

    send_messages(f"Gathering {(', ').join([char['name'] for char in character_list])}", 'output')
    for index, character in enumerate(character_list):
        character_data = get_character_data(character['name'], skill_levels=character['skill_enhance'])
        temp_image = make_character_image(character_data)
        date_suffix = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
        file_name = os.path.join(ui.outputLocationEdit.text(),f'{character["name"]}-{date_suffix}.png' )
        send_messages(f"{character['name']} image saved to {file_name}", 'output')
        temp_image.save(file_name)
        img.paste(temp_image, (0, index * 175), temp_image)
    send_messages(f'Group image saved to {filename}', 'output')
    bottom_tag = build_app_info_footer()
    if bottom_tag_included == 1:
        img.paste(bottom_tag, (0, (index+1) * 175), bottom_tag)
    if show_preview == 1:
        img.show()
    img.save(filename)
# End e7-infographic code

def build_app_info_footer():
    """Generates app info footer"""
    img = Image.new(mode='RGBA', size=(920, 15), color=(33, 37, 41))
    d1 = ImageDraw.Draw(img)
    d1.line([(0,0),(920,0)], width=1, fill=(200,200,200))
    msg = 'Image Generated by Otherworldly Machinery. Visit hhttps://github.com/zaprocalypse/otherworldly-machinery to make your own'
    w, h = d1.textsize(msg, font=FNT5)
    d1.text(((920-w)/2,2),msg, font=FNT5, fill=(200,200,200))
    return img

def goButton():
    '''Handles what happens when the GO! button is pressed'''
    rows = ui.heroViewList.rowCount()
    hero_val_list = []
    hero_list = []

    # Iterate over rows to get list of values from table, as that seems to be the only way in pygt6
    for row in range(rows):
        row_ig_value = ui.heroViewList.item(row, 1)
        if ui.heroViewList.item(row, 2) is not None:
            row_s1_enhance = ui.heroViewList.item(row, 2).text()
        else:
            row_s1_enhance = '?'
        if ui.heroViewList.item(row, 3) is not None:
            row_s2_enhance = ui.heroViewList.item(row, 3).text()
        else:
            row_s2_enhance = '?'
        if ui.heroViewList.item(row, 4) is not None:
            row_s3_enhance = ui.heroViewList.item(row, 4).text()
        else:
            row_s3_enhance = '?'
        if row_ig_value is not None:
            if row_ig_value.text().isnumeric():
                hero_val_list.append({'row_val':row, 'order':row_ig_value.text(), 'skill_enhance':[row_s1_enhance, row_s2_enhance, row_s3_enhance]})

    # Sort the list of dicts by the order value for the order for infographic
    # This actually means that you could use a lot of different values to sort by
    hero_val_list = sorted(hero_val_list, key=lambda x: int(x['order']))

    # Get the human-names for the heroes in the order from the previous list, and put them in a list
    for hero in hero_val_list:
        hero_list.append({'name':ui.heroViewList.item(hero['row_val'], 0).text(), 'skill_enhance': hero['skill_enhance']})

    # Confirm that we found a hero, and then send it off to the image generator
    if len(hero_list) > 0:
        send_messages('Config looks good! Now Generating files!', 'output')
        filename = os.path.join(ui.outputLocationEdit.text(), f'output-{datetime.datetime.now().strftime("%Y-%m-%d-%H%M")}.png')
        make_multichar(hero_list, filename)
    else:
        ui.outputLogText.appendPlainText('No units were numbered for image generation')


def config_load():
    '''Load app configuration from json, and trigger any data loads from data jsons'''
    with open(config_file, 'r') as config_json:
        saved_config = json.loads(config_json.read())
        ui.heroDataEdit.setText(saved_config['herodata.json'])
        ui.artifactDataEdit.setText(saved_config['artifactdata.json'])
        ui.fribbelsDataEdit.setText(saved_config['fribbels.json'])
        ui.outputLocationEdit.setText(saved_config['output'])
        ui.appDetailCheck.setChecked(saved_config['footer'])
        ui.previewCheck.setChecked(saved_config['preview'])
        ui.darkModeCheck.setChecked(saved_config['dark'])
        loadFileData(saved_config['herodata.json'], saved_config['artifactdata.json'], saved_config['fribbels.json'])


def config_save():
    '''Save app configurations to json'''
    json_save_dict = {
        "herodata.json": ui.heroDataEdit.text(),
        "artifactdata.json": ui.artifactDataEdit.text() ,
        "fribbels.json": ui.fribbelsDataEdit.text(),
        "dark": ui.darkModeCheck.isChecked(),
        "output": ui.outputLocationEdit.text(),
        "preview": ui.previewCheck.isChecked(),
        "footer": ui.appDetailCheck.isChecked(),
    }
    with open(config_file, 'w') as config_json:
        json.dump(json_save_dict, config_json)

def boldening():
    '''Bolds a bunch of elements that for some reason don't bold properly from the ui file'''
    boldFont = QtGui.QFont('MS Shell Dlg 2', weight=99)
    boldFont.setBold(True)
    ui.herodataLabel.setFont(boldFont)
    ui.artifactdataLabel.setFont(boldFont)
    ui.fribbelsLabel.setFont(boldFont)
    ui.outputLocationLabel.setFont(boldFont)
    ui.herodataLabel.setFont(boldFont)
    ui.loadFileDataButton.setFont(boldFont)
    ui.saveConfigButton.setFont(boldFont)
    ui.goButton.setFont(boldFont)

def toggle_dark_style():
    '''Toggles the styling of the app to use a dark style or return to a default style'''
    global style_state
    if style_state == 'light':
        with open('styles.qss', 'r') as f:
            style = f.read()
            # Set the stylesheet of the application

            app.setStyleSheet(style)
            style_state = 'dark'
    else:
        app.setStyleSheet(base_style)
        style_state = 'light'
    boldening()

def toggle_bad_units_visible():
    '''Hide units with issues from table'''
    if ui.hideBadCheckBox.isChecked():
        for i in range(0, ui.heroViewList.rowCount()):
            item = ui.heroViewList.item(i,5)
            if item is not None:
                ui.heroViewList.hideRow(i)
    else:
        for i in range(0, ui.heroViewList.rowCount()):
            item = ui.heroViewList.item(i,5)
            if item is not None:
                ui.heroViewList.showRow(i)

def trim(im):
    '''Do some automagic to try to trim images to fit. Sometimes fails to do so, and will return image as is'''
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    else:
        return im


def open_link(url):
    '''Open url in default browser for device'''
    webbrowser.open(url)

def except_hook(cls, exception, traceback_val):
    '''Handles exceptions in a way that makes more sense than the qt6 default, and logs'''
    sys.__excepthook__(cls, exception, traceback_val)
    send_messages(f'An error occured', 'output')
    send_messages(f'{traceback.format_tb(traceback_val)[-1]}', 'output')
    send_messages(f'{cls} {exception}', 'output')
    send_messages(f'An error occured', 'input')
    send_messages(f'{traceback.format_tb(traceback_val)[-1]}', 'input')
    send_messages(f'{cls} {exception}', 'input')

def ui_setup():
    '''Setting up UI configuration and connecting UI elements to functions'''
    ui.outputLogText.setPlainText('Setup your heroes on the Hero Picker tab, configure above - and then click the giant Go! button!')
    ui.outputLogText.setReadOnly(1)
    ui.goButton.clicked.connect(lambda:goButton())
    ui.herodataButton.clicked.connect(lambda: fileInputDialogButton('herodataButton'))
    ui.artifactdataButton.clicked.connect(lambda: fileInputDialogButton('artifactDataButton'))
    ui.fribbelsButton.clicked.connect(lambda: fileInputDialogButton('fribbelsButton'))
    ui.outputLocationButton.clicked.connect(lambda: fileOutputDialogButton('outputLocationButton'))
    ui.saveConfigButton.clicked.connect(lambda: config_save())
    config_load()
    if ui.darkModeCheck.isChecked():
        toggle_dark_style()
    ui.darkModeCheck.stateChanged.connect(lambda: toggle_dark_style())
    ui.actionAbout.setShortcut('F1')
    ui.actionAbout.triggered.connect(lambda: open_link('https://github.com/zaprocalypse/e7-infographic'))
    ui.actionExit.setShortcut('Ctrl+Q')
    ui.actionExit.triggered.connect(lambda: app.quit())
    ui.hideBadCheckBox.stateChanged.connect(lambda: toggle_bad_units_visible())
    ui.loadFileDataButton.clicked.connect(lambda: loadFileData(ui.heroDataEdit.text(), ui.artifactDataEdit.text(),ui.fribbelsDataEdit.text()))
    # For some reason the ui does not bold properly from the ui_def file. This is a hacky fix for now.
    boldening()

# Config Filename
config_file = 'config.json'

# PYQT6 Handling Code
app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowIcon(QtGui.QIcon('assets/app_icon.png'))
ui = Ui_MainWindow()
ui.setupUi(window)
style_state = 'light'
# Base style is stored for switching back from dark mode - light mode set as default
base_style = app.styleSheet()
# Data Objects (will make this nicer in the future)
hero_data = []
player_data = []
artifact_data = []

ui_setup()




# PYQT6 Handling Code
window.show()
sys.excepthook = except_hook
sys.exit(app.exec())

