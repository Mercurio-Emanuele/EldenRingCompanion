#!/usr/bin/env python3
"""
Elden Ring Tracker — Image Downloader
======================================
Scarica tutte le immagini degli item da eldenring.wiki.fextralife.com
e le salva nella cartella /images/ accanto ai file HTML.

Uso:
  pip install requests Pillow
  python3 download_images.py

Poi carica la cartella /images/ su GitHub insieme agli HTML.
"""

import os, time, re, sys, urllib.request, urllib.error

BASE_URL = "https://eldenring.wiki.fextralife.com/file/Elden-Ring/"

def get_url(slug):
    if '_elden_ring_wiki_guide' in slug:
        return BASE_URL + slug + '_200px.png'
    if slug.endswith('_elden_ring_wiki'):
        return BASE_URL + slug + '_guide_200px.png'
    return BASE_URL + slug + '_elden_ring_wiki_guide_200px.png'

# All item slugs organised by category
ITEMS = {
'talismans': [
  'ancestral_spirits_horn_talisman','arrows_reach_talisman','arrows_soaring_sting_talisman',
  'arsenal_charm_talisman','arsenal_charm_1_talisman','assassins_cerulean_dagger_talisman',
  'assassins_crimson_dagger_talisman','axe_talisman','beloved_stardust_talisman',
  'blade_of_mercy_talisman','blessed_blue_dew_talisman','blessed_dew_talisman',
  'blue_dancer_charm_talisman','blue-feathered_branchsword_talisman','boltdrake_talisman',
  'boltdrake_talisman_1','boltdrake_talisman_2','boltdrake_talisman_3',
  'bull-goats_talisman','cerulean_amber_medallion_talisman','cerulean_amber_medallion_1_talisman',
  'cerulean_amber_medallion_2_talisman','cerulean_amber_medallion_3_talisman',
  'cerulean_seed_talisman','cerulean_seed_talisman_1','claw_talisman','concealing_veil_talisman',
  'crimson_amber_medallion_talisman','crimson_amber_medallion_1_talisman',
  'crimson_amber_medallion_2_talisman','crimson_amber_medallion_3_talisman',
  'crimson_seed_talisman','crimson_seed_talisman_1','crusade_insignia_talisman',
  'dagmar_greatshield_talisman','dragoncrest_greatshield_talisman','dragoncrest_shield_talisman',
  'dragoncrest_shield_talisman_1','dragoncrest_shield_talisman_2','dried_bouquet_talisman',
  'erdtrees_favor_talisman','erdtrees_favor_1_talisman','erdtrees_favor_2_talisman',
  'fine_crucible_feather_talisman','flamedrake_talisman','flamedrake_talisman_1',
  'flamedrake_talisman_2','flamedrake_talisman_3','flocks_canvas_talisman',
  'godfrey_icon_talisman','godskin_swaddling_cloth_talisman','gold_scarab_talisman',
  'golden_braid_talisman','graven-mass_talisman','graven-school_talisman',
  'great-jars_arsenal_talisman','green_turtle_talisman','haligdrake_talisman',
  'haligdrake_talisman_1','haligdrake_talisman_2','kindred_of_rots_exultation_talisman',
  'lacerating_crossed-tree_talisman','lord_of_bloods_exultation_talisman',
  'magic_scorpion_charm_talisman','marikas_scarseal_talisman','marikas_soreseal_talisman',
  'millicents_prosthesis_talisman','moon_of_nokstella_talisman','mottled_necklace_talisman',
  'mottled_necklace_1_talisman','mottled_necklace_2_talisman','old_lords_talisman',
  'outer_god_heirloom_talisman','pearl_shield_talisman','pearldrake_talisman',
  'pearldrake_talisman_1','pearldrake_talisman_2','pearldrake_talisman_3',
  'prosthesis-wearer_heirloom_talisman','radagon_icon_talisman','radagons_scarseal_talisman',
  'radagons_soreseal_talisman','red-feathered_branchsword_talisman','rellanas_cameo_talisman',
  'retaliatory_crossed-tree_talisman','ritual_shield_talisman','ritual_sword_talisman',
  'sacred_scorpion_charm_talisman','shabriris_woe_talisman','shard_of_alexander_talisman',
  'sharpshot_talisman','silver_scarab_talisman','smithing_talisman','spear_talisman',
  'spelldrake_talisman','spelldrake_talisman_1','spelldrake_talisman_2','spelldrake_talisman_3',
  'st_trinas_smile_talisman','stalwart_horn_charm_talisman','stalwart_horn_charm_1_talisman',
  'stalwart_horn_charm_2_talisman','stargazer_heirloom_talisman','starscourge_heirloom_talisman',
  'talisman_of_all_crucibles_talisman','talisman_of_lords_bestowal_talisman',
  'takers_cameo_talisman','two_fingers_heirloom_talisman','two-handed_sword_talisman',
  'two-headed_turtle_talisman','verdigris_discus_talisman','viridian_amber_medallion_talisman',
  'viridian_amber_medallion_1_talisman','viridian_amber_medallion_2_talisman',
  'viridian_amber_medallion_3_talisman','warrior_jar_shard_talisman',
  'white-feathered_branchsword_talisman','winged_sword_insignia_talisman',
],
'weapons': [
  'blasphemous_blade_greatsword_weapon','black_knife_dagger_weapon',
  'bloodhounds_fang_curved_greatsword_weapon','bolt_of_gransax_spear_weapon',
  'claymore_greatsword_weapon','coded_sword_straight_sword_weapon',
  'commanders_standard_halberd_weapon','cross-naginata_spear_weapon',
  'deaths_poker_greatsword_weapon','dragon_kings_cragblade_heavy_thrusting_sword_weapon',
  'dragonscale_blade_katana_weapon','eclipse_shotel_curved_sword_weapon',
  'fallingstar_beast_jaw_colossal_weapon_weapon','flamberge_greatsword_weapon',
  'godslayers_greatsword_colossal_sword_weapon','golden_order_greatsword_weapon',
  'grafted_blade_greatsword_colossal_sword_weapon','greatsword_colossal_sword_weapon',
  'hand_of_malenia_katana_weapon','loretta_war_sickle_halberd_weapon',
  'malikeths_black_blade_colossal_sword_weapon','marais_executioners_sword_colossal_sword_weapon',
  'meteoric_ore_blade_katana_weapon','misericorde_dagger_weapon','mohgwyns_sacred_spear_weapon',
  'moonveil_katana_weapon','morgotts_cursed_sword_curved_greatsword_weapon',
  'nagakiba_katana_weapon','reduvia_dagger_weapon','rivers_of_blood_katana_weapon',
  'ruins_greatsword_colossal_sword_weapon','sacred_relic_sword_greatsword_weapon',
  'starscourge_greatsword_colossal_sword_weapon','sword_of_night_and_flame_straight_sword_weapon',
  'treespear_spear_weapon','uchigatana_katana_weapon','winged_scythe_reaper_weapon',
  'euporia_twinblade_weapon','sword_of_night_straight_sword_weapon',
],
'armor': [
  'answbachs_helm_armor_elden_ring_wiki','answbachs_armor_elden_ring_wiki',
  'answbachs_gauntlets_armor_elden_ring_wiki','answbachs_greaves_armor_elden_ring_wiki',
  'black_knife_hood_armor_elden_ring_wiki','black_knife_armor_elden_ring_wiki',
  'black_knife_gauntlets_armor_elden_ring_wiki','black_knife_greaves_armor_elden_ring_wiki',
  'blaids_helm_armor_elden_ring_wiki','blaids_armor_elden_ring_wiki',
  'blaids_gauntlets_armor_elden_ring_wiki','blaids_greaves_armor_elden_ring_wiki',
  'bull-goat_helm_armor_elden_ring_wiki','bull-goat_armor_elden_ring_wiki',
  'bull-goat_gauntlets_armor_elden_ring_wiki','bull-goat_greaves_armor_elden_ring_wiki',
  'crucible_axe_helm_armor_elden_ring_wiki','crucible_axe_armor_elden_ring_wiki',
  'crucible_axe_gauntlets_armor_elden_ring_wiki','crucible_axe_greaves_armor_elden_ring_wiki',
  'fire_knight_helm_armor_elden_ring_wiki','fire_knight_armor_elden_ring_wiki',
  'fire_knight_gauntlets_armor_elden_ring_wiki','fire_knight_greaves_armor_elden_ring_wiki',
  'malenias_helm_armor_elden_ring_wiki','malenias_armor_elden_ring_wiki',
  'malenias_gauntlet_armor_elden_ring_wiki','malenias_greaves_armor_elden_ring_wiki',
  'raging_wolf_helm_armor_elden_ring_wiki','raging_wolf_armor_elden_ring_wiki',
  'raging_wolf_gauntlets_armor_elden_ring_wiki','raging_wolf_greaves_armor_elden_ring_wiki',
  'radahns_lion_helm_armor_elden_ring_wiki','radahns_lion_armor_elden_ring_wiki',
  'veterans_helm_armor_elden_ring_wiki','veterans_armor_elden_ring_wiki',
  'veterans_gauntlets_armor_elden_ring_wiki','veterans_greaves_armor_elden_ring_wiki',
  'white_reed_helm_armor_elden_ring_wiki','white_reed_armor_elden_ring_wiki',
  'white_reed_gauntlets_armor_elden_ring_wiki','white_reed_greaves_armor_elden_ring_wiki',
],
'sorceries': [
  'adulas_moonblade_sorcery_elden_ring_wiki_guide','cannon_of_haima_sorcery_elden_ring_wiki_guide',
  'carian_greatsword_sorcery_elden_ring_wiki_guide','carian_phalanx_sorcery_elden_ring_wiki_guide',
  'carian_piercer_sorcery_elden_ring_wiki_guide','carian_retaliation_sorcery_elden_ring_wiki_guide',
  'carian_slicer_sorcery_elden_ring_wiki_guide','comet_sorcery_elden_ring_wiki_guide',
  'comet_azur_sorcery_elden_ring_wiki_guide','crystal_torrent_sorcery_elden_ring_wiki_guide',
  'eternal_darkness_sorcery_elden_ring_wiki_guide','founding_rain_of_stars_sorcery_elden_ring_wiki_guide',
  'freezing_mist_sorcery_elden_ring_wiki_guide','full_moon_of_nokstella_sorcery_elden_ring_wiki_guide',
  'gavel_of_haima_sorcery_elden_ring_wiki_guide','glintstone_icecrag_sorcery_elden_ring_wiki_guide',
  'glintstone_pebble_sorcery_elden_ring_wiki_guide','gravity_well_sorcery_elden_ring_wiki_guide',
  'greatblade_phalanx_sorcery_elden_ring_wiki_guide','lorettas_greatbow_sorcery_elden_ring_wiki_guide',
  'lorettas_mastery_sorcery_elden_ring_wiki_guide','magic_downpour_sorcery_elden_ring_wiki_guide',
  'meteorite_sorcery_elden_ring_wiki_guide','meteorite_of_astel_sorcery_elden_ring_wiki_guide',
  'night_comet_sorcery_elden_ring_wiki_guide','night_shard_sorcery_elden_ring_wiki_guide',
  'oracle_bubbles_sorcery_elden_ring_wiki_guide','rannis_dark_moon_sorcery_elden_ring_wiki_guide',
  'rennalas_full_moon_sorcery_elden_ring_wiki_guide','rock_sling_sorcery_elden_ring_wiki_guide',
  'stars_of_ruin_sorcery_elden_ring_wiki_guide','terra_magica_sorcery_elden_ring_wiki_guide',
  'vortex_of_lunacy_sorcery_elden_ring_wiki_guide','miriams_vanishing_sorcery_elden_ring_wiki_guide',
  'trinas_mist_sorcery_elden_ring_wiki_guide',
],
'incantations': [
  'ancient_dragons_lightning_spear_incantation_elden_ring_wiki_guide',
  'aspects_of_the_crucible_breath_incantation_elden_ring_wiki_guide',
  'aspects_of_the_crucible_horns_incantation_elden_ring_wiki_guide',
  'aspects_of_the_crucible_tail_incantation_elden_ring_wiki_guide',
  'barrier_of_gold_incantation_elden_ring_wiki_guide','black_blade_incantation_elden_ring_wiki_guide',
  'black_flame_incantation_elden_ring_wiki_guide','black_flame_blade_incantation_elden_ring_wiki_guide',
  'bloodboon_incantation_elden_ring_wiki_guide','bloodflame_blade_incantation_elden_ring_wiki_guide',
  'bloodflame_talons_incantation_elden_ring_wiki_guide','burn_o_flame_incantation_elden_ring_wiki_guide',
  'catch_flame_incantation_elden_ring_wiki_guide','dragonfire_incantation_elden_ring_wiki_guide',
  'dragonmaw_incantation_elden_ring_wiki_guide','elden_stars_incantation_elden_ring_wiki_guide',
  'electrify_armament_incantation_elden_ring_wiki_guide','erdtree_heal_incantation_elden_ring_wiki_guide',
  'flame_of_the_fell_god_incantation_elden_ring_wiki_guide','flame_sling_incantation_elden_ring_wiki_guide',
  'flame_grant_me_strength_incantation_elden_ring_wiki_guide',
  'fortissaxs_lightning_spear_incantation_elden_ring_wiki_guide',
  'frenzied_burst_incantation_elden_ring_wiki_guide',
  'giant_flame_shrouding_incantation_elden_ring_wiki_guide',
  'giantsflame_take_thee_incantation_elden_ring_wiki_guide',
  'golden_vow_incantation_elden_ring_wiki_guide','greyolls_roar_incantation_elden_ring_wiki_guide',
  'howl_of_shabriri_incantation_elden_ring_wiki_guide',
  'inescapable_frenzy_incantation_elden_ring_wiki_guide',
  'law_of_causality_incantation_elden_ring_wiki_guide','lightning_spear_incantation_elden_ring_wiki_guide',
  'litany_of_proper_death_incantation_elden_ring_wiki_guide',
  'lords_heal_incantation_elden_ring_wiki_guide','o_flame_incantation_elden_ring_wiki_guide',
  'pest_threads_incantation_elden_ring_wiki_guide','placidusaxs_ruin_incantation_elden_ring_wiki_guide',
  'poison_armament_incantation_elden_ring_wiki_guide','rotten_breath_incantation_elden_ring_wiki_guide',
  'scarlet_aeonia_incantation_elden_ring_wiki_guide','shadows_of_death_incantation_elden_ring_wiki_guide',
  'stone_of_gurranq_incantation_elden_ring_wiki_guide','swarm_of_flies_incantation_elden_ring_wiki_guide',
  'the_flame_of_frenzy_incantation_elden_ring_wiki_guide','thunderbolt_incantation_elden_ring_wiki_guide',
  'urgent_heal_incantation_elden_ring_wiki_guide','vykes_dragonbolt_incantation_elden_ring_wiki_guide',
  'wrath_of_gold_incantation_elden_ring_wiki_guide','darkness_incantation_elden_ring_wiki_guide',
  'frenzied_eruption_incantation_elden_ring_wiki_guide',
  'mass_of_putrescence_incantation_elden_ring_wiki_guide',
],
'spiritashes': [
  'ancient_dragon_knight_kristoff_ashes_spirit_elden_ring_wiki_guide',
  'banished_knight_oleg_ashes_spirit_elden_ring_wiki_guide',
  'black_knife_tiche_spirit_ashes_elden_ring_wiki_guide',
  'cleanrot_knight_finlay_spirit_ashes_elden_ring_wiki_guide',
  'divine_bird_warrior_ashes_spirit_elden_ring_wiki_guide',
  'dung_eater_puppet_spirit_ashes_elden_ring_wiki_guide',
  'fanged_imp_ashes_spirit_elden_ring_wiki_guide','fire_prelate_spirit_ashes_elden_ring_wiki_guide',
  'greatshield_soldier_ashes_spirit_elden_ring_wiki_guide',
  'horned_warrior_ashes_spirit_elden_ring_wiki_guide','jellyfish_spirit_ashes_elden_ring_wiki_guide',
  'knight_bernahl_ashes_spirit_elden_ring_wiki_guide',
  'lhutel_the_headless_spirit_ashes_elden_ring_wiki_guide',
  'lone_wolf_ashes_spirit_elden_ring_wiki_guide','messmer_soldier_ashes_spirit_elden_ring_wiki_guide',
  'mimic_tear_ashes_spirit_elden_ring_wiki_guide',
  'nightmaiden_and_swordstress_ashes_spirit_elden_ring_wiki_guide',
  'omenkiller_rollo_spirit_ashes_elden_ring_wiki_guide',
  'perfumer_tricia_spirit_ashes_elden_ring_wiki_guide',
  'redmane_knight_ogha_spirit_ashes_elden_ring_wiki_guide',
  'skeletal_bandit_ashes_spirit_elden_ring_wiki_guide',
  'soldjars_of_fortune_spirit_ashes_elden_ring_wiki_guide',
  'spirit_jellyfish_ashes_spirit_elden_ring_wiki_guide',
  'stormhawk_deenh_spirit_ashes_elden_ring_wiki_guide',
  'twinsage_sorcerer_spirit_ashes_elden_ring_wiki_guide',
  'avionette_soldier_ashes_spirit_elden_ring_wiki_guide',
  'wandering_noble_ashes_spirit_elden_ring_wiki_guide',
],
'shields': [
  'brass_shield_shields_elden_ring_wiki_guide',
  'dragon_towershield_shields_elden_ring_wiki_guide',
  'eclipse_crest_heater_shield_shields_elden_ring_wiki_guide',
  'erdtree_greatshield_shields_elden_ring_wiki_guide','golden_epitaph_straight_sword_weapon',
  'haligtree_crest_greatshield_shields_elden_ring_wiki_guide',
  'jellyfish_shield_shields_elden_ring_wiki_guide','one-eyed_shield_shields_elden_ring_wiki_guide',
  'scorpion_kite_shield_shields_elden_ring_wiki_guide',
  'shield_of_the_guilty_shields_elden_ring_wiki_guide',
  'silver_mirrorshield_shields_elden_ring_wiki_guide','stone-sheathed_sword_straight_sword_weapon',
  'visage_shield_shields_elden_ring_wiki_guide','blue-gold_kite_shield_shields_elden_ring_wiki_guide',
  'pearl_shield_shields_elden_ring_wiki_guide',
],
}

