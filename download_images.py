#!/usr/bin/env python3
"""
Elden Ring Tracker — Image Downloader
=======================================
Scarica tutte le immagini degli item da eldenring.wiki.gg
e le salva in images/<categoria>/<nome>.png

Uso:
  pip install requests
  python3 download_images.py

Poi carica la cartella images/ su GitHub insieme agli HTML.
"""

import os, time, urllib.request, urllib.error, sys

WIKI_BASE = "https://eldenring.wiki.gg/images/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://eldenring.wiki.gg/',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

# ── Mappatura slug → filename wiki.gg ────────────────────────────────────────
# Formato: ER_Icon_<Categoria>_<Nome con underscore>.png
# Categoria: Talisman, Weapon, Armor, Incantation, Sorcery, SpiritAsh, Shield

ITEMS = {
'talismans': {
  'ancestral_spirits_horn_talisman':        'ER_Icon_Talisman_Ancestral_Spirit\'s_Horn.png',
  'arrows_reach_talisman':                  'ER_Icon_Talisman_Arrow\'s_Reach_Talisman.png',
  'arrows_soaring_sting_talisman':          'ER_Icon_Talisman_Arrow\'s_Soaring_Sting_Talisman.png',
  'arsenal_charm_talisman':                 'ER_Icon_Talisman_Arsenal_Charm.png',
  'arsenal_charm_1_talisman':               'ER_Icon_Talisman_Arsenal_Charm+1.png',
  'assassins_cerulean_dagger_talisman':     'ER_Icon_Talisman_Assassin\'s_Cerulean_Dagger.png',
  'assassins_crimson_dagger_talisman':      'ER_Icon_Talisman_Assassin\'s_Crimson_Dagger.png',
  'axe_talisman':                           'ER_Icon_Talisman_Axe_Talisman.png',
  'beloved_stardust_talisman':              'ER_Icon_Talisman_Beloved_Stardust.png',
  'blade_of_mercy_talisman':                'ER_Icon_Talisman_Blade_of_Mercy.png',
  'blessed_blue_dew_talisman':              'ER_Icon_Talisman_Blessed_Blue_Dew_Talisman.png',
  'blessed_dew_talisman':                   'ER_Icon_Talisman_Blessed_Dew_Talisman.png',
  'blue_dancer_charm_talisman':             'ER_Icon_Talisman_Blue_Dancer_Charm.png',
  'boltdrake_talisman':                     'ER_Icon_Talisman_Boltdrake_Talisman.png',
  'boltdrake_talisman_1':                   'ER_Icon_Talisman_Boltdrake_Talisman+1.png',
  'boltdrake_talisman_2':                   'ER_Icon_Talisman_Boltdrake_Talisman+2.png',
  'boltdrake_talisman_3':                   'ER_Icon_Talisman_Boltdrake_Talisman+3.png',
  'bull-goats_talisman':                    'ER_Icon_Talisman_Bull-Goat\'s_Talisman.png',
  'cerulean_amber_medallion_talisman':      'ER_Icon_Talisman_Cerulean_Amber_Medallion.png',
  'cerulean_amber_medallion_1_talisman':    'ER_Icon_Talisman_Cerulean_Amber_Medallion+1.png',
  'cerulean_amber_medallion_2_talisman':    'ER_Icon_Talisman_Cerulean_Amber_Medallion+2.png',
  'cerulean_amber_medallion_3_talisman':    'ER_Icon_Talisman_Cerulean_Amber_Medallion+3.png',
  'cerulean_seed_talisman':                 'ER_Icon_Talisman_Cerulean_Seed_Talisman.png',
  'cerulean_seed_talisman_1':               'ER_Icon_Talisman_Cerulean_Seed_Talisman+1.png',
  'claw_talisman':                          'ER_Icon_Talisman_Claw_Talisman.png',
  'concealing_veil_talisman':               'ER_Icon_Talisman_Concealing_Veil.png',
  'crimson_amber_medallion_talisman':       'ER_Icon_Talisman_Crimson_Amber_Medallion.png',
  'crimson_amber_medallion_1_talisman':     'ER_Icon_Talisman_Crimson_Amber_Medallion+1.png',
  'crimson_amber_medallion_2_talisman':     'ER_Icon_Talisman_Crimson_Amber_Medallion+2.png',
  'crimson_amber_medallion_3_talisman':     'ER_Icon_Talisman_Crimson_Amber_Medallion+3.png',
  'crimson_seed_talisman':                  'ER_Icon_Talisman_Crimson_Seed_Talisman.png',
  'crimson_seed_talisman_1':                'ER_Icon_Talisman_Crimson_Seed_Talisman+1.png',
  'crusade_insignia_talisman':              'ER_Icon_Talisman_Crusade_Insignia.png',
  'dagmar_greatshield_talisman':            'ER_Icon_Talisman_Dagmar_Greatshield_Talisman.png',
  'dragoncrest_greatshield_talisman':       'ER_Icon_Talisman_Dragoncrest_Greatshield_Talisman.png',
  'dragoncrest_shield_talisman':            'ER_Icon_Talisman_Dragoncrest_Shield_Talisman.png',
  'dragoncrest_shield_talisman_1':          'ER_Icon_Talisman_Dragoncrest_Shield_Talisman+1.png',
  'dragoncrest_shield_talisman_2':          'ER_Icon_Talisman_Dragoncrest_Shield_Talisman+2.png',
  'dried_bouquet_talisman':                 'ER_Icon_Talisman_Dried_Bouquet.png',
  'erdtrees_favor_talisman':                'ER_Icon_Talisman_Erdtree\'s_Favor.png',
  'erdtrees_favor_1_talisman':              'ER_Icon_Talisman_Erdtree\'s_Favor+1.png',
  'erdtrees_favor_2_talisman':              'ER_Icon_Talisman_Erdtree\'s_Favor+2.png',
  'fine_crucible_feather_talisman':         'ER_Icon_Talisman_Fine_Crucible_Feather_Talisman.png',
  'flamedrake_talisman':                    'ER_Icon_Talisman_Flamedrake_Talisman.png',
  'flamedrake_talisman_1':                  'ER_Icon_Talisman_Flamedrake_Talisman+1.png',
  'flamedrake_talisman_2':                  'ER_Icon_Talisman_Flamedrake_Talisman+2.png',
  'flamedrake_talisman_3':                  'ER_Icon_Talisman_Flamedrake_Talisman+3.png',
  'flocks_canvas_talisman':                 'ER_Icon_Talisman_Flock\'s_Canvas_Talisman.png',
  'godfrey_icon_talisman':                  'ER_Icon_Talisman_Godfrey_Icon.png',
  'godskin_swaddling_cloth_talisman':       'ER_Icon_Talisman_Godskin_Swaddling_Cloth.png',
  'gold_scarab_talisman':                   'ER_Icon_Talisman_Gold_Scarab.png',
  'golden_braid_talisman':                  'ER_Icon_Talisman_Golden_Braid.png',
  'graven-mass_talisman':                   'ER_Icon_Talisman_Graven-Mass_Talisman.png',
  'graven-school_talisman':                 'ER_Icon_Talisman_Graven-School_Talisman.png',
  'great-jars_arsenal_talisman':            'ER_Icon_Talisman_Great-Jar\'s_Arsenal.png',
  'green_turtle_talisman':                  'ER_Icon_Talisman_Green_Turtle_Talisman.png',
  'haligdrake_talisman':                    'ER_Icon_Talisman_Haligdrake_Talisman.png',
  'haligdrake_talisman_1':                  'ER_Icon_Talisman_Haligdrake_Talisman+1.png',
  'haligdrake_talisman_2':                  'ER_Icon_Talisman_Haligdrake_Talisman+2.png',
  'kindred_of_rots_exultation_talisman':    'ER_Icon_Talisman_Kindred_of_Rot\'s_Exultation.png',
  'lacerating_crossed-tree_talisman':       'ER_Icon_Talisman_Lacerating_Crossed-Tree.png',
  'lord_of_bloods_exultation_talisman':     'ER_Icon_Talisman_Lord_of_Blood\'s_Exultation.png',
  'magic_scorpion_charm_talisman':          'ER_Icon_Talisman_Magic_Scorpion_Charm.png',
  'marikas_scarseal_talisman':              'ER_Icon_Talisman_Marika\'s_Scarseal.png',
  'marikas_soreseal_talisman':              'ER_Icon_Talisman_Marika\'s_Soreseal.png',
  'millicents_prosthesis_talisman':         'ER_Icon_Talisman_Millicent\'s_Prosthesis.png',
  'moon_of_nokstella_talisman':             'ER_Icon_Talisman_Moon_of_Nokstella.png',
  'mottled_necklace_talisman':              'ER_Icon_Talisman_Mottled_Necklace.png',
  'mottled_necklace_1_talisman':            'ER_Icon_Talisman_Mottled_Necklace+1.png',
  'mottled_necklace_2_talisman':            'ER_Icon_Talisman_Mottled_Necklace+2.png',
  'old_lords_talisman':                     'ER_Icon_Talisman_Old_Lord\'s_Talisman.png',
  'outer_god_heirloom_talisman':            'ER_Icon_Talisman_Outer_God_Heirloom.png',
  'pearl_shield_talisman':                  'ER_Icon_Talisman_Pearl_Shield_Talisman.png',
  'pearldrake_talisman':                    'ER_Icon_Talisman_Pearldrake_Talisman.png',
  'pearldrake_talisman_1':                  'ER_Icon_Talisman_Pearldrake_Talisman+1.png',
  'pearldrake_talisman_2':                  'ER_Icon_Talisman_Pearldrake_Talisman+2.png',
  'pearldrake_talisman_3':                  'ER_Icon_Talisman_Pearldrake_Talisman+3.png',
  'prosthesis-wearer_heirloom_talisman':    'ER_Icon_Talisman_Prosthesis-Wearer_Heirloom.png',
  'radagon_icon_talisman':                  'ER_Icon_Talisman_Radagon_Icon.png',
  'radagons_scarseal_talisman':             'ER_Icon_Talisman_Radagon\'s_Scarseal.png',
  'radagons_soreseal_talisman':             'ER_Icon_Talisman_Radagon\'s_Soreseal.png',
  'red-feathered_branchsword_talisman':     'ER_Icon_Talisman_Red-Feathered_Branchsword.png',
  'rellanas_cameo_talisman':                'ER_Icon_Talisman_Rellana\'s_Cameo.png',
  'retaliatory_crossed-tree_talisman':      'ER_Icon_Talisman_Retaliatory_Crossed-Tree.png',
  'ritual_shield_talisman':                 'ER_Icon_Talisman_Ritual_Shield_Talisman.png',
  'ritual_sword_talisman':                  'ER_Icon_Talisman_Ritual_Sword_Talisman.png',
  'sacred_scorpion_charm_talisman':         'ER_Icon_Talisman_Sacred_Scorpion_Charm.png',
  'shabriris_woe_talisman':                 'ER_Icon_Talisman_Shabriri\'s_Woe.png',
  'shard_of_alexander_talisman':            'ER_Icon_Talisman_Shard_of_Alexander.png',
  'sharpshot_talisman':                     'ER_Icon_Talisman_Sharpshot_Talisman.png',
  'silver_scarab_talisman':                 'ER_Icon_Talisman_Silver_Scarab.png',
  'smithing_talisman':                      'ER_Icon_Talisman_Smithing_Talisman.png',
  'spear_talisman':                         'ER_Icon_Talisman_Spear_Talisman.png',
  'spelldrake_talisman':                    'ER_Icon_Talisman_Spelldrake_Talisman.png',
  'spelldrake_talisman_1':                  'ER_Icon_Talisman_Spelldrake_Talisman+1.png',
  'spelldrake_talisman_2':                  'ER_Icon_Talisman_Spelldrake_Talisman+2.png',
  'spelldrake_talisman_3':                  'ER_Icon_Talisman_Spelldrake_Talisman+3.png',
  'st_trinas_smile_talisman':               'ER_Icon_Talisman_St._Trina\'s_Smile.png',
  'stalwart_horn_charm_talisman':           'ER_Icon_Talisman_Stalwart_Horn_Charm.png',
  'stalwart_horn_charm_1_talisman':         'ER_Icon_Talisman_Stalwart_Horn_Charm+1.png',
  'stalwart_horn_charm_2_talisman':         'ER_Icon_Talisman_Stalwart_Horn_Charm+2.png',
  'stargazer_heirloom_talisman':            'ER_Icon_Talisman_Stargazer_Heirloom.png',
  'starscourge_heirloom_talisman':          'ER_Icon_Talisman_Starscourge_Heirloom.png',
  'talisman_of_all_crucibles_talisman':     'ER_Icon_Talisman_Talisman_of_All_Crucibles.png',
  'talisman_of_lords_bestowal_talisman':    'ER_Icon_Talisman_Talisman_of_Lord\'s_Bestowal.png',
  'takers_cameo_talisman':                  'ER_Icon_Talisman_Taker\'s_Cameo.png',
  'two_fingers_heirloom_talisman':          'ER_Icon_Talisman_Two_Fingers_Heirloom.png',
  'two-handed_sword_talisman':              'ER_Icon_Talisman_Two-Handed_Sword_Talisman.png',
  'two-headed_turtle_talisman':             'ER_Icon_Talisman_Two-Headed_Turtle_Talisman.png',
  'verdigris_discus_talisman':              'ER_Icon_Talisman_Verdigris_Discus.png',
  'viridian_amber_medallion_talisman':      'ER_Icon_Talisman_Viridian_Amber_Medallion.png',
  'viridian_amber_medallion_1_talisman':    'ER_Icon_Talisman_Viridian_Amber_Medallion+1.png',
  'viridian_amber_medallion_2_talisman':    'ER_Icon_Talisman_Viridian_Amber_Medallion+2.png',
  'viridian_amber_medallion_3_talisman':    'ER_Icon_Talisman_Viridian_Amber_Medallion+3.png',
  'warrior_jar_shard_talisman':             'ER_Icon_Talisman_Warrior_Jar_Shard.png',
  'white-feathered_branchsword_talisman':   'ER_Icon_Talisman_White-Feathered_Branchsword.png',
  'winged_sword_insignia_talisman':         'ER_Icon_Talisman_Winged_Sword_Insignia.png',
},
'weapons': {
  'blasphemous_blade_greatsword_weapon':                  'ER_Icon_Weapon_Blasphemous_Blade.png',
  'black_knife_dagger_weapon':                            'ER_Icon_Weapon_Black_Knife.png',
  'bloodhounds_fang_curved_greatsword_weapon':            'ER_Icon_Weapon_Bloodhound\'s_Fang.png',
  'bolt_of_gransax_spear_weapon':                         'ER_Icon_Weapon_Bolt_of_Gransax.png',
  'claymore_greatsword_weapon':                           'ER_Icon_Weapon_Claymore.png',
  'coded_sword_straight_sword_weapon':                    'ER_Icon_Weapon_Coded_Sword.png',
  'commanders_standard_halberd_weapon':                   'ER_Icon_Weapon_Commander\'s_Standard.png',
  'cross-naginata_spear_weapon':                          'ER_Icon_Weapon_Cross-Naginata.png',
  'deaths_poker_greatsword_weapon':                       'ER_Icon_Weapon_Death\'s_Poker.png',
  'dragon_kings_cragblade_heavy_thrusting_sword_weapon':  'ER_Icon_Weapon_Dragon_King\'s_Cragblade.png',
  'dragonscale_blade_katana_weapon':                      'ER_Icon_Weapon_Dragonscale_Blade.png',
  'eclipse_shotel_curved_sword_weapon':                   'ER_Icon_Weapon_Eclipse_Shotel.png',
  'fallingstar_beast_jaw_colossal_weapon_weapon':         'ER_Icon_Weapon_Fallingstar_Beast_Jaw.png',
  'flamberge_greatsword_weapon':                          'ER_Icon_Weapon_Flamberge.png',
  'godslayers_greatsword_colossal_sword_weapon':          'ER_Icon_Weapon_Godslayer\'s_Greatsword.png',
  'golden_order_greatsword_weapon':                       'ER_Icon_Weapon_Golden_Order_Greatsword.png',
  'grafted_blade_greatsword_colossal_sword_weapon':       'ER_Icon_Weapon_Grafted_Blade_Greatsword.png',
  'greatsword_colossal_sword_weapon':                     'ER_Icon_Weapon_Greatsword.png',
  'hand_of_malenia_katana_weapon':                        'ER_Icon_Weapon_Hand_of_Malenia.png',
  'loretta_war_sickle_halberd_weapon':                    'ER_Icon_Weapon_Loretta\'s_War_Sickle.png',
  'malikeths_black_blade_colossal_sword_weapon':          'ER_Icon_Weapon_Maliketh\'s_Black_Blade.png',
  'marais_executioners_sword_colossal_sword_weapon':      'ER_Icon_Weapon_Marais_Executioner\'s_Sword.png',
  'meteoric_ore_blade_katana_weapon':                     'ER_Icon_Weapon_Meteoric_Ore_Blade.png',
  'misericorde_dagger_weapon':                            'ER_Icon_Weapon_Misericorde.png',
  'mohgwyns_sacred_spear_weapon':                         'ER_Icon_Weapon_Mohgwyn\'s_Sacred_Spear.png',
  'moonveil_katana_weapon':                               'ER_Icon_Weapon_Moonveil.png',
  'morgotts_cursed_sword_curved_greatsword_weapon':       'ER_Icon_Weapon_Morgott\'s_Cursed_Sword.png',
  'nagakiba_katana_weapon':                               'ER_Icon_Weapon_Nagakiba.png',
  'reduvia_dagger_weapon':                                'ER_Icon_Weapon_Reduvia.png',
  'rivers_of_blood_katana_weapon':                        'ER_Icon_Weapon_Rivers_of_Blood.png',
  'ruins_greatsword_colossal_sword_weapon':               'ER_Icon_Weapon_Ruins_Greatsword.png',
  'sacred_relic_sword_greatsword_weapon':                 'ER_Icon_Weapon_Sacred_Relic_Sword.png',
  'starscourge_greatsword_colossal_sword_weapon':         'ER_Icon_Weapon_Starscourge_Greatsword.png',
  'sword_of_night_and_flame_straight_sword_weapon':       'ER_Icon_Weapon_Sword_of_Night_and_Flame.png',
  'treespear_spear_weapon':                               'ER_Icon_Weapon_Treespear.png',
  'uchigatana_katana_weapon':                             'ER_Icon_Weapon_Uchigatana.png',
  'winged_scythe_reaper_weapon':                          'ER_Icon_Weapon_Winged_Scythe.png',
  'euporia_twinblade_weapon':                             'ER_Icon_Weapon_Euporia.png',
  'sword_of_night_straight_sword_weapon':                 'ER_Icon_Weapon_Sword_of_Night.png',
},
'armor': {
  'answbachs_helm_armor_elden_ring_wiki':         'ER_Icon_Armor_Ansbach\'s_Helm.png',
  'answbachs_armor_elden_ring_wiki':              'ER_Icon_Armor_Ansbach\'s_Armor.png',
  'answbachs_gauntlets_armor_elden_ring_wiki':    'ER_Icon_Armor_Ansbach\'s_Gauntlets.png',
  'answbachs_greaves_armor_elden_ring_wiki':      'ER_Icon_Armor_Ansbach\'s_Greaves.png',
  'black_knife_hood_armor_elden_ring_wiki':       'ER_Icon_Armor_Black_Knife_Hood.png',
  'black_knife_armor_elden_ring_wiki':            'ER_Icon_Armor_Black_Knife_Armor.png',
  'black_knife_gauntlets_armor_elden_ring_wiki':  'ER_Icon_Armor_Black_Knife_Gauntlets.png',
  'black_knife_greaves_armor_elden_ring_wiki':    'ER_Icon_Armor_Black_Knife_Greaves.png',
  'blaids_helm_armor_elden_ring_wiki':            'ER_Icon_Armor_Blaidd\'s_Helm.png',
  'blaids_armor_elden_ring_wiki':                 'ER_Icon_Armor_Blaidd\'s_Armor.png',
  'blaids_gauntlets_armor_elden_ring_wiki':       'ER_Icon_Armor_Blaidd\'s_Gauntlets.png',
  'blaids_greaves_armor_elden_ring_wiki':         'ER_Icon_Armor_Blaidd\'s_Greaves.png',
  'bull-goat_helm_armor_elden_ring_wiki':         'ER_Icon_Armor_Bull-Goat_Helm.png',
  'bull-goat_armor_elden_ring_wiki':              'ER_Icon_Armor_Bull-Goat_Armor.png',
  'bull-goat_gauntlets_armor_elden_ring_wiki':    'ER_Icon_Armor_Bull-Goat_Gauntlets.png',
  'bull-goat_greaves_armor_elden_ring_wiki':      'ER_Icon_Armor_Bull-Goat_Greaves.png',
  'crucible_axe_helm_armor_elden_ring_wiki':      'ER_Icon_Armor_Crucible_Axe_Helm.png',
  'crucible_axe_armor_elden_ring_wiki':           'ER_Icon_Armor_Crucible_Axe_Armor.png',
  'crucible_axe_gauntlets_armor_elden_ring_wiki': 'ER_Icon_Armor_Crucible_Axe_Gauntlets.png',
  'crucible_axe_greaves_armor_elden_ring_wiki':   'ER_Icon_Armor_Crucible_Axe_Greaves.png',
  'fire_knight_helm_armor_elden_ring_wiki':       'ER_Icon_Armor_Fire_Knight_Helm.png',
  'fire_knight_armor_elden_ring_wiki':            'ER_Icon_Armor_Fire_Knight_Armor.png',
  'fire_knight_gauntlets_armor_elden_ring_wiki':  'ER_Icon_Armor_Fire_Knight_Gauntlets.png',
  'fire_knight_greaves_armor_elden_ring_wiki':    'ER_Icon_Armor_Fire_Knight_Greaves.png',
  'malenias_helm_armor_elden_ring_wiki':          'ER_Icon_Armor_Malenia\'s_Helm.png',
  'malenias_armor_elden_ring_wiki':               'ER_Icon_Armor_Malenia\'s_Armor.png',
  'malenias_gauntlet_armor_elden_ring_wiki':      'ER_Icon_Armor_Malenia\'s_Gauntlet.png',
  'malenias_greaves_armor_elden_ring_wiki':       'ER_Icon_Armor_Malenia\'s_Greaves.png',
  'raging_wolf_helm_armor_elden_ring_wiki':       'ER_Icon_Armor_Raging_Wolf_Helm.png',
  'raging_wolf_armor_elden_ring_wiki':            'ER_Icon_Armor_Raging_Wolf_Armor.png',
  'raging_wolf_gauntlets_armor_elden_ring_wiki':  'ER_Icon_Armor_Raging_Wolf_Gauntlets.png',
  'raging_wolf_greaves_armor_elden_ring_wiki':    'ER_Icon_Armor_Raging_Wolf_Greaves.png',
  'radahns_lion_helm_armor_elden_ring_wiki':      'ER_Icon_Armor_Radahn\'s_Lion_Helm.png',
  'radahns_lion_armor_elden_ring_wiki':           'ER_Icon_Armor_Radahn\'s_Lion_Armor.png',
  'veterans_helm_armor_elden_ring_wiki':          'ER_Icon_Armor_Veteran\'s_Helm.png',
  'veterans_armor_elden_ring_wiki':               'ER_Icon_Armor_Veteran\'s_Armor.png',
  'veterans_gauntlets_armor_elden_ring_wiki':     'ER_Icon_Armor_Veteran\'s_Gauntlets.png',
  'veterans_greaves_armor_elden_ring_wiki':       'ER_Icon_Armor_Veteran\'s_Greaves.png',
  'white_reed_helm_armor_elden_ring_wiki':        'ER_Icon_Armor_White_Reed_Helm.png',
  'white_reed_armor_elden_ring_wiki':             'ER_Icon_Armor_White_Reed_Armor.png',
  'white_reed_gauntlets_armor_elden_ring_wiki':   'ER_Icon_Armor_White_Reed_Gauntlets.png',
  'white_reed_greaves_armor_elden_ring_wiki':     'ER_Icon_Armor_White_Reed_Greaves.png',
},
'sorceries': {
  'adulas_moonblade_sorcery_elden_ring_wiki_guide':             'ER_Icon_Sorcery_Adula\'s_Moonblade.png',
  'cannon_of_haima_sorcery_elden_ring_wiki_guide':              'ER_Icon_Sorcery_Cannon_of_Haima.png',
  'carian_greatsword_sorcery_elden_ring_wiki_guide':            'ER_Icon_Sorcery_Carian_Greatsword.png',
  'carian_phalanx_sorcery_elden_ring_wiki_guide':               'ER_Icon_Sorcery_Carian_Phalanx.png',
  'carian_piercer_sorcery_elden_ring_wiki_guide':               'ER_Icon_Sorcery_Carian_Piercer.png',
  'carian_retaliation_sorcery_elden_ring_wiki_guide':           'ER_Icon_Sorcery_Carian_Retaliation.png',
  'carian_slicer_sorcery_elden_ring_wiki_guide':                'ER_Icon_Sorcery_Carian_Slicer.png',
  'comet_sorcery_elden_ring_wiki_guide':                        'ER_Icon_Sorcery_Comet.png',
  'comet_azur_sorcery_elden_ring_wiki_guide':                   'ER_Icon_Sorcery_Comet_Azur.png',
  'crystal_torrent_sorcery_elden_ring_wiki_guide':              'ER_Icon_Sorcery_Crystal_Torrent.png',
  'eternal_darkness_sorcery_elden_ring_wiki_guide':             'ER_Icon_Sorcery_Eternal_Darkness.png',
  'founding_rain_of_stars_sorcery_elden_ring_wiki_guide':       'ER_Icon_Sorcery_Founding_Rain_of_Stars.png',
  'freezing_mist_sorcery_elden_ring_wiki_guide':                'ER_Icon_Sorcery_Freezing_Mist.png',
  'full_moon_of_nokstella_sorcery_elden_ring_wiki_guide':       'ER_Icon_Sorcery_Full_Moon_of_Nokstella.png',
  'gavel_of_haima_sorcery_elden_ring_wiki_guide':               'ER_Icon_Sorcery_Gavel_of_Haima.png',
  'glintstone_icecrag_sorcery_elden_ring_wiki_guide':           'ER_Icon_Sorcery_Glintstone_Icecrag.png',
  'glintstone_pebble_sorcery_elden_ring_wiki_guide':            'ER_Icon_Sorcery_Glintstone_Pebble.png',
  'gravity_well_sorcery_elden_ring_wiki_guide':                 'ER_Icon_Sorcery_Gravity_Well.png',
  'greatblade_phalanx_sorcery_elden_ring_wiki_guide':           'ER_Icon_Sorcery_Greatblade_Phalanx.png',
  'lorettas_greatbow_sorcery_elden_ring_wiki_guide':            'ER_Icon_Sorcery_Loretta\'s_Greatbow.png',
  'lorettas_mastery_sorcery_elden_ring_wiki_guide':             'ER_Icon_Sorcery_Loretta\'s_Mastery.png',
  'magic_downpour_sorcery_elden_ring_wiki_guide':               'ER_Icon_Sorcery_Magic_Downpour.png',
  'meteorite_sorcery_elden_ring_wiki_guide':                    'ER_Icon_Sorcery_Meteorite.png',
  'meteorite_of_astel_sorcery_elden_ring_wiki_guide':           'ER_Icon_Sorcery_Meteorite_of_Astel.png',
  'night_comet_sorcery_elden_ring_wiki_guide':                  'ER_Icon_Sorcery_Night_Comet.png',
  'night_shard_sorcery_elden_ring_wiki_guide':                  'ER_Icon_Sorcery_Night_Shard.png',
  'oracle_bubbles_sorcery_elden_ring_wiki_guide':               'ER_Icon_Sorcery_Oracle_Bubbles.png',
  'rannis_dark_moon_sorcery_elden_ring_wiki_guide':             'ER_Icon_Sorcery_Ranni\'s_Dark_Moon.png',
  'rennalas_full_moon_sorcery_elden_ring_wiki_guide':           'ER_Icon_Sorcery_Rennala\'s_Full_Moon.png',
  'rock_sling_sorcery_elden_ring_wiki_guide':                   'ER_Icon_Sorcery_Rock_Sling.png',
  'stars_of_ruin_sorcery_elden_ring_wiki_guide':                'ER_Icon_Sorcery_Stars_of_Ruin.png',
  'terra_magica_sorcery_elden_ring_wiki_guide':                 'ER_Icon_Sorcery_Terra_Magica.png',
  'vortex_of_lunacy_sorcery_elden_ring_wiki_guide':             'ER_Icon_Sorcery_Vortex_of_Lunacy.png',
  'miriams_vanishing_sorcery_elden_ring_wiki_guide':            'ER_Icon_Sorcery_Miriam\'s_Vanishing.png',
  'trinas_mist_sorcery_elden_ring_wiki_guide':                  'ER_Icon_Sorcery_St._Trina\'s_Mist.png',
},
'incantations': {
  'ancient_dragons_lightning_spear_incantation_elden_ring_wiki_guide':    'ER_Icon_Incantation_Ancient_Dragons\'_Lightning_Spear.png',
  'aspects_of_the_crucible_breath_incantation_elden_ring_wiki_guide':     'ER_Icon_Incantation_Aspects_of_the_Crucible_Breath.png',
  'aspects_of_the_crucible_horns_incantation_elden_ring_wiki_guide':      'ER_Icon_Incantation_Aspects_of_the_Crucible_Horns.png',
  'aspects_of_the_crucible_tail_incantation_elden_ring_wiki_guide':       'ER_Icon_Incantation_Aspects_of_the_Crucible_Tail.png',
  'barrier_of_gold_incantation_elden_ring_wiki_guide':                    'ER_Icon_Incantation_Barrier_of_Gold.png',
  'black_blade_incantation_elden_ring_wiki_guide':                        'ER_Icon_Incantation_Black_Blade.png',
  'black_flame_incantation_elden_ring_wiki_guide':                        'ER_Icon_Incantation_Black_Flame.png',
  'black_flame_blade_incantation_elden_ring_wiki_guide':                  'ER_Icon_Incantation_Black_Flame_Blade.png',
  'bloodboon_incantation_elden_ring_wiki_guide':                          'ER_Icon_Incantation_Bloodboon.png',
  'bloodflame_blade_incantation_elden_ring_wiki_guide':                   'ER_Icon_Incantation_Bloodflame_Blade.png',
  'bloodflame_talons_incantation_elden_ring_wiki_guide':                  'ER_Icon_Incantation_Bloodflame_Talons.png',
  'burn_o_flame_incantation_elden_ring_wiki_guide':                       'ER_Icon_Incantation_Burn,_O_Flame!.png',
  'catch_flame_incantation_elden_ring_wiki_guide':                        'ER_Icon_Incantation_Catch_Flame.png',
  'dragonfire_incantation_elden_ring_wiki_guide':                         'ER_Icon_Incantation_Dragonfire.png',
  'dragonmaw_incantation_elden_ring_wiki_guide':                          'ER_Icon_Incantation_Dragonmaw.png',
  'elden_stars_incantation_elden_ring_wiki_guide':                        'ER_Icon_Incantation_Elden_Stars.png',
  'electrify_armament_incantation_elden_ring_wiki_guide':                 'ER_Icon_Incantation_Electrify_Armament.png',
  'erdtree_heal_incantation_elden_ring_wiki_guide':                       'ER_Icon_Incantation_Erdtree_Heal.png',
  'flame_of_the_fell_god_incantation_elden_ring_wiki_guide':              'ER_Icon_Incantation_Flame_of_the_Fell_God.png',
  'flame_sling_incantation_elden_ring_wiki_guide':                        'ER_Icon_Incantation_Flame_Sling.png',
  'flame_grant_me_strength_incantation_elden_ring_wiki_guide':            'ER_Icon_Incantation_Flame,_Grant_Me_Strength.png',
  'fortissaxs_lightning_spear_incantation_elden_ring_wiki_guide':         'ER_Icon_Incantation_Fortissax\'s_Lightning_Spear.png',
  'frenzied_burst_incantation_elden_ring_wiki_guide':                     'ER_Icon_Incantation_Frenzied_Burst.png',
  'giant_flame_shrouding_incantation_elden_ring_wiki_guide':              'ER_Icon_Incantation_Giant_Flame_Shrouding.png',
  'giantsflame_take_thee_incantation_elden_ring_wiki_guide':              'ER_Icon_Incantation_Giantsflame_Take_Thee.png',
  'golden_vow_incantation_elden_ring_wiki_guide':                         'ER_Icon_Incantation_Golden_Vow.png',
  'greyolls_roar_incantation_elden_ring_wiki_guide':                      'ER_Icon_Incantation_Greyoll\'s_Roar.png',
  'howl_of_shabriri_incantation_elden_ring_wiki_guide':                   'ER_Icon_Incantation_Howl_of_Shabriri.png',
  'inescapable_frenzy_incantation_elden_ring_wiki_guide':                 'ER_Icon_Incantation_Inescapable_Frenzy.png',
  'law_of_causality_incantation_elden_ring_wiki_guide':                   'ER_Icon_Incantation_Law_of_Causality.png',
  'lightning_spear_incantation_elden_ring_wiki_guide':                    'ER_Icon_Incantation_Lightning_Spear.png',
  'litany_of_proper_death_incantation_elden_ring_wiki_guide':             'ER_Icon_Incantation_Litany_of_Proper_Death.png',
  'lords_heal_incantation_elden_ring_wiki_guide':                         'ER_Icon_Incantation_Lord\'s_Heal.png',
  'o_flame_incantation_elden_ring_wiki_guide':                            'ER_Icon_Incantation_O,_Flame!.png',
  'pest_threads_incantation_elden_ring_wiki_guide':                       'ER_Icon_Incantation_Pest_Threads.png',
  'placidusaxs_ruin_incantation_elden_ring_wiki_guide':                   'ER_Icon_Incantation_Placidusax\'s_Ruin.png',
  'poison_armament_incantation_elden_ring_wiki_guide':                    'ER_Icon_Incantation_Poison_Armament.png',
  'rotten_breath_incantation_elden_ring_wiki_guide':                      'ER_Icon_Incantation_Rotten_Breath.png',
  'scarlet_aeonia_incantation_elden_ring_wiki_guide':                     'ER_Icon_Incantation_Scarlet_Aeonia.png',
  'shadows_of_death_incantation_elden_ring_wiki_guide':                   'ER_Icon_Incantation_Shadows_of_Death.png',
  'stone_of_gurranq_incantation_elden_ring_wiki_guide':                   'ER_Icon_Incantation_Stone_of_Gurranq.png',
  'swarm_of_flies_incantation_elden_ring_wiki_guide':                     'ER_Icon_Incantation_Swarm_of_Flies.png',
  'the_flame_of_frenzy_incantation_elden_ring_wiki_guide':                'ER_Icon_Incantation_The_Flame_of_Frenzy.png',
  'thunderbolt_incantation_elden_ring_wiki_guide':                        'ER_Icon_Incantation_Thunderbolt.png',
  'urgent_heal_incantation_elden_ring_wiki_guide':                        'ER_Icon_Incantation_Urgent_Heal.png',
  'vykes_dragonbolt_incantation_elden_ring_wiki_guide':                   'ER_Icon_Incantation_Vyke\'s_Dragonbolt.png',
  'wrath_of_gold_incantation_elden_ring_wiki_guide':                      'ER_Icon_Incantation_Wrath_of_Gold.png',
  'darkness_incantation_elden_ring_wiki_guide':                           'ER_Icon_Incantation_Darkness.png',
  'frenzied_eruption_incantation_elden_ring_wiki_guide':                  'ER_Icon_Incantation_Frenzied_Eruption.png',
  'mass_of_putrescence_incantation_elden_ring_wiki_guide':                'ER_Icon_Incantation_Mass_of_Putrescence.png',
},
'spiritashes': {
  'ancient_dragon_knight_kristoff_ashes_spirit_elden_ring_wiki_guide':    'ER_Icon_SpiritAsh_Ancient_Dragon_Knight_Kristoff_Ashes.png',
  'banished_knight_oleg_ashes_spirit_elden_ring_wiki_guide':              'ER_Icon_SpiritAsh_Banished_Knight_Oleg_Ashes.png',
  'black_knife_tiche_spirit_ashes_elden_ring_wiki_guide':                 'ER_Icon_SpiritAsh_Black_Knife_Tiche_Ashes.png',
  'cleanrot_knight_finlay_spirit_ashes_elden_ring_wiki_guide':            'ER_Icon_SpiritAsh_Cleanrot_Knight_Finlay_Ashes.png',
  'divine_bird_warrior_ashes_spirit_elden_ring_wiki_guide':               'ER_Icon_SpiritAsh_Divine_Bird_Warrior_Ashes.png',
  'dung_eater_puppet_spirit_ashes_elden_ring_wiki_guide':                 'ER_Icon_SpiritAsh_Dung_Eater_Puppet_Ashes.png',
  'fanged_imp_ashes_spirit_elden_ring_wiki_guide':                        'ER_Icon_SpiritAsh_Fanged_Imp_Ashes.png',
  'fire_prelate_spirit_ashes_elden_ring_wiki_guide':                      'ER_Icon_SpiritAsh_Fire_Prelate_Ashes.png',
  'greatshield_soldier_ashes_spirit_elden_ring_wiki_guide':               'ER_Icon_SpiritAsh_Greatshield_Soldier_Ashes.png',
  'horned_warrior_ashes_spirit_elden_ring_wiki_guide':                    'ER_Icon_SpiritAsh_Horned_Warrior_Ashes.png',
  'jellyfish_spirit_ashes_elden_ring_wiki_guide':                         'ER_Icon_SpiritAsh_Jellyfish_Ashes.png',
  'knight_bernahl_ashes_spirit_elden_ring_wiki_guide':                    'ER_Icon_SpiritAsh_Knight_Bernahl_Ashes.png',
  'lhutel_the_headless_spirit_ashes_elden_ring_wiki_guide':               'ER_Icon_SpiritAsh_Lhutel_the_Headless_Ashes.png',
  'lone_wolf_ashes_spirit_elden_ring_wiki_guide':                         'ER_Icon_SpiritAsh_Lone_Wolf_Ashes.png',
  'messmer_soldier_ashes_spirit_elden_ring_wiki_guide':                   'ER_Icon_SpiritAsh_Messmer_Soldier_Ashes.png',
  'mimic_tear_ashes_spirit_elden_ring_wiki_guide':                        'ER_Icon_SpiritAsh_Mimic_Tear_Ashes.png',
  'nightmaiden_and_swordstress_ashes_spirit_elden_ring_wiki_guide':       'ER_Icon_SpiritAsh_Nightmaiden_%26_Swordstress_Ashes.png',
  'omenkiller_rollo_spirit_ashes_elden_ring_wiki_guide':                  'ER_Icon_SpiritAsh_Omenkiller_Rollo_Ashes.png',
  'perfumer_tricia_spirit_ashes_elden_ring_wiki_guide':                   'ER_Icon_SpiritAsh_Perfumer_Tricia_Ashes.png',
  'redmane_knight_ogha_spirit_ashes_elden_ring_wiki_guide':               'ER_Icon_SpiritAsh_Redmane_Knight_Ogha_Ashes.png',
  'skeletal_bandit_ashes_spirit_elden_ring_wiki_guide':                   'ER_Icon_SpiritAsh_Skeletal_Bandit_Ashes.png',
  'soldjars_of_fortune_spirit_ashes_elden_ring_wiki_guide':               'ER_Icon_SpiritAsh_Soldjars_of_Fortune_Ashes.png',
  'spirit_jellyfish_ashes_spirit_elden_ring_wiki_guide':                  'ER_Icon_SpiritAsh_Spirit_Jellyfish_Ashes.png',
  'stormhawk_deenh_spirit_ashes_elden_ring_wiki_guide':                   'ER_Icon_SpiritAsh_Stormhawk_Deenh_Ashes.png',
  'twinsage_sorcerer_spirit_ashes_elden_ring_wiki_guide':                 'ER_Icon_SpiritAsh_Twinsage_Sorcerer_Ashes.png',
  'avionette_soldier_ashes_spirit_elden_ring_wiki_guide':                 'ER_Icon_SpiritAsh_Avionette_Soldier_Ashes.png',
  'wandering_noble_ashes_spirit_elden_ring_wiki_guide':                   'ER_Icon_SpiritAsh_Wandering_Noble_Ashes.png',
},
'shields': {
  'brass_shield_shields_elden_ring_wiki_guide':                   'ER_Icon_Shield_Brass_Shield.png',
  'dragon_towershield_shields_elden_ring_wiki_guide':             'ER_Icon_Shield_Dragon_Towershield.png',
  'eclipse_crest_heater_shield_shields_elden_ring_wiki_guide':    'ER_Icon_Shield_Eclipse_Crest_Heater_Shield.png',
  'erdtree_greatshield_shields_elden_ring_wiki_guide':            'ER_Icon_Shield_Erdtree_Greatshield.png',
  'golden_epitaph_straight_sword_weapon':                         'ER_Icon_Weapon_Golden_Epitaph.png',
  'haligtree_crest_greatshield_shields_elden_ring_wiki_guide':    'ER_Icon_Shield_Haligtree_Crest_Greatshield.png',
  'jellyfish_shield_shields_elden_ring_wiki_guide':               'ER_Icon_Shield_Jellyfish_Shield.png',
  'one-eyed_shield_shields_elden_ring_wiki_guide':                'ER_Icon_Shield_One-Eyed_Shield.png',
  'scorpion_kite_shield_shields_elden_ring_wiki_guide':           'ER_Icon_Shield_Scorpion_Kite_Shield.png',
  'shield_of_the_guilty_shields_elden_ring_wiki_guide':           'ER_Icon_Shield_Shield_of_the_Guilty.png',
  'silver_mirrorshield_shields_elden_ring_wiki_guide':            'ER_Icon_Shield_Silver_Mirrorshield.png',
  'stone-sheathed_sword_straight_sword_weapon':                   'ER_Icon_Weapon_Stone-Sheathed_Sword.png',
  'visage_shield_shields_elden_ring_wiki_guide':                  'ER_Icon_Shield_Visage_Shield.png',
  'blue-gold_kite_shield_shields_elden_ring_wiki_guide':          'ER_Icon_Shield_Blue-Gold_Kite_Shield.png',
  'pearl_shield_shields_elden_ring_wiki_guide':                   'ER_Icon_Shield_Pearl_Shield.png',
},
}