def get_url(slug):
    base = 'https://eldenring.wiki.fextralife.com/file/Elden-Ring/'
    if '_elden_ring_wiki_guide' in slug:
        return base + slug + '_200px.png'
    if slug.endswith('_elden_ring_wiki'):
        return base + slug + '_guide_200px.png'
    return base + slug + '_elden_ring_wiki_guide_200px.png'

total = sum(len(v) for v in ITEMS.values())
downloaded = 0
failed = []

script_dir = os.path.dirname(os.path.abspath(__file__))
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://eldenring.wiki.fextralife.com/Elden-Ring-Wiki',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'sec-fetch-dest': 'image',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-origin',
}

print(f"Downloading {total} images...")
for cat, slugs in ITEMS.items():
    folder = os.path.join(script_dir, 'images', cat)
    os.makedirs(folder, exist_ok=True)
    for slug in slugs:
        out_path = os.path.join(folder, slug + '.png')
        if os.path.exists(out_path):
            downloaded += 1
            continue
        url = get_url(slug)
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                if resp.headers.get('content-type','').startswith('image'):
                    with open(out_path, 'wb') as f:
                        f.write(data)
                    downloaded += 1
                    print(f'  [{downloaded}/{total}] OK: {slug[:50]}')
                else:
                    failed.append((cat, slug, 'wrong content-type'))
                    print(f'  SKIP: {slug[:50]} ({resp.headers.get("content-type","")})')
        except Exception as e:
            failed.append((cat, slug, str(e)))
            print(f'  FAIL: {slug[:50]} — {e}')
        time.sleep(0.15)  # be polite

print(f'\nDone: {downloaded} downloaded, {len(failed)} failed')
if failed:
    print('Failed items:')
    for cat, slug, err in failed[:10]:
        print(f'  {cat}/{slug}: {err}')