def download(url, dest):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=12) as r:
        ct = r.headers.get('content-type', '')
        if 'image' not in ct and 'octet' not in ct:
            raise ValueError(f"Wrong content-type: {ct}")
        data = r.read()
        if len(data) < 100:
            raise ValueError("File too small, likely error page")
        with open(dest, 'wb') as f:
            f.write(data)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    total = sum(len(v) for v in ITEMS.values())
    done = 0
    failed = []

    print(f"Downloading {total} images from eldenring.wiki.gg...\n")

    for cat, mapping in ITEMS.items():
        folder = os.path.join(script_dir, 'images', cat)
        os.makedirs(folder, exist_ok=True)

        for slug, wiki_fname in mapping.items():
            dest = os.path.join(folder, slug + '.png')
            if os.path.exists(dest):
                done += 1
                continue
            url = WIKI_BASE + wiki_fname
            try:
                download(url, dest)
                done += 1
                print(f"[{done}/{total}] OK  {slug[:55]}")
            except Exception as e:
                # Try alternate: replace apostrophes with %27
                url2 = WIKI_BASE + wiki_fname.replace("'", "%27")
                try:
                    download(url2, dest)
                    done += 1
                    print(f"[{done}/{total}] OK' {slug[:55]}")
                except Exception as e2:
                    failed.append((cat, slug, wiki_fname, str(e2)[:50]))
                    print(f"  FAIL {slug[:55]} → {str(e2)[:50]}")
            time.sleep(0.12)

    print(f"\n{'='*60}")
    print(f"Done: {done}/{total} downloaded")
    if failed:
        print(f"Failed ({len(failed)}):")
        for cat, slug, fname, err in failed:
            print(f"  {cat}/{slug}: {err}")
        print("\nPer i file falliti, prova a scaricarli manualmente da:")
        print("  https://eldenring.wiki.gg/wiki/Special:Search")
        print("  Cerca il nome dell'item e salva l'immagine in images/<categoria>/<slug>.png")
    else:
        print("Tutte le immagini scaricate con successo!")

if __name__ == '__main__':
    main()
